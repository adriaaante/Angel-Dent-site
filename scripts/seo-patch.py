#!/usr/bin/env python3
"""Идемпотентные SEO/производительность правки по всем HTML:
1) defer на внешние скрипты main.js / cookies.js / portfolio.js (не трогает inline Метрику);
2) width/height на фото врачей (thumb 256x320, полный портрет 480x600) — против CLS.
Запуск из корня репозитория: python3 scripts/seo-patch.py
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
htmls = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts]

defer_re = re.compile(r'(<script\s+src="[^"]*(?:main|cookies|portfolio)\.js")(\s*></script>)')
def add_defer(m):
    head = m.group(1)
    return head + (m.group(2) if "defer" in head else " defer" + m.group(2))

img_re = re.compile(r'<img\s+(?![^>]*\bwidth=)[^>]*src="[^"]*doctors/[a-z-]+\.(?:png|webp)"[^>]*>')
def add_dims(m):
    tag = m.group(0)
    w, h = (256, 320) if "-thumb." in tag else (480, 600)
    return tag[:4] + f' width="{w}" height="{h}"' + tag[4:]

n_defer = n_img = 0
for p in htmls:
    s = p.read_text(encoding="utf-8")
    s2, c1 = defer_re.subn(add_defer, s)
    s3, c2 = img_re.subn(add_dims, s2)
    if s3 != s:
        p.write_text(s3, encoding="utf-8")
    n_defer += c1; n_img += c2
print(f"defer добавлен: {n_defer} тегов; width/height у фото врачей: {n_img} тегов")
