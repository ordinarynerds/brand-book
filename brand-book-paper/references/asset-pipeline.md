# Asset pipeline

Brand SVGs carry absolute coordinates and inconsistent inks. Normalize them before
they touch the design. `scripts/svgkit.py` is stdlib-only (no pip).

## Golden rules (hard-won)

1. **Cloning brand SVGs in Paper misplaces them** (absolute coords) — `export` the
   node to SVG and place it as `<img src="paper-asset:///abs/path.svg">`.
2. **`export` does ONE node per call** and races if fired in parallel — call it
   sequentially. Only top-level SVG/Frame nodes export; a child group inside an SVG
   won't export directly (extract it with svgkit instead).
3. **Never rasterize to measure.** qlmanage/Quick-Look squares the canvas and turns
   transparency black, so pixel analysis lies. svgkit reads the vector path data.
4. **The symbol usually lives inside the wordmark.** Extract it — don't hunt for a
   look-alike standalone file. Confirm with the user which nodes are the *approved*
   logos before using anything.
5. **Persist assets to the companion skill's `assets/` dir.** Exports land in
   `~/Downloads`; a scratchpad is temporary. Copy the final SVGs somewhere durable
   (the `<brand>-brand/assets/` folder) and reference those.

## Recipes

Get the raw marks first: `export` the approved wordmark / mascot-row nodes to SVG
(sequential calls), note the `~/Downloads/...svg` paths.

**Extract the symbol out of the wordmark** (leftmost cluster = the mark), unify its
ink, and make variants:
```
svgkit extract wordmark.svg --out mark-ink.svg --pick left \
       --recolor-from "#2E3135,#2F2E33" --to "#38353C"
svgkit recolor mark-ink.svg --out mark-white.svg --map "#38353C=#FFFFFF"
svgkit recolor mark-ink.svg --out mark-accent.svg --map "#38353C=#FF6B4A"
```
`extract` includes a little padding from curve control points; that's fine. Screenshot
it in Paper to confirm framing (Paper renders SVG correctly; qlmanage does not).

**Unify / recolour the full wordmark** for reversed lockups:
```
svgkit recolor wordmark.svg --out wordmark-ink.svg   --map "#2E3135=#38353C,#2F2E33=#38353C"
svgkit recolor wordmark.svg --out wordmark-white.svg --map "#2E3135=#FFFFFF,#2F2E33=#FFFFFF"
```

**Slice a mascot/icon sprite row** (a strip of N faces/icons) into tight, COMMON-
HEIGHT slices so they render at a uniform size in a grid:
```
svgkit clusters faces-row.svg              # sanity check: expect N
svgkit slice-row faces-row.svg --out ./out --name face \
       --recolor-from "#38353C" --colors "ink=#38353C,white=#FFFFFF"
```
It prints `display_widths` at `--height` (default 112). Place each slice as
`<img style="height:112px; width:<that width>px; object-fit:contain">` — same height,
per-glyph width → the grid reads uniform. (Even 1/N slicing looks broken: the first
and last glyph inherit the row's outer canvas margin and render small. slice-row fixes
this by measuring each glyph.) If a sprite has odd spacing, pass `--n N` to force N
clusters or tune `--gap`.

**Fix a mark that sits off-centre in an oversized viewBox:**
```
svgkit tight mark.svg --out mark.svg --pad 6
```

## Construction-grid generator (spread 03)

The symbol-construction plate is a generated SVG placed behind the mark. Keep it a
file + `<img>` (don't inline complex SVG into `write_html`). Minimal generator:

```python
# writes an SxS field: grid, guide circle, dashed baseline, accent optical axis, ticks
S, N = 520, 8; step = S / N
L = [f'<svg viewBox="0 0 {S} {S}" width="{S}" height="{S}" xmlns="http://www.w3.org/2000/svg">']
for i in range(1, N):
    p = i*step
    L += [f'<line x1="{p}" y1="0" x2="{p}" y2="{S}" stroke="#E9E7EA" stroke-width="1"/>',
          f'<line x1="0" y1="{p}" x2="{S}" y2="{p}" stroke="#E9E7EA" stroke-width="1"/>']
L += [f'<circle cx="{S/2}" cy="{S/2}" r="{S/2-step/2}" fill="none" stroke="#C7C4CC" stroke-width="1.25"/>',
      f'<line x1="0" y1="{S/2}" x2="{S}" y2="{S/2}" stroke="#A8A5AD" stroke-width="1" stroke-dasharray="5 5"/>',
      f'<line x1="{S/2}" y1="0" x2="{S/2}" y2="{S}" stroke="#FF6B4A" stroke-width="1.5"/>',  # accent axis
      f'<rect x="0.75" y="0.75" width="{S-1.5}" height="{S-1.5}" fill="none" stroke="#38353C" stroke-width="1.5"/>']
t = 14
for cx, cy in [(0,0),(S,0),(0,S),(S,S)]:
    sx = 1 if cx==0 else -1; sy = 1 if cy==0 else -1
    L += [f'<line x1="{cx}" y1="{cy}" x2="{cx+sx*t}" y2="{cy}" stroke="#38353C" stroke-width="2"/>',
          f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy+sy*t}" stroke="#38353C" stroke-width="2"/>']
L.append('</svg>')
open('construction-grid.svg','w').write("\n".join(L))
```

## Placement (per medium)

- Size mascot/icon slices by **height** with per-glyph width (from `slice-row`) so a
  fixed-height row stays uniform; sizing by width makes tall glyphs shrink. This holds
  in both mediums.
- **HTML** (the `brand-book-html` skill): inline the marks as `<svg>` or as
  `<img src="data:image/svg+xml;base64,…">`; author with relative paths and let
  `scripts/embed_assets.py` do the embedding.
- **Paper** (`build-paper.md`): `<img src="paper-asset:///absolute/path.svg">` (three
  slashes + absolute path); swap a placed image with `write_html` `mode:"replace"`.
