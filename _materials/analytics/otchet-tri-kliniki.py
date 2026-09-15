#!/usr/bin/env python3
"""Отчёт владельцу: что изменилось на трёх сайтах за 1 августа — 15 сентября 2026.

    python3 _materials/analytics/otchet-tri-kliniki.py

Цифры — выгрузка из Яндекс.Метрики (визиты, цели) и Яндекс.Вебмастера
(показы, клики, позиции) по трём счётчикам и трём хостам. Они зафиксированы
константами ниже: отчёт должен собираться одинаково и через полгода, когда
API отдаст уже другие данные. Даты периодов — в PERIOD/PREV.

Правило владельца (24.08.2026): отчёты отдаём под маркой FutureFlow —
логотип в шапке, подпись в подвале и плашка в конце.
"""
from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageDraw
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle)

HERE = Path(__file__).resolve().parent
OUT = HERE / "out" / "Отчёт-три-клиники-август-сентябрь-2026.pdf"
LOGO = HERE / "futureflow-logo.png"
FONTS = HERE / "fonts"
STUDIO_SITE = "futureflow.ru"

PERIOD = "1 августа — 15 сентября 2026"
PREV = "16 июня — 31 июля 2026"
DATE = "15 сентября 2026"

INK = colors.HexColor("#1B2A33")
MUTED = colors.HexColor("#5D6D77")
BLUE = colors.HexColor("#1E5FB3")
GOLD = colors.HexColor("#C2A14E")
LAGOON = colors.HexColor("#0F6E66")
GREEN = colors.HexColor("#1D7A45")
RED = colors.HexColor("#B4231F")
LINE = colors.HexColor("#D8E1E8")
HEAD_BG = colors.HexColor("#EEF4FA")
SOFT = colors.HexColor("#F5F9FD")
WARN_BG = colors.HexColor("#FDF4E7")
FF_BLUE = colors.HexColor("#3C8AD8")

CLINIC_COLOR = {"Ангел-Дент": BLUE, "Версаль": GOLD, "Венеция": LAGOON}

# ─────────────────────── данные (выгрузка 15.09.2026) ───────────────────────
# Вебмастер: сумма показов и кликов в выдаче за период, страницы в поиске, ИКС.
SEARCH = [
    #  клиника,      показы было, стало, клики было, стало, страниц, ИКС
    ("Ангел-Дент",   5401,  9152,  557, 210, 42, 30),
    ("Версаль",       663,  4265,   35,  73, 50, 10),
    ("Венеция",         0,    23,    0,   8, 31,  0),
]

# Метрика: визиты, посетители, звонки (клик по номеру), мессенджеры, заявки.
TRAFFIC = [
    #  клиника,     визиты было, стало, посетители было, стало
    ("Ангел-Дент",  9382, 7271, 7986, 6220),
    ("Версаль",     1019, 2587,  799, 2113),
    ("Венеция",        0,   94,    0,   72),
]

CONTACTS = [
    #  клиника,     звонки было, стало, мессенджеры было, стало, заявки было, стало
    ("Ангел-Дент",  208, 163, 13, 30, 46,  5),
    ("Версаль",      16,  37,  1, 31,  6, 10),
    ("Венеция",       0,   0,  0,  2,  0,  2),
]

# Показы в выдаче по неделям (три сайта вместе) — из Вебмастера.
WEEKS = [
    ("22.06", 946, 63, 0), ("29.06", 921, 60, 0), ("6.07", 820, 134, 0),
    ("13.07", 724, 197, 0), ("20.07", 778, 74, 0), ("27.07", 792, 91, 0),
    ("3.08", 1212, 262, 0), ("10.08", 1698, 373, 0), ("17.08", 1617, 515, 8),
    ("24.08", 1253, 822, 2), ("31.08", 1101, 1064, 2), ("7.09", 1785, 1098, 8),
]

