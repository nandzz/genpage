# GenPage

Converts any structured AI response — tables, grouped sections, metrics, dependency maps, comparisons, diagrams — into a self-contained interactive HTML report rendered by the local **GenPage App**.

The skill intercepts responses that would naturally produce structured output and routes them to a browser-based viewer instead of dumping markdown into the chat.

---

## Prerequisites

| Requirement | Notes |
|---|---|
| **GenPage App** | Must be running on `127.0.0.1:5678`. [Install here →](https://github.com/nandzz/genpage) |
| **Python 3.6+** | Pre-installed on macOS/Linux. [Download for Windows →](https://www.python.org/downloads/) |

> **Windows:** Use `python` instead of `python3` in all commands below.

---

## Installation

### GitHub CLI (recommended)

```bash
gh skill install nandzz/genpage
```

### Claude Code

```bash
claude plugin marketplace add nandzz/genpage
```

Then install the plugin:

```bash
claude plugin install genpage@genpage-marketplace
```

### Manual install (all other clients)

Copy `skills/genpage/SKILL.md` to your client's skill directory:

| Client | Skill directory |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Cursor | `.cursor/skills/` in your project |
| Windsurf | `.windsurf/skills/` in your project |
| Copilot (VS Code) | `.github/` + configure in `copilot-instructions.md` |
| Continue | `.continue/` |
| Kiro | `.kiro/skills/` |
| Roo Code / Kilo Code | `.roo/skills/` |

---

## How it works

1. **Trigger detection** — The skill fires when a response would produce a table (3+ rows), grouped sections, metrics, comparisons, dependency maps, or diagrams.
2. **Consent** — Asks once per session: *"Visualize in GenPage?"*
3. **Detail level** — Lean / Standard / Deep (controls token usage).
4. **HTML generation** — Generates a self-contained report using Tailwind CSS + DaisyUI for styling, with optional Chart.js (quantitative charts) and Mermaid (flow/sequence/ER diagrams). React is only loaded when interactivity is needed.
5. **POST** — Writes the report to `~/.genpage/report-<timestamp>.html`, POSTs it to the GenPage App, deletes the file. A log is appended to `~/.genpage/genpage.log`.
6. **Rendered** — The GenPage App displays the report in your browser.

---

## Theme and colors

All colors are controlled by the `genpage` DaisyUI theme defined in the GenPage App. The skill only assigns semantic tokens (`text-primary`, `badge-success`, `bg-base-200`, etc.) — it never hardcodes color values. To change the palette, update the theme in the App.

---

## Directory structure

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
│               ├── SKILL.md      # Skill definition
│               └── scripts/
│                   └── post-to-result-hub.py  # POST script (Python stdlib only)
├── README.md
└── skill.json                    # Multi-platform skill metadata
```

---

## GenPage App

The GenPage App is the local server that receives and renders reports. It binds to `127.0.0.1:5678` and applies the `genpage` DaisyUI theme.

[https://github.com/nandzz/genpage](https://github.com/nandzz/genpage)

---

## License

MIT © [Felipe Fernandes](https://github.com/nandzz)
