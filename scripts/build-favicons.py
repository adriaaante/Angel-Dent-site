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


def load_logo_mask() -> tuple[Image.Image, float, float]:
    """Тесно кропаем лого по bbox + считаем относительное положение
    центроида (центра массы непрозрачных пикселей) внутри маски.
    Этот центроид мы потом ставим в центр иконки — поэтому при заливке
    bbox-а на всю площадь канваса лого визуально стоит посередине.
    Лого асимметричное (крыло справа, тонкий кончик зуба снизу),
    поэтому при максимальном размере низ кончика может слегка обрезаться."""
    logo = Image.open(SRC).convert("RGBA")
    alpha = logo.split()[-1]
    bbox = alpha.getbbox()
    if not bbox:
        return alpha, 0.5, 0.5
    x0, y0, x1, y1 = bbox
    px = alpha.load()
    total = sx = sy = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            v = px[x, y]
            if v > 30:
                sx += x * v
                sy += y * v
                total += v
    cx_rel = (sx / total - x0) / (x1 - x0)
    cy_rel = (sy / total - y0) / (y1 - y0)
    return alpha.crop(bbox), cx_rel, cy_rel


def render(size: int, mask_src: Image.Image, cx_rel: float, cy_rel: float) -> Image.Image:
    canvas = Image.new("RGBA", (size, size), BG)
    target = int(size * LOGO_RATIO)
    mask = ImageOps.contain(mask_src, (target, target), Image.LANCZOS)
    fg = Image.new("RGBA", mask.size, LOGO_FILL)
    fg.putalpha(mask)
    pos = (
        round(size / 2 - cx_rel * mask.width),
        round(size / 2 - cy_rel * mask.height),
    )
    canvas.alpha_composite(fg, pos)
    return canvas


def main() -> None:
    mask, cx_rel, cy_rel = load_logo_mask()
    for name, size in SIZES.items():
        img = render(size, mask, cx_rel, cy_rel)
        out = OUT_DIR / name
        img.save(out, "PNG", optimize=True)
        print(f"  {name}  {size}x{size}")

    ico_sizes = [16, 32, 48]
    ico_imgs = [render(s, mask, cx_rel, cy_rel).convert("RGBA") for s in ico_sizes]
    ico_imgs[0].save(
        OUT_DIR / "favicon.ico",
        format="ICO",
        sizes=[(s, s) for s in ico_sizes],
        append_images=ico_imgs[1:],
    )
    print("  favicon.ico  16/32/48")


if __name__ == "__main__":
    main()
