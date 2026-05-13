# Accessibility (WCAG AA baseline)

Every Space must be usable without a mouse and without color perception. These are the rules.

- Use semantic JSX: `<header>`, `<main>`, `<nav>`, `<section>`, `<article>`, `<footer>`, real `<button>` and `<a>` (or the shadcn `Button` / a styled `<a>` — never `<div onClick>`).
- One `<h1>` per Space; nest headings logically (`h2` → `h3`); don't skip levels.
- All `<img>` need meaningful `alt` (or `alt=""` if purely decorative).
- Contrast: 4.5:1 body, 3:1 for large text/UI. Never rely on color alone — pair with icons, labels, or patterns.
- Focus states must be visible. Don't strip outlines without a replacement.
- Interactive elements must be keyboard-reachable (Tab, Enter, Space, Esc).
- Form inputs need associated `<label>`.
- Icon buttons need `aria-label`. Decorative icons need `aria-hidden="true"` (lucide icons accept it directly).
- Charts/diagrams need a short text caption or summary nearby — the data must be reachable without seeing the visual.
