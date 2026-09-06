#!/usr/bin/env python3
"""Единый договор клиники с пациентом → .docx (для правки и печати) + .pdf.

Текст живёт в `contract_text.py` — там же объяснено, почему договор один на
три клиники и что обязательно заполнить перед печатью.

    python3 _materials/dogovor-pacienta/build.py

.docx нужен клинике и юристу — его правят и печатают. .pdf собирается тем же
текстом, чтобы владелец мог посмотреть документ с телефона: там docx теряет
таблицы и отступы (та же причина, что и у счетов в _materials/docs/).
"""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageTemplate,
                                Paragraph, Spacer)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import contract_text as T  # noqa: E402

OUT = HERE / "out"
NAME = "Договор-на-оказание-стоматологических-услуг"
FONTS = Path("/tmp/claude-0/-home-user/0c942a14-b9d6-5314-9918-7c11e119dac0/scratchpad/fonts")

INK = colors.HexColor("#111418")
MUTED = colors.HexColor("#5D6D77")


def placeholders(text: str) -> str:
    """{{...}} — то, что заполняют руками. В обоих форматах показываем одинаково."""
    return text.replace("{{", "___ ").replace("}}", " ___")


# ────────────────────────────── DOCX ──────────────────────────────
def docx_base() -> Document:
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(10.5)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    pf = st.paragraph_format
    pf.space_after = Pt(4)
    pf.line_spacing = 1.08
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Cm(1.6)
        s.left_margin = Cm(2.2)
        s.right_margin = Cm(1.4)
    return doc


def p(doc, text="", bold=False, align="just", size=None, space=None, indent=None):
    par = doc.add_paragraph()
    par.alignment = {"just": WD_ALIGN_PARAGRAPH.JUSTIFY, "left": WD_ALIGN_PARAGRAPH.LEFT,
                     "center": WD_ALIGN_PARAGRAPH.CENTER,
                     "right": WD_ALIGN_PARAGRAPH.RIGHT}[align]
    if space is not None:
        par.paragraph_format.space_after = Pt(space)
    if indent is not None:
        par.paragraph_format.left_indent = Cm(indent)
    run = par.add_run(placeholders(text))
    run.bold = bold
    if size:
        run.font.size = Pt(size)
    return par


def build_docx() -> Path:
    doc = docx_base()
    for line in T.TITLE.split("\n"):
        p(doc, line, bold=True, align="center", size=12.5, space=2)
    p(doc, "", space=2)
    p(doc, "г. ____________________                    «____» ______________ 20___ г.",
      align="left", space=8)

    for block in T.PREAMBLE:
        p(doc, block)

    p(doc, "", space=2)
    p(doc, T.PLACE_BLOCK_TITLE, bold=True, align="left", space=2)
    for name, addr, phone in T.CLINICS:
        p(doc, f"[   ]  Стоматология {name} — {addr}, тел. {phone}", align="left",
          space=1, indent=0.6)
    p(doc, T.PLACE_NOTE, size=9, space=8)

    for title, items in T.SECTIONS:
        p(doc, title, bold=True, align="left", space=3)
        for num, text in items:
            p(doc, f"{num} {text}")
        p(doc, "", space=2)

    p(doc, "14. Приложения", bold=True, align="left", space=3)
    for a in T.APPENDICES:
        p(doc, a, align="left", space=1, indent=0.4)
    p(doc, "", space=6)

    p(doc, T.CONSENTS_TITLE, bold=True, align="left", space=3)
    for c in T.CONSENTS:
        p(doc, f"[   ] Согласен(на)    [   ] Не согласен(на)    —    {c}", space=3, indent=0.4)
    p(doc, "", space=6)

    p(doc, "15. Реквизиты и подписи Сторон", bold=True, align="left", space=4)
    p(doc, "ИСПОЛНИТЕЛЬ", bold=True, align="left", space=2)
    c = T.COMPANY
    for line in (
        c["full"],
        f"Место нахождения и фактический адрес: {c['address']}",
        f"ОГРН {c['ogrn']}   ИНН {c['inn']}   КПП {c['kpp']}",
        "Расчётный счёт ____________________ в ____________________",
        "Корреспондентский счёт ____________________   БИК ____________________",
        f"Телефон {c['phone']}   Электронная почта ____________________",
        f"Лицензия № {c['license']} (бессрочно)",
    ):
        p(doc, line, align="left", space=1)
    p(doc, "", space=4)
    p(doc, "_______________ / ________________________   М. П.", align="left", space=10)

    p(doc, "ЗАКАЗЧИК", bold=True, align="left", space=2)
    for line in ("Ф. И. О. ______________________________________________",
                 "Дата рождения ____________________",
                 "Паспорт: серия ______ № ______________ выдан ____________________",
                 "________________________________ дата выдачи ____________________",
                 "Адрес регистрации ____________________________________________",
                 "Почтовый адрес ______________________________________________",
                 "Телефон ____________________   Электронная почта ______________"):
        p(doc, line, align="left", space=1)
    p(doc, "", space=4)
    p(doc, "_______________ / ________________________", align="left", space=10)

    p(doc, "ПАЦИЕНТ (заполняется, если Пациент и Заказчик — разные лица)",
      bold=True, align="left", space=2)
    for line in ("Ф. И. О. ______________________________________________",
                 "Дата рождения ____________________",
                 "Адрес регистрации ____________________________________________",
                 "Телефон ____________________",
                 "Заказчик приходится Пациенту ____________________ "
                 "(родитель, опекун, попечитель, иное)"):
        p(doc, line, align="left", space=1)
    p(doc, "", space=4)
    p(doc, "_______________ / ________________________", align="left", space=2)
    p(doc, "За Пациента, не достигшего 15 лет, Договор подписывает законный "
           "представитель (ст. 54 Федерального закона № 323-ФЗ).", size=9, align="left")

    path = OUT / f"{NAME}.docx"
    doc.save(path)
    return path


