#!/usr/bin/env python3
"""Отчёт: цены на отбеливание зубов в Реутове (конкуренты vs наши клиники).

Собирает PDF со сравнительной таблицей — каждая строка со ссылкой на
страницу, где эта цена видна своими глазами.

    python3 _materials/analytics/otbelivanie-reutov.py

⚠️ В таблицу попадают ТОЛЬКО цены, которые опубликованы на сайте самой
клиники и проверены открытием страницы. Числа из агрегаторов (ПроДокторов
и т. п.) идут отдельным блоком «контекст» и помечены как данные агрегатора —
клиника за них не отвечает, ссылка ведёт не на её прайс.
"""
from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle)

HERE = Path(__file__).resolve().parent
OUT = HERE / "out" / "Отбеливание-цены-Реутов.pdf"
FONTS = Path("/tmp/claude-0/-home-user/0c942a14-b9d6-5314-9918-7c11e119dac0/scratchpad/fonts")

DATE = "24 августа 2026"

INK = colors.HexColor("#1B2A33")
MUTED = colors.HexColor("#5D6D77")
BLUE = colors.HexColor("#1E5FB3")
LINE = colors.HexColor("#D8E1E8")
OURS_BG = colors.HexColor("#FFF6E0")
OURS_LINE = colors.HexColor("#E3B341")
HEAD_BG = colors.HexColor("#EEF4FA")

# Клиника, адрес, метод, цена, url. Цена — как опубликована на сайте клиники.
ROWS = [
    ("Реутов Клиника", "Ашхабадская, 3", "Amazing White, клиническое", "8 000 ₽",
     "https://reutovclinic.ru/price/"),
    ("Моя Семья", "Реутов", "Opalescence кабинетное, 2 челюсти", "12 500 ₽",
     "https://klinikams.ru/stomatologiya-ceny-reutov/"),
    ("Реутов Клиника", "Ашхабадская, 3", "Flash, клиническое", "16 000 ₽",
     "https://reutovclinic.ru/price/"),
    ("S.E. Dental Clinic", "Носовихинское ш., 17", "Amazing White", "от 16 000 ₽",
     "https://se-dentalclinic.ru/uslugi/profilaktika-i-otbelivanie/otbelivanie-zubov/"),
    ("Моя Семья", "Реутов", "Домашнее в каппах, 2 челюсти", "18 000 ₽",
     "https://klinikams.ru/stomatologiya-ceny-reutov/"),
    ("НАШИ: Ангел-Дент и Версаль", "Победы, 22", "Amazing White, под ключ, 2 челюсти",
     "17 500 ₽ (акция)\n25 000 ₽ базовая", "https://angel-denta.ru/promotions.html"),
    ("Dental Str.25", "Носовихинское ш., 25", "Zoom 4", "35 000 ₽",
     "https://dentalstr25.ru/zoom"),
    ("Бриллиант Дент", "Юбилейный пр., 72", "Zoom 4", "35 000 ₽",
     "https://brilliantdent.ru/uslugi/otbelivanie-zubov-v-reutove/"
     "ceny-na-otbelivanie-zubov-v-reutove/"),
    ("Арти Дент", "Юбилейный пр.", "Zoom 4", "38 000 ₽",
     "https://arti-dent.ru/services/zubnaya-gigiena/otbelivanie-zubov/"),
    ("Моя Семья", "Реутов", "Клиническое за 1 визит, 2 челюсти", "48 000 ₽",
     "https://klinikams.ru/stomatologiya-ceny-reutov/"),
    ("РЕУТДЕНТ", "Реутов", "Zoom 4, Flash, лазерное —\nцену на сайте не публикует",
     "нет цены", "https://reutdent.ru/services/otbelivanie-zubov/"),
]

