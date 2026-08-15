#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF-версия счёта — тот же макет, что в .docx, но открывается одинаково
ровно везде (владелец смотрит документы с телефона, а мобильные
просмотрщики docx теряют границы и ширину колонок таблиц).

Данные берутся из registry.json тем же путём, что в build-docs.py;
шрифт — Liberation Serif (метрический двойник Times New Roman).

    python3 invoice-pdf.py --no 1547 --date 2026-08-15 \
        --month "август 2026 (с 15 по 31 августа)" --amount 75000
"""
import argparse
import importlib.util
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("bd", ROOT / "build-docs.py")
bd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bd)

FONTS = "/usr/share/fonts/truetype/liberation"
pdfmetrics.registerFont(TTFont("Serif", f"{FONTS}/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-B", f"{FONTS}/LiberationSerif-Bold.ttf"))

GRID = TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.6, "black"),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 2),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
])


def st(size=10, bold=False, align=0, leading=None):
    return ParagraphStyle(
        "s", fontName="Serif-B" if bold else "Serif", fontSize=size,
        leading=leading or size * 1.25, alignment=align)


def build(no, inv_date, amount, month_label, basis="contract", name_override=""):
    cfg = bd.load_cfg()
    ex, cu, c = cfg["executor"], cfg["customer"], cfg["contract"]
    money, words = bd.money, bd.rub_words

    out = ROOT / "out" / (f"Счёт № {no} от {bd.date_dots(inv_date)} "
                          f"({money(amount).replace(chr(160), ' ')}).pdf")
    doc = SimpleDocTemplate(
        str(out), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=1.5 * cm, bottomMargin=1.5 * cm, title=f"Счёт № {no}")

    s9, s10 = st(9), st(10)
    story = []

    bank = Table(
        [[Paragraph(f"Банк получателя: {ex['bank']}", s9), Paragraph("БИК", s9),
          Paragraph(ex["bic"], s9)],
         ["", Paragraph("Сч. №", s9), Paragraph(ex["corr_account"], s9)],
         [Paragraph(f"ИНН {ex['inn']}   ОГРНИП {ex['ogrnip']}<br/>"
                    f"Получатель: {ex['short']}", s9),
          Paragraph("Сч. №", s9), Paragraph(ex["account"], s9)]],
        colWidths=[10 * cm, 2.2 * cm, 5.4 * cm])
    bank.setStyle(GRID)
    bank.setStyle(TableStyle([("SPAN", (0, 0), (0, 1))]))
    story += [bank, Spacer(0, 0.5 * cm)]

    story += [Paragraph(f"Счёт на оплату № {no} от {bd.date_ru(inv_date)}",
                        st(13, bold=True)), Spacer(0, 0.4 * cm)]

    lines = [
        f"Поставщик (Исполнитель): {bd.requisites_line(ex, 'executor')}.",
        f"Покупатель (Заказчик): {bd.requisites_line(cu, 'customer')}.",
    ]
    if basis == "contract":
        lines.append(f"Основание: {bd.contract_ref(cfg)}")
    elif basis:
        lines.append(f"Основание: {basis}")
    for line in lines:
        story += [Paragraph(line, st(10, align=4)), Spacer(0, 0.12 * cm)]
    story += [Spacer(0, 0.3 * cm)]

    # без адресов сайтов и периода — они зафиксированы в договоре
    if name_override:
        name = name_override
    elif basis == "contract":
        name = f"Оплата по договору № {c['no']} от {bd.date_dots(c['date'])} г."
    else:
        name = "Оплата услуг по продвижению"
    items = Table(
        [[Paragraph(h, st(10, bold=True, align=a)) for h, a in
          zip(("№", "Товары (работы, услуги)", "Кол-во", "Ед.", "Цена", "Сумма"),
              (1, 0, 1, 1, 1, 1))],
         [Paragraph("1", st(10, align=1)), Paragraph(name, s10),
          Paragraph("1", st(10, align=1)), Paragraph("усл.", st(10, align=1)),
          Paragraph(money(amount), st(10, align=2)),
          Paragraph(money(amount), st(10, align=2))]],
        colWidths=[1 * cm, 8.4 * cm, 1.6 * cm, 1.4 * cm, 2.6 * cm, 2.6 * cm])
    items.setStyle(GRID)
    story += [items, Spacer(0, 0.4 * cm)]

    story += [
        Paragraph(f"Итого: {money(amount)}", st(10, bold=True, align=2)),
        Paragraph("Без НДС", st(10, align=2)),
        Paragraph(f"Всего к оплате: {money(amount)}", st(10, bold=True, align=2)),
        Spacer(0, 0.35 * cm),
        Paragraph(f"Всего наименований 1, на сумму {money(amount)} руб.", s10),
        Spacer(0, 0.1 * cm),
        Paragraph(f"Всего к оплате: {words(amount)}. Без НДС.", st(10, bold=True)),
        Spacer(0, 1.1 * cm),
        Paragraph("Индивидуальный предприниматель  _______________________  "
                  f"/ {ex['sign_name']} /", s10),
    ]

    # платёжный QR по ГОСТ Р 56042-2014 — после подписи, как у Сферикса
    import tempfile
    tf = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    bd.payment_qr_png(cfg, no, inv_date, amount, tf.name)
    story += [
        Spacer(0, 0.7 * cm),
        Image(tf.name, width=3.6 * cm, height=3.6 * cm, hAlign="LEFT"),
    ]
    doc.build(story)
    print(f"  ✓ {out.relative_to(ROOT)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--no", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--month", default="")
    ap.add_argument("--amount", type=float, required=True)
    ap.add_argument("--basis", default="contract",
                    help='«Основание»: по умолчанию договор; свой текст; "" — не печатать')
    ap.add_argument("--name", default="", help="своё наименование услуги в таблице")
    a = ap.parse_args()
    build(a.no, a.date, a.amount, a.month, basis=a.basis, name_override=a.name)
