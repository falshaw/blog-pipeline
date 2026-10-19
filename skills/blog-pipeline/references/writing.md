# Writing — bilingual-native posts, answer-first GEO, SEO floor

## Contents
- The #1 rule: the expert's take, not the source
- Bilingual, not translated
- Answer-first GEO structure
- SEO floor (checked in both languages)
- Worked example: one distinct topic per site

## The #1 rule: the expert's take, not the source

The topic, news item or search query is the **seed, not the script**. A post that reads like a news recap or a bullet-list rewrite of its source fails. Write the site's **opinionated, from-experience** view: what actually works, why it fails in practice, the trade-offs, the contrarian read. Lead with a real insight, never "In this article we will explore". No prompt-restating, no marketing fluff.

Use a headline formula, an [Action] + [What-they-get] CTA, and vary section shapes (prose, a table, a short checklist where it earns its place).

## Bilingual, not translated

Search engines treat unedited machine translation as low value: Google's spam policy lists "automated transformations like synonymizing, translating, or other obfuscation techniques, where little value is provided to users" as scaled content abuse (Google Search Central, "Spam policies for Google web search"). Readers notice faster than crawlers.

- **Write the twin from the facts and the argument, not from the sentences.** Same claims, same numbers, same sources, same links; free structure, idiom and examples.
- **Localise what differs:** regulators and agencies (name the national body the reader deals with), legal terms, date and number formats (`3. Juni 2026`, `1.500` in German), units, currency, examples the audience recognises.
- **Keep terms of art** the audience uses in that language (Prompt Injection, Zero Trust) and translate common words (Veröffentlichung, not Disclosure). The stop-slop German section covers Denglisch overload.
- **Slug, title, meta, alt, headings and breadcrumbs** are written in the twin's language. URL language = body language.
- **Quotes:** keep the original-language quote and add a translation in the body language, or paraphrase without quote marks. Never put your translation in quote marks as if the speaker said it.
- **Quality gate:** a fluent reader of the secondary language (the user, or a separate review pass) must find it natural. Machine-stiff text does not ship.

## Answer-first GEO structure

AI answer engines (Google AI Overviews / AI Mode, ChatGPT Search, Perplexity, Gemini, Claude) retrieve at the **passage level** and weight a page's opening heavily — roughly the first 30% of a document supplies ~44% of citations (2026 retrieval research, directional). GEO is strong classic SEO applied to an AI surface. Evidence and sources → [geo-2026.md](geo-2026.md).

- **Answer-first, in self-contained chunks.** Open the post AND every H2/H3 with a **40–75 word direct answer** before any context; the first ~200 words must completely answer the query. Write each section as a **self-contained 120–180 word chunk** with **explicit entities** (name the subject; don't lean on "it" / "this" / "the above").
- **Information gain.** Add knowledge not already in the top results — first-hand experience, a proprietary number, a framework, a contrarian read. Scaled, unedited, commodity AI copy is what recent spam and core updates hit.
- **Citation levers:** statistics with a named source, cited named sources, a quotation from an authority. Include **≥1 comparison/spec table** and **1–2 hard stats with a named source** above the fold.
- **Entity:** name the brand or author consistently; strengthen the author/brand entity. A `person` site can lean on named-author E-E-A-T (Person `@id` + `sameAs`); `brand` and `pseudonym` sites win on information gain and quality instead.
- **Freshness:** visible date + accurate `dateModified`. **Never bump `dateModified` cosmetically** — crawlers compare snapshots. Refresh a cornerstone post's substance on its existing URL instead of spawning a near-duplicate.
- **Schema:** BlogPosting + BreadcrumbList always; FAQPage where it fits (Google still parses it, but the FAQ rich result is gone — never sell it as one). Schema is identity hygiene, not a citation lever.
- **Crawlers:** keep AI *search* crawlers allowed (Googlebot, OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User, PerplexityBot). Blocking *training* crawlers costs no citations. Check your CDN's default AI-bot blocking.
- **llms.txt** is not a ranking or citation lever. Keep it current because it is cheap; don't spend real effort on it.

## SEO floor (checked in both languages)

Values come from `defaults.seo` in the config; the defaults are:

- **Title** 50–60 characters (Google truncates past ~60), focus keyword near the start, unique. Measure the `<title>` / `og:title` / `twitter:title` string itself; the H1 may run longer.
- **Meta description** 140–160 characters measured as **decoded glyphs** (an HTML entity counts as 1, not 6 — decode first).
- **Phrase 1–2 H2s as the literal question a searcher types** ("How long does a firewall migration take?").
- **Visible dates in `<time>`:** published always; when `dateModified` > `datePublished`, also an "Updated" / „Aktualisiert am“ line. BlogPosting carries `inLanguage`.
- **One `<h1>`**, clean heading hierarchy.
- **Canonical** self-referencing. **OG + Twitter per page** (`og:url` == canonical, `og:title` == title, `og:description` == meta) — template inheritance is the classic silent failure; verify, don't assume.
- **hreflang** primary + secondary + `x-default`, **reciprocal**, each page listing **itself** too. Codes are ISO 639-1 (`en`, `de`) with an optional region, never a region alone. One method per site (HTML `<link>`, HTTP header or sitemap). "If two pages don't both point to each other, the tags will be ignored" (Google Search Central, "Tell Google about localized versions of your page").
- **OG card** ≥ 1200×630, close to 1.91:1, ≤ 8 MB (Meta, "Images in Link Shares").
- **BlogPosting JSON-LD** valid, dates consistent with the visible date, author + publisher = the config's `entity_jsonld`. **Hero alt** ≥ 20 characters. **≥ 600 words** (target 1,500–2,500). **≥ 3 internal links** (aim 5–7), all resolving. **≥ 1 table.**
- Close with "Related reading" / „Weiterführende Lektüre“ linking existing posts in the same language.

## Worked example: one distinct topic per site

Three sites, three beats, one run — each topic hung on a primary source no roundup carried:

- **AI site** → *A crypto exchange opened live trading to AI agents with no cap on losses* (the funded sub-account balance as the only limit), set against a custody firm shipping agent accounts with identity, spending limits and remote pause. Load-bearing material: one line from an exchange executive in a trade-press interview — "We really cannot see the reasoning of what the user's action is." Slugs `ai-agents-with-money-spending-limits` / `ki-agenten-mit-geld-ausgabenlimits`.
- **Infrastructure-change site** → a search-led guide: *how to run a firewall change-management process an auditor accepts*, built on the query cluster with ~1,200 impressions and zero clicks at positions 11–18.
- **Field-notes site** → *Shadow AI: two thirds of staff use unapproved AI tools and most of those paste work data in* — the take: most companies already have a policy, so this is a speed gap, not a policy gap.

Three topics, three beats, no overlap — and the user chose each from the board.
