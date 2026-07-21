---
name: brand-book
description: >-
  Build a full brand guidelines document ("brand book") as a self-contained HTML
  artifact (no design app required), and ship it with a matching agent-usable brand
  skill. Optionally render it in Paper instead. The brand can be your own or a
  client's. Use when the user wants to create brand guidelines, a brand book, a
  brand/identity system, a style guide, a logo/mascot spec, or asks to "turn these
  assets into guidelines" or "make a brand skill for <brand>". Two deliverables every
  time: (1) the brand book, (2) a `<brand>-brand` skill that keeps that brand's
  product on-brand during agentic coding.
metadata:
  origin: local
  surface: design + engineering
  version: 3.0.0
---

# Brand Book Builder

Turn a brand's raw assets (a logo, maybe a mascot, colours, fonts, a bit of voice)
into two things:

1. **The brand book** — an 11-spread, Swiss-editorial guidelines document. Default
   output is a **single self-contained HTML file** you can open anywhere, print to
   PDF, or publish as a Claude **Artifact**. No design app needed. (If you have
   [Paper](https://paper.design) and want an editable canvas instead, there's an
   optional Paper path.)
2. **The companion brand skill** — a self-contained `<brand>-brand/` skill (SKILL.md
   + tokens + logo rules + voice + the actual asset files) that any coding agent loads
   to apply and update the brand in that brand's codebase.

The brand is whoever's you're documenting — your own product, or a client's. Nothing
here assumes a client relationship.

Deliverable #2 is not optional. A brand book nobody can operationalize is a PDF that
rots. The skill is how the brand stays alive in the product.

**Both deliverables derive from one file: `brand.json`** — a machine-readable spec of
the whole brand (colours as semantic roles + oklch, type, logo/mascot, voice, layout).
Author it once at intake; generate the book, the companion skill, and the token files
from it so they can't drift. Schema: `references/brand-json.md`.

## Pick a render target

| | **HTML artifact** (default) | **Paper** (optional) |
|---|---|---|
| Needs | nothing but a browser | Paper desktop + its MCP |
| Output | one `.html` → Artifact / print-to-PDF | editable canvas → PDF export |
| Best when | most people; sharing a link; agentic pipelines | you want to hand-edit on a canvas |
| How | `references/build-html.md` | `references/build-paper.md` |

The **content** (what's on each spread, the copy, the rules) is identical either way
and lives in `references/spread-map.md`. Only the rendering differs. Default to HTML
unless the user asks for Paper.

## Workflow

1. **Intake → `brand.json`.** Either **measure a live site** (drive a browser; resolve
   the seven colour roles by frequency, harvest fonts/logo/imagery — never guess from
   memory) or take a **structured brief**. Score confidence and raise **open questions**
   (never dead-end on ambiguity — recommend an answer so the user can confirm/override).
   Post the brief for sign-off, then write `brand.json`. Full method:
   `references/intake.md`.

2. **Assets.** Normalize the marks with `scripts/svgkit.py` — extract the symbol out
   of the wordmark, unify inks, emit ink/white/accent variants, slice any mascot/icon
   sprite row into tight uniform slices. Full recipe + gotchas:
   `references/asset-pipeline.md`. **Persist assets into the companion skill's
   `assets/` dir** — never leave them only in a temp scratchpad.

3. **Design tokens (generated from `brand.json`).** Emit the token set — colours as
   semantic roles (+oklch), fonts, type/weight/tracking scales, radius, spacing:
   `references/design-system.md`. In HTML they're `:root` custom properties (+ a real
   `tokens.css`/`tokens.json` in the companion skill); in Paper they're file tokens.

4. **Build the spreads.** 11 landscape spreads (1440×900), same content either way
   (`references/spread-map.md`). Then follow your render target:
   - HTML → `references/build-html.md` (one file, embedded fonts + assets, print CSS,
     publish as an Artifact). Self-review each spread by opening/screenshotting it.
   - Paper → `references/build-paper.md` (canvas grid, duplicate-the-chrome, export).

5. **Review & export.** Run the review checklist (`references/design-system.md`) on
   every spread; reconcile cross-spread inconsistencies (clear-space value, page
   numbers, section numbers). HTML: print → PDF (or publish the Artifact). Paper:
   `export_combined_pdf`.

6. **Generate the companion brand skill.** Emit `<brand>-brand/` (usually inside the
   brand's own repo at `.claude/skills/<brand>-brand/`, so it travels with the code):
   `references/companion-skill.md`.

## Non-negotiables (the taste rules)

- **One accent, once per view.** Monochrome ink-on-paper is the ground; the accent
  colour is a spotlight, not a wash — a persistent tiny section marker plus one
  deliberate accent moment per spread. Never a rainbow.
- **Extract the real mark.** The symbol usually lives *inside* the wordmark. Do not
  grab a stray "pictorial" file that looks similar — confirm which nodes/files are the
  approved logos before using anything. (A wrong outline mark slipped through once.)
- **Measure, don't eyeball, and don't rasterize to measure.** `svgkit` reads the
  vector; thumbnailers lie (they square the canvas and blacken transparency).
- **Values are measured or chosen, never recalled.** Colours and fonts come from a live
  site or the brief — not memory. An unguided LLM regresses to the mean (Inter, an
  indigo accent, a purple gradient), which is off-brand for everyone. Mark inferred
  values, and turn ambiguity into an open question, not a silent guess.
- **Pure white ground for a high-chroma accent.** A saturated accent (coral, cobalt,
  cadmium) wants `#FFFFFF`, not a tinted cream.
- **Self-contained output (HTML).** A brand book is meant to travel — inline the fonts
  (@font-face data URI; the Artifact CSP blocks font CDNs) and the SVG assets. No
  external requests.
- **A brand book is single-theme paper.** It legitimately commits to a white-paper
  world; it does not need a dark mode. Sit the white spreads on a neutral gallery
  ground so they read as pages.
- **Register discipline in the copy.** Book copy is calm and declarative. A separate
  loud/social voice is *documented* on the Voice & Tone spread, never used to write
  the book.
- **Accessibility is a rule.** State the passing text-contrast pairs; if the accent
  fails as small text on white, ship a darker text-only variant and say so.

## Reference files

- `references/brand-json.md` — **the `brand.json` source-of-truth schema** everything
  derives from.
- `references/intake.md` — measure a live site or take a structured brief → `brand.json`
  (confidence + open questions).
- `references/spread-map.md` — the 11 spreads, shared chrome, per-spread layout & copy
  (medium-neutral).
- `references/build-html.md` — render as a self-contained HTML artifact (**default**).
- `references/build-paper.md` — render on the Paper canvas (optional).
- `references/design-system.md` — tokens, type scale, review checklist.
- `references/asset-pipeline.md` — `svgkit` recipes + placement per medium.
- `references/companion-skill.md` — how to emit the `<brand>-brand` companion skill.
- `scripts/svgkit.py` — clusters / slice-row / extract / tight / recolor.
- `scripts/embed_assets.py` — inline local imgs/fonts as data URIs → self-contained.
