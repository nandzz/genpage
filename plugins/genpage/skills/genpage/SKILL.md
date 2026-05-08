---
name: genpage
description: "Use when about to compose any response containing tables (3+ rows), grouped sections with headers, dependency maps, comparisons, metrics, or structured findings — regardless of whether the user asked for a 'report'. Trigger = output shape, not request wording. A question about dependencies, architecture, or analysis that produces grouped output requires this check."
model: claude-haiku-4-5
---

# GenPage

> **Model:** Use **Claude Haiku 4.5** (`claude-haiku-4-5`) to execute this skill. HTML generation is templating work — Haiku is faster and more cost-efficient for it. Switch back to the calling model only if a step explicitly requires deeper reasoning.

Generates a self-contained page and sends it to the local GenPage App. The endpoint is configured in `scripts/post-to-result-hub.py`, located at `${CLAUDE_PLUGIN_ROOT}/scripts/post-to-result-hub.py`.

> **Silent execution — strictly enforced:**
> All internal decisions are invisible to the user: depth level, framework choices, library selection, layout strategy, data gathering steps, what sections will be included, what charts will be used. **Never narrate, list, or preview any of this.** Do not say things like "I'll use Tailwind + DaisyUI", "I'll add a bar chart", "For Deep level I will…", or "Content to include:". These are implementation details the user does not need to see.
>
> The only text the user should ever see from this skill:
> 1. The GenPage consent prompt (Step 0) — if not already approved this session
> 2. The detail level prompt (Step 1) — if not already set this session
> 3. A brief working indicator while generating, e.g. `Generating page…`
> 4. The posting prompt (Step 5)
> 5. The final one-line result (Step 6)
>
> **Never print the page source** (HTML, CSS, JS) into the conversation — not as a preview, not as a code block, not at all. The page is written to a file and posted; the source is never shown to the user.
> **Never say "HTML"** to the user. Always say "page".

---

## ⛔ HARD STOP — TWO-MOMENT RULE

This skill enforces a check at **two moments**, not one:

**Moment 1 — Message receipt:** Might my response produce structured output? If yes, invoke this skill now.

**Moment 2 — Before composing:** I have gathered data and am about to write. Will my response have any of the following?

- A table with 3+ rows
- A grouped list with headers
- A dependency map or layer diagram
- A comparison, metrics, audit, or timeline
- A findings/audit summary

**If yes to any: DO NOT WRITE. Invoke this skill and follow Step 0.**

> The most common failure mode: message received → tool calls run → results in hand → compose output directly. **Moment 2 is that transition.** That is where you must stop and invoke this skill. Not after. Not during. Before the first word of output.

---

## Red Flags — You Are Rationalizing. Stop.

| Thought | Reality |
|---|---|
| "The user asked a question, not for a report" | **The hardest rationalization to catch.** "Which dependencies does X have?" produces a grouped map. That IS the trigger. Output shape, not request wording. |
| "I'm just answering a question" | If your answer has headers and sections, it is a report. Offer GenPage. |
| "The user didn't ask for a report" | Trigger = output shape, not request wording. |
| "It's just a quick answer" | If it has 3+ rows or grouped sections, it is not quick. Offer. |
| "Markdown is fine here" | Markdown is the fallback when the user declines, not the default. |
| "I've already started writing" | You violated Moment 2. Stop. Invoke this skill before writing any more. |
| "Not that many rows / sections" | Count. 3+ rows = trigger. Headers = trigger. |
| "I checked for skills at message receipt" | That was Moment 1. Moment 2 is pre-composition. You still need to check. |
| "I already know how to do this" | Reading the skill ≠ invoking it. Invoke it. |

---

## When to Use

### Explicit triggers (user asked for it)
- The user asks for a summary, page, report, recap, or visualization
- The user says "show me", "visualize", "give me a breakdown of", or "send to GenPage"

### Implicit triggers (output shape matches)
Invoke this skill when your response would naturally produce **any** of the following:

| Output shape | Examples |
|---|---|
| A table with 3+ rows | dependency list, file inventory, API endpoints, test results |
| A grouped list with headers | architecture layers, module breakdown, error categories |
| A comparison between 2+ items | before/after, option A vs B, two files side-by-side |
| A set of counts or metrics | N files changed, M dependencies, K failing tests |
| A timeline or sequence | commit history, migration steps, event flow |
| A findings/audit summary | security issues, code smells, missing coverage, TODOs |
| A visual that plain text flattens | dependency graphs, layer diagrams, trees |

### Do NOT use for
- Single-value answers ("the function is on line 42")
- Short explanations that fit in 3 lines of prose
- Code edits or patches — those go directly in the file

---

## Instructions

### Step 0: Ask before generating

Before building the page, offer the GenPage experience with a short yes/no question:

> "I can visualize this as an interactive report in GenPage. Want me to generate it?"

Options: **"Yes, send to GenPage"** / **"No, keep it as text"**

