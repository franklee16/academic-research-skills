#!/usr/bin/env python3
"""Format normalized metadata as Chinese academic references and BibTeX."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from typing import Any


STOP_WORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "by",
    "for",
    "from",
    "in",
    "into",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
    "via",
    "vs",
}


TYPE_MARKS = {
    "article": "J",
    "journal": "J",
    "inproceedings": "C",
    "conference": "C",
    "proceedings": "C",
    "book": "M",
    "monograph": "M",
    "thesis": "D",
    "dissertation": "D",
    "report": "R",
    "standard": "S",
    "patent": "P",
    "newspaper": "N",
    "chapter": "M",
    "online": "EB/OL",
    "web": "EB/OL",
}


BIB_TYPES = {
    "article": "article",
    "journal": "article",
    "inproceedings": "inproceedings",
    "conference": "inproceedings",
    "proceedings": "inproceedings",
    "book": "book",
    "monograph": "book",
    "thesis": "phdthesis",
    "dissertation": "phdthesis",
    "report": "techreport",
    "standard": "misc",
    "patent": "misc",
    "newspaper": "misc",
    "chapter": "incollection",
    "online": "misc",
    "web": "misc",
}


def has_cjk(text: str) -> bool:
    return bool(re.search(r"[\u3400-\u9fff]", text))


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def clean(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def strip_trailing_period(value: str) -> str:
    return value.rstrip().rstrip(".。")


def title_for_reference(title: str) -> str:
    title = clean(title)
    if has_cjk(title):
        return title
    words = title.split(" ")
    formatted: list[str] = []
    for idx, word in enumerate(words):
        prefix = re.match(r"^\W+", word)
        suffix = re.search(r"\W+$", word)
        left = prefix.group(0) if prefix else ""
        right = suffix.group(0) if suffix else ""
        core = word[len(left) : len(word) - len(right) if right else len(word)]
        if not core:
            formatted.append(word)
            continue
        lower = core.lower()
        if idx > 0 and lower in STOP_WORDS:
            new_core = lower
        elif core.isupper() or any(ch.isdigit() for ch in core):
            new_core = core
        else:
            new_core = core[:1].upper() + core[1:].lower()
        formatted.append(f"{left}{new_core}{right}")
    return " ".join(formatted)


def western_author_name(name: str) -> str:
    name = clean(name).replace(".", "")
    if "," in name:
        family, given = [part.strip() for part in name.split(",", 1)]
        given_parts = re.split(r"[\s-]+", given)
    else:
        parts = name.split()
        if len(parts) == 1:
            return parts[0]
        family = parts[-1]
        given_parts = parts[:-1]
    initials = " ".join(part[:1].upper() for part in given_parts if part)
    return f"{family} {initials}".strip()


def author_display(author: Any) -> str:
    if isinstance(author, dict):
        literal = clean(author.get("literal"))
        if literal:
            return literal
        family = clean(author.get("family"))
        given = clean(author.get("given"))
        if has_cjk(family + given):
            return family + given
        if family and given:
            return western_author_name(f"{family}, {given}")
        return clean(author.get("name"))
    name = clean(author)
    if has_cjk(name):
        return name
    return western_author_name(name)


def format_authors(authors: list[Any]) -> str:
    authors = [author for author in authors if clean(author)]
    if not authors:
        return ""
    visible = authors[:3]
    rendered = [author_display(author) for author in visible]
    english = not any(has_cjk(author_display(author)) for author in visible)
    if len(authors) > 3:
        rendered.append("et al" if english else "等")
    return (", " if english else "，").join(rendered)


def original_authors_for_bibtex(authors: list[Any]) -> str:
    rendered = []
    for author in authors:
        if isinstance(author, dict):
            literal = clean(author.get("literal"))
            if literal:
                rendered.append(literal)
                continue
            family = clean(author.get("family"))
            given = clean(author.get("given"))
            rendered.append(f"{family}, {given}".strip(", "))
        else:
            rendered.append(clean(author))
    return " and ".join(author for author in rendered if author)


def append_pages(segment: str, pages: str) -> str:
    if pages:
        return f"{segment}:{pages}"
    return segment


def append_doi_url(reference: str, item: dict[str, Any]) -> str:
    doi = clean(item.get("doi"))
    if doi:
        return f"{strip_trailing_period(reference)}. DOI:{doi}."
    return reference


def year_part(item: dict[str, Any]) -> str:
    year = clean(item.get("year"))
    volume = clean(item.get("volume"))
    issue = clean(item.get("issue") or item.get("number"))
    segment = year
    if volume:
        segment += f", {volume}"
    if issue:
        segment += f"({issue})"
    return segment


def reference_line(item: dict[str, Any], number: int) -> str:
    title = clean(item.get("title"))
    if clean(item.get("status")) == "not_found":
        return f"未找到与“{title}”明确对应的公开文献。"
    if clean(item.get("status")) == "ambiguous":
        note = clean(item.get("note")) or "多个来源信息冲突，无法确定唯一对应文献。"
        return f"无法确定“{title}”的唯一对应文献：{note}"

    kind = clean(item.get("type")).lower() or "article"
    mark = clean(item.get("mark")) or TYPE_MARKS.get(kind, "J")
    authors = format_authors(as_list(item.get("authors") or item.get("author")))
    title_ref = title_for_reference(title)
    prefix = f"[{number}] "
    author_prefix = f"{authors}. " if authors else ""
    pages = clean(item.get("pages"))

    if kind in {"article", "journal"}:
        journal = clean(item.get("journal") or item.get("container"))
        segment = append_pages(f"{journal}, {year_part(item)}", pages)
        ref = f"{prefix}{author_prefix}{title_ref}[{mark}]. {segment}."
        return append_doi_url(ref, item)

    if kind in {"inproceedings", "conference", "proceedings"}:
        booktitle = clean(item.get("booktitle") or item.get("container"))
        segment = append_pages(f"{booktitle}, {clean(item.get('year'))}", pages)
        return f"{prefix}{author_prefix}{title_ref}[{mark}]. {segment}."

    if kind in {"book", "monograph"}:
        edition = clean(item.get("edition") or item.get("version"))
        edition_part = "" if edition in {"", "1", "1st", "第一版"} else f"{edition}. "
        translators = format_authors(as_list(item.get("translators") or item.get("translator")))
        translator_part = f"{translators}, 译. " if translators else ""
        place = clean(item.get("place") or item.get("address"))
        publisher = clean(item.get("publisher"))
        pub = f"{place}:{publisher}" if place and publisher else publisher or place
        segment = append_pages(f"{pub}, {clean(item.get('year'))}", pages)
        return f"{prefix}{author_prefix}{title_ref}[{mark}]. {translator_part}{edition_part}{segment}."

    if kind in {"thesis", "dissertation"}:
        place = clean(item.get("place") or item.get("address"))
        school = clean(item.get("school") or item.get("institution"))
        pub = f"{place}:{school}" if place and school else school or place
        segment = append_pages(f"{pub}, {clean(item.get('year'))}", pages)
        return f"{prefix}{author_prefix}{title_ref}[{mark}]. {segment}."

    if kind == "report":
        place = clean(item.get("place") or item.get("address"))
        institution = clean(item.get("institution") or item.get("publisher"))
        pub = f"{place}:{institution}" if place and institution else institution or place
        segment = append_pages(f"{pub}, {clean(item.get('year'))}", pages)
        return f"{prefix}{author_prefix}{title_ref}[{mark}]. {segment}."

    if kind == "patent":
        country = clean(item.get("country"))
        patent_type = clean(item.get("patent_type"))
        patent_number = clean(item.get("patent_number") or item.get("number"))
        date = clean(item.get("published_date") or item.get("date"))
        parts = ", ".join(part for part in [country, patent_type, patent_number] if part)
        tail = f"{parts}. {date}" if date else parts
        return f"{prefix}{author_prefix}{title_ref}[{mark}]. {tail}."

    if kind == "standard":
        code = clean(item.get("standard_code") or item.get("code"))
        place = clean(item.get("place") or item.get("address"))
        publisher = clean(item.get("publisher"))
        year = clean(item.get("year"))
        pub = ".".join(part for part in [place, publisher] if part)
        tail = ".".join(part for part in [code, title_ref, pub, year] if part)
        return f"{prefix}{author_prefix}{tail}[{mark}]."

    if kind == "newspaper":
        newspaper = clean(item.get("newspaper") or item.get("container"))
        date = clean(item.get("published_date") or item.get("date"))
        edition = clean(item.get("edition"))
        date_part = f"{date}({edition})" if edition else date
        return f"{prefix}{author_prefix}{title_ref}[{mark}]. {newspaper}, {date_part}."

    if kind == "chapter":
        booktitle = clean(item.get("booktitle"))
        book_authors = format_authors(as_list(item.get("book_authors") or item.get("editors")))
        place = clean(item.get("place") or item.get("address"))
        publisher = clean(item.get("publisher"))
        year = clean(item.get("year"))
        pub = f"{place}:{publisher}" if place and publisher else publisher or place
        container = f"{book_authors}. {booktitle}" if book_authors else booktitle
        segment = append_pages(f"{container}. {pub}, {year}", pages)
        return f"{prefix}{author_prefix}{title_ref}[{mark}]//{segment}."

    published = clean(item.get("published_date") or item.get("date"))
    access = clean(item.get("access_date"))
    url = clean(item.get("url"))
    date_part = ""
    if published:
        date_part += f"({published})"
    if access:
        date_part += f"[{access}]"
    return f"{prefix}{author_prefix}{title_ref}[{mark}]. {date_part}. {url}."


def slug(text: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)?", text.lower())
    words = [word for word in words if word not in STOP_WORDS]
    return "-".join(words[:3])


def first_author_slug(authors: list[Any]) -> str:
    if not authors:
        return "ref"
    first = authors[0]
    if isinstance(first, dict):
        family = clean(first.get("family") or first.get("literal") or first.get("name"))
    else:
        name = clean(first)
        family = name.split(",", 1)[0] if "," in name else name.split()[-1]
    candidate = slug(family)
    return candidate or "ref"


def bib_key(item: dict[str, Any]) -> str:
    authors = as_list(item.get("authors") or item.get("author"))
    year = clean(item.get("year") or item.get("published_date") or "nd")[:4] or "nd"
    title = clean(item.get("title"))
    title_slug = slug(title)
    base = "-".join(part for part in [first_author_slug(authors), year, title_slug] if part)
    if title_slug:
        return base
    digest = hashlib.md5(title.encode("utf-8")).hexdigest()[:8]
    return f"{base}-{digest}" if base else f"ref-{digest}"


def bibtex_entry(item: dict[str, Any]) -> str:
    if clean(item.get("status")) in {"not_found", "ambiguous"}:
        return ""
    kind = clean(item.get("type")).lower() or "article"
    bib_type = BIB_TYPES.get(kind, "misc")
    fields: list[tuple[str, str]] = []
    authors = original_authors_for_bibtex(as_list(item.get("authors") or item.get("author")))
    if authors:
        fields.append(("author", authors))
    for key, candidates in [
        ("title", ["title"]),
        ("journal", ["journal"]),
        ("booktitle", ["booktitle"]),
        ("publisher", ["publisher"]),
        ("address", ["place", "address"]),
        ("school", ["school", "institution"]),
        ("institution", ["institution"]),
        ("year", ["year"]),
        ("volume", ["volume"]),
        ("number", ["issue", "number"]),
        ("pages", ["pages"]),
        ("doi", ["doi"]),
        ("url", ["url"]),
        ("note", ["note"]),
    ]:
        value = ""
        for candidate in candidates:
            value = clean(item.get(candidate))
            if value:
                break
        if value and (key != "journal" or bib_type == "article"):
            if key == "booktitle" and bib_type not in {"inproceedings", "incollection"}:
                continue
            if key == "school" and bib_type not in {"phdthesis", "mastersthesis"}:
                continue
            if key == "institution" and bib_type != "techreport":
                continue
            fields.append((key, value))
    if kind == "online" and clean(item.get("access_date")):
        fields.append(("urldate", clean(item.get("access_date"))))
    lines = [f"@{bib_type}{{{bib_key(item)},"]
    for idx, (field, value) in enumerate(fields):
        comma = "," if idx < len(fields) - 1 else ""
        lines.append(f"  {field} = {{{value}}}{comma}")
    lines.append("}")
    return "\n".join(lines)


def sources_line(item: dict[str, Any]) -> str:
    sources = [clean(source) for source in as_list(item.get("sources")) if clean(source)]
    if not sources:
        if clean(item.get("url")):
            sources.append(clean(item.get("url")))
        elif clean(item.get("doi")):
            sources.append(f"DOI:{clean(item.get('doi'))}")
    return "核验来源：" + ("; ".join(sources) if sources else "未提供")


def render_item(item: dict[str, Any], number: int) -> str:
    ref = reference_line(item, number)
    if clean(item.get("status")) in {"not_found", "ambiguous"}:
        return ref
    bib = bibtex_entry(item)
    return f"标准参考文献：{ref}\nBibTeX：\n```bibtex\n{bib}\n```\n{sources_line(item)}"


def load_payload(args: argparse.Namespace) -> Any:
    if args.input:
        with open(args.input, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return json.load(sys.stdin)


def normalize_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("items"), list):
        return payload["items"]
    if isinstance(payload, dict):
        return [payload]
    raise SystemExit("Input JSON must be an object, an object with items, or a list.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="Path to normalized metadata JSON. Defaults to stdin.")
    parser.add_argument("--start", type=int, default=1, help="Starting reference number.")
    args = parser.parse_args()

    items = normalize_payload(load_payload(args))
    rendered = [render_item(item, args.start + idx) for idx, item in enumerate(items)]
    print("\n\n".join(rendered))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
