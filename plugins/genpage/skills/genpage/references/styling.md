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

Match the framework to the **shape of the content**, not to a "tier." Tailwind handles layout on every page; pick **one** specialised library per concern (one chart lib, one diagram lib, one interactivity lib). Every extra CDN is a network hop inside the iframe — don't load D3 *and* ECharts just because both could work.

### Layout & components (always)

| Need | Library | CDN |
|---|---|---|
| Utility-first layout | Tailwind CSS | `https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4` |
| Component classes (card, badge, stat, table, btn, alert, tabs) | DaisyUI | `https://cdn.jsdelivr.net/npm/daisyui@5/daisyui.css` |
| Icons | Lucide | `https://unpkg.com/lucide@latest` |

Tailwind v4 browser build needs DaisyUI activated explicitly. Put this in `<head>` after the Tailwind script:

```html
<style type="text/tailwindcss">
  @plugin "daisyui" { themes: light --default, dark --prefersdark, business, corporate, night; }
</style>
```

### Interactivity (pick at most one)

| Need | Library | CDN |
|---|---|---|
| Tabs, accordions, toggles | DaisyUI zero-JS patterns (`<details>`, radio tabs) — no library |
| Show/hide, local state, simple bindings | Alpine.js | `https://cdn.jsdelivr.net/npm/alpinejs@3/dist/cdn.min.js` |
| Multi-view dashboard with shared state | React + ReactDOM | `https://unpkg.com/react@18/umd/react.production.min.js` + `https://unpkg.com/react-dom@18/umd/react-dom.production.min.js` |

### Visualisation — choose by what you're rendering

| If the content is… | Use | CDN |
|---|---|---|
| Bar / line / pie / area / scatter | Chart.js | `https://cdn.jsdelivr.net/npm/chart.js@4` |
| Heatmap, sankey, treemap, radar, gauge, candlestick | ECharts | `https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js` |
| Declarative statistical charts from JSON | Vega-Lite | `https://cdn.jsdelivr.net/npm/vega@5` + `https://cdn.jsdelivr.net/npm/vega-lite@5` + `https://cdn.jsdelivr.net/npm/vega-embed@6` |
| Force-directed / network / dependency graphs | Cytoscape.js | `https://cdn.jsdelivr.net/npm/cytoscape@3/dist/cytoscape.min.js` |
| Custom SVG, bespoke viz, geo projections | D3.js | `https://cdn.jsdelivr.net/npm/d3@7` |
| Flowchart, sequence, ER, state, gantt | Mermaid | `https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js` |
| Geographic data, points/regions on a map | Leaflet | `https://cdn.jsdelivr.net/npm/leaflet@1/dist/leaflet.js` + `https://cdn.jsdelivr.net/npm/leaflet@1/dist/leaflet.css` |
| Large interactive data table (sort/filter/paginate) | Tabulator | `https://cdn.jsdelivr.net/npm/tabulator-tables@6/dist/js/tabulator.min.js` + `https://cdn.jsdelivr.net/npm/tabulator-tables@6/dist/css/tabulator.min.css` |

### Content extras

| Need | Library | CDN |
|---|---|---|
| Code snippets with syntax highlighting | highlight.js | `https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11/highlight.min.js` + a theme CSS from the same package |
| Math / equations (LaTeX) | KaTeX | `https://cdn.jsdelivr.net/npm/katex@0.16/dist/katex.min.js` + `https://cdn.jsdelivr.net/npm/katex@0.16/dist/katex.min.css` |

### Decision rules

- **One viz library per page.** If the content needs both a flowchart and a bar chart, that's Mermaid + Chart.js — but never Chart.js + ECharts, or D3 + Cytoscape.
- **Reach down before reaching up.** DaisyUI zero-JS → Alpine → React. Chart.js → ECharts → D3. Don't skip tiers without a concrete reason.
- **Mermaid for diagrams, D3 only for bespoke.** If a flowchart, sequence, ER, state, or gantt fits, use Mermaid. Save D3 for visuals no off-the-shelf library expresses.
- **No JS unless the content needs it.** A static report is HTML + Tailwind + DaisyUI. Don't load Alpine "just in case."

### Legibility floor — never crush content to fit

Every visual element must stay readable at the size it actually renders. If labels would shrink below the floor, **change the layout, not the font size**.

- **Minimum text size**: 12px in charts/diagrams, 14px in body, 11px only for axis ticks.
- **Don't shoehorn long sequences into Mermaid.** A horizontal flow with more than ~6 nodes will compress into illegible pills inside a card. Options instead:
  - Switch direction (`graph TD` top-down) so it grows vertically.
  - Render as a numbered **stepper / breadcrumb list** in plain HTML (DaisyUI `steps`, or a Tailwind flex-wrap row of `rounded-full` chips with `flex-wrap` so they wrap to multiple lines).
  - Group into stages and show a short Mermaid per stage.
