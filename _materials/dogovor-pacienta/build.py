#!/usr/bin/env python3
"""Договор клиники с пациентом → .docx (один файл, его правят и печатают).

Текст и реквизиты живут в `contract_text.py`: там же сказано, что поменять,
чтобы собрать бланк для «Версаля» или «Венеции» (юрлицо и лицензия общие —
различаются только адрес места оказания услуг, телефон и почта).

    python3 _materials/dogovor-pacienta/build.py          # docx
    python3 _materials/dogovor-pacienta/build.py --pdf    # + pdf для телефона

Вёрстка живёт только в .docx; pdf получается конвертацией того же файла
(LibreOffice), поэтому форматы не расходятся.
"""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import contract_text as T  # noqa: E402

OUT = HERE / "out"
NAME = "Договор-на-оказание-стоматологических-услуг"
def placeholders(text: str) -> str:
    """{{...}} — то, что заполняют руками. В обоих форматах показываем одинаково."""
    return text.replace("{{", "___ ").replace("}}", " ___")


# ────────────────────────────── DOCX ──────────────────────────────
# Вёрстка «как у юриста»: поля под подшивку, висячий отступ у номеров пунктов,
# заголовки не отрываются от текста, таблицы для мест оказания, согласий и
# подписей, в колонтитуле — номер страницы и подписи сторон (защита от
# подмены листа).
BODY_FONT = "Times New Roman"
BODY_SIZE = 10.5


def _set_font(run, size=None, bold=False, italic=False):
    run.font.name = BODY_FONT
    run.font.size = Pt(size or BODY_SIZE)
    run.bold = bold
    run.italic = italic
    run._element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)


def docx_base() -> Document:
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = BODY_FONT
    st.font.size = Pt(BODY_SIZE)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
    pf = st.paragraph_format
    pf.space_after = Pt(3)
    pf.line_spacing = 1.1
    for s in doc.sections:
        s.top_margin = Cm(1.8)
        s.bottom_margin = Cm(1.6)
        s.left_margin = Cm(2.0)      # поле под подшивку, но без «канцелярских» полей
        s.right_margin = Cm(1.5)
    return doc


def p(doc, text="", bold=False, align="just", size=None, space=None, indent=None,
      first_line=None, keep_with_next=False, italic=False):
    par = doc.add_paragraph()
    par.alignment = {"just": WD_ALIGN_PARAGRAPH.JUSTIFY, "left": WD_ALIGN_PARAGRAPH.LEFT,
                     "center": WD_ALIGN_PARAGRAPH.CENTER,
                     "right": WD_ALIGN_PARAGRAPH.RIGHT}[align]
    pf = par.paragraph_format
    if space is not None:
        pf.space_after = Pt(space)
    if indent is not None:
        pf.left_indent = Cm(indent)
    if first_line is not None:
        pf.first_line_indent = Cm(first_line)
    pf.keep_with_next = keep_with_next
    _set_font(par.add_run(placeholders(text)), size, bold, italic)
    return par


def clause(doc, num: str, text: str):
    """Пункт договора: номер висит слева, текст выровнен по общей левой кромке."""
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = par.paragraph_format
    pf.left_indent = Cm(0.9)
    pf.first_line_indent = Cm(-0.9)   # висячий отступ: номер слева, текст ровной кромкой
    pf.space_after = Pt(3)
    _set_font(par.add_run(f"{num}\t"), bold=True)
    _set_font(par.add_run(placeholders(text)))
    par.paragraph_format.tab_stops.add_tab_stop(Cm(0.9))
    return par


def borderless(table):
    tbl = table._tbl
    borders = tbl.makeelement(qn("w:tblBorders"), {})
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = tbl.makeelement(qn(f"w:{edge}"), {qn("w:val"): "none", qn("w:sz"): "0"})
        borders.append(el)
    tbl.tblPr.append(borders)
    return table


def set_widths(table, widths_cm):
    """python-docx ширину берёт с ячеек — ставим и на них, и на колонки."""
    table.autofit = False
    for row in table.rows:
        row.cant_split = True
        for cell, w in zip(row.cells, widths_cm):
            cell.width = Cm(w)
    for col, w in zip(table.columns, widths_cm):
        col.width = Cm(w)
    return table


def cell_text(cell, lines, bold_first=False, size=None):
    cell.text = ""
    for i, line in enumerate(lines):
        par = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.LEFT
        par.paragraph_format.space_after = Pt(1)
        _set_font(par.add_run(placeholders(line)), size, bold=bold_first and i == 0)