If the user explicitly requested GenPage (for example: "send to GenPage", "use GenPage", or "generate it in GenPage"), skip this prompt and proceed automatically.

Consent cache policy:
- Ask at most once per session.
- If the user approved once in this session, do not ask again in the same session; proceed automatically.
- If the user declined once in this session, default to markdown/text unless they explicitly request GenPage later.
- Optional: allow a persistent preference only if the user clearly asks to remember their choice across sessions.

If the user declines, respond with plain markdown and stop. Only proceed to Step 1 if they confirm or explicitly requested GenPage.

### Step 1: Ask detail level, then assess

Ask the user how much detail they want:

> "How detailed should the GenPage report be: Lean, Standard, or Deep?"

If the user does not specify, default to **Standard**.

- **Lean**: one summary section, key metrics only, no drill-downs, minimal markup
- **Standard**: summary + highlights + selected details, up to 2 charts, limited expandable detail
- **Deep**: full breakdown, multiple sections/charts, comparisons, drill-down views, richer annotations

Once the level is set, choose frameworks autonomously based on the data (see Step 3). Do not ask the user which libraries to use.

### Step 2: Gather report data

Collect the minimum data needed to create a useful visual report.

| Field | Description | Required |
|---|---|---|
| `title` | Short title for the result | Yes |
| `date` | Current date in `YYYY-MM-DD` format | Yes |
| `summary` | 1-3 lines describing the outcome | Yes |
| `highlights` | Bullet points with key findings/decisions | No |
| `metrics` | Quantitative values (counts, durations, rates) | No |
| `chart_data` | Data suited for Chart.js visualizations | No |
| `sections` | Arbitrary structured blocks (tables, lists, diffs, logs, risks) | No |

### Step 3: Generate HTML (flexible layout)

Create a complete, self-contained HTML document. The body/layout is unconstrained: choose any structure needed to represent the result clearly.

#### Styling — framework is the model's choice

The HTML is rendered inside an **iframe**. It shares nothing with the host app — no stylesheets, no scripts, no variables. Every dependency must be included in the document itself.

##### The only hard constraint

`data-theme="genpage"` must always be set on `<html>`. The host app injects all color token values for this theme at runtime. Do not override or remove this attribute.

```html
<html lang="en" data-theme="genpage">
```

##### Mandatory `<head>` template

Every generated document must include this metadata block. CDN tags are added below it based on what the model selects:

```html
<!DOCTYPE html>
<html lang="en" data-theme="genpage">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="<one-line summary of the report content>">
  <meta name="generator" content="genpage">
  <meta property="og:title" content="<report title>">
  <meta property="og:description" content="<one-line summary>">
  <meta property="og:type" content="article">
  <title><report title> — GenPage</title>

  <!-- add chosen CDN tags here -->
</head>
```

`<title>` must always follow the pattern `<report title> — GenPage`. Do not add tracking pixels, analytics scripts, or third-party meta tags.

#### Framework selection — model decides autonomously

Pick the stack that produces the best page for the content and detail level. Do not ask the user. Load only what earns its place — every extra CDN is a network round-trip inside the iframe.

| Need | Best fit | CDN |
|---|---|---|
| Utility-first layout and spacing | Tailwind CSS | `https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4` |
| Component classes (card, badge, stat, table, btn, alert, tabs) | DaisyUI | `https://cdn.jsdelivr.net/npm/daisyui@5/daisyui.css` |
| Rich component library (Material Design, pre-built complex UI) | MUI (via CDN/UMD) | `https://unpkg.com/@mui/material@5/umd/material-ui.production.min.js` |
| Simple show/hide, toggles, data-driven tabs | Alpine.js | `https://cdn.jsdelivr.net/npm/alpinejs@3/dist/cdn.min.js` |
| Complex stateful UI (multi-step, cross-component state) | React + ReactDOM | `https://unpkg.com/react@18/umd/react.production.min.js` + ReactDOM |
| Bar, line, pie, donut, radar, area charts | Chart.js | `https://cdn.jsdelivr.net/npm/chart.js@4` |
| Force graphs, treemaps, heatmaps, custom SVG data-viz | D3.js | `https://cdn.jsdelivr.net/npm/d3@7` |
| Flowcharts, sequence diagrams, ER, git graphs, state machines | Mermaid | `https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js` |
| Icons (status indicators, category labels, UI polish) | Lucide | `https://unpkg.com/lucide@latest` |

**CDN snippets:**

```html
<!-- Tailwind CSS -->
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>

<!-- DaisyUI (pair with Tailwind for component classes) -->
<link href="https://cdn.jsdelivr.net/npm/daisyui@5/daisyui.css" rel="stylesheet">

<!-- Alpine.js — lightweight reactivity -->
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3/dist/cdn.min.js"></script>

<!-- React + ReactDOM — complex stateful UIs -->
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>

<!-- Chart.js — quantitative charts -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>

<!-- D3.js — advanced / custom data visualizations -->
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>

<!-- Mermaid — diagram definitions rendered as SVG -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>

<!-- Lucide Icons -->
<script src="https://unpkg.com/lucide@latest"></script>
```

