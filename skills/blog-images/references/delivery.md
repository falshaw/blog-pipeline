# Delivery — web image specs, markup, privacy

The site's own config (`images.dir`, `images.og`, `images.widths`) and the newest live post are the canonical source for paths and markup. This file is the reasoning and the specs.

## Contents
- The web set
- Hero markup
- Alt text
- Privacy in image metadata
- Web image specs, with sources
- Generating ≠ publishing

## The web set

- **Filename = the slug** (the focus keyword), never a descriptive render name like `polished-mission-control-diorama.png`.
- `{slug}.webp` (full width) + `{slug}-400w.webp` / `-800w.webp` / `-1200w.webp`, or the widths the site uses. Pillow: `save("WEBP", quality=80–82, method=6)`; heroes land at a few dozen KB. `scripts/make_web_set.py` does the whole set.
- **AVIF** is optional: 25–50% smaller, broad support, but only add it if the site already serves it (via `<picture>` with AVIF first and the WebP `<img>` last). Don't introduce a new format in one post.
- **OG card** 1200×630, centre-cropped from the approved hero (1344×768 → 1.91:1 → 1200×630), text-free for the same reason as the hero. Never overwrite an existing hand-picked card.

## Hero markup

Copy the newest post's `<img>` (newest by `datePublished` — older posts often declare a different aspect ratio or lack `srcset`):

- `srcset` + `sizes`; real `width`/`height` matching the file (prevents layout shift);
- `fetchpriority="high"` and **never `loading="lazy"`** — the hero is the LCP image; lazy-load only below-the-fold images;
- `decoding="async"` is fine;
- both languages point at the same files.

## Alt text

- **Never omitted.** On a blog post: descriptive, **≥ 20 characters**, concrete ("Isometric model of a central hub routing work to five worker robots, one track looping back"), one per language.
- Never keyword-stuffed, never naming people, places or the owner.
- Outside a blog (a purely decorative image whose meaning is already in the heading) `alt=""` is correct — empty, still never missing, because a missing alt makes some screen readers read the filename.

## Privacy in image metadata

An alt, a `srcset` filename, an OG path and a JSON-LD `image` URL are all public, indexed text. The site's identity rules apply to them exactly as to the body:

| Identity mode | Rule for alt / filename / OG / prompt log |
|---------------|-------------------------------------------|
| `brand` | brand name only; no personal name; none of the banned terms |
| `pseudonym` | the pseudonym only; no real name, location, employer or other PII |
| `person` | the byline name may appear where the site uses it; never an address, street, phone, salary or client name |

Run the blog-pipeline banned-term gate over the new image paths and the post files before handing over. Strip EXIF/metadata from any photo you did not generate.

## Web image specs, with sources

| Item | Spec | Source |
|------|------|--------|
| OG / social card | at least **1200×630**, as close to **1.91:1** as possible, ≤ 8 MB (min 200×200; 600×315 for the large preview) | Meta, "Images in Link Shares": https://developers.facebook.com/docs/sharing/webmasters/images/ |
| WebP vs AVIF | WebP "widely supported"; AVIF "reasonably decent support", ">50% savings when compared to JPEG in some cases" | web.dev, "Image performance": https://web.dev/learn/performance/image-performance |
| `<picture>` fallback | "the browser picks the first `<source>` element specified that matches" — AVIF first, WebP `<img>` last | same web.dev page |
| LCP hero priority | `fetchpriority="high"` on the LCP image; a published case study cut LCP from 2.6 s to 1.9 s | web.dev, "Optimize resource loading with the Fetch Priority API": https://web.dev/articles/fetch-priority |
| Never lazy-load the hero | lazy-loading only below-the-fold images "results in a complete reversal of the LCP regression" | web.dev, "The performance effects of too much lazy-loading": https://web.dev/articles/lcp-lazy-loading |

## Generating ≠ publishing

Producing and wiring the image locally is not shipping it. For a framework-built site the production build + upload is the deploy; for a hand-built static site the upload is the deploy. Either way it is the blog-pipeline **ask-first** deploy gate. Show the result locally, hand over, and stop until the user says deploy. Then upload the image set and OG card **with** the post (an HTML-only deploy 404s the hero) and `curl -sI` the page and the `.webp` → 200.