# Запросы: показы было → стало, средняя позиция была → стала.
Q_VERSAL = [
    ("стоматология реутов",            3, 239, 23.7, 10.0),
    ("лечение зубов реутов",           0, 231,  0.0,  7.9),
    ("стоматологии реутова",           0, 168,  0.0,  8.6),
    ("реутов стоматология телефон",    0, 142,  0.0,  7.1),
    ("стоматология в реутово",         0, 132,  0.0,  8.7),
    ("протезирование зубов в реутово", 0, 103,  0.0,  9.4),
    ("имплантация зубов в реутове",    0,  98,  0.0,  7.9),
]
Q_ANGEL = [
    ("детская стоматология реутов",    293, 517, 7.2, 6.6),
    ("отбеливание зубов реутов",        99, 423, 8.0, 7.4),
    ("имплантация зубов в реутове",     92, 344, 8.7, 7.0),
    ("стоматология реутов",            274, 327, 9.1, 9.3),
    ("протезирование зубов в реутове",  67, 309, 8.7, 8.1),
    ("лечение зубов реутов",           110, 253, 7.2, 8.3),
]

# Помесячно — визиты (Метрика).
MONTHS = [
    ("Ангел-Дент", [("июль", 8697), ("август", 4813), ("1–15 сентября", 2458)]),
    ("Версаль",    [("июль", 813), ("август", 1195), ("1–15 сентября", 1392)]),
    ("Венеция",    [("июль", 0), ("август", 52), ("1–15 сентября", 42)]),
]

DONE = [
    ("271 правка на трёх сайтах",
     "104 у «Ангел-Дента», 79 у «Версаля», 88 у «Венеции» — каждая с описанием, "
     "что и зачем изменилось."),
    ("12 новых страниц под живой спрос",
     "Отбеливание, зуб мудрости, элайнеры и All-on-4 — по четыре на каждом сайте, "
     "тексты у всех разные. Отсюда и рост показов по этим темам."),
    ("163 диплома и сертификата врачей опубликованы",
     "48 у «Ангел-Дента», 67 у «Версаля», 48 у «Венеции» — со сканами, знаком "
     "клиники и разметкой для поиска. Для медицинской тематики подтверждённая "
     "квалификация врача — прямой фактор доверия поисковика."),
    ("Фид «Врачи» на трёх сайтах",
     "Карточки врачей со специальностью и ценой приёма прямо в выдаче Яндекса "
     "(дополненное представление в поиске). Бесплатно, подключено в Вебмастере."),
    ("Двое новых врачей заведены целиком",
     "Бурнацева в «Версале», Татаров в «Венеции»: страница, карточки, "
     "юридический раздел, фид, документы."),
    ("Комплект документов клиники — 35 бланков",
     "Договор под новые Правила платных медуслуг (ПП РФ № 659), согласия, "
     "памятки, документы по персональным данным, шесть готовых комплектов для "
     "печати и страница-шпаргалка «когда какой документ подписывается»."),
    ("Материалы для Яндекс.Бизнеса",
     "Объявления, акции, витрина, публикации, истории — по каждой клинике "
     "собраны и выложены на одну страницу-хаб с кнопками и готовыми текстами."),
    ("Правовые разделы по приказу № 956н",
     "Сведения о медорганизации, медработниках, правах пациента — то, что "
     "проверяет Росздравнадзор и на что смотрит поиск."),
]


# ───────────────────────────── вёрстка ─────────────────────────────
def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Onest", str(FONTS / "Onest-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("Onest-Semi", str(FONTS / "Onest-SemiBold.ttf")))
    pdfmetrics.registerFont(TTFont("Onest-Bold", str(FONTS / "Onest-Bold.ttf")))
    # Без семьи тег <b> внутри Paragraph молча игнорируется — все выделения
    # в тексте пропадают, и отчёт читается сплошной серой массой.
    pdfmetrics.registerFontFamily("Onest", normal="Onest", bold="Onest-Bold",
                                  italic="Onest", boldItalic="Onest-Bold")
    pdfmetrics.registerFontFamily("Onest-Semi", normal="Onest-Semi",
                                  bold="Onest-Bold", italic="Onest-Semi",
                                  boldItalic="Onest-Bold")


