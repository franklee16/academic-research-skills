#!/usr/bin/env python3
"""Deterministic helpers for local paper storage and deduplication."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
from urllib.parse import quote

DEFAULT_LIBRARY_ENV_VAR = "AUTOPAPER_LIBRARY_DIR"
CONFIG_FILE_ENV_VAR = "AUTOPAPER_CONFIG_FILE"
HTML_INDEX_FILENAME = "papers.html"
TITLE_SIMILARITY_THRESHOLD = 0.92
CANONICAL_BUNDLE_FILES = {
    "paper_pdf": "paper.pdf",
    "metadata_json": "metadata.json",
    "pdf_analysis_json": "pdf_analysis.json",
    "analysis_json": "analysis.json",
    "report_tex": "report.tex",
    "report_pdf": "report.pdf",
}
CANONICAL_BUNDLE_DIRS = {
    "images_dir": "images",
    "sources_dir": "sources",
}
DOI_PREFIXES = (
    "https://doi.org/",
    "http://doi.org/",
    "doi:",
)
ARXIV_PREFIXES = (
    "https://arxiv.org/abs/",
    "http://arxiv.org/abs/",
    "https://arxiv.org/pdf/",
    "http://arxiv.org/pdf/",
    "arxiv:",
)


def default_config_path() -> Path:
    override = os.environ.get(CONFIG_FILE_ENV_VAR)
    if override:
        return Path(override).expanduser()

    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config_home:
        return Path(xdg_config_home).expanduser() / "autopaper-skill" / "config.json"

    return Path.home() / ".config" / "autopaper-skill" / "config.json"


def load_user_config(config_path: Path | None = None) -> dict[str, Any]:
    path = config_path or default_config_path()
    if not path.exists():
        return {}
    payload = load_json(path)
    if not isinstance(payload, dict):  # load_json already enforces this, kept for clarity.
        raise ValueError(f"{path} does not contain a JSON object")
    return payload


def write_user_config(config: dict[str, Any], config_path: Path | None = None) -> Path:
    path = config_path or default_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    write_json(path, config)
    return path


def is_under_path(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def is_temporary_library_dir(path: Path) -> bool:
    resolved = path.expanduser().resolve()
    temporary_roots = {
        Path(tempfile.gettempdir()).resolve(),
        Path("/tmp").resolve(),
        Path("/var/tmp").resolve(),
    }
    return any(is_under_path(resolved, root) for root in temporary_roots)


def validate_library_dir(library_dir: Path, allow_temp_library: bool = False) -> Path:
    resolved = library_dir.expanduser().resolve()
    if is_temporary_library_dir(resolved) and not allow_temp_library:
        raise ValueError(
            f"Refusing to use temporary directory as durable paper library: {resolved}. "
            "Choose a stable library root, set AUTOPAPER_LIBRARY_DIR, or pass "
            "--allow-temp-library only for tests and disposable experiments."
        )
    return resolved


def resolve_library_dir(
    library_dir: str | None,
    allow_temp_library: bool = False,
) -> Path:
    if library_dir:
        return validate_library_dir(Path(library_dir), allow_temp_library)

    env_value = os.environ.get(DEFAULT_LIBRARY_ENV_VAR)
    if env_value:
        return validate_library_dir(Path(env_value), allow_temp_library)

    config = load_user_config()
    config_value = config.get("library_dir")
    if config_value:
        return validate_library_dir(Path(str(config_value)), allow_temp_library)

    raise ValueError(
        "No paper library root configured. Pass --library-dir, set "
        f"{DEFAULT_LIBRARY_ENV_VAR}, or run "
        "`python3 scripts/paper_store.py config set-library --library-dir <dir>`."
    )


def set_default_library_dir(library_dir: str, allow_temp_library: bool = False) -> dict[str, Any]:
    resolved = validate_library_dir(Path(library_dir), allow_temp_library)
    config = load_user_config()
    config["library_dir"] = str(resolved)
    config_path = write_user_config(config)
    return {
        "config_path": str(config_path.resolve()),
        "library_dir": str(resolved),
    }


def collapse_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_text(value: str | None) -> str:
    if not value:
        return ""
    normalized = unicodedata.normalize("NFKD", str(value))
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^a-z0-9]+", " ", ascii_value.lower())
    return collapse_whitespace(cleaned)


def normalize_doi(value: str | None) -> str | None:
    if not value:
        return None
    doi = str(value).strip()
    lower = doi.lower()
    for prefix in DOI_PREFIXES:
        if lower.startswith(prefix):
            doi = doi[len(prefix) :]
            break
    doi = doi.strip().lower()
    return doi or None


def normalize_arxiv_id(value: str | None) -> str | None:
    if not value:
        return None
    arxiv_id = str(value).strip()
    lower = arxiv_id.lower()
    for prefix in ARXIV_PREFIXES:
        if lower.startswith(prefix):
            arxiv_id = arxiv_id[len(prefix) :]
            break
    arxiv_id = arxiv_id.strip()
    if arxiv_id.lower().endswith(".pdf"):
        arxiv_id = arxiv_id[:-4]
    arxiv_id = arxiv_id.lower()
    return arxiv_id or None


def safe_identifier(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", value)
    safe = safe.strip("._-")
    return safe or "unknown"


def title_hash(title: str | None) -> str:
    normalized = normalize_text(title)
    digest = hashlib.sha1(normalized.encode("utf-8")).hexdigest()
    return digest[:12]


def compute_paper_id(metadata: dict[str, Any]) -> str:
    doi = normalize_doi(metadata.get("doi"))
    if doi:
        return f"doi-{safe_identifier(doi)}"

    arxiv_id = normalize_arxiv_id(metadata.get("arxiv_id"))
    if arxiv_id:
        return f"arxiv-{safe_identifier(arxiv_id)}"

    return f"title-{title_hash(metadata.get('title'))}"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} does not contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def normalize_authors(authors: Any) -> list[dict[str, Any]]:
    if not isinstance(authors, list):
        return []
    normalized: list[dict[str, Any]] = []
    for author in authors:
        if not isinstance(author, dict):
            continue
        item = dict(author)
        item["name"] = collapse_whitespace(str(item.get("name", "")))
        if not item["name"]:
            continue
        item["affiliation"] = item.get("affiliation") or None
        item["citation_count"] = item.get("citation_count")
        item["h_index"] = item.get("h_index")
        item["is_high_impact"] = bool(item.get("is_high_impact"))
        item["evidence_source"] = item.get("evidence_source") or None
        normalized.append(item)
    return normalized


def normalize_sources(sources: Any) -> list[dict[str, Any]]:
    if not isinstance(sources, list):
        return []
    normalized: list[dict[str, Any]] = []
    for source in sources:
        if not isinstance(source, dict):
            continue
        item = dict(source)
        item["source_name"] = collapse_whitespace(str(item.get("source_name", "")))
        if not item["source_name"]:
            continue
        item["source_type"] = item.get("source_type") or None
        item["source_url"] = item.get("source_url") or None
        item["is_official"] = bool(item.get("is_official"))
        item["retrieved_at"] = item.get("retrieved_at") or None
        fields = item.get("fields")
        item["fields"] = [str(field) for field in fields] if isinstance(fields, list) else []
        normalized.append(item)
    return normalized


def prepare_record(payload: dict[str, Any]) -> dict[str, Any]:
    record = dict(payload)
    record["title"] = collapse_whitespace(str(record.get("title", "")))
    record["doi"] = normalize_doi(record.get("doi"))
    record["arxiv_id"] = normalize_arxiv_id(record.get("arxiv_id"))
    record["authors"] = normalize_authors(record.get("authors"))
    record["metadata_sources"] = normalize_sources(record.get("metadata_sources"))
    record["indexing_notes"] = list(record.get("indexing_notes") or [])
    record["notes"] = list(record.get("notes") or [])
    record["paper_id"] = str(record.get("paper_id") or compute_paper_id(record))
    record["pdf_path"] = record.get("pdf_path") or None
    record["landing_page"] = record.get("landing_page") or None
    record["published_at"] = record.get("published_at") or None
    record["abstract_en"] = record.get("abstract_en") or None
    record["abstract_zh"] = record.get("abstract_zh") or None
    record["venue"] = record.get("venue") or None
    record["venue_type"] = record.get("venue_type") or None
    record["citation_count"] = record.get("citation_count")
    return record


def bundle_layout(library_dir: Path, metadata: dict[str, Any]) -> dict[str, Any]:
    record = prepare_record(metadata)
    bundle_dir = library_dir / record["paper_id"]
    paths: dict[str, Any] = {
        "paper_id": record["paper_id"],
        "bundle_dir": str(bundle_dir.resolve()),
    }
    for key, dirname in CANONICAL_BUNDLE_DIRS.items():
        paths[key] = str((bundle_dir / dirname).resolve())
    for key, filename in CANONICAL_BUNDLE_FILES.items():
        paths[key] = str((bundle_dir / filename).resolve())
    return paths


def ensure_bundle_dirs(paths: dict[str, Any]) -> None:
    Path(str(paths["bundle_dir"])).mkdir(parents=True, exist_ok=True)
    for key in CANONICAL_BUNDLE_DIRS:
        Path(str(paths[key])).mkdir(parents=True, exist_ok=True)


def validate_bundle_dir(bundle_dir: Path) -> dict[str, Any]:
    metadata_path = bundle_dir / CANONICAL_BUNDLE_FILES["metadata_json"]
    metadata = load_json(metadata_path) if metadata_path.exists() else {}
    expected_name = prepare_record(metadata).get("paper_id") if metadata else None
    present = []
    missing = []
    for filename in CANONICAL_BUNDLE_FILES.values():
        target = bundle_dir / filename
        (present if target.exists() else missing).append(filename)
    for dirname in CANONICAL_BUNDLE_DIRS.values():
        target = bundle_dir / dirname
        (present if target.is_dir() else missing).append(dirname + "/")
    name_matches = expected_name in (None, bundle_dir.name)
    required = {
        CANONICAL_BUNDLE_FILES["metadata_json"],
        CANONICAL_BUNDLE_DIRS["images_dir"] + "/",
        CANONICAL_BUNDLE_DIRS["sources_dir"] + "/",
    }
    required_missing = [item for item in missing if item in required]
    return {
        "bundle_dir": str(bundle_dir.resolve()),
        "metadata_path": str(metadata_path.resolve()),
        "expected_paper_id": expected_name,
        "bundle_dir_name_matches_paper_id": name_matches,
        "present": present,
        "missing": missing,
        "required_missing": required_missing,
        "valid": not required_missing and name_matches,
    }


def scan_library(library_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    records: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    if not library_dir.exists():
        return records, errors

    for metadata_path in sorted(library_dir.rglob("metadata.json")):
        relative_parts = metadata_path.relative_to(library_dir).parts
        if CANONICAL_BUNDLE_DIRS["sources_dir"] in relative_parts[:-1]:
            continue
        try:
            record = prepare_record(load_json(metadata_path))
            record["storage_dir"] = str(metadata_path.parent.resolve())
            records.append(record)
        except Exception as exc:  # pragma: no cover - defensive path
            errors.append(
                {
                    "path": str(metadata_path),
                    "error": str(exc),
                }
            )
    return records, errors


def first_present(*values: Any) -> str:
    for value in values:
        if value not in (None, "", []):
            return str(value)
    return ""


def paper_year(record: dict[str, Any]) -> str:
    value = first_present(record.get("year"), record.get("published_at"), record.get("publication_date"))
    match = re.search(r"\b(19|20)\d{2}\b", value)
    return match.group(0) if match else ""


def authors_label(authors: Any, limit: int = 3) -> str:
    normalized = normalize_authors(authors)
    names = [author["name"] for author in normalized if author.get("name")]
    if not names:
        return ""
    if len(names) > limit:
        return ", ".join(names[:limit]) + ", et al."
    return ", ".join(names)


def html_text(value: Any) -> str:
    text = "" if value is None else str(value)
    return html.escape(text, quote=True)


def file_href(library_dir: Path, target: Path) -> str:
    resolved_library = library_dir.resolve()
    resolved_target = target.resolve()
    try:
        relative = resolved_target.relative_to(resolved_library)
        return "/".join(quote(part) for part in relative.parts)
    except ValueError:
        return quote(str(resolved_target))


def existing_bundle_file(record: dict[str, Any], filename: str) -> Path | None:
    storage_dir = record.get("storage_dir")
    if not storage_dir:
        return None
    target = Path(str(storage_dir)) / filename
    return target if target.exists() else None


def link_or_dash(library_dir: Path, target: Path | None, label: str) -> str:
    if target is None:
        return '<span class="muted">-</span>'
    return f'<a href="{html_text(file_href(library_dir, target))}">{html_text(label)}</a>'


def pdf_view_button_or_dash(
    library_dir: Path,
    target: Path | None,
    label: str,
    title: str,
) -> str:
    if target is None:
        return '<span class="muted">-</span>'
    href = html_text(file_href(library_dir, target))
    button_label = html_text(label)
    button_title = html_text(title)
    return (
        f'<button type="button" class="pdf-button" '
        f'data-pdf-href="{href}" data-pdf-title="{button_title}">{button_label}</button>'
    )


def venue_group_label(record: dict[str, Any]) -> str:
    venue = first_present(record.get("venue"), record.get("publication_venue"))
    if not venue:
        return "Unspecified Venue"
    cleaned = re.sub(r"\((?:19|20)\d{2}\)", " ", venue)
    cleaned = re.sub(r"\b(?:19|20)\d{2}\b", " ", cleaned)
    cleaned = re.sub(
        r"(?:[\s,;:/|_-]+(?:poster|oral|spotlight|talk|workshop|demo|findings)\b)+\s*$",
        " ",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.strip(" ,;:-/|")
    return cleaned or "Unspecified Venue"


def record_sort_key(record: dict[str, Any]) -> tuple[int, str, str]:
    year = paper_year(record)
    year_value = int(year) if year.isdigit() else 0
    title = normalize_text(record.get("title"))
    paper_id = str(record.get("paper_id") or "")
    return (-year_value, title, paper_id)


def venue_group_sort_key(item: tuple[str, list[dict[str, Any]]]) -> tuple[int, str]:
    label, _records = item
    is_unspecified = int(label == "Unspecified Venue")
    return (is_unspecified, normalize_text(label))


def render_html_index(
    library_dir: Path,
    records: list[dict[str, Any]],
    errors: list[dict[str, str]] | None = None,
) -> str:
    sorted_records = sorted(records, key=record_sort_key)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    grouped_records: dict[str, list[dict[str, Any]]] = {}
    for record in sorted_records:
        grouped_records.setdefault(venue_group_label(record), []).append(record)

    sections: list[str] = []
    for group_label, group_records in sorted(grouped_records.items(), key=venue_group_sort_key):
        rows: list[str] = []
        years = sorted(
            {year for year in (paper_year(record) for record in group_records) if year},
            reverse=True,
        )
        years_label = ", ".join(years) if years else "unknown year"
        for record in group_records:
            title = first_present(record.get("title"), record.get("paper_id"), "Untitled")
            authors = authors_label(record.get("authors"))
            venue = first_present(record.get("venue"), record.get("venue_type"))
            year = paper_year(record)
            paper_id = first_present(record.get("paper_id"))
            citation_count = first_present(record.get("citation_count"))
            summary = first_present(
                record.get("summary_one_liner"),
                record.get("abstract_zh"),
                record.get("abstract_en"),
            )
            if len(summary) > 320:
                summary = summary[:317].rstrip() + "..."
            storage_dir = Path(str(record.get("storage_dir", "")))
            metadata_link = link_or_dash(library_dir, storage_dir / "metadata.json", "metadata")
            pdf_link = pdf_view_button_or_dash(
                library_dir,
                existing_bundle_file(record, "paper.pdf"),
                "view paper",
                f"{title} - paper.pdf",
            )
            report_link = pdf_view_button_or_dash(
                library_dir,
                existing_bundle_file(record, "report.pdf"),
                "view report",
                f"{title} - report.pdf",
            )
            tex_link = link_or_dash(library_dir, existing_bundle_file(record, "report.tex"), "tex")
            landing_page = first_present(record.get("landing_page"))
            landing_link = (
                f'<a href="{html_text(landing_page)}">source</a>'
                if landing_page.startswith(("http://", "https://"))
                else '<span class="muted">-</span>'
            )
            search_text = " ".join(
                [
                    title,
                    authors,
                    venue,
                    group_label,
                    year,
                    paper_id,
                    summary,
                    first_present(record.get("doi")),
                    first_present(record.get("arxiv_id")),
                ]
            )
            rows.append(
                "          <tr "
                f'data-search="{html_text(normalize_text(search_text))}" '
                f'data-year="{html_text(year or "unknown")}" '
                f'data-venue="{html_text(normalize_text(group_label) or "unknown")}">\n'
                f"            <td><div class=\"title\">{html_text(title)}</div>"
                f"<div class=\"summary\">{html_text(summary or '暂无摘要。')}</div></td>\n"
                f"            <td>{html_text(authors or '暂无信息。')}</td>\n"
                f"            <td>{html_text(year or '暂无')}</td>\n"
                f"            <td>{html_text(venue or '暂无信息。')}</td>\n"
                f"            <td>{html_text(str(citation_count) if citation_count else '暂无')}</td>\n"
                f"            <td><code>{html_text(paper_id)}</code></td>\n"
                f"            <td class=\"links\">{pdf_link} {report_link} {tex_link} {metadata_link} {landing_link}</td>\n"
                "          </tr>"
            )
        sections.append(
            "    <details class=\"venue-group\" open>\n"
            "      <summary>"
            f"<span class=\"venue-heading\">{html_text(group_label)}</span>"
            f"<span class=\"group-meta\"><span data-group-count>{len(group_records)}</span>/{len(group_records)} papers | years: {html_text(years_label)}</span>"
            "</summary>\n"
            "      <table>\n"
            "        <thead>\n"
            "          <tr>\n"
            "            <th>Title</th>\n"
            "            <th>Authors</th>\n"
            "            <th>Year</th>\n"
            "            <th>Venue</th>\n"
            "            <th>Cites</th>\n"
            "            <th>Paper ID</th>\n"
            "            <th>Files</th>\n"
            "          </tr>\n"
            "        </thead>\n"
            "        <tbody>\n"
            f"{chr(10).join(rows)}\n"
            "        </tbody>\n"
            "      </table>\n"
            "    </details>"
        )

    if not sections:
        sections.append('    <div class="empty">No papers found in this library.</div>')

    error_items = ""
    if errors:
        items = "\n".join(
            f"      <li><code>{html_text(error.get('path'))}</code>: {html_text(error.get('error'))}</li>"
            for error in errors
        )
        error_items = (
            "  <section class=\"errors\">\n"
            "    <h2>Scan Warnings</h2>\n"
            "    <ul>\n"
            f"{items}\n"
            "    </ul>\n"
            "  </section>\n"
        )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Paper Library</title>
  <style>
    :root {{ color-scheme: light; --border: #d0d7de; --border-soft: #eaeef2; --muted: #59636e; --bg: #f6f8fa; --panel: #fff; --text: #1f2328; --accent: #0969da; --accent-soft: #ddf4ff; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: var(--text); background: #f3f5f7; }}
    header {{ padding: 24px 28px 16px; border-bottom: 1px solid var(--border); background: var(--panel); }}
    h1 {{ margin: 0 0 8px; font-size: 26px; font-weight: 650; letter-spacing: 0; }}
    .meta {{ color: var(--muted); font-size: 13px; }}
    .app-shell {{ display: grid; grid-template-columns: minmax(560px, 0.85fr) minmax(640px, 1.15fr); gap: 18px; padding: 18px 20px 28px; align-items: start; }}
    .library-pane, .preview-pane {{ min-width: 0; }}
    .toolbar {{ display: flex; gap: 12px; align-items: center; margin-bottom: 14px; padding: 12px; border: 1px solid var(--border); background: var(--panel); border-radius: 6px; }}
    input[type="search"] {{ width: min(720px, 100%); padding: 10px 12px; border: 1px solid var(--border); border-radius: 6px; font-size: 15px; background: #fff; color: var(--text); }}
    input[type="search"]:focus {{ outline: 2px solid var(--accent-soft); border-color: var(--accent); }}
    .preview-pane {{ position: sticky; top: 16px; height: calc(100vh - 32px); border: 1px solid var(--border); border-radius: 6px; overflow: hidden; background: var(--panel); }}
    .viewer-bar {{ display: flex; justify-content: space-between; gap: 12px; align-items: center; min-height: 44px; padding: 10px 12px; border-bottom: 1px solid var(--border); background: var(--bg); }}
    #viewer-title {{ overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
    .viewer-empty {{ display: grid; place-items: center; height: calc(100vh - 78px); padding: 24px; color: var(--muted); text-align: center; line-height: 1.5; }}
    #pdf-frame {{ display: block; width: 100%; height: calc(100vh - 78px); border: 0; background: #fff; }}
    #pdf-frame[hidden], .viewer-empty[hidden], #viewer-close[hidden] {{ display: none; }}
    .venue-group {{ margin: 0 0 14px; border: 1px solid var(--border); border-radius: 6px; overflow: hidden; background: var(--panel); }}
    .venue-group[hidden] {{ display: none; }}
    .venue-group summary {{ display: flex; justify-content: space-between; gap: 16px; align-items: center; cursor: pointer; padding: 12px 14px; background: #f8fafc; border-bottom: 1px solid var(--border-soft); }}
    .venue-heading {{ font-weight: 650; font-size: 16px; }}
    .group-meta {{ color: var(--muted); font-size: 13px; white-space: nowrap; }}
    table {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
    th, td {{ border-bottom: 1px solid var(--border-soft); padding: 11px 10px; text-align: left; vertical-align: top; }}
    tbody tr:hover {{ background: #f8fafc; }}
    th {{ background: #fbfcfd; font-size: 12px; color: var(--muted); font-weight: 650; text-transform: uppercase; }}
    td {{ font-size: 13px; }}
    th:nth-child(1), td:nth-child(1) {{ width: 36%; }}
    th:nth-child(2), td:nth-child(2) {{ width: 15%; }}
    th:nth-child(3), td:nth-child(3) {{ width: 7%; }}
    th:nth-child(4), td:nth-child(4) {{ width: 12%; }}
    th:nth-child(5), td:nth-child(5) {{ width: 7%; }}
    th:nth-child(6), td:nth-child(6) {{ width: 11%; }}
    th:nth-child(7), td:nth-child(7) {{ width: 12%; }}
    .title {{ font-weight: 650; line-height: 1.35; }}
    .summary {{ margin-top: 6px; color: var(--muted); line-height: 1.45; }}
    .links a, .pdf-button {{ display: inline-block; margin: 0 6px 6px 0; }}
    .pdf-button, .preview-pane button {{ border: 1px solid var(--border); border-radius: 6px; background: #fff; color: var(--accent); cursor: pointer; font: inherit; padding: 3px 8px; }}
    .pdf-button:hover, .preview-pane button:hover {{ background: var(--accent-soft); border-color: #54aeff; }}
    code {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 12px; word-break: break-all; }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .muted, .empty {{ color: var(--muted); }}
    .empty {{ padding: 20px; border: 1px solid var(--border); border-radius: 6px; background: var(--panel); }}
    .errors {{ margin-top: 18px; padding: 12px 16px; border: 1px solid #d4a72c; border-radius: 6px; background: #fff8c5; }}
    @media (max-width: 900px) {{
      header {{ padding-left: 16px; padding-right: 16px; }}
      .app-shell {{ display: block; padding: 14px 16px 24px; }}
      .preview-pane {{ position: static; height: auto; margin-top: 16px; }}
      .viewer-empty, #pdf-frame {{ height: 70vh; }}
      table {{ display: block; overflow-x: auto; white-space: normal; }}
      th, td {{ min-width: 120px; }}
      th:nth-child(1), td:nth-child(1) {{ min-width: 300px; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Paper Library</h1>
    <div class="meta">{len(sorted_records)} papers | generated at {html_text(generated_at)} | root: <code>{html_text(str(library_dir.resolve()))}</code></div>
  </header>
  <main class="app-shell">
    <section class="library-pane">
      <div class="toolbar">
        <input id="search" type="search" placeholder="Search title, author, venue, year, paper id, DOI, arXiv...">
        <span id="count" class="meta">{len(sorted_records)} shown</span>
      </div>
      <section id="papers">
{chr(10).join(sections)}
      </section>
{error_items}    </section>
    <aside id="viewer" class="preview-pane" aria-label="PDF preview">
      <div class="viewer-bar">
        <strong id="viewer-title">PDF Preview</strong>
        <button id="viewer-close" type="button" hidden>Close</button>
      </div>
      <div id="viewer-empty" class="viewer-empty">Select a paper or report from the list to preview it here.</div>
      <iframe id="pdf-frame" title="PDF preview" hidden></iframe>
    </aside>
  </main>
  <script>
    const input = document.getElementById('search');
    const rows = Array.from(document.querySelectorAll('#papers tr[data-search]'));
    const groups = Array.from(document.querySelectorAll('.venue-group'));
    const count = document.getElementById('count');
    const viewer = document.getElementById('viewer');
    const viewerTitle = document.getElementById('viewer-title');
    const pdfFrame = document.getElementById('pdf-frame');
    const viewerClose = document.getElementById('viewer-close');
    const viewerEmpty = document.getElementById('viewer-empty');
    function normalize(value) {{
      return value.toLowerCase().normalize('NFKD').replace(/[^a-z0-9]+/g, ' ').trim();
    }}
    function applyFilter() {{
      const terms = normalize(input.value).split(' ').filter(Boolean);
      let visible = 0;
      for (const row of rows) {{
        const haystack = row.dataset.search || '';
        const match = terms.every(term => haystack.includes(term));
        row.style.display = match ? '' : 'none';
        if (match) visible += 1;
      }}
      for (const group of groups) {{
        const groupRows = Array.from(group.querySelectorAll('tr[data-search]'));
        const groupVisible = groupRows.filter(row => row.style.display !== 'none').length;
        const groupCount = group.querySelector('[data-group-count]');
        if (groupCount) groupCount.textContent = groupVisible;
        group.hidden = groupVisible === 0;
      }}
      count.textContent = visible + ' shown';
    }}
    for (const button of document.querySelectorAll('[data-pdf-href]')) {{
      button.addEventListener('click', () => {{
        pdfFrame.src = button.dataset.pdfHref || '';
        viewerTitle.textContent = button.dataset.pdfTitle || 'PDF Preview';
        pdfFrame.hidden = false;
        viewerEmpty.hidden = true;
        viewerClose.hidden = false;
        viewer.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      }});
    }}
    viewerClose.addEventListener('click', () => {{
      pdfFrame.removeAttribute('src');
      pdfFrame.hidden = true;
      viewerEmpty.hidden = false;
      viewerClose.hidden = true;
      viewerTitle.textContent = 'PDF Preview';
    }});
    input.addEventListener('input', applyFilter);
  </script>
</body>
</html>
"""


