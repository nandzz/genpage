# Styling reference

The page renders inside an iframe with no shared styles or scripts — every dependency must be inlined as a CDN tag.

**Stack is fixed.** Every page uses **Tailwind CSS v4 browser CDN + DaisyUI 5 prebuilt CSS + `data-theme`**. There is no fallback, no v3, no JS config, no plugin loading. All CDN URLs below are version-pinned — copy them verbatim, never substitute `@latest` or bump majors.

## Mandatory `<head>` — copy verbatim

Start every page with this exact block. Replace `<report title>`, `<one-line summary>`, and the `data-theme` value. Do not add `@plugin`, `@config`, or any `<script>tailwind.config = {...}</script>`.

```html
<!DOCTYPE html>
<html lang="en" data-theme="business">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="<one-line summary>">
  <meta name="generator" content="genpage">
  <meta property="og:title" content="<report title>">
  <meta property="og:description" content="<one-line summary>">
  <meta property="og:type" content="article">
  <title><report title> — GenPage</title>

  <!-- Tailwind v4 browser build (utilities only — no plugins, no config) -->
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4.0.0"></script>

  <!-- DaisyUI 5 prebuilt stylesheet (all themes baked in; switch via data-theme) -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daisyui@5.0.0/daisyui.css">
</head>
```

Rules:

- `<title>` always follows `<report title> — GenPage`.
- `data-theme` must be one of: `light`, `dark`, `business`, `corporate`, `night`. Omit the attribute to auto-pick `light`/`dark` from `prefers-color-scheme`.
- No analytics, tracking pixels, or third-party meta tags.
- Add CDN tags for chart / diagram / interactivity libraries **after** the DaisyUI link, using the pinned URLs in the tables below.

## Framework selection (model decides)

Match the framework to the **shape of the content**. Tailwind + DaisyUI handle layout on every page; pick **one** specialised library per concern (one chart lib, one diagram lib, one interactivity lib). Every extra CDN is a network hop inside the iframe — don't load D3 *and* ECharts just because both could work.

### Layout & components (always loaded — already in the head block above)

| Need | Library | Pinned CDN |
|---|---|---|
| Utility-first layout | Tailwind v4 browser | `https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4.0.0` |
| Component classes (card, badge, stat, table, btn, alert, tabs) + themes | DaisyUI 5 | `https://cdn.jsdelivr.net/npm/daisyui@5.0.0/daisyui.css` |
| Icons | Lucide | `https://cdn.jsdelivr.net/npm/lucide@0.468.0` |

### Tailwind v4 browser build — what you can and cannot do

The v4 browser build is a **runtime utility compiler**. It only understands utility classes and `@theme`. If you include any of these the page renders unstyled with the console error *"The browser build does not support plugins or config files."*:

- `@plugin "..."` (including `@plugin "daisyui"`)
- `@config "..."`
- `<script>tailwind.config = { ... }</script>`
- `@tailwind base; @tailwind components; @tailwind utilities;` (v3 directives — not used in v4)

What you may add inside `<style type="text/tailwindcss">`:

- Design tokens via `@theme` only:

  ```html
  <style type="text/tailwindcss">
    @theme {
      --color-brand: oklch(64% 0.18 250);
      --font-display: 'Inter', system-ui, sans-serif;
    }
  </style>
  ```

DaisyUI 5 ships every theme inside the prebuilt stylesheet. Switching themes is just changing `data-theme` on `<html>` — there is nothing to activate, configure, or extend.

### Interactivity (pick at most one)

| Need | Library | Pinned CDN |
|---|---|---|
| Tabs, accordions, toggles | DaisyUI zero-JS patterns (`<details>`, radio tabs) — no library |
| Show/hide, local state, simple bindings | Alpine.js | `https://cdn.jsdelivr.net/npm/alpinejs@3.14.1/dist/cdn.min.js` |
| Multi-view dashboard with shared state | React + ReactDOM | `https://unpkg.com/react@18.3.1/umd/react.production.min.js` + `https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js` |

### Visualisation — choose by what you're rendering