def add_footer(doc):
    """Только номер страницы: подписи сторон — в разделе 15 (решение владельца)."""
    from docx.oxml import OxmlElement
    footer = doc.sections[0].footer
    par = footer.paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.space_before = Pt(2)
    _set_font(par.add_run("Договор на оказание платных медицинских (стоматологических) "
                          "услуг · страница "), 8)
    for tag, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag:
            el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), tag)
        else:
            el = OxmlElement("w:instrText"); el.set(qn("xml:space"), "preserve")
            el.text = " PAGE "
        run = par.add_run(); _set_font(run, 8); run._r.append(el)
    _set_font(par.add_run(" из "), 8)
    for tag, txt in (("begin", None), (None, "NUMPAGES"), ("end", None)):
        if tag:
            el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), tag)
        else:
            el = OxmlElement("w:instrText"); el.set(qn("xml:space"), "preserve")
            el.text = " NUMPAGES "
        run = par.add_run(); _set_font(run, 8); run._r.append(el)


def form_table(doc, rows, label_w=5.2, total_w=17.0, tall=frozenset(),
               extra_tall=frozenset()):
    """Таблица «подпись поля | значение» с тонкой сеткой.

    Пустое значение — клетка под рукописное заполнение; строки из `tall`
    выше (Ф. И. О., адрес, подпись), остальные компактные.
    """
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml import OxmlElement
    from docx.shared import RGBColor
    table = doc.add_table(rows=len(rows), cols=2)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    set_widths(table, [label_w, total_w - label_w])
    # тонкая серая сетка вместо чёрной по умолчанию
    borders = table._tbl.tblPr.find(qn("w:tblBorders"))
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        table._tbl.tblPr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = borders.find(qn(f"w:{edge}"))
        if el is None:
            el = OxmlElement(f"w:{edge}")
            borders.append(el)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:color"), "A6A6A6")
    for row, (label, value) in zip(table.rows, rows):
        row.height = Cm(1.1 if label in extra_tall else 0.85 if label in tall else 0.58)
        lc, vc = row.cells
        lc.text = ""
        par = lc.paragraphs[0]
        par.paragraph_format.space_after = Pt(0)
        run = par.add_run(label)
        _set_font(run, 9)
        run.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
        vc.text = ""
        par = vc.paragraphs[0]
        par.paragraph_format.space_after = Pt(0)
        _set_font(par.add_run(placeholders(value)))
        for cell in (lc, vc):
            cell.vertical_alignment = 1  # WD_ALIGN_VERTICAL.CENTER
    return table


