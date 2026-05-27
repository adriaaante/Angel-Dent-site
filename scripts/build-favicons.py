#!/usr/bin/env python3
"""Generates favicons / apple-touch-icon from assets/img/logo.png.

Логотип `logo.png` рисуется белым на фирменном синем фоне (#1e5fb3 =
`--c-primary` и `<meta name="theme-color">`), центрируется и занимает
~78% площади канваса — без прозрачности, чтобы iOS не подкладывал
белые поля под apple-touch-icon.

Запуск из корня репо: `python3 scripts/build-favicons.py`.
"""
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "img" / "logo.png"
OUT_DIR = ROOT / "assets" / "img"

BG = (234, 242, 252, 255)        # #eaf2fc = --c-primary-50
LOGO_FILL = (30, 95, 179, 255)   # #1e5fb3 = --c-primary
LOGO_RATIO = 1.0                 # доля канваса, занимаемая логотипом

SIZES = {
    "favicon-16.png": 16,
    "favicon-32.png": 32,
    "favicon-48.png": 48,
    "favicon-180.png": 180,  # apple-touch-icon
    "favicon-192.png": 192,  # android / PWA
    "favicon-512.png": 512,  # PWA splash
}


def load_logo_mask() -> Image.Image:
    """Возвращает alpha-маску логотипа, тесно обрезанную по bbox.
    Это даёт максимальный размер лого в иконке. Центрирование происходит
    в render() — компенсируем асимметрию (центроид ≠ центр bbox)
    сдвигом при вставке."""
    logo = Image.open(SRC).convert("RGBA")
    alpha = logo.split()[-1]
    bbox = alpha.getbbox()
    return alpha.crop(bbox) if bbox else alpha


def render(size: int, mask_src: Image.Image) -> Image.Image:
    canvas = Image.new("RGBA", (size, size), BG)
    target = int(size * LOGO_RATIO)
    mask = ImageOps.contain(mask_src, (target, target), Image.LANCZOS)
    fg = Image.new("RGBA", mask.size, LOGO_FILL)
    fg.putalpha(mask)
    pos = ((size - mask.width) // 2, (size - mask.height) // 2)
    canvas.alpha_composite(fg, pos)
    return canvas


def main() -> None:
    mask = load_logo_mask()
    for name, size in SIZES.items():
        img = render(size, mask)
        out = OUT_DIR / name
        img.save(out, "PNG", optimize=True)
        print(f"  {name}  {size}x{size}")

    ico_sizes = [16, 32, 48]
    ico_imgs = [render(s, mask).convert("RGBA") for s in ico_sizes]
    ico_imgs[0].save(
        OUT_DIR / "favicon.ico",
        format="ICO",
        sizes=[(s, s) for s in ico_sizes],
        append_images=ico_imgs[1:],
    )
    print("  favicon.ico  16/32/48")


if __name__ == "__main__":
    main()