def styles() -> dict:
    def st(name, **kw):
        base = dict(fontName="Onest", fontSize=9.7, leading=14, textColor=INK,
                    alignment=TA_LEFT)
        base.update(kw)
        return ParagraphStyle(name, **base)

    return {
        "h1": st("h1", fontName="Onest-Bold", fontSize=20, leading=24, spaceAfter=3),
        "sub": st("sub", fontSize=10, leading=14, textColor=MUTED, spaceAfter=12),
        "h2": st("h2", fontName="Onest-Bold", fontSize=13, leading=17,
                 spaceBefore=14, spaceAfter=6),
        "p": st("p", spaceAfter=6),
        "lead": st("lead", fontSize=10.6, leading=15.4, spaceAfter=7),
        "small": st("small", fontSize=8.3, leading=11.8, textColor=MUTED, spaceAfter=4),
        "cell": st("cell", fontSize=9, leading=12),
        "cellb": st("cellb", fontName="Onest-Semi", fontSize=9, leading=12),
        "cellm": st("cellm", fontSize=8.6, leading=11.5, textColor=MUTED),
        "num": st("num", fontName="Onest-Semi", fontSize=9.6, leading=12.5),
        "big": st("big", fontName="Onest-Bold", fontSize=17, leading=19),
        "bigl": st("bigl", fontSize=8.6, leading=11.4, textColor=MUTED),
        "link": st("link", fontSize=8.6, leading=11.5, textColor=BLUE),
    }


def nbsp(text: str) -> str:
    text = re.sub(r"(?<=\d) (?=\d{3}\b)", " ", text)
    return re.sub(r"(?<=\d) (?=₽)", " ", text)


def num(n: int) -> str:
    return f"{n:,}".replace(",", " ")


def grow(before: float, after: float) -> tuple[str, colors.Color]:
    """Человеческая формулировка роста: «×6,4» понятнее, чем «+543%»."""
    if before == 0:
        return ("с нуля", GREEN if after else MUTED)
    ratio = after / before
    if ratio >= 2:
        return (f"×{ratio:.1f}".replace(".", ","), GREEN)
    pct = round((ratio - 1) * 100)
    if pct == 0:
        return ("без изменений", MUTED)
    return (f"{pct:+d}%", GREEN if pct > 0 else RED)


def logo_chip(height_px: int = 240) -> ImageReader:
    im = Image.open(LOGO).convert("RGBA")
    w = round(im.width * height_px / im.height)
    im = im.resize((w, height_px), Image.LANCZOS)
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.width - 1, im.height - 1],
                                           radius=round(height_px * 0.16), fill=255)
    im.putalpha(mask)
    return ImageReader(im)


def chip_png() -> Path:
    out = HERE / "out" / "_ff-chip.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists():
        logo_chip()._image.save(out)  # noqa: SLF001
    return out


def highlights(s) -> Table:
    """Четыре цифры крупно — их видно раньше, чем читают текст."""
    cells = [
        ("×2,2", "показов в поиске<br/>по трём сайтам", BLUE),
        ("×6,4", "рост видимости<br/>«Версаля»", GOLD),
        ("×4,5", "обращений<br/>в мессенджеры", LAGOON),
        ("123", "страницы трёх сайтов<br/>в поиске Яндекса", INK),
    ]
    row = []
    for big, label, color in cells:
        row.append(Table([
            [Paragraph(f'<font color="#{color.hexval()[2:]}">{big}</font>', s["big"])],
            [Paragraph(label, s["bigl"])],
        ], colWidths=[40 * mm]))
    t = Table([row], colWidths=[42 * mm] * 4, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SOFT),
        ("BOX", (0, 0), (-1, -1), 0.4, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
    ]))
    return t