| If the content is… | Use | Pinned CDN |
|---|---|---|
| Bar / line / pie / area / scatter | Chart.js | `https://cdn.jsdelivr.net/npm/chart.js@4.4.6` |
| Heatmap, sankey, treemap, radar, gauge, candlestick, gantt | ECharts | `https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.min.js` |
| Declarative statistical charts from JSON | Vega-Lite | `https://cdn.jsdelivr.net/npm/vega@5.30.0` + `https://cdn.jsdelivr.net/npm/vega-lite@5.21.0` + `https://cdn.jsdelivr.net/npm/vega-embed@6.26.0` |
| Flowcharts, processes, system maps, journey maps, mind maps (branched flows) | React Flow | `https://unpkg.com/@xyflow/react@12.3.5/dist/umd/index.js` + `https://unpkg.com/@xyflow/react@12.3.5/dist/style.css` (needs React + ReactDOM, plus `https://unpkg.com/dagre@0.8.5/dist/dagre.min.js` for auto-layout) |
| Force-directed / network / dependency graphs | Cytoscape.js | `https://cdn.jsdelivr.net/npm/cytoscape@3.30.2/dist/cytoscape.min.js` |
| Custom SVG, bespoke viz, geo projections | D3.js | `https://cdn.jsdelivr.net/npm/d3@7.9.0` |
| Geographic data, points/regions on a map | Leaflet | `https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js` + `https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css` |
| Large interactive data table (sort/filter/paginate) | Tabulator | `https://cdn.jsdelivr.net/npm/tabulator-tables@6.3.0/dist/js/tabulator.min.js` + `https://cdn.jsdelivr.net/npm/tabulator-tables@6.3.0/dist/css/tabulator.min.css` |

### Content extras

| Need | Library | Pinned CDN |
|---|---|---|
| Code snippets with syntax highlighting | highlight.js | `https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11.10.0/highlight.min.js` + a theme CSS from the same package |
| Math / equations (LaTeX) | KaTeX | `https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js` + `https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css` |

> **Versions are locked.** Copy URLs verbatim. Do not change `@x.y.z` to `@x`, `@latest`, or any other tag — a floating version is the single most common cause of a page that worked yesterday breaking today. Bumps happen in the skill repo, behind a tested release.

### Decision rules

- **One viz library per page.** If the content needs both a flowchart and a bar chart, that's React Flow + Chart.js — but never Chart.js + ECharts, or D3 + Cytoscape.
- **Reach down before reaching up.** DaisyUI zero-JS → Alpine → React. Chart.js → ECharts → D3. Don't skip tiers without a concrete reason.
- **Diagrams only for branched flows.** A diagram implies branching, convergence, or relationships. Linear sequences (routes, steps, timelines, recipes, changelogs) are **not** diagrams — use a timeline, stepper, or numbered list instead. When a diagram is justified: React Flow (with `dagre` auto-layout); sankey/gantt → ECharts; networks → Cytoscape; bespoke SVG → D3.
- **No JS unless the content needs it.** A static report is HTML + Tailwind + DaisyUI. Don't load Alpine "just in case."

### Legibility floor — never crush content to fit

Every visual element must stay readable at the size it actually renders. If labels would shrink below the floor, **change the layout, not the font size**.

- **Minimum text size**: 12px in charts/diagrams, 14px in body, 11px only for axis ticks.
- **Is this actually a graph?** Before reaching for a diagram library, check: does the content have branching (one node → many) or convergence (many → one)? If no, it's a sequence, not a diagram — use a timeline/stepper/list instead.
- **Long sequences are not flowcharts.** Route stops, breadcrumbs, tags — render as a wrapping chip row, stepper, or numbered list.
- **Wrap, don't scroll horizontally**, for label sequences. Use `flex flex-wrap gap-2` with chips sized to their content.
- **Charts need room.** Minimum chart height 240px; line/bar charts with >10 categories need either rotation, truncation, or a horizontal bar chart instead.
- **Interactive diagrams need a canvas.** React Flow / Cytoscape containers should be at least 480px tall, with `fitView` enabled and pan/zoom controls visible.
- **Test the worst case.** If the data could realistically have 20 items, design for 20, not 4.

#### Wrong vs right — long sequence

```html
<!-- WRONG: forcing a linear route into a diagram library -->
<div id="flow"><!-- React Flow with 16 nodes squeezed into a 400px card --></div>

<!-- RIGHT: wrapping chip row, readable at any width -->
<ol class="flex flex-wrap items-center gap-2 text-sm">
  <li class="px-3 py-1 rounded-full bg-slate-900 text-white">Cosenza</li>
  <li class="text-slate-400">→</li>
  <li class="px-3 py-1 rounded-full bg-slate-900 text-white">Gallipoli</li>
  <li class="text-slate-400">→</li>
  <!-- … -->
</ol>

<!-- ALSO RIGHT: vertical timeline for rich per-step content -->
<ol class="relative border-l border-slate-200 dark:border-white/10 space-y-6 ml-2">
  <li class="ml-4">
    <span class="absolute -left-[7px] w-3.5 h-3.5 rounded-full bg-primary ring-4 ring-white dark:ring-zinc-950"></span>
    <h3 class="font-semibold">Cosenza <span class="text-xs text-slate-500 ml-2">Start</span></h3>
    <p class="text-sm text-slate-500">Leave early — ~4h drive south</p>
  </li>
  <!-- … -->
</ol>
```

