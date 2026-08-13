# -*- coding: utf-8 -*-
"""
Истории Яндекс.Бизнеса «Ангел-Дент» — перенос с Google Диска на страницу-хаб.

Слайды собраны 16.07.2026 и хранились только на Диске; здесь перезалиты
в постоянное хранилище (`from-drive/_uploads.json`).

⚠️ История «До и После» в линейку НЕ входит: модерация Яндекса отклонила
   клинические фото «до/после» в сторис (проверено 16.07.2026). На сайте
   портфолио можно, в сторис — нет.

Перенесены пока три истории; остальные («Нам доверяют», «Первый визит»,
«Ровные зубы», «Имплантация», «Детям без слёз», «Отбеливание») лежат
в тех же папках Диска и переносятся тем же способом.

Запуск: python3 stories.py  → stories.json
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://angel-denta.ru'

STORIES = [
    ('ist1', 'Не страшно', 'Записаться', '/contacts.html',
     'Страх боли: анестезия, спокойный приём, можно остановиться в любой момент.'),
    ('ist2', 'Цены честно', 'Смотреть цены', '/promotions.html',
     'План лечения с фиксированными ценами, смета до начала работы.'),
    ('ist5', 'Наши врачи', 'Врачи', '/doctors/',
     'Реальные врачи клиники — единственная история, где показываем настоящие лица.'),
]


def export():
    up = {k: url for k, mid, code, url in
          json.load(open(os.path.join(HERE, 'from-drive', '_uploads.json')))}
    items = []
    for pref, name, btn, link, about in STORIES:
        imgs = [up[k] for k in sorted(up) if k.startswith(pref + '-')]
        items.append({'key': pref, 'title': name, 'btn': btn, 'link': SITE + link,
                      'about': about, 'imgs': imgs})
    json.dump({'title': 'Истории (сторис)', 'items': items},
              open(os.path.join(HERE, 'stories.json'), 'w'), ensure_ascii=False, indent=1)
    for it in items:
        print(f"{it['key']}  {it['title']:14s} слайдов {len(it['imgs'])}")


if __name__ == '__main__':
    export()
