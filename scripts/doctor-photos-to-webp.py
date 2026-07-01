#!/usr/bin/env python3
"""Генерация WebP-версий портретов врачей из PNG (ускорение загрузки).

PNG-портреты (~210 КБ полный / ~70 КБ миниатюра) тяжёлые — фото «доезжает»
рывками. WebP того же кадра в ~5 раз легче. Скрипт делает `<slug>.webp` и
`<slug>-thumb.webp` рядом с PNG. Видимые `<img>` ссылаются на WebP; PNG
оставляем для `og:image`/JSON-LD (мессенджеры/схема любят png/jpg).

Идемпотентно: просто перегенерит webp из png. Запуск из корня репо:
    python3 scripts/doctor-photos-to-webp.py
"""
import pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIR = ROOT / "assets/img/doctors"
QUALITY = 82  # визуально без потерь для портрета, кратно легче png

def main():
    pngs = sorted(DIR.glob("*.png"))
    if not pngs:
        print("PNG-портретов не найдено:", DIR); return
    total_png = total_webp = 0
    for p in pngs:
        out = p.with_suffix(".webp")
        im = Image.open(p).convert("RGBA")
        im.save(out, "WEBP", quality=QUALITY, method=6)
        pk, wk = p.stat().st_size, out.stat().st_size
        total_png += pk; total_webp += wk
        print(f"  {p.name:28} {pk//1024:4} КБ → {out.name:28} {wk//1024:4} КБ")
    print(f"итого: {total_png//1024} КБ png → {total_webp//1024} КБ webp "
          f"(−{100*(total_png-total_webp)//total_png}%)")

if __name__ == "__main__":
    main()
