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
2. **A companion `<brand>-brand` skill** — real token files (`tokens.css`/`tokens.json`),
   logo/mascot usage, an *enforceable* voice (We-Are/We-Are-Not, vocabulary, UI-copy
   rules), the SVG assets, and an optional advisory **enforcement hook** — so a coding
   agent keeps the product on-brand and can update the brand safely.

### One source of truth

Both deliverables derive from a single machine-readable **`brand.json`** — colours as
semantic roles (+ OKLCH), typography, logo/mascot, voice, layout. Author it once at
intake (by **measuring a live site** — resolving the seven colour roles by frequency,
harvesting fonts/logo — or from a structured brief), and generate the book, the
companion skill, and the token files from it, so they can't drift. Never guess values
from memory: an unguided model regresses to the mean (Inter, an indigo accent, a purple
gradient), which is off-brand for everyone.

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
  brand-json.md              the brand.json source-of-truth schema (everything derives)
  intake.md                  measure a live site or take a brief -> brand.json
  spread-map.md              the 11 spreads, shared chrome, layout & copy (neutral)
  build-html.md              render as a self-contained HTML artifact (default)
  build-paper.md             render on the Paper canvas (optional)
  design-system.md           tokens, semantic colour roles, oklch, review checklist
  asset-pipeline.md          svgkit recipes + placement per medium
  companion-skill.md         emit the <brand>-brand skill: tokens, enforceable voice, hook
scripts/
  svgkit.py                  stdlib SVG toolkit (below)
  gen_tokens.py              brand.json -> tokens.css (+ Tailwind @theme) + tokens.json
  embed_assets.py            inline local imgs/fonts as data URIs -> self-contained HTML
```

Method distilled from the best of the ecosystem's brand skills — measured extraction
and a machine-readable kit (open-design), real token files (extract-design-system),
a two-register enforceable voice (Sentry, Anthropic brand-voice), and evidence-based
token-role mapping for existing codebases (open-design token-map).

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
