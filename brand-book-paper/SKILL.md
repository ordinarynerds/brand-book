---
name: brand-book-paper
description: >-
  Build a full brand guidelines document ("brand book") on the Paper design canvas (an
  editable, exportable file), and ship it with a matching agent-usable brand skill. Requires
  the Paper desktop app + its MCP. The brand can be your own or a client's. Use when the user
  wants a brand book / brand guidelines / identity system ON PAPER specifically, or wants an
  editable design-canvas version they can keep tweaking. If they just want a portable
  document (open anywhere, print to PDF, publish as an Artifact), use `brand-book-html`
  instead — that's the better default for most people. Two deliverables every time: (1) the
  Paper book (→ PDF), (2) a `<brand>-brand` skill that keeps that brand's product on-brand
  during agentic coding.
metadata:
  origin: local
  surface: design + engineering
  version: 1.0.0
---

# Brand Book Builder — Paper

Turn a brand's raw assets (a logo, maybe a mascot, colours, fonts, a bit of voice) into two
things:

1. **The brand book** — an 11-spread, Swiss-editorial guidelines document built on the
   **Paper** canvas (via the `plugin:paper-desktop:paper` MCP tools), exported to PDF.
   Editable by hand afterward.
2. **The companion brand skill** — a self-contained `<brand>-brand/` skill (SKILL.md +
   tokens + logo rules + voice + the actual asset files) that any coding agent loads to
   apply and update the brand in that brand's codebase.

The brand is whoever's you're documenting — your own product, or a client's. Nothing here
assumes a client relationship.

Deliverable #2 is not optional. A brand book nobody can operationalize is a PDF that rots.
The skill is how the brand stays alive in the product.

**Both deliverables derive from one file: `brand.json`** — a machine-readable spec of the
whole brand (colours as semantic roles + oklch, type, logo/mascot, voice, layout). Author it
once at intake; generate the book, the companion skill, and the token files from it so they
can't drift. Schema: `references/brand-json.md`.

> **Paper vs HTML.** This skill builds an editable canvas in the Paper desktop app — reach
> for it only when the user wants Paper specifically or wants to hand-edit the design.
> Otherwise the sibling `brand-book-html` skill is the better default: it outputs one
> portable HTML file that opens in any browser, prints to PDF, and publishes as an Artifact —
> no design app required. The content is identical; only the rendering differs.
>
> Load the Paper guide first: `get_guide({ topic: "paper-mcp-instructions" })`. Confirm the
> Paper MCP tools are available (load via ToolSearch if deferred). This skill runs in the
> **main loop**, not a subagent — it needs the Paper MCP interactively.

## Workflow

Work the phases in order. Screenshot and self-review after every spread (see
`references/design-system.md` → Review checklist). Build **incrementally** — one visual
group per `write_html`, never a whole spread in one call. Call `finish_working_on_nodes`
when done.

1. **Intake → `brand.json`.** Either **measure a live site** (drive a browser; resolve the
   seven colour roles by frequency, harvest fonts/logo/imagery — never guess from memory) or
   take a **structured brief**. Score confidence and raise **open questions** (never
   dead-end on ambiguity — recommend an answer so the user can confirm/override). Post the
   brief for sign-off, then write `brand.json`. Full method: `references/intake.md`.

2. **Assets.** Export the approved logo/mascot nodes to SVG (**one node per `export` call** —
   it races in parallel), normalize with `scripts/svgkit.py` (extract the symbol from the
   wordmark, unify inks, emit variants, slice a mascot sprite row into tight uniform slices),
   then place as `<img src="paper-asset:///abs/path.svg">`. Full recipe + gotchas:
   `references/asset-pipeline.md`. **Persist assets into the companion skill's `assets/`
   dir** — never leave them only in a temp scratchpad.

3. **Design tokens (generated from `brand.json`).** Create the file-level token set with
   `create_tokens` — colours as semantic roles (+oklch), fonts, type/weight/tracking scales,
   radius, spacing: `references/design-system.md` + `scripts/gen_tokens.py` (also emits the
   real `tokens.css`/`tokens.json` for the companion skill).

4. **Build the Paper book.** 11 landscape artboards (1440×900) in a 3×4 canvas grid whose
   reading order matches canvas position (so the combined-PDF export comes out in order).
   Build spread 1 fully — including the shared running-head + footer chrome — then
   `duplicate_nodes` for the rest and replace each body. Canvas mechanics:
   `references/build-paper.md`. Content per spread: `references/spread-map.md`.

5. **Review & export.** Run the review checklist on each spread; reconcile cross-spread
   inconsistencies (clear-space value, page numbers, section numbers). Export with
   `export_combined_pdf` (auto-orders by canvas position) →
   `~/Downloads/<Brand>-Brand-Book.pdf`. Call `finish_working_on_nodes` when done.

6. **Generate the companion brand skill.** Emit `<brand>-brand/` (usually inside the brand's
   own repo at `.claude/skills/<brand>-brand/`, so it travels with the code). Template + how
   to wire tokens into the stack: `references/companion-skill.md`.

## Non-negotiables (the taste rules)

- **One accent, once per view.** Monochrome ink-on-paper is the ground; the accent colour is
  a spotlight, not a wash — a persistent tiny section marker plus one deliberate accent
  moment per spread. Never a rainbow.
- **Extract the real mark.** The symbol usually lives *inside* the wordmark. Don't grab a
  stray "pictorial" file that looks similar — confirm which nodes are the approved logos.
- **Measure, don't eyeball, and don't rasterize to measure.** `svgkit` reads the vector;
  thumbnailers lie (they square the canvas and blacken transparency).
- **Values are measured or chosen, never recalled.** Colours and fonts come from a live site
  or the brief — not memory. An unguided LLM regresses to the mean (Inter, an indigo accent,
  a purple gradient), which is off-brand for everyone. Mark inferred values; turn ambiguity
  into an open question, not a silent guess.
- **Pure white ground for a high-chroma accent.** A saturated accent wants `#FFFFFF`, not a
  tinted cream.
- **Register discipline in the copy.** Book copy is calm and declarative. A separate
  loud/social voice is *documented* on the Voice & Tone spread, never used to write the book.
- **Accessibility is a rule.** State the passing text-contrast pairs; if the accent fails as
  small text on white, ship a darker text-only variant and say so.

## Reference files

- `references/brand-json.md` — **the `brand.json` source-of-truth schema** everything derives
  from.
- `references/intake.md` — measure a live site or take a structured brief → `brand.json`.
- `references/spread-map.md` — the 11 spreads, shared chrome, per-spread layout & copy.
- `references/build-paper.md` — render on the Paper canvas (grid, duplicate-the-chrome,
  export).
- `references/design-system.md` — tokens, semantic colour roles, oklch, review checklist.
- `references/asset-pipeline.md` — `svgkit` recipes + Paper placement.
- `references/companion-skill.md` — how to emit the `<brand>-brand` companion skill.
- `scripts/svgkit.py` — clusters / slice-row / extract / tight / recolor.
- `scripts/gen_tokens.py` — `brand.json` → tokens.css (+ Tailwind @theme) + tokens.json.
