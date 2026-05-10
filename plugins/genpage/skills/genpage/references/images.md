# Images — sourcing policy

Two sources only. Anything else is blocked by the security check.

| Source | Reference as | Use for |
|---|---|---|
| Local files the user provided | `file:///absolute/path/to/image.jpg` | Galleries, screenshots, user-supplied assets |
| Wikimedia Commons | `https://upload.wikimedia.org/wikipedia/commons/...` | Factual subjects — people, flags, buildings, species, maps |

Rules:

- Only embed a Wikimedia URL if you are confident it resolves to the right image. Don't guess or construct URLs speculatively.
- If you're unsure of the exact URL, omit the image or use a labeled placeholder `<div>` instead.
- No other external image domains — no news sites, stock services, CDNs, social media.
- No `data:` URIs for content fetched at generation time.
