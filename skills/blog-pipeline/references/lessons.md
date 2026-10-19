# Why the gates exist — failure patterns behind each rule

Every rule in this skill exists because the failure it prevents is easy to make and expensive to undo. Read this when a rule looks like overkill.

| Rule | Failure it prevents |
|------|--------------------|
| **The user picks the topic** | A "fully automated, never ask" run wrote, imaged, audited and deployed several articles on topics the owner never chose. The owner found out what was being published by asking mid-run. Automation between the two stops is fine; choosing *what* goes public is not the agent's call. |
| **One distinct topic per site** | "A post for all sites" read as one story angled N ways produced near-duplicate content across domains that compete with each other in search. |
| **Collision check on the candidate's own terms** | A grep built from other topics' keywords missed an existing post on the same intent (different wording, other language stem), so a near-duplicate reached the board as "Clean: none". |
| **Privacy at pick time** | A location-tied case study almost published a location that was banned for safety reasons. A topic that needs a banned term is disqualified before writing, not scrubbed after. |
| **Banned terms kept out of skill files** | The literal list (home town, entity names, registration numbers) is itself sensitive. It lives in a local-only file and never in a repo, a prompt log or a public skill. |
| **Read the number on the source page** | A scout board led on two growth percentages taken from a search summary; neither existed in the cited source, so the picked post had to change angle after the pick. |
| **Fact gate with a separate verifier** | A citation audit found dozens of factual errors across a set of live posts: guides written from model memory (wrong model sizes, wrong price ratios, cost tables off by 2–4×) and news posts copying coverage instead of the source (a network total credited to one member, two papers merged into one). The "verify against two sources" instruction already existed and did not stop them. |
| **CSS-integrity gate** | An em-dash / punctuation sweep collapsed `,.` → `.` across a site and invalidated every `rgba()` colour — the whole design broke silently. The first version of the gate used `\d` with `grep -E`, matched nothing and passed on broken CSS for months. |
| **OG-card gate** | Several of the newest posts on a site shipped with `og:image` pointing at files that did not exist (404 social cards). Separately, an unconditional card generator overwrote every hand-picked card locally and was only caught before deploy. |
| **Entity `@id` from the config** | Post pairs copied from an older template shipped author/publisher blocks without `@id`, unlinked from the site entity. |
| **JSON-LD URL = canonical** | Several secondary-language posts carried an umlaut variant of their ASCII slug in `mainEntityOfPage` and the breadcrumb. Canonical, `og:url` and hreflang were correct, so no other check caught the 404 URLs. |
| **Never re-stamp lastmod** | One deploy flattened almost every `<lastmod>` in a sitemap to the deploy date; crawlers stop trusting lastmod after that. |
| **Copy the newest post, not an old one** | A post built from a stale template shipped a 404 footer link and three redirecting CTAs; another pair was never added to the sitemap, llms file or hubs and sat off the discovery path for months. |
| **Registration + link gate after exit** | Checking discovery files while a long upload was still running reported false failures — sitemaps and llms files upload last. |
| **Feeds verified** | A post went live without its feed item because the feed was generated and nobody ran the generator. Feeds on another site sat frozen for months, dozens of posts behind. |
| **Detached long deploys** | A foreground deploy hit the tool timeout and was killed mid-upload: primary post live, hero 404, twin missing — on a public site — until a re-run finished. |
| **One FTP session per hosting account** | Two sites' deploys overlapped on one shared account with a connection cap. Both happened to finish clean; that was luck, not evidence. |
| **"No dry-run" said out loud** | A deploy script that read no arguments silently ignored `--dry-run` and deployed for real. Check that a flag is parsed before relying on it. |
| **No vulnerability IDs in prose** | Identifier-led posts read as patch-news recaps, date fast and attract the wrong audience. An incident can carry a take; describe it instead. |
| **Search-led guides first** | On one evergreen site, practical guides earned roughly 30× the clicks and 40× the impressions of opinion posts over the same 90 days. |
| **Post-deploy SEO audit, unasked** | Skipping it let small on-page misses (a 63-character title, a 138-character meta description, a missing `Updated` line in an llms file) sit live until the next audit. |
| **Native secondary language** | Machine-translated twins read stiff to native readers and match Google's description of scaled content abuse. |
