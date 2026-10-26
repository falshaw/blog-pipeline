---
name: blog-images
description: Generates post-grounded blog hero images locally via ComfyUI + FLUX.1-schnell — a literal, text-free subject taken from the post body, never random abstract art, with a randomised style per post — then delivers the responsive WebP set, a 1200x630 OG card and per-language alt text. Use for "make images for the blog", "blog hero image", "create a picture for this post", "OG image for this post", "generate blog visuals", or as step 4 of blog-pipeline.
---

# Blog Images — post-grounded hero images via local ComfyUI + FLUX

The failure this skill exists to stop: a pretty-but-meaningless picture that ignores the article. Every image must be **legible as "this is what the post is about"** at a glance.

Two things are always separate, and conflating them is the root mistake:

- **Subject** = *what is depicted*. Comes from the post's actual content. This is the hard part and the part people skip.
- **Style** = *how it's rendered*. Drawn at random from the verified pool (Styles 4–17 in [references/prompt-recipes.md](references/prompt-recipes.md); Style 6 is for security posts only, Styles 12–17 for simple subjects only). This is the easy part.

If you only get one thing right, get the subject right. A plain-but-on-topic image beats a gorgeous off-topic one every time.

Per-site settings (image dir, OG path, widths, hero size, style family) come from the blog-pipeline config (`.claude/blog-pipeline/sites.yaml` → `images`). Without a config, ask for the target paths once.

## Workflow

### 1. Read the actual post first — non-negotiable

Read the post's **body**, not just the title or meta description. **Metadata is not enough — and a batch is no excuse.** Title + excerpt produce generic metaphors ("a library" for a retrieval post, "a tightrope" for a project-failure post — neither shows the technology). The specific, depictable mechanism lives in the section headings and the opening sentence of each section; read those for every post, even in a 40-post run. An off-topic image is a 100% rework.

Then write a one-line **concept brief**: *what must this image communicate?* Pull the 1–2 most concrete, visual ideas — the spine, not every topic. Example for an agent-orchestration post: "one orchestrator coordinating a fleet of agents running tasks in parallel, with retries when one fails."

### 2. Turn the concept into a subject (a concrete scene)

Map the abstract idea to something a camera or sculptor could capture. Lead with the *thing*, not the vibe. Worked mappings → [references/prompt-recipes.md](references/prompt-recipes.md) § Worked subject mappings.

**Show the actual subject — literally.** The post's real subject (the model, the pipeline, the agents, the firewall, the output) must be *visibly in the frame*. **Banned generic metaphors:** tightrope/bridge, library shelves/archive, balance scale, one glowing sphere among grey ones — each could illustrate any article. If the only idea you have is "glowing nodes connected by lines", stop: that is the slop default. Test: *would a reader who knows the topic recognise it as THIS, with the technical part visible?*

### 3. Pick a DISTINCT style per post — variety is the point

> **RULE — RANDOMISE the style per post.** For a multi-post run, shuffle the verified pool and assign each post a *different* style + palette, random order, **no repeats until the pool is used up** (then reshuffle). No two posts — never two adjacent ones — share a look. The classic failure is piloting one recipe and painting the whole set in it. Random *style* ≠ random *subject*: the subject still comes from each post's body.

- **Per-site style family.** If a site's existing heroes share a house style (e.g. warm clay characters in teal/cream/amber), set `images.style_family` and randomise *within* that family so new heroes sit well next to the old ones. Palette coherence with the live blog beats raw randomness.
- **Vary art style AND palette** — a one-palette set reads as templated slop. Palette per post (amber/teal, navy/gold, indigo/electric-blue, charcoal/red, blue/gold…). The hard floor is the **slop signature**: dark navy + glowing orbs + floating particles + mesh grid.
- **Text-free.** FLUX.1-schnell garbles in-image text. Avoid subjects built on a *text surface* (card, label, button, screen, list); let meaning ride on shape, colour and mechanism. Never ship a hero with garbled words.
- **Engine verdicts:** Styles 4–11 (3D/photographic) hold on any subject, except Style 6 (dark cinematic), which is for security posts only; Styles 12–17 (flat/illustrated) only on a simple 1–2-element subject. Paper-cut, low-poly and dark-cinematic-on-a-neutral-subject tested poorly. **Glossy over-smooth 3D/clay is itself a slop dialect** — vary toward grain and texture. Detail → [references/engine-notes.md](references/engine-notes.md).

### 4. Write the prompt — subject first, style second

The model weights the front of the prompt most; a long style description up front makes it render the style and ignore the meaning. FLUX parses **flowing prose**, not keyword lists. Steer with **positive description** (at cfg 1 the negative prompt is largely ignored). No dead tags ("4k, masterpiece, trending on artstation").

