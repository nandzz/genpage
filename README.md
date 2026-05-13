<div align="center">

# GenPage

### Stop reading walls of markdown. Start *seeing* your AI's answers.

**GenPage turns the structured output your AI assistant already produces — tables, metrics, comparisons, dependency maps, audits — into Nandz Spaces: React mini-apps the local Nandz App compiles and renders live in your browser.**

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.7.0-blue.svg?style=for-the-badge)](skill.json)
[![Platforms](https://img.shields.io/badge/platforms-19+-purple.svg?style=for-the-badge)](#-works-everywhere)
[![Made with Skills](https://img.shields.io/badge/AI-Skill-ff69b4.svg?style=for-the-badge)](https://github.com/nandzz/genpage)

[**Install**](#-install-in-30-seconds) · [**How it works**](#-how-it-works) · [**Compatibility**](#-works-everywhere) · [**Nandz App**](https://github.com/nandzz/genpage)

</div>

---

## ✨ Why GenPage

Your AI assistant is brilliant at producing structured answers — but the chat window is the worst place to read them. Long tables wrap. Diagrams collapse into ASCII art. Comparisons lose their alignment. Findings get buried in scroll.

**GenPage fixes that.** It detects when an answer *wants* to be a Space — and routes it to a polished, interactive React app instead of dumping markdown into chat.

| Without GenPage | With GenPage |
|---|---|
| 📜 Endless scroll of markdown | 🖼️ A clean, scannable dashboard |
| 📋 Tables that wrap and break | 📊 Sortable, filterable tables |
| 🧩 ASCII diagrams | 🎨 Polished shadcn cards, timelines, and Recharts visualizations |
| 🔍 Findings lost in noise | 🎯 Audit panels with status, badges, deltas |
| 📵 Mobile-hostile output | 📱 Responsive, dark-mode aware, keyboard-friendly |

Every Space is a **plain `.tsx` bundle** — the local Nandz App owns the build, theming, and runtime. No telemetry, no cloud, no account.

---

## 🚀 Install in 30 seconds

> **Prerequisite:** the [Nandz App](https://github.com/nandzz/genpage) running on `127.0.0.1:5678`. It's a tiny local server that compiles and mounts Spaces — no cloud, no account, no tracking.
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

Drop `plugins/nandz-app/skills/genpage/SKILL.md` into your client's skills directory:

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

That's it. Next time your AI is about to produce a structured answer, it'll ask once: *"Send to Nandz?"* — and you're off.

---

## 🎬 How it works

```
┌────────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  AI assistant      │────▶│  GenPage skill   │────▶│  Nandz App       │
│  (any platform)    │     │  builds .tsx     │     │  compiles +      │
│                    │     │  bundle          │     │  mounts in iframe│
└────────────────────┘     └──────────┬───────┘     └──────────────────┘
        ▲                             │                       │
        │                             ▼                       │
        │                ~/.nandz/spaces/<id>/ ── POST ───────┘
        │                (manifest.json + index.tsx,
        │                 kept on disk after send)
        │
   "should this be
    a Space?"
```

1. **Trigger detection** — Fires when a response would naturally produce a table (3+ rows), grouped sections, metrics, comparisons, dependency maps, or diagrams. Trigger is the *shape of the answer*, not the wording of the question.
2. **One-time consent** — Asks once per session: *"Send to Nandz?"* with a detail level (Lean / Standard / Deep).
3. **Space generation** — Builds the Space as one or more `.tsx` files plus a `manifest.json`. Every file imports from one shared package: **`@nandz/ui`** — which re-exports shadcn primitives, shadcn chart wrappers (Recharts), and Lucide icons — plus `react`. Nothing else.
4. **POST** — Writes the folder to `~/.nandz/spaces/space-<timestamp>/`, packs it into a JSON envelope, and POSTs to `${NANDZ_HUB_URL}` (default `http://127.0.0.1:5678/render`). Files stay on disk for re-send. Logs to `~/.nandz/nandz.log`.
5. **Render** — The Nandz App compiles the bundle against its own monorepo (shared `@nandz/ui`, `ThemeProvider`, Inter, dark-mode shell) and mounts the entry component in your browser.

---

## 🌍 Works everywhere

Nandz is **model-agnostic** and **client-agnostic**. One skill, every assistant.

<div align="center">

`Claude Code` · `Cursor` · `Windsurf` · `GitHub Copilot` · `Continue` · `Kiro`
`Roo Code` · `Kilo Code` · `Codex` · `Qoder` · `Gemini` · `Trae`
`OpenCode` · `CodeBuddy` · `Droid` · `Warp` · `Augment` · `Antigravity`

</div>

If your assistant supports skills, plugins, or custom instructions — GenPage works.

---

## 🎨 What it can render

GenPage uses a single fixed stack — **React 18 + shadcn/ui** — for every Space. Every `.tsx` file imports from one shared package, **`@nandz/ui`**, which the host's monorepo provides: shadcn primitives, shadcn chart wrappers (built on Recharts), and Lucide icons. No other UI framework, chart library, or interactivity layer is permitted.

| You want to show… | GenPage uses |
|---|---|
| KPIs, deltas, status grids | shadcn `Card` + `Badge` + tabular-nums |
| Bar / line / pie / area / scatter | shadcn `ChartContainer` (Recharts under the hood) |
| Tables (sortable, stacked on mobile) | shadcn `Table` (stacked card list <`md:`) |
| Tabs, accordions, dialogs, tooltips | shadcn primitives over Radix UI |
| Linear sequences, steppers, timelines | shadcn `Card` + `Separator` + Lucide icons |
| Icons | Lucide React (re-exported from `@nandz/ui`) |
| Code snippets, math, maps, flowcharts, networks | not in the stack — redesigned as structured shadcn layouts |

Spaces are responsive, dark-mode aware, keyboard-navigable, and inherit the host's twelve named shadcn themes. Reduced-motion is honored. WCAG AA contrast by default.

---

## 📁 Repository layout

```
genpage/
├── .claude-plugin/
│   └── marketplace.json          # Claude Code marketplace catalog
├── plugins/
│   └── nandz-app/
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

- **100% local by default.** Spaces POST to `127.0.0.1:5678`. Nothing leaves your machine unless you point `NANDZ_HUB_URL` at a remote host yourself.
- **No telemetry.** No analytics, no tracking pixels, no third-party meta tags.
- **Local-only persistence.** Space bundles stay in `~/.nandz/spaces/` on your machine — nothing is uploaded anywhere. Delete them whenever you want.
- **No secrets in Spaces.** The skill's reference docs explicitly forbid embedding tokens, env vars, or credentials.
- **No CDNs in source, no eval, no `dangerouslySetInnerHTML`.** Every `.tsx` file imports only from `@nandz/ui`, `lucide-react`, and `react`.

---

## 🤝 Contributing

Issues and PRs welcome. The trigger evals live in [`evals/`](evals/) — if you've found a case where GenPage *should* fire but doesn't (or vice versa), add it there and open a PR.

---

## 📦 The Nandz App

The local renderer: a tiny server bound to `127.0.0.1:5678` that compiles and mounts whatever `.tsx` bundle the skill sends. The host owns the monorepo, the shared `@nandz/ui` package, the `ThemeProvider`, fonts, and the iframe shell.

**→ [github.com/nandzz/genpage](https://github.com/nandzz/genpage)**

---

<div align="center">

**Built by [Felipe Fernandes](https://github.com/nandzz)** · MIT License

*If GenPage made your AI feel less like a chatbot and more like a tool, ⭐ the repo.*

</div>
