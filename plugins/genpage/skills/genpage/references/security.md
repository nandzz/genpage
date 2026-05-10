# Security checklist

Run through every item before posting. If any fail, fix the page first.

1. No secrets, tokens, or credentials in HTML, JS, data blocks, or comments.
2. User/tool-provided text is escaped before insertion into HTML.
3. No external script/style/font URLs except the approved CDNs: Tailwind, DaisyUI, MUI, Alpine.js, React/ReactDOM, Chart.js, D3.js, Mermaid, Lucide. External images permitted only from `upload.wikimedia.org` or local `file://` paths.
4. No unsafe dynamic execution (`eval`, `new Function`, dynamic script injection).
5. No tracking, analytics, or network exfiltration logic.