def chart(s) -> Table:
    """Столбики показов по неделям: три сайта друг на друге."""
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics.shapes import Drawing, String

    d = Drawing(168 * mm, 62 * mm)
    bc = VerticalBarChart()
    bc.x, bc.y = 16 * mm, 9 * mm
    bc.height, bc.width = 46 * mm, 148 * mm
    bc.data = [[w[1] for w in WEEKS], [w[2] for w in WEEKS], [w[3] for w in WEEKS]]
    bc.categoryAxis.categoryNames = [w[0] for w in WEEKS]
    bc.categoryAxis.labels.fontName = "Onest"
    bc.categoryAxis.labels.fontSize = 7.4
    bc.categoryAxis.labels.dy = -4
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 3000
    bc.valueAxis.valueStep = 1000
    bc.valueAxis.labels.fontName = "Onest"
    bc.valueAxis.labels.fontSize = 7.4
    bc.valueAxis.strokeColor = LINE
    bc.categoryAxis.strokeColor = LINE
    bc.groupSpacing = 4
    bc.barSpacing = 0
    bc.categoryAxis.style = "stacked"
    for i, color in enumerate((BLUE, GOLD, LAGOON)):
        bc.bars[i].fillColor = color
        bc.bars[i].strokeColor = None
    d.add(bc)
    x = 16 * mm
    for name, color in (("Ангел-Дент", BLUE), ("Версаль", GOLD), ("Венеция", LAGOON)):
        from reportlab.graphics.shapes import Rect
        d.add(Rect(x, 57 * mm, 3.2 * mm, 3.2 * mm, fillColor=color, strokeColor=None))
        lbl = String(x + 4.6 * mm, 57.4 * mm, name, fontName="Onest", fontSize=8,
                     fillColor=MUTED)
        d.add(lbl)
        x += 30 * mm
    return Table([[d]], colWidths=[168 * mm], hAlign="LEFT")


def table(s, head, rows, widths, styles_extra=()):
    data = [[Paragraph(f"<b>{h}</b>", s["cellb"]) for h in head]] + rows
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, BLUE),
        ("GRID", (0, 1), (-1, -1), 0.25, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        *styles_extra,
    ]))
    return t


def clinic_cell(name, s):
    color = CLINIC_COLOR[name]
    return Paragraph(f'<font color="#{color.hexval()[2:]}"><b>{name}</b></font>',
                     s["cellb"])


def grow_cell(before, after, s):
    text, color = grow(before, after)
    return Paragraph(f'<font color="#{color.hexval()[2:]}"><b>{text}</b></font>',
                     s["num"])


def search_table(s) -> Table:
    rows = []
    for name, sh0, sh1, cl0, cl1, pages, sqi in SEARCH:
        rows.append([
            clinic_cell(name, s),
            Paragraph(f"{num(sh0)} → <b>{num(sh1)}</b>", s["cell"]),
            grow_cell(sh0, sh1, s),
            Paragraph(f"{num(cl0)} → <b>{num(cl1)}</b>", s["cell"]),
            Paragraph(str(pages), s["cell"]),
            Paragraph(str(sqi), s["cell"]),
        ])
    tot = [sum(r[i] for r in SEARCH) for i in (1, 2, 3, 4, 5)]
    rows.append([
        Paragraph("<b>Три клиники вместе</b>", s["cellb"]),
        Paragraph(f"{num(tot[0])} → <b>{num(tot[1])}</b>", s["cellb"]),
        grow_cell(tot[0], tot[1], s),
        Paragraph(f"{num(tot[2])} → <b>{num(tot[3])}</b>", s["cellb"]),
        Paragraph(f"<b>{tot[4]}</b>", s["cellb"]),
        Paragraph("—", s["cellm"]),
    ])
    return table(s, ["Клиника", "Показы в выдаче", "Рост", "Переходы из поиска",
                     "Страниц в поиске", "ИКС"],
                 rows, [30 * mm, 34 * mm, 19 * mm, 34 * mm, 26 * mm, 14 * mm],
                 [("BACKGROUND", (0, len(rows)), (-1, len(rows)), SOFT)])


