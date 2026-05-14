<div align="center">

# GenPage

### Stop reading walls of markdown. Start *seeing* your AI's answers.

**GenPage turns the structured output your AI assistant already produces — tables, metrics, comparisons, dependency maps, audits — into beautiful, interactive HTML reports rendered live in your browser.**

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.8.1-blue.svg?style=for-the-badge)](skill.json)
[![Platforms](https://img.shields.io/badge/platforms-19+-purple.svg?style=for-the-badge)](#-works-everywhere)
[![Made with Skills](https://img.shields.io/badge/AI-Skill-ff69b4.svg?style=for-the-badge)](https://github.com/nandzz/genpage)

[**Install**](#-install-in-30-seconds) · [**How it works**](#-how-it-works) · [**Compatibility**](#-works-everywhere) · [**GenPage App**](https://github.com/nandzz/genpage)

</div>

---

## ✨ Why GenPage

Your AI assistant is brilliant at producing structured answers — but the chat window is the worst place to read them. Long tables wrap. Diagrams collapse into ASCII art. Comparisons lose their alignment. Findings get buried in scroll.

**GenPage fixes that.** It detects when an answer *wants* to be a report — and routes it to a polished, interactive page instead of dumping markdown into chat.

| Without GenPage | With GenPage |
|---|---|
| 📜 Endless scroll of markdown | 🖼️ A clean, scannable dashboard |
| 📋 Tables that wrap and break | 📊 Sortable, filterable tables |
| 🧩 ASCII diagrams | 🎨 Real flowcharts (React Flow, ECharts, D3) |
| 🔍 Findings lost in noise | 🎯 Audit panels with status, badges, deltas |
| 📵 Mobile-hostile output | 📱 Responsive, dark-mode aware, keyboard-friendly |

Every page is **self-contained HTML** — no build step, no framework lock-in, no telemetry. Just one file, sent to a local app on your machine.

---

## 🚀 Install in 30 seconds

> **Prerequisite:** the [GenPage App](https://github.com/nandzz/genpage) running on `127.0.0.1:5678`. It's a tiny local server that renders the reports — no cloud, no account, no tracking.
>
> **macOS / Linux:**
> ```bash
> curl -fsSL https://genpagehub.com/install.sh | sh
> ```
>
> **Windows (PowerShell):**
> ```powershell
> irm https://genpagehub.com/install.ps1 | iex
> ```
>
> The installer downloads the latest release, installs it, and launches the app.

### 🥇 GitHub CLI (recommended)

```bash
gh skill install nandzz/genpage
```

### 🤖 Claude Code

```bash
claude plugin marketplace add nandzz/genpage
claude plugin install genpage@genpage-marketplace
```

### 🛠️ Manual install (everything else)

Drop `plugins/genpage/skills/genpage/SKILL.md` into your client's skills directory:

| Client | Path |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Cursor | `.cursor/skills/` |
| Windsurf | `.windsurf/skills/` |
| GitHub Copilot (VS Code) | `.github/` + reference in `copilot-instructions.md` |
| Continue | `.continue/` |
| Kiro | `.kiro/skills/` |
| Roo Code / Kilo Code | `.roo/skills/` |
| Codex / Gemini / Trae / Warp | client-specific skills folder |

That's it. Next time your AI is about to produce a structured answer, it'll ask once: *"Visualize in GenPage?"* — and you're off.

---

## 🎬 How it works

```
┌────────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  AI assistant      │────▶│  GenPage skill   │────▶│  GenPage App     │
│  (any platform)    │     │  builds HTML     │     │  renders in      │
│                    │     │  (self-contained)│     │  your browser    │
└────────────────────┘     └──────────────────┘     └──────────────────┘
        ▲                          │                         │
        │                          ▼                         │
        │                  ~/.genpage/pages/*.html ── POST ──┘
        │                  (kept on disk after send)
        │
   "should this be
    a report?"
```

1. **Trigger detection** — Fires when a response would naturally produce a table (3+ rows), grouped sections, metrics, comparisons, dependency maps, or diagrams. Trigger is the *shape of the answer*, not the wording of the question.
2. **One-time consent** — Asks once per session: *"Visualize in GenPage?"* with a detail level (Lean / Standard / Deep).
3. **HTML generation** — Builds a self-contained report using Tailwind CSS + DaisyUI, plus the *one* viz library that fits the data (Chart.js, ECharts, React Flow, D3, Cytoscape, Leaflet, Tabulator, KaTeX…).
4. **POST** — Writes to `~/.genpage/pages/report-<timestamp>.html`, POSTs to the local app, and keeps the file on disk so you can re-open or re-send it. Logs to `~/.genpage/genpage.log`.
5. **Render** — The GenPage App displays it in your browser.

---

## 🌍 Works everywhere

GenPage is **model-agnostic** and **client-agnostic**. One skill, every assistant.

<div align="center">

`Claude Code` · `Cursor` · `Windsurf` · `GitHub Copilot` · `Continue` · `Kiro`
`Roo Code` · `Kilo Code` · `Codex` · `Qoder` · `Gemini` · `Trae`
`OpenCode` · `CodeBuddy` · `Droid` · `Warp` · `Augment` · `Antigravity`

</div>

If your assistant supports skills, plugins, or custom instructions — GenPage works.

---

## 🎨 What it can render

GenPage picks the right tool for each shape of data — never more than one viz library per page.

| You want to show… | GenPage uses |
|---|---|
| KPIs, deltas, status grids | Tailwind + DaisyUI stat cards |
| Bar / line / pie / area | Chart.js |
| Heatmap, sankey, treemap, gauge, gantt | ECharts |
| Flowcharts, architecture diagrams, mind maps | React Flow + dagre auto-layout |
| Network / dependency graphs | Cytoscape.js |
| Maps, geo data | Leaflet |
| Large sortable/filterable tables | Tabulator |
| Math / equations | KaTeX |
| Code with syntax highlighting | highlight.js |
| Custom SVG, bespoke viz | D3.js |

Pages are responsive, dark-mode aware, keyboard-navigable, and ship with theme-matched scrollbars. Reduced-motion is honored. WCAG AA contrast by default.

---

## 📁 Repository layout

```
genpage/
├── .claude-plugin/
│   └── marketplace.json          # Claude Code marketplace catalog
├── plugins/
│   └── genpage/
│       ├── .claude-plugin/
│       │   └── plugin.json       # Claude Code plugin manifest
│       └── skills/
│           └── genpage/
│               ├── SKILL.md           # Skill definition
│               ├── references/        # Styling, accessibility, security, images, footer
│               └── scripts/
│                   └── post-to-result-hub.py  # Python stdlib only
├── evals/                        # Trigger-detection evals
├── README.md
├── LICENSE
└── skill.json                    # Multi-platform skill metadata
```

---

## 🔒 Privacy & security

- **100% local.** Reports POST to `127.0.0.1:5678`. Nothing leaves your machine.
- **No telemetry.** No analytics, no tracking pixels, no third-party meta tags.
- **Local-only persistence.** HTML reports stay in `~/.genpage/pages/` on your machine — nothing is uploaded anywhere. Delete them whenever you want.
- **No secrets in pages.** The skill's reference docs explicitly forbid embedding tokens, env vars, or credentials.

---

## 🤝 Contributing

Issues and PRs welcome. The trigger evals live in [`evals/`](evals/) — if you've found a case where GenPage *should* fire but doesn't (or vice versa), add it there and open a PR.

---

## 📦 The GenPage App

The local renderer: a tiny server bound to `127.0.0.1:5678` that displays whatever HTML the skill sends.

**→ [github.com/nandzz/genpage](https://github.com/nandzz/genpage)**

---

<div align="center">

**Built by [Felipe Fernandes](https://github.com/nandzz)** · MIT License

*If GenPage made your AI feel less like a chatbot and more like a tool, ⭐ the repo.*

</div>