HYGIENE = [
    ("НАШИ: Ангел-Дент и Версаль", "Комплекс: УЗ + Air Flow + полировка", "5 000 ₽",
     "https://angel-denta.ru/services/gigiena.html"),
    ("Реутов Клиника", "Комплекс: Air Flow + УЗ", "5 000 ₽",
     "https://reutovclinic.ru/price/"),
    ("Моя Семья", "Гигиена Air Flow", "5 300 ₽",
     "https://klinikams.ru/stomatologiya-ceny-reutov/"),
    ("Моя Семья", "Комплексная гигиена (импортные материалы)", "3 750 – 9 400 ₽",
     "https://klinikams.ru/stomatologiya-ceny-reutov/"),
    ("Арти Дент", "Комплекс: УЗ + Air Flow + полировка", "7 000 ₽",
     "https://arti-dent.ru/services/zubnaya-gigiena/otbelivanie-zubov/"),
]


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Onest", str(FONTS / "Onest-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("Onest-Semi", str(FONTS / "Onest-SemiBold.ttf")))
    pdfmetrics.registerFont(TTFont("Onest-Bold", str(FONTS / "Onest-Bold.ttf")))


def styles() -> dict:
    def st(name, **kw):
        base = dict(fontName="Onest", fontSize=9.5, leading=13.5, textColor=INK,
                    alignment=TA_LEFT)
        base.update(kw)
        return ParagraphStyle(name, **base)

    return {
        "h1": st("h1", fontName="Onest-Bold", fontSize=19, leading=23, spaceAfter=3),
        "sub": st("sub", fontSize=10, leading=14, textColor=MUTED, spaceAfter=13),
        "h2": st("h2", fontName="Onest-Bold", fontSize=12.5, leading=16,
                 spaceBefore=13, spaceAfter=6),
        "p": st("p", spaceAfter=5),
        "small": st("small", fontSize=8.3, leading=11.5, textColor=MUTED, spaceAfter=4),
        "cell": st("cell", fontSize=9, leading=12),
        "cellb": st("cellb", fontName="Onest-Semi", fontSize=9, leading=12),
        "cellm": st("cellm", fontSize=8.6, leading=11.5, textColor=MUTED),
        "link": st("link", fontSize=8.6, leading=11.5, textColor=BLUE),
    }


def nbsp(text: str) -> str:
    """Неразрывные пробелы в суммах: иначе «16 000 ₽» рвётся на границе строки
    как «16» / «000 ₽» — та же болячка, что была в прайсе на сайте."""
    text = re.sub(r"(?<=\d) (?=\d{3}\b)", "\u00A0", text)
    return re.sub(r"(?<=\d) (?=₽)", "\u00A0", text)


def link(url: str, s) -> Paragraph:
    return Paragraph(f'<link href="{url}"><u>открыть</u></link>', s["link"])


def price_table(s) -> Table:
    head = ["Клиника", "Адрес", "Метод", "Цена", "Источник"]
    data = [[Paragraph(f"<b>{h}</b>", s["cellb"]) for h in head]]
    ours_at = None
    for i, (clinic, addr, method, price, url) in enumerate(ROWS, start=1):
        ours = clinic.startswith("НАШИ")
        if ours:
            ours_at = i
        data.append([
            Paragraph(clinic, s["cellb"] if ours else s["cell"]),
            Paragraph(addr, s["cellm"]),
            Paragraph(method.replace("\n", "<br/>"), s["cell"]),
            Paragraph(nbsp(price).replace("\n", "<br/>"), s["cellb"] if ours else s["cell"]),
            link(url, s),
        ])
    t = Table(data, colWidths=[37 * mm, 27 * mm, 46 * mm, 31 * mm, 21 * mm],
              repeatRows=1, hAlign="LEFT")
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, BLUE),
        ("GRID", (0, 1), (-1, -1), 0.25, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]
    if ours_at:
        style += [("BACKGROUND", (0, ours_at), (-1, ours_at), OURS_BG),
                  ("BOX", (0, ours_at), (-1, ours_at), 1.0, OURS_LINE)]
    t.setStyle(TableStyle(style))
    return t


