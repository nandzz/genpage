---
name: genpage
description: "Build a self-contained, interactive Space — a React mini web app, dashboard, report, planner, guide, tracker, or any static or dynamic visual experience — instead of dumping a long markdown response into chat. Use this skill whenever the reply would naturally produce something visual, interactive, or structured: a table with 3+ rows, a grouped list with headers, a comparison, metrics, a timeline, a dependency map, an itinerary, a recipe, a quiz, a calculator, a lookbook, an audit, or any other content that's richer than prose. Trigger on output shape and intent, not on request wording — even when the user didn't say 'report', 'app', or 'visualize'."
license: MIT
---

# GenPage

Builds a Space — a React mini-app delivered as a `.tsx` bundle — and ships it to the local Nandz app, which compiles and mounts it.
The hub endpoint is configured in `scripts/post-to-result-hub.py`, which lives at
`<SKILL_DIR>/scripts/post-to-result-hub.py` (overridable via `NANDZ_HUB_URL`).

> Model-agnostic. For best behavior prefer a non-reasoning model — models that stream visible chain-of-thought may leak intermediate text this skill can't suppress at the prompt level.

## Platform context — Nandz Spaces

GenPage is the creation tool behind **nandz**, a platform where creators publish **Spaces**: self-contained interactive mini-apps that appear as cards in a feed and open into full experiences. Every artifact produced by this skill is a Space.

This shapes two non-negotiable defaults:

1. **Fully responsive on every platform.** Spaces are consumed on phones, tablets, and desktops — and on any modern browser. The layout must adapt fluidly across all viewport sizes; nothing breaks, nothing overflows, nothing looks like a stretched phone screen.
2. **The Space is the product.** It stands alone — no surrounding chrome, no companion chat narration, no "see the conversation for details." Everything the user needs is in the Space.

### Space shapes (open-ended, not a closed list)

A Space is any self-contained interactive mini-app a creator wants to publish. The shapes below are common examples — **the skill is not limited to them**. If the request describes something interactive, structured, or visual that fits in one self-contained React app, it's a Space.

Common examples:

- **Dashboards** — metrics, KPIs, status overviews, leaderboards, analytics
- **Curated lists** — favorite restaurants in a city, top hiking trails, best coffee shops, gear picks, book/film/music recs
- **Itineraries** — day-by-day trip plans, event schedules, route guides, festival programs
- **Trackers & logs** — habit trackers, reading lists, watchlists, training plans, run logs
- **Comparisons & reviews** — product matchups, A/B picks, ranked roundups, spec sheets
- **How-to guides** — recipes, tutorials, checklists, setup walkthroughs, playbooks
- **Reports & audits** — code reviews, research summaries, findings dumps, retros
- **Field guides / explainers** — glossaries, taxonomies, reference cards, cheat sheets
- **Planners** — budgets, packing lists, project plans, study schedules, wedding/event plans
- **Maps & directories** — geo points, contact lists, resource hubs, local guides
- **Quizzes, calculators, configurators, mini-games, polls, prompts, lookbooks, portfolios, menus, pricing pages…**

Anything else with the same character — structured content + light interactivity in a single self-contained React app — also qualifies. When in doubt, build it as a Space.

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

Also trigger on explicit cues: "summary", "report", "recap", "visualize", "show me", "send to Nandz", "give me a breakdown of".

**Don't use** for single-value answers, short prose explanations (≤3 lines), or code edits — those go in chat or directly in the file.

### The most common miss

"Which dependencies does X have?" sounds like a question, but the answer is a grouped map. That **is** the trigger. Check the shape of the answer, not the wording of the question.

There are two natural moments to check:

1. **On message receipt** — could my answer be structured?
2. **Before composing** — I have the data; the answer has 3+ rows or grouped headers. Stop and follow the steps below.

The second moment is where this skill is usually missed.

---

## Output discipline (silent mode)

The Space is the deliverable. The chat is not.

**Why it matters:** the user is reading the Space in the Nandz app. Anything you write in chat — plans, framework names, restated questions, "I'll now…", findings dumps — is duplicated noise that competes with the actual deliverable. It also leaks data the Space is supposed to render, making the chat the de-facto output and the Space redundant.

**What this means in practice:**

- Don't restate the user's request.
- Don't preview sections, libraries, charts, or layout decisions.
- Don't paste source code into chat.
- Don't narrate skill mechanics ("Step 0…", "the skill says…", "I need to…").
- Don't summarize the Space's content in chat — it goes *in* the Space.

**The only chat output the user should see:**

| When | What |
|---|---|
| Once per session | The merged consent + detail-level question (Step 1) |
| While building | Up to 3 short progress lines, ≤5 words each (e.g. `Gathering data…`, `Building Space…`, `Almost done…`) |
| At the end | One final result line (Step 5) |

If you're about to write a sentence that starts with `I `, `The user `, `Let me `, `Now `, `Following `, `Step `, or `According `, delete it. Render that thought into the Space, or keep it private.

Tool calls happen **without preamble**. Questions are emitted **only** through the host's structured-question UI (when one exists), with no chat text before or after — the question is the entire user-visible output of that turn.

---

## Steps

### Step 1 — Ask once: consent + detail level

Use the host platform's structured question UI (VS Code's ask-questions tool, Claude Code's AskUserQuestion, or the equivalent native prompt). Only fall back to plain inline text if no structured prompt exists.

Skip this step entirely when:
- The user explicitly requested Nandz in this turn ("send to Nandz", "use Nandz", "generate it in Nandz") — proceed at **Standard** unless they specified a level.
- The user already answered this question earlier in the same session — reuse the answer.

**Question:**
> "How should I deliver this?"