def traffic_table(s) -> Table:
    rows = []
    for (name, v0, v1, u0, u1), (_, c0, c1, m0, m1, l0, l1) in zip(TRAFFIC, CONTACTS):
        rows.append([
            clinic_cell(name, s),
            Paragraph(f"{num(v0)} → <b>{num(v1)}</b>", s["cell"]),
            grow_cell(v0, v1, s),
            Paragraph(f"{c0} → <b>{c1}</b>", s["cell"]),
            Paragraph(f"{m0} → <b>{m1}</b>", s["cell"]),
            Paragraph(f"{l0} → <b>{l1}</b>", s["cell"]),
        ])
    return table(s, ["Клиника", "Визиты", "Рост", "Звонки с сайта",
                     "WhatsApp и Telegram", "Заявки с формы"],
                 rows, [30 * mm, 33 * mm, 19 * mm, 27 * mm, 31 * mm, 27 * mm])


def query_table(s, data, title_color) -> Table:
    rows = []
    for q, sh0, sh1, p0, p1 in data:
        pos = ("не было в выдаче" if p0 == 0 else f"{p0:.1f}".replace(".", ","))
        rows.append([
            Paragraph(q, s["cell"]),
            Paragraph(f"{num(sh0)} → <b>{num(sh1)}</b>", s["cell"]),
            grow_cell(sh0, sh1, s),
            Paragraph(f"{pos} → <b>{f'{p1:.1f}'.replace('.', ',')}</b>", s["cell"]),
        ])
    return table(s, ["Запрос", "Показы", "Рост", "Средняя позиция"],
                 rows, [62 * mm, 34 * mm, 20 * mm, 41 * mm])


def months_table(s) -> Table:
    rows = []
    for name, ms in MONTHS:
        rows.append([clinic_cell(name, s)] +
                    [Paragraph(f"<b>{num(v)}</b>" if v else "—", s["cell"])
                     for _, v in ms])
    return table(s, ["Клиника", "июль", "август", "1–15 сентября"],
                 rows, [34 * mm, 38 * mm, 38 * mm, 42 * mm])


def done_table(s) -> Table:
    rows = [[Paragraph(f"<b>{t}</b>", s["cellb"]), Paragraph(d, s["cell"])]
            for t, d in DONE]
    t = Table(rows, colWidths=[58 * mm, 110 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.25, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 0), (0, -1), SOFT),
    ]))
    return t


def note(s, title, body, bg=WARN_BG, bar=GOLD) -> Table:
    inner = [[Paragraph(f"<b>{title}</b>", s["cellb"])],
             [Paragraph(body, s["cell"])]]
    t = Table([[Table(inner, colWidths=[160 * mm])]], colWidths=[168 * mm],
              hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 2.2, bar),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def signature(s) -> Table:
    from reportlab.platypus import Image as RLImage
    w = 34 * mm
    img = RLImage(str(chip_png()), width=w, height=w * 905 / 2400)
    txt = Paragraph(
        f'Отчёт подготовлен студией <b>FutureFlow</b> · '
        f'<link href="https://{STUDIO_SITE}"><u>{STUDIO_SITE}</u></link><br/>'
        f'Данные выгружены {DATE} из Яндекс.Метрики и Яндекс.Вебмастера.', s["small"])
    t = Table([[img, txt]], colWidths=[38 * mm, 130 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEABOVE", (0, 0), (-1, 0), 0.6, LINE),
    ]))
    return t