def refresh_html_index(library_dir: Path, output_file: Path | None = None) -> dict[str, Any]:
    records, errors = scan_library(library_dir)
    index_path = output_file or (library_dir / HTML_INDEX_FILENAME)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(render_html_index(library_dir, records, errors), encoding="utf-8")
    return {
        "library_dir": str(library_dir.resolve()),
        "html_index": str(index_path.resolve()),
        "count": len(records),
        "errors": errors,
    }


def title_similarity(left: str | None, right: str | None) -> float:
    return SequenceMatcher(None, normalize_text(left), normalize_text(right)).ratio()


def find_duplicate(candidate: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
    prepared = prepare_record(candidate)
    candidate_id = prepared["paper_id"]
    candidate_title = prepared.get("title") or ""
    candidate_title_key = normalize_text(candidate_title)

    for record in records:
        if record.get("paper_id") == candidate_id:
            return {
                "matched": True,
                "reason": "paper_id",
                "score": 1.0,
                "paper_id": record.get("paper_id"),
                "storage_dir": record.get("storage_dir"),
                "title": record.get("title"),
            }

    if candidate_title_key:
        for record in records:
            title = record.get("title") or ""
            if normalize_text(title) == candidate_title_key:
                return {
                    "matched": True,
                    "reason": "title_exact",
                    "score": 1.0,
                    "paper_id": record.get("paper_id"),
                    "storage_dir": record.get("storage_dir"),
                    "title": title,
                }

    best_match: dict[str, Any] | None = None
    for record in records:
        title = record.get("title") or ""
        if not title:
            continue
        score = title_similarity(candidate_title, title)
        if score >= TITLE_SIMILARITY_THRESHOLD:
            if best_match is None or score > best_match["score"]:
                best_match = {
                    "matched": True,
                    "reason": "title_near",
                    "score": round(score, 4),
                    "paper_id": record.get("paper_id"),
                    "storage_dir": record.get("storage_dir"),
                    "title": title,
                }

    return best_match or {
        "matched": False,
        "reason": None,
        "score": 0.0,
        "paper_id": None,
        "storage_dir": None,
        "title": None,
    }


def merge_records(existing: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    merged = dict(existing)
    fresh = prepare_record(incoming)

    for key, value in fresh.items():
        if key in {"authors", "metadata_sources", "indexing_notes", "notes"}:
            continue
        if key == "paper_id":
            merged[key] = merged.get(key) or value
            continue
        if value not in (None, "", []):
            merged[key] = value

    merged["authors"] = merge_authors(existing.get("authors"), fresh.get("authors"))
    merged["metadata_sources"] = merge_sources(
        existing.get("metadata_sources"),
        fresh.get("metadata_sources"),
    )
    merged["indexing_notes"] = merge_scalar_lists(
        existing.get("indexing_notes"),
        fresh.get("indexing_notes"),
    )
    merged["notes"] = merge_scalar_lists(existing.get("notes"), fresh.get("notes"))
    return prepare_record(merged)


def merge_scalar_lists(left: Any, right: Any) -> list[Any]:
    merged: list[Any] = []
    seen: set[str] = set()
    for values in (left, right):
        if not isinstance(values, list):
            continue
        for value in values:
            marker = json.dumps(value, ensure_ascii=False, sort_keys=True)
            if marker in seen:
                continue
            seen.add(marker)
            merged.append(value)
    return merged


def merge_authors(left: Any, right: Any) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for collection in (normalize_authors(left), normalize_authors(right)):
        for author in collection:
            key = normalize_text(author.get("name"))
            current = merged.get(key, {})
            combined = dict(current)
            for field, value in author.items():
                if value not in (None, "", []):
                    combined[field] = value
            merged[key] = combined
    return list(merged.values())


def merge_sources(left: Any, right: Any) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for collection in (normalize_sources(left), normalize_sources(right)):
        for source in collection:
            key = "|".join(
                [
                    source.get("source_name") or "",
                    source.get("source_url") or "",
                    source.get("source_type") or "",
                ]
            )
            current = merged.get(key, {})
            combined = dict(current)
            for field, value in source.items():
                if field == "fields":
                    combined[field] = merge_scalar_lists(current.get("fields"), value)
                elif value not in (None, "", []):
                    combined[field] = value
            merged[key] = combined
    return list(merged.values())


def safe_copy(source: Path, destination: Path) -> None:
    if source.resolve() == destination.resolve():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def safe_copy_tree_contents(source_dir: Path, destination_dir: Path) -> None:
    if not source_dir.exists():
        return
    if not source_dir.is_dir():
        raise ValueError(f"{source_dir} is not a directory")
    if source_dir.resolve() == destination_dir.resolve():
        return
    destination_dir.mkdir(parents=True, exist_ok=True)
    for source_path in sorted(source_dir.rglob("*")):
        if source_path.is_dir():
            continue
        relative = source_path.relative_to(source_dir)
        safe_copy(source_path, destination_dir / relative)


def upsert_bundle(
    library_dir: Path,
    metadata: dict[str, Any],
    pdf_source: Path | None = None,
    pdf_analysis_file: Path | None = None,
    analysis_file: Path | None = None,
    report_file: Path | None = None,
    report_pdf_file: Path | None = None,
    images_dir: Path | None = None,
    sources_dir: Path | None = None,
    refresh_index: bool = True,
) -> dict[str, Any]:
    library_dir.mkdir(parents=True, exist_ok=True)
    records, _errors = scan_library(library_dir)
    candidate = prepare_record(metadata)
    duplicate = find_duplicate(candidate, records)

    created = not duplicate["matched"]
    if duplicate["matched"]:
        target_dir = Path(str(duplicate["storage_dir"]))
        existing_metadata_path = target_dir / "metadata.json"
        existing = load_json(existing_metadata_path) if existing_metadata_path.exists() else {}
        final_record = merge_records(existing, candidate)
        duplicate_reason = duplicate["reason"]
    else:
        target_dir = library_dir / candidate["paper_id"]
        final_record = candidate
        duplicate_reason = None

    target_dir.mkdir(parents=True, exist_ok=True)
    layout_paths = bundle_layout(library_dir, final_record)
    layout_paths["bundle_dir"] = str(target_dir.resolve())
    for key, dirname in CANONICAL_BUNDLE_DIRS.items():
        layout_paths[key] = str((target_dir / dirname).resolve())
    for key, filename in CANONICAL_BUNDLE_FILES.items():
        layout_paths[key] = str((target_dir / filename).resolve())
    ensure_bundle_dirs(layout_paths)

    final_record["paper_id"] = final_record.get("paper_id") or candidate["paper_id"]
    final_record["bundle_dir"] = str(target_dir.resolve())
    final_record["images_dir"] = layout_paths["images_dir"]
    final_record["sources_dir"] = layout_paths["sources_dir"]

    if pdf_source is not None:
        pdf_destination = Path(str(layout_paths["paper_pdf"]))
        safe_copy(pdf_source, pdf_destination)
        final_record["pdf_path"] = str(pdf_destination.resolve())

    if pdf_analysis_file is not None:
        pdf_analysis_destination = Path(str(layout_paths["pdf_analysis_json"]))
        safe_copy(pdf_analysis_file, pdf_analysis_destination)
        final_record["pdf_analysis_path"] = str(pdf_analysis_destination.resolve())

    if analysis_file is not None:
        analysis_destination = Path(str(layout_paths["analysis_json"]))
        safe_copy(analysis_file, analysis_destination)
        final_record["analysis_path"] = str(analysis_destination.resolve())

    if report_file is not None:
        report_tex_destination = Path(str(layout_paths["report_tex"]))
        safe_copy(report_file, report_tex_destination)
        final_record["report_tex_path"] = str(report_tex_destination.resolve())

    if report_pdf_file is not None:
        report_pdf_destination = Path(str(layout_paths["report_pdf"]))
        safe_copy(report_pdf_file, report_pdf_destination)
        final_record["report_pdf_path"] = str(report_pdf_destination.resolve())

    if images_dir is not None:
        safe_copy_tree_contents(images_dir, Path(str(layout_paths["images_dir"])))

    if sources_dir is not None:
        safe_copy_tree_contents(sources_dir, Path(str(layout_paths["sources_dir"])))

    write_json(Path(str(layout_paths["metadata_json"])), final_record)
    index_payload = refresh_html_index(library_dir) if refresh_index else None

    payload = {
        "created": created,
        "paper_id": final_record["paper_id"],
        "target_dir": str(target_dir.resolve()),
        "duplicate_reason": duplicate_reason,
        "pdf_path": final_record.get("pdf_path"),
        "paths": layout_paths,
    }
    if index_payload is not None:
        payload["html_index"] = index_payload["html_index"]
    return payload


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local paper storage helpers.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    config_parser = subparsers.add_parser("config", help="Read or write paper_store defaults.")
    config_subparsers = config_parser.add_subparsers(dest="config_command", required=True)
    get_library_parser = config_subparsers.add_parser("get-library", help="Print the configured library root.")
    get_library_parser.add_argument("--json", action="store_true")
    set_library_parser = config_subparsers.add_parser("set-library", help="Persist the default library root.")
    set_library_parser.add_argument("--library-dir", required=True)
    set_library_parser.add_argument(
        "--allow-temp-library",
        action="store_true",
        help="Allow /tmp or another temporary directory as the library root.",
    )
    set_library_parser.add_argument("--json", action="store_true")

    scan_parser = subparsers.add_parser("scan", help="Scan a paper library.")
    scan_parser.add_argument("--library-dir")
    scan_parser.add_argument(
        "--allow-temp-library",
        action="store_true",
        help="Allow /tmp or another temporary directory as the library root.",
    )
    scan_parser.add_argument("--json", action="store_true")

    match_parser = subparsers.add_parser("match", help="Match a candidate against a library.")
    match_parser.add_argument("--library-dir")
    match_parser.add_argument(
        "--allow-temp-library",
        action="store_true",
        help="Allow /tmp or another temporary directory as the library root.",
    )
    match_parser.add_argument("--metadata-file", required=True)
    match_parser.add_argument("--json", action="store_true")

    layout_parser = subparsers.add_parser("layout", help="Print the canonical bundle layout for a paper.")
    layout_parser.add_argument("--library-dir")
    layout_parser.add_argument(
        "--allow-temp-library",
        action="store_true",
        help="Allow /tmp or another temporary directory as the library root.",
    )
    layout_parser.add_argument("--metadata-file", required=True)
    layout_parser.add_argument("--create-dirs", action="store_true")
    layout_parser.add_argument("--json", action="store_true")

    index_parser = subparsers.add_parser("refresh-index", help="Create or update the library HTML index.")
    index_parser.add_argument("--library-dir")
    index_parser.add_argument("--output-file")
    index_parser.add_argument(
        "--allow-temp-library",
        action="store_true",
        help="Allow /tmp or another temporary directory as the library root.",
    )
    index_parser.add_argument("--json", action="store_true")

    validate_parser = subparsers.add_parser("validate-layout", help="Validate a canonical paper bundle directory.")
    validate_parser.add_argument("--bundle-dir", required=True)
    validate_parser.add_argument("--json", action="store_true")

    upsert_parser = subparsers.add_parser("upsert", help="Create or update a paper bundle.")
    upsert_parser.add_argument("--library-dir")
    upsert_parser.add_argument(
        "--allow-temp-library",
        action="store_true",
        help="Allow /tmp or another temporary directory as the library root.",
    )
    upsert_parser.add_argument("--metadata-file", required=True)
    upsert_parser.add_argument("--pdf-source")
    upsert_parser.add_argument("--pdf-analysis-file")
    upsert_parser.add_argument("--analysis-file")
    upsert_parser.add_argument("--report-file")
    upsert_parser.add_argument("--report-pdf-file")
    upsert_parser.add_argument("--images-dir")
    upsert_parser.add_argument("--sources-dir")
    upsert_parser.add_argument(
        "--no-refresh-index",
        action="store_true",
        help="Skip updating papers.html after the bundle is written.",
    )
    upsert_parser.add_argument("--json", action="store_true")

    return parser.parse_args(argv)


def emit(payload: dict[str, Any], as_json: bool) -> int:
    if as_json:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0

    for key, value in payload.items():
        print(f"{key}: {value}")
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv or sys.argv[1:])

        if args.command == "config":
            if args.config_command == "get-library":
                library_dir = resolve_library_dir(None)
                return emit(
                    {
                        "config_path": str(default_config_path().resolve()),
                        "library_dir": str(library_dir),
                    },
                    args.json,
                )

            if args.config_command == "set-library":
                payload = set_default_library_dir(
                    args.library_dir,
                    allow_temp_library=args.allow_temp_library,
                )
                return emit(payload, args.json)

        if args.command == "scan":
            library_dir = resolve_library_dir(args.library_dir, args.allow_temp_library)
            records, errors = scan_library(library_dir)
            payload = {
                "library_dir": str(library_dir.resolve()),
                "count": len(records),
                "records": records,
                "errors": errors,
            }
            return emit(payload, args.json)

        if args.command == "match":
            library_dir = resolve_library_dir(args.library_dir, args.allow_temp_library)
            candidate = load_json(Path(args.metadata_file))
            records, errors = scan_library(library_dir)
            payload = {
                "candidate": prepare_record(candidate),
                "match": find_duplicate(candidate, records),
                "library_errors": errors,
            }
            return emit(payload, args.json)

        if args.command == "layout":
            library_dir = resolve_library_dir(args.library_dir, args.allow_temp_library)
            payload = bundle_layout(library_dir, load_json(Path(args.metadata_file)))
            if args.create_dirs:
                ensure_bundle_dirs(payload)
            return emit(payload, args.json)

        if args.command == "refresh-index":
            library_dir = resolve_library_dir(args.library_dir, args.allow_temp_library)
            payload = refresh_html_index(
                library_dir=library_dir,
                output_file=Path(args.output_file) if args.output_file else None,
            )
            return emit(payload, args.json)

        if args.command == "validate-layout":
            return emit(validate_bundle_dir(Path(args.bundle_dir)), args.json)

        if args.command == "upsert":
            library_dir = resolve_library_dir(args.library_dir, args.allow_temp_library)
            payload = upsert_bundle(
                library_dir=library_dir,
                metadata=load_json(Path(args.metadata_file)),
                pdf_source=Path(args.pdf_source) if args.pdf_source else None,
                pdf_analysis_file=Path(args.pdf_analysis_file) if args.pdf_analysis_file else None,
                analysis_file=Path(args.analysis_file) if args.analysis_file else None,
                report_file=Path(args.report_file) if args.report_file else None,
                report_pdf_file=Path(args.report_pdf_file) if args.report_pdf_file else None,
                images_dir=Path(args.images_dir) if args.images_dir else None,
                sources_dir=Path(args.sources_dir) if args.sources_dir else None,
                refresh_index=not args.no_refresh_index,
            )
            return emit(payload, args.json)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
