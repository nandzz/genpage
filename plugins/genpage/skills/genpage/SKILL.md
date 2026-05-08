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

### Step 1: Ask detail level (token control)

Before gathering data, ask the user how much detail they want so they can control token usage.

Suggested prompt:
> "How detailed should the GenPage report be: Lean, Standard, or Deep?"

If the user does not specify, default to **Standard**.

Detail levels:
- **Lean (lowest token usage):** one summary section, key metrics only, max 1 chart, no drill-down sections, concise labels/text.
- **Standard (balanced):** summary + highlights + selected details, up to 2 charts, limited expandable detail.
- **Deep (highest token usage):** full breakdown, multiple sections/charts, comparisons, drill-down views, richer annotations.

Apply the selected level to:
- data collection depth
- number of sections and charts
- interactivity complexity
- length of explanatory text

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

#### Interactivity — use when it earns its place

For static layouts (Lean mode, flat tables, single metrics): **do not load React or Chart.js.** Plain HTML + Tailwind/DaisyUI is sufficient and generates fewer tokens.

Only add these when genuinely needed:

```html
<!-- Only for interactivity / state -->
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>

<!-- Only for quantitative charts -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>

<!-- Only for diagrams (flows, sequences, trees, ER) -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
```

**Good reasons to load React:**
- The report has tabs, toggles, or filters that switch visible content
- Comparing two states (before/after, pass/fail) benefits from a toggle
- Expandable drill-down rows that can't be done with a `<details>` element

**Good reasons to load Chart.js:**
- The data has a quantitative distribution, trend, or comparison that a table can't communicate

**Good reasons to load Mermaid:**
- The data is graph-shaped: dependency trees, call chains, architecture layers, state machines, ER diagrams, git graphs, sequence flows
- A table or list would flatten relationships that have direction or hierarchy
- Mermaid is more token-efficient than generating SVG or canvas code — the model writes a short text definition, Mermaid renders it

Mermaid usage pattern:
```html
<script>mermaid.initialize({ startOnLoad: true, theme: 'dark' });</script>
<div class="mermaid">
graph TD
  A[Entry] --> B[Step]
  B --> C[Result]
</div>
```

Use `theme: 'dark'` to stay consistent with the `genpage` DaisyUI theme. Do not hardcode colors inside Mermaid definitions.

**Do not add interactivity when:**
- A single well-structured static layout already tells the full story
- The only data is a flat list or a single metric
- The interaction would be decoration rather than navigation

DaisyUI provides many interactive-looking patterns (tabs via radio inputs, collapse via `<details>`, badges, stats) that require **zero JavaScript** — prefer these over React for simple navigation.

### Step 4: Security verification (mandatory)

Before sending HTML to GenPage, verify all of the following:

1. No secrets/tokens/credentials are included in HTML, JS, data blocks, or comments.
2. User/tool-provided text is safely escaped before insertion into HTML.
3. No arbitrary external script/style/image/font URLs except the allowed React/ReactDOM/Chart.js/Mermaid CDNs.
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
