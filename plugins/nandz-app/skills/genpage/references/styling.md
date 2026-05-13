# Styling reference

A Space is a small React app delivered as one or more `.tsx` files. The host owns bundling, theming, fonts, and the iframe shell — your job is the component tree.

## The one and only import

Every `.tsx` file imports from exactly two packages:

```tsx
import * as React from 'react';
// Any shadcn component, the shadcn chart wrappers, the Recharts chart parts
// you compose inside them, and the `cn` helper — all from one package.
import { Card, Tabs, /* …whatever you need */ cn } from '@nandz/ui';
// Icons — straight from lucide-react.
import { ArrowRight, Check /* …whatever you need */ } from 'lucide-react';
```

`@nandz/ui` re-exports the **entire shadcn/ui catalog** plus the shadcn chart family, the Recharts chart parts you compose inside `ChartContainer`, and the `cn` helper. Use whichever shadcn components you need.

No other imports — no `clsx`, `tailwind-merge`, `class-variance-authority`, no `@radix-ui/*`, no CDNs. If a need can't be met with shadcn, redesign the section.

## Theming — pick a name, write it to the manifest

Pick one of shadcn's twelve built-in themes by name and put it in `manifest.json` as `theme`:

`zinc` (default) · `slate` · `stone` · `gray` · `neutral` · `red` · `rose` · `orange` · `green` · `blue` · `yellow` · `violet`

Pick the one whose mood fits the domain. Default to `zinc` when no clear signal. The host's `ThemeProvider` applies it; your `.tsx` files use the shadcn semantic tokens (`bg-background`, `text-foreground`, `bg-card`, `border-border`, `text-muted-foreground`, `bg-primary`, `text-primary-foreground`, `bg-destructive`, …) and the right colors fall through automatically.

Never hand-pick hex/HSL/Tailwind palette colors (`bg-blue-500`, `text-red-600`). Always go through the semantic tokens. If you need a second neutral or accent, use `secondary`/`accent`/`muted` — that's what they're there for.

The host also owns light/dark mode. Don't toggle it from inside a Space, don't read or write a `dark` class on `<html>`, don't ship a theme switcher.

## Responsive

A Space is a full webapp — it must feel native on phones, tablets, and desktops. Design responsively: progressively enhance from a phone-friendly base up to wider viewports, neither desktop-first nor mobile-only. Use Tailwind's `sm:` / `md:` / `lg:` / `xl:` breakpoints the way you'd expect.

Keep in mind that on phones, a Space first appears as a feed card before opening full-screen — so the top of the layout should communicate what the Space is at a glance (title, one-line summary, the most important element).

## Visual style

Aim for the contemporary product-UI feel (Linear, Vercel, Stripe, Resend, shadcn). The defaults are: **calm, dense, neutral, hairline structure, soft depth.**

- Surfaces: `bg-background` root, `Card` for grouped content (already styled).
- Borders define structure; shadows don't. Default `shadow-sm`. No glow, no neon.
- One accent (`primary`), used sparingly. Status colors (`destructive`, plus a `success`/`warning` if you map them) only for status.
- Numbers in stats and tables: always `tabular-nums`.
- Headings tight (`tracking-tight font-semibold`); labels small + muted (`text-xs text-muted-foreground`).

## Charts

Use `ChartContainer` to wrap the chart — it auto-picks palette tokens from the active theme, drops default chartjunk, and styles tooltips with shadcn tokens. Compose the Recharts primitives (`BarChart`, `Bar`, …) inside it; they're re-exported from `@nandz/ui` for you.

```tsx
<ChartContainer config={chartConfig} className="aspect-[16/9] sm:aspect-[2/1]">
  <BarChart data={data}>
    <Bar dataKey="value" />
    <ChartTooltip content={<ChartTooltipContent />} />
  </BarChart>
</ChartContainer>
```

- Always wrap in `ChartContainer`. Never set fixed pixel widths.
- Hide vertical grid lines (`vertical={false}`); show only horizontal at low opacity.
- One series → hide the legend.
- Soften axes (`axisLine={false}`, `tickLine={false}`).
- If a viz need is outside Recharts' chart catalogue (flowcharts, networks, maps, sankeys, gantts, geo), **redesign the section** as a styled list, table, stepper, or bento grid built from shadcn primitives.

## Component contracts

Short and universal, mostly to head off common LLM mistakes:

- **Cards**: the workhorse for grouped content. Compose `Card` + `CardHeader` + `CardTitle` + `CardDescription` + `CardContent` + optional `CardFooter`. Don't put `h-*` on a `Card` — content-sized.
- **Item**: use for compact list rows (one per entity, with optional media/title/description/actions). Prefer `Item` over a custom `Card` when rendering homogeneous lists — it's tighter and built for repetition.
- **Separator**: thin divider between sibling sections inside a `Card` or between rows. Don't sprinkle them everywhere — spacing first, separators only when grouping is otherwise ambiguous.
- **Badges**: content-sized via padding; never `w-*`, never `truncate`. `variant="secondary"` by default; `variant="default"` (primary) for at most one emphasised item per group; `variant="destructive"` only for errors.
- **Buttons**: `default` only for the primary CTA; `outline`/`secondary` for everything else; `ghost` for inline actions; `link` for in-prose links.
- **Tables**: right-align numeric columns with `text-right tabular-nums`. Render a stacked `Item` list instead when the viewport is narrow or the table has too many columns to fit comfortably.
- **Tabs**: only for genuinely parallel content the user switches between (views, time ranges, categories). Not for forcing sequential reading.
- **Carousel**: only when content is genuinely horizontal-browse-able (image gallery, set of related cards). Never for paginating tables or long-form content.
- **Toggle / ToggleGroup**: for switching view modes (chart vs. table, day/week/month, etc.). Pair every toggle with an icon or short label — never icon-only without an `aria-label`.
- **Typography**: use the `Typography` helpers for headings and prose instead of styling raw `<h1>`/`<p>` tags. Headings tight (`tracking-tight font-semibold`); labels small + muted (`text-xs text-muted-foreground`).
- **Tags / chips / breadcrumbs**: `flex flex-wrap gap-2` of `Badge` (or use the `Breadcrumb` component). Never `overflow-x-auto` with hidden scrollbars.
- **Categorical encoding**: differentiate by text/icon/position first. Reach for color only when there are several distinct categories AND color is the primary affordance AND a legend exists.
- **Diagrams / flowcharts / networks / maps / sankeys / gantts**: not in the stack. Redesign as a numbered list, vertical timeline (stacked `Item`s with `Separator`), indented hierarchical list, or a `Table` with relationship columns.

## Motion

A Space is a focused experience, not a landing page.

- Allowed: subtle hover transitions (≤200ms), Radix's default fade/slide on open, Recharts' default entry animation.
- Avoid: animated backgrounds, marquee, auto-carousels, particle effects, scroll-jacking, anything looping indefinitely.
- The host honors `prefers-reduced-motion` globally — don't fight it.
