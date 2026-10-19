# Prompt Recipes — copy-paste styles + worked examples

Read this right before writing a FLUX prompt. The style blocks are *treatments*. You still supply the **subject** (the scene derived from the post) and put it **first**.

## Contents
- Worked subject mappings · Banned generic metaphors + gold reference · Styles that landed · Variety and palette rules
- Concept-derivation checklist · Prompt framework
- Styles 1–3 (bright cyan+purple — brand option only) · Styles 4–11 (3D/photographic) · Styles 12–17 (flat/illustrated, simple subjects only)
- Negative tail + ratio/resolution
- Worked examples (subject-first)
- Iterating with a fixed seed
- When FLUX is the wrong tool (labelled diagrams)
- Gotchas · Anti-slop detail and sources

## Worked subject mappings

| Post is about… | Subject that reads instantly |
|---|---|
| Agent orchestration / multi-agent systems | A central conductor/hub directing several worker units along parallel tracks; one track loops back (retry) |
| Production RAG pipeline | The pipeline itself: documents → chunks → vector space → **AI model** → grounded answer (the gold reference below; "pull the right card from an indexed archive" lost to it — an archive is a banned metaphor and a card is a text surface) |
| Threat model / security layers | Concentric layered shells around a core; one probe deflected at an outer layer |
| Demo → production gap | Two sides: a fragile sketch vs. a solid engineered structure built from it |
| Cost / ROI of AI | A lever turning a small input into a large coordinated output — with the AI model visibly doing the work (a bare balance scale is banned) |
| Firewall / network change | Walls and zones with a gate being re-routed; colour-tagged flows moving from an old appliance to a new one |
| Compliance audit evidence | A physical binder-free evidence trail: tagged tokens flowing from systems into one sealed container an inspector lifts |

## Banned generic metaphors + gold reference

**Show the actual subject — literally.** The post's real subject must be *visibly in the frame*, not replaced by a generic metaphor a reader can't connect to the topic. Banned — each could illustrate almost any article and carries no technical signifier:

| Generic metaphor | Reads as | Why it fails |
|---|---|---|
| Tightrope / bridge over a chasm | "any risky leap" | nothing about the topic |
| Library shelves / archive | "any search/lookup" | shows lookup, not the topic |
| Balance scale | "any trade-off" | generic |
| One glowing sphere among grey ones | "any odd-one-out" | abstract, not the subject |

**Gold reference:** a RAG post's winning hero literally drew the pipeline — documents → chunks → vector space → **AI model** → grounded answer. It beat an abstract "pull a book from a library" image, because that showed *lookup*, not retrieval-augmented **generation**. Test every concept: *would a reader who knows the topic recognise it as THIS, with the technical part visible?* If not, it's a metaphor, not a subject.

## Styles that landed

| Style | Example that landed |
|---|---|
| Soft 3D clay (warm, friendly, characterful) | Containers → a clay whale hauling shipping containers |
| Premium hyperreal 3D, rich materials | Logistics → navy + brass-gold ship's wheel scanning a manifest |
| Clean 3D infographic / explicit pipeline | RAG → docs → chunks → vector space → AI model → grounded answer |
| 3D diorama with a mood split | AI-project failure → warm-gold demo vs cool-grey production, same robot |
| Editorial ink, flat vector, isometric, paper-cut, blueprint, low-poly | pick what fits — but paper-cut and low-poly tested poorly, and flat styles hold only on simple subjects (verdicts below) |

## Variety and palette rules

**Vary the art style AND the palette for every post.** A set where every image shares one palette and a couple of layouts reads as templated AI slop — a whole batch can be rejected for "they all look the same". Each post should look like its own piece.

**Palette is per post** — amber/teal, navy/gold, indigo/electric-blue, charcoal/red, blue/gold… never a fixed cyan+purple. The hard floor is the **slop signature**: dark navy + omnidirectional glowing orbs + floating particles + mesh grid. Moody/dark is fine where the topic wants it (a security post); generic neon-on-navy is not.

Styles 1–3 (bright cyan+purple) are an option only for a brand that already uses those colours. The general pool to **rotate randomly through** is **Styles 4–11** (clay · brass-and-navy · isometric · hyperreal macro · exploded-view · tilt-shift miniature · liquid-metal; dark-cinematic = security posts only), plus **Styles 12–17** on simple subjects. Random order, no repeats until the pool is used up; per-site style family overrides (SKILL.md step 3).

## Concept-derivation checklist (before touching a style)

