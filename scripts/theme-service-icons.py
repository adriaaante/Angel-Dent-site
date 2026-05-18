#!/usr/bin/env python3
"""
Replace abstract SVG icons in service cards with thematic dental icons.

Targets: every <a href="...services/X.html" class="service-card"> on every page —
finds the <svg> inside <span class="service-card__icon"> and replaces it.

Idempotent: skips if icon already contains data-themed="true".
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Common SVG attrs
ATTRS = 'width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" data-themed="true"'

# Reusable tooth shape (centered, fits ~24×24)
TOOTH = ('M9 2.5c-1.7 0-3 1.1-3 3 0 1.9.3 3.7 1 5.6l1.3 4.5c.3.9 1.6.9 1.8 0'
         'L11 12h2l.9 3.6c.2.9 1.5.9 1.8 0l1.3-4.5c.7-1.9 1-3.7 1-5.6 0-1.9-1.3-3-3-3'
         '-.7 0-1.4.4-1.7.8C12 2.9 11.4 2.5 9 2.5z')

ICONS = {
    "implantaciya": (
        f'<svg {ATTRS}>'
        f'<path d="{TOOTH}"/>'
        '<line x1="9" y1="18" x2="15" y2="18"/>'
        '<line x1="10" y1="20" x2="14" y2="20"/>'
        '<line x1="11" y1="22" x2="13" y2="22"/>'
        '</svg>'
    ),
    "ortodontiya": (
        f'<svg {ATTRS}>'
        '<line x1="3" y1="10" x2="21" y2="10"/>'
        '<rect x="5" y="7" width="3" height="6" rx=".6"/>'
        '<rect x="10.5" y="7" width="3" height="6" rx=".6"/>'
        '<rect x="16" y="7" width="3" height="6" rx=".6"/>'
        '<path d="M6.5 13v8M12 13v8M17.5 13v8"/>'
        '</svg>'
    ),
    "terapiya": (
        f'<svg {ATTRS}>'
        f'<path d="{TOOTH}"/>'
        '<circle cx="14" cy="8" r="1.6" fill="currentColor" stroke="none"/>'
        '</svg>'
    ),
    "hirurgiya": (
        f'<svg {ATTRS}>'
        '<path d="M9 4l4 6-2 10-2-1 1-7-3-6z"/>'
        '<path d="M15 4l-4 6 2 10 2-1-1-7 3-6z"/>'
        '<circle cx="9" cy="3.5" r="1"/>'
        '<circle cx="15" cy="3.5" r="1"/>'
        '</svg>'
    ),
    "detskaya": (
        f'<svg {ATTRS}>'
        f'<path d="{TOOTH}"/>'
        '<circle cx="10" cy="7" r=".9" fill="currentColor" stroke="none"/>'
        '<circle cx="14" cy="7" r=".9" fill="currentColor" stroke="none"/>'
        '<path d="M10 9.6c.6.9 1.3 1.3 2 1.3s1.4-.4 2-1.3"/>'
        '</svg>'
    ),
    "protezirovanie": (
        f'<svg {ATTRS}>'
        '<path d="M3.5 13L5 5l3 5 4-7 4 7 3-5 1.5 8"/>'
        '<path d="M3.5 13h17v4.5c0 1.1-.9 2-2 2H5.5c-1.1 0-2-.9-2-2z"/>'
        '<line x1="6" y1="16" x2="18" y2="16"/>'
        '</svg>'
    ),
    "viniry": (
        f'<svg {ATTRS}>'
        '<path d="M5 8c0-1 .9-2 2-2s2 1 2 2v6l-2 5-2-5z"/>'
        '<path d="M10 8c0-1 .9-2 2-2s2 1 2 2v6l-2 5-2-5z"/>'
        '<path d="M15 8c0-1 .9-2 2-2s2 1 2 2v6l-2 5-2-5z"/>'
        '<path d="M20.5 2.5l.4 1.3 1.3.4-1.3.4-.4 1.3-.4-1.3-1.3-.4 1.3-.4z" fill="currentColor" stroke="none"/>'
        '</svg>'
    ),
    "gigiena": (
        f'<svg {ATTRS}>'
        # toothbrush handle + head
        '<rect x="4" y="14" width="11" height="2.5" rx="1" transform="rotate(-22 9.5 15.25)"/>'
        # bristles
        '<line x1="6" y1="9.5" x2="7" y2="13.5"/>'
        '<line x1="8" y1="8.6" x2="9" y2="12.5"/>'
        '<line x1="10" y1="7.8" x2="11" y2="11.7"/>'
        '<line x1="12" y1="7" x2="13" y2="10.8"/>'
        # sparkle
        '<path d="M19 4l.4 1.3 1.3.4-1.3.4-.4 1.3-.4-1.3-1.3-.4 1.3-.4z" fill="currentColor" stroke="none"/>'
        '<path d="M21 11l.3 1 1 .3-1 .3-.3 1-.3-1-1-.3 1-.3z" fill="currentColor" stroke="none"/>'
        '</svg>'
    ),
    "parodontologiya": (
        f'<svg {ATTRS}>'
        # smaller tooth (raised)
        'M9 3c-1.4 0-2.5 1-2.5 2.6 0 1.5.3 3 .8 4.4l1 3.2c.2.7 1.3.7 1.5 0L10.4 11h3.2l.6 2.2c.2.7 1.3.7 1.5 0l1-3.2c.5-1.4.8-2.9.8-4.4C17.5 4 16.4 3 15 3c-.7 0-1.3.3-1.6.7C13 3.3 12.5 3 9 3z" fill="none"/>'
        # gum lines underneath (heart-like wave)
        '<path d="M3 17.5c1.5-1 3-1 4.5 0s3 1 4.5 0 3-1 4.5 0 3 1 4.5 0"/>'
        '<path d="M3 20.5c1.5-1 3-1 4.5 0s3 1 4.5 0 3-1 4.5 0 3 1 4.5 0"/>'
        '</svg>'
    ),
}

# Bug fix: parodontologiya path is malformed (no opening M). Rebuild it cleanly.
ICONS["parodontologiya"] = (
    f'<svg {ATTRS}>'
    '<path d="M9 3c-1.4 0-2.5 1-2.5 2.6 0 1.5.3 3 .8 4.4l1 3.2c.2.7 1.3.7 1.5 0L10.4 11h3.2l.6 2.2c.2.7 1.3.7 1.5 0l1-3.2c.5-1.4.8-2.9.8-4.4C17.5 4 16.4 3 15 3c-.7 0-1.3.3-1.6.7C13 3.3 12.5 3 9 3z"/>'
    '<path d="M3 17.5c1.5-1 3-1 4.5 0s3 1 4.5 0 3-1 4.5 0 3 1 4.5 0"/>'
    '<path d="M3 20.5c1.5-1 3-1 4.5 0s3 1 4.5 0 3-1 4.5 0 3 1 4.5 0"/>'
    '</svg>'
)


def process(html: str) -> tuple[str, int]:
    """Replace icon SVGs inside service-card__icon for service-card links."""
    if 'data-themed="true"' in html and 'class="service-card__icon"' not in html:
        # All cards already themed
        return html, 0

    count = 0

    # Match: <a href="...{slug}.html" class="service-card"> ... <span class="service-card__icon"><svg ...>...</svg></span>
    for slug, new_svg in ICONS.items():
        # Find all service-card anchors for this slug, then replace the icon SVG inside.
        # The pattern is greedy-safe because we scope to the first <svg>...</svg> after the icon span.
        pattern = re.compile(
            r'(<a [^>]*href="[^"]*services/' + re.escape(slug) + r'\.html"[^>]*class="service-card"[^>]*>'
            r'\s*<span class="service-card__icon">)'
            r'<svg\b[^>]*>.*?</svg>',
            re.DOTALL,
        )
        new_html, n = pattern.subn(lambda m: m.group(1) + new_svg, html)
        if n > 0:
            html = new_html
            count += n
    return html, count


def main() -> None:
    files = list(ROOT.rglob("*.html"))
    total = 0
    for f in files:
        original = f.read_text(encoding="utf-8")
        updated, n = process(original)
        if n > 0 and updated != original:
            f.write_text(updated, encoding="utf-8")
            total += n
            print(f"  {f.relative_to(ROOT)}: {n} icon(s) replaced")
    print(f"\nDone. {total} icons replaced.")


if __name__ == "__main__":
    main()
