# Deploy gates — read in full before every deploy ask

Every gate is mandatory. Pre-deploy gates run on the files you are about to ship; post-deploy gates run only after the deploy task has **exited**.

## Contents
- Gate table
- Gate details (commands)
- The deploy hook contract
- Deploy method examples (FTP/FTPS, SFTP, rsync, GitHub Pages, custom)
- Post-deploy

## Gate table

| Gate | Pass condition |
|------|----------------|
| **Ask-first** | The user's explicit yes to THIS deploy. A build that produces the shipped artefact counts as part of the deploy. |
| CSS-integrity (pre) | comma-stripped `rgba()` count = **0** in shipped files; after deploy, 0 live |
| Forbidden-pattern (pre) | every `privacy.forbid_patterns` regex = **0** over the new/edited post files |
| Banned-term (pre) | every line of the banned-terms file = **0** over the new/edited files (site-scoped lines included) |
| Fact (pre) | claim table, **0 unlinked rows**, separate verifier agent, totals in the ask → [fact-gate.md](fact-gate.md) |
| OG-card (pre + post) | every `og:image` / `twitter:image` file exists in the shipped tree; 200 live; never overwrite a hand-picked card |
| Entity | author AND publisher = the config's `entity_jsonld`, copied from the config, never from an older post |
| JSON-LD URL | `mainEntityOfPage` and the last BreadcrumbList `item` equal the canonical byte for byte; ASCII-only URLs |
| lastmod | new sitemap entries get the post's `dateModified`; **never re-stamp** existing `<lastmod>` values |
| No new trackers | no analytics or third-party script added by a post unless the site already has a consent setup for it |
| Run it right | detached for long deploys; one session per hosting account; images WITH the post |
| Registration + link (post) | both languages in live sitemap, llms files, feeds, hubs; every internal `href` = 200 |
| IndexNow (post) | ping for sites with `indexnow.enabled` |
| Secondary-language quality | the twin reads native; unedited machine translation does not ship |
| SEO audit (post) | run your SEO-audit skill over the new pages; fix findings on the new posts; re-deploy is ask-first again |

## Gate details (commands)

Run these from the site's `source_tree`. `$NEW` = the new and edited post files plus their discovery files.

- **CSS-integrity.** A de-slop or punctuation edit can collapse `,.`→`.` and invalidate every `rgba()`, silently destroying a design.
  ```bash
  grep -rnE 'rgba\([0-9]+,[0-9]+,[0-9]+\.[0-9]+\)' $NEW   # must print nothing
  ```
  Use `[0-9]`, never `\d` — `grep -E` has no `\d`, so that pattern matches nothing and the gate silently passes on broken CSS.
- **Forbidden-pattern.** Per site, over `$NEW` only (older posts may predate the rule; the whole tree still ships):
  ```bash
  grep -rniE 'CVE-[0-9]{4}-[0-9]+' $NEW   # one grep per forbid_patterns entry
  ```
  Non-zero = rewrite the sentence; don't ship.
- **Banned-term.** Load the local banned-terms file, apply global lines and the lines scoped to this site:
  ```bash
  site=example-ai
  grep -vE '^[[:space:]]*(#|$)' .claude/blog-pipeline/banned-terms.local.txt \
    | awk -v s="${site}:" 'index($0, s) == 1 { print substr($0, length(s) + 1); next } !/^[a-z0-9-]+:/' > /tmp/bp-banned.txt
  grep -rniEf /tmp/bp-banned.txt $NEW     # must print nothing
  ```
  Check alt text, filenames, OG paths, JSON-LD and llms entries too — they are public, indexed text. After the deploy, sweep the live URLs once more if you have a crawler for it.
- **Fact** → [fact-gate.md](fact-gate.md).
- **OG-card.** Every `og:image` / `twitter:image` URL in the pages you ship must exist as a file in the tree you upload. A generator that creates missing cards must **only create missing ones** — an unconditional run can overwrite every hand-picked card on the site. Back up the OG directory before any bulk change.
- **JSON-LD URL.** `grep -oE '"(mainEntityOfPage|@id|item)": *"[^"]+"' <post>` against the `<link rel=canonical>`. A non-ASCII character in a URL (an umlaut variant of an ASCII slug) is a fail: canonical, `og:url` and hreflang can all be right while the JSON-LD points at a 404.
- **lastmod.** Touch only the new entries plus the hub pages whose content changed (and the homepage if `bump_lastmod_on_hubs`). Flattening every `<lastmod>` to the deploy date teaches crawlers to ignore your lastmod.
- **No new trackers.** A tracker without a consent gate is a privacy-law exposure in many jurisdictions (GDPR/ePrivacy in the EU). Don't paste one in with a template, and don't widen a CSP for one.
- **Secondary-language quality.** Google lists automated translation with little added value as scaled content abuse. Ship the twin only when it reads native.

## The deploy hook contract

`deploy.command` in the config is whatever ships the site. blog-pipeline treats it as a black box with this contract:

