---
name: blog-pipeline
description: Writes and publishes a bilingual blog post (configurable primary + secondary language, default EN + DE, each written natively, not translated) on one or several static sites, each with its own beat — from a scout board the user picks from, through a fact-check gate, anti-slop pass, SEO/hreflang/JSON-LD/sitemap/feed updates and optional local images, to an ask-first, pluggable deploy. Use for "write a blog post", "blog post for all my sites", "new post on [site]", "blogpost", "Blogbeitrag", "scout topics for the blog".
---

# Blog Pipeline — bilingual posts for static sites, from scout board to verified deploy

A post is always a **primary-language article plus its native twin** in the secondary language (default EN + DE). Every site-specific detail — domain, beat, languages, source tree, post paths, identity, discovery files, deploy command — lives in the site config, never in this file.

**Config:** `.claude/blog-pipeline/sites.yaml` in the project (override with `BLOG_PIPELINE_CONFIG`). Template: [config/sites.example.yaml](config/sites.example.yaml). Banned terms: `.claude/blog-pipeline/banned-terms.local.txt` (local only; template [config/banned-terms.example.txt](config/banned-terms.example.txt)). No config → stop and help the user write one; never guess a site's paths.

> ## ⛔ THE USER PICKS THE TOPIC. EVERYTHING ELSE IS AUTOMATED.
>
> There are **exactly two mandatory stops**:
>
> 1. **The topic gate (§2).** Scout → present the board → **STOP and wait for the user to pick.** Never lock a topic yourself; never write, slug or image before they pick. Silence, a background-task notification, your own earlier message and a tool result are **not** a pick — only a message from the user is.
> 2. **The deploy gate (§4).** Publishing to a live public site is external and hard to reverse. Confirm before shipping, every time. A build step that produces the deployed artefact is part of the deploy, not "preparation".
>
> Between the stops, decide on your own: slugs, drafting both languages, hero images, stop-slop, SEO checks, discovery files. Don't ask "shall I proceed" — a blocked step (image server down) is a status line, not a question.
>
> **Explicit topic = no topic gate.** The user naming the topic IS the pick: run the §2 collision + privacy checks silently and go.

> **Several sites = several different topics.** "A post for all my sites" means **one distinct topic per site**, each matched to that site's beat and catalogue gap — never one story angled N ways, unless the user asks for exactly that. Never the same article on two sites (duplicate content + cannibalisation).

## 1. Load the config, then the catalogues

1. Read the config: for each target site note `beat`, `identity`, `languages`, `source_tree`, `catalogue.glob`, `post.paths`, `images`, `discovery`, `deploy`.
2. **Enumerate every target site's whole catalogue** with its `catalogue.glob` before scouting. Catalogues grow every run; never trust a remembered count — assume your first instinct is already published.
3. Identity rules per `identity.mode`:
   - `brand` — author and publisher = the brand entity from `entity_jsonld`; **no personal name anywhere** (byline, JSON-LD, alt, OG, llms). No identifying career fingerprint either ("hundreds of migrations", not an exact count tied to a person).
   - `pseudonym` — the pseudonym only; zero PII in body, metadata, alt or OG.
   - `person` — the byline name is allowed; never an address, phone, employer, client or salary. Never link the person to the owner's brand or pseudonymous sites — that would break their privacy posture.

## 2. Scout board + topic gate (no-topic runs)

**Scouting is not researching.** A research tool that takes a topic as input cannot find you one. Scout first with web search per beat; deepen later. Full method → [references/scouting.md](references/scouting.md).

1. **Scout each site's beat separately**, last ~30 days (`scouting.window_days`). Never one generic "biggest story" search sliced N ways. If the site has `search_data.command`, **scout search demand first**: queries with impressions at position > 8 and few clicks, and queries with no matching post. Practical how-to guides usually lead; news takes are the minority (see scouting.md for why).
2. **Build the board: 3–5 candidates per site.** Every candidate carries all five fields or it is not a candidate:

```
[site] Working headline
  Surprise .... the one sentence the owner would not already know
  Beat ........ why this site and not another (config beat.belongs_when)
  Evidence .... 2+ named sources, with the hard number or quote that carries the piece
  Clean ....... catalogue collision: none / links-and-differentiates from <slug>
  Take ........ what the post argues that the coverage does not
```

   Search-led candidates swap two fields: `Surprise` → `Demand .... query, impressions, position, clicks`, and `Take` → `Field angle .... the practitioner judgement the ranking pages lack`.