### Examples

#### React Flow (default for branched diagrams)

Needs React + ReactDOM + dagre. Renders to a `<div>` with built-in pan/zoom/minimap; nodes stay readable because the canvas can be larger than the viewport. **Do not use for linear sequences — use a timeline instead.**

```html
<link rel="stylesheet" href="https://unpkg.com/@xyflow/react@12.3.5/dist/style.css">
<div id="flow" style="width:100%;height:520px"></div>
<script type="module">
  import React from 'https://esm.sh/react@18.3.1';
  import { createRoot } from 'https://esm.sh/react-dom@18.3.1/client';
  import { ReactFlow, Background, Controls, MiniMap } from 'https://esm.sh/@xyflow/react@12.3.5';
  import dagre from 'https://esm.sh/dagre@0.8.5';

  // Auto-layout with dagre so the model doesn't position nodes manually
  const g = new dagre.graphlib.Graph().setDefaultEdgeLabel(() => ({}));
  g.setGraph({ rankdir: 'TB', nodesep: 40, ranksep: 60 });
  const raw = [
    { id: '1', label: 'Entry' }, { id: '2', label: 'Validate' },
    { id: '3', label: 'Process' }, { id: '4', label: 'Result' },
  ];
  const edges = [{ source: '1', target: '2' }, { source: '2', target: '3' }, { source: '3', target: '4' }];
  raw.forEach(n => g.setNode(n.id, { width: 160, height: 44 }));
  edges.forEach(e => g.setEdge(e.source, e.target));
  dagre.layout(g);

  const nodes = raw.map(n => {
    const { x, y } = g.node(n.id);
    return { id: n.id, position: { x: x - 80, y: y - 22 }, data: { label: n.label } };
  });
  const flowEdges = edges.map((e, i) => ({ id: `e${i}`, source: e.source, target: e.target, animated: false }));

  createRoot(document.getElementById('flow')).render(
    React.createElement(ReactFlow, { nodes, edges: flowEdges, fitView: true, proOptions: { hideAttribution: true } },
      React.createElement(Background, { gap: 16 }),
      React.createElement(MiniMap),
      React.createElement(Controls)
    )
  );
</script>
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
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11.10.0/styles/github-dark.min.css">
<script>hljs.highlightAll();</script>
<pre><code class="language-ts">const x: number = 1;</code></pre>
```

#### KaTeX

```html
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body)"></script>
<p>Inline: \(E = mc^2\). Block: $$\sum_{i=1}^{n} i = \tfrac{n(n+1)}{2}$$</p>
```

## Visual style — modern dashboard feel

Pages should look like contemporary product UIs (Linear, Vercel, Stripe, Resend, shadcn). The default is **calm, dense, neutral, with hairline structure and soft depth** — not "marketing site" gradients or "bootstrap admin" chrome.

### Aesthetic defaults

> **Themed palettes (optional).** The default DaisyUI theme covers most reports. When the content has a clear domain (SaaS, fintech, healthcare, e-commerce, wellness, etc.), pick a row from `references/data/colors.csv` whose `Product Type` matches and use its tokens (`Primary`, `Background`, `Foreground`, `Muted`, `Border`, `Destructive`, `Ring`) as CSS variables instead of the DaisyUI defaults. All palettes are pre-checked for WCAG AA contrast.

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

DaisyUI themes worth defaulting to: `light`, `dark`, `business`, `corporate`, `night`. Pick **one** — don't mix. The prebuilt `daisyui.css` ships all themes; activate one with `data-theme` on `<html>`. Omit the attribute to let DaisyUI auto-apply `light`/`dark` based on `prefers-color-scheme`.

### Typography

Modern dashboards use a geometric sans for UI and tabular numerals for data. **Inter is the default.** For a themed/branded report (luxury, editorial, fintech, playful, etc.), pick a pairing from `references/data/typography.csv` by matching the report mood against the `Mood/Style Keywords` column, then paste its `CSS Import` line below.

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