1. Read the post body (not just the title). Note the headings — they are the argument.
2. Write one sentence: *what must this image communicate?* The 1–2 most concrete ideas, not all of them.
3. Translate that sentence into a **physical scene** — something a camera or sculptor could capture. If the scene is "nodes connected by glowing lines", reject it and find something specific to this post.
4. Only now pick a style and assemble the prompt subject-first.

## Prompt framework — flowing prose, subject first

FLUX parses **flowing prose far better than keyword lists** — tag soup ("4k, masterpiece, trending on artstation, octane render") does nothing and dates the prompt. Write 2–4 plain sentences, **subject first**. FLUX-schnell runs at cfg 1, so the negative prompt is essentially ignored — steer positively.

**Subject + descriptors → Composition/camera → Action → Location/context → Style/medium.**

Two craft rules that outrank any style keyword:

- **Positive constraints beat negatives.** Say "flat, even, overcast studio light, matte surfaces", don't just say "no dramatic lighting". Keep a *short* negative tail as a backstop.
- **Name the imperfection.** The #1 AI-image tell is the too-perfect render: poreless surfaces, omnidirectional golden glow with no real source, over-saturation, dead symmetry. Counter it explicitly — "visible material texture, slight grain, one off-axis light source, gentle asymmetry, minor real-world wear". For any photographic look add a camera/lens/film ref ("shot on a mirrorless camera, 56mm, f/2.8").

## Styles 1–3 — bright cyan+purple (brand option, NOT a default)

Use only for a brand that already lives in cyan+purple; never paint a whole set in it.

