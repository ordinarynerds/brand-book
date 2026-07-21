# brand-book

An agent skill that builds a full **brand guidelines document** ("brand book") and
ships it with a matching **agent-usable brand skill** — so the brand doesn't just live
in a PDF, it stays enforceable in code.

Default output is a **single self-contained HTML file** — open it anywhere, print it
to PDF, or publish it as a live Claude Artifact. No design app required. (If you have
[Paper](https://paper.design) and want an editable canvas, there's an optional path
for that too.)

Built by [Ordinary Nerds](https://ordinarynerds.com). Works with Claude Code (or any
agent that can load skills). The brand can be your own or a client's — nothing here
assumes a client relationship.

## Two deliverables, every time

1. **The brand book** — 11 landscape spreads (1440×900), Swiss-editorial:
   Introduction · Logo System (symbol construction, lockups, do's & don'ts) · Mascot
   /Illustration · Typography (specimen + hierarchy) · Colour (palette + neutrals +
   accessibility) · Voice & Tone · Applications. Fonts and SVGs are inlined, so the
   one HTML file is fully portable and prints one-spread-per-page.
2. **A companion `<brand>-brand` skill** — tokens, logo/mascot usage, voice, and the
   real SVG assets, packaged so a coding agent keeps the product on-brand and can
   update the brand safely.

## Requirements

- An agent that supports skills (e.g. Claude Code).
- `python3` for the scripts (standard library only — no dependencies).
- **HTML target:** just a browser. **Paper target (optional):** the Paper desktop app
  + its MCP server.

## Install

With the [skills CLI](https://skills.sh):

```bash
npx skills add ordinarynerds/brand-book
```

Or copy this folder into your project (or `~`) at `.claude/skills/brand-book/`.

## Use

In Claude Code:

```
/brand-book
```

…or just ask to "turn these brand assets into guidelines" / "make a brand book and a
brand skill for <brand>". Have the brand's logo/mascot (SVG is best), colours, fonts,
and a sense of voice ready. The skill posts a design brief for sign-off, builds
spread-by-spread with self-review, produces the HTML (or Paper) book, and generates
the companion skill.

## What's inside

```
SKILL.md                     the workflow + the taste rules
references/
  spread-map.md              the 11 spreads, shared chrome, layout & copy (neutral)
  build-html.md              render as a self-contained HTML artifact (default)
  build-paper.md             render on the Paper canvas (optional)
  design-system.md           design tokens, type scale, review checklist
  asset-pipeline.md          svgkit recipes + placement per medium
  companion-skill.md         how to emit the <brand>-brand companion skill (+template)
scripts/
  svgkit.py                  stdlib SVG toolkit (below)
  embed_assets.py            inline local imgs/fonts as data URIs -> self-contained HTML
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

### embed_assets

Turns a readable HTML file (relative `src=`/`url()` paths) into one self-contained
document — required for Artifacts, handy everywhere.

```bash
embed_assets.py book.src.html --out book.html
```

## Design principles it enforces

- One accent, used **once per view** — monochrome ink-on-paper is the ground.
- Extract the **real** mark (usually inside the wordmark), don't grab a look-alike.
- Pure-white ground for a high-chroma accent; a brand book is single-theme paper.
- Self-contained output: inline the fonts (@font-face data URI — CDNs are CSP-blocked)
  and the assets.
- Calm, declarative book copy; a separate loud/social voice is *documented*, never
  used to write the book.
- Accessibility is a rule: state the passing contrast pairs; ship a darker text-only
  variant when the accent fails as small text.

## License

[MIT](./LICENSE) © Ordinary Nerds
