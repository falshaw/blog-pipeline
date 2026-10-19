# blog-pipeline — Claude Code skills for bilingual blog posts on static sites

Three [Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills) that take a blog post from "what should I write about?" to a verified, live, bilingual post on one or several static sites — with the human in charge of the two decisions that matter: **what** gets published and **when** it goes live.

| Skill | What it does |
|-------|--------------|
| [`blog-pipeline`](skills/blog-pipeline/SKILL.md) | Scout board → you pick → deepen → write primary + native secondary language → fact gate → SEO/discovery files → ask-first deploy → post-deploy checks |
| [`blog-images`](skills/blog-images/SKILL.md) | Post-grounded, text-free hero images via local ComfyUI + FLUX.1-schnell, randomised style per post, WebP set + OG card + alt text |
| [`stop-slop`](skills/stop-slop/SKILL.md) | Anti-AI-writing pass with a five-axis score, **including a German section** (fork of [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)) |

## What's different

- **Bilingual-native, not translated.** Each post is a primary article plus a twin written natively for the second audience — localised regulators, examples, date formats and idioms; same facts, sources and links. Primary/secondary languages are per site (default EN + DE; a site can be German-first).
- **You pick the topic.** No-topic runs end at a scout board: 3–5 candidates per site, each with the surprise, the beat fit, two named sources with the load-bearing number read on the source page, a catalogue-collision check and the take. Nothing is written until you choose.
- **Fact-check gate.** Every number, date, study, incident and quote gets a primary-source link in a claim table; a separate verifier agent confirms each against the fetched page; unconfirmed claims are cut. Plus six traps writers fall into (headline stronger than the source, misattributed venue, syndication mistaken for the original outlet, quote cut mid-phrase, relative time, thesis written as finding).
- **Anti-slop, in English and German.** Mandatory stop-slop pass on both languages, scored ≥ 35/50, with a guard that keeps punctuation edits from corrupting CSS.
- **Multi-site beats.** Each site has its own beat, identity mode (brand / person / pseudonym) and privacy rules. "A post for all my sites" means one distinct topic per site, never one story spread across domains.
- **SEO + GEO done properly for static sites.** Answer-first structure for AI answer engines, title/meta lengths, question H2s, reciprocal self-listing hreflang, BlogPosting + BreadcrumbList JSON-LD with a stable entity `@id`, sitemap without lastmod re-stamping, llms.txt, feeds, hubs, IndexNow, and a post-deploy registration + link check.
- **Local models optional.** Drafts and source digests can run on a local [Ollama](https://ollama.com) model to save tokens; heroes render on local ComfyUI + FLUX. Both are off by default; the pipeline works without them.
- **Ask-first, pluggable deploy.** Your deploy is a command in the config (FTP/FTPS, SFTP, rsync, GitHub Pages, anything). The pipeline shows the dry run and asks before it runs. A generic FTPS script is included: credentials from environment variables only, hash-diff uploads, atomic renames, server-only files protected.

## Install

```bash
# from your project root
mkdir -p .claude/skills
cp -r path/to/blog-pipeline/skills/* .claude/skills/
# or for every project: cp -r path/to/blog-pipeline/skills/* ~/.claude/skills/
```

Then configure:

```bash
mkdir -p .claude/blog-pipeline
cp .claude/skills/blog-pipeline/config/sites.example.yaml   .claude/blog-pipeline/sites.yaml
cp .claude/skills/blog-pipeline/config/banned-terms.example.txt .claude/blog-pipeline/banned-terms.local.txt
```

Edit `sites.yaml` — one entry per site: domain, beat, identity, languages, source tree, post paths, image paths, discovery files, deploy command. Keep `banned-terms.local.txt` and any `.env.*` files out of version control (see [.gitignore](.gitignore)).

Start a run in Claude Code: *"write a blog post for example.com"* or *"scout topics for all my sites"*.

## Config at a glance

```yaml
sites:
  - id: example-ai
    domain: example.com
    identity: { mode: brand, entity_jsonld: '{"@type":"Organization","@id":"https://example.com/about#organization",...}' }
    beat: { summary: ..., belongs_when: ..., never: [...] }
    languages: { primary: en, secondary: de }
    source_tree: sites/example-ai
    post: { paths: { primary: "blog/{slug}/index.html", secondary: "de/blog/{slug}/index.html" } }
    discovery: { sitemap: sitemap.xml, llms: [llms.txt], feeds: [...], hubs: [...] }
    deploy: { method: ftp, command: "...", dry_run: "...", detached: true }
```

Full annotated example with two fictional sites: [skills/blog-pipeline/config/sites.example.yaml](skills/blog-pipeline/config/sites.example.yaml).

## Requirements

| Need | For |
|------|-----|
| Claude Code with web search/fetch | everything |
| A static site tree on disk (hand-built HTML or an SSG output) | writing posts |
| `grep`, `curl` | gates and live verification |
| Python 3.9+ | `ftp-deploy.py`, `indexnow-ping.py`, `comfy_generate.py` (stdlib only) |
| Pillow | `make_web_set.py` (WebP set + OG card) |
| Node.js 18+ and Ollama | optional local drafting (`local-llm.mjs`) |
| ComfyUI + a FLUX.1-schnell checkpoint, a GPU (8 GB works, slowly) | optional local images |
| [`last30days`](https://github.com/mvanhorn/last30days-skill) skill | optional community-reaction pass |

## Layout

```
skills/
  blog-pipeline/   SKILL.md · config/ · references/ (scouting, writing, fact-gate, static-site-mechanics,
                   deploy-gates, geo-2026, local-llm, last30days, lessons) · scripts/ (local-llm.mjs,
                   prompts/no-slop-writer.md, ftp-deploy.py, indexnow-ping.py)
  blog-images/     SKILL.md · references/ (prompt-recipes, engine-notes, delivery) · scripts/ (comfy_generate.py, make_web_set.py)
  stop-slop/       SKILL.md · LICENSE (upstream MIT) · NOTICE.md (fork changes) · references/
```

Scripts live inside the skill folders so the skills stay self-contained after you copy them into `.claude/skills/`.

## Licence and credits

MIT — see [LICENSE](LICENSE). Created by Nick Falshaw.

`skills/stop-slop/` is a fork of [stop-slop](https://github.com/hardikpandya/stop-slop) by Hardik Pandya (MIT, original licence kept in [skills/stop-slop/LICENSE](skills/stop-slop/LICENSE)), with additional patterns from [no-ai-slop](https://github.com/petergyang/no-ai-slop) by Peter Yang (MIT). The fork's changes, including the German section, are listed in [skills/stop-slop/NOTICE.md](skills/stop-slop/NOTICE.md). FLUX.1-schnell is by Black Forest Labs (Apache-2.0); ComfyUI and Ollama are separate projects under their own licences.
