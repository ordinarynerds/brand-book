#!/usr/bin/env python3
"""
svgkit — dependency-free SVG helpers for the brand-book skill.

Brand SVGs (wordmarks, mascot marks, sprite rows of faces/icons) carry their own
absolute coordinates. Cloning them in Paper misplaces them and even/naive slicing
leaves uneven margins. svgkit measures the *real* geometry from the path data so
crops are tight and uniform.

Commands
--------
  clusters  FILE [--gap N] [--n N]
      Detect glyph groups in a horizontal sprite (row of faces/icons) by
      clustering paths on the x-axis. Prints JSON bboxes. Use to sanity-check
      before slice-row.

  slice-row FILE --out DIR --name PREFIX [--n N] [--gap N]
                 [--pad-x 70] [--pad-y 32] [--height 112]
                 [--recolor-from #38353C] [--colors ink=#38353C,white=#FFFFFF]
      Slice a sprite row into N tight, COMMON-HEIGHT slices (so every glyph
      renders at the same size when placed in a fixed-height <img>). Writes
      PREFIX-<i>-<colorname>.svg and prints a JSON of per-glyph display widths
      at --height (feed these straight into the Paper <img> width/height).

  extract   FILE --out FILE [--pick left|right|INDEX] [--pad 8]
                 [--recolor-from "#2E3135,#2F2E33"]
      Pull one glyph out of a multi-glyph SVG (e.g. the mark out of a wordmark)
      into its own tight-viewBox file. `--pick left` = leftmost cluster.

  tight     FILE --out FILE [--pad 6]
      Rewrite the viewBox to the drawn bounds + padding (fixes a mark that sits
      off-centre in an oversized viewBox).

  recolor   FILE --out FILE --map "#2E3135=#38353C,#2F2E33=#38353C"
      Replace fill/stroke hexes. Use to unify a logo to one ink, or emit
      coral / white / off-brand variants.

Notes
-----
* Bounding boxes come from on-curve points + control points, so they slightly
  over-estimate (safe: adds a little padding, never clips the drawing).
* Everything is stdlib only. Renderers (qlmanage/cairosvg) are NOT reliable for
  measuring here — qlmanage squares the canvas and composites transparency to
  black. Parse the vector, don't rasterize.
"""
import re, sys, os, json, argparse

NUM = r'[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?'
ARGC = {'m':2,'l':2,'h':1,'v':1,'c':6,'s':4,'q':4,'t':2,'a':7,'z':0}


def read(path):
    return open(path, 'r', encoding='utf-8').read()


def inner_and_viewbox(svg):
    m = re.search(r'<svg[^>]*>(.*)</svg>', svg, re.S)
    inner = m.group(1) if m else svg
    vb = re.search(r'viewBox="([^"]+)"', svg)
    vb = [float(x) for x in vb.group(1).split()] if vb else None
    return inner, vb


def path_bbox(d):
    toks = re.findall(r'[MmLlHhVvCcSsQqTtAaZz]|' + NUM, d)
    i = 0; cx = cy = sx = sy = 0.0; cmd = None
    mnx = mny = 1e18; mxx = mxy = -1e18
    def upd(x, y):
        nonlocal mnx, mny, mxx, mxy
        mnx = min(mnx, x); mxx = max(mxx, x); mny = min(mny, y); mxy = max(mxy, y)
    while i < len(toks):
        t = toks[i]
        if re.match(r'[A-Za-z]', t):
            cmd = t; i += 1
            if cmd in 'Zz':
                cx, cy = sx, sy
            continue
        c = cmd.lower(); rel = cmd.islower(); n = ARGC[c]
        a = [float(v) for v in toks[i:i+n]]; i += n
        if len(a) < n:
            break
        if c == 'h':
            x = cx + a[0] if rel else a[0]; y = cy; cx = x; upd(x, y)
        elif c == 'v':
            y = cy + a[0] if rel else a[0]; x = cx; cy = y; upd(x, y)
        elif c == 'a':
            x = cx + a[5] if rel else a[5]; y = cy + a[6] if rel else a[6]; cx, cy = x, y; upd(x, y)
        else:
            pts = []
            for k in range(0, n, 2):
                px = a[k] + (cx if rel else 0); py = a[k+1] + (cy if rel else 0)
                pts.append((px, py))
            for (px, py) in pts:
                upd(px, py)
            cx, cy = pts[-1]
            if c == 'm':
                sx, sy = pts[0]
                cmd = 'L' if cmd == 'M' else ('l' if cmd == 'm' else cmd)
    if mnx > mxx:
        return None
    return [mnx, mny, mxx, mxy]


