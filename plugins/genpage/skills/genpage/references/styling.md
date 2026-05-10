# Styling reference

The page renders inside an iframe with no shared styles or scripts — every dependency must be inlined as a CDN tag.

## Mandatory `<head>`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="<one-line summary>">
  <meta name="generator" content="genpage">
  <meta property="og:title" content="<report title>">
  <meta property="og:description" content="<one-line summary>">
  <meta property="og:type" content="article">
  <title><report title> — GenPage</title>
  <!-- chosen CDN tags here -->
</head>
```

`<title>` always follows `<report title> — GenPage`. No analytics, tracking pixels, or third-party meta tags.

## Framework selection (model decides)

Pick the smallest stack that delivers the content. Every extra CDN is a network hop inside the iframe.

| Need | Library | CDN |
|---|---|---|
| Utility-first layout | Tailwind CSS | `https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4` |
| Component classes (card, badge, stat, table, btn, alert, tabs) | DaisyUI | `https://cdn.jsdelivr.net/npm/daisyui@5/daisyui.css` |
| Rich Material components | MUI (UMD) | `https://unpkg.com/@mui/material@5/umd/material-ui.production.min.js` |
| Show/hide, toggles, tabs | Alpine.js | `https://cdn.jsdelivr.net/npm/alpinejs@3/dist/cdn.min.js` |
| Complex stateful UI | React + ReactDOM | `https://unpkg.com/react@18/umd/react.production.min.js` (+ ReactDOM) |
| Bar/line/pie/area charts | Chart.js | `https://cdn.jsdelivr.net/npm/chart.js@4` |
| Force graphs, treemaps, custom SVG | D3.js | `https://cdn.jsdelivr.net/npm/d3@7` |
| Flowcharts, sequence, ER, state | Mermaid | `https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js` |
| Icons | Lucide | `https://unpkg.com/lucide@latest` |

### Decision rules

- **Lean** → plain HTML + Tailwind/DaisyUI; no JS unless data is graph-shaped (Mermaid only).
- **Standard** → Tailwind + DaisyUI as default. Add Chart.js or Mermaid when data warrants. Alpine for interactivity.
- **Deep** → full palette as the content justifies (React/Alpine, D3/Chart.js, Mermaid, Lucide).
- Prefer DaisyUI zero-JS patterns (radio tabs, `<details>` collapse, stat cards) before adding Alpine or React.
- Prefer Alpine over React unless you genuinely need cross-component state.
- Reach for D3 only when Chart.js can't express the visual.

### Mermaid

```html
<script>mermaid.initialize({ startOnLoad: true });</script>
<div class="mermaid">
graph TD
  A[Entry] --> B[Step] --> C[Result]
</div>
```

### Lucide

```html
<script>lucide.createIcons();</script>
<i data-lucide="check-circle"></i>
```

## Colors

Use any palette that fits — Tailwind/DaisyUI utilities (`bg-slate-900`, `text-emerald-500`, `bg-primary`) or hex/rgb. Keep contrast at WCAG AA (4.5:1 body, 3:1 large text/UI). Use a small consistent palette, not a rainbow.

## Layout

- Fluid, responsive. CSS Grid, Flexbox, or Tailwind responsive utilities (`sm:`, `md:`, `lg:`). No fixed-pixel layouts.
- Centered container, ~`max-w-6xl`/`max-w-7xl`, generous padding (`px-4 sm:px-6 lg:px-8`).
- Mobile-first; single-column on small, multi-column when there's room.
- Cards/tables/charts must reflow or scroll — never overflow the viewport.
- Typography: ≥16px body, line-height 1.5–1.7, line length 60–80ch.

## Scrollbars

Default browser scrollbars usually clash with the page's palette. Style them — both the page and any inner scrollable container — to match.

- Style WebKit/Blink (`::-webkit-scrollbar*`) and Firefox (`scrollbar-width`, `scrollbar-color`).
- Track blends with surface; thumb is a muted variant of the page's primary/neutral, slightly stronger on hover.
- Slim but visible (8–12px). Don't hide them on desktop.
- Adapt to dark mode if the page uses one.

```css
html { scrollbar-width: thin; scrollbar-color: theme(colors.slate.400) transparent; }
*::-webkit-scrollbar { width: 10px; height: 10px; }
*::-webkit-scrollbar-track { background: transparent; }
*::-webkit-scrollbar-thumb { background: theme(colors.slate.300); border-radius: 9999px; }
*::-webkit-scrollbar-thumb:hover { background: theme(colors.slate.500); }
```

## Motion — keep it minimal

Heavy motion distracts from the content. The page is a report, not a landing page.

- Allowed: subtle hover transitions (≤200ms), simple fade/slide on tab/modal open, Chart.js's default entry animation.
- Avoid: animated background gradients, marquee, auto-carousels, particle effects, scroll-jacking, anything looping indefinitely.
- Always honor `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```