def hygiene_table(s) -> Table:
    data = [[Paragraph("<b>Клиника</b>", s["cellb"]),
             Paragraph("<b>Услуга</b>", s["cellb"]),
             Paragraph("<b>Цена</b>", s["cellb"]),
             Paragraph("<b>Источник</b>", s["cellb"])]]
    ours_at = None
    for i, (clinic, service, price, url) in enumerate(HYGIENE, start=1):
        ours = clinic.startswith("НАШИ")
        if ours:
            ours_at = i
        data.append([Paragraph(clinic, s["cellb"] if ours else s["cell"]),
                     Paragraph(service, s["cell"]),
                     Paragraph(nbsp(price), s["cellb"] if ours else s["cell"]),
                     link(url, s)])
    t = Table(data, colWidths=[44 * mm, 64 * mm, 32 * mm, 22 * mm],
              repeatRows=1, hAlign="LEFT")
    style = [("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
             ("LINEBELOW", (0, 0), (-1, 0), 0.8, BLUE),
             ("GRID", (0, 1), (-1, -1), 0.25, LINE),
             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
             ("TOPPADDING", (0, 0), (-1, -1), 5),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
             ("LEFTPADDING", (0, 0), (-1, -1), 6)]
    if ours_at:
        style += [("BACKGROUND", (0, ours_at), (-1, ours_at), OURS_BG),
                  ("BOX", (0, ours_at), (-1, ours_at), 1.0, OURS_LINE)]
    t.setStyle(TableStyle(style))
    return t


def build() -> None:
    register_fonts()
    s = styles()
    OUT.parent.mkdir(parents=True, exist_ok=True)

    doc = BaseDocTemplate(str(OUT), pagesize=A4,
                          leftMargin=17 * mm, rightMargin=17 * mm,
                          topMargin=16 * mm, bottomMargin=16 * mm,
                          title="Отбеливание зубов — цены в Реутове",
                          author="Ангел-Дент · Версаль")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")

    def footer(canvas, d):
        canvas.saveState()
        canvas.setFont("Onest", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(doc.leftMargin, 10 * mm,
                          f"Цены собраны {DATE} с сайтов клиник · "
                          f"«открыть» — кликабельная ссылка на страницу с ценой")
        canvas.drawRightString(A4[0] - doc.rightMargin, 10 * mm, f"стр. {d.page}")
        canvas.restoreState()

    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=footer)])

    P = lambda t, k="p": Paragraph(nbsp(t), s[k])
    story = [
        P("Отбеливание зубов: цены в Реутове", "h1"),
        P(f"Сравнение с ценами «Ангел-Дент» и «Версаль» · данные на {DATE}", "sub"),
        price_table(s),
        Spacer(1, 5),
        P("Все цены в таблице открыты на сайтах самих клиник — ссылка в правой "
          "колонке ведёт на страницу, где эта цифра видна. Цены агрегаторов "
          "(ПроДокторов и подобных) в таблицу не брали: клиники за них не отвечают "
          "и они часто устаревают.", "small"),

        P("Что это значит", "h2"),
        P("Рынок Реутова делится надвое. <b>Zoom 4 и Flash — премиум-полка "
          "35–38 тыс. ₽</b>, всё остальное кабинетное отбеливание — "
          "<b>8–16 тыс. ₽</b>. Мы стоим ровно в разрыве между полками.", "p"),
        P("<b>По своей системе мы самые дорогие в городе.</b> Даже с акцией: "
          "17 500 ₽ против 8 000 ₽ у «Реутов Клиники» и 16 000 ₽ у S.E. Dental — "
          "это тот же Amazing White. Базовая цена 25 000 ₽ вне рынка: за эти "
          "деньги рядом уже подступает Zoom.", "p"),
        P("Наши 17 500 ₽ — это «под ключ»: обе челюсти, защита дёсен, гель и "
          "реминерализация. У конкурентов «от 8 000 ₽» вполне может быть один "
          "сеанс без реминерализации. Но в поиске и на Картах состав никто не "
          "сравнивает — сравнивают число.", "p"),
        P("Для контекста: по данным агрегатора ПроДокторов средняя цена Amazing "
          "White по всей Москве — <b>16 609 ₽</b> (197 клиник), а разброс цен на "
          "отбеливание в Реутове — от 1 450 до 35 000 ₽ (11 клиник). Мы дороже "
          "московской средней, находясь в подмосковном городе.", "p"),
        P('<link href="https://prodoctorov.ru/moskva/uslugi/otbelivanie-zubov-amazing-white/">'
          '<u>Amazing White в Москве — ПроДокторов</u></link>  ·  '
          '<link href="https://prodoctorov.ru/reutov/uslugi/stomatologiya/otbelivanie-zubov/">'
          '<u>Отбеливание в Реутове — ПроДокторов</u></link>', "link"),

        P("Гигиена, для сравнения, стоит правильно", "h2"),
        hygiene_table(s),
        Spacer(1, 4),
        P("Наш комплекс 5 000 ₽ — ровно как у «Реутов Клиники», дешевле Арти Дент "
          "(7 000 ₽) и середины прайса «Моей Семьи». Здесь менять нечего.", "p"),

        P("Что говорит наша статистика", "h2"),
        P("За 60 дней по запросу «отбеливание зубов реутов» у «Ангел-Дента» "
          "<b>242 показа и 1 клик</b>, средняя позиция 8,2.", "p"),
        P("Важная оговорка, чтобы не сделать ложный вывод: такой же нулевой CTR у "
          "нас <b>на всех коммерческих запросах</b> с восьмой позиции — "
          "имплантация 0 кликов из 271 показа, протезирование 1 из 253, лечение "
          "зубов 0 из 208. То есть до цены люди просто не доходят: их "
          "останавливает позиция, а не прайс.", "p"),
        P("<b>И главное, что нашлось попутно: у «Ангел-Дента» и «Версаля» нет "
          "отдельной страницы «Отбеливание зубов».</b> Тема спрятана внутри "
          "страницы гигиены. У всех конкурентов из таблицы такая страница есть — "
          "и они стоят выше нас.", "p"),

        P("Рекомендация", "h2"),
        P("<b>Повышать — нет.</b> Обосновать нечем: у нас нет ни Zoom 4, ни "
          "лазера, а премиальную цену рынок отдаёт именно этим брендам.", "p"),
        P("<b>Снизить до рынка своей системы:</b>", "p"),
        P("— базовая <b>19 900 ₽</b> вместо 25 000 ₽ — ниже Zoom, но верх "
          "коридора кабинетного отбеливания;", "p"),
        P("— акция <b>14 900 ₽</b> вместо 17 500 ₽ — дешевле ближайшего "
          "конкурента по той же системе (S.E. Dental, 16 000 ₽) и объяснимо "
          "дороже «Реутов Клиники», потому что у нас под ключ;", "p"),
        P("— пакет <b>«Гигиена + Amazing White» — 17 900 ₽</b> вместо 19 900 ₽ "
          "порознь. Чистка перед отбеливанием обязательна, её всё равно "
          "оплачивают: реальный чек сегодня 22 500 ₽. Пакет даёт видимую выгоду "
          "2 000 ₽, убирает строку «отбеливание» из прямого сравнения по цене и "
          "роняет наш чек всего на пару тысяч.", "p"),
        P("<b>Но первым делом — отдельная страница «Отбеливание зубов» на обоих "
          "сайтах.</b> Снижение цены на восьмой позиции не даст ничего: её никто "
          "не увидит. Страница вытащит нас в топ-5, и тогда цена начнёт "
          "работать.", "p"),
        Spacer(1, 6),
        P("Правка цен на сайте потянет пересборку YML-фида Яндекс.Бизнеса, "
          "карточек акций и витрины — сайт у нас источник правды для них.", "small"),
    ]
    doc.build(story)
    print(f"{OUT.relative_to(HERE.parent.parent)}  {OUT.stat().st_size // 1024} КБ")


if __name__ == "__main__":
    build()
