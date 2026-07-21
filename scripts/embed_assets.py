#!/usr/bin/env python3
"""
embed_assets — inline local assets into an HTML file so it becomes a single
self-contained document (required for Claude Artifacts: strict CSP, no external
requests).

Rewrites, to `data:` URIs:
  * <img ... src="local.(svg|png|jpg|webp|gif)">
  * CSS url(local.(woff2|woff|ttf|otf|svg|png|jpg|...))  — covers @font-face and
    background-image, in <style> blocks or inline style="".

Leaves alone anything already a data:/http(s):// / protocol-relative URL.

Usage:
  embed_assets.py in.html --out book.html [--base DIR]

--base defaults to the input file's directory (paths resolve relative to it).
Stdlib only.
"""
import re, os, sys, base64, argparse, mimetypes

MIME = {
    '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp',
    '.avif': 'image/avif', '.woff2': 'font/woff2', '.woff': 'font/woff',
    '.ttf': 'font/ttf', '.otf': 'font/otf',
}


def is_remote(u):
    return u.startswith(('data:', 'http:', 'https:', '//', '#'))


def to_data_uri(path):
    ext = os.path.splitext(path)[1].lower()
    mime = MIME.get(ext) or mimetypes.guess_type(path)[0] or 'application/octet-stream'
    with open(path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('ascii')
    return f'data:{mime};base64,{b64}'


def main():
    ap = argparse.ArgumentParser(prog='embed_assets')
    ap.add_argument('input')
    ap.add_argument('--out', required=True)
    ap.add_argument('--base', default=None)
    a = ap.parse_args()
    base = a.base or os.path.dirname(os.path.abspath(a.input)) or '.'
    html = open(a.input, 'r', encoding='utf-8').read()

    stats = {'embedded': 0, 'missing': [], 'skipped': 0}

    def resolve(url):
        url = url.split('?')[0].split('#')[0]
        p = url if os.path.isabs(url) else os.path.join(base, url)
        return p if os.path.isfile(p) else None

    def sub_src(m):
        pre, url, post = m.group(1), m.group(2), m.group(3)
        if is_remote(url):
            stats['skipped'] += 1
            return m.group(0)
        p = resolve(url)
        if not p:
            stats['missing'].append(url)
            return m.group(0)
        stats['embedded'] += 1
        return f'{pre}{to_data_uri(p)}{post}'

    # <img src="...">  (and any src="..." attribute)
    html = re.sub(r'(\ssrc=")([^"]+)(")', sub_src, html)
    # CSS url(...) with optional quotes
    def sub_url(m):
        q = m.group(1) or ''
        url = m.group(2)
        if is_remote(url):
            stats['skipped'] += 1
            return m.group(0)
        p = resolve(url)
        if not p:
            stats['missing'].append(url)
            return m.group(0)
        stats['embedded'] += 1
        return f'url({q}{to_data_uri(p)}{q})'
    html = re.sub(r'url\((["\']?)([^)"\']+)\1\)', sub_url, html)

    open(a.out, 'w', encoding='utf-8').write(html)
    size = os.path.getsize(a.out)
    print(f'wrote {a.out} ({size/1024:.0f} KB) — embedded {stats["embedded"]}, '
          f'skipped {stats["skipped"]} remote')
    if stats['missing']:
        print('MISSING (left as-is):', file=sys.stderr)
        for u in dict.fromkeys(stats['missing']):
            print('  ' + u, file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
