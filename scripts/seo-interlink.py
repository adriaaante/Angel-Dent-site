#!/usr/bin/env python3
"""Идемпотентно добавляет на страницы услуг блок «Полезные статьи» со ссылками
на релевантные статьи блога (перелинковка услуги↔блог, топические кластеры).
Использует существующие CSS-классы .related. Запуск из корня репозитория.

Идемпотентно и ОБНОВЛЯЕМО: старый авто-блок (по `id="articles-title"`)
вырезается и пишется заново — можно расширять MAP и перегонять."""
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent

MAP = {
 "implantaciya": [("skolko-stoit-implantaciya","Сколько стоит имплантация зуба","Из чего складывается цена «под ключ»"),
                  ("implantaciya-ili-most","Имплантация или мост — что выбрать","Сравнение, цены и сроки службы"),
                  ("uxod-posle-implantacii","Уход после имплантации","Памятка по дням и на годы вперёд")],
 "protezirovanie": [("implantaciya-ili-most","Имплантация или мост","Что выбрать в 2026: разбор"),
                    ("viniry-ili-koronki","Виниры или коронки","Когда что уместнее")],
 "viniry": [("viniry-ili-koronki","Виниры или коронки","Что выбрать — с примерами")],
 "hirurgiya": [("ostraya-zubnaya-bol-flyus","Острая боль и флюс — что делать","Первая помощь до приёма"),
               ("zub-mudrosti-udalyat-ili-lechit","Зуб мудрости: удалять или лечить","Разбор хирурга: показания, восстановление")],
 "parodontologiya": [("krovotochat-desny","Кровоточат дёсны при чистке","Причины и что реально помогает")],
 "gigiena": [("krovotochat-desny","Кровоточат дёсны","Почему и как лечить")],
 "terapiya": [("ostraya-zubnaya-bol-flyus","Острая зубная боль и флюс","Что делать до приёма"),
              ("kak-vybrat-stomatologa","Как выбрать стоматолога","Чек-лист из 9 пунктов")],
 "detskaya": [("rebenok-u-stomatologa","Как подготовить ребёнка к визиту","Без страха, с какого возраста")],
}
related_re = re.compile(r'(<section class="related" aria-labelledby="related-title">.*?</section>)', re.S)
# старый авто-блок «Полезные статьи» (для обновления/идемпотентности)
articles_re = re.compile(r'<section class="related" aria-labelledby="articles-title">.*?</section>', re.S)

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
    if not p.exists():
        print("!! страница услуги не найдена:", p.name); continue
    s=p.read_text(encoding="utf-8")
    s=articles_re.sub("", s)  # убрать прежний авто-блок (обновляемость)
    m=related_re.search(s)
    if not m:
        print("!! related-блок не найден:", p.name); continue
    new=s[:m.end()]+block(items)+s[m.end():]
    if new!=p.read_text(encoding="utf-8"):
        p.write_text(new,encoding="utf-8"); n+=1
        print("обновлено:", p.name, f"({len(items)} ссылок)")
print(f"Блок «Полезные статьи» проставлен на {n} страниц услуг")
