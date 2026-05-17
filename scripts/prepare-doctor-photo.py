#!/usr/bin/env python3
"""Prepare a doctor portrait for the Angel-Dent site.

Steps:
  1. Remove the background with rembg (alpha channel transparency).
  2. Crop to the subject's bounding box plus padding, focusing on the
     upper portion so the face stays centred when cropped to a square.
  3. Produce two PNGs: a 600x600 hero image and a 320x320 thumbnail.

Usage:
    python scripts/prepare-doctor-photo.py <source> <slug>

The output files are written to assets/img/doctors/<slug>.png and
assets/img/doctors/<slug>-thumb.png relative to the repo root.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image
from rembg import remove

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "assets" / "img" / "doctors"


def prepare(src_path: Path, slug: str) -> None:
    raw = Image.open(src_path).convert("RGBA")
    cut = remove(raw)
    if cut.mode != "RGBA":
        cut = cut.convert("RGBA")

    # Bounding box of non-transparent pixels.
    alpha = cut.split()[-1]
    bbox = alpha.getbbox()
    if bbox is None:
        raise SystemExit(f"rembg produced empty alpha for {src_path}")
    left, top, right, bottom = bbox
    subject = cut.crop(bbox)

    w, h = subject.size
    # Build a square canvas that frames the subject from the top
    # (so head/shoulders stay centred). Add a little side padding.
    side_pad = int(0.06 * w)
    square = max(w + 2 * side_pad, int(h * 0.72))
    # Height we keep from the top of the subject equals one square side.
    crop_h = min(h, square)

    canvas = Image.new("RGBA", (square, square), (0, 0, 0, 0))
    paste_x = (square - w) // 2
    # Anchor a touch below the very top so the head has some breathing room.
    top_pad = int(0.02 * square)
    canvas.paste(subject.crop((0, 0, w, crop_h)), (paste_x, top_pad), subject.crop((0, 0, w, crop_h)))

    big = canvas.resize((600, 600), Image.LANCZOS)
    small = canvas.resize((320, 320), Image.LANCZOS)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    big.save(OUT_DIR / f"{slug}.png", optimize=True)
    small.save(OUT_DIR / f"{slug}-thumb.png", optimize=True)
    print(f"wrote {OUT_DIR / f'{slug}.png'} and {OUT_DIR / f'{slug}-thumb.png'}")


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 1
    prepare(Path(argv[1]), argv[2])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
