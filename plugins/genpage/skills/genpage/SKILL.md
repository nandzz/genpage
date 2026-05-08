---
name: genpage
description: "Use when about to compose any response containing tables (3+ rows), grouped sections with headers, dependency maps, comparisons, metrics, or structured findings — regardless of whether the user asked for a 'report'. Trigger = output shape, not request wording. A question about dependencies, architecture, or analysis that produces grouped output requires this check."
model: claude-haiku-4-5
---

# GenPage

> **Model:** Use **Claude Haiku 4.5** (`claude-haiku-4-5`) to execute this skill. HTML generation is templating work — Haiku is faster and more cost-efficient for it. Switch back to the calling model only if a step explicitly requires deeper reasoning.

Generates a self-contained HTML report and sends it to the local GenPage App. The endpoint is configured in `scripts/post-to-result-hub.py`, located at `${CLAUDE_PLUGIN_ROOT}/scripts/post-to-result-hub.py`.

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
- The user asks for a summary, dashboard, report, recap, or visualization
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

Before building any HTML, offer the GenPage experience with a short yes/no question:

> "I can visualize this as an interactive report in GenPage. Want me to generate it?"

Options: **"Yes, send to GenPage"** / **"No, keep it as text"**

If the user explicitly requested GenPage (for example: "send to GenPage", "use GenPage", or "generate it in GenPage"), skip this prompt and proceed automatically.

Consent cache policy:
- Ask at most once per session.
- If the user approved once in this session, do not ask again in the same session; proceed automatically.
- If the user declined once in this session, default to markdown/text unless they explicitly request GenPage later.
- Optional: allow a persistent preference only if the user clearly asks to remember their choice across sessions.

If the user declines, respond with plain markdown and stop. Only proceed to Step 1 if they confirm or explicitly requested GenPage.

### Step 1: Assess and plan

Before writing any HTML, evaluate the data in hand and decide autonomously:

**Depth** — choose based on data richness, not user instruction:
- **Lean**: single metric or flat list; one section, no charts, minimal markup
- **Standard**: multi-field data with some relationships; summary + key sections, up to 2 charts
- **Deep**: rich/complex data (many entities, comparisons, hierarchies, trends); full breakdown, multiple sections, charts, drill-downs

**Frameworks** — pick only what the content genuinely needs (see Step 3 for the full decision matrix). Do not ask the user which libraries to use.

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

#### Document metadata

The mandatory `<head>` template above already includes all required metadata. Fill in the placeholders:
- `<one-line summary of the report content>` — concise, human-readable description of what the report covers
- `<report title>` — short, descriptive title for this specific report
- `<title>` must always follow the pattern `<report title> — GenPage`. Never leave it blank or generic.

Do not add tracking pixels, analytics scripts, or third-party meta tags.

#### Styling — Tailwind CSS + DaisyUI (mandatory)

The HTML is rendered inside an **iframe**. It shares nothing with the host app — no stylesheets, no scripts, no variables. Every dependency must be included in the document itself.

**Do not write `<style>` blocks or inline `style=` attributes.** Use class names only.

##### Mandatory `<head>` template

Every generated document must open with exactly this `<head>` block. Do not omit or reorder these tags:

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

  <!-- Styling (always required) -->
  <link href="https://cdn.jsdelivr.net/npm/daisyui@5/daisyui.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
```

`data-theme="genpage"` is **always** set on `<html>`. The host app injects all CSS variable values for this theme at runtime — the model never knows or sets them. Do not override or replace this attribute.

Styling rules:
1. Use Tailwind utility classes for layout and spacing (`flex`, `gap-4`, `p-3`, `grid`, `w-full`, etc.).
2. Use DaisyUI component classes for UI patterns (`table table-zebra`, `badge badge-success`, `btn btn-primary`, `card`, `stat`, `alert`, etc.).
3. Do not write `<style>` blocks. Do not use inline `style=` attributes. Do not hardcode color values anywhere.
4. Do not introduce custom CSS tokens or variables — the App owns the theme.
5. Keep the document self-contained — no additional CSS files.

Semantic token assignment (how to pick the right class):
- **Primary** (`btn-primary`, `text-primary`, `bg-primary`) — main actions, key highlights, CTAs
- **Secondary** (`btn-secondary`, `text-secondary`) — supporting actions, secondary labels
- **Accent** (`text-accent`, `bg-accent`) — emphasis, callouts, decorative highlights
- **Base** (`bg-base-100/200/300`, `text-base-content`) — backgrounds, surfaces, body text
- **Success** (`badge-success`, `text-success`) — passing tests, healthy metrics, positive deltas
- **Warning** (`badge-warning`, `text-warning`) — degraded state, low coverage, slow durations
- **Error** (`badge-error`, `text-error`) — failures, missing items, critical issues
- **Info** (`badge-info`, `text-info`) — neutral metadata, counts, informational notes

Visibility rule: prefer these semantic classes over raw Tailwind color classes (`text-blue-500`, etc.) — the App theme controls the actual values, keeping reports consistent.

#### Framework selection — model decides autonomously

The model selects libraries based on what the content requires. Do not ask the user. Load only what earns its place — every extra CDN is a network round-trip inside the iframe.

**Always included** (already in the mandatory head template):
- **Tailwind CSS** — layout, spacing, typography
- **DaisyUI** — component classes (`card`, `badge`, `stat`, `table`, `btn`, `alert`, `collapse`, tabs via radio inputs)

**Load on demand — pick the right tool for the job:**

| Need | Best fit | CDN |
|---|---|---|
| Tabs, toggles, filters, show/hide — simple | DaisyUI radio/checkbox patterns (zero JS) | already loaded |
| Tabs, toggles, filters — dynamic or data-driven | Alpine.js | `https://cdn.jsdelivr.net/npm/alpinejs@3/dist/cdn.min.js` |
| Complex stateful UI (multi-step, cross-component state) | React + ReactDOM | see below |
| Bar, line, pie, donut, radar, area charts | Chart.js | `https://cdn.jsdelivr.net/npm/chart.js@4` |
| Force graphs, treemaps, heatmaps, custom SVG data-viz | D3.js | `https://cdn.jsdelivr.net/npm/d3@7` |
| Flowcharts, sequence diagrams, ER diagrams, git graphs, state machines | Mermaid | `https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js` |
| Icons (status indicators, labels, UI polish) | Lucide | `https://unpkg.com/lucide@latest` |

