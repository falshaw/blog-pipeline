#!/usr/bin/env python3
"""Turn an approved hero PNG into the web set: {slug}.webp + -{w}w.webp widths + a 1200x630 OG card.

Requires Pillow (pip install Pillow).

Usage:
  python make_web_set.py --src hero.png --slug my-post --img-dir site/images --og site/og/my-post.jpg
  python make_web_set.py --src hero.png --slug my-post --img-dir site/assets/img --widths 400 800 --og site/og/my-post.jpg

The base {slug}.webp keeps the source width. The OG card is a centre crop to 1.91:1, resized to 1200x630,
saved as JPEG or PNG by its extension. An existing OG card is never overwritten unless --force-og is passed.
"""
import argparse
import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow missing: pip install Pillow")


def save_atomic(img, path, fmt, **kw):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    img.save(tmp, fmt, **kw)
    os.replace(tmp, path)
    print(f"{path}  {img.width}x{img.height}  {path.stat().st_size // 1024} KB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--img-dir", required=True)
    ap.add_argument("--widths", type=int, nargs="*", default=[400, 800, 1200])
    ap.add_argument("--quality", type=int, default=82)
    ap.add_argument("--og", default=None, help="OG card path (.jpg or .png); omit to skip")
    ap.add_argument("--og-size", type=int, nargs=2, default=[1200, 630])
    ap.add_argument("--force-og", action="store_true", help="overwrite an existing OG card")
    a = ap.parse_args()

    src = Image.open(a.src).convert("RGB")
    out = Path(a.img_dir)
    save_atomic(src, out / f"{a.slug}.webp", "WEBP", quality=a.quality, method=6)
    for w in a.widths:
        if w >= src.width:
            print(f"skip {w}w: source is only {src.width}px wide", file=sys.stderr)
            continue
        h = round(src.height * w / src.width)
        save_atomic(src.resize((w, h), Image.LANCZOS), out / f"{a.slug}-{w}w.webp", "WEBP", quality=a.quality, method=6)

    if a.og:
        og = Path(a.og)
        if og.exists() and not a.force_og:
            print(f"OG card exists, kept: {og} (use --force-og to replace)", file=sys.stderr)
            return
        tw, th = a.og_size
        ratio = tw / th
        if src.width / src.height > ratio:
            cw, ch = round(src.height * ratio), src.height
        else:
            cw, ch = src.width, round(src.width / ratio)
        left, top = (src.width - cw) // 2, (src.height - ch) // 2
        card = src.crop((left, top, left + cw, top + ch)).resize((tw, th), Image.LANCZOS)
        if og.suffix.lower() == ".png":
            save_atomic(card, og, "PNG", optimize=True)
        else:
            save_atomic(card, og, "JPEG", quality=85, optimize=True, progressive=True)


if __name__ == "__main__":
    main()