# ────────────────────────────── PDF ──────────────────────────────
def pdf_styles() -> dict:
    pdfmetrics.registerFont(TTFont("Onest", str(FONTS / "Onest-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("Onest-Bold", str(FONTS / "Onest-Bold.ttf")))

    def st(name, **kw):
        base = dict(fontName="Onest", fontSize=8.8, leading=12.2, textColor=INK,
                    alignment=TA_JUSTIFY)
        base.update(kw)
        return ParagraphStyle(name, **base)

    return {
        "title": st("title", fontName="Onest-Bold", fontSize=13, leading=17,
                    alignment=TA_CENTER, spaceAfter=2),
        "meta": st("meta", alignment=TA_LEFT, spaceAfter=8),
        "h": st("h", fontName="Onest-Bold", fontSize=10, leading=13.5,
                alignment=TA_LEFT, spaceBefore=8, spaceAfter=3),
        "p": st("p", spaceAfter=3.5),
        "li": st("li", alignment=TA_LEFT, spaceAfter=2, leftIndent=10),
        "small": st("small", fontSize=7.8, leading=10.5, textColor=MUTED, spaceAfter=4),
        "sign": st("sign", alignment=TA_LEFT, spaceAfter=2),
    }


def build_pdf() -> Path:
    s = pdf_styles()
    path = OUT / f"{NAME}.pdf"
    doc = BaseDocTemplate(str(path), pagesize=A4,
                          leftMargin=20 * mm, rightMargin=14 * mm,
                          topMargin=15 * mm, bottomMargin=15 * mm,
                          title="Договор на оказание стоматологических услуг",
                          author=T.COMPANY["short"])
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")

    def decorate(canvas, d):
        canvas.saveState()
        canvas.setFont("Onest", 7)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(A4[0] - doc.rightMargin, 9 * mm, f"стр. {d.page}")
        canvas.restoreState()

    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=decorate)])

    P = lambda t, k="p": Paragraph(placeholders(t), s[k])
    story = []
    for line in T.TITLE.split("\n"):
        story.append(P(line, "title"))
    story.append(Spacer(1, 4))
    story.append(P("г. ____________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                   "«____» ______________ 20___ г.", "meta"))
    for block in T.PREAMBLE:
        story.append(P(block))

    story.append(P(T.PLACE_BLOCK_TITLE, "h"))
    for name, addr, phone in T.CLINICS:
        story.append(P(f"[&nbsp;&nbsp;&nbsp;]&nbsp; Стоматология {name} — {addr}, тел. {phone}", "li"))
    story.append(P(T.PLACE_NOTE, "small"))

    for title, items in T.SECTIONS:
        block = [P(title, "h")] + [P(f"{n} {t}") for n, t in items]
        story.append(KeepTogether(block) if len(items) <= 4 else block[0])
        if len(items) > 4:
            story.extend(block[1:])

    story.append(P("14. Приложения", "h"))
    for a in T.APPENDICES:
        story.append(P(a, "li"))

    story.append(P(T.CONSENTS_TITLE, "h"))
    for c in T.CONSENTS:
        story.append(P(f"[&nbsp;&nbsp;&nbsp;] Согласен(на)&nbsp;&nbsp;&nbsp; [&nbsp;&nbsp;&nbsp;] Не согласен(на)&nbsp;&nbsp;—&nbsp;&nbsp;{c}", "li"))

    story.append(P("15. Реквизиты и подписи Сторон", "h"))
    c = T.COMPANY
    for line in ("<b>ИСПОЛНИТЕЛЬ</b>", c["full"],
                 f"Место нахождения и фактический адрес: {c['address']}",
                 f"ОГРН {c['ogrn']} · ИНН {c['inn']} · КПП {c['kpp']}",
                 "Расчётный счёт ____________________ в ____________________",
                 "Корреспондентский счёт ____________________ · БИК ______________",
                 f"Телефон {c['phone']} · Электронная почта ____________________",
                 f"Лицензия № {c['license']} (бессрочно)", "",
                 "_______________ / ________________________&nbsp;&nbsp; М. П.", "",
                 "<b>ЗАКАЗЧИК</b>",
                 "Ф. И. О. ______________________________________________",
                 "Дата рождения ____________________",
                 "Паспорт: серия ______ № ______________ выдан ____________________",
                 "Адрес регистрации ____________________________________________",
                 "Телефон ____________________ · Электронная почта ______________", "",
                 "_______________ / ________________________", "",
                 "<b>ПАЦИЕНТ</b> (если Пациент и Заказчик — разные лица)",
                 "Ф. И. О. ______________________________________________",
                 "Дата рождения ____________________",
                 "Адрес регистрации ____________________________________________",
                 "Телефон ____________________",
                 "Заказчик приходится Пациенту ____________________", "",
                 "_______________ / ________________________"):
        story.append(P(line or "&nbsp;", "sign"))
    story.append(P("За Пациента, не достигшего 15 лет, Договор подписывает законный "
                   "представитель (ст. 54 Федерального закона № 323-ФЗ).", "small"))

    doc.build(story)
    return path


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    d = build_docx()
    f = build_pdf()
    for x in (d, f):
        print(f"  ✓ {x.relative_to(HERE.parent.parent)}  ({x.stat().st_size // 1024} КБ)")
    print("\n  ⚠️ Перед печатью обязательно заполнить:")
    for t in T.TODO:
        print(f"     — {t}")


if __name__ == "__main__":
    main()
