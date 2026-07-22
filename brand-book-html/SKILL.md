---
name: brand-book-html
description: >-
  Build a full brand guidelines document ("brand book") as a self-contained HTML file —
  open it anywhere, print it to PDF, or publish it as a Claude Artifact — and ship it with
  a matching agent-usable brand skill. No design app required. The brand can be your own or
  a client's. Use when the user wants to create brand guidelines, a brand book, a brand /
  identity system, a style guide, or a logo/mascot spec, or asks to "turn these assets into
  guidelines" or "make a brand book for <brand>". For an editable Paper canvas instead, use
  `brand-book-paper`. Two deliverables every time: (1) the HTML book, (2) a `<brand>-brand`
  skill that keeps that brand's product on-brand during agentic coding.
metadata:
  origin: local
  surface: design + engineering
  version: 1.0.0
---

# Brand Book Builder — HTML

Turn a brand's raw assets (a logo, maybe a mascot, colours, fonts, a bit of voice) into
two things:

1. **The brand book** — an 11-spread, Swiss-editorial guidelines document rendered as a
   **single self-contained HTML file**: open it in any browser, print it to PDF, or
   publish it as a Claude **Artifact**. Fonts and SVGs are inlined, so it travels with no
   external requests.
2. **The companion brand skill** — a self-contained `<brand>-brand/` skill (SKILL.md +
   tokens + logo rules + voice + the actual asset files) that any coding agent loads to
   apply and update the brand in that brand's codebase.

The brand is whoever's you're documenting — your own product, or a client's. Nothing here
assumes a client relationship.

Deliverable #2 is not optional. A brand book nobody can operationalize is a PDF that rots.
The skill is how the brand stays alive in the product.

**Both deliverables derive from one file: `brand.json`** — a machine-readable spec of the
whole brand (colours as semantic roles + oklch, type, logo/mascot, voice, layout). Author
it once at intake; generate the book, the companion skill, and the token files from it so
they can't drift. Schema: `references/brand-json.md`.

> **HTML vs Paper.** This skill outputs a portable HTML file — the right default for almost
> everyone (a browser is all it takes; it prints to PDF and publishes as an Artifact). If
> the user specifically wants to hand-edit on a design canvas and has Paper, use the sibling
> `brand-book-paper` skill instead. The content is identical; only the rendering differs.

## Workflow

Work the phases in order. Screenshot/open and self-review after every spread (see
`references/design-system.md` → Review checklist). Build **incrementally** — one visual
group at a time, never a whole spread in one shot.

1. **Intake → `brand.json`.** Either **measure a live site** (drive a browser; resolve the
   seven colour roles by frequency, harvest fonts/logo/imagery — never guess from memory)
   or take a **structured brief**. Score confidence and raise **open questions** (never
   dead-end on ambiguity — recommend an answer so the user can confirm/override). Post the
   brief for sign-off, then write `brand.json`. Full method: `references/intake.md`.

2. **Assets.** Normalize the marks with `scripts/svgkit.py` — extract the symbol out of the
   wordmark, unify inks, emit ink/white/accent variants, slice any mascot/icon sprite row
   into tight uniform slices. Full recipe + gotchas: `references/asset-pipeline.md`.
   **Persist assets into the companion skill's `assets/` dir** — never leave them only in a
   temp scratchpad.

3. **Design tokens (generated from `brand.json`).** Emit the token set — colours as
   semantic roles (+oklch), fonts, type/weight/tracking scales, radius, spacing:
   `references/design-system.md` + `scripts/gen_tokens.py`. In HTML they're `:root` custom
   properties (and a real `tokens.css`/`tokens.json` in the companion skill).

4. **Build the HTML book.** 11 landscape spreads (1440×900) in one self-contained file —
   embedded fonts + assets, a fit-to-viewport script, print-one-spread-per-page CSS. Build
   spread 1 fully (including the shared running-head + footer chrome), then reuse the chrome
   for the rest. Content per spread: `references/spread-map.md`. Full HTML recipe:
   `references/build-html.md`.

5. **Review, embed & publish.** Run the review checklist on each spread; reconcile
   cross-spread inconsistencies (clear-space value, page numbers, section numbers). Run
   `scripts/embed_assets.py` to inline every local img/font → one portable file. Then
   **print → PDF** or **publish the Artifact** (set a stable `<title>`, a one-line
   `description`, a `favicon` emoji).

6. **Generate the companion brand skill.** Emit `<brand>-brand/` (usually inside the brand's
   own repo at `.claude/skills/<brand>-brand/`, so it travels with the code). Template + how
   to wire tokens into the stack: `references/companion-skill.md`.

## Non-negotiables (the taste rules)

- **One accent, once per view.** Monochrome ink-on-paper is the ground; the accent colour is
  a spotlight, not a wash — a persistent tiny section marker plus one deliberate accent
  moment per spread. Never a rainbow.
- **Extract the real mark.** The symbol usually lives *inside* the wordmark. Don't grab a
  stray "pictorial" file that looks similar — confirm which files are the approved logos.
- **Measure, don't eyeball, and don't rasterize to measure.** `svgkit` reads the vector;
  thumbnailers lie (they square the canvas and blacken transparency).
- **Values are measured or chosen, never recalled.** Colours and fonts come from a live site
  or the brief — not memory. An unguided LLM regresses to the mean (Inter, an indigo accent,
  a purple gradient), which is off-brand for everyone. Mark inferred values; turn ambiguity
  into an open question, not a silent guess.
- **Pure white ground for a high-chroma accent.** A saturated accent (coral, cobalt, cadmium)
  wants `#FFFFFF`, not a tinted cream.
- **Self-contained output.** Inline the fonts (@font-face data URI; the Artifact CSP blocks
  font CDNs) and the SVG assets. No external requests.
- **A brand book is single-theme paper.** It legitimately commits to a white-paper world; it
  does not need a dark mode. Sit the white spreads on a neutral gallery ground.
- **Register discipline in the copy.** Book copy is calm and declarative. A separate
  loud/social voice is *documented* on the Voice & Tone spread, never used to write the book.
- **Accessibility is a rule.** State the passing text-contrast pairs; if the accent fails as
  small text on white, ship a darker text-only variant and say so.

## Reference files

- `references/brand-json.md` — **the `brand.json` source-of-truth schema** everything derives
  from.
- `references/intake.md` — measure a live site or take a structured brief → `brand.json`.
- `references/spread-map.md` — the 11 spreads, shared chrome, per-spread layout & copy.
- `references/build-html.md` — render as a self-contained HTML artifact.
- `references/design-system.md` — tokens, semantic colour roles, oklch, review checklist.
- `references/asset-pipeline.md` — `svgkit` recipes + placement.
- `references/companion-skill.md` — how to emit the `<brand>-brand` companion skill.
- `scripts/svgkit.py` — clusters / slice-row / extract / tight / recolor.
- `scripts/gen_tokens.py` — `brand.json` → tokens.css (+ Tailwind @theme) + tokens.json.
- `scripts/embed_assets.py` — inline local imgs/fonts as data URIs → self-contained HTML.
