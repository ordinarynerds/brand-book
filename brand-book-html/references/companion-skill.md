# Generating the companion brand skill

Every brand book ships with a `<brand>-brand/` skill so a coding agent can apply,
enforce, and update the brand in the product's codebase. It is the operational half of
the deliverable — the book is the reference, the skill is the API. It is generated from
`brand.json` (`brand-json.md`), the single source of truth.

Create it inside the brand's own repo at `.claude/skills/<brand>-brand/` (so it travels
with the code). Mirror a finished one if you have it.

## Structure

```
<brand>-brand/
  SKILL.md
  brand.json                 # the source of truth (brand-json.md)
  tokens.css                 # :root { --color-<role> … }  — generated from brand.json
  tokens.json                # { color, font, radius, spacing } — generated
  assets/                    # the real, final SVGs (durable home for the marks)
  hooks/enforce.sh           # OPTIONAL brand-enforcement hook (see below)
```

Ship the **real token files**, not just paste-in blocks — `tokens.css` (`:root` +
Tailwind `@theme`) and `tokens.json`, both derived from `brand.json.colors` (→
`--color-<role>`), `typography`, and `layout`. Regenerate them whenever `brand.json`
changes. Copy the finalized SVGs into `assets/`. Keep SKILL.md the human-readable index.

## What SKILL.md must contain

1. **Frontmatter** — `name: <brand>-brand`; `description` packed with triggers (the
   brand name, "apply/update `<brand>` brand", "brand colors/fonts/tokens", "on-brand",
   "style this like `<brand>`"); `metadata.surface: engineering`.
2. **Tokens** — point at `tokens.css`/`tokens.json`; restate the role of each colour
   and the accent-once rule.
3. **Applying in code — two cases:**
   - *New surface:* use the role tokens directly (background/foreground/accent…).
   - *Existing codebase:* **map its tokens onto the brand roles by evidence, not by
     value.** Infer each source token's role from usage (name, position — bg/text/
     border/focus-ring, contrast pairing, reuse across primary buttons/active nav).
     Map only when the evidence is role-based; leave ambiguous ones **unmatched for a
     human to review** — never silently collapse two source tokens onto one brand token
     or invent a token. (Record collisions/unmatched explicitly.)
4. **Logo & mascot usage** — which asset for which context, clear space, min size,
   reversal rules, the don'ts — pointing at `assets/`.
5. **Voice & tone** (the enforceable part — below).
6. **Accessibility** — the passing text/bg pairs + the accent-as-text fallback.
7. **Update protocol** — edit `brand.json` values (never role names), regenerate
   tokens + marks, keep book and skill in sync, never add a second accent.

## Voice & tone — make it enforceable

Voice is the personality (constant); tone flexes by context. Encode both so an agent
can *apply* them, not just admire them:

- **We Are / We Are Not** table (4+ rows) — the identity anchor, from
  `brand.json.voice.weAre/weAreNot`.
- **Vocabulary** — words to `use` / words to `avoid`.
- **Registers + boundary** — the calm primary vs. any loud/social register, and the
  "never mix them" rule (link a separate social-voice skill if one exists).
- **Tone-by-context matrix** — formality / energy / technical-depth per context
  (marketing, docs, error, empty state…).
- **UI copy rules** (so product text is on-brand by construction):
  - Buttons: action verb, specific ("Create project"), no period, no "!".
  - Errors: what happened → why (if useful) → what to do next. No "Oops/Sorry".
  - Empty states: what goes here + the action to fill it.
  - Active voice; drop "please"; be specific ("3 errors" not "some errors").
  - Dashes: hyphen for compounds/ranges, em-dash for interruption; sentence case
    for body, title case for headings; no ALL-CAPS except acronyms.
- **Strictness** — read `.claude/<brand>-brand.local.md` for `strictness: strict |
  balanced | flexible` and `always-explain`. On conflict between a request and the
  guidelines, explain the tradeoff and default to adapting with a note (unless strict).

