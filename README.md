# brand-book

An agent skill that builds a full **brand guidelines document** ("brand book") in
[Paper](https://paper.design) and ships it with a matching **agent-usable brand
skill** — so the brand doesn't just live in a PDF, it stays enforceable in code.

Built by [Ordinary Nerds](https://ordinarynerds.com). Works with Claude Code (or any
agent that can load skills and drive the Paper desktop MCP). The brand can be your own
or a client's — nothing here assumes a client relationship.

## Two deliverables, every time

1. **The brand book** — 11 landscape spreads (1440×900) in a 3×4 grid, Swiss-editorial:
   Introduction · Logo System (symbol construction, lockups, do's & don'ts) · Mascot
   /Illustration · Typography (specimen + hierarchy) · Colour (palette + neutrals +
   accessibility) · Voice & Tone · Applications. Exported to a single PDF.
2. **A companion `<brand>-brand` skill** — tokens, logo/mascot usage, voice, and the
   real SVG assets, packaged so a coding agent keeps the product on-brand and can
   update the brand safely.

## Requirements

- An agent that supports skills (e.g. Claude Code).
- The **Paper desktop app** + its MCP server (`plugin:paper-desktop:paper`).
- `python3` for `scripts/svgkit.py` (standard library only — no dependencies).

## Install

With the [skills CLI](https://skills.sh):

```bash
npx skills add ordinarynerds/brand-book
```

Or copy this folder into your project (or `~`) at `.claude/skills/brand-book/`.

## Use

In Claude Code, invoke it:

```
/brand-book
```

…or just ask to "turn these brand assets into guidelines" / "make a brand book and a
brand skill for <brand>". Have the brand's logo/mascot (SVG is best), colours, fonts,
and a sense of voice ready. The skill posts a design brief for sign-off, then builds
spread-by-spread with self-review, exports the PDF, and generates the companion skill.

## What's inside

```
SKILL.md                     the workflow + the taste rules
references/
  spread-map.md              the 11 spreads, shared chrome, per-spread layout & copy
  design-system.md           design tokens, type scale, grid math, review checklist
  asset-pipeline.md          svgkit recipes + Paper gotchas + construction-grid gen
  companion-skill.md         how to emit the <brand>-brand companion skill (+template)
scripts/
  svgkit.py                  stdlib SVG toolkit (below)
```

### svgkit

Brand SVGs carry absolute coordinates and inconsistent inks; naive slicing leaves
uneven margins. `svgkit` measures the real geometry from the vector path data (never
rasterize to measure — thumbnailers square the canvas and blacken transparency).

```bash
svgkit clusters  row.svg                          # detect glyphs in a sprite row
svgkit slice-row row.svg --out ./o --name face    # tight, common-height slices + widths
svgkit extract   wordmark.svg --out mark.svg --pick left   # pull the symbol out of a lockup
svgkit tight     mark.svg --out mark.svg           # crop viewBox to the drawing
svgkit recolor   mark.svg --out mark-white.svg --map "#38353C=#FFFFFF"
```

## Design principles it enforces

- One accent, used **once per view** — monochrome ink-on-paper is the ground.
- Extract the **real** mark (usually inside the wordmark), don't grab a look-alike.
- Pure-white ground for a high-chroma accent.
- Calm, declarative book copy; a separate loud/social voice is *documented*, never
  used to write the book.
- Accessibility is a rule: state the passing contrast pairs; ship a darker text-only
  variant when the accent fails as small text.

## License

[MIT](./LICENSE) © Ordinary Nerds
