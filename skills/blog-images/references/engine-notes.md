# Engine notes — ComfyUI + FLUX.1-schnell

## Contents
- Setup
- In-image text gotcha
- Style verdicts
- Render details
- Common failures
- Model facts, with sources
- Newer free local models (not required)

## Setup

- **ComfyUI** (https://github.com/comfyanonymous/ComfyUI), run natively or in Docker, listening on `127.0.0.1:8188` by default. Bind it to localhost; the API has no auth.
- **Checkpoint:** an all-in-one FLUX.1-schnell fp8 checkpoint (bundles T5 + CLIP + VAE, ~17 GB) in `ComfyUI/models/checkpoints/`. The script auto-picks the first checkpoint whose name contains `flux`; `--model` forces one.
- **Health check:** `curl -s 127.0.0.1:8188/system_stats`. The script exits with "ComfyUI not reachable" when it is down.
- **Optional:** ComfyUI-Manager for installing nodes/models from the GUI; an upscaler model (e.g. a 4× ESRGAN variant in `models/upscale_models/`) if you need a 2K hero. The GUI at `http://127.0.0.1:8188` reloads a render's exact graph when you drag the PNG onto the canvas.

## In-image text gotcha

FLUX.1-schnell is a few-step distilled model that renders in-image text **poorly** (garbled, misspelled). Keep heroes **text-free** and keep the no-text tail. The trap is a subject built on a *text surface* — a card, label, button, screen or list: schnell fills those with gibberish. Re-pick the metaphor so meaning rides on **shape, colour and mechanism** — walls/zones, flows/conduits, colour-tagged tokens and sockets, a single capped tile among many. The same subjects re-rolled text-free usually land first try. Never ship a hero with garbled words.

## Style verdicts

- **3D / photographic (Styles 4–11) hold on any subject**: isometric diorama, hyperreal macro, exploded-view, soft-clay robot characters, brass-and-navy precision machine, **tilt-shift miniature photograph** (the strongest result — reads as a real physical model, not CGI), liquid-metal chrome.
- **Flat / print / illustrated (Styles 12–17)** — risograph, gouache poster, film still, claymation photo, origami, Bauhaus — render cleanly on FLUX **only on a simple 1–2-element subject**; on a busy scene FLUX reverts to hyperreal 3D.
- **Tested poorly:** paper-cut and risograph on busy subjects (bland, leaked readable text), low-poly (gamey/abstract), dark-cinematic on a neutral subject ("boring" — security posts only).
- **Caveat:** the glossy, over-smooth, too-symmetrical premium-3D/clay render is itself a slop dialect. Vary toward grain, texture, visible linework and editorial treatments, not just clean 3D in a new palette.

## Render details

- **Params (hard-coded in the script's graph):** cfg **1**, **4–6 steps**, sampler **euler**, scheduler **simple**, **16-channel SD3 latent** (`EmptySD3LatentImage`, not SDXL's `EmptyLatentImage`).
- **Graph:** `CheckpointLoaderSimple` → two `CLIPTextEncode` (pos/neg, clip `[4,1]`) → `EmptySD3LatentImage` → `KSampler` → `VAEDecode` (vae `[4,2]`) → `SaveImage`. Raw API: `POST /prompt {prompt: <graph>}` → `{prompt_id}`; poll `GET /history/{id}`; fetch `GET /view?filename=&subfolder=&type=output`.
- **Size:** default 1344×768 (16:9 hero); square 1024×1024; vertical 768×1344. FLUX is happy at 768–1536 px.
- **Speed:** on an 8 GB GPU the fp8 checkpoint offloads to system RAM — tens of seconds to a few minutes per image depending on VRAM pressure. On 16 GB+ it is much faster.
- **Output:** a real PNG at `--out`, verified (PNG magic bytes + size) and written atomically, so a bad render fails loud instead of saving an empty file.
- **Reproducibility:** omit `--seed` for a fresh image; `--seed N` (N ≥ 1) reproduces a pick exactly. `--seed 0` means random, not seed zero.

## Common failures

1. **`:8188` unreachable** → start ComfyUI and wait until `/system_stats` answers.
2. **VRAM contention / OOM / crawl** → another GPU app is loaded (a second ComfyUI or UI front-end, a local LLM holding VRAM, a game). One heavy model at a time. Slow ≠ broken. If it still OOMs, cut resolution before switching model.
3. **No FLUX checkpoint** → the script falls back to the first checkpoint installed. An SDXL model needs real settings: `--model <file> --steps 25 --cfg 5`.
4. **Over-cooked / noisy render** → `--steps 4` first; fewer steps is the usual fix on a distilled model.
5. **Garbled text** → redesign the subject text-free (above).

## Model facts, with sources

| Fact | Value | Source |
|------|-------|--------|
| FLUX.1-schnell step range | "1 to 4 steps"; card example uses `num_inference_steps=4`, `guidance_scale=0.0`, `max_sequence_length=256` | https://huggingface.co/black-forest-labs/FLUX.1-schnell |
| FLUX.1-schnell licence | Apache-2.0 (commercial use allowed) | same model card |
| ComfyUI checkpoint location | all-in-one fp8 checkpoint in `ComfyUI/models/checkpoints/`; the fp8-checkpoint note says to set CFG to 1.0 | https://comfyanonymous.github.io/ComfyUI_examples/flux/ |

- The script's default `--steps 6` sits above the card's 1–4 range; it is the value the approved pilot heroes were rendered with. Try 4 if a render looks over-cooked.
- `guidance_scale=0.0` in diffusers and `cfg 1` in ComfyUI both mean "no classifier-free guidance" — which is why the negative prompt barely registers.

## Newer free local models (not required)

Both claim better in-image text than schnell, the engine's biggest gap. Adopting one means a download, a new ComfyUI graph and a fresh pilot.

| Model | Licence | Steps | VRAM (vendor claim) | Text rendering (vendor claim) | Source |
|-------|---------|-------|---------------------|-------------------------------|--------|
| FLUX.2 [klein] 4B (Black Forest Labs) | Apache-2.0 | 4 in the card's example | "~13GB", RTX 3090/4070 and above | card warns text "may be inaccurate or subject to distortion" | https://huggingface.co/black-forest-labs/FLUX.2-klein-4B |
| Z-Image-Turbo 6B (Tongyi-MAI) | Apache-2.0 | 8 NFEs, guidance 0 | "fits comfortably within 16G VRAM consumer devices" | "accurately rendering complex Chinese and English text" | https://huggingface.co/Tongyi-MAI/Z-Image-Turbo |