- **Wrap, don't scroll horizontally**, for label sequences (route stops, tags, breadcrumbs). Use `flex flex-wrap gap-2` with chips sized to their content.
- **Charts need room.** Minimum chart height 240px; line/bar charts with >10 categories need either rotation, truncation, or a horizontal bar chart instead.
- **Mermaid sizing**: set a minimum width on the container and let it scroll horizontally if needed (`overflow-x-auto`), rather than letting it shrink. Better: pick a different representation.
- **Test the worst case.** If the data could realistically have 20 items, design for 20, not 4.

#### Wrong vs right — long sequence

```html
<!-- WRONG: 16 stops crushed into one Mermaid LR row -->
<div class="mermaid">graph LR; A-->B-->C-->D-->E-->F-->G-->H-->I-->J-->K-->L-->M-->N-->O-->P</div>

<!-- RIGHT: wrapping chip row, readable at any width -->
<ol class="flex flex-wrap items-center gap-2 text-sm">
  <li class="px-3 py-1 rounded-full bg-slate-900 text-white">Cosenza</li>
  <li class="text-slate-400">→</li>
  <li class="px-3 py-1 rounded-full bg-slate-900 text-white">Gallipoli</li>
  <li class="text-slate-400">→</li>
  <!-- … -->
</ol>
```

### Examples

#### Mermaid

```html
<script>mermaid.initialize({ startOnLoad: true });</script>
<div class="mermaid">
graph TD
  A[Entry] --> B[Step] --> C[Result]
</div>
```

#### Lucide

```html
<script>lucide.createIcons();</script>
<i data-lucide="check-circle"></i>
```

#### ECharts

```html
<div id="chart" style="width:100%;height:360px"></div>
<script>
  const c = echarts.init(document.getElementById('chart'));
  c.setOption({
    tooltip: {},
    series: [{ type: 'treemap', data: [{ name: 'A', value: 10 }, { name: 'B', value: 6 }] }]
  });
  window.addEventListener('resize', () => c.resize());
</script>
```

#### highlight.js

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11/styles/github-dark.min.css">
<script>hljs.highlightAll();</script>
<pre><code class="language-ts">const x: number = 1;</code></pre>
```

#### KaTeX

```html
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body)"></script>
<p>Inline: \(E = mc^2\). Block: $$\sum_{i=1}^{n} i = \tfrac{n(n+1)}{2}$$</p>
```

## Visual style — modern dashboard feel

Pages should look like contemporary product UIs (Linear, Vercel, Stripe, Resend, shadcn). The default is **calm, dense, neutral, with hairline structure and soft depth** — not "marketing site" gradients or "bootstrap admin" chrome.

### Aesthetic defaults

- **Surfaces**: layered neutrals. `bg-white` / `bg-slate-50` for the page, `bg-white` cards on light; `bg-zinc-950` page with `bg-zinc-900` cards on dark. Avoid pure `#000` and pure `#fff` cards stacked on each other.
- **Borders**: hairline, low-contrast (`border border-slate-200` light / `border-white/5` or `border-zinc-800` dark). Borders define structure; shadows don't.
- **Radius**: `rounded-xl` (cards, inputs, buttons) or `rounded-2xl` (large surfaces). Never `rounded-full` on cards, never `rounded-none` on interactive elements.
- **Shadows**: soft and small (`shadow-sm`, occasionally `shadow`). No `shadow-2xl`, no glow, no neon.
- **Whitespace**: generous. Card padding `p-5`/`p-6`, grid gaps `gap-4`/`gap-6`, section spacing `space-y-6`/`space-y-8`.
- **Color use**: one accent (DaisyUI `primary` or a single Tailwind hue), used sparingly for emphasis, links, primary CTAs, and one chart series. Status colors (success/warning/error) only for status.

### Dark mode

Default to dark for dashboards, light for prose/reports. Always provide both via DaisyUI themes — switching is just a `data-theme` change.

```html
<html lang="en" data-theme="dark">
```

DaisyUI themes worth defaulting to: `light`, `dark`, `business`, `corporate`, `night`. Pick **one** — don't mix. With the `@plugin` config above, DaisyUI auto-applies `light`/`dark` based on `prefers-color-scheme` when you omit `data-theme`.

### Typography

Modern dashboards use a geometric sans for UI and tabular numerals for data.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root { font-family: 'Inter', ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif; }
  /* Tabular numerals for stat cards, tables, deltas */
  .num, td.num, .stat-value { font-variant-numeric: tabular-nums; }
