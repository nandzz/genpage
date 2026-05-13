# Brand footer (mandatory)

Every Space ends with the Nandz footer. It is the visual signature that makes a Nandz Space recognizable across creations, machines, and shared exports. Even Lean Spaces include it.

Three lines, in order:

1. **Wordmark** — `— Nandz —` (em-dashes both sides).
2. **Tagline** — exactly: `Generating Pages` (don't paraphrase or translate).
3. **Date** — `Generated <human date>` with a real `<time dateTime="YYYY-MM-DD">` element.

## Style

- Render at the bottom of the Space, after all content, separated by a top border.
- Centered, small (~12–13px), muted via `text-muted-foreground`.
- No links, no logos, no icons. Pure typographic mark.
- Inherits the active theme automatically through shadcn semantic tokens — never hand-pick colors.

## Reference component

```tsx
function NandzFooter({ generatedOn }: { generatedOn: Date }) {
  const iso = generatedOn.toISOString().slice(0, 10);
  const human = generatedOn.toLocaleDateString(undefined, {
    day: 'numeric', month: 'long', year: 'numeric',
  });
  return (
    <footer className="mt-16 pt-6 pb-8 border-t text-center text-xs text-muted-foreground print:hidden">
      <p className="font-medium tracking-widest uppercase">— Nandz —</p>
      <p className="mt-1 italic opacity-80">Generating Pages</p>
      <p className="mt-2 opacity-70">
        Generated <time dateTime={iso}>{human}</time>
      </p>
    </footer>
  );
}
```

Drop it at the end of your root component's JSX. One footer per Space.