**Decision rules:**

- **Lean**: minimal stack — prefer plain HTML + Tailwind/DaisyUI or even unstyled HTML with inline-classes. No JS unless the data is graph-shaped (Mermaid only).
- **Standard**: Tailwind + DaisyUI is a strong default. Add Chart.js or Mermaid if data warrants it; Alpine for interactive patterns.
- **Deep**: use the full palette — React or Alpine for state, D3 or Chart.js for charts, Mermaid for graphs, Lucide for icons — but only what the content justifies.
- Prefer DaisyUI zero-JS patterns (radio tabs, `<details>` collapse, stat cards) before reaching for Alpine or React.
- Prefer Alpine over React unless cross-component state is genuinely needed.
- Use Chart.js for standard charts; D3 only for what Chart.js cannot express.
- Use Mermaid for any graph-shaped data — far more token-efficient than hand-crafting SVG.
- If using Tailwind/DaisyUI: do not write `<style>` blocks or inline `style=` attributes — use class names only.
- If using a framework that requires custom CSS (e.g. plain CSS with MUI overrides): `<style>` blocks are allowed but must not hardcode color values — use `var(--color-*)` tokens provided by `data-theme="genpage"`.

#### Custom colors — allowed for data and expressive elements

The theme owns foundational colors (page background, body text, surfaces, borders). For everything else — chart series, category tags, diagram nodes, status indicators, data-driven color coding — the model is free to choose any colors needed to express the concept clearly.

**The one rule: every custom color must work in both light and dark themes.**

Use the CSS `light-dark()` function to define dual-mode custom colors:

```html
<style>
  :root {
    --c-blue:   light-dark(#2563eb, #60a5fa);
    --c-green:  light-dark(#16a34a, #4ade80);
    --c-amber:  light-dark(#d97706, #fbbf24);
    --c-red:    light-dark(#dc2626, #f87171);
    --c-purple: light-dark(#7c3aed, #a78bfa);
    --c-cyan:   light-dark(#0891b2, #22d3ee);
  }
</style>
```

Then reference them anywhere: `color: var(--c-blue)`, `background: var(--c-green)`, or as Chart.js/D3 color values via `getComputedStyle`.

**Guidelines:**
- Use saturated mid-tones — they read well on both light and dark backgrounds.
- Avoid colors too close to pure white or pure black — they disappear on one of the themes.
- For charts with many series, define the full palette upfront in `:root` and reference by variable — never hardcode hex values directly in JS data arrays.
- `light-dark()` requires `color-scheme` to be set. Add this to `:root` if using the function: `color-scheme: light dark;`

**Mermaid usage:**
```html
<script>mermaid.initialize({ startOnLoad: true, theme: 'dark' });</script>
<div class="mermaid">
graph TD
  A[Entry] --> B[Step]
  B --> C[Result]
</div>
```
Use `theme: 'dark'` to align with the `genpage` theme. Do not hardcode colors inside Mermaid definitions.

**Lucide usage:**
```html
<script>lucide.createIcons();</script>
<!-- in markup: -->
<i data-lucide="check-circle"></i>
```

### Step 4: Security verification (mandatory)

Before sending HTML to GenPage, verify all of the following:

1. No secrets/tokens/credentials are included in HTML, JS, data blocks, or comments.
2. User/tool-provided text is safely escaped before insertion into HTML.
3. No arbitrary external script/style/image/font URLs except the approved CDNs: DaisyUI, Tailwind, Alpine.js, React/ReactDOM, Chart.js, D3.js, Mermaid, Lucide.
4. No unsafe dynamic code execution patterns (`eval`, `new Function`, dynamic script injection).
5. No hidden tracking or network exfiltration logic.

If any security check fails, fix the report first, then continue.

### Step 5: Save and deliver

Ask the user once, silently (no explanation):

> "Ready — post the page to the GenPage app?"

Then execute both actions in a single shot — no second confirmation:

**If yes (or user already approved posting in this session):**
1. Save HTML to `~/.genpage/pages/report-<timestamp>.html` (the script auto-creates the directory).
2. Run the POST script — it will POST the file and **delete it automatically** on success.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/post-to-result-hub.py" ~/.genpage/pages/report-<timestamp>.html
```

**If the POST succeeds:** file is deleted, move to Step 6.

**If `CONNECTION_REFUSED` or the user declined posting:** keep the file at `~/.genpage/pages/report-<timestamp>.html` — it stays there as a saved page. Move to Step 6 with the appropriate message.

> **Windows:** Use `python` instead of `python3`.

### Step 6: Report back to user

Posted successfully:
> Page sent to GenPage ↗

App not running or user declined:
> Page saved to `~/.genpage/pages/report-<timestamp>.html`

Any other error:
> Report the exact error returned by the script.