</style>
```

- Body 14–16px, line-height 1.5–1.6.
- Headings tight (`tracking-tight`, `font-semibold`, not `font-bold`).
- Numbers in stat cards and tables: **always tabular** (`font-variant-numeric: tabular-nums`).
- Labels for metrics: small, uppercase optional, muted (`text-xs text-slate-500 dark:text-slate-400`).

### Layout patterns

- **Page shell**: `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8` with `space-y-8` between sections.
- **Stat row**: 2 cols mobile → 4 cols desktop, `grid grid-cols-2 lg:grid-cols-4 gap-4`. Each card: label (xs muted), value (3xl semibold tabular), delta (xs success/error).
- **Bento grid** for mixed content: `grid grid-cols-12 gap-4` with cards spanning `col-span-12 md:col-span-6 lg:col-span-4` (or 8/4 splits for chart + side panel).
- **Hierarchy**: stat row → primary chart (full or 2/3 width) → secondary charts → tables/lists. One H1 per page; sections use H2.
- **Tables**: zebra off by default; rely on row borders. Sticky header on long tables. Right-align numeric columns.

### Chart polish (defaults look dated — override them)

Whatever the library, apply these:

- **Inherit the page palette.** One accent series; secondary series in muted neutrals. Never use the library's default rainbow.
- **Drop chartjunk.** Remove vertical gridlines on bar/line charts; keep horizontal at low opacity. Hide the legend if there's only one series. Hide axis lines, keep tick labels.
- **Soften axes.** Tick labels in `text-slate-500`-equivalent, no axis title unless ambiguous.
- **Tooltips on hover only**, no permanent data labels unless the chart is small.
- **Honor dark mode.** Read CSS variables / theme at init, don't hardcode `#fff` or `#000`.

Chart.js example (reads DaisyUI's base content color so it follows the theme):

```js
const css = getComputedStyle(document.documentElement);
const muted = css.getPropertyValue('--color-base-content').trim() || '#64748b';
Chart.defaults.font.family = "'Inter', system-ui, sans-serif";
Chart.defaults.color = muted;
Chart.defaults.borderColor = 'rgba(148,163,184,0.15)';
Chart.defaults.plugins.legend.display = false;
```

### Density tokens (use consistently)

| Token | Value |
|---|---|
| Card padding | `p-5` (compact) / `p-6` (default) |
| Grid gap | `gap-4` (dense) / `gap-6` (roomy) |
| Section spacing | `space-y-6` / `space-y-8` |
| Border radius | `rounded-xl` elements / `rounded-2xl` surfaces |
| Border color | `border-slate-200` / `border-white/5` |
| Muted text | `text-slate-500` / `text-slate-400` |

## Layout & color baseline

Always true, regardless of the visual style chosen above:

- **Responsive only.** CSS Grid, Flexbox, or Tailwind responsive utilities (`sm:`/`md:`/`lg:`). No fixed-pixel layouts.
- **Centered container** `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`. Reports may use `max-w-6xl` for narrower line length.
- **Mobile-first**: single-column on small viewports, multi-column when there's room. Cards/tables/charts reflow or scroll — never overflow the viewport.
- **Body line length** 60–80ch for prose; dashboards can go wider for tables.
- **Palette discipline**: one neutral scale + one accent + status colors (success/warning/error). No rainbows.
- **WCAG AA contrast** (4.5:1 body text, 3:1 large text and UI elements). Verify accent-on-surface combinations.

## Scrollbars — must match the layout

Every scrollable surface (page, card, table, code block, modal, sidebar, Tabulator, Mermaid overflow container) **must** use a scrollbar styled to the active theme. Default OS scrollbars break the design instantly — especially in dark mode where they appear as bright grey bars.

- Style WebKit/Blink (`::-webkit-scrollbar*`) **and** Firefox (`scrollbar-width`, `scrollbar-color`).
- Apply to `html` **and** `*` so nested scroll containers inherit consistently.
- Track is transparent or matches the surface; thumb is a muted neutral derived from the page's palette, slightly stronger on hover.
- Slim but visible: 8–12px on desktop. Don't `display: none` — invisible scrollbars are a usability bug.
- Theme-aware: read CSS variables / `prefers-color-scheme` so the bar adapts when the page does.
- Apply to **every** scrollable element you create — not just the page. Common misses:
  - `overflow-x-auto` table wrappers
  - `overflow-auto` code blocks (`<pre>`)
  - Tabulator's internal scroll area (`.tabulator-tableholder`)
  - Mermaid containers wrapped in `overflow-x-auto`
  - Sticky sidebars and modal bodies

```css
:root {
  --gp-scroll-thumb: rgb(148 163 184 / 0.5);   /* slate-400/50 */
  --gp-scroll-thumb-hover: rgb(100 116 139 / 0.8); /* slate-500/80 */
}
@media (prefers-color-scheme: dark) {
  :root {
    --gp-scroll-thumb: rgb(255 255 255 / 0.12);
    --gp-scroll-thumb-hover: rgb(255 255 255 / 0.22);
  }
}

html, * { scrollbar-width: thin; scrollbar-color: var(--gp-scroll-thumb) transparent; }
*::-webkit-scrollbar { width: 10px; height: 10px; }
*::-webkit-scrollbar-track { background: transparent; }
*::-webkit-scrollbar-thumb { background: var(--gp-scroll-thumb); border-radius: 9999px; border: 2px solid transparent; background-clip: padding-box; }
*::-webkit-scrollbar-thumb:hover { background: var(--gp-scroll-thumb-hover); background-clip: padding-box; }
*::-webkit-scrollbar-corner { background: transparent; }
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
