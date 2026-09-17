"""
SciPilot-cite :: format_citation.py
多格式学术引用格式化引擎
支持 IEEE / APA 7th / Nature / Vancouver / GB-T-7714
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

from utils import author_initials_first, author_last_initials, logger, normalize_author

ASSETS_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "assets", "format_templates"))


def _authors_initials_first(authors: list[str], max_display: int = 6, et_al_threshold: int = 7) -> str:
    if not authors:
        return ""
    formatted = [author_initials_first(a) for a in authors]
    if len(formatted) >= et_al_threshold:
        return f"{formatted[0]}, et al."
    if len(formatted) <= max_display:
        if len(formatted) == 1:
            return formatted[0]
        return ", ".join(formatted[:-1]) + ", and " + formatted[-1]
    return ", ".join(formatted[:max_display]) + ", et al."


def _authors_last_initials_apa(authors: list[str], max_display: int = 20) -> str:
    if not authors:
        return ""
    formatted = [author_last_initials(a) for a in authors]
    if len(formatted) > max_display:
        return ", ".join(formatted[: max_display - 1]) + f", ... {formatted[-1]}"
    if len(formatted) == 1:
        return formatted[0]
    return ", ".join(formatted[:-1]) + ", & " + formatted[-1]


def _authors_nature(authors: list[str]) -> str:
    if not authors:
        return ""
    formatted = [author_last_initials(a).replace(",", "") for a in authors]
    if len(formatted) > 5:
        return f"{formatted[0]} et al"
    if len(formatted) == 1:
        return formatted[0]
    return ", ".join(formatted[:-1]) + " & " + formatted[-1]


def _authors_vancouver(authors: list[str], max_display: int = 6) -> str:
    if not authors:
        return ""
    formatted = []
    for a in authors:
        rendered = author_last_initials(a).replace(",", "").replace(".", "")
        formatted.append(rendered)
    if len(formatted) > max_display:
        return ", ".join(formatted[:max_display]) + ", et al"
    return ", ".join(formatted)


def _authors_gbt7714(authors: list[str], max_display: int = 3) -> str:
    if not authors:
        return ""
    fmt = []
    for a in authors:
        name = normalize_author(a)
        if any("一" <= ch <= "鿿" for ch in name):
            fmt.append(name)
        else:
            fmt.append(author_last_initials(a).replace(",", "").replace(".", ""))
    if len(fmt) > max_display:
        return ", ".join(fmt[:max_display]) + ", 等"
    return ", ".join(fmt)


def format_ieee(paper: dict, number: int | None = None) -> str:
    """IEEE 格式（数字编号）。"""
    prefix = f"[{number}] " if number is not None else ""
    authors = _authors_initials_first(paper.get("authors") or [])
    title = (paper.get("title", "") or "").rstrip(".")
    venue = paper.get("venue", "") or ""
    year = paper.get("year") or ""
    doi = paper.get("doi") or ""

    is_conf = bool(venue) and any(k in venue.lower() for k in ("conf", "proceedings", "workshop", "symposium"))

    chunks: list[str] = []
    if authors:
        chunks.append(authors + ",")
    chunks.append(f'"{title},"')
    tail_parts: list[str] = []
    if venue:
        tail_parts.append(f"in *{venue}*" if is_conf else f"*{venue}*")
    if year:
        tail_parts.append(str(year))
    if tail_parts:
        chunks.append(", ".join(tail_parts))
    body = " ".join(chunks)
    if doi:
        body = body.rstrip(".") + f", doi: {doi}"
    body = body.rstrip(".") + "."
    return prefix + body


def format_apa7(paper: dict) -> str:
    """APA 第 7 版（作者-年份）。"""
    authors = _authors_last_initials_apa(paper.get("authors") or [])
    year = paper.get("year") or "n.d."
    title = (paper.get("title") or "").rstrip(".")
    venue = paper.get("venue") or ""
    doi = paper.get("doi") or ""

    bits = []
    if authors:
        bits.append(f"{authors}")
    bits.append(f"({year}).")
    bits.append(f"{title}.")
    if venue:
        bits.append(f"*{venue}*.")
    if doi:
        bits.append(f"https://doi.org/{doi}")
    return " ".join(bits)


def format_nature(paper: dict, number: int | None = None) -> str:
    """Nature 格式（上标数字编号）。"""
    n = f"{number}. " if number is not None else ""
    authors = _authors_nature(paper.get("authors") or [])
    title = (paper.get("title") or "").rstrip(".")
    venue = paper.get("venue") or ""
    year = paper.get("year") or ""
    if year:
        tail = f"*{venue}* ({year})." if venue else f"({year})."
    else:
        tail = f"*{venue}*." if venue else ""
    parts = [n.rstrip()] if n else []
    if authors:
        parts.append(f"{authors}.")
    parts.append(f"{title}.")
    parts.append(tail)
    return " ".join(p for p in parts if p)


def format_vancouver(paper: dict, number: int | None = None) -> str:
    """Vancouver 格式（数字编号，医学/生物）。"""
    n = f"{number}. " if number is not None else ""
    authors = _authors_vancouver(paper.get("authors") or [])
    title = (paper.get("title") or "").rstrip(".")
    venue = paper.get("venue") or ""
    year = paper.get("year") or ""
    parts = [n.rstrip()] if n else []
    if authors:
        parts.append(f"{authors}.")
    parts.append(f"{title}.")
    if venue:
        parts.append(f"{venue}.")
    if year:
        parts.append(f"{year}.")
    return " ".join(p for p in parts if p)


def format_gbt7714(paper: dict, number: int | None = None) -> str:
    """GB/T 7714-2015 中文国标格式。"""
    n = f"[{number}] " if number is not None else ""
    authors = _authors_gbt7714(paper.get("authors") or [])
    title = (paper.get("title") or "").rstrip(".")
    venue = paper.get("venue") or ""
    year = paper.get("year") or ""
    doi = paper.get("doi") or ""
    parts = []
    if authors:
        parts.append(f"{authors}.")
    parts.append(f"{title}[J].")
    if venue:
        parts.append(f"{venue},")
    if year:
        parts.append(f"{year}.")
    if doi:
        parts.append(f"DOI: {doi}.")
    return n + " ".join(p for p in parts if p)


_FORMATTERS = {
    "ieee": format_ieee,
    "apa7": format_apa7,
    "apa": format_apa7,
    "nature": format_nature,
    "vancouver": format_vancouver,
    "gb-t-7714": format_gbt7714,
    "gbt7714": format_gbt7714,
}


def load_template(style: str) -> dict[str, Any]:
    """加载 assets/format_templates/{style}.json"""
    path = os.path.join(ASSETS_DIR, f"{style}.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def format_citation(paper: dict, style: str = "ieee", number: int | None = None) -> str:
    """主入口：根据 style 调用对应格式化函数。"""
    style = (style or "ieee").lower()
    fn = _FORMATTERS.get(style)
    if not fn:
        logger.warning(f"Unknown style '{style}', falling back to IEEE")
        fn = format_ieee
    try:
        return fn(paper, number) if fn in (format_ieee, format_nature, format_vancouver, format_gbt7714) else fn(paper)
    except TypeError:
        return fn(paper)


def format_bibtex_entry(paper: dict) -> str:
    """生成 BibTeX 条目。"""
    key = paper.get("bibtex_key") or "paper"
    title = (paper.get("title") or "").replace("{", "\\{").replace("}", "\\}")
    authors = " and ".join(paper.get("authors") or [])
    year = paper.get("year") or ""
    venue = paper.get("venue") or ""
    doi = paper.get("doi") or ""

    is_conf = bool(venue) and any(k in venue.lower() for k in ("conf", "proceedings", "workshop", "symposium"))
    entry_type = "inproceedings" if is_conf else "article"
    venue_key = "booktitle" if is_conf else "journal"

    lines = [f"@{entry_type}{{{key},"]
    lines.append(f"  title     = {{{title}}},")
    if authors:
        lines.append(f"  author    = {{{authors}}},")
    if venue:
        lines.append(f"  {venue_key:9}= {{{venue}}},")
    if year:
        lines.append(f"  year      = {{{year}}},")
    if doi:
        lines.append(f"  doi       = {{{doi}}}")
    if lines[-1].endswith(","):
        lines[-1] = lines[-1].rstrip(",")
    lines.append("}")
    return "\n".join(lines)


def _cli() -> int:
    p = argparse.ArgumentParser(description="SciPilot-cite citation formatter")
    p.add_argument("--style", default="ieee", choices=list(_FORMATTERS.keys()) + ["bibtex"])
    p.add_argument("--input", help="paper JSON file (default stdin)")
    p.add_argument("--number", type=int)
    args = p.parse_args()

    if args.input:
        with open(args.input, encoding="utf-8") as f:
            paper = json.load(f)
    else:
        paper = json.load(sys.stdin)

    if args.style == "bibtex":
        print(format_bibtex_entry(paper))
    else:
        print(format_citation(paper, args.style, args.number))
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