1. **Ask first.** Show the user: the files that will ship, the dry-run output (`deploy.dry_run`, if the method has one), the fact-table totals, the stop-slop scores. Run nothing that touches the live site before the yes. A method without a dry-run is said so in the ask — a flag the script does not parse is NOT a dry run; check before trusting `--dry-run`.
2. **Credentials from the environment only** (`deploy.env_file` loaded into the process, never echoed, never committed). Never put a host, user or password in the config, a skill file or a prompt.
3. **Detached when long.** If the deploy can exceed your tool's foreground timeout, run it in the background and wait for it to exit. A foreground run killed mid-upload leaves a live site half-updated (page up, hero 404, twin missing).
4. **One session per hosting account.** Sites sharing `deploy.shared_account_group` never deploy concurrently — chain them in one detached command. Shared hosts cap connections per account.
5. **Images and discovery files ship with the post.** An HTML-only deploy 404s the hero. Upload pages before the sitemap/feeds/llms files so discovery never points at a missing page (the bundled FTP script orders it that way).
6. **Protect server-only files.** A full mirror must never delete or overwrite `.htaccess`, `.well-known/`, search-engine verification files or anything else that exists only on the server.
7. **Exit code** 0 = success. Anything else = report and stop; don't retry blindly.

## Deploy method examples

**FTP / FTPS (bundled example)** — [../scripts/ftp-deploy.py](../scripts/ftp-deploy.py): hash-diff against a local manifest, assets → pages → discovery order, upload-then-rename, protected server-only files, `--dry-run`, opt-in `--delete-orphans` (only files it uploaded itself).
```bash
set -a; . ./.env.example-ai; set +a        # FTP_HOST FTP_USER FTP_PASSWORD FTP_REMOTE_DIR [FTP_TLS FTP_PORT]
python .claude/skills/blog-pipeline/scripts/ftp-deploy.py --local sites/example-ai --dry-run
python .claude/skills/blog-pipeline/scripts/ftp-deploy.py --local sites/example-ai
```
First deploy: with no manifest in `.deploy-state/` yet, every file counts as new and the whole tree goes up over the live site. The script refuses that run without `--first-run`; make it its own ask-first step, after the user has seen the full dry-run list.

**SFTP** (key-based auth, no password in env):
```bash
sftp -b - deploy@host.example <<'EOF'
put -r sites/example-ai/* /var/www/example.com/
EOF
```
For incremental SFTP prefer `rsync` over SSH, or `lftp -e "mirror -R --only-newer --exclude .htaccess ..."`.

**rsync over SSH:**
```bash
rsync -avzn --exclude '.htaccess' --exclude '.well-known/' sites/example-notes/ deploy@example.org:/var/www/example.org/   # dry run
rsync -avz  --exclude '.htaccess' --exclude '.well-known/' sites/example-notes/ deploy@example.org:/var/www/example.org/
```
Never add `--delete` without the same excludes and a dry run first.

**GitHub Pages / any git-based host:** the deploy is the push to the publishing branch (or the Actions workflow it triggers). The ask-first gate applies to the push. Dry run = `git status` + `git diff --stat` on the publishing branch.

**Custom:** any command honouring the contract above (a CI trigger, a cloud-storage sync, an SSG build + upload). If it includes a build, the build runs after the yes.

## Post-deploy

1. **Live verify:** `curl -sI` both language URLs and the hero `.webp` → 200; spot-check title, hero, JSON-LD, hreflang in the live HTML. Better still, open the page in a real browser and check the console and network tabs — curl can't see a CSP that blocks a script or a font.
2. **Registration + link gate** (both languages; the deploy is not done until all pass):
   1. in the live sitemap (`curl -s <base>/sitemap.xml | grep -c <slug>` ≥ 1);
   2. in every live llms file, with today's `Updated:` stamp where the file has one;
   3. in every live feed (`curl -s <feed> | grep -c <slug>` ≥ 1);
   4. listed on every hub page;
   5. **every internal `href` on the new pages returns 200** — extract and `curl -s -o /dev/null -w '%{http_code}'` each; a 301 or 404 is a fail.
   Copy footer and CTA from the newest live post, never an old one — old templates carry dead footer links and redirecting CTAs.
3. **IndexNow** for sites with `indexnow.enabled`: [../scripts/indexnow-ping.py](../scripts/indexnow-ping.py) `--key "$INDEXNOW_KEY_EXAMPLE_AI" <host> <primary-url> <secondary-url>` (the script reads only `--key` or `INDEXNOW_KEY`, so pass the site's `indexnow.key_env` variable explicitly). Google doesn't consume IndexNow; Bing, Yandex, Naver and Seznam do, and Bing's index feeds several AI answer engines.
4. **SEO audit** of the new pages with whatever SEO-audit skill you use. Fix findings on the new posts locally without asking; site-wide findings go into the closing report with a recommendation; the re-deploy is ask-first again. The run is not done until that report exists.