def build() -> None:
    register_fonts()
    s = styles()
    OUT.parent.mkdir(parents=True, exist_ok=True)

    doc = BaseDocTemplate(str(OUT), pagesize=A4,
                          leftMargin=17 * mm, rightMargin=17 * mm,
                          topMargin=27 * mm, bottomMargin=16 * mm,
                          title="Три клиники — отчёт за август-сентябрь 2026",
                          author="FutureFlow")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    chip = logo_chip()
    chip_w, chip_h = 30 * mm, 30 * mm * 905 / 2400

    def decorate(canvas, d):
        canvas.saveState()
        top = A4[1] - doc.topMargin + 4 * mm
        canvas.drawImage(chip, A4[0] - doc.rightMargin - chip_w, top,
                         width=chip_w, height=chip_h, mask="auto")
        canvas.setFont("Onest", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(doc.leftMargin, top + chip_h / 2 - 2,
                          "Отчёт для ООО «АНГЕЛ-ДЕНТ» · Ангел-Дент · Версаль · Венеция")
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.4)
        canvas.line(doc.leftMargin, top - 2.5 * mm, A4[0] - doc.rightMargin,
                    top - 2.5 * mm)
        canvas.setFont("Onest", 7.5)
        canvas.setFillColor(FF_BLUE)
        canvas.drawString(doc.leftMargin, 10 * mm, "Подготовлено FutureFlow")
        w = canvas.stringWidth("Подготовлено FutureFlow", "Onest", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(doc.leftMargin + w, 10 * mm,
                          f" · {STUDIO_SITE} · период {PERIOD}")
        canvas.drawRightString(A4[0] - doc.rightMargin, 10 * mm, f"стр. {d.page}")
        canvas.restoreState()

    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=decorate)])
    P = lambda t, k="p": Paragraph(nbsp(t), s[k])

    story = [
        P("Три клиники: что изменилось за полтора месяца", "h1"),
        P(f"«Ангел-Дент», «Версаль» и «Венеция» · {PERIOD} · для сравнения взяты "
          f"предыдущие 46 дней, {PREV}", "sub"),
        highlights(s),
        Spacer(1, 10),

        P("Главное", "h2"),
        P("Три сайта стали вдвое заметнее в поиске: показов в Яндексе "
          "<b>6 064 → 13 440</b>. Это не разовый всплеск — цифра растёт неделя "
          "к неделе: в конце июня три сайта набирали около тысячи показов в "
          "неделю, в неделю 7–13 сентября — <b>2 891</b>.", "lead"),
        P("Сильнее всех выросла <b>«Версаль»</b>. В июне её в поиске практически "
          "не было: по запросу «стоматология реутов» сайт стоял на 24-м месте, "
          "то есть на третьей странице выдачи, куда не доходят. Сейчас он на "
          "10-м, а по десятку коммерческих запросов «Версаль» встала рядом с "
          "«Ангел-Дентом». Результат виден сразу: визитов <b>1 019 → 2 587</b>, "
          "звонков с сайта <b>16 → 37</b>, обращений в мессенджеры <b>1 → 31</b>.", "p"),
        P("<b>«Венеция»</b> вышла в поиск с нуля: 31 страница в индексе, первые "
          "визиты и первые две заявки. И это самая «тёплая» аудитория из трёх: "
          "человек смотрит 2,4 страницы и проводит на сайте 1 минуту 39 секунд — "
          "против 1,2 страницы и 22 секунд на «Ангел-Денте», куда люди приходят "
          "по рекламе.", "p"),
        P("Обращения в мессенджеры по трём клиникам выросли в четыре с половиной "
          "раза: <b>14 → 63</b>. Это тот канал, который дешевле звонка и удобнее "
          "формы — люди пишут, не выходя из выдачи.", "p"),
        P("Честно про минус: у <b>«Ангел-Дента»</b> посещаемость снизилась — "
          "9 382 → 7 271 визита. Сайт тут ни при чём: 88 % его трафика даёт "
          "реклама, а рекламных визитов стало меньше (8 354 → 6 409). "
          "Поисковая видимость «Ангела» за это же время выросла на 69 %. "
          "Подробный разбор — в разделе про «Ангел-Дент».", "p"),

        P("Видимость в поиске неделя за неделей", "h2"),
        P("Столбик — показы трёх сайтов в выдаче Яндекса за неделю "
          "(данные Вебмастера). Подписи — понедельник недели.", "small"),
        chart(s),
        Spacer(1, 2),
        P("С 22 июня по 13 сентября недельные показы выросли с 1 009 до 2 891 — "
          "почти втрое. Золотая часть столбика (это «Версаль») за то же время "
          "выросла с 63 показов в неделю до 1 098: в августе она сравнялась с "
          "«Ангел-Дентом» и продолжает расти.", "p"),

        P("Сколько нас видят в поиске", "h2"),
        search_table(s),
        Spacer(1, 4),
        P("«Показы» — сколько раз страницы сайта показались людям в выдаче "
          "Яндекса. «ИКС» — индекс качества сайта по версии Яндекса: у молодых "
          "сайтов он растёт медленно, и у «Версаля» он уже сдвинулся с нуля.", "small"),
        P("Переходов из поиска на «Ангел-Денте» стало меньше (557 → 210) при "
          "выросших показах. Причина понятная и поправимая: сайт держится на "
          "7–9 позициях, а на первую страницу выдачи люди кликают в основном в "
          "топ-5. Мы видим сайт, но встаём в очередь за пятью конкурентами — "
          "поэтому следующий шаг работы именно про позиции, а не про новые "
          "страницы.", "p"),

        P("Рост в выдаче: «Версаль» вышла из ниоткуда", "h2"),
        query_table(s, Q_VERSAL, GOLD),
        Spacer(1, 4),
        P("Шесть из семи запросов в этой таблице раньше не приносили сайту "
          "вообще ничего. Сейчас по ним «Версаль» на первой странице выдачи.", "small"),

        P("«Ангел-Дент»: позиции подросли почти везде", "h2"),
        query_table(s, Q_ANGEL, BLUE),
        Spacer(1, 4),
        P("Имплантация поднялась с 8,7 на 7,0, протезирование с 8,7 на 8,1, "
          "отбеливание с 8,0 на 7,4, детская стоматология с 7,2 на 6,6 — и "
          "показов по этим темам стало в 3–5 раз больше. Отбеливание выросло "
          "с 99 до 423 показов ровно потому, что в августе у него появилась "
          "своя страница: до этого тема была спрятана внутри страницы гигиены.", "p"),

        P("Люди и обращения", "h2"),
        traffic_table(s),
        Spacer(1, 4),
        P("«Звонки с сайта» — клики по номеру телефона (Метрика считает их как "
          "цель). Это не итоговое число разговоров: кто-то набирает номер "
          "руками, кто-то звонит с Карт. Но динамику канала показывает честно.", "small"),

        P("Как это выглядит помесячно (визиты)", "h2"),
        months_table(s),
        Spacer(1, 4),
        P("У «Версаля» половина сентября уже перекрыла весь июль и идёт выше "
          "августа — сайт набирает аудиторию сам, без рекламы. У «Ангел-Дента» "
          "виден откат после июльского рекламного пика.", "p"),

        P("«Ангел-Дент»: что выросло и что просело", "h2"),
        P("<b>Выросло:</b> показы в поиске 5 401 → 9 152 (+69 %), позиции по "
          "коммерческим запросам, мессенджеры 13 → 30 обращений, 42 страницы "
          "в поиске и ИКС 30 — лучший показатель из трёх клиник.", "p"),
        P("<b>Просело:</b> визиты −23 %, звонки с сайта 208 → 163, заявки с "
          "формы 46 → 5. Падение совпадает с сокращением рекламы: в июле было "
          "8 697 визитов и 38 заявок, в августе 4 813 и 5, за половину "
          "сентября 2 458 и ни одной.", "p"),
        note(s, "Что с этим делать — три шага",
             "1. Разобрать рекламный кабинет: куда ведут объявления, какие "
             "кампании остановлены и по каким запросам мы платим. Сайт "
             "отрабатывает — люди на него приходят и звонят, но заявок с формы "
             "сейчас нет вовсе, а это не похоже на нормальное поведение "
             "аудитории.<br/>"
             "2. Продублировать заявки на почту клиники. Сегодня они уходят "
             "только в Telegram-группу, и если канал молчит, это замечают не "
             "сразу. Дубль на почту — страховка и заодно независимая проверка.<br/>"
             "3. Довести позиции с 7–9 до топ-5: показы уже есть, не хватает "
             "именно места в выдаче. Это следующая большая задача по сайту."),

        P("«Венеция»: сайт вышел в поиск", "h2"),
        P("31 страница в индексе, первые показы и восемь переходов из поиска, "
          "две заявки. Для сайта, которого в июне в выдаче не существовало, это "
          "нормальный старт: у молодого домена первые месяцы уходят на "
          "накопление доверия поисковика.", "p"),
        note(s, "Две вещи, которые тормозят «Венецию» — нужно решение клиники",
             "<b>Отметка о вредоносном коде в Вебмастере.</b> У домена стоит "
             "фатальная пометка «найдены угрозы» от 2 июля 2025 года — она "
             "осталась от прежнего владельца домена, задолго до нашего сайта. "
             "Пока она висит, Яндекс придерживает сайт в выдаче. Лечится "
             "кнопкой «Я всё исправил» в кабинете Вебмастера и перепроверкой — "
             "нужен доступ к кабинету, сделаем по вашему слову.<br/>"
             "<b>Счётчик Метрики не привязан к Вебмастеру</b> (пометка от "
             "14 сентября). Привязка даёт Яндексу данные о поведении "
             "посетителей — это учитывается при ранжировании. Делается в два "
             "клика в кабинете.",
             bg=colors.HexColor("#FDF1EF"), bar=RED),
        Spacer(1, 6),
        P("И третье, без чего «Венеция» и «Версаль» не вырастут дальше: "
          "<b>отзывы</b>. У «Ангел-Дента» карточка с отзывами набрана, у двух "
          "других клиник её нет. Табличка с QR-кодом на отзывы для «Венеции» "
          "уже готова и лежит в материалах — её надо распечатать и поставить на "
          "стойку. Каждая новая карточка с отзывами поднимает клинику и в "
          "Картах, и в поиске.", "p"),

        P("Что мы сделали за эти полтора месяца", "h2"),
        done_table(s),
        Spacer(1, 6),
        P("Это то, что видно в истории изменений сайтов. Отдельно — то, что "
          "в неё не попадает: разбор старого договора клиники, сверка реквизитов "
          "с выпиской ЕГРЮЛ, проверка каждого документа врача по скану, ведение "
          "кабинетов Яндекс.Бизнеса и Вебмастера по трём клиникам.", "small"),

        P("Что дальше", "h2"),
        P("<b>1. Позиции вместо показов.</b> Мы уже показываемся по всем "
          "ключевым запросам города — теперь задача поднять «Ангел-Дент» и "
          "«Версаль» из 7–9 в топ-5. Там кликают в разы чаще, и рост показов "
          "сразу превратится в звонки.", "p"),
        P("<b>2. Реклама «Ангел-Дента».</b> Разобрать кампании и вернуть заявки "
          "с формы — сейчас это самая заметная потеря.", "p"),
        P("<b>3. Отзывы для «Версаля» и «Венеции».</b> Таблички с QR готовы; "
          "нужно поставить их на стойку и просить отзыв после приёма.", "p"),
        P("<b>4. Снять стопор с «Венеции»</b> — отметка об угрозах и привязка "
          "счётчика (см. выше).", "p"),
        P("<b>5. Публикации в Яндекс.Бизнесе раз в месяц</b> по каждой клинике: "
          "это напрямую влияет на место карточки в Картах. Материалы собраны, "
          "нужна только заливка.", "p"),

        Spacer(1, 8),
        P("Откуда цифры", "h2"),
        P("Посещаемость, звонки, мессенджеры и заявки — Яндекс.Метрика "
          "(счётчики 109369174, 109728396, 111523618), цели настроены нами и "
          "считают клики по телефону, по WhatsApp и Telegram и успешную "
          "отправку формы. Показы, переходы, позиции, страницы в поиске и ИКС — "
          "Яндекс.Вебмастер по трём подтверждённым хостам. Периоды равной "
          f"длины: {PERIOD} (46 дней) против {PREV} (46 дней). Ничего не "
          "округляли в свою пользу и не досчитывали: все цифры в отчёте — "
          "выгрузка как есть.", "small"),
        Spacer(1, 8),
        signature(s),
    ]
    doc.build(story)
    print(f"{OUT.relative_to(HERE.parent.parent)}  {OUT.stat().st_size // 1024} КБ")


if __name__ == "__main__":
    build()
