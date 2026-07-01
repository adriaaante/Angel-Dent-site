#!/usr/bin/env python3
"""Идемпотентно добавляет на страницы услуг блок «Полезные статьи» со ссылками
на релевантные статьи блога (перелинковка услуги↔блог, топические кластеры).
Использует существующие CSS-классы .related. Запуск из корня репозитория."""
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent

MAP = {
 "implantaciya": [("implantaciya-ili-most","Имплантация или мост — что выбрать","Сравнение, цены и сроки службы"),
                  ("uxod-posle-implantacii","Уход после имплантации","Памятка по дням и на годы вперёд")],
 "protezirovanie": [("implantaciya-ili-most","Имплантация или мост","Что выбрать в 2026: разбор"),
                    ("viniry-ili-koronki","Виниры или коронки","Когда что уместнее")],
 "viniry": [("viniry-ili-koronki","Виниры или коронки","Что выбрать — с примерами")],
 "hirurgiya": [("zub-mudrosti-udalyat-ili-lechit","Зуб мудрости: удалять или лечить","Разбор хирурга: показания, восстановление")],
 "parodontologiya": [("krovotochat-desny","Кровоточат дёсны при чистке","Причины и что реально помогает")],
 "gigiena": [("krovotochat-desny","Кровоточат дёсны","Почему и как лечить")],
 "terapiya": [("kak-vybrat-stomatologa","Как выбрать стоматолога","Чек-лист из 9 пунктов")],
}
related_re = re.compile(r'(<section class="related" aria-labelledby="related-title">.*?</section>)', re.S)

def block(items):
    cards="".join(
        f'<a href="../blog/{slug}.html" class="related__card"><div class="related__name">{title} →</div>'
        f'<div class="related__desc">{desc}</div></a>' for slug,title,desc in items)
    return ('<section class="related" aria-labelledby="articles-title"><div class="container">'
            '<h2 class="related__title" id="articles-title">Полезные статьи</h2>'
            f'<div class="related__grid">{cards}</div></div></section>')

n=0
for key,items in MAP.items():
    p=ROOT/"services"/f"{key}.html"
    if not p.exists(): continue
    s=p.read_text(encoding="utf-8")
    if 'id="articles-title"' in s:  # уже добавлено
        continue
    m=related_re.search(s)
    if not m:
        print("!! related-блок не найден:", p.name); continue
    s=s[:m.end()]+block(items)+s[m.end():]
    p.write_text(s,encoding="utf-8"); n+=1
print(f"Блок «Полезные статьи» добавлен на {n} страниц услуг")
