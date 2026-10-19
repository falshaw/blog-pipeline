# Static-site mechanics — what a post touches

Paths come from the site config (`post.paths`, `images`, `discovery`). This file says what goes in them.

## Contents
- A post = two files + discovery updates
- `<head>` checklist
- JSON-LD blocks
- hreflang
- Hero image markup
- Discovery files
- Framework-built sites (SSG / static export)
- Pre-ship checklist

## A post = two files + discovery updates

- **Primary** at `post.paths.primary`, **secondary** at `post.paths.secondary`, made by **copying the STRUCTURE of the newest post** by `datePublished` (not alphabetical, not the first one you find) and replacing the content. Old posts carry stale footers, lazy-loaded heroes, missing `srcset` and outdated stylesheet versions.
- **Never invent CSS** or pull in a new framework, font or CDN for one post. Use the live classes; keep the live `<head>` stylesheet links exactly, including the cache-busting `?v=` the newest post uses.
- After copying, **replace the author/publisher JSON-LD with the literal block from the config**. Never trust what the copied post carries.
- Body text may use UTF-8 literals (typographic apostrophes, umlauts). Escape only `&` → `&amp;` and literal `<` / `>` in HTML.
- **5–7 internal links** to existing posts in the same language (verify each target file exists), **2–3 external authority links** (official docs, regulators, vendor advisories, papers), end CTA from `post.cta`.
- **Category** from the live set only — derive it from existing posts (`grep -hoE 'post-kicker[^>]*>[^<]+'` or your theme's equivalent), never invent one. The twin uses the category's name in its own language.
- Length ~1,500–2,000 words unless the site sets otherwise.
- The secondary twin: `<html lang>` set, its own title/meta/OG, `inLanguage`, localised breadcrumb and nav, localised date format in the byline (`3. Juni 2026 · 8 Min. Lesezeit`).

## `<head>` checklist

`<html lang>` · `<title>` (≤ 60 chars) · `<meta name="description">` · `<link rel="canonical">` (self) · `og:type/title/description/url/image` (+ `og:image:width/height` 1200/630) · `twitter:card/title/description/image` · hreflang set · stylesheet links exactly as the newest post · BlogPosting JSON-LD · BreadcrumbList JSON-LD · no analytics block unless the site already has consent handling.

## JSON-LD blocks

```html
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BlogPosting",
 "headline":"…","description":"…",
 "datePublished":"YYYY-MM-DD","dateModified":"YYYY-MM-DD",
 "inLanguage":"en","articleSection":"Guides",
 "mainEntityOfPage":"https://example.com/blog/{slug}/",
 "image":"https://example.com/og/{slug}.jpg",
 "author": <identity.entity_jsonld>,
 "publisher": <identity.entity_jsonld>}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {"@type":"ListItem","position":1,"name":"Home","item":"https://example.com/"},
 {"@type":"ListItem","position":2,"name":"Blog","item":"https://example.com/blog/"},
 {"@type":"ListItem","position":3,"name":"…","item":"https://example.com/blog/{slug}/"}]}
</script>
```

- The `@id` inside `entity_jsonld` is mandatory — without it every post ships unlinked from the site entity.
- `mainEntityOfPage` and the last breadcrumb `item` = the canonical, byte for byte.
- `brand` / `pseudonym` sites: never a `Person` node, never a real name.
- FAQPage only with real questions the post answers; it aids comprehension but no longer earns a rich result.

## hreflang

```html
<link rel="alternate" hreflang="en" href="https://example.com/blog/{slug}/" />
<link rel="alternate" hreflang="de" href="https://example.com/de/blog/{slug-de}/" />
<link rel="alternate" hreflang="x-default" href="https://example.com/blog/{slug}/" />
```
The identical set goes on BOTH pages (each lists itself and its twin). `x-default` points at the primary-language page unless the site says otherwise. Add a visible language switch link to the twin.

## Hero image markup

Copy the newest post's `<img>` and change only the values:

```html
<img decoding="async" fetchpriority="high"
     src="/images/{slug}.webp"
     srcset="/images/{slug}-400w.webp 400w, /images/{slug}-800w.webp 800w, /images/{slug}-1200w.webp 1200w"
     sizes="(max-width: 780px) 100vw, 760px"
     width="1344" height="768"
     alt="…descriptive, ≥ 20 characters, in this page's language…" />
```

- The hero is the **LCP element**: `fetchpriority="high"`, **never `loading="lazy"`** (lazy-loading the LCP costs ~200–400 ms). Lazy-load only below-the-fold images.
- `width`/`height` = the real file's dimensions (prevents layout shift). Check the newest post before generating — a stale aspect ratio means re-rendering the whole set.
- Both languages share the image files; each has its own alt text.
- Make sure the stylesheet sets `height: auto` on content images, or a 16:9 hero gets squashed on phones.

## Discovery files

| File | What to do |
|------|------------|
| `sitemap.xml` | Add one `<url>` per language. `lastmod` = the post's `dateModified`. Match existing priority/changefreq conventions. Touch only the new entries plus hubs whose listing changed. Never re-stamp other entries. |
| `llms.txt` / `llms-full.txt` | Usually hand-maintained even on generated sites. Add the primary entry under the primary-language section and the twin under the secondary one, matching existing order. Keep exactly one heading per section. Update any `Updated: YYYY-MM-DD` line. |
| Feeds (`feed.xml`, per language) | If `generator` is set, run it — never hand-edit a generated feed — and ship the result. If `null`, add an `<item>` by hand matching the existing items (guid = permalink). Verify the new slug is in each feed. |
| Hub pages | Add a newest-first card to every hub in `discovery.hubs`, matching existing card markup exactly. If the homepage is the only listing, bump its `lastmod`. |
| `robots.txt` | Not touched by a post. If your deploy uploads robots.txt from somewhere other than the source tree, note it in the config so nobody edits the wrong copy. |

## Framework-built sites (SSG / static export)

For a site built by Next.js static export, Astro, Hugo, Eleventy and similar:

- A post usually means: a metadata entry (slug, title, description, dates, keywords, category), a content file or component per language, and a slug map that drives hreflang and the sitemap. Find all of them by grepping the newest post's slug across the source tree before writing.
- Generated files (sitemap, feeds, llms-full) update on build — but check each one; a hand-kept `llms.txt` next to generated files is common and silently falls behind.
- Per-post OG cards are often a separate script, not part of the build. Run it before the build, and only for missing cards.
- **The build is part of the deploy.** Run typecheck/lint freely, but the production build that produces the uploaded artefact happens after the user's yes.
- In metadata files use real UTF-8 characters for the secondary language (`für`, not `fuer`).

## Pre-ship checklist

- [ ] both post files exist, one `<h1>` each, canonical + OG + Twitter match the page
- [ ] hreflang identical on both, reciprocal, self-listed, `x-default` present
- [ ] JSON-LD valid; entity block from the config; URLs = canonical; ASCII slugs
- [ ] hero set + OG card exist at the configured paths; alt ≥ 20 chars per language
- [ ] sitemap, llms, feeds, hubs updated for both languages
- [ ] internal links resolve locally; the page renders locally (open it, screenshot it)
- [ ] all pre-deploy gates in [deploy-gates.md](deploy-gates.md) pass
