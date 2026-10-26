#!/usr/bin/env python3
"""Generate a blog hero image locally via ComfyUI + FLUX.1-schnell.

Stdlib only — no pip dependencies.

The intelligence (subject from the post body, style rotation, anti-slop) comes from the
blog-images skill — this script is just the render engine. Pass the fully written prompt;
it returns a verified PNG on disk.

Usage:
  python comfy_generate.py --prompt "<subject-first prompt>" --out path/to/hero.png
  python comfy_generate.py --prompt "..." --out h.png --width 1344 --height 768 --steps 6

Defaults: first checkpoint whose name contains "flux" (else the first installed),
1344x768 (16:9 hero), cfg 1, 6 steps, euler/simple.
ComfyUI URL: --url, else $COMFYUI_URL, else http://127.0.0.1:8188.
FLUX at cfg 1 ignores classic negatives, so --negative defaults to empty (kept for parity).
"""
import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error

DEFAULT_URL = os.environ.get("COMFYUI_URL", "http://127.0.0.1:8188")


def _get(url, timeout=8):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _post(url, payload, timeout=20):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def pick_flux_model(base, override=None):
    if override:
        return override
    info = _get(f"{base}/object_info/CheckpointLoaderSimple")
    names = info["CheckpointLoaderSimple"]["input"]["required"]["ckpt_name"][0]
    if not names:
        raise SystemExit("ComfyUI has no checkpoint installed (put a FLUX checkpoint in ComfyUI/models/checkpoints/).")
    flux = [n for n in names if "flux" in n.lower()]
    return flux[0] if flux else names[0]


def build_workflow(model, prompt, negative, width, height, steps, cfg, seed):
    # FLUX text2img: 16-channel SD3 latent (NOT SDXL EmptyLatentImage), cfg 1, euler/simple.
    return {
        "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": model}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["4", 1]}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"text": negative, "clip": ["4", 1]}},
        "5": {"class_type": "EmptySD3LatentImage", "inputs": {"width": width, "height": height, "batch_size": 1}},
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed, "steps": steps, "cfg": cfg,
                "sampler_name": "euler", "scheduler": "simple", "denoise": 1,
                "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0],
            },
        },
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "bloghero", "images": ["8", 0]}},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", required=True, help="where to write the PNG")
    ap.add_argument("--negative", default="")
    ap.add_argument("--width", type=int, default=1344)
    ap.add_argument("--height", type=int, default=768)
    ap.add_argument("--steps", type=int, default=6)
    ap.add_argument("--cfg", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=0, help="N >= 1 reproduces a render; 0 = random")
    ap.add_argument("--model", default=None, help="checkpoint filename to force")
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--timeout", type=int, default=300, help="seconds to wait for the render")
    a = ap.parse_args()
    base = a.url.rstrip("/")

    seed = a.seed if a.seed > 0 else int(time.time() * 1000) % 1_000_000_000

    try:
        model = pick_flux_model(base, a.model)
    except (urllib.error.URLError, OSError) as e:
        raise SystemExit(f"ComfyUI not reachable on {base} — start ComfyUI first. ({e})")

    print(f"model={model} size={a.width}x{a.height} steps={a.steps} cfg={a.cfg} seed={seed}", file=sys.stderr)
    wf = build_workflow(model, a.prompt, a.negative, a.width, a.height, a.steps, a.cfg, seed)
    try:
        queued = _post(f"{base}/prompt", {"prompt": wf})
    except urllib.error.HTTPError as e:
        # A 400 carries ComfyUI's validation error (unknown checkpoint, bad size, missing node) in the body.
        body = e.read().decode("utf-8", "replace")[:2000]
        raise SystemExit(f"ComfyUI rejected the prompt (HTTP {e.code}): {body}")
    pid = queued.get("prompt_id")
    if not pid:
        raise SystemExit(f"ComfyUI did not queue the prompt: {queued}")

    for _ in range(max(1, a.timeout // 2)):
        time.sleep(2)
        try:
            hist = _get(f"{base}/history/{pid}")
        except (urllib.error.URLError, OSError):
            continue
        outputs = hist.get(pid, {}).get("outputs")
        if not outputs:
            continue
        for node in outputs.values():
            imgs = node.get("images") or []
            if imgs and imgs[0].get("filename"):
                im = imgs[0]
                q = urllib.parse.urlencode({
                    "filename": im["filename"],
                    "subfolder": im.get("subfolder", ""),
                    "type": im.get("type", "output"),
                })
                with urllib.request.urlopen(f"{base}/view?{q}", timeout=30) as r:
                    data = r.read()
                if len(data) < 1000 or data[:8] != b"\x89PNG\r\n\x1a\n":
                    raise SystemExit("ComfyUI returned a non-PNG / empty file.")
                tmp = a.out + ".tmp"
                with open(tmp, "wb") as f:
                    f.write(data)
                os.replace(tmp, a.out)
                print(a.out)  # stdout = the saved path
                return
    raise SystemExit(f"ComfyUI render timed out after {a.timeout}s.")


if __name__ == "__main__":
    main()
