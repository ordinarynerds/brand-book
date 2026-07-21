# Build in Paper (optional)

Only if the user has [Paper](https://paper.design) and wants an editable canvas.
Otherwise use `build-html.md`. Content is identical (`spread-map.md`); this is just
the canvas mechanics.

Load the Paper guide first: `get_guide({ topic: "paper-mcp-instructions" })`. Confirm
the `plugin:paper-desktop:paper` MCP tools are available (load via ToolSearch if
deferred). Build **incrementally** — one visual group per `write_html`, screenshot to
self-review, never a whole spread in one call. Call `finish_working_on_nodes` when done.

## Tokens

`create_tokens` for the full set (see `design-system.md`), then reference them in
markup as `var(--color-ink)` etc.

## Canvas grid (3×4)

- Artboards `1440×900`, white, `display:flex;flex-direction:column`. Grid pitch
  **1520px** horizontal, **980px** vertical. Reading order must equal canvas position
  (top→bottom, left→right) so `export_combined_pdf` pages come out 1→11.
- With spread 1 at world (−720, −450): cols x = −720, 800, 2320; rows y = −450, 530,
  1510, 2490.
- `create_artboard` auto-places; set final position with `update_styles` `left`/`top`
  (= the world coords). Verify with `get_children(root)`.

## Reuse the chrome

Build spread 1 fully (running-head + footer + first content), then `duplicate_nodes`
×N to clone the chrome. For each clone: `update_styles` to position it, `rename_nodes`,
`set_text_content` the section label + page number, delete the cloned body children
(from the `descendantIdMap` the duplicate returns — a source→clone id map), then build
the new body into the emptied content frame.

## Assets

- Export approved logo/mascot nodes to SVG (**one node per `export` call** — it races
  in parallel), normalize with `svgkit`, then place as
  `<img src="paper-asset:///absolute/path.svg">` (three slashes + absolute path).
  Cloning brand SVGs with `x-paper-clone` misplaces them (absolute coords) — always
  export + `<img>`.
- Swap an already-placed image with `write_html` `mode:"replace"` on the image node.
- Size mascot slices by height with per-glyph width (from `svgkit slice-row`).

## Edit / add a spread later

Reflow so canvas order still equals reading order (move affected artboards with
`update_styles`), then renumber page footers + section labels. The exporter orders
purely by position.

## Export

`export_combined_pdf` on the 11 artboard ids (auto-orders by canvas position) →
`~/Downloads/<Brand>-Brand-Book.pdf`.
