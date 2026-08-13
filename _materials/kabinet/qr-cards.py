# -*- coding: utf-8 -*-
"""
QR-коды для клиник: чистый код + фирменная табличка на стойку ресепшена.

Зачем: отзывы на Яндекс.Картах — главный рычаг локального ранжирования,
но пациенты не ищут карточку сами. Табличка у стойки с просьбой оценить
и наведённой камерой решает это за 10 секунд.

Что делает скрипт (для каждой клиники — в её же репозиторий,
`_materials/qr/`):
- `qr-<тема>-plain.png` 1200×1200 — чистый код без оформления. Для
  визиток, наклеек, чеков и памяток: печатать можно хоть 2×2 см.
- `qr-<тема>-card-A6.pdf` + превью .jpg — табличка 105×148 мм, 300 dpi,
  в фирменных цветах клиники. Печатать на плотной бумаге, ставить в
  подставку-тейбл-тент у стойки.

⚠️ QR ведёт на реальную карточку клиники. У «Венеции» карточки с
отзывами ещё нет — для неё сделан QR на сайт; появится ссылка на отзывы
в кабинете Яндекс.Бизнеса → добавить сюда и перегенерировать.

Запуск: python3 qr-cards.py
"""
import os

import qrcode
from qrcode.constants import ERROR_CORRECT_Q
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
FONTS = os.path.join(HERE, 'fonts')

MM = 300 / 25.4                       # 300 dpi
W, H = round(105 * MM), round(148 * MM)   # A6

CLINICS = {
    'angel': dict(
        repo='Angel-Dent-site', logo='assets/img/logo.png',
        bg=(234, 242, 252), ink=(26, 38, 56), accent=(30, 95, 179),
        head='PlayfairDisplay.ttf', body='Manrope[wght].ttf',
        name='АНГЕЛ-ДЕНТ', sub='Стоматология · Реутов',
        codes=[('otziv', 'Оцените нас\nна Яндексе',
                'https://yandex.ru/profile/1155929397/reviews')]),
    'versal': dict(
        repo='Versal-Dent-site', logo='assets/img/logo-mark.png',
        bg=(252, 250, 246), ink=(44, 38, 32), accent=(194, 161, 78),
        head='PlayfairDisplay.ttf', body='Manrope[wght].ttf',
        name='ВЕРСАЛЬ', sub='Стоматология · Реутов',
        codes=[('otziv', 'Оцените нас\nна Яндексе',
                'https://yandex.ru/maps/org/versal/107897418441/reviews/')]),
    'venecia': dict(
        repo='venecia-dent.ru', logo='assets/img/logo.png',
        bg=(247, 250, 248), ink=(19, 41, 42), accent=(15, 110, 102),
        head='Prata-Regular.ttf', body='Onest[wght].ttf',
        name='ВЕНЕЦИЯ', sub='Семейная стоматология · Мытищи',
        # карточки с отзывами ещё нет — ведём на сайт
        codes=[('sait', 'Наш сайт\nи запись онлайн', 'https://venecia-dent.ru/')]),
}

TIP = 'Наведите камеру телефона'
THANKS = 'Ваш отзыв помогает нам становиться лучше'
THANKS_SITE = 'Цены, врачи и запись на приём — на сайте'


def font(name, size, weight=None):
    f = ImageFont.truetype(os.path.join(FONTS, name), size)
    if weight and 'wght' in name:
        f.set_variation_by_axes([weight])
    return f


def qr_image(data, px, dark):
    q = qrcode.QRCode(error_correction=ERROR_CORRECT_Q, box_size=10, border=0)
    q.add_data(data)
    q.make(fit=True)
    im = q.make_image(fill_color=dark, back_color='white').convert('RGB')
    return im.resize((px, px), Image.NEAREST)


def centered(d, y, text, f, fill, line=1.25):
    for part in text.split('\n'):
        w = d.textbbox((0, 0), part, font=f)[2]
        d.text(((W - w) / 2, y), part, font=f, fill=fill)
        y += round(f.size * line)
    return y


def card(c, title, data, thanks):
    im = Image.new('RGB', (W, H), c['bg'])
    d = ImageDraw.Draw(im)

    # тонкая фирменная рамка — табличка не сливается со стойкой
    d.rectangle([round(6 * MM), round(6 * MM), W - round(6 * MM), H - round(6 * MM)],
                outline=c['accent'], width=max(2, round(0.6 * MM)))

    logo = Image.open(os.path.join(ROOT, c['repo'], c['logo'])).convert('RGBA')
    s = round(16 * MM)
    logo = logo.resize((s, s), Image.LANCZOS)
    im.paste(logo, ((W - s) // 2, round(13 * MM)), logo)

    y = round(32 * MM)
    y = centered(d, y, c['name'], font(c['body'], round(4.4 * MM), 700), c['ink'], 1.35)
    centered(d, y, c['sub'], font(c['body'], round(3.1 * MM), 400), c['accent'], 1.4)

    y = round(45 * MM)
    y = centered(d, y, title, font(c['head'], round(7.6 * MM)), c['ink'], 1.28)

    # QR на белой плашке — код читается с любой поверхности
    qs = round(46 * MM)
    pad = round(3.5 * MM)
    plate = Image.new('RGB', (qs + pad * 2, qs + pad * 2), 'white')
    plate.paste(qr_image(data, qs, tuple(c['ink'])), (pad, pad))
    px, py = (W - plate.width) // 2, round(66 * MM)
    d.rectangle([px - 1, py - 1, px + plate.width, py + plate.height],
                outline=c['accent'], width=max(1, round(0.4 * MM)))
    im.paste(plate, (px, py))

    y = py + plate.height + round(7 * MM)
    y = centered(d, y, TIP, font(c['body'], round(3.8 * MM), 600), c['accent'], 1.4)
    centered(d, y + round(1.5 * MM), thanks, font(c['body'], round(3.1 * MM), 400),
             c['ink'], 1.4)
    return im


def build():
    for cid, c in CLINICS.items():
        out = os.path.join(ROOT, c['repo'], '_materials', 'qr')
        os.makedirs(out, exist_ok=True)
        for key, title, data in c['codes']:
            qr_image(data, 1200, tuple(c['ink'])).save(
                os.path.join(out, f'qr-{key}-plain.png'))
            thanks = THANKS if key == 'otziv' else THANKS_SITE
            im = card(c, title, data, thanks)
            im.save(os.path.join(out, f'qr-{key}-card-A6.pdf'), 'PDF',
                    resolution=300)
            im.resize((W // 2, H // 2), Image.LANCZOS).save(
                os.path.join(out, f'qr-{key}-card-preview.jpg'), quality=90)
            print(f'{cid:8s} {key:6s} → {data}')


if __name__ == '__main__':
    build()
