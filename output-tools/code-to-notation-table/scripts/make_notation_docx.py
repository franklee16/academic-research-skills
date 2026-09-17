#!/usr/bin/env python3
"""Create a Word docx notation table with editable OMML equation cells.

Input JSON schema:
{
  "title": "Code Variable To Paper Symbol Table",
  "rows": [
    {"code": "v_true", "latex": "v^\\ast", "meaning": "...",
     "category": "Physical quantity", "note": "..."}
  ]
}

This converter intentionally supports a small, publication-notation subset.
Keep symbols simple instead of forcing code-like detail into formulas.
"""

from __future__ import annotations

import json
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple
from xml.sax.saxutils import escape


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


GREEK = {
    "alpha": "α",
    "beta": "β",
    "gamma": "γ",
    "Gamma": "Γ",
    "delta": "δ",
    "Delta": "Δ",
    "epsilon": "ε",
    "varepsilon": "ε",
    "eta": "η",
    "theta": "θ",
    "kappa": "κ",
    "lambda": "λ",
    "mu": "μ",
    "nu": "ν",
    "pi": "π",
    "psi": "ψ",
    "rho": "ρ",
    "sigma": "σ",
    "varphi": "φ",
    "phi": "φ",
    "omega": "ω",
    "Omega": "Ω",
    "ast": "∗",
    "in": "∈",
    "times": "×",
    "pm": "±",
}


def xml_text(text: str) -> str:
    return escape(text, {'"': "&quot;"})


def w_text_run(text: str, code: bool = False, bold: bool = False) -> str:
    text = xml_text(text)
    rpr = ""
    if code:
        rpr += '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>'
    if bold:
        rpr += "<w:b/>"
    if rpr:
        rpr = f"<w:rPr>{rpr}</w:rPr>"
    return f"<w:r>{rpr}<w:t xml:space=\"preserve\">{text}</w:t></w:r>"


def m_run(text: str, plain: bool = False) -> str:
    text = xml_text(text)
    style = '<m:rPr><m:sty m:val="p"/></m:rPr>' if plain else ""
    return f"<m:r>{style}<m:t>{text}</m:t></m:r>"


def m_group(items: List[str]) -> str:
    return "".join(items)


def m_sub(base: str, sub: str) -> str:
    return f"<m:sSub><m:e>{base}</m:e><m:sub>{sub}</m:sub></m:sSub>"


def m_sup(base: str, sup: str) -> str:
    return f"<m:sSup><m:e>{base}</m:e><m:sup>{sup}</m:sup></m:sSup>"


def m_subsup(base: str, sub: str, sup: str) -> str:
    return f"<m:sSubSup><m:e>{base}</m:e><m:sub>{sub}</m:sub><m:sup>{sup}</m:sup></m:sSubSup>"


def m_hat(base: str) -> str:
    return (
        '<m:acc><m:accPr><m:chr m:val="̂"/></m:accPr>'
        f"<m:e>{base}</m:e></m:acc>"
    )


def m_tilde(base: str) -> str:
    return (
        '<m:acc><m:accPr><m:chr m:val="̃"/></m:accPr>'
        f"<m:e>{base}</m:e></m:acc>"
    )


@dataclass
class Atom:
    omml: str
    start: int
    end: int


class LatexSubsetParser:
    def __init__(self, text: str):
        self.text = text.strip()
        self.i = 0

    def parse(self, stop: Optional[str] = None) -> str:
        items: List[str] = []
        while self.i < len(self.text):
            if stop and self.text.startswith(stop, self.i):
                self.i += len(stop)
                break
            if self.text[self.i].isspace():
                self.i += 1
                items.append(m_run(" "))
                continue
            atom = self.parse_atom()
            if atom is None:
                break
            base = atom.omml
            sub = None
            sup = None
            while self.i < len(self.text) and self.text[self.i] in "_^":
                marker = self.text[self.i]
                self.i += 1
                script = self.parse_script()
                if marker == "_":
                    sub = script
                else:
                    sup = script
            if sub is not None and sup is not None:
                items.append(m_subsup(base, sub, sup))
            elif sub is not None:
                items.append(m_sub(base, sub))
            elif sup is not None:
                items.append(m_sup(base, sup))
            else:
                items.append(base)
        return m_group(items)

    def parse_atom(self) -> Optional[Atom]:
        start = self.i
        ch = self.text[self.i]
        if ch == "{":
            self.i += 1
            inner = self.parse("}")
            return Atom(inner, start, self.i)
        if ch == "\\":
            return self.parse_command()
        self.i += 1
        return Atom(m_run(ch), start, self.i)

    def parse_script(self) -> str:
        if self.i >= len(self.text):
            return m_run("")
        if self.text[self.i] == "{":
            self.i += 1
            return self.parse("}")
        atom = self.parse_atom()
        return atom.omml if atom else m_run("")

    def parse_command(self) -> Atom:
        start = self.i
        self.i += 1
        if self.i < len(self.text) and self.text[self.i] in "{}":
            ch = self.text[self.i]
            self.i += 1
            return Atom(m_run(ch), start, self.i)

        name_start = self.i
        while self.i < len(self.text) and self.text[self.i].isalpha():
            self.i += 1
        name = self.text[name_start:self.i]

        if name == "mathrm":
            content = self.read_braced_text()
            return Atom(m_run(content, plain=True), start, self.i)
        if name == "hat":
            return Atom(m_hat(self.parse_required_group_or_atom()), start, self.i)
        if name == "tilde":
            return Atom(m_tilde(self.parse_required_group_or_atom()), start, self.i)
        if name in ("left", "right"):
            if self.i < len(self.text):
                ch = self.text[self.i]
                self.i += 1
                return Atom(m_run(ch), start, self.i)
            return Atom(m_run(""), start, self.i)
        if name in GREEK:
            return Atom(m_run(GREEK[name]), start, self.i)
        return Atom(m_run("\\" + name), start, self.i)

    def parse_required_group_or_atom(self) -> str:
        if self.i < len(self.text) and self.text[self.i] == "{":
            self.i += 1
            return self.parse("}")
        atom = self.parse_atom()
        return atom.omml if atom else m_run("")

    def read_braced_text(self) -> str:
        if self.i >= len(self.text) or self.text[self.i] != "{":
            return ""
        self.i += 1
        depth = 1
        start = self.i
        while self.i < len(self.text) and depth:
            if self.text[self.i] == "{":
                depth += 1
            elif self.text[self.i] == "}":
                depth -= 1
                if depth == 0:
                    content = self.text[start:self.i]
                    self.i += 1
                    return content.replace("\\_", "_")
            self.i += 1
        return self.text[start:self.i]