def build_docx() -> Path:
    doc = docx_base()
    add_footer(doc)

    for line in T.TITLE.split("\n"):
        p(doc, line, bold=True, align="center", size=12.5, space=2, keep_with_next=True)
    p(doc, "", space=4)

    # Город слева, дата справа — одной строкой через таблицу без границ.
    head = borderless(doc.add_table(rows=1, cols=2))
    head.autofit = True
    cell_text(head.rows[0].cells[0], [T.CLINIC["city"]])
    par = head.rows[0].cells[1].paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    _set_font(par.add_run("«____» ______________ 20___ г."))
    p(doc, "", space=6)

    for block in T.PREAMBLE:
        p(doc, block, first_line=0.75)

    p(doc, "", space=2)
    p(doc, T.PLACE_LINE, space=8)

    for title, items in T.SECTIONS:
        p(doc, title, bold=True, align="left", space=3, size=11, keep_with_next=True)
        for num, text in items:
            clause(doc, num, text)
        p(doc, "", space=2)

    p(doc, "14. Приложения", bold=True, align="left", size=11, space=3,
      keep_with_next=True)
    for a in T.APPENDICES:
        p(doc, a, align="left", space=1, indent=0.9, first_line=-0.5)
    p(doc, "", space=6)

    p(doc, T.CONSENTS_TITLE, bold=True, align="left", space=3, size=11,
      keep_with_next=True)
    cons = set_widths(borderless(doc.add_table(rows=len(T.CONSENTS), cols=2)),
                      [4.4, 12.6])
    for row, c in zip(cons.rows, T.CONSENTS):
        cell_text(row.cells[0], ["[   ] Согласен(на)", "[   ] Не согласен(на)"])
        cell_text(row.cells[1], [c])
    p(doc, "", space=8)

    # ── Реквизиты и подписи: отдельным листом, таблицами-формами ───────────
    # Подчёркивания в две колонки в Word «плывут» — владелец попросил чистые
    # таблицы: слева подпись поля, справа значение или пустая клетка под руку.
    doc.add_page_break()
    p(doc, "15. Реквизиты и подписи Сторон", bold=True, align="left", size=11,
      space=6, keep_with_next=True)

    c, b, sg, cl = T.COMPANY, T.BANK, T.SIGNATORY, T.CLINIC
    p(doc, "ИСПОЛНИТЕЛЬ", bold=True, align="left", space=3, keep_with_next=True)
    form_table(doc, [
        ("Наименование", c["full"]),
        ("Место нахождения", c["address"]),
        ("Место оказания услуг", cl["address"]),
        ("ОГРН / ИНН / КПП", f"{c['ogrn']} / {c['inn']} / {c['kpp']}"),
        ("Лицензия", f"№ {c['license']}, предоставлена бессрочно"),
        ("Банк", f"{b['bank']}, БИК {b['bik']}"),
        ("Расчётный счёт", b["account"]),
        ("Корреспондентский счёт", b["corr"]),
        ("Телефон, почта, сайт", f"{cl['phone']} · {cl['email']} · {cl['site']}"),
        ("Подпись", f"{sg['short_position']}  __________________  "
                    f"/ {sg['short_name']}      М. П."),
    ], tall={"Подпись"})
    p(doc, "", space=8)

    p(doc, "ПАЦИЕНТ", bold=True, align="left", space=3, keep_with_next=True)
    form_table(doc, [
        ("Фамилия, имя, отчество", ""),
        ("Дата рождения", ""),
        ("Паспорт: серия, номер", ""),
        ("Кем и когда выдан", ""),
        ("Адрес места жительства", ""),
        ("Телефон", ""),
        ("Электронная почта", ""),
        ("Подпись. Экземпляр Договора получен; с его условиями, прейскурантом и "
         "информацией по п. 13.5 ознакомлен(а) до подписания", ""),
    ], tall={"Фамилия, имя, отчество", "Кем и когда выдан", "Адрес места жительства"},
       extra_tall={"Подпись. Экземпляр Договора получен; с его условиями, прейскурантом "
                   "и информацией по п. 13.5 ознакомлен(а) до подписания"})
    p(doc, "", space=6)

    p(doc, "ЗАКОННЫЙ ПРЕДСТАВИТЕЛЬ ПАЦИЕНТА — заполняется, если Пациент не достиг "
           "15 лет или признан недееспособным", bold=True, align="left", space=3,
      keep_with_next=True)
    form_table(doc, [
        ("Фамилия, имя, отчество", ""),
        ("Паспорт: серия, номер, кем и когда выдан", ""),
        ("Адрес места жительства, телефон", ""),
        ("Кем приходится Пациенту", ""),
        ("Документ о полномочиях (свидетельство о рождении, акт органа опеки)", ""),
        ("Подпись представителя", ""),
    ], tall={"Фамилия, имя, отчество", "Паспорт: серия, номер, кем и когда выдан",
             "Адрес места жительства, телефон", "Подпись представителя"})

    path = OUT / f"{NAME}.docx"
    doc.save(path)
    return path


# ────────────────────────── PDF (по запросу) ──────────────────────────
# Вёрстка живёт только в .docx — второй раз её повторять нечем и незачем:
# pdf собирается из того же файла конвертацией, поэтому расхождений нет.
def build_pdf(docx_path: Path) -> Path | None:
    import shutil
    import subprocess
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        print("  · pdf не собран: нет LibreOffice "
              "(apt-get install -y --no-install-recommends libreoffice-writer)")
        return None
    subprocess.run([soffice, "--headless", "--convert-to", "pdf",
                    "--outdir", str(OUT), str(docx_path)],
                   check=True, capture_output=True, timeout=300)
    return docx_path.with_suffix(".pdf")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    docx = build_docx()
    print(f"  ✓ {docx.relative_to(HERE.parent.parent)}  "
          f"({docx.stat().st_size // 1024} КБ)")
    if "--pdf" in sys.argv:
        pdf = build_pdf(docx)
        if pdf:
            print(f"  ✓ {pdf.relative_to(HERE.parent.parent)}  "
                  f"({pdf.stat().st_size // 1024} КБ)")
    print("\n  ⚠️ Заполняется руками:")
    for t in T.TODO:
        print(f"     — {t}")


if __name__ == "__main__":
    main()