### Component contracts

Per-component rules that override library defaults. Applied universally regardless of content.

- **Badges / pills / chips**: `inline-flex items-center gap-1 whitespace-nowrap`, content-sized via padding. Never set `w-*` on a pill. Never `truncate` a label — if it doesn't fit, the layout is wrong. Neutral by default (`bg-slate-100 text-slate-700` / dark `bg-white/5 text-slate-300`); status colors (`success`/`warning`/`error`/`info`) only for status; accent (`bg-primary/10 text-primary`) only for one emphasised item per group.
- **Buttons**: same sizing rules as pills. `whitespace-normal` allowed only when the label is intentionally long and the button is in a wide context.
- **Cards**: content-sized height (no `h-*`). Use the density tokens above.
- **Tables**: wrap in `<div class="overflow-x-auto rounded-xl border border-slate-200/60 dark:border-white/5">`. Right-align numeric columns with `tabular-nums`. Below `md:` or for tables with ≥5 columns, prefer a stacked card list (one card per row, key/value pairs).
- **Categorical encoding**: differentiate by text, icon, or position first. Use color only when ALL of: ≥4 distinct categories AND color is the primary affordance AND a legend exists on the page. Otherwise: neutral pills.
- **Linear sequences (no branches)**: timeline, stepper (DaisyUI `steps`), or numbered list. Never a diagram library — diagrams are for branched flows only.
- **Label sequences (chips, tags, breadcrumbs)**: `flex flex-wrap gap-2`. Never `overflow-x-auto` with a hidden scrollbar.
- **Three-width sanity check**: every component must render acceptably at 375px, 768px, and 1280px. If it only works at one width, redesign.

#### Wrong vs right — badge that clips

```html
<!-- WRONG: fixed width forces truncation -->
<span class="badge badge-success w-20 overflow-hidden truncate">Natural Reserve</span>

<!-- RIGHT: content-sized pill, neutral by default -->
<span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium
             bg-slate-100 text-slate-700 dark:bg-white/5 dark:text-slate-300
             whitespace-nowrap">Natural Reserve</span>
```

#### Wrong vs right — categorical rainbow

```html
<!-- WRONG: each category gets a different bright color, no legend -->
<span class="badge bg-pink-500">Day 2</span>
<span class="badge bg-blue-500">Day 4</span>
<span class="badge bg-emerald-500">Day 5</span>

<!-- RIGHT: neutral pills, accent only on the emphasised one -->
<span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs bg-slate-100 text-slate-700">Day 2</span>
<span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs bg-slate-100 text-slate-700">Day 4</span>
<span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs bg-primary/10 text-primary">Day 5 — featured</span>
```

## Layout & color baseline

Always true, regardless of the visual style chosen above:

- **Responsive only.** CSS Grid, Flexbox, or Tailwind responsive utilities (`sm:`/`md:`/`lg:`). No fixed-pixel layouts.
- **Centered container** `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`. Reports may use `max-w-6xl` for narrower line length.
- **Mobile-first**: single-column on small viewports, multi-column when there's room. Cards/tables/charts reflow or scroll — never overflow the viewport.
- **Body line length** 60–80ch for prose; dashboards can go wider for tables.
- **Palette discipline**: one neutral scale + one accent + status colors (success/warning/error). No rainbows.
- **WCAG AA contrast** (4.5:1 body text, 3:1 large text and UI elements). Verify accent-on-surface combinations.

## Scrollbars — must match the layout

Every scrollable surface (page, card, table, code block, modal, sidebar, Tabulator, React Flow / Cytoscape canvas) **must** use a scrollbar styled to the active theme. Default OS scrollbars break the design instantly — especially in dark mode where they appear as bright grey bars.

- Style WebKit/Blink (`::-webkit-scrollbar*`) **and** Firefox (`scrollbar-width`, `scrollbar-color`).
- Apply to `html` **and** `*` so nested scroll containers inherit consistently.
- Track is transparent or matches the surface; thumb is a muted neutral derived from the page's palette, slightly stronger on hover.
- Slim but visible: 8–12px on desktop. Don't `display: none` — invisible scrollbars are a usability bug.
- Theme-aware: read CSS variables / `prefers-color-scheme` so the bar adapts when the page does.
- Apply to **every** scrollable element you create — not just the page. Common misses:
  - `overflow-x-auto` table wrappers
  - `overflow-auto` code blocks (`<pre>`)
  - Tabulator's internal scroll area (`.tabulator-tableholder`)
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