def all_path_bboxes(svg):
    boxes = []
    for d in re.findall(r'\bd="([^"]+)"', svg):
        b = path_bbox(d)
        if b:
            boxes.append(b)
    return boxes


def cluster(boxes, gap=120.0, force_n=None):
    boxes = sorted(boxes, key=lambda b: (b[0] + b[2]) / 2)
    cl = []
    for b in boxes:
        if cl and b[0] <= cl[-1]['x1'] + gap:
            c = cl[-1]
            c['x0'] = min(c['x0'], b[0]); c['x1'] = max(c['x1'], b[2])
            c['y0'] = min(c['y0'], b[1]); c['y1'] = max(c['y1'], b[3])
        else:
            cl.append({'x0': b[0], 'y0': b[1], 'x1': b[2], 'y1': b[3]})
    if force_n:
        # merge nearest neighbours until exactly force_n clusters remain
        while len(cl) > force_n:
            gaps = [(cl[i+1]['x0'] - cl[i]['x1'], i) for i in range(len(cl) - 1)]
            _, i = min(gaps)
            a, b = cl[i], cl[i+1]
            a['x1'] = max(a['x1'], b['x1']); a['y0'] = min(a['y0'], b['y0']); a['y1'] = max(a['y1'], b['y1'])
            del cl[i+1]
    return cl


def recolor_text(svg, mapping):
    for frm, to in mapping.items():
        svg = re.sub(re.escape(frm), to, svg, flags=re.I)
    return svg


def parse_colors(spec):
    out = {}
    for pair in spec.split(','):
        name, hexv = pair.split('=')
        out[name.strip()] = hexv.strip()
    return out


def cmd_clusters(a):
    svg = read(a.file)
    cl = cluster(all_path_bboxes(svg), gap=a.gap, force_n=a.n)
    print(json.dumps({'count': len(cl), 'clusters': cl}, indent=2))


def cmd_slice_row(a):
    svg = read(a.file)
    inner, _ = inner_and_viewbox(svg)
    cl = cluster(all_path_bboxes(svg), gap=a.gap, force_n=a.n)
    gy0 = min(c['y0'] for c in cl); gy1 = max(c['y1'] for c in cl)
    vy0 = gy0 - a.pad_y; vh = (gy1 - gy0) + 2 * a.pad_y
    colors = parse_colors(a.colors)
    os.makedirs(a.out, exist_ok=True)
    widths = {}
    for i, c in enumerate(cl, 1):
        vx0 = c['x0'] - a.pad_x; vw = (c['x1'] - c['x0']) + 2 * a.pad_x
        vb = f'{vx0:.2f} {vy0:.2f} {vw:.2f} {vh:.2f}'
        for name, hexv in colors.items():
            body = re.sub(re.escape(a.recolor_from), hexv, inner, flags=re.I) if a.recolor_from else inner
            out = (f'<svg viewBox="{vb}" width="{vw:.0f}" height="{vh:.0f}" '
                   f'xmlns="http://www.w3.org/2000/svg">{body}</svg>')
            open(os.path.join(a.out, f'{a.name}-{i}-{name}.svg'), 'w').write(out)
        widths[i] = round(a.height * vw / vh, 1)
    print(json.dumps({'count': len(cl), 'height': a.height, 'display_widths': widths}, indent=2))


