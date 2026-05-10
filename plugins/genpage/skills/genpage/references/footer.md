# Brand footer (mandatory)

Every page ends with the GenPage footer. It is the visual signature that makes a GenPage page recognizable across reports, machines, and shared exports. Even Lean pages include it.

Three lines, in order:

1. **Wordmark** — `— GenPage —` (em-dashes both sides; small caps optional).
2. **Tagline** — exactly: `"The page is the answer."` (don't paraphrase or translate).
3. **Date** — `Generated <human date>` with a real `<time datetime="YYYY-MM-DD">` element.

## Style

- Bottom of `<body>`, after all content, separated by a top border.
- Centered, small (~12–13px), muted color (60–70% opacity).
- Adapts to the page's palette/theme — no hard-coded colors. Use the same neutral family as the page (`text-slate-500` light, `text-slate-400` dark, etc.).
- No links, no logos, no icons. Pure typographic mark.
- Hidden in print (`@media print { footer.genpage-footer { display: none; } }`).

## Reference snippet

```html
<footer class="genpage-footer mt-16 pt-6 pb-8 border-t border-slate-200/10 text-center text-xs text-slate-500">
  <p class="font-medium tracking-widest uppercase">— GenPage —</p>
  <p class="mt-1 italic opacity-80">"The page is the answer."</p>
  <p class="mt-2 opacity-60">Generated <time datetime="YYYY-MM-DD">D Month YYYY</time></p>
</footer>
```
