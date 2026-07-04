#!/usr/bin/env python3
"""Герой страниц услуг: якорная цена из прайса + ссылка «весь прайс» (#prices).

Зачем: реклама с Карт (geoadv) приводит по запросам с «ценой», а на первом
экране услуги цены не было → отказы 76–79%. Показываем ПЕРВУЮ позицию
таблицы цен этой же страницы (это всегда базовая услуга: консультация,
лечение кариеса, имплант и т.п.), зачёркнутые старые цены <s> отбрасываем.
Идемпотентно: строка заменяется при повторном запуске, якорь не дублируется.
Запуск из корня: python3 scripts/seo-service-price-hero.py"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARK = 'page-hero__prices'

def first_row(html):
    t = re.search(r'<table class="prices-table".*?</table>', html, re.S)
    if not t: return None
    body = re.sub(r'<s\b[^>]*>.*?</s>', '', t.group(0), flags=re.S)  # без старых цен
    r = re.search(r'<tr><td>(.*?)</td>\s*<td[^>]*>(.*?)</td></tr>', body, re.S)
    if not r: return None
    name = re.sub(r'<[^>]+>', '', r.group(1))
    name = name.replace('Акция', '').strip().rstrip('·').strip()
    name = name.split(' (')[0].strip()
    price = re.sub(r'<[^>]+>', '', r.group(2))
    price = re.sub(r'\s+', ' ', price).strip()
    return name, price

changed = 0
for p in sorted((ROOT/'services').glob('*.html')):
    if p.name == 'index.html': continue
    s = p.read_text(encoding='utf-8')
    row = first_row(s)
    if not row:
        print('  пропуск (нет прайса):', p.name); continue
    name, price = row
    if 'id="prices"' not in s:
        s = s.replace('<h2 class="section__title">Цены</h2>',
                      '<h2 class="section__title" id="prices">Цены</h2>', 1)
    line = (f'<p class="{MARK}">{name} — <strong>{price}</strong> · '
            f'<a href="#prices">весь прайс ↓</a></p>')
    s = re.sub(r'<p class="page-hero__prices">.*?</p>', '', s, flags=re.S)
    hero = re.search(r'(<section class="page-hero">.*?)(</div></section>)', s, re.S)
    if not hero:
        print('  пропуск (нет героя):', p.name); continue
    s = s[:hero.end(1)] + line + s[hero.end(1):]
    p.write_text(s, encoding='utf-8'); changed += 1
    print(f'  {p.name}: {name} — {price}')
print('страниц обновлено:', changed)
