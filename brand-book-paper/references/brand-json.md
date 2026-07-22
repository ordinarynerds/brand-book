# brand.json — the single source of truth

One machine-readable file captures the whole brand. **Everything else is generated
from it** — the book spreads, the companion `<brand>-brand` skill, and the token files
(`tokens.css` / `tokens.json` / Tailwind `@theme`). Author `brand.json` once (from the
brief or by measuring a live site — see `intake.md`), keep it in the companion skill,
and regenerate downstream artifacts from it so the book and the code never drift.

> Why: a brand book and a code-facing token file that are hand-kept in two places
> always diverge. Derive both from `brand.json` and they can't.

## Schema

```jsonc
{
  "name": "Acme",
  "tagline": "one-line brand tagline",
  "mission": "one sentence — why the brand exists",
  "vision": "one sentence — the future it's after",
  "values": ["Value — brief gloss", "..."],           // 3–5; become Brand Principles
  "audience": "who it's for (primary; secondary)",
  "sourceUrl": "https://acme.com",

  // COLOUR — seven semantic roles + hex + oklch + name + usage.
  // Add optional cmyk/pantone for print. Accent is the ONE spotlight.
  "colors": [
    { "role":"background","hex":"#FFFFFF","oklch":"oklch(100% 0 0)",    "name":"Paper",    "usage":"ground / walls" },
    { "role":"surface",   "hex":"#F4F3F2","oklch":"oklch(96% .002 60)", "name":"Mist",     "usage":"panels, tiles" },
    { "role":"border",    "hex":"#E6E4E7","oklch":"oklch(91% .004 310)","name":"Line",     "usage":"hairlines, dividers" },
    { "role":"muted",     "hex":"#737278","oklch":"oklch(52% .006 310)","name":"Graphite", "usage":"captions, metadata" },
    { "role":"foreground","hex":"#38353C","oklch":"oklch(30% .008 320)","name":"Nerd Ink", "usage":"text, marks",
      "cmyk":"0 4 0 76","pantone":"Black 7 C" },
    { "role":"accent",    "hex":"#FF6B4A","oklch":"oklch(70% .18 35)",  "name":"Signal Coral","usage":"one moment per view (FILL)",
      "accentText":"#E24E2E", "cmyk":"0 58 71 0" }
    // optional: "accent-secondary" — only if a semantic-state colour is genuinely needed
  ],

  "typography": {
    "display": { "family":"Geist","fallbacks":["system-ui","sans-serif"],"weights":[500,600,700],"notes":"headlines + body" },
    "body":    { "family":"Geist","fallbacks":["system-ui","sans-serif"],"weights":[400,500] },
    "mono":    { "family":"Geist Mono","fallbacks":["ui-monospace","monospace"],"weights":[400,500],"notes":"labels, code, metadata" },
    "scale":   { "display":64,"title":32,"subtitle":20,"body":16,"caption":13,"label":11 },
    "tracking":{ "tight":"-0.02em","label":"0.12em" }
  },

  "logo": {
    "primary":"assets/wordmark-ink.svg",                 // best vector lockup
    "symbol":"assets/head-ink.svg",                       // the mark extracted from the wordmark
    "variants":["wordmark-white.svg","head-white.svg","head-accent.svg"],
    "clearSpace":"1 head-height","minSize":"24px",
    "donts":["recolour off-palette","stretch/squash","rotate","outline","effects","crowd"]
  },

  "mascot": { "has":true,"set":"assets/faces-*.svg","count":8,"notes":"rotate for variety, never redraw" },

  "iconography": { "style":"outline","stroke":"1.5px","grid":"24px","radius":"2px","source":"Tabler" },

  "voice": {
    "adjectives":["plain","calm","confident","dryly funny"],
    "weAre":  ["Plain","Declarative","Specific"],
    "weAreNot":["Clever for its own sake","Hypey","Vague"],
    "vocabulary": { "use":["ship","build","plain"], "avoid":["guru","rockstar","synergy","revolutionary"] },
    "registers": [
      { "id":"primary","name":"Manifesto","where":"site, product, docs","how":"calm, declarative, no jokes","sample":"We do software. That's it." },
      { "id":"social","name":"Nerd","where":"X / social only","how":"deadpan, hyper-technical, one landed joke","sample":"PATCH NOTES — …" }
    ],
    "boundary":"never mix registers — a joke on the landing page reads as a bug"
  },

  "imagery": { "style":"one line","subjects":["…"],"treatment":"…","avoid":["clichés"],"samples":["imagery/hero.png"] },

  "layout": { "radius":{"sm":"4px","md":"8px","lg":"16px"}, "spacingBase":"8px", "gutter":"56px",
              "posture":["3–5 observed rules — e.g. full-width sections, hairline dividers"] },

  "applications": ["banner","avatar","business card","sticker","social header 1500×500","email signature"],

  "notes":"provenance — which values were measured vs. inferred (mark inferred ones)"
}
```

## Rules

- **Never invent colours from memory.** Each `hex` is measured (a live site — see
  `intake.md`) or explicitly chosen in the brief. Derive a missing role from a measured
  one with `oklch()` and say so in `usage`. An LLM left alone regresses to the mean
  (Inter, an indigo accent, a purple gradient) — off-brand for everyone.
- **Roles, not hues.** Style through the seven roles so a rebrand is a value change.
  Our token names map 1:1: background→`--color-paper`, surface→`--color-mist`,
  border→`--color-line`, muted→`--color-graphite`, foreground→`--color-ink`,
  accent→`--color-accent` (+`--color-accent-text` from `accentText`). Keep a light
  neutral (`--color-slate`) between border and muted if the ramp needs it.
- **One accent.** Exactly one `accent`. Add `accent-secondary` only as a semantic state
  (success/warning), never as a second brand colour.
- **oklch alongside hex** for every colour (enables programmatic light/dark + tints).
- **Provenance.** Mark any value you inferred rather than measured, in `usage`/`notes`.

## What derives from it

| Artifact | From `brand.json` |
|---|---|
| Book tokens / spreads | `colors`, `typography`, `logo`, `mascot`, `layout`, `voice`, `values`, `audience` |
| `tokens.css` / `tokens.json` / Tailwind `@theme` | `colors` (→ `--color-<role>`), `typography`, `layout.radius/spacing` |
| Companion skill body | the whole file, prose-rendered (`companion-skill.md`) |
| Quick-reference card | `name`, top colours, fonts, `logo.minSize/clearSpace`, `voice.weAre` |

Keep `brand.json` in the companion skill (`<brand>-brand/brand.json`) as the artifact
of record; regenerate the rest when it changes.
