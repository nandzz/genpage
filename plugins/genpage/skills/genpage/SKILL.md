---
name: genpage
description: "Send a self-contained, interactive HTML report to the local GenPage app instead of dumping a long markdown response into chat. Use this skill whenever your reply would naturally produce a table with 3+ rows, a grouped list with headers, a comparison, a set of metrics, a timeline, a dependency map, or any audit/findings summary — even when the user didn't explicitly say 'report' or 'visualize'. Trigger on output shape, not on request wording."
license: MIT
---

# GenPage

Generates a self-contained HTML page and posts it to the local GenPage app.
The endpoint is configured in `scripts/post-to-result-hub.py`, which lives at
`<SKILL_DIR>/scripts/post-to-result-hub.py`.

> Model-agnostic. For best behavior prefer a non-reasoning model — models that stream visible chain-of-thought may leak intermediate text this skill can't suppress at the prompt level.

---

## When to use

The trigger is the **shape of the answer**, not the words in the request.

Use GenPage when your reply would otherwise contain any of:

| Shape | Examples |
|---|---|
| Table with 3+ rows | dependency list, file inventory, API endpoints, test results |
| Grouped list with headers | architecture layers, module breakdown, error categories |
| Comparison between 2+ items | before/after, A vs B, file-vs-file |
| Counts or metrics | N files changed, M dependencies, K failing tests |
| Timeline or sequence | commit history, migration steps, event flow |
| Findings / audit summary | security issues, code smells, missing coverage, TODOs |
| Anything plain text flattens | dependency graphs, layer diagrams, trees |

Also trigger on explicit cues: "summary", "report", "recap", "visualize", "show me", "send to GenPage", "give me a breakdown of".

**Don't use** for single-value answers, short prose explanations (≤3 lines), or code edits — those go in chat or directly in the file.

### The most common miss

"Which dependencies does X have?" sounds like a question, but the answer is a grouped map. That **is** the trigger. Check the shape of the answer, not the wording of the question.

There are two natural moments to check:

1. **On message receipt** — could my answer be structured?
2. **Before composing** — I have the data; the answer has 3+ rows or grouped headers. Stop and follow the steps below.

The second moment is where this skill is usually missed.

---

## Output discipline (silent mode)

The page is the deliverable. The chat is not.

**Why it matters:** the user is reading the page in the GenPage app. Anything you write in chat — plans, framework names, restated questions, "I'll now…", findings dumps — is duplicated noise that competes with the actual deliverable. It also leaks data the page is supposed to render, making the chat the de-facto output and the page redundant.

**What this means in practice:**

- Don't restate the user's request.
- Don't preview sections, libraries, charts, or layout decisions.
- Don't paste HTML/CSS/JS into chat.
- Don't narrate skill mechanics ("Step 0…", "the skill says…", "I need to…").
- Don't summarize the report's findings in chat — those go *in* the report.

**The only chat output the user should see:**

| When | What |
|---|---|
| Once per session | The merged consent + detail-level question (Step 1) |
| While building | Up to 3 short progress lines, ≤5 words each (e.g. `Gathering data…`, `Building page…`, `Almost done…`) |
| At the end | One final result line (Step 5) |

If you're about to write a sentence that starts with `I `, `The user `, `Let me `, `Now `, `Following `, `Step `, or `According `, delete it. Render that thought into the page, or keep it private.

Tool calls happen **without preamble**. Questions are emitted **only** through the host's structured-question UI (when one exists), with no chat text before or after — the question is the entire user-visible output of that turn.

---

## Steps

### Step 1 — Ask once: consent + detail level

Use the host platform's structured question UI (VS Code's ask-questions tool, Claude Code's AskUserQuestion, or the equivalent native prompt). Only fall back to plain inline text if no structured prompt exists.

Skip this step entirely when:
- The user explicitly requested GenPage in this turn ("send to GenPage", "use GenPage", "generate it in GenPage") — proceed at **Standard** unless they specified a level.
- The user already answered this question earlier in the same session — reuse the answer.

