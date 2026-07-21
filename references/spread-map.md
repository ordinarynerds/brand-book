# Spread map

11 landscape spreads, **1440×900**, laid out in a **3×4 canvas grid** (3 columns ×
4 rows, last row has 2). Reading order = canvas position (top→bottom, left→right) so
`export_combined_pdf` pages come out 1→11.

Grid pitch: **1520px** horizontal (1440 + 80 gap), **980px** vertical (900 + 80).
With spread 1 at world (−720, −450):
- cols x: −720, 800, 2320  ·  rows y: −450, 530, 1510, 2490

| # | Section | Spread |
|---|---------|--------|
| 01 | Introduction | What is <Brand>? — manifesto lead + hero mark |
| 02 | Introduction | Brand Principles (2×2) |
| 03 | Logo System | Symbol Concept (construction) |
| 04 | Logo System | Logo Overview (lockups + reversal) |
| 05 | Logo System | Do's & Don'ts (misuse grid + clear space + min size) |
| 06 | Mascot / Illustration | The set (grid) — *drop if the brand has no mascot; renumber* |
| 07 | Typography | Typeface (specimen + weight ladder) |
| 08 | Typography | Hierarchy (type scale table) |
| 09 | Colour System | Core palette + neutral ramp + usage/a11y |
| 10 | Voice & Tone | Register(s) + boundary rule + examples |
| 11 | Applications | Real collateral (banner, avatar, card, sticker) |

If the brand has no mascot, cut spread 06 and renumber to 10 spreads (3×4 minus 2).
A cover + colophon can bookend it if the brand wants a "bound" feel — offer, don't
assume (it breaks the clean grid).

## Shared chrome (build once on spread 1, then duplicate)

Every spread is: **[running-head] · [content flex:1] · [footer]**, artboard is a
white flex column.

- **Running-head** (top): `border-bottom:1px solid --color-line`, `padding:26px 56px`,
  row space-between. Left = the symbol mark at ~21px + mono section label
  (`01 · Introduction`, 11px, +0.12em, uppercase, ink). Right = mono
  `<Brand> — Brand Book` (11px, +0.12em, uppercase, graphite).
- **Footer** (bottom): `border-top:1px solid --color-line`, `padding:20px 56px`,
  space-between mono 11px graphite: left = `brand.com`, right = page `01 / 11`.
- **Section marker**: a small accent diamond (`8px, rotate(45deg)`) before every
  spread title — this is the accent's persistent through-line. The *one* deliberate
  accent moment per spread is separate (a mascot tile, the coral card, a callout rule).

Reuse the chrome across all spreads — a shared class/partial in HTML, or duplicate the
first artboard in Paper. Only the section label and page number change per spread. The
mechanics live in your build reference (`build-html.md` / `build-paper.md`); this file
is medium-neutral.

## Per-spread layout & copy

Default layout is a **left column** (title block + supporting copy, `border-right`)
and a **right column** (the exhibit). Some spreads go full-width — say so below.

**01 — What is <Brand>?** Left: accent diamond + `What is <Brand>?` (32/600), a
lead paragraph (18/400), then at the column bottom 2 body paragraphs + the tagline
(20/600 with an ink diamond). Right: the symbol mark, oversized (~400px), centered,
with a mono figure caption (`Fig. 01 — <mark name>, primary mark`).

**02 — Brand Principles.** Left: title + one-line intro + a small bottom note. Right:
a 2×2 grid (flex rows/cells with hairline `border-right`/`border-bottom` making a
cross divider). Each cell: mono index (`P—01`, graphite), principle title (21/600),
2-line body (14, graphite). 4 principles derived from the brand's values.

**03 — Symbol Concept.** Left: title + why-the-mark paragraphs + a mono spec table
(Field 1:1, crown breaks top, optical axis, clear space). Right: a construction plate
— generate a grid SVG (8×8 field, guide circle, dashed baseline, one accent optical
axis, corner ticks) as a file, `<img>` it full-bleed in a ~520px square, and place the
symbol centered on top. See asset-pipeline for the grid generator.

