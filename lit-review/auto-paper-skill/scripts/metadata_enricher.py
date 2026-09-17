#!/usr/bin/env python3
"""Merge cross-source paper metadata without hiding missing fields or conflicts."""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

IMPORTANT_FIELDS = (
    "doi",
    "arxiv_id",
    "citation_count",
    "authors",
    "first_author",
    "last_author",
    "corresponding_authors",
)
HIGH_IMPACT_CITATIONS = 10000
HIGH_IMPACT_H_INDEX = 40


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} does not contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def collapse(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_name(value: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def normalize_doi(value: Any) -> str | None:
    if value in (None, ""):
        return None
    text = str(value).strip()
    text = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^doi:\s*", "", text, flags=re.IGNORECASE)
    return text.lower() or None


def normalize_arxiv_id(value: Any) -> str | None:
    if value in (None, ""):
        return None
    text = str(value).strip()
    text = re.sub(r"^https?://arxiv\.org/(?:abs|pdf)/", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^arxiv:\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\.pdf$", "", text, flags=re.IGNORECASE)
    return text.lower() or None


def first_nonempty(*values: Any) -> Any:
    for value in values:
        if value not in (None, "", []):
            return value
    return None


def safe_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def date_from_parts(value: Any) -> str | None:
    if not isinstance(value, dict):
        return None
    parts = value.get("date-parts")
    if not isinstance(parts, list) or not parts or not isinstance(parts[0], list):
        return None
    numbers = [int(part) for part in parts[0] if isinstance(part, int)]
    if not numbers:
        return None
    while len(numbers) < 3:
        numbers.append(1)
    return f"{numbers[0]:04d}-{numbers[1]:02d}-{numbers[2]:02d}"


def normalize_author(author: Any, source_name: str) -> dict[str, Any] | None:
    if isinstance(author, str):
        name = collapse(author)
        return {"name": name, "evidence_source": source_name} if name else None
    if not isinstance(author, dict):
        return None

    name = first_nonempty(
        author.get("name"),
        " ".join(str(part) for part in (author.get("given"), author.get("family")) if part),
    )
    if not name:
        return None

    affiliations = author.get("affiliations") or author.get("affiliation")
    if isinstance(affiliations, list):
        affiliation = first_nonempty(
            *[
                item.get("name") if isinstance(item, dict) else item
                for item in affiliations
            ]
        )
    else:
        affiliation = affiliations

    citation_count = first_nonempty(author.get("citation_count"), author.get("citationCount"))
    h_index = first_nonempty(author.get("h_index"), author.get("hIndex"))
    citation_count_int = safe_int(citation_count)
    h_index_int = safe_int(h_index)
    item = {
        "name": collapse(str(name)),
        "affiliation": affiliation or None,
        "citation_count": citation_count_int if citation_count_int is not None else citation_count,
        "h_index": h_index_int if h_index_int is not None else h_index,
        "semantic_scholar_author_id": first_nonempty(author.get("semantic_scholar_author_id"), author.get("authorId")),
        "is_corresponding": bool(author.get("is_corresponding") or author.get("corresponding")),
        "evidence_source": first_nonempty(author.get("evidence_source"), source_name),
    }
    item["is_high_impact"] = bool(
        citation_count_int is not None and citation_count_int >= HIGH_IMPACT_CITATIONS
        or h_index_int is not None and h_index_int >= HIGH_IMPACT_H_INDEX
    )
    return item


def source_record(source_name: str, source_url: str | None, fields: list[str]) -> dict[str, Any]:
    return {
        "source_name": source_name,
        "source_type": "api_or_mcp",
        "source_url": source_url,
        "is_official": source_name in {"openreview", "arxiv", "crossref"},
        "retrieved_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "fields": sorted(set(fields)),
    }


def normalize_openreview(payload: dict[str, Any]) -> dict[str, Any]:
    content = payload.get("content") if isinstance(payload.get("content"), dict) else payload

    def content_value(key: str) -> Any:
        value = content.get(key)
        if isinstance(value, dict) and "value" in value:
            return value["value"]
        return value

    authors = content_value("authors") or payload.get("authors")
    url_id = first_nonempty(payload.get("forum"), payload.get("id"))
    record = {
        "title": content_value("title"),
        "abstract_en": content_value("abstract"),
        "authors": authors,
        "venue": first_nonempty(content_value("venue"), content_value("venueid"), payload.get("venue")),
        "doi": normalize_doi(first_nonempty(content_value("doi"), payload.get("doi"))),
        "arxiv_id": normalize_arxiv_id(first_nonempty(content_value("arxiv_id"), payload.get("arxiv_id"))),
        "landing_page": f"https://openreview.net/forum?id={url_id}" if url_id else payload.get("landing_page"),
        "pdf_url": first_nonempty(payload.get("pdf_url"), payload.get("pdf")),
    }
    fields = [key for key, value in record.items() if value not in (None, "", [])]
    record["metadata_sources"] = [source_record("openreview", record.get("landing_page"), fields)]
    return record


def normalize_semantic_scholar(payload: dict[str, Any]) -> dict[str, Any]:
    external_ids = payload.get("externalIds") if isinstance(payload.get("externalIds"), dict) else {}
    record = {
        "title": payload.get("title"),
        "abstract_en": payload.get("abstract"),
        "authors": payload.get("authors"),
        "published_at": first_nonempty(payload.get("publicationDate"), str(payload.get("year")) if payload.get("year") else None),
        "venue": first_nonempty(payload.get("venue"), payload.get("publicationVenue", {}).get("name") if isinstance(payload.get("publicationVenue"), dict) else None),
        "doi": normalize_doi(first_nonempty(external_ids.get("DOI"), payload.get("doi"))),
        "arxiv_id": normalize_arxiv_id(first_nonempty(external_ids.get("ArXiv"), payload.get("arxiv_id"))),
        "citation_count": first_nonempty(payload.get("citationCount"), payload.get("citation_count")),
        "landing_page": first_nonempty(payload.get("url"), payload.get("landing_page")),
    }
    fields = [key for key, value in record.items() if value not in (None, "", [])]
    record["metadata_sources"] = [source_record("semantic_scholar", record.get("landing_page"), fields)]
    return record


def normalize_crossref(payload: dict[str, Any]) -> dict[str, Any]:
    message = payload.get("message") if isinstance(payload.get("message"), dict) else payload
    title = message.get("title")
    container = message.get("container-title")
    record = {
        "title": title[0] if isinstance(title, list) and title else title,
        "abstract_en": message.get("abstract"),
        "authors": message.get("author"),
        "published_at": first_nonempty(
            date_from_parts(message.get("published-print")),
            date_from_parts(message.get("published-online")),
            date_from_parts(message.get("issued")),
        ),
        "venue": container[0] if isinstance(container, list) and container else container,
        "doi": normalize_doi(message.get("DOI")),
        "landing_page": first_nonempty(message.get("URL"), payload.get("URL")),
    }
    fields = [key for key, value in record.items() if value not in (None, "", [])]
    record["metadata_sources"] = [source_record("crossref", record.get("landing_page"), fields)]
    return record


def normalize_arxiv(payload: dict[str, Any]) -> dict[str, Any]:
    authors = payload.get("authors")
    if isinstance(authors, list):
        normalized_authors = [item.get("name") if isinstance(item, dict) else item for item in authors]
    else:
        normalized_authors = authors
    record = {
        "title": payload.get("title"),
        "abstract_en": first_nonempty(payload.get("summary"), payload.get("abstract"), payload.get("abstract_en")),
        "authors": normalized_authors,
        "published_at": first_nonempty(payload.get("published"), payload.get("published_at")),
        "venue": first_nonempty(payload.get("journal_ref"), payload.get("venue")),
        "doi": normalize_doi(payload.get("doi")),
        "arxiv_id": normalize_arxiv_id(first_nonempty(payload.get("arxiv_id"), payload.get("id"))),
        "landing_page": first_nonempty(payload.get("entry_id"), payload.get("landing_page")),
    }
    fields = [key for key, value in record.items() if value not in (None, "", [])]
    record["metadata_sources"] = [source_record("arxiv", record.get("landing_page"), fields)]
    return record


def normalize_source(source_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    source = source_name.lower().replace("-", "_")
    if source == "openreview":
        return normalize_openreview(payload)
    if source in {"semantic_scholar", "semanticscholar", "s2"}:
        return normalize_semantic_scholar(payload)
    if source == "crossref":
        return normalize_crossref(payload)
    if source == "arxiv":
        return normalize_arxiv(payload)
    record = dict(payload)
    record.setdefault("metadata_sources", [source_record(source_name, record.get("landing_page"), list(record.keys()))])
    return record


def merge_authors(existing: Any, incoming: Any, source_name: str) -> list[dict[str, Any]]:
    authors: list[dict[str, Any]] = []
    by_name: dict[str, dict[str, Any]] = {}

    def add(author: Any, source: str) -> None:
        normalized = normalize_author(author, source)
        if not normalized:
            return
        key = normalize_name(normalized["name"])
        target = by_name.get(key)
        if target is None:
            by_name[key] = normalized
            authors.append(normalized)
            return
        for field, value in normalized.items():
            if target.get(field) in (None, "", False) and value not in (None, "", False):
                target[field] = value
        target["is_high_impact"] = bool(target.get("is_high_impact") or normalized.get("is_high_impact"))

    for author in existing if isinstance(existing, list) else []:
        add(author, "existing")
    for author in incoming if isinstance(incoming, list) else []:
        add(author, source_name)
    return authors


def merge_sources(existing: Any, incoming: Any) -> list[dict[str, Any]]:
    sources = [item for item in existing if isinstance(item, dict)] if isinstance(existing, list) else []
    for source in incoming if isinstance(incoming, list) else []:
        if isinstance(source, dict):
            sources.append(source)
    seen = set()
    unique = []
    for source in sources:
        key = (
            source.get("source_name"),
            source.get("source_url"),
            tuple(source.get("fields", [])) if isinstance(source.get("fields"), list) else (),
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(source)
    return unique


def merge_metadata(base: dict[str, Any], normalized_sources: list[tuple[str, dict[str, Any]]]) -> dict[str, Any]:
    merged = dict(base)
    conflicts: list[dict[str, Any]] = []
    checked_sources: list[str] = []

    for source_name, source in normalized_sources:
        checked_sources.append(source_name)
        for field in (
            "title",
            "abstract_en",
            "published_at",
            "venue",
            "venue_type",
            "doi",
            "arxiv_id",
            "citation_count",
            "landing_page",
            "pdf_url",
        ):
            value = source.get(field)
            if value in (None, "", []):
                continue
            if field == "doi":
                value = normalize_doi(value)
            if field == "arxiv_id":
                value = normalize_arxiv_id(value)
            existing = merged.get(field)
            if existing in (None, "", []):
                merged[field] = value
            elif str(existing).strip().lower() != str(value).strip().lower():
                conflicts.append({"field": field, "existing": existing, "incoming": value, "source": source_name})

        merged["authors"] = merge_authors(merged.get("authors"), source.get("authors"), source_name)
        merged["metadata_sources"] = merge_sources(merged.get("metadata_sources"), source.get("metadata_sources"))

    authors = merged.get("authors") if isinstance(merged.get("authors"), list) else []
    if authors:
        merged.setdefault("first_author", authors[0])
        merged.setdefault("last_author", authors[-1])
    corresponding = [author for author in authors if author.get("is_corresponding")]
    if corresponding:
        merged["corresponding_authors"] = corresponding
    else:
        merged.setdefault("corresponding_authors", [])
        merged.setdefault("corresponding_author_status", "未在可用来源中可靠识别，未猜测。")

    high_impact = [author for author in authors if author.get("is_high_impact")]
    if high_impact and not merged.get("author_influence_summary"):
        merged["author_influence_summary"] = [
            f"{author.get('name')} 的引用或 h-index 达到高影响力阈值，来源: {author.get('evidence_source') or '未知'}。"
            for author in high_impact
        ]

    field_status = {
        field: "found" if merged.get(field) not in (None, "", []) else "not_found"
        for field in IMPORTANT_FIELDS
    }
    merged["metadata_enrichment_status"] = {
        "sources_checked": checked_sources,
        "field_status": field_status,
        "missing_fields": [field for field, status in field_status.items() if status != "found"],
        "conflicts": conflicts,
    }
    return merged


def parse_source_arg(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("source must use name=/path/to/file.json")
    name, path = value.split("=", 1)
    if not name.strip() or not path.strip():
        raise argparse.ArgumentTypeError("source must use name=/path/to/file.json")
    return name.strip(), Path(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge metadata from OpenReview, Semantic Scholar, Crossref, arXiv, or normalized JSON.")
    parser.add_argument("--base", help="Existing metadata.json. If omitted, starts from an empty record.")
    parser.add_argument("--source", action="append", type=parse_source_arg, default=[], help="Source payload as name=/path/file.json.")
    parser.add_argument("--output", required=True, help="Path for merged metadata.json.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base = load_json(Path(args.base)) if args.base else {}
    normalized_sources = [
        (name, normalize_source(name, load_json(path)))
        for name, path in args.source
    ]
    merged = merge_metadata(base, normalized_sources)
    write_json(Path(args.output), merged)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