def latex_to_omml(latex: str) -> str:
    parser = LatexSubsetParser(latex)
    body = parser.parse()
    return f"<m:oMath>{body}</m:oMath>"


def paragraph(children: str = "") -> str:
    return f"<w:p>{children}</w:p>"


def cell(children: str, width: int = 2400) -> str:
    return (
        f"<w:tc><w:tcPr><w:tcW w:w=\"{width}\" w:type=\"dxa\"/></w:tcPr>"
        f"{children}</w:tc>"
    )


def row(cells: List[str]) -> str:
    return "<w:tr>" + "".join(cells) + "</w:tr>"


def table(rows: List[str]) -> str:
    borders = (
        "<w:tblPr><w:tblW w:w=\"0\" w:type=\"auto\"/>"
        "<w:tblBorders>"
        "<w:top w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"808080\"/>"
        "<w:left w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"808080\"/>"
        "<w:bottom w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"808080\"/>"
        "<w:right w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"808080\"/>"
        "<w:insideH w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"D0D0D0\"/>"
        "<w:insideV w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"D0D0D0\"/>"
        "</w:tblBorders></w:tblPr>"
    )
    return "<w:tbl>" + borders + "".join(rows) + "</w:tbl>"


def document_xml(title: str, rows_data: List[dict]) -> str:
    body: List[str] = []
    body.append(paragraph(w_text_run(title, bold=True)))
    header = ["Code variable", "Paper symbol", "Meaning", "Category", "Notes"]
    widths = [3300, 1800, 4300, 1900, 3900]
    rows_xml = [
        row([cell(paragraph(w_text_run(h, bold=True)), widths[i]) for i, h in enumerate(header)])
    ]
    for item in rows_data:
        code = str(item.get("code", ""))
        latex = str(item.get("latex", ""))
        meaning = str(item.get("meaning", ""))
        category = str(item.get("category", ""))
        note = str(item.get("note", ""))
        rows_xml.append(
            row(
                [
                    cell(paragraph(w_text_run(code, code=True)), widths[0]),
                    cell(paragraph(latex_to_omml(latex)), widths[1]),
                    cell(paragraph(w_text_run(meaning)), widths[2]),
                    cell(paragraph(w_text_run(category)), widths[3]),
                    cell(paragraph(w_text_run(note)), widths[4]),
                ]
            )
        )
    body.append(table(rows_xml))
    body.append("<w:sectPr><w:pgSz w:w=\"16838\" w:h=\"11906\" w:orient=\"landscape\"/><w:pgMar w:top=\"720\" w:right=\"720\" w:bottom=\"720\" w:left=\"720\" w:header=\"360\" w:footer=\"360\" w:gutter=\"0\"/></w:sectPr>")
    return (
        f'<w:document xmlns:w="{W_NS}" xmlns:m="{M_NS}" xmlns:r="{R_NS}">'
        "<w:body>" + "".join(body) + "</w:body></w:document>"
    )


def styles_xml() -> str:
    return (
        f'<w:styles xmlns:w="{W_NS}">'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
        "<w:name w:val=\"Normal\"/>"
        "<w:rPr><w:rFonts w:ascii=\"Times New Roman\" w:hAnsi=\"Times New Roman\" w:eastAsia=\"SimSun\"/></w:rPr>"
        "</w:style>"
        "</w:styles>"
    )


def write_docx(input_json: Path, output_docx: Path) -> None:
    data = json.loads(input_json.read_text(encoding="utf-8-sig"))
    title = str(data.get("title", "Code Variable To Paper Symbol Table"))
    rows_data = data.get("rows", [])
    if not isinstance(rows_data, list):
        raise ValueError("JSON field 'rows' must be a list")

    output_docx.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_docx, "w", zipfile.ZIP_DEFLATED) as docx:
        docx.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>""",
        )
        docx.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>""",
        )
        docx.writestr("word/document.xml", document_xml(title, rows_data))
        docx.writestr("word/styles.xml", styles_xml())


def main(argv: List[str]) -> int:
    if len(argv) != 3:
        print("Usage: make_notation_docx.py rows.json output.docx", file=sys.stderr)
        return 2
    write_docx(Path(argv[1]), Path(argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
