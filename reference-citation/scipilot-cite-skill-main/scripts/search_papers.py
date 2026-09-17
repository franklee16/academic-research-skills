"""
SciPilot-cite :: search_papers.py
多源学术论文并行检索引擎
支持 Semantic Scholar / OpenAlex / Crossref 三源检索、合并去重
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from utils import (
    append_jsonl,
    logger,
    make_bibtex_key,
    normalize_author,
    paper_id_hash,
    rate_limited_request,
    title_similarity,
    utc_now_iso,
)

SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
OPENALEX_URL = "https://api.openalex.org/works"
CROSSREF_URL = "https://api.crossref.org/works"

POLITE_EMAIL = "scipilot@example.org"
USER_AGENT = "SciPilot-cite/1.0 (mailto:scipilot@example.org)"

PREPRINT_VENUE_RE = re.compile(r"\b(arxiv|biorxiv|medrxiv|preprint|chemrxiv|ssrn|techrxiv)\b", re.I)


def _clean_paper(p: dict) -> dict:
    p.setdefault("title", "")
    p.setdefault("authors", [])
    p.setdefault("year", None)
    p.setdefault("venue", "")
    p.setdefault("citation_count", 0)
    p.setdefault("doi", None)
    p.setdefault("abstract", "")
    p.setdefault("source_apis", [])
    p["authors"] = [normalize_author(a) for a in p["authors"]]
    if p["doi"]:
        p["doi"] = str(p["doi"]).lower().strip()
    p["bibtex_key"] = make_bibtex_key(p)
    return p


def search_semantic_scholar(
    query: str, year_range: tuple[int, int], limit: int, fields_of_study: list | None = None
) -> list[dict]:
    """通过 Semantic Scholar API 检索论文。"""
    params = {
        "query": query,
        "year": f"{year_range[0]}-{year_range[1]}",
        "limit": min(limit, 100),
        "fields": "title,authors,year,venue,citationCount,externalIds,abstract,publicationDate",
    }
    if fields_of_study:
        params["fieldsOfStudy"] = ",".join(fields_of_study)
    data = rate_limited_request(
        SEMANTIC_SCHOLAR_URL,
        params=params,
        headers={"User-Agent": USER_AGENT},
        min_interval=1.0,
    )
    if not data or "data" not in data:
        logger.warning("Semantic Scholar returned no data")
        return []
    out: list[dict] = []
    for item in data.get("data") or []:
        doi = (item.get("externalIds") or {}).get("DOI")
        out.append(
            _clean_paper(
                {
                    "title": item.get("title") or "",
                    "authors": [a.get("name", "") for a in (item.get("authors") or [])],
                    "year": item.get("year"),
                    "venue": item.get("venue") or "",
                    "citation_count": item.get("citationCount") or 0,
                    "doi": doi,
                    "abstract": item.get("abstract") or "",
                    "source_apis": ["semantic_scholar"],
                }
            )
        )
    logger.info(f"Semantic Scholar: {len(out)} results for '{query[:50]}'")
    return out


def search_openalex(query: str, year_range: tuple[int, int], limit: int) -> list[dict]:
    """通过 OpenAlex API 检索论文。"""
    params = {
        "search": query,
        "filter": f"from_publication_date:{year_range[0]}-01-01,to_publication_date:{year_range[1]}-12-31",
        "sort": "cited_by_count:desc",
        "per_page": min(limit, 200),
        "mailto": POLITE_EMAIL,
    }
    data = rate_limited_request(
        OPENALEX_URL, params=params, headers={"User-Agent": USER_AGENT}, min_interval=0.5
    )
    if not data or "results" not in data:
        logger.warning("OpenAlex returned no data")
        return []
    out: list[dict] = []
    for item in data["results"]:
        doi = item.get("doi")
        if doi and doi.startswith("https://doi.org/"):
            doi = doi[len("https://doi.org/"):]
        authors = []
        for au in item.get("authorships", []) or []:
            disp = (au.get("author") or {}).get("display_name")
            if disp:
                authors.append(disp)
        venue = ""
        ploc = item.get("primary_location") or {}
        src = ploc.get("source") or {}
        venue = src.get("display_name") or ""
        out.append(
            _clean_paper(
                {
                    "title": item.get("title") or item.get("display_name") or "",
                    "authors": authors,
                    "year": item.get("publication_year"),
                    "venue": venue,
                    "citation_count": item.get("cited_by_count") or 0,
                    "doi": doi,
                    "abstract": _reconstruct_abstract(item.get("abstract_inverted_index")),
                    "source_apis": ["openalex"],
                }
            )
        )
    logger.info(f"OpenAlex: {len(out)} results for '{query[:50]}'")
    return out


def _reconstruct_abstract(inverted: dict | None) -> str:
    """OpenAlex returns abstract as inverted index. Reconstruct linear text."""
    if not inverted or not isinstance(inverted, dict):
        return ""
    positions: list[tuple[int, str]] = []
    for word, pos_list in inverted.items():
        for p in pos_list or []:
            positions.append((p, word))
    positions.sort()
    return " ".join(w for _, w in positions)


def search_crossref(query: str, year_range: tuple[int, int], limit: int) -> list[dict]:
    """通过 Crossref API 检索论文。"""
    params = {
        "query": query,
        "filter": f"from-pub-date:{year_range[0]},until-pub-date:{year_range[1]},type:journal-article",
        "sort": "is-referenced-by-count",
        "order": "desc",
        "rows": min(limit, 100),
        "mailto": POLITE_EMAIL,
    }
    data = rate_limited_request(
        CROSSREF_URL, params=params, headers={"User-Agent": USER_AGENT}, min_interval=0.5
    )
    if not data or "message" not in data:
        logger.warning("Crossref returned no data")
        return []
    out: list[dict] = []
    for item in data["message"].get("items", []):
        title_list = item.get("title") or []
        title = title_list[0] if title_list else ""
        authors = []
        for a in item.get("author") or []:
            authors.append(normalize_author(a))
        venue_list = item.get("container-title") or []
        venue = venue_list[0] if venue_list else ""
        year = None
        for key in ("issued", "published-print", "published-online"):
            dp = (item.get(key) or {}).get("date-parts")
            if dp and dp[0]:
                year = dp[0][0]
                break
        out.append(
            _clean_paper(
                {
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "venue": venue,
                    "citation_count": item.get("is-referenced-by-count") or 0,
                    "doi": item.get("DOI"),
                    "abstract": item.get("abstract", "") or "",
                    "source_apis": ["crossref"],
                }
            )
        )
    logger.info(f"Crossref: {len(out)} results for '{query[:50]}'")
    return out


def merge_and_deduplicate(results: list[list[dict]]) -> list[dict]:
    """合并多源结果并去重。DOI 主键去重；无 DOI 用标题+年份+首作者。"""
    flat: list[dict] = []
    for batch in results:
        flat.extend(batch)

    by_doi: dict[str, dict] = {}
    no_doi: list[dict] = []
    for p in flat:
        if p.get("doi"):
            doi = p["doi"]
            if doi in by_doi:
                by_doi[doi] = _merge_two(by_doi[doi], p)
            else:
                by_doi[doi] = p
        else:
            no_doi.append(p)

    merged: list[dict] = list(by_doi.values())
    for p in no_doi:
        match = None
        for i, m in enumerate(merged):
            if m.get("year") != p.get("year"):
                continue
            if not _first_author_match(m, p):
                continue
            if title_similarity(m.get("title", ""), p.get("title", "")) > 0.9:
                match = i
                break
        if match is not None:
            merged[match] = _merge_two(merged[match], p)
        else:
            merged.append(p)

    merged.sort(key=lambda x: -(x.get("citation_count") or 0))
    return merged


def _first_author_match(p1: dict, p2: dict) -> bool:
    a1 = (p1.get("authors") or [""])[0]
    a2 = (p2.get("authors") or [""])[0]
    if not a1 or not a2:
        return False
    last1 = a1.split()[-1].lower().strip(",.")
    last2 = a2.split()[-1].lower().strip(",.")
    return last1 == last2 and len(last1) > 1


def _merge_two(a: dict, b: dict) -> dict:
    """Crossref DOI 优先；引用量取最大；其他字段取更长/更完整的。"""
    out = dict(a)
    cr_b = "crossref" in (b.get("source_apis") or [])
    cr_a = "crossref" in (a.get("source_apis") or [])
    if cr_b and not cr_a:
        if b.get("doi"):
            out["doi"] = b["doi"]
    if (b.get("citation_count") or 0) > (out.get("citation_count") or 0):
        out["citation_count"] = b["citation_count"]
    for k in ("title", "venue", "abstract"):
        if len(b.get(k) or "") > len(out.get(k) or ""):
            out[k] = b[k]
    if len(b.get("authors") or []) > len(out.get("authors") or []):
        out["authors"] = b["authors"]
    if not out.get("year") and b.get("year"):
        out["year"] = b["year"]
    out["source_apis"] = sorted(set((a.get("source_apis") or []) + (b.get("source_apis") or [])))
    return out


def search_papers(
    query: str,
    year_range: tuple[int, int] = (2021, 2026),
    limit: int = 15,
    fields: list | None = None,
    include_preprint: bool = False,
    log_path: str | None = "evidence_log.jsonl",
) -> list[dict]:
    """主入口：并行三源检索 → 合并去重 → 按引用量降序返回。

    Writes one JSONL record per merged result to `log_path` so the downstream
    audit can prove each paper came from a real API response.
    Pass log_path=None or "" to disable logging (for unit tests).
    """
    per_api = max(limit, int(math.ceil(limit * 3)))
    logger.info(f"Searching '{query}' (limit={limit}, per_api={per_api}, years={year_range})")

    results: list[list[dict]] = []
    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {
            ex.submit(search_semantic_scholar, query, year_range, per_api, fields): "s2",
            ex.submit(search_openalex, query, year_range, per_api): "oa",
            ex.submit(search_crossref, query, year_range, per_api): "cr",
        }
        for fut in as_completed(futures):
            name = futures[fut]
            try:
                results.append(fut.result() or [])
            except Exception as e:
                logger.warning(f"{name} failed: {e}")
                results.append([])

    merged = merge_and_deduplicate(results)
    if not include_preprint:
        merged = [p for p in merged if not PREPRINT_VENUE_RE.search(p.get("venue") or "")]
    logger.info(f"After merge/dedupe: {len(merged)} unique papers")

    if log_path:
        ts = utc_now_iso()
        for p in merged:
            append_jsonl(
                log_path,
                {
                    "timestamp": ts,
                    "event": "search_result",
                    "paper_id": paper_id_hash(p),
                    "query": query,
                    "title": p.get("title"),
                    "doi": p.get("doi"),
                    "year": p.get("year"),
                    "venue": p.get("venue"),
                    "first_author": (p.get("authors") or [""])[0],
                    "citation_count": p.get("citation_count"),
                    "source_apis": p.get("source_apis"),
                },
            )
        logger.info(f"Wrote {len(merged)} search-result records to {log_path}")
    return merged


def _cli() -> int:
    p = argparse.ArgumentParser(description="SciPilot-cite paper searcher")
    p.add_argument("query")
    p.add_argument("--from-year", type=int, default=2021)
    p.add_argument("--to-year", type=int, default=2026)
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--include-preprint", action="store_true")
    p.add_argument("--json", action="store_true", help="output JSON")
    p.add_argument("--log", default="evidence_log.jsonl", help="evidence log path; '' disables")
    args = p.parse_args()
    papers = search_papers(
        args.query,
        (args.from_year, args.to_year),
        args.limit,
        include_preprint=args.include_preprint,
        log_path=args.log or None,
    )
    if args.json:
        json.dump(papers[: args.limit], sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        for i, p in enumerate(papers[: args.limit], 1):
            print(
                f"[{i}] ({p.get('citation_count', 0)} cites) {p.get('year')} — "
                f"{p.get('title', '')[:90]}"
            )
            print(f"     by {', '.join((p.get('authors') or [])[:3])}  | venue: {p.get('venue')}")
            print(f"     doi={p.get('doi')}  sources={p.get('source_apis')}")
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