**CDN snippets:**

```html
<!-- Alpine.js — lightweight reactivity -->
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3/dist/cdn.min.js"></script>

<!-- React — only for complex stateful UIs -->
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

- Prefer DaisyUI's zero-JS patterns (radio tabs, `<details>` collapse, stat cards) before reaching for Alpine or React.
- Prefer Alpine.js over React when all that's needed is show/hide, x-data toggling, or simple loops.
- Use React only when the UI has cross-component state that Alpine can't cleanly express.
- Use Chart.js for standard quantitative charts. Use D3 only when Chart.js cannot express the visualization (force-directed graphs, treemaps, custom path shapes).
- Use Mermaid for any graph-shaped data — it's far more token-efficient than hand-crafting SVG or canvas.
- Load Lucide only when icons meaningfully aid scannability (status rows, category labels, navigation).
- **Lean depth**: Tailwind + DaisyUI only. No JS libraries unless the data is graph-shaped (Mermaid only).
- **Standard depth**: add Chart.js or Mermaid if the data warrants it; Alpine for any interactive pattern.
- **Deep depth**: use the full palette as needed — React, D3, Mermaid, Chart.js, Lucide — but only what the content justifies.

**Mermaid usage:**
```html
<script>mermaid.initialize({ startOnLoad: true, theme: 'dark' });</script>
<div class="mermaid">
graph TD
  A[Entry] --> B[Step]
  B --> C[Result]
</div>
```
Use `theme: 'dark'` to stay consistent with the `genpage` DaisyUI theme. Do not hardcode colors inside Mermaid definitions.

**Lucide usage:**
```html
<script>
  lucide.createIcons();
</script>
<!-- in markup: -->
<i data-lucide="check-circle" class="text-success"></i>
```

### Step 4: Security verification (mandatory)

Before sending HTML to GenPage, verify all of the following:

1. No secrets/tokens/credentials are included in HTML, JS, data blocks, or comments.
2. User/tool-provided text is safely escaped before insertion into HTML.
3. No arbitrary external script/style/image/font URLs except the approved CDNs: DaisyUI, Tailwind, Alpine.js, React/ReactDOM, Chart.js, D3.js, Mermaid, Lucide.
4. No unsafe dynamic code execution patterns (`eval`, `new Function`, dynamic script injection).
5. No hidden tracking or network exfiltration logic.

If any security check fails, fix the report first, then continue.

### Step 5: POST to GenPage

Do not inline full HTML inside a bash heredoc command. That causes unnecessary execution confirmations and noisy prompts.

Preferred flow:
1. Save the generated HTML to `~/.genpage/report-<timestamp>.html`. The script auto-creates `~/.genpage/` on first run.
2. Use file creation (not in-place overwrite) so no pre-read step is required.
3. Execute the script — it will POST, log the result to `~/.genpage/genpage.log`, and **delete the file automatically** after a successful POST.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/post-to-result-hub.py" ~/.genpage/report-<timestamp>.html
```

> **Windows:** Use `python` instead of `python3`. If Python is not installed, download it from [python.org](https://www.python.org/downloads/) or the Microsoft Store.

Fallback (only when file write tools are unavailable):

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/post-to-result-hub.py" << 'HTML_EOF'
PASTE_FULL_HTML_HERE
HTML_EOF
```

If the output is `CONNECTION_REFUSED`, report:
> ⚠️ GenPage App is not running. Install or start it: https://github.com/nandzz/genpage

### Step 6: Report back to user

On success:
> Result sent to GenPage ↗

On failure:
- Report the exact error returned by the POST step.