def cmd_extract(a):
    svg = read(a.file)
    inner, _ = inner_and_viewbox(svg)
    cl = cluster(all_path_bboxes(svg), gap=a.gap)
    if a.pick == 'left':
        c = cl[0]
    elif a.pick == 'right':
        c = cl[-1]
    else:
        c = cl[int(a.pick)]
    x0 = c['x0'] - a.pad; y0 = c['y0'] - a.pad
    w = (c['x1'] - c['x0']) + 2 * a.pad; h = (c['y1'] - c['y0']) + 2 * a.pad
    body = inner
    if a.recolor_from:
        for frm in a.recolor_from.split(','):
            body = re.sub(re.escape(frm.strip()), a.to or frm.strip(), body, flags=re.I)
    out = (f'<svg viewBox="{x0:.2f} {y0:.2f} {w:.2f} {h:.2f}" width="{w:.0f}" height="{h:.0f}" '
           f'xmlns="http://www.w3.org/2000/svg">{body}</svg>')
    open(a.out, 'w').write(out)
    print(json.dumps({'viewBox': [round(x0,2), round(y0,2), round(w,2), round(h,2)], 'out': a.out}))


def cmd_tight(a):
    svg = read(a.file)
    inner, _ = inner_and_viewbox(svg)
    boxes = all_path_bboxes(svg)
    x0 = min(b[0] for b in boxes) - a.pad; y0 = min(b[1] for b in boxes) - a.pad
    x1 = max(b[2] for b in boxes) + a.pad; y1 = max(b[3] for b in boxes) + a.pad
    w = x1 - x0; h = y1 - y0
    out = (f'<svg viewBox="{x0:.2f} {y0:.2f} {w:.2f} {h:.2f}" width="{w:.0f}" height="{h:.0f}" '
           f'xmlns="http://www.w3.org/2000/svg">{inner}</svg>')
    open(a.out, 'w').write(out)
    print(json.dumps({'viewBox': [round(x0,2), round(y0,2), round(w,2), round(h,2)], 'out': a.out}))


def cmd_recolor(a):
    mapping = {}
    for pair in a.map.split(','):
        frm, to = pair.split('=')
        mapping[frm.strip()] = to.strip()
    open(a.out, 'w').write(recolor_text(read(a.file), mapping))
    print(json.dumps({'out': a.out, 'replaced': mapping}))


def main():
    p = argparse.ArgumentParser(prog='svgkit')
    sub = p.add_subparsers(dest='cmd', required=True)

    c = sub.add_parser('clusters'); c.add_argument('file'); c.add_argument('--gap', type=float, default=120.0); c.add_argument('--n', type=int, default=None); c.set_defaults(fn=cmd_clusters)

    s = sub.add_parser('slice-row'); s.add_argument('file'); s.add_argument('--out', required=True); s.add_argument('--name', required=True)
    s.add_argument('--n', type=int, default=None); s.add_argument('--gap', type=float, default=120.0)
    s.add_argument('--pad-x', dest='pad_x', type=float, default=70.0); s.add_argument('--pad-y', dest='pad_y', type=float, default=32.0)
    s.add_argument('--height', type=float, default=112.0); s.add_argument('--recolor-from', dest='recolor_from', default='#38353C')
    s.add_argument('--colors', default='ink=#38353C,white=#FFFFFF'); s.set_defaults(fn=cmd_slice_row)

    e = sub.add_parser('extract'); e.add_argument('file'); e.add_argument('--out', required=True); e.add_argument('--pick', default='left')
    e.add_argument('--pad', type=float, default=8.0); e.add_argument('--gap', type=float, default=120.0)
    e.add_argument('--recolor-from', dest='recolor_from', default=None); e.add_argument('--to', default=None); e.set_defaults(fn=cmd_extract)

    t = sub.add_parser('tight'); t.add_argument('file'); t.add_argument('--out', required=True); t.add_argument('--pad', type=float, default=6.0); t.set_defaults(fn=cmd_tight)

    r = sub.add_parser('recolor'); r.add_argument('file'); r.add_argument('--out', required=True); r.add_argument('--map', required=True); r.set_defaults(fn=cmd_recolor)

    a = p.parse_args()
    a.fn(a)


if __name__ == '__main__':
    main()
