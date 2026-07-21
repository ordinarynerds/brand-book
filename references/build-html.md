# Build as an HTML artifact (default)

One **self-contained** `.html` file that renders all 11 spreads, embeds its fonts and
SVG assets, scales to any viewport, and prints one-spread-per-page to PDF. It can be
opened locally, emailed, or published as a Claude **Artifact** (strict CSP: no
external requests, so everything is inlined).

Load `artifact-design` for the craft fundamentals; this file is the brand-book-specific
structure on top of them.

## The shape

```
<style> … tokens + components … </style>
<main class="book">
  <section class="spread"> … 11 of these … </section>
</main>
<script> … fit-to-viewport … </script>
```

Author with the same layouts as `spread-map.md` — they were already flexbox. Write
one spread, screenshot/open it, self-review (design-system checklist), then the rest.
Keep each `.spread` a real page, not a scroll section.

## Tokens (`:root`)

Put the full token set from `design-system.md` as CSS custom properties on `:root`
and style everything through them. A brand book is **single-theme paper** — do not add
a dark mode; instead sit the white spreads on a neutral gallery ground:

```css
:root{
  --font-sans:"Geist", system-ui, sans-serif;
  --font-mono:"Geist Mono", ui-monospace, monospace;
  --color-paper:#FFFFFF; --color-mist:#F4F3F2; --color-line:#E6E4E7;
  --color-slate:#A8A5AD; --color-graphite:#737278; --color-ink:#38353C;
  --color-accent:#FF6B4A; --color-accent-text:#E24E2E;
  --gallery:#E7E5E4;                 /* the ground the pages sit on */
}
html,body{margin:0;background:var(--gallery);}
```

## The spread as a page

Each spread is a fixed **1440×900** box (the design size) so pixel values from the
Paper layouts port 1:1. Scale the whole book to the viewport with **`zoom`** (it
reflows, unlike `transform`, so page heights stay correct), set by a tiny script.
Reset to 1 for print.

```css
.book{display:flex; flex-direction:column; align-items:center; gap:28px; padding:28px 0;}
.spread{
  width:1440px; height:900px; flex:none;
  background:var(--color-paper); color:var(--color-ink);
  font-family:var(--font-sans);
  display:flex; flex-direction:column; overflow:hidden;
  box-shadow:0 1px 3px rgba(0,0,0,.06), 0 12px 40px rgba(0,0,0,.08);
}
.book{ zoom: var(--fit, 1); }               /* set by script below */

@media print{
  html,body{background:#fff;} .book{zoom:1; gap:0; padding:0;}
  .spread{box-shadow:none; break-after:page;}
  @page{ size:1440px 900px; margin:0; }
}
```

```html
<script>
  const fit = () => {
    const s = Math.min(1, (Math.min(window.innerWidth, 1520) - 56) / 1440);
    document.documentElement.style.setProperty('--fit', s);
  };
  addEventListener('resize', fit); fit();
</script>
```

Chrome + component classes (build once, reuse on every spread):

```css
.rh{display:flex;justify-content:space-between;align-items:center;
    padding:26px 56px;border-bottom:1px solid var(--color-line);flex:none;}
.ft{display:flex;justify-content:space-between;align-items:center;
    padding:20px 56px;border-top:1px solid var(--color-line);flex:none;}
.content{flex:1;display:flex;min-height:0;}          /* the exhibit area */
.mono{font-family:var(--font-mono);font-size:11px;letter-spacing:.12em;
      text-transform:uppercase;color:var(--color-graphite);}
.diamond{width:8px;height:8px;background:var(--color-accent);transform:rotate(45deg);flex:none;}
.title{font-size:32px;font-weight:600;letter-spacing:-.02em;}
.left{padding:64px 48px 56px 56px;border-right:1px solid var(--color-line);
      display:flex;flex-direction:column;justify-content:space-between;}
```

A spread then reads:

```html
<section class="spread">
  <header class="rh">
    <span style="display:flex;gap:12px;align-items:center">
      <img class="mark" src="mark-ink.svg" alt="" style="width:21px;height:21px">
      <span class="mono" style="color:var(--color-ink)">01 · Introduction</span>
    </span>
    <span class="mono">Ordinary Nerds — Brand Book</span>
  </header>
  <div class="content"> … left column + exhibit … </div>
  <footer class="ft"><span class="mono">brand.com</span><span class="mono">01 / 11</span></footer>
</section>
```

## Fonts — inline, don't link (CSP)

The Artifact CSP blocks font CDNs, so a `<link>` to Google Fonts silently falls back.
Embed the brand faces as `@font-face` **data URIs** (a latin-subset variable woff2 is
usually ~30KB). Base64 a local woff2:

```bash
b64=$(base64 -i geist-latin-wght-normal.woff2 | tr -d '\n')
# then write:  src:url("data:font/woff2;base64,$b64") format("woff2");
```
```css
@font-face{font-family:"Geist";font-style:normal;font-weight:100 900;
  font-display:swap;src:url("data:font/woff2;base64,…") format("woff2");}
@font-face{font-family:"Geist Mono";font-weight:100 900;
  src:url("data:font/woff2;base64,…") format("woff2");}
```
Always keep a system fallback in the stack (`system-ui`, `ui-monospace`) so the page
survives if a face is missing. If the brand font isn't available locally, pick the
closest system stack and tell the user it's a substitute.

## Assets — inline, don't reference

External/relative image paths won't resolve inside an Artifact. Two options:
- **Inline `<svg>…</svg>`** for the marks (best for crisp scaling, small marks).
- **`<img src="data:image/svg+xml;base64,…">`** for everything (uniform, simple).

Author with plain relative `src="mark-ink.svg"` (readable), keep the SVGs beside the
HTML, then run `scripts/embed_assets.py in.html --out book.html` to inline every local
`<img src>`, CSS `url()`, and `@font-face` as data URIs → one portable file. Publish
that file.

## Generative bits

The construction plate (spread 03), grid, guide circle, coral optical axis: generate
as an inline `<svg>` (see `asset-pipeline.md` generator) or draw on a `<canvas>`. Don't
hand-author long path data.

## Publish / export

- **As an Artifact:** call the Artifact tool on the embedded `.html` — set a stable
  `<title>` (e.g. "<Brand> — Brand Book"), a one-line `description`, and a `favicon`
  emoji. It starts private; the user chooses to share. Redeploy to the same URL by
  passing the same file path.
- **As a PDF:** open the file and Print → Save as PDF (the `@page` + `break-after`
  rules give one landscape spread per page). This replaces Paper's PDF export.
- **As a file:** the single `.html` is already the deliverable — it opens in any
  browser offline.

## Fidelity checklist (in addition to the design-system review)

- Spread scales cleanly at phone / tablet / desktop widths; body never scrolls
  sideways; each `.spread` keeps its 16:10.
- Fonts render as the brand face, not a fallback (check a heading's shapes).
- Every asset shows (no broken-image icons) → it embedded.
- Print preview shows 11 clean landscape pages, no chrome bleed, no blank pages.
- `prefers-reduced-motion` respected; focus states visible on any links.
