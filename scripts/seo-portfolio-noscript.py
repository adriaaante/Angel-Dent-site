#!/usr/bin/env python3
"""
SEO: статический <noscript>-фолбэк портфолио на страницах врачей.

Портфолио «до/после» рендерится только через assets/js/portfolio.js, поэтому
для краулеров без JS работы врача невидимы (минус к E-E-A-T). Скрипт достаёт
данные из portfolio.js (единственный источник правды) через Node и вставляет
идемпотентный <noscript>-блок сразу после <div class="portfolio-grid"
data-portfolio="<slug>"></div> на каждой doctors/<slug>.html.

Блок содержит статический список работ (заголовок + описание + реальные фото
«до/после» с alt) — обычный текст/картинки, которые видит поисковик. При
включённом JS блок не показывается (внутри <noscript>).

Идемпотентно: старый сгенерированный блок (между маркерами) вырезается и
пишется заново. Запускать после правок portfolio.js:
    python3 scripts/seo-portfolio-noscript.py
"""
import json, re, subprocess, sys, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORT_JS = ROOT / "assets/js/portfolio.js"
DOCTORS = ROOT / "doctors"

BEGIN = "<!-- pf-noscript:begin (auto, scripts/seo-portfolio-noscript.py) -->"
END = "<!-- pf-noscript:end -->"

NODE = r"""
global.document = { readyState:'complete', addEventListener(){}, querySelectorAll(){return[]}, getElementById(){return null} };
global.window = {};
require(process.argv[1]);
const p = global.window.AD_PORTFOLIO || global.AD_PORTFOLIO || {};
const out = {};
for (const k of Object.keys(p)) out[k] = p[k].map(c => ({
  title: c.title||'', description: c.description||'',
  before: c.before||'', after: c.after||''
}));
process.stdout.write(JSON.stringify(out));
"""

def esc(s):
    return html.escape(s, quote=True)

def build_block(slug, cases):
    if not cases:
        return ""
    items = []
    for c in cases:
        title = esc(c["title"])
        desc = esc(c["description"])
        imgs = ""
        # только реальные фото (не placeholder) отдаём краулеру
        for src, lbl in ((c["before"], "До"), (c["after"], "После")):
            if src and src != "placeholder":
                imgs += ('<img src="%s" width="1200" height="896" loading="lazy" '
                         'alt="%s — %s лечения" />') % (esc(src), title, lbl)
        li = "<li><h3>%s</h3>" % title
        if desc:
            li += "<p>%s</p>" % desc
        if imgs:
            li += imgs
        li += "</li>"
        items.append(li)
    inner = ("<section class=\"pf-noscript\" aria-label=\"Работы врача — до и после\">"
             "<ul>" + "".join(items) + "</ul></section>")
    return "%s\n<noscript>%s</noscript>\n%s" % (BEGIN, inner, END)

def main():
    raw = subprocess.check_output(["node", "-e", NODE, str(PORT_JS)], cwd=str(ROOT))
    data = json.loads(raw)
    # маркерный блок (со старым содержимым) + опциональный перевод строки
    strip_re = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", re.S)
    changed = 0
    for slug, cases in data.items():
        page = DOCTORS / (slug + ".html")
        if not page.exists():
            print("skip (no page):", slug)
            continue
        txt = page.read_text(encoding="utf-8")
        txt = strip_re.sub("", txt)  # убрать прежний авто-блок
        grid_re = re.compile(
            r'(<div class="portfolio-grid" data-portfolio="' + re.escape(slug) + r'"\s*></div>)')
        m = grid_re.search(txt)
        if not m:
            print("skip (no grid):", slug)
            continue
        block = build_block(slug, cases)
        if not block:
            print("skip (no cases):", slug)
            continue
        new = txt[:m.end()] + "\n" + block + txt[m.end():]
        if new != txt:
            page.write_text(new, encoding="utf-8")
            changed += 1
            print("patched:", slug, "(%d works)" % len(cases))
    print("done, pages changed:", changed)

if __name__ == "__main__":
    main()