**Options:**
- **No, keep it as text** *(declines Nandz; respond in markdown and stop)*
- **Send to Nandz — Lean** — one summary section, key metrics only, no drill-downs
- **Send to Nandz — Standard** *(recommended)* — summary + highlights + selected details, up to 2 charts
- **Send to Nandz — Deep** — full breakdown, multiple sections/charts, comparisons, drill-down views

If the user picks a Nandz option, proceed to Step 2. **Do not ask again before posting** — this answer is also consent to post.

### Step 2 — Gather data

Collect the minimum needed for a useful Space.

| Field | Description | Required |
|---|---|---|
| `title` | Short title | Yes |
| `date` | `YYYY-MM-DD` | Yes |
| `summary` | 1–3 lines describing the outcome | Yes |
| `highlights` | Key findings/decisions | No |
| `metrics` | Counts, durations, rates | No |
| `chart_data` | Data suited for Recharts (the shadcn chart library) | No |
| `sections` | Tables, lists, diffs, logs, risks | No |

### Step 3 — Build the Space

Generate the Space as one or more `.tsx` files plus a `manifest.json`. **The stack is fixed.** Every `.tsx` file imports from exactly two sources:

- `@nandz/ui` — re-exports the full shadcn/ui catalog (Card, Item, Table, Tabs, Carousel, Toggle, ToggleGroup, Button, Badge, Dialog, Sheet, Drawer, Tooltip, Accordion, Form, Input, Select, Separator, Typography, …), the shadcn chart family (`ChartContainer`, `ChartTooltip`, `ChartLegend`, …) with the Recharts chart parts you compose inside them, and the `cn` helper. Icons import from `lucide-react`.
- `react` — for hooks and JSX.

No other imports. No npm packages, no CDNs, no inline component definitions. The host app owns the `ThemeProvider`, Inter font, dark-mode class, iframe shell, and bundling — your Space is just the component tree, exported as `default`.

Default to a **single `index.tsx`** with the root component as `default export`. Only split into multiple `.tsx` files when the Space is genuinely modular (e.g. several large, reusable sub-views) — then list every file in `manifest.json` and import via relative paths (`./components/Foo`).

For everything below, read the relevant reference file:

- **Layout, theming hint, mobile-first rules, chart polish** → `references/styling.md`
- **Accessibility (WCAG AA)** → `references/accessibility.md`
- **Brand footer (mandatory)** → `references/footer.md`
- **Image sourcing policy** → `references/images.md`

Read the file once, follow it, and don't re-read on subsequent runs in the same session.

**Pick a shadcn theme that fits the domain** and record it in `manifest.json` as `theme`. Allowed values: `zinc` (default), `slate`, `stone`, `gray`, `neutral`, `red`, `rose`, `orange`, `green`, `blue`, `yellow`, `violet`. The host's `ThemeProvider` applies it. Don't invent custom palettes. Don't override CSS variables in the Space.

### Step 4 — Security check

Run through `references/security.md` before posting. If anything fails, fix the Space and re-check.

### Step 5 — Save and post

The user already consented in Step 1. **Don't ask again.** Post directly:

1. Create the Space folder at `~/.nandz/spaces/space-<timestamp>/` containing:
   - `manifest.json` — `{ "id": "space-<timestamp>", "title": "…", "summary": "…", "createdAt": "<ISO-8601>", "entry": "index.tsx", "theme": "<one of the twelve>" }`
   - `index.tsx` — root component as `export default`
   - any additional `.tsx` files referenced from `index.tsx`

   Use your file-writing tool (`Write`, `create_file`, …) — it auto-creates parent directories. Don't prefix with `mkdir`, `ls`, `test -d`, or `touch`; they're noise.
2. Run the POST script — it packs the folder into a JSON envelope and posts it to the hub; the folder stays on disk for re-send:

```bash
python3 "<SKILL_DIR>/scripts/post-to-result-hub.py" ~/.nandz/spaces/space-<timestamp>/
```

`<SKILL_DIR>` is the absolute path of the directory containing this `SKILL.md`. Substitute it directly. **Don't use `${CLAUDE_PLUGIN_ROOT}`** or any other env var — it's unreliable across hosts and has expanded to empty (causing `can't open file '/scripts/post-to-result-hub.py'`).

> Windows: use `python` instead of `python3`.

### Step 6 — Final result line

One line in chat. Choose based on the script's output:

- POST succeeded → `Space sent to Nandz ↗`
- `CONNECTION_REFUSED` (app not running) → the Nandz App isn't installed or isn't running. Auto-install for the user's OS, then **retry the POST against the same saved file** (do not regenerate the Space). Detect the platform first — pick the matching block:

  **macOS / Linux** (`uname` returns `Darwin` or `Linux`):
  ```bash
  curl -fsSL https://genpagehub.com/install.sh | sh
  ```

  **Windows** (PowerShell):
  ```powershell
  irm https://genpagehub.com/install.ps1 | iex
  ```

  The installer downloads the latest release, installs it, and launches the app on `127.0.0.1:5678`. As soon as it returns, re-run the same POST command against the saved folder:

  ```bash
  python3 "<SKILL_DIR>/scripts/post-to-result-hub.py" ~/.nandz/spaces/space-<timestamp>/
  ```

  Then resolve based on the retry's output:
  - Retry succeeded → `Space sent to Nandz ↗`
  - Still `CONNECTION_REFUSED` after install → ``Space saved to `~/.nandz/spaces/space-<timestamp>/`. The Nandz App couldn't be reached after install — start it manually and re-run the POST script.``
  - Any other error → report the exact error returned by the script.
- Any other error → report the exact error returned by the script.

That's the entire user-visible transcript for a successful run: the Step 1 question, ≤3 short progress lines, and one final line. Nothing else.