```
[SUBJECT — concrete, from the post, with descriptors. 1–2 sentences. Lead here.]
[COMPOSITION/CAMERA — off-center, shallow depth, the angle.] [ACTION.] [LOCATION/CONTEXT.]
rendered as [ONE style], on a [bright/flat background], [topic-fit palette].
[Anti-slop, stated POSITIVELY: flat even/overcast studio light, matte materials, visible texture + slight grain, gentle asymmetry, minor real-world wear; for photographic looks a camera/lens/film ref.]
Negative backstop: no dark navy background, no glowing orbs, no floating particles, no mesh grid, no neon/volumetric/cinematic glow, no text/words/numbers/logos/watermarks.
```
Never put "16:9" or a resolution in the prompt — FLUX may render it as text. Set the shape with `--width/--height`.

### 5. Generate locally via ComfyUI + FLUX

```bash
python .claude/skills/blog-images/scripts/comfy_generate.py \
  --prompt "<subject-first prompt>" --out "<scratch>/<slug>.png" \
  --width 1344 --height 768 --steps 6
```

- **ComfyUI must be running** (Docker or native) with a FLUX.1-schnell checkpoint in `models/checkpoints/` (the all-in-one fp8 file bundles T5 + CLIP + VAE). Check: `curl -s 127.0.0.1:8188/system_stats`. Set `COMFYUI_URL` or `--url` for another host.
- **Flags:** `--prompt` + `--out` required; `--width/--height` (default 1344×768; square 1024×1024; vertical 768×1344), `--steps` (6; try 4 if over-cooked), `--cfg` (1.0), `--seed N` (N ≥ 1 reproduces; 0/omitted = random), `--negative`, `--model`, `--url`, `--timeout`. The PNG is verified (magic bytes + size) before it is written.
- **One GPU consumer at a time.** On an 8 GB card FLUX-fp8 offloads to system RAM: a render takes tens of seconds to a few minutes; slow ≠ broken. Stop other GPU apps first; stop ComfyUI again after the run if it holds RAM you need.

Render details and common failures → [references/engine-notes.md](references/engine-notes.md).

### 6. Pilot → pick → batch

Don't batch blind. Generate **3–5 genuinely different concepts on ONE flagship post** — vary the *metaphor* AND the *treatment*. The user triages fast ("1 no, 2 no, 3 yes"), so spread the bets. Let them pick, optionally refine once (same `--seed`, adjusted prompt), *then* batch the rest. Both language versions share one image.

### 7. Deliver web-correct

```bash
python .claude/skills/blog-images/scripts/make_web_set.py --src <slug>.png --slug <slug> \
  --img-dir <source_tree>/<images.dir> --widths 400 800 1200 --og <source_tree>/og/<slug>.jpg
```

- **Filename = the slug.** WebP set `{slug}.webp` + `-400w` / `-800w` / `-1200w` (or the site's `images.widths`).
- **OG card** 1200×630, centre-cropped from the approved hero, text-free. Every post ships with one. Never overwrite a hand-picked card (the script refuses without `--force-og`).
- **Hero markup = copy the newest post's `<img>`**: `srcset`/`sizes`, real `width`/`height`, `fetchpriority="high"`, **never `loading="lazy"`** (LCP image).
- **Alt text is never omitted:** descriptive, ≥ 20 characters, one per language, never keyword-stuffed, never naming people or places.
- **Privacy:** banned terms and PII never appear in an alt, a filename, an OG path, a JSON-LD `image` URL or the prompt log. Run the blog-pipeline banned-term gate over the new files before handing over. Filenames are slugs, so a banned term can only enter through a slug — fix the slug first.
- **Show it locally** before any deploy: open the page (or the dev server) and screenshot it.

Specs with sources → [references/delivery.md](references/delivery.md).

### 8. Generating ≠ publishing

Producing and wiring the image locally is not shipping it. Going live is the blog-pipeline deploy gate: **ask first**, upload the image set and OG card WITH the post, then `curl -sI` the page and the `.webp` → 200.

## Anti-slop rules (why the negatives matter)

One look screams "AI generated": **dark navy background + glowing cyan/purple orbs/nodes + floating particles + a mesh grid + "cinematic/volumetric/soft bloom" glow.** Avoid that whole vocabulary. Counter it, and the broader "too perfect" tells (poreless surfaces, sourceless golden glow, over-saturation, dead symmetry, glossy over-smooth 3D), by **steering positively and naming the imperfection**: real material, one mundane light source, limited palette, off-centre composition, visible texture and grain. The negative tail is only a backstop.

## Reference material

- [references/prompt-recipes.md](references/prompt-recipes.md) — subject mappings, banned metaphors, Styles 1–17, variety rules, prompt framework, worked examples. **Read before writing a prompt.**
- [references/engine-notes.md](references/engine-notes.md) — render details, common failures, style verdicts, model facts with sources, newer local models.
- [references/delivery.md](references/delivery.md) — web image specs with sources, alt-text and privacy rules.
- `scripts/comfy_generate.py` — the ComfyUI client (stdlib only). `scripts/make_web_set.py` — WebP set + OG card (Pillow).
- Keep an approve/reject log per project (e.g. `.claude/blog-pipeline/image-style-notes.md`) and read it before a run; update it as the user reacts.
