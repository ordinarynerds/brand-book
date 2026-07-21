# Generating the companion brand skill

Every brand book ships with a `<brand>-brand/` skill so a coding agent can apply and
update the brand in the product's codebase. It is the operational half of the
deliverable — the book is the reference, the skill is the API.

Create it inside the brand's own repo at `.claude/skills/<brand>-brand/` (so it
travels with the code), or as a sibling of `brand-book/`. Mirror the shape of a
finished one if you have it.

## Structure

```
<brand>-brand/
  SKILL.md
  assets/            # the real, final SVGs — the durable home for the marks
    wordmark-ink.svg  wordmark-white.svg
    mark-ink.svg      mark-white.svg  mark-accent.svg
    ...(mascot slices if any)
```

Copy the finalized SVGs from the build into `assets/` (do not reference a scratchpad).
Keep the file small: one SKILL.md is usually enough; only split into `references/` if
tokens/voice/usage get long.

## What the skill must contain

1. **Frontmatter** — `name: <brand>-brand`, and a `description` packed with triggers:
   the brand name, "apply/update `<brand>` brand", "brand colors/fonts/tokens",
   "on-brand", "style this like `<brand>`". Add `metadata.surface: engineering`.
2. **Tokens, paste-ready** — the exact token set from the book, as BOTH a vanilla
   `:root{}` block and a Tailwind v4 `@theme{}` block, with the role of each.
3. **Applying in code** — how to wire tokens into the actual stack (CSS variables /
   Tailwind theme / design-token file), which token is text vs bg vs accent, and the
   accent-once rule restated for UI.
4. **Logo usage** — which asset for which context, clear space, min size, the reversal
   rules, and the don'ts — pointing at the files in `assets/`.
5. **Voice & tone** — the register(s) and the boundary rule, with one calm and (if it
   exists) one loud example. Cross-link a separate social-voice skill if there is one.
6. **Accessibility** — the passing text/bg pairs and the accent-as-text fallback.
7. **Update protocol** — how an agent should *change* the brand safely: edit token
   values (not names), regenerate marks with `brand-book`'s `svgkit`, keep the book
   and the skill in sync, never introduce a second accent.

Keep it declarative and specific. It is loaded into a coding agent's context to make
on-brand decisions — no narrative, just the rules and the values.

## Template (fill the {{...}} and delete anything that doesn't apply)

`{{brand}}` is whoever the brand belongs to — a company, a product, or you.

````markdown
---
name: {{brand-slug}}-brand
description: >-
  {{Brand}}'s brand system for agentic coding — colours, typography, logo usage,
  and voice. Use when building or editing {{Brand}}'s product, site, emails, or
  collateral, or when the user says "apply {{Brand}} brand", "make this on-brand",
  "{{Brand}} colours/fonts/tokens", or "style this like {{Brand}}".
metadata:
  surface: engineering
  version: 1.0.0
---

# {{Brand}} Brand

{{One line: what {{Brand}} is + the palette in a sentence, e.g. "charcoal on white,
one loud coral".}} The full reference is the brand book (`{{path/to}}.pdf`); this skill
is how it lands in code.

## Tokens

CSS custom properties (paste into `:root`):
```css
:root{
  --font-sans:{{Family}}; --font-mono:{{Mono}};
  --color-paper:{{#fff}};   /* ground */
  --color-mist:{{#..}};     /* panels/tiles */
  --color-line:{{#..}};     /* hairlines */
  --color-graphite:{{#..}}; /* captions */
  --color-ink:{{#..}};      /* text, marks */
  --color-accent:{{#..}};   /* ONE accent, once per view */
}
```
Tailwind v4 (`@theme`):
```css
@theme{
  --font-sans:{{Family}}; --color-ink:{{#..}}; --color-accent:{{#..}}; /* ...rest... */
}
```

## Applying in code
- Ground `--color-paper`; text `--color-ink`; secondary text `--color-graphite`;
  hairlines/dividers `--color-line`; panels `--color-mist`.
- **Accent once per view.** {{--color-accent}} is a spotlight (one CTA, one active
  state, one highlight) — never a section background or a second text colour.
- Type: `--font-sans` for UI/headings/body, `--font-mono` for labels, code, metadata.
  Tight tracking on large headings, +0.12em on small uppercase labels.
- Radius {{--radius-*}}; base spacing {{unit}}.

## Logo usage  (assets/ ships the SVGs)
- Default: **{{primary lockup}}** ({{wordmark-ink.svg}}). Symbol-only
  ({{mark-ink.svg}}) only where the name is already obvious (favicon, avatar).
- On dark or accent grounds use the **-white** variant. Never grey-on-grey.
- Clear space ≥ {{1 mark-height}} all sides. Minimum {{24px}}.
- Never: recolour off-palette, stretch/squash, rotate, outline, add effects, crowd.

## Voice & tone
- **{{Primary register}}** (site/product/docs): {{plain, declarative, calm}}.
  e.g. "{{calm sample}}".
- {{**Secondary register** (social) if any: {{deadpan/technical}}. e.g. "{{sample}}".
  Boundary: never mix them — {{a joke on the landing page reads as a bug}}. See
  {{[[brand-social-voice]]}}.}}

## Accessibility
- {{--color-ink}} on {{--color-paper}} ≈ {{ratio}} (AAA). Passing pairs: {{list}}.
- {{--color-accent}} is a **fill**, not white-text-on-accent, and fails as small text
  on white — use {{#darker}} for accent-coloured type.

## Updating the brand
- Change token **values**, never names — a rebrand is a value swap.
- Regenerate marks with the `brand-book` skill's `scripts/svgkit.py` (extract /
  recolor / slice-row); keep `assets/` and the book in sync.
- Do not introduce a second accent. If a new colour is truly needed, pull it from the
  same scene and demote it to a semantic state (success/warning), not a brand accent.
````

After writing it, tell the user the skill exists and how to invoke it
(`/{{brand-slug}}-brand`), and that it lives with the brand's repo so it ships with
the code.