**04 — Logo Overview.** Left: title + "horizontal lockup is default" + a usage
checklist (✓ clear space, ✓ ink/reversed, ✕ don't distort — the ✕ in accent). Right:
a large primary-lockup tile (wordmark on `--color-mist`), and a row below with a
symbol tile (mist) + a reversed tile (wordmark-white on ink). Mono corner labels.

**05 — Do's & Don'ts.** Left: title + intro + a **clear-space** diagram (mark in a
mist tile with a dashed inset boundary + caption) + **min-size** marks (e.g. 40px /
24px with labels). Right: a 2×2 "Never do this" grid, white tiles with `--color-line`
border, each a *mis-used* mark + an accent `✕` badge + caption: recolour (off-brand
head), stretch (`transform:scaleX(1.4)`), rotate (`transform:rotate(-14deg)`),
low-contrast (a pale slate head). Generate the off-brand/pale variants with svgkit
recolor.

**06 — Mascot set.** Left: title + intro + a big count (`08 / faces, one studio`).
Right: a 4×2 grid of tight, **common-height** face slices (see asset-pipeline
slice-row). Make one tile the accent treatment (white mark on accent bg, "Avatar")
and one the reversed (white on ink, "On ink"); the rest ink-on-mist. Number them.

**07 — Typeface.** Left: title + why-this-face + a family list (each face + role).
Right (space-between column): character set (upper / lower / numerals+symbols), a
weight ladder (one sample line repeated at 400/500/600/700 with mono weight labels),
and a giant specimen of the typeface name (~150px).

**08 — Hierarchy.** Full-width. Header band (title + right-aligned intro,
`border-bottom`). Then a type-scale table, rows distributed `space-between`: each row
has a fixed ~210px spec lane (mono name + `size · weight · tracking`) and the rendered
sample. Levels: Display 64 · Title 32 · Subtitle 20 · Body 16 · Caption 13 · Label 11
(mono, uppercase, tracked).

**09 — Colour System.** Left: title + palette philosophy + a proportion bar
(ground/ink/accent ≈ 64/28/8) + the a11y rule + a mini swatch legend at the bottom.
Right: two big core cards (ink + accent) each with name / hex / RGB / role, then a
neutral ramp of ~6 swatches (chip + name + hex), light chips get a `--color-line`
border.

**10 — Voice & Tone.** Left: title + intro + a "the one rule" callout
(accent left-border, mist bg) stating the register boundary. Right: two register
cards side by side (calm/primary vs. the loud/social one if it exists) — eyebrow
(where it's used) + name + a real sample + a trait line; then a "same fact, two
registers" comparison row. Keep every sample truthful.

**11 — Applications.** Left: title + intro + a bottom note. Right: a hero application
(rebuild the brand's real banner/social header in vector from the assets), then a
row of smaller apps: app icon (accent bg, white mark, rounded), business card (mist,
wordmark + details), sticker (ink, white mark/face). Mono corner labels.

## Copy register

Calm, plain, declarative, confident. Short sentences. No exclamation, no jokes, no
hype — even for a playful brand, the *book* is the calm artifact. Derive principle
and manifesto copy from the brand's actual values/voice, not filler. If the brand
runs a separate loud voice, it appears only as *quoted samples* on spread 10.

## Optional content — scale to the brand

Add only when the brand has it; don't pad. From `brand.json`:

- **Mission / Vision / Values / Audience** — fold `mission`/`vision`/`audience` into the
  intro spread; `values` become the Brand Principles.
- **Print values** — add CMYK (+ Pantone) rows to the core colour cards for brands that
  print.
- **Iconography** — a small panel (source, stroke, grid, radius, fill/outline) on the
  Logo or Applications spread if `iconography` is set.
- **Social sizes** — in Applications, a mono list of the real avatar/cover dimensions
  (e.g. X 1500×500, LinkedIn 1128×191) beside the banner mock.
- **Quick-reference card** — an optional final (or cover) card: name, the two or three
  key colours (hex), the fonts, `logo.minSize`/`clearSpace`, and the top `voice.weAre`
  words. A one-glance cheat-sheet someone can screenshot.
