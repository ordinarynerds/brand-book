---
name: brand-book
description: >-
  Build a full brand guidelines document ("brand book") in Paper, and ship it with a
  matching agent-usable brand skill. The brand can be your own or a client's. Use when
  the user wants to create brand guidelines, a brand book, a brand/identity system, a
  style guide, a logo/mascot spec, or asks to "turn these assets into guidelines" or
  "make a brand skill for <brand>". Two deliverables every time: (1) an 11-spread Paper
  document, (2) a `<brand>-brand` skill that keeps that brand's product on-brand during
  agentic coding.
metadata:
  origin: local
  surface: design + engineering
  version: 1.0.0
---

# Brand Book Builder

Turn a brand's raw assets (a logo, maybe a mascot, colours, fonts, a bit of voice)
into two things:

1. **The brand book** — an 11-spread, Swiss-editorial guidelines document built in
   **Paper** (via the `plugin:paper-desktop:paper` MCP tools), exported to PDF.
2. **The companion brand skill** — a self-contained `<brand>-brand/` skill (SKILL.md
   + tokens + logo rules + voice + the actual asset files) that any coding agent loads
   to apply and update the brand in that brand's codebase.

The brand is whoever's you're documenting — your own product, or a client's. Nothing
here assumes a client relationship.

Deliverable #2 is not optional. A brand book nobody can operationalize is a PDF that
rots. The skill is how the brand stays alive in the product.

> This skill runs in the **main loop**, not a subagent — it needs the Paper MCP
> interactively (write a group, screenshot, critique, fix). Load the Paper guide
> first: `get_guide({ topic: "paper-mcp-instructions" })`.

## Prerequisites

- Paper desktop running with the brand's file open (or create one). Confirm the Paper
  MCP tools are available; load them via ToolSearch if deferred.
- Brand inputs, ideally: logo/wordmark (SVG best), any mascot/illustration, colour
  values, font choices, and a sense of voice. Missing pieces are fine — infer from
  what exists and confirm the gaps in the brief.
- `python3` for `scripts/svgkit.py` (stdlib only — no pip).

## Workflow

Work the phases in order. Screenshot and self-review after every spread (see
`references/design-system.md` → Review checklist). Build **incrementally** — one
visual group per `write_html`, never a whole spread in one call.

1. **Intake & brief.** Inspect any brand assets already in the file (`get_basic_info`,
   `get_tree_summary`, screenshot the logo/marks). Then post a short brief to the user
   (mood/register, palette with roles + hex, type + scale, the spread list) and get a
   nod before building. If the brand is already defined, the brief just restates it.

2. **Assets.** Normalize the marks with `scripts/svgkit.py` — extract the symbol out
   of the wordmark, unify inks, emit ink/white/accent variants, slice any mascot/icon
   sprite row into tight uniform slices. Full recipe + gotchas:
   `references/asset-pipeline.md`. **Persist assets into the companion skill's
   `assets/` dir** — never leave them only in a temp scratchpad.

3. **Design tokens.** Create the file-level token set (colours with roles, fonts,
   type/weight/tracking/leading scales, radius, spacing). Exact set + the name→role
   mapping: `references/design-system.md`.

4. **Build the spreads.** 11 landscape spreads (1440×900) in a 3×4 canvas grid whose
   reading order matches canvas position (so the combined-PDF export comes out in
   order). Build spread 1 fully — including the shared running-head + footer chrome —
   then **duplicate it** for the rest and replace each body. Per-spread content, copy
   patterns, and the chrome spec: `references/spread-map.md`.

5. **Review & export.** Run the review checklist on each spread; reconcile any
   cross-spread inconsistencies (clear-space value, page numbers, section numbers).
   Export with `export_combined_pdf` (auto-orders by canvas position) →
   `~/Downloads/<Brand>-Brand-Book.pdf`. Call `finish_working_on_nodes` when done.

6. **Generate the companion brand skill.** Emit `<brand>-brand/` (usually inside the
   brand's own repo at `.claude/skills/<brand>-brand/`, so it travels with the code).
   Template + what to fill + how to wire tokens into the stack:
   `references/companion-skill.md`.

## Non-negotiables (the taste rules)

- **One accent, once per view.** Monochrome ink-on-paper is the ground; the accent
  colour is a spotlight, not a wash — a persistent tiny section marker plus one
  deliberate accent moment per spread. Never a rainbow.
- **Extract the real mark.** The symbol usually lives *inside* the wordmark. Do not
  grab a stray "pictorial" file that looks similar — confirm which nodes are the
  approved logos before using anything. (A wrong outline mark slipped through once;
  don't repeat it.)
- **Measure, don't eyeball, and don't rasterize to measure.** `svgkit` reads the
  vector; qlmanage/thumbnails lie (they square the canvas and blacken transparency).
- **Pure white ground for a high-chroma accent.** A saturated accent (coral, cobalt,
  cadmium) wants `#FFFFFF`, not a tinted cream. Tinted grounds are for muted,
  sun-bleached palettes only.
- **Register discipline in the copy.** Brand-book body copy is calm and declarative.
  If the brand has a separate loud/social voice, document it on the Voice & Tone
  spread but never write the book itself in it.
- **Accessibility is a rule, not a footnote.** State the text-contrast pairs that
  pass; if the accent fails as small text on white, ship a darker text-only variant
  and say so.

## Reference files

- `references/spread-map.md` — the 11 spreads, chrome spec, per-spread layout & copy.
- `references/design-system.md` — tokens, type scale, grid math, review checklist.
- `references/asset-pipeline.md` — `svgkit` recipes + Paper asset gotchas.
- `references/companion-skill.md` — how to emit the `<brand>-brand` companion skill.
- `scripts/svgkit.py` — clusters / slice-row / extract / tight / recolor.

A finished companion skill to mirror is `ordinary-nerds-brand/` (a sibling skill in
this repo) — the concrete instance of everything below. When open-sourcing this skill,
that folder is just an example; each user replaces it with their own brand.