Persist generated guidelines at `.claude/<brand>-brand-guidelines.md` (archive any
prior version to `…-YYYY-MM-DD.md`). An enforcement pass loads them and, when
`always-explain`, notes which rules it applied.

## Optional: a brand-enforcement hook

Ship `hooks/enforce.sh` and a `settings.json` snippet so the brand nudges itself in the
repo — pick the lightest that fits:

- **UserPromptSubmit** — inject a one-line reminder + the token file path when the
  prompt touches UI/styles, so the agent has the palette in context.
- **PostToolUse (Edit|Write)** — lint the touched file for **off-palette hex** (any
  colour not in `tokens.json`) and **banned vocabulary**, and surface a warning (not a
  hard block, unless `strictness: strict`).

```jsonc
// .claude/settings.json (merge, don't overwrite)
{ "hooks": { "PostToolUse": [ { "matcher": "Edit|Write",
  "hooks": [ { "type": "command",
    "command": ".claude/skills/<brand>-brand/hooks/enforce.sh" } ] } ] } }
```
Keep the hook dependency-free and fast; read the allowed values from `tokens.json` so it
stays in sync with `brand.json`. Make it advisory by default — a brand hook that hard-
blocks edits gets disabled.

## Template

`{{brand}}` is whoever the brand belongs to — a company, a product, or you. Fill the
`{{…}}` (most come straight from `brand.json`) and delete what doesn't apply.

````markdown
---
name: {{brand-slug}}-brand
description: >-
  {{Brand}}'s brand system for agentic coding — colours, typography, logo usage,
  voice. Use when building or editing {{Brand}}'s product, site, emails, or collateral,
  or when the user says "apply {{Brand}} brand", "make this on-brand", "{{Brand}}
  colours/fonts/tokens", or "style this like {{Brand}}".
metadata: { surface: engineering, version: 1.0.0 }
---

# {{Brand}} Brand

{{one line: what {{Brand}} is + the palette in a sentence}}. Source of truth:
`brand.json`. Tokens: `tokens.css` / `tokens.json`. Book: `{{path}}.pdf|.html`.

## Tokens
Use `tokens.css` (`:root` + Tailwind `@theme`). Roles: `--color-paper` (ground),
`--color-ink` (text/marks), `--color-graphite` (secondary), `--color-line` (dividers),
`--color-mist` (panels), `--color-accent` (ONE spotlight — a fill; `--color-accent-text`
for accent-coloured type on white).

## Applying in code
- New surfaces: use the role tokens directly; accent **once per view**.
- Existing codebase: map its tokens to these roles **by usage evidence**, not by value;
  leave ambiguous tokens unmatched for review — never silently collapse or invent.
- `--font-sans` for UI/headings/body, `--font-mono` for labels/code/metadata.

## Logo & mascot ( assets/ )
Default {{wordmark-ink.svg}}; symbol-only {{head-ink.svg}} where the name is obvious.
`-white` on dark/accent. Clear space ≥ {{1 mark-height}}, min {{24px}}. Never recolour,
stretch, rotate, outline, add effects, or crowd.

## Voice & tone
We Are: {{…}} · We Are Not: {{…}}. Use: {{words}} · Avoid: {{words}}.
- {{Primary register}} (site/product/docs): {{calm, declarative}} — "{{sample}}".
- {{Social register if any}} — see {{[[brand-social-voice]]}}; never mix registers.
UI copy: action-verb buttons, no "!"; errors say what/why/next; active voice; specific.

## Accessibility
{{ink}} on {{paper}} ≈ {{ratio}} (AAA). {{accent}} is a fill — use {{accentText}} for
accent-coloured text on white.

## Updating
Edit `brand.json` values (never role names) → regenerate `tokens.*` + marks (svgkit) →
keep book + skill in sync → no second accent (new colour = a semantic state only).
````

After writing it, tell the user how to invoke it (`/{{brand-slug}}-brand`) and that it
ships with the code.
