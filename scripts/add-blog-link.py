#!/usr/bin/env python3
"""
Add 'Блог' link to nav and footer of pages that don't have it yet.

The nav is split into two layouts in this codebase:
  • root level — uses 'reviews.html' / './' style hrefs
  • nested (services/, doctors/) — uses '../reviews.html' / '../doctors/' style

We detect which prefix to use by inspecting an existing link in the file.

Idempotent. Skips files that already include 'href="(?:\.\./)?blog/"'.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def is_in_blog(path: Path) -> bool:
    return "blog" in path.parts


def nav_blog_link(prefix: str) -> str:
    return f'<a href="{prefix}blog/">Блог</a>'


def footer_blog_li(prefix: str) -> str:
    return f'<li><a href="{prefix}blog/">Блог</a></li>'


def detect_prefix(html: str) -> str:
    """Return '' for root pages, '../' for nested."""
    if 'href="../"' in html or 'href="../services/"' in html:
        return "../"
    return ""


def process(html: str) -> str:
    if re.search(r'href="(?:\.\./)?blog/"', html):
        return html
    prefix = detect_prefix(html)

    # 1) Insert Блог link in nav, right before 'О клинике'.
    nav_link = nav_blog_link(prefix)
    about_pat = re.compile(r'(<a href="(?:\.\./)?about\.html">О клинике</a>)')
    if about_pat.search(html):
        html = about_pat.sub(rf'{nav_link}\1', html, count=1)

    # 2) Insert Блог in the "Клиника" footer list, before "Отзывы".
    footer_li = footer_blog_li(prefix)
    reviews_pat = re.compile(r'(<li><a href="(?:\.\./)?reviews\.html">Отзывы</a></li>)')
    if reviews_pat.search(html):
        html = reviews_pat.sub(rf'{footer_li}\1', html, count=1)

    return html


def main() -> None:
    files = [p for p in ROOT.rglob("*.html") if not is_in_blog(p)]
    changed = 0
    for f in files:
        original = f.read_text(encoding="utf-8")
        updated = process(original)
        if updated != original:
            f.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"  updated {f.relative_to(ROOT)}")
    print(f"\nDone. {changed} / {len(files)} files updated.")


if __name__ == "__main__":
    main()
