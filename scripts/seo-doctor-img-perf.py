#!/usr/bin/env python3
"""Ускорение показа фото врачей: видимые <img> на WebP + правильный loading.

Проблема: портреты грузились рывками — тяжёлый PNG + `loading="lazy"` на
фото над сгибом (герой страницы врача, карточки на «Врачи»). Фикс:
- в видимых <img> меняем `doctors/<slug>.png` → `.webp` (лёгкие, см.
  scripts/doctor-photos-to-webp.py). `og:image`/JSON-LD НЕ трогаем (там нужен png);
- герой на `doctors/<slug>.html` (полный портрет) → `loading="eager"` + `fetchpriority="high"` (это LCP);
- карточки на `doctors/index.html` (над сгибом) → `loading="eager"`;
- карусель на `index.html` (ниже сгиба) — только webp, `lazy` оставляем.

Идемпотентно. Запуск из корня репо:
    python3 scripts/seo-doctor-img-perf.py
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG_TAG = re.compile(r"<img\b[^>]*>", re.I)
SRC_PNG = re.compile(r'src="([^"]*doctors/([a-z-]+)\.png)"')


def set_loading(tag, value):
    if re.search(r'loading="[^"]*"', tag):
        return re.sub(r'loading="[^"]*"', 'loading="%s"' % value, tag)
    return tag[:-1] + ' loading="%s">' % value


def ensure_fetchpriority(tag, value):
    if "fetchpriority=" in tag:
        return re.sub(r'fetchpriority="[^"]*"', 'fetchpriority="%s"' % value, tag)
    return tag[:-1] + ' fetchpriority="%s">' % value


def patch_file(path):
    rel = path.relative_to(ROOT)
    is_doctor_page = rel.parts[0] == "doctors" and rel.name != "index.html"
    is_doctors_index = rel.as_posix() == "doctors/index.html"
    txt = path.read_text(encoding="utf-8")

    def repl(m):
        tag = m.group(0)
        sm = SRC_PNG.search(tag)
        if not sm:
            return tag  # <img> не про фото врача — не трогаем
        src, name = sm.group(1), sm.group(2)
        tag = tag.replace('src="%s"' % src, 'src="%s"' % (src[:-4] + ".webp"))
        is_thumb = name.endswith("-thumb")
        if is_doctor_page and not is_thumb:      # герой = LCP
            tag = set_loading(tag, "eager")
            tag = ensure_fetchpriority(tag, "high")
        elif is_doctors_index:                    # карточки над сгибом
            tag = set_loading(tag, "eager")
        # index.html карусель — ниже сгиба, lazy оставляем (только webp)
        return tag

    new = IMG_TAG.sub(repl, txt)
    if new != txt:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def main():
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        if patch_file(path):
            changed += 1
            print("patched:", path.relative_to(ROOT))
    print("файлов изменено:", changed)


if __name__ == "__main__":
    main()
