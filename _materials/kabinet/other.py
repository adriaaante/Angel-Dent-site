# -*- coding: utf-8 -*-
"""
Прочие материалы клиник (печать, документы, наружка) — манифест для хаба.

Кроме кабинета Яндекс.Бизнеса для клиник сделано много «оффлайновых»
вещей: паспорта имплантов, визитки, буклеты, вывески, билборды, прайсы
и юридические документы. Раньше они лежали россыпью по репозиториям, и
владелец каждый раз просил прислать файл. Теперь они на той же странице
(правило владельца 13.08.2026: всё в одном месте) — с превью и
постоянными ссылками на скачивание.

Как это устроено:
- список материалов — `ITEMS` ниже (клиника → карточки);
- превью и сами файлы залиты в постоянное хранилище, ссылки лежат в
  `other_uploads.json` (ключ = путь файла от корня репозитория клиники);
- `python3 other.py` собирает `other.json`, который читает `build-hub.py`.

Добавляешь материал: положить файл в репозиторий клиники → дописать
строку в `ITEMS` → залить файл (`media_upload` → curl PUT →
`media_confirm`) и добавить ссылку в `other_uploads.json` → `python3
other.py` → `python3 build-hub.py`.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = {'angel': 'Angel-Dent-site', 'versal': 'Versal-Dent-site',
        'venecia': 'venecia-dent.ru'}

# клиника → [(заголовок, описание, [превью], [(подпись файла, путь)])]
ITEMS = {
    'angel': [
        ('Паспорт имплантов',
         'Двусторонний A4 с тройным фальцем: пациент уносит данные об установленных '
         'имплантатах, гарантии и памятку по уходу. Печатать без полей, фальцовка на '
         '99,5 и 199 мм от верхнего реза.',
         ['_materials/implant-passport/preview-page-1.png',
          '_materials/implant-passport/preview-page-2.png'],
         [('PDF для типографии', '_materials/implant-passport/Паспорт_имплантов_Ангел-Дент.pdf')]),
        ('QR-код на отзыв в Яндексе',
         'Ведёт на отзывы в карточке клиники. Два варианта: табличка A6 на стойку '
         'ресепшена (печатать на плотной бумаге, ставить в подставку) и чистый код — '
         'для визиток, наклеек и памяток, его можно печатать хоть 2×2 см. Отзывы — '
         'главный рычаг локального ранжирования, поэтому просить их лучше на месте, '
         'пока пациент доволен.',
         ['_materials/qr/qr-otziv-card-preview.jpg', '_materials/qr/qr-otziv-plain.png'],
         [('Табличка A6 (PDF)', '_materials/qr/qr-otziv-card-A6.pdf')]),
        ('Прайс для кабинета',
         'Файл для ручной загрузки в «Товары и услуги». Основной способ — автозагрузка '
         'по ссылке angel-denta.ru/yandex-business.yml, файл нужен как запасной.',
         [], [('XLSX', '_materials/yandex-business/angel-dent-yandex-business-price.xlsx')]),
        ('Документы по продвижению',
         'Договор, счёт и акты между клиникой и исполнителем, плюс выписка из ЕГРЮЛ, '
         'по которой сверены реквизиты. Комплект на каждый месяц: счёт → платёж → акт.',
         [],
         [('Договор № 1547', '_materials/docs/out/Договор № 1547 (продвижение сайтов клиник).docx'),
          ('Счёт № 1547', '_materials/docs/out/Счёт № 1547 от 15.08.2026 (75 000,00).docx'),
          ('Акт № 3', '_materials/docs/out/Акт № 3 от 15.08.2026 (период с 01.05.2026 по 31.07.2026).docx'),
          ('Акт сверки', '_materials/docs/out/Акт сверки взаимных расчётов.docx'),
          ('Выписка ЕГРЮЛ', '_materials/docs/egrul-angel-dent-2026-08-13.pdf')]),
    ],
    'versal': [
        ('QR-код на отзыв в Яндексе',
         'Табличка A6 на стойку ресепшена и чистый код для визиток и наклеек. '
         'Ведёт на отзывы в карточке клиники на Яндекс.Картах.',
         ['_materials/qr/qr-otziv-card-preview.jpg', '_materials/qr/qr-otziv-plain.png'],
         [('Табличка A6 (PDF)', '_materials/qr/qr-otziv-card-A6.pdf')]),
        ('Прайс для кабинета',
         'Для ручной загрузки в «Товары и услуги». Основной способ — автозагрузка по '
         'ссылке versal-dent.ru/yandex-business.yml.',
         [], [('XLSX', '_materials/yandex-business/versal-dent-yandex-business-price.xlsx')]),
    ],
    'venecia': [
        ('QR-код на сайт',
         '⚠️ Карточки с отзывами у «Венеции» ещё нет, поэтому код ведёт на сайт — '
         'на нём цены, врачи и запись. Появится ссылка на отзывы в кабинете — '
         'пришлите, перегенерирую на неё за минуту. Табличка A6 — на стойку, '
         'чистый код — для визиток и наклеек.',
         ['_materials/qr/qr-sait-card-preview.jpg', '_materials/qr/qr-sait-plain.png'],
         [('Табличка A6 (PDF)', '_materials/qr/qr-sait-card-A6.pdf')]),
        ('Паспорт имплантов',
         'Двусторонний A4 с тройным фальцем в стиле «Венеции». Панели неравные — '
         '99,5 + 99,5 + 98 мм, сгибы на 99,5 и 199 мм от верхнего реза (схема от типографии).',
         ['_materials/implant-passport/out/preview-page-1.jpg',
          '_materials/implant-passport/out/preview-page-2.jpg'],
         [('PDF для типографии', '_materials/implant-passport/out/Паспорт_имплантов_Венеция.pdf')]),
        ('Визитки врачей',
         'По визитке на каждого врача плюс общий оборот с контактами и QR. '
         'Печать 90×50 мм с вылетами.',
         ['_materials/vizitki/card-drobkova-front.jpg',
          '_materials/vizitki/card-kilasoniya-front.jpg',
          '_materials/vizitki/card-kendabaeva-front.jpg',
          '_materials/vizitki/card-back.jpg'],
         [('PDF для типографии', '_materials/vizitki/venecia-vizitki-print.pdf')]),
        ('Рекламный буклет A5',
         '⚠️ В буклете свои акционные цены — они действуют только при предъявлении '
         'буклета и могут отличаться от сайта. На каждой стороне дисклеймер и оговорка '
         '«не является публичной офертой».',
         ['_materials/buklet/out/preview-front.jpg',
          '_materials/buklet/out/preview-back.jpg'],
         [('PDF для типографии', '_materials/buklet/out/venecia-buklet-A5-print.pdf')]),
        ('Консольная вывеска-зуб',
         'Фигурный рез по контуру зуба, высота 700 мм, внутри только надпись «ВЕНЕЦИЯ». '
         'Для чёрного фасада взята светлая схема: белое поле с золотой каймой. '
         'Контур реза один на все цветовые схемы.',
         ['_materials/naruzhka/izgotovlenie/venecia-tooth-sign-white-gold-edge-preview.jpg',
          '_materials/naruzhka/izgotovlenie/facade-mockup-white-gold-edge.jpg'],
         [('Макет 1:1 (печать)', '_materials/naruzhka/izgotovlenie/venecia-tooth-sign-white-gold-edge-print.pdf'),
          ('Контур реза', '_materials/naruzhka/izgotovlenie/venecia-tooth-sign-cutline.pdf'),
          ('Чертёж с размерами', '_materials/naruzhka/izgotovlenie/venecia-tooth-sign-drawing.pdf')]),
        ('Билборд 3×6 м',
         'Два варианта: семейный и про улыбку. Полоса с предупреждением о '
         'противопоказаниях занимает больше 5 % площади — этого требует закон о рекламе, '
         'обрезать её нельзя.',
         ['_materials/naruzhka/billboard-family-6x3.jpg',
          '_materials/naruzhka/billboard-smile-6x3.jpg'], []),
        ('Боковая вывеска 60×80 см',
         'Панель на фасад рядом с входом: логотип, название и режим работы.',
         ['_materials/naruzhka/side-sign-60x80.jpg'],
         [('PDF для печати', '_materials/naruzhka/venecia-side-sign-60x80.pdf')]),
        ('Прайс для кабинета',
         'Для ручной загрузки в «Товары и услуги». Основной способ — автозагрузка по '
         'ссылке venecia-dent.ru/yandex-business.yml.',
         [], [('XLSX', '_materials/yandex-business/venecia-dent-yandex-business-price.xlsx')]),
    ],
}


def export():
    up = json.load(open(os.path.join(HERE, 'other_uploads.json'), encoding='utf-8'))
    out, missing = {}, []
    for cid, cards in ITEMS.items():
        rows = []
        for title, about, previews, files in cards:
            key = lambda p: f'{cid}/{p}'
            for p in previews + [f for _, f in files]:
                if key(p) not in up:
                    missing.append(key(p))
            rows.append({
                'title': title, 'about': about,
                'previews': [up[key(p)] for p in previews if key(p) in up],
                'files': [{'label': l, 'url': up[key(p)],
                           'name': os.path.basename(p)}
                          for l, p in files if key(p) in up],
                'path': f'{REPO[cid]}/{(previews or [f for _, f in files] or ["—"])[0].rsplit("/", 1)[0]}',
            })
        out[cid] = rows
    json.dump(out, open(os.path.join(HERE, 'other.json'), 'w'),
              ensure_ascii=False, indent=1)
    for cid, rows in out.items():
        print(f'{cid:8s} карточек {len(rows)}, '
              f'файлов {sum(len(r["files"]) for r in rows)}, '
              f'превью {sum(len(r["previews"]) for r in rows)}')
    if missing:
        print('НЕ ЗАЛИТО:', *missing, sep='\n  ')


if __name__ == '__main__':
    export()
