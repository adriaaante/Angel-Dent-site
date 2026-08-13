# -*- coding: utf-8 -*-
"""
Истории Яндекс.Бизнеса «Ангел-Дент» — данные для страницы-хаба.

Слайды собраны 16.07.2026 и жили только на Google Диске. Ссылки на
картинки постоянные (хранилище Higgsfield):
- ist1/ist2/ist5 — перезалиты из репо, ссылки в `from-drive/_uploads.json`;
- остальные — CDN-ссылки прямо из google-доков историй на Диске
  (в каждом доке лежит порядок слайдов и настройки кабинета).
Копии слайдов на всякий случай сохранены в `from-drive/*.jpg`.

⚠️ История №4 «До и После» в линейку НЕ входит: модерация Яндекса
   отклоняет клинические фото «до/после» в сторис (проверено 16.07.2026).
   На сайте портфолио — можно, в сторис — нет.

Порядок на карточке (свежая история показывается первой → заливать
снизу вверх): Не страшно → Цены честно → Нам доверяют → Ровные зубы →
Имплантация → Детям без слёз → Отбеливание → Наши врачи → Первый визит.

Запуск: python3 stories.py  → stories.json
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://angel-denta.ru'
CDN = 'https://d2ol7oe51mr4n9.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/'

# ключ, название истории (≤15), текст кнопки (≤15), ссылка кнопки,
# о чём история, id слайдов в хранилище ('' = взять из _uploads.json)
STORIES = [
    ('ist1', 'Не страшно', 'Записаться', '/contacts.html',
     'Страх боли: анестезия, спокойный приём, можно остановиться в любой момент.',
     []),
    ('ist2', 'Цены честно', 'Смотреть цены', '/promotions.html',
     'План лечения с фиксированными ценами, смета до начала работы.',
     []),
    ('ist3', 'Нам доверяют', 'Читать отзывы', '/reviews.html',
     'Четыре реальных отзыва с Яндекс.Карт: детский приём, каналы, брекеты, гигиена.',
     ['4023b9dc-7bc7-48be-9d5e-0deea144b367',
      '4a0edebf-2c9c-4baa-9173-c9508c02c46a',
      '9406881d-bc20-4442-b08a-24c3045fd958',
      '3e203a90-6528-4650-a24b-e35228e49249']),
    ('ist7', 'Ровные зубы', 'Записаться', '/services/ortodontiya.html',
     'Брекеты или элайнеры, зачем ровный прикус, консультация ортодонта 0 ₽.',
     ['742f2680-8322-4399-bf60-f334defa1a9f',
      '91a4fe88-4636-4f2a-8e40-c248cee9a84a',
      '1cf41ffb-d9fc-4524-a319-5ca3e851a59e',
      'b58f7328-49c9-487f-ab6e-ccd9e564be40']),
    ('ist8', 'Имплантация', 'Записаться', '/services/implantaciya.html',
     'Как появляется новый зуб, Straumann/Osstem/Dentium, каждый 3-й имплант — 0 ₽.',
     ['7552a654-eb7b-4df0-ab2e-cf0857486eb7',
      '7c870646-0a3f-4a3d-bd9c-a4c6a7d27853',
      '18ccca7b-8787-4ba2-9916-6b1ce92c337d',
      'fbf9f740-7743-4a3e-9ac6-3553ad1233af']),
    ('ist9', 'Детям без слёз', 'Записаться', '/services/detskaya.html',
     'Приём с 2 лет, мультики и игра, цветные пломбы Twinky Star, всё за один визит.',
     ['b1509d16-8490-4a33-8ccf-e52457d7bece',
      '5a55d6e8-3bb9-421b-acf0-6317fb6f5420',
      'a21b395f-f9e9-462a-83ba-3fb873ee52f4',
      '8e28411f-f25e-4061-8fad-790f045426ff']),
    ('ist10', 'Отбеливание', 'Записаться', '/services/gigiena.html',
     'Почему улыбка тускнеет и как вернуть белизну: Amazing White 17 500 ₽ вместо 25 000 ₽.',
     ['b8e165ae-45b2-4173-8e28-bd5ea2a7acd5',
      '22ebd4c8-b4ae-467f-80a5-481263757a47',
      '145ec43b-c3a1-4d58-95c5-49d653d7732a',
      'd8df3236-addb-4c80-9b06-49f7f6c3ffe7']),
    ('ist5', 'Наши врачи', 'Врачи', '/doctors/',
     'Реальные врачи клиники — единственная история, где показываем настоящие лица.',
     []),
    ('ist6', 'Первый визит', 'Записаться', '/contacts.html',
     'Как пройдёт первый приём в три шага, адрес и график — «мы совсем рядом».',
     ['2ae28eb7-36b7-4094-beaf-ec28840b8cfe',
      'dd74f55e-ce6d-4c8a-b37a-1db60726f34d',
      '0c3511f3-5e96-4350-a039-d628a80ceb53',
      '2beb951b-3894-4ee3-8fdd-53e518591dd3']),
]


def export():
    up = {k: url for k, mid, code, url in
          json.load(open(os.path.join(HERE, 'from-drive', '_uploads.json')))}
    items = []
    for pref, name, btn, link, about, ids in STORIES:
        imgs = [CDN + i + '.jpg' for i in ids] or \
               [up[k] for k in sorted(up) if k.startswith(pref + '-')]
        items.append({'key': pref, 'title': name, 'btn': btn, 'link': SITE + link,
                      'about': about, 'imgs': imgs})
    json.dump({'title': 'Истории (сторис)', 'items': items},
              open(os.path.join(HERE, 'stories.json'), 'w'), ensure_ascii=False, indent=1)
    for it in items:
        print(f"{it['key']:6s} {it['title']:14s} слайдов {len(it['imgs'])}")


if __name__ == '__main__':
    export()
