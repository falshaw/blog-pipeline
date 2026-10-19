# Scouting — finding topics worth a post

The rules live in `SKILL.md` §2. This file is the method: sources per beat type, search-demand scouting, the deepen passes, and why the filters exist.

## Contents
- Scouting vs researching
- Sources and query shapes per beat type
- Search-demand-first scouting
- The surprise test and the take
- Banned framings (defaults you can override per site)
- Deepen passes (after the pick)
- Cost to state on the board

## Scouting vs researching

Scouting finds candidates; research deepens a story you already have. Tools that take a topic as input (community-reaction tools, deep-research agents) cannot find a topic — feeding them a vague one returns a generic month summary. Scout with plain web search per beat, then deepen the picked story.

## Sources and query shapes per beat type

Build a table like this for each site in your config and keep it next to the config (`.claude/blog-pipeline/scouting-sources.md`). Typical shapes:

| Beat type | Scout these | Query shapes that work |
|-----------|-------------|------------------------|
| **AI / ML engineering** | HN front-page velocity, r/LocalLLaMA · r/MachineLearning · r/OpenAI · r/ClaudeAI, lab and vendor announcements, AI-policy trackers, tech press AI sections | "AI \<month\> controversy/backlash", "\<vendor\> launched agents that …", "regulator + AI", "AI money/valuation/stake" |
| **Infrastructure / network change** | Search data first (below). Then vendor strategy news (M&A, platform moves, end-of-life deadlines), management-tooling vendors, outage post-mortems, regulatory **change-evidence** angles, r/networking · r/sysadmin | "\<vendor\> acquisition/platform \<month\>", "outage caused by config change", "\<product\> end of life migration deadline", "AI rule management" |
| **Consultant / contractor field notes** | National trade press, freelancer-market reports and rate surveys, consulting-industry disruption, contractor-status politics, compliance-enforcement reality, enterprise-transformation studies | "IT freelancer market \<year\>", "consulting AI disruption insourcing", "\<regulation\> implementation status", "enterprise AI pilots fail \<study\>" — always through the consultant's lens |

For a German-language site, scout German sources too (trade press, the national security agency, industry associations) — a German-first post built only from English coverage reads imported.

## Search-demand-first scouting

On an evergreen niche site, people search for the problem in front of them, not for a take on this month's news. One site's 90-day Search Console data, as an illustration: about a hundred practical guides (migration plans, audit checklists, process guides) drew ~218 clicks and ~25,500 impressions; about thirty opinion posts on recent news drew 7 clicks and ~585 impressions. That pattern is common enough to make it the default:

- **Source of candidates:** the site's `search_data.command` (any script that prints Search Console or Bing Webmaster queries as JSON). Look for queries with impressions at position > 8 and few clicks (page-2 opportunities), clusters with many impressions and zero clicks, and queries with no matching post.
- **Format:** a practical, evergreen guide — plans, process steps, checklists, comparisons, templates — written for **whoever owns the problem** (the lead or manager facing the migration or audit), with practitioner judgement in it. It answers the query in the first paragraph.
- **Mix:** about 3 of 4 posts search-led guides; news takes are the minority. A news hook may open a guide.
- **An existing post that already targets the query is improved, not duplicated** (better title/meta, answer-first intro, missing sections). Propose that as the candidate.
- No search data yet (new or small site): use the problem the reader has, phrased as they would search it.

## The surprise test and the take

For the news-take minority, a candidate must pass the **surprise test**: finish *"The owner probably does not know that ___."* in one line. Someone with decades in the field already knows "there was a critical flaw in a popular product". They may not know "a government agency cut the patch deadline to three days and named AI-accelerated exploitation as the reason".

**Wanted:** real, surprising news on power, money, trust or geopolitics, written as a **sharp opinionated take**, not a recap or checklist. Evergreen contrarian takes are welcome. The enemy is the recap treatment, not newsworthiness.

## Banned framings (defaults you can override per site)

- **Vulnerability-of-the-month recaps** and identifier-led stories. An incident may carry a take; describe it ("the hypervisor flaw exploited five days after disclosure"), never lead with or print its ID. Enforce with `privacy.forbid_patterns`.
- **Patch / hardening guides on a site whose beat is something else** (e.g. a change-management site is about *changing* systems well, not patching them).
- **Percentage-stat bait** ("36.7% of servers are vulnerable to X") with no take.
- **Generic workplace or survey news** on a field-notes site — the candidate must land on the life or judgement of the person in that seat, not on "workers in general".
- **Breach stories on a non-breach beat** earn one supporting sentence inside an on-beat story at most.
- **The owner's own products or projects** on a personal field-notes site.

## Deepen passes (after the pick)

1. **Primary-source pass, FIRST.** Fetch the actual document, advisory, filing, release or interview — never a roundup *about* it. That is where the load-bearing material lives: the exact clause, the number, the quote nobody else pulled. A whole post can hang on one sentence from a primary interview that no roundup carried. **Verify every specific name and number against ≥2 named sources** — a single summary confabulates both.
2. **Engagement pass** (optional, e.g. the `last30days` skill): for the community *reaction*, not the story — the contrarian read, the real pain point, the quotable practitioner take with a named handle. Not a discovery tool. → [last30days.md](last30days.md)
3. **Reaction-quality check.** Every cluster tagged single-source is noise, not reaction: the story has not landed, or a source is down. Say so rather than quoting a two-like post as a groundswell.

## Cost to state on the board

So the pick is informed: a full multi-site run is roughly 45–60 min end to end; each deploy adds its own time (measure yours once and note it in the config comments). Deploys that can exceed your tool's foreground timeout always run detached.