**Question:**
> "How should I deliver this?"

**Options:**
- **No, keep it as text** *(declines GenPage; respond in markdown and stop)*
- **Send to GenPage — Lean** — one summary section, key metrics only, no drill-downs
- **Send to GenPage — Standard** *(recommended)* — summary + highlights + selected details, up to 2 charts
- **Send to GenPage — Deep** — full breakdown, multiple sections/charts, comparisons, drill-down views

If the user picks a GenPage option, proceed to Step 2. **Do not ask again before posting** — this answer is also consent to post.

### Step 2 — Gather data

Collect the minimum needed for a useful page.

| Field | Description | Required |
|---|---|---|
| `title` | Short title | Yes |
| `date` | `YYYY-MM-DD` | Yes |
| `summary` | 1–3 lines describing the outcome | Yes |
| `highlights` | Key findings/decisions | No |
| `metrics` | Counts, durations, rates | No |
| `chart_data` | Data suited for Chart.js | No |
| `sections` | Tables, lists, diffs, logs, risks | No |

### Step 3 — Build the page

Generate one self-contained HTML document. The body layout is unconstrained — pick whatever structure best represents the data.

For everything below, read the relevant reference file:

- **Framework choice, CDNs, colors, scrollbars, motion, layout** → `references/styling.md`
- **Accessibility (WCAG AA)** → `references/accessibility.md`
- **Brand footer (mandatory)** → `references/footer.md`
- **Image sourcing policy** → `references/images.md`

Read the file once, follow it, and don't re-read on subsequent runs in the same session.

**Optional design data** — when the report would benefit from a non-default palette or font pair (branded report, themed dashboard, content with a clear mood like "financial", "wellness", "editorial"), consult `references/data/`:

- `colors.csv` — 161 industry-mapped palettes (`Product Type` column → palette tokens). Pick one whose `Product Type` or `Notes` matches the report's domain.
- `typography.csv` — 57 Google Fonts pairings with `Mood/Style Keywords` and `CSS Import`. Drop the `CSS Import` line straight into `<head>`.
- `ux-guidelines.csv` — 99 anti-patterns/best practices (Do / Don't / Severity). Skim for `High` severity rules relevant to your sections (tables, navigation, forms, accessibility).

Don't load these files for every report — only when default Inter + DaisyUI theme isn't a good fit. Files are bundled under MIT from `nextlevelbuilder/ui-ux-pro-max-skill`; see `references/data/NOTICE.md`.

### Step 4 — Security check

Run through `references/security.md` before posting. If anything fails, fix the page and re-check.

### Step 5 — Save and post

The user already consented in Step 1. **Don't ask again.** Post directly:

1. Write the page to `~/.genpage/pages/report-<timestamp>.html` using your file-writing tool (`Write`, `create_file`, etc.) — these auto-create missing parent directories. Don't prefix with `mkdir`, `ls`, `test -d`, or `touch`; they're noise.
2. Run the POST script — it posts the file and deletes it on success:

```bash
python3 "<SKILL_DIR>/scripts/post-to-result-hub.py" ~/.genpage/pages/report-<timestamp>.html
```

`<SKILL_DIR>` is the absolute path of the directory containing this `SKILL.md`. Substitute it directly. **Don't use `${CLAUDE_PLUGIN_ROOT}`** or any other env var — it's unreliable across hosts and has expanded to empty (causing `can't open file '/scripts/post-to-result-hub.py'`).

> Windows: use `python` instead of `python3`.

### Step 6 — Final result line

One line in chat. Choose based on the script's output:

- POST succeeded → `Page sent to GenPage ↗`
- `CONNECTION_REFUSED` (app not running) → ``Page saved to `~/.genpage/pages/report-<timestamp>.html` ``
- Any other error → report the exact error returned by the script.

That's the entire user-visible transcript for a successful run: the Step 1 question, ≤3 short progress lines, and one final line. Nothing else.