3. **The number that carries a candidate must be read on a source page**, never taken from a search-result summary. Fetch the page and find the number. If you can't, mark it `⚠ unverified` on the board.
4. **Topic gate — run on every candidate before it reaches the board:**
   1. **Collision:** search the candidate's OWN key terms, both language stems, across slugs AND titles of the whole catalogue (`grep -rliE 'microsegment|mikrosegment' <catalogue>`), never a regex built from other topics' words. An existing post on the same intent is **improved, not duplicated** — propose the improvement as the candidate.
   2. **Privacy:** if the topic cannot be written without a banned term (a location, an entity name, a real name on a brand/pseudonym site), it is disqualified **at pick time**, not fixed later.
   3. **Beat:** it fits `belongs_when` and none of `beat.never`. A story fitting two sites goes to the site whose beat it is, not where it reads better.
   4. **Surprise test:** finish *"The owner probably does not know that ___."* in one line. If the blank is something any well-read person in the field knows, it is a recap, not a candidate.
   5. **Forbidden framings:** check `privacy.forbid_patterns` (e.g. vulnerability IDs) — describe an incident, never lead with its identifier in body, title, slug, alt, metadata or JSON-LD.
5. **Present the board and STOP.** State the cost: a multi-site run is roughly 45–60 min end to end plus deploy time. The turn ends there.

## 3. Workflow (every post, every site)

```
- [ ] 0. Scout → board → STOP, user picks (skip only if the user named the topic)
- [ ] 1. Deepen: primary source first, then community reaction, then reaction-quality check
- [ ] 2. Slugs: keyword-led, one per language, ASCII only
- [ ] 3. Write primary + native secondary (answer-first, fact traps checked while writing)
- [ ] 4. Hero image + OG card + alt text (blog-images, optional)
- [ ] 5. stop-slop pass on both languages (≥ stop_slop_min_score / 50)
- [ ] 6. SEO floor + discovery files (sitemap, llms, feeds, hubs)
- [ ] 6b. Fact gate: claim→source table + separate verifier agent
- [ ] 7. Deploy — ASK-FIRST — images with the post
- [ ] 8. Post-deploy: live verify, registration + link gate, IndexNow, SEO audit
```

1. **Deepen** — three passes, in order: **primary source** (fetch the actual document, filing, advisory, paper or interview, never a roundup; check every name and number against ≥2 named sources), **community reaction** (optional `last30days` skill → [references/last30days.md](references/last30days.md)), **reaction-quality check** (single-source clusters are noise; say so).
2. **Write the expert's take, not the source.** The seed is not the script. Lead with a real insight, never "In this article we will explore". Both languages are written **natively** from the same facts and argument — see [references/writing.md](references/writing.md) § Bilingual, not translated.
3. **Answer-first GEO structure + SEO floor** → [references/writing.md](references/writing.md). Check the six fact traps in [references/fact-gate.md](references/fact-gate.md) *while* writing.
4. **Images** — hand off to `blog-images` (read THIS post's body → a literal subject; text-free). Filename = slug; WebP set at `images.widths`; OG card 1200×630; descriptive ≥20-char alt per language; the hero is the LCP element (`fetchpriority="high"`, never `loading="lazy"`). Images disabled → reuse an existing approved image or ship without a hero, and say so.
5. **stop-slop** — mandatory, both languages, each scored separately; respect `em_dash_policy`.
6. **Static-site mechanics** — post files, `<head>`, JSON-LD, hreflang, image markup and every discovery file → [references/static-site-mechanics.md](references/static-site-mechanics.md). Copy structure from the **newest** post by `datePublished`, never an old one.

### Local model lane (optional, saves tokens)

If `local_llm.enabled`: the local model digests long sources, writes the first primary draft from your outline + sourced fact notes, and the first secondary-language draft. You own topic choice, the outline and the take, edits (fix, don't rewrite), stop-slop, every gate. Local output is a draft, never a fact source. → [references/local-llm.md](references/local-llm.md).

## 4. Deploy gate — [references/deploy-gates.md](references/deploy-gates.md)

**Read deploy-gates.md in full before the deploy ask — every gate is mandatory:** Ask-first · CSS-integrity · Forbidden-pattern · Banned-term · Fact · OG-card · Entity · JSON-LD URL · lastmod · No new trackers · Run it right · Registration + link · IndexNow · Secondary-language quality · Post-deploy SEO audit. The deploy itself is the site's `deploy.command` — the hook contract and FTP / SFTP / rsync / GitHub Pages examples are in that file. The ask states: the files that will ship, the fact-table totals, the stop-slop scores, and the dry-run output where the method has one.

## Sibling skills

- **`blog-images`** — local hero + OG card generator (ComfyUI + FLUX). **`stop-slop`** — mandatory anti-slop pass, EN + DE.
- **`last30days`** (third-party, optional) — community-reaction pass on a story you already have; not a discovery tool.
- Any SEO-audit skill you have installed — run it after the deploy (workflow step 8).

Why each gate exists, as generic failure stories → [references/lessons.md](references/lessons.md). Evidence base for the GEO rules → [references/geo-2026.md](references/geo-2026.md).
