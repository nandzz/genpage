# Images — sourcing & framing policy

## Sources

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

## Framing — never crop through a face or subject

You don't know the source image's dimensions or where the subject sits inside the frame. Treat every remote image as **unknown aspect ratio + unknown focal point** and let the browser fit it safely. The most common failure is a portrait stuffed into a square `object-cover` box, slicing the face down the middle or chopping off the top of the head.

### Default — show the whole image (safe everywhere)

When in doubt, use `object-contain`. The image is never cropped; whitespace appears around it instead.

```html
<!-- Card / hero / inline figure where cropping the subject is unacceptable -->
<figure className="aspect-[4/3] w-full overflow-hidden rounded-xl bg-muted">
  <img
    src="https://upload.wikimedia.org/wikipedia/commons/..."
    alt="<descriptive alt>"
    loading="lazy"
    decoding="async"
    className="w-full h-full object-contain"
  />
</figure>
```

### When cropping is required (tiles, banners, avatars)

If the layout *must* fill the box, use `object-cover` **with an explicit `object-position`** biased toward where the subject usually lives:

| Subject | `object-position` | Why |
|---|---|---|
| Person / portrait / headshot | `object-top` (or `object-[center_top]`) | Faces sit in the top third — `center` clips foreheads |
| Group photo, full-body | `object-[center_30%]` | Heads near the top, not dead center |
| Building / landscape / map | `object-center` | Default is fine |
| Product / object on background | `object-center` | Default is fine |
| Flag | `object-contain` only — never crop a flag | Crops change the flag's meaning |

```html
<!-- Portrait tile that must fill a fixed ratio -->
<figure className="aspect-square w-full overflow-hidden rounded-2xl bg-muted">
  <img
    src="https://upload.wikimedia.org/wikipedia/commons/..."
    alt="<descriptive alt>"
    loading="lazy"
    decoding="async"
    className="w-full h-full object-cover object-top"
  />
</figure>
```

### Avatars (circular crops)

Circular masks amplify bad framing — any miss shows as a sliced jaw or forehead.

```html
<img
  src="..."
  alt="<name>"
  className="w-16 h-16 rounded-full object-cover object-top ring-2 ring-border"
/>
```

### Hard rules

- **Never** apply `object-cover` without an `object-position` on photos of people. Default `object-position: center` will cut faces in half on portraits.
- **Never** force a fixed `width` *and* `height` (or a different `aspect-ratio`) on an `<img>` without `object-contain` or `object-cover` — the image will stretch or squash.
- **Always** set `alt`. Decorative-only images get `alt=""`, never a missing attribute.
- **Always** set `loading="lazy"` and `decoding="async"` on non-critical images.
- **Always** give the wrapper a neutral background (`bg-muted`) so `object-contain` letterboxing doesn't look like a layout bug.
- Prefer **portrait-friendly aspect ratios** (`aspect-[3/4]`, `aspect-square`) for portrait subjects. Don't drop a tall portrait into `aspect-video` and crop.
- If a Wikimedia image's framing is unknown and the layout demands a tight crop, **pick `object-contain` and accept the letterboxing** — a whole face with bars beats half a face filling the box.
