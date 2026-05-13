# Security checklist

Run through every item before posting. If any fail, fix the Space first.

1. **No secrets.** No tokens, API keys, env vars, or credentials anywhere in the source, in data literals, or in comments.
2. **Imports are locked.** Every `.tsx` file imports only from `@nandz/ui`, `lucide-react` (icons), and `react`. No other packages, no inline CDN URLs in source, no `import('https://…')`, no dynamic imports.
3. **No DOM injection.** Never use `dangerouslySetInnerHTML`. Render data as text content; user/tool-provided strings flow through normal JSX interpolation so React escapes them.
4. **No dynamic execution.** No `eval`, no `new Function`, no `Function()` calls.
5. **No network calls.** The Space does not `fetch`, open `WebSocket`/`EventSource`, or load resources from any external origin. State persistence (when it lands) goes through the host SDK only.
6. **No tracking.** No analytics scripts, pixels, beacons, or telemetry side-effects.
7. **Images** follow `references/images.md` — only Wikimedia Commons URLs or local `file://` paths the user provided. No other domains, no `data:` URIs constructed at generation time.
8. **No iframes, no `<script>` tags, no `<style>` tags** authored in the Space. The host owns all of that.