### Style 1 — Iridescent glass 3D
> rendered as a premium 3D iridescent glass sculpture: translucent frosted-glass forms on a bright, very-light cool-gray studio background; subtle cyan (#06b6d4) and purple (#7c3aed) iridescence only in refractions, caustics and edge highlights; otherwise neutral glass. Soft studio lighting, gentle shadows, shallow depth of field, off-center, clean and minimal, slight realistic surface imperfection (faint micro-scratches, frosting variation).

### Style 2 — Neon on light gradient
> rendered as a bright, airy, premium abstract tech illustration: soft off-white to very pale cool-gray gradient background with subtle paper-like texture; cyan (#06b6d4) and purple (#7c3aed) as crisp luminous threads and small forms, high contrast against the light background; gentle soft shadows, subtle depth; keep it bright.

### Style 3 — Ink + neon generative
> rendered as abstract ink-in-water / marbling meeting neon signal lines: bright background (white to very pale lavender); flowing ink plumes in soft purple tones with crisp cyan (#06b6d4) filament lines threading through; artistic, organic, editorial, high-end.

## Styles 4–11 — 3D / photographic (verified in a style pilot; hold on any subject)

Pilot verdicts: all seven of 4, 5, 7–11 landed on a constant orchestration subject. Rejected in the same pilot: paper-cut and risograph on a busy subject (bland, and they leaked readable text), low-poly (gamey/abstract), dark-cinematic on a neutral subject ("boring"). Append the subject in front and the negative tail at the end.

### Style 4 — Soft 3D clay, warm (amber/teal)
> rendered as soft Pixar-like 3D clay: rounded matte plasticine forms with visible fingerprint/clay texture and gentle imperfection; warm amber (#f59e0b) + soft teal (#14b8a6) palette on a bright cream studio background; one soft overhead light, gentle shadows, shallow depth, off-center, characterful and friendly.
> *Tip: works well with cute clay **robot characters** as the subject (orchestrator bot + worker bots).*

### Style 5 — Hyperreal 3D, navy + brass-gold (premium)
> rendered as a premium hyperreal 3D product render: rich real materials (brushed brass, deep navy enamel, matte steel) with believable micro-scratches and fingerprints; deep navy (#1e293b) + brass-gold (#b08d57) palette on a clean light-gray studio sweep; single soft key light, true reflections, shallow depth of field, off-center, museum-product feel.
> *Landed as a precision brass clockwork/instrument machine — gears, arms, a belt loop.*

### Style 6 — Dark cinematic 3D, charcoal + red (security topics ONLY) ⚠️
> rendered as a restrained dark cinematic 3D scene (NOT neon-on-navy slop): matte charcoal (#1c1c1e) surfaces with a single warning-red (#dc2626) accent and one hard practical light source casting a real directional shadow; gritty texture, slight grain, asymmetric composition, tense and serious — moody but legible, no glow, no particles.
> ⚠️ Reads "boring" on a neutral subject. Reserve for genuine security/threat posts. Don't write "glowing X" while banning glow — use a *reflective* red metal inlay that catches the light.

### Style 7 — Isometric 3D diorama / micro-world (mint + coral)
> rendered as a clean isometric 3D diorama / tiny micro-world on a bright cream background: neat low-rise blocks, ramps and tracks built at a 2:1 isometric angle; mint-green (#34d399) + coral (#fb7185) palette, soft matte surfaces; gentle ambient occlusion, soft shadows, slight imperfection; tidy, playful, explanatory.

### Style 8 — Hyperreal macro close-up (gunmetal + electric blue)
> rendered as an extreme hyperreal macro photograph, shallow depth of field (f/2.0): a single close-up object filling the frame with crisp real material detail (brushed gunmetal, anodised edges, fine dust motes); gunmetal grey with one electric-blue (#3b82f6) accent of light; one soft off-axis source, true reflections, visible micro-texture and a little grain; shot on a 100mm macro lens.

### Style 9 — Exploded-view / cutaway 3D (aluminium + emerald)
> rendered as a premium exploded-view 3D render: a device or mechanism separated into stacked component layers floating in alignment to reveal how it fits together; brushed aluminium and matte-white parts with a single emerald (#059669) accent; clean light-gray studio sweep, soft key light, true material reflections, shallow depth, slight realistic wear; technical but elegant.

### Style 10 — Tilt-shift miniature photograph (teal + warm-orange) — strongest pilot result
> photographed as a tilt-shift miniature so it reads as a genuine physical scale model on a desk: a real-looking tiny tabletop model of the scene, strong miniature-faking blur top and bottom, a shallow focus band across the centre, soft warm daylight, teal + warm-orange props, real materials and tiny imperfections. Photographic, NOT CGI — looks like a photo of an actual model, which is exactly why it reads as "not AI."

### Style 11 — Liquid-metal / polished chrome 3D (silver + one warm accent)
> rendered as a premium liquid-metal / polished chrome 3D abstract: flowing reflective mercury-like forms with true studio reflections and soft caustics; monochrome silver with a single warm-gold accent; clean very-light gradient studio background, soft key light, shallow depth, off-center, sleek and high-end.

## Styles 12–17 — flat / illustrated / photographic (FLUX-verified, simple subjects only)

On FLUX these render cleanly — but **only on a simple, 1–2-element subject** (a lighthouse, a single folded form). On a busy multi-element scene the literal subject overrides the treatment and FLUX-schnell snaps back to hyperreal 3D. So: keep the subject simple and front-load the style; if the scene must be busy, use Styles 4–11.

### Style 12 — Risograph / 2-tone screenprint
> rendered as a two-tone risograph screenprint: coarse halftone grain, slight ink mis-registration, a limited 2–3 ink palette (e.g. warm coral + deep teal) on cream paper, flat layered shapes, visible print texture.

### Style 13 — Mid-century gouache travel poster
> rendered as a 1950s mid-century travel poster painted in gouache: bold simplified shapes, a warm retro palette (mustard, burnt-orange, sage), flat stylised clouds/forms, subtle paper texture, confident brushwork.

### Style 14 — Cinematic anamorphic film still (photographic)
> a cinematic anamorphic film still: shallow depth of field, soft natural side light, gentle film grain and subtle lens character, a muted teal-and-amber colour grade, shot on 35mm; atmospheric and real — reads strongly as "not AI".

### Style 15 — Claymation stop-motion photograph
> photographed as a real stop-motion claymation set: everything moulded from plasticine with visible fingerprints and tool marks, a tabletop model world, soft studio light, warm friendly palette — looks like a photo of an actual clay model, NOT a CGI render. (Distinct from Style 4, which is a clean render.)

### Style 16 — Origami / folded paper
> rendered entirely as folded origami paper: crisp creases, faceted folded planes, layered paper textures, soft studio light and gentle shadows, a warm paper palette (cream / coral / slate) on a clean background.

### Style 17 — Bauhaus geometric poster
> reduced to bold Bauhaus geometry: simple circles, triangles and rectangles, a primary-leaning palette (red / blue / yellow + black + cream), flat hard-edged shapes, balanced asymmetric composition, subtle paper grain.

## Negative tail + ratio/resolution (append to every prompt)

> No dark navy background, no glowing orbs/nodes, no floating particles, no mesh grid, no neon/volumetric/cinematic/bloom glow. No text, words, numbers, logos or watermarks.

A **backstop only** — the steering happens positively in the prompt body.

**Ratio/resolution — script flags, NEVER the prompt.** Writing "16:9" or a resolution into the prompt invites FLUX to render it as text. Default **1344×768** (16:9 hero), square **1024×1024**, vertical **768×1344**. FLUX is happy at 768–1536 px.

## Worked examples (subject-first)

**Example A — agent orchestration post, isometric subject + glass style (brand option)**
Post argues: one orchestrator coordinates a fleet of agents running tasks in parallel, with retries on failure.
```
An isometric 3D diorama: a central orchestrator hub dispatches work along several parallel
tracks to a row of smaller worker-agent units, each running a different task at once; thin
cyan lines show the hub→worker coordination; one track loops back on itself to suggest a
retry/fallback path; small abstract tool-blocks beside each worker — rendered as a premium
3D iridescent glass sculpture on a bright very-light cool-gray studio background, cyan
#06b6d4 + purple #7c3aed iridescence in refractions and edge highlights only. Soft studio
lighting, gentle shadows, shallow depth, off-center, slight realistic imperfection.
No dark navy background, no glowing orbs, no floating particles, no mesh grid, no
cinematic/volumetric glow. No text, words, numbers, logos or watermarks.
```

**Anti-example — what NOT to write for a RAG post**
"A precise retrieval mechanism drawing one glowing card out of a large, neatly indexed archive of cards…" breaks three rules: an archive is a banned metaphor, a card is a text surface FLUX fills with gibberish, and "glowing" contradicts the no-glow tail.

**Example B — RAG pipeline post, exploded-view style (Style 9)** — written to the rules above; pilot it before batching.
Post argues: the answer is only as good as the chunk the retriever hands the model.
```
A literal retrieval-augmented generation pipeline laid out left to right as one physical
machine: a short stack of blank paper documents feeds a cutter that slices them into small
uniform tiles; the tiles drop into a clear acrylic cube where they hang in loose clusters;
a mechanical arm lifts two matching tiles out of one cluster and slots them into a compact
brushed-aluminium module that stands for the AI model; a single finished tile slides out the
far end. Seen from a slightly raised three-quarter angle, off-centre, shallow depth of field.
Rendered as a premium exploded-view 3D render: brushed aluminium and matte-white parts with a
single emerald accent on the two chosen tiles, clean light-grey studio sweep, one soft key
light, true material reflections, slight realistic wear and fine surface scratches.
No dark navy background, no glowing orbs, no floating particles, no mesh grid, no neon or
volumetric glow. No text, words, numbers, logos or watermarks.
```

## Iterating — re-run with a tweaked prompt (+ fixed seed)

There is no conversational "edit". To refine, re-run `comfy_generate.py` with an adjusted prompt and the winner's `--seed N` to keep the composition stable while you nudge one thing (same prompt + same seed = deterministic). Effective nudges:
- "…on a brighter, cleaner, cooler background."
- "…remove the stray reflection in the lower right."
- "…push the central element slightly off-center to the left."
- "…reduce the purple, keep the cyan."

Omit `--seed` for a genuinely fresh composition. The script is text-prompt only (no image references): hold consistency across a series by re-using a seed and re-describing the recurring element in prose.

## When FLUX is the wrong tool (labelled diagrams)

If a post genuinely needs a clean **labelled** diagram (stage names on a pipeline), FLUX-schnell will garble the labels. Either compose without text, draw the diagram as SVG/HTML in the post itself, or use an image model with strong text rendering for that one image — and proofread every label (in every language) before shipping.

## Gotchas

- **Subject clause ignored** → it was too short or too far back. If the render nails the style but misses the meaning, lengthen the subject, move it further front, shorten the style block.

## Anti-slop detail and sources

Keep the subject clause doing the heavy lifting; the positive anti-slop description does the second-most work; the negative tail is a backstop (FLUX follows "what it is" far better than "what it isn't", and at cfg 1 barely reads the negative).

The broader AI-image slop tells are about the render being **too perfect**: porcelain/poreless surfaces, an omnidirectional golden-hour glow with no real light source, over-saturation, dead symmetry — plus the glossy, over-smooth premium-3D/clay look that has itself become a dialect. Counter all of it the same way: **steer positively, then name the imperfection.** Real craft/material and *mundane* lighting (one overhead/overcast source), a limited palette, off-centre composition, visible texture, slight grain, gentle asymmetry, minor real-world wear; for photographic looks a camera/lens/film reference and visible grain.

Background reading for the prompt-craft principles: Google's published prompting guides for its image models (blog.google, cloud.google.com), and practitioner write-ups on making AI images that don't look AI-generated.
