# Design system

## Design tokens (create these at file level, once)

Use Paper `create_tokens`. Follow the Tailwind v4 namespaces. Order colours
semantically: neutrals light→dark, then primary (ink), then accent last.

```
# fonts
--font-sans        <Display/body family>          e.g. Geist
--font-mono        <mono family>                   e.g. Geist Mono

# colours (roles, not just values)
--color-paper      #FFFFFF   ground / walls
--color-mist       <tint of paper>  panel & tile fill      e.g. #F4F3F2
--color-line       <hairline>       dividers               e.g. #E6E4E7
--color-slate      <light neutral>                          e.g. #A8A5AD
--color-graphite   <mid neutral>    captions / metadata     e.g. #737278
--color-ink        <primary>        text, marks             e.g. #38353C
--color-accent     <the one accent> once per view           e.g. #FF6B4A

# type scale
--text-label 11px  --text-caption 13px  --text-body 16px
--text-subtitle 20px  --text-title 32px  --text-display 64px  --text-mega 180px

# weights   --font-weight-regular 400 / -medium 500 / -semibold 600 / -bold 700
# tracking  --tracking-tight -0.02em / -normal 0 / -label 0.12em
# leading   --leading-tight 1.05 / -snug 1.3 / -body 1.55
# radius    --radius-sm 4px / -md 8px / -lg 16px
# plus one --space-*, one --breakpoint-*, one --container-* to cover the namespaces
```

Name tokens by **role**, not hue — `--color-ink` / `--color-accent`, so a rebrand is
a value change, not a rename. The companion skill re-exports this exact set
(`references/companion-skill.md`), generated from `brand.json` (`brand-json.md`).

## Colour: roles, oklch, print

- The palette is **seven semantic roles** (from `brand.json`): background, surface,
  border, muted, foreground, accent (+ optional accent-secondary as a semantic state
  only). They map 1:1 to our tokens — background→`--color-paper`, surface→`--color-mist`,
  border→`--color-line`, muted→`--color-graphite`, foreground→`--color-ink`,
  accent→`--color-accent`; keep `--color-slate` as a light neutral if the ramp needs it.
- Carry **oklch** next to every hex (enables tints and programmatic light/dark).
- For any colour used in print, also record **CMYK** (and Pantone if the brand has one)
  on the Colour spread — screen hex ≠ press output.

## Iconography (if the brand uses an icon set)

Note the system on the Logo or a dedicated spread: source/family, stroke width, grid
size, corner radius, and fill vs. outline — so product icons stay on-system.

## Type

- One family carries display + body (a neutral grotesk reads as a spec sheet yet
  warms up as a headline). One mono for labels, specs, metadata, code.
- **px** for font-size, **em** for letter-spacing, **px** for line-height (Paper).
- Maximise contrast: heavy display next to light mono labels. Tight tracking on big
  sizes (−2 to −3%), open tracking on small caps/mono labels (+12%).
- Confirm availability with `get_font_family_info` before styling. Prefer families
  already loaded in the file.

## Grid math (3×4)

- Artboards: `1440×900`, white, `display:flex; flex-direction:column`.
- Gutters inside content: `56px` side, `48–64px` top. Column split via `flex` +
  `border-right:1px solid --color-line`.
- Place spread 1, build it, then `duplicate_nodes` ×N. Position with `update_styles`
  `left`/`top` = the world coords above. `left/top` on a top-level artboard set its
  canvas position directly; verify with `get_children(root)`.
- If you add/remove a spread later, you must reflow (move the affected artboards) so
  canvas order still equals reading order, then renumber page footers + section
  labels. The PDF exporter orders purely by position.

## Accent discipline

- The accent appears as: the **section-marker diamond** on every spread (persistent,
  systematic) **plus one** deliberate moment per spread. That's it.
- Everything else is ink / graphite / slate on paper / mist. Uniform mono-label
  colour across a set reads as intent; one odd accent reads as an accident.

## Review checklist (run after every spread — screenshot, critique, fix)

- **Spacing** — deliberate rhythm; tight to group, generous to breathe; no accidental
  voids and no cramping.
- **Typography** — nothing unreadable; strong step between title / body / caption;
  small text (<16px) has enough contrast.
- **Contrast** — text passes at a glance; no element melting into its ground.
- **Alignment** — repeated rows share vertical lanes (fixed-width slots for icons /
  numbers / trailing labels, `flex-shrink:0`); trace a line through them.
- **Artboard fit** — nothing clipped; if content overflows, switch the artboard to
  `height:"fit-content"` rather than guessing a taller fixed height.
- **Consistency across spreads** — page numbers `NN / total`, section numbers,
  clear-space value, tagline wording all agree. This is where brand books rot; audit
  it before export.
- **Accent budget** — count the accent uses on the spread; diamond + one moment.

## Mood / palette (only if the brand has no defined palette)

Commit to a physical **mood word** first (mineral, bookish, gallery, nocturnal,
signage…), then derive each colour from an object in that scene. High-chroma accent →
pure-white ground. Muted/earth palette → a tinted ground from the same scene. One
intense colour beats five. Avoid the tired warm-off-white × terracotta combo and
navy/charcoal × electric-purple SaaS cliché.
