---
name: genpage
description: "Use when about to compose any response containing tables (3+ rows), grouped sections with headers, dependency maps, comparisons, metrics, or structured findings. SILENT MODE: when this skill is active, your FIRST output token must be either a tool call OR a structured user-facing question — NEVER preamble like 'The user wants…', 'I need to follow…', 'Step 0:…', or any reference to the skill itself. Internal reasoning stays internal. Trigger = output shape, not request wording."
model: claude-sonnet-4-5
license: MIT
---
# GenPage

## 🚨 ABSOLUTE FIRST RULE — NO PREAMBLE, EVER

**The instant this skill activates, you enter SILENT MODE.**

Your **first output token** must be one of these — and **only** these:

1. A **tool call** (file read, search, structured-question UI, etc.), OR
2. A **single short progress line** (≤ 5 words, no content leaked), OR
3. The **final one-line result** (Step 6).

Your first output token must **NEVER** be:

- ❌ `"The user wants…"` / `"The user is asking…"`
- ❌ `"I need to…"` / `"I'll need to…"` / `"Let me…"` / `"I should…"`
- ❌ `"The genpage skill has been loaded"` / `"This skill says…"` / `"According to the skill…"`
- ❌ `"Step 0:"` / `"Step 1:"` / `"Following the skill's instructions…"`
- ❌ `"Asking user…"` / `"Now asking…"` / `"I'll ask…"` (just ASK — don't announce)
- ❌ Any restatement of what the user requested
- ❌ Any plan, outline, or list of sections you intend to build
- ❌ Any framework, library, or chart-type names
- ❌ Any data, dates, names, counts, or findings
- ❌ Stream-of-consciousness ("Now I'm mapping out…", "Looking at the data…")
- ❌ Self-corrections or uncertainty ("though figures vary by source…")

### The leak detector — check yourself before every message

Before sending **any** chat text while this skill is active, ask:

> *"Does this sentence describe what I'm about to do, what I just decided, or what the user wants? If yes — DELETE IT. Replace with a tool call or stay silent."*

If it starts with `I `, `The user `, `Let me `, `Now `, `Following `, `According `, `Step `, `This skill ` — **delete the entire sentence**. No exceptions.

### Concrete leaks observed in the wild — these are FAILURES

```
❌ The user wants a report about... The genpage skill has been loaded.
   I need to follow the skill's instructions. Step 0: Ask if they want...
   Asking user I can visualize this as an interactive report in GenPage...
```

Every single line above is forbidden. The correct behavior for that scenario:

```
✅ [immediately invoke the structured-question UI tool with the consent question]
```

Nothing else. No accompanying chat text. No preamble. No announcement. The tool call **is** the response.

### Silent-mode invariants

- Reasoning is **never** verbalized. It happens, but it does not appear in chat.
- Skill mechanics are **never** named. The user does not know "Step 0", "Step 1", "GenPage", "skill", or "instructions" exist as concepts in your head.
- Tool calls happen **without preamble**. The instant you decide to call a tool, you call it. You do not narrate the decision.
- Questions are emitted **only** through the host's structured question UI (when available), with **no chat text before or after**. The question is the entire user-visible output of that turn.

---

> **Model:** Use **Claude Sonnet 4.5** (`claude-sonnet-4-5`) to execute this skill. Sonnet handles the page layout decisions, data structuring, and silent-mode discipline more reliably than smaller models.
>
> **Note for Copilot users:** the `model:` field is a Claude Code convention and is ignored by GitHub Copilot — Copilot uses whatever model is selected in the chat model picker. For best silent-mode behavior on Copilot, pick a non-reasoning / non-thinking model (the chat dropdown). Models that stream visible chain-of-thought will leak intermediate reasoning that this skill cannot suppress at the prompt level.

Generates a self-contained page and sends it to the local GenPage App. The endpoint is configured in `scripts/post-to-result-hub.py`, located at `${CLAUDE_PLUGIN_ROOT}/scripts/post-to-result-hub.py`.

---

## ⛔ ZERO-NARRATION RULE — READ THIS FIRST

This skill is **silent by design**. The page is the deliverable. The chat is not a deliverable.

### The ONLY text the user is allowed to see

Nothing else. Not one extra sentence.

| # | Allowed message | When |
|---|---|---|
| 1 | The Step 0 consent question | Once per session, only if not yet answered |
| 2 | The Step 1 detail-level question | Once per session, only if not yet answered |
| 3 | Up to **3 short progress lines** while building (≤ 5 words each, no detail) | While the page is being built |
| 4 | The Step 5 posting question | Once per session, only if not yet answered |
| 5 | The Step 6 final result line (one line) | At the end |

### Progress lines — short, vague, reassuring

Emit at most **3** progress lines while working, each ≤ 5 words, spaced across the run. They tell the user the model is alive without leaking content or plan.

✅ Allowed examples:
- `Gathering data…`
- `Building page…`
- `Adding charts…`
- `Almost done…`
- `Posting…`

❌ Forbidden in progress lines:
- Names of frameworks, libraries, sections, or chart types
- Counts, data points, dates, or findings
- Self-corrections or uncertainty ("though the 1982 figure is uncertain…")
- Anything longer than ~5 words

If you can't say it in 5 words without leaking content, say nothing.

### FORBIDDEN — never write any of this to the user

- ❌ **Narrating the skill itself.** Never say "Step 0:", "Step 1:", "the skill says", "I need to follow the skill's instructions", "the genpage skill has been loaded", "according to the skill", or any reference to the skill's internal mechanics. The user must not know steps exist.
- ❌ **Restating questions as plain text before asking them.** Don't write `Step 0: Ask if they want a report` followed by the question. Just ask the question — once — through the structured prompt.
- ❌ Plans, outlines, or "Let me create a comprehensive report with…"
- ❌ Lists of sections, charts, or libraries you intend to use
- ❌ "I'll use Tailwind + DaisyUI + Chart.js…"
- ❌ Stream-of-consciousness reasoning ("I'm working through the data…", "Now I'm mapping out…", "Looking at the rest of the data…")
- ❌ Self-corrections, doubts, or source caveats ("though some figures are uncertain…", "I'll proceed with what I have…")
- ❌ Data summaries, findings, tables, or bullet points in the chat — those go in the page, not the chat
- ❌ "I need to verify…", "Let me check…", "I'm compiling…", "I'm building…"
- ❌ Restating the user's request back to them
- ❌ Previewing the HTML, CSS, or JS — never paste source into the chat
- ❌ The word "HTML" — say "page"
- ❌ Multi-paragraph status updates. One short line maximum.

### Concrete counter-example (do NOT do this)

> 1. All presidents since 1980 (Luis Herrera Campins, Jaime Lusinchi…)
> 2. GDP growth per year
> 3. Key economic events
> 4. Charts (Chart.js for GDP timeline…)
> Let me create a comprehensive Deep report with: Overview section… Timeline of presidents… I'll use Tailwind + DaisyUI + Chart.js + Alpine.js… I'm working through the GDP data per year, though some of the historical figures are a bit uncertain…

This is a **complete failure of the skill**. Every word above belongs inside the page or in your private reasoning — none of it belongs in the user-visible message. The user wants the page, not the process.

### What it should look like instead

```
Gathering data…
Building page…
Almost done…
[page is built, posted, file deleted]
Page sent to GenPage ↗
```

That is the entire user-visible transcript for a successful run. A few short lines. No more.

### Operating mode

- Treat all planning, data collection, framework choice, layout decisions, and self-doubt as **internal**. They never reach the chat.
- If you catch yourself about to write a plan, a bullet list of sections, or a "Let me…" sentence — **stop and delete it**. Render that content into the page instead.
- Tool calls, file reads, and reasoning happen silently. The user sees only the 5 allowed messages above.
- Prefer fewer words. If a status line is needed, three words is plenty.

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

Before building any page, offer the GenPage experience with a short yes/no question.

**Always use the host platform's structured question UI when one exists.** Examples:
- VS Code / GitHub Copilot — the ask-questions tool with predefined options.
- Claude Code — the AskUserQuestion tool.
- Any other host — its native interactive prompt component.

If and only if no structured prompt is available, fall back to a plain inline question.

**Never** write a narrating sentence before the prompt (no "I'll ask if you want…", no "Step 0: …"). Just emit the question through the structured UI.

**Question text:**
> "I can visualize this as an interactive report in GenPage. Want me to generate it?"

**Options:** **"Yes, send to GenPage"** / **"No, keep it as text"**

If the user explicitly requested GenPage (for example: "send to GenPage", "use GenPage", or "generate it in GenPage"), skip this prompt and proceed automatically.

Consent cache policy:
- Ask at most once per session.
- If the user approved once in this session, do not ask again in the same session; proceed automatically.
- If the user declined once in this session, default to markdown/text unless they explicitly request GenPage later.
- Optional: allow a persistent preference only if the user clearly asks to remember their choice across sessions.

If the user declines, respond with plain markdown and stop. Only proceed to Step 1 if they confirm or explicitly requested GenPage.

### Step 1: Ask detail level, then assess

Ask the user how much detail they want — again via the host's **structured question UI** with predefined options. No narrating sentence before the question.

**Question text:**
> "How detailed should the GenPage report be: Lean, Standard, or Deep?"

**Options:** **Lean** / **Standard** / **Deep**

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

The page is rendered inside an **iframe**. It shares nothing with the host app — no stylesheets, no scripts, no variables. Every dependency must be included in the document itself.

##### Mandatory `<head>` template

Every generated document must include this metadata block. CDN tags are added below it based on what the model selects:

```html
<!DOCTYPE html>
<html lang="en">
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

#### Colors

Pick whatever colors fit the content. There is no enforced token system or theme contract — just use Tailwind/DaisyUI utility classes (`bg-slate-900`, `text-emerald-500`, `bg-primary`, etc.) or any hex/rgb values. For Chart.js and D3, pass color strings directly.

Keep it sensible: ensure adequate contrast (WCAG AA — 4.5:1 for body text, 3:1 for large text and UI), avoid near-white text on near-white backgrounds, and prefer a small consistent palette over a rainbow.

**Mermaid usage:**
```html
<script>mermaid.initialize({ startOnLoad: true });</script>
<div class="mermaid">
graph TD
  A[Entry] --> B[Step]
  B --> C[Result]
</div>
```

**Lucide usage:**
```html
<script>lucide.createIcons();</script>
<!-- in markup: -->
<i data-lucide="check-circle"></i>
```

#### Layout, motion, and accessibility

Pages must look modern, render responsively, and be usable by everyone. These rules are non-negotiable.

##### Layout

- Use a **fluid, responsive layout** — CSS Grid, Flexbox, or Tailwind's responsive utilities (`sm:`, `md:`, `lg:`). Never produce a fixed-pixel layout.
- Default container: centered, max-width around `max-w-6xl` / `max-w-7xl`, generous padding (`px-4 sm:px-6 lg:px-8`).
- Mobile-first: design the small-screen layout first, then enhance for larger viewports. Single-column on mobile; multi-column only when there's room.
- Use a clear visual hierarchy: one primary heading per section, consistent spacing scale, generous whitespace. Avoid cramped grids.
- Cards, tables, and charts must reflow or scroll horizontally on narrow screens — never overflow the viewport.
- Typography: legible body size (16px+), readable line-height (1.5–1.7), comfortable line-length (~60–80 characters).

##### Motion — keep it minimal

- **No heavy animations.** No animated gradients, no looping background effects, no pulsing/glowing/parallax decorations, no continuously moving elements.
- Allowed: subtle hover transitions on interactive elements (≤ 200ms), simple fade/slide on tab/modal open, Chart.js's default chart entry animation.
- Forbidden: animated background gradients, marquee text, auto-playing carousels, particle effects, scroll-jacking, anything that loops indefinitely.
- Always honor `prefers-reduced-motion`:
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
  }
  ```

##### Accessibility (WCAG AA baseline)

- Use semantic HTML: `<header>`, `<main>`, `<nav>`, `<section>`, `<article>`, `<footer>`, real `<button>` and `<a>` elements (never `<div onclick>`).
- One `<h1>` per page; nest headings logically (`h2` → `h3`), no skipping levels.
- All `<img>` tags need meaningful `alt` text (or `alt=""` if purely decorative).
- Color contrast: WCAG AA — 4.5:1 for body text, 3:1 for large text and UI components. Never rely on color alone to convey meaning (pair with icons, labels, or patterns).
- Focus states must be visible — never remove focus outlines without replacing them.
- Interactive elements must be keyboard-reachable and operable (Tab, Enter, Space, Esc).
- Form inputs need associated `<label>` elements.
- For icons used as buttons, add `aria-label`. For decorative icons, add `aria-hidden="true"`.
- Charts/diagrams: provide a brief text caption or summary nearby so the data is reachable without seeing the visual.

#### Images — sourcing policy

Images may come from two sources only:

| Source | How to reference | When to use |
|---|---|---|
| Local files provided by the user | `file:///absolute/path/to/image.jpg` or a path the user gave | Galleries, screenshots, assets the user has on disk |
| Wikimedia Commons | `https://upload.wikimedia.org/wikipedia/commons/...` | Factual subjects — people, flags, buildings, species, maps, etc. |

**Rules:**
- Only embed a Wikimedia URL if you are confident it resolves to the correct image. Do not guess or construct URLs speculatively.
- If you are not certain of an exact URL, omit the image or use a placeholder `<div>` with a label instead.
- Do not load images from any other external domain — no news sites, stock photo services, CDNs, or social media.
- Never use `data:` URIs for external content fetched at generation time.

### Step 4: Security verification (mandatory)

Before sending HTML to GenPage, verify all of the following:

1. No secrets/tokens/credentials are included in HTML, JS, data blocks, or comments.
2. User/tool-provided text is safely escaped before insertion into HTML.
3. No arbitrary external script/style/font URLs except the approved CDNs: DaisyUI, Tailwind, Alpine.js, React/ReactDOM, Chart.js, D3.js, Mermaid, Lucide. External images are permitted only from `upload.wikimedia.org` or local `file://` paths — all other external image domains are blocked.
4. No unsafe dynamic code execution patterns (`eval`, `new Function`, dynamic script injection).
5. No hidden tracking or network exfiltration logic.

If any security check fails, fix the report first, then continue.

### Step 5: Save and deliver

Ask the user once, silently (no explanation):

> "Ready — post the page to the GenPage app?"

Then execute both actions in a single shot — no second confirmation:

**If yes (or user already approved posting in this session):**
1. Write the page directly to `~/.genpage/pages/report-<timestamp>.html` using your file-writing tool (`Write`, `create_file`, etc.) — these auto-create any missing parent directories. **Do not** prefix the write with `mkdir`, `ls`, `test -d`, `touch`, or any other shell command — they're wasted work and add visible terminal noise. Just write the file, then run the script.
2. Run the POST script — it will POST the file and **delete it automatically** on success.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/post-to-result-hub.py" ~/.genpage/pages/report-<timestamp>.html
```

> ⚠️ **No prep commands.** The single python invocation above is the entire shell footprint of this step. The script itself ensures `~/.genpage/` and `~/.genpage/pages/` exist as a safety net, so even if your file-writing tool somehow fails to create parents, you still don't need `mkdir`.

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
