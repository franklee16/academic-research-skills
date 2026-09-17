"""
SciPilot-cite :: verify_paper.py
学术文献真实性验证引擎
DOI 解析验证 + 多源交叉确认，三级验证分级（VERIFIED / LIKELY_REAL / UNVERIFIED）
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from utils import (
    append_jsonl,
    first_author_last_name,
    logger,
    normalize_author,
    paper_id_hash,
    rate_limited_request,
    title_similarity,
    utc_now_iso,
)

CROSSREF_WORK_URL = "https://api.crossref.org/works/{doi}"
SEMANTIC_SCHOLAR_DOI_URL = "https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
SEMANTIC_SCHOLAR_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"
OPENALEX_DOI_URL = "https://api.openalex.org/works/https://doi.org/{doi}"
OPENALEX_SEARCH_URL = "https://api.openalex.org/works"

USER_AGENT = "SciPilot-cite/1.0 (mailto:scipilot@example.org)"

TITLE_THRESHOLD = 0.85
TITLE_THRESHOLD_STRICT = 0.90


def verify_by_doi(
    doi: str, expected_title: str, expected_year: int | None, expected_authors: list
) -> dict:
    """
    通过 DOI 在 Crossref 验证论文真实性。
    返回 {status: VERIFIED|MISMATCH|NOT_FOUND, details: {...}}。
    """
    url = CROSSREF_WORK_URL.format(doi=doi)
    data = rate_limited_request(url, headers={"User-Agent": USER_AGENT}, min_interval=0.6)
    if not data or "message" not in data:
        return {"status": "NOT_FOUND", "details": {"reason": "Crossref returned no record"}}

    msg = data["message"]
    title_list = msg.get("title") or []
    real_title = title_list[0] if title_list else ""
    title_score = title_similarity(real_title, expected_title)

    real_year = None
    for key in ("issued", "published-print", "published-online"):
        dp = (msg.get(key) or {}).get("date-parts")
        if dp and dp[0]:
            real_year = dp[0][0]
            break

    real_authors = [normalize_author(a) for a in (msg.get("author") or [])]

    title_ok = title_score >= TITLE_THRESHOLD
    year_ok = (expected_year is None) or (real_year == expected_year)
    expected_last = first_author_last_name(expected_authors).lower()
    real_last = first_author_last_name(real_authors).lower()
    author_ok = (not expected_last) or (not real_last) or (expected_last == real_last)

    details = {
        "real_title": real_title,
        "real_year": real_year,
        "real_first_author": real_authors[0] if real_authors else "",
        "title_similarity": round(title_score, 4),
        "year_match": year_ok,
        "first_author_match": author_ok,
    }
    if title_ok and year_ok and author_ok:
        return {"status": "VERIFIED", "details": details}
    return {"status": "MISMATCH", "details": details}


def _search_s2_title(title: str, limit: int = 3) -> list[dict]:
    params = {"query": title, "limit": limit, "fields": "title,year,authors,externalIds"}
    data = rate_limited_request(
        SEMANTIC_SCHOLAR_SEARCH, params=params, headers={"User-Agent": USER_AGENT}, min_interval=1.0
    )
    return (data or {}).get("data") or []


def _search_openalex_title(title: str, limit: int = 3) -> list[dict]:
    params = {"search": title, "per_page": limit, "mailto": "scipilot@example.org"}
    data = rate_limited_request(
        OPENALEX_SEARCH_URL, params=params, headers={"User-Agent": USER_AGENT}, min_interval=0.5
    )
    return (data or {}).get("results") or []


def verify_by_cross_check(title: str, year: int | None, authors: list) -> dict:
    """
    无 DOI 时，在 S2 和 OpenAlex 中各搜索，确认至少 2 源高度匹配。
    """
    expected_last = first_author_last_name(authors).lower()
    hits: list[str] = []

    for s in _search_s2_title(title):
        s_title = s.get("title") or ""
        s_year = s.get("year")
        s_authors = [(a or {}).get("name", "") for a in (s.get("authors") or [])]
        s_last = first_author_last_name(s_authors).lower()
        if (
            title_similarity(s_title, title) >= TITLE_THRESHOLD
            and (year is None or s_year == year)
            and (not expected_last or not s_last or expected_last == s_last)
        ):
            hits.append("semantic_scholar")
            break

    for o in _search_openalex_title(title):
        o_title = o.get("title") or o.get("display_name") or ""
        o_year = o.get("publication_year")
        o_authors = []
        for au in o.get("authorships", []) or []:
            disp = (au.get("author") or {}).get("display_name")
            if disp:
                o_authors.append(disp)
        o_last = first_author_last_name(o_authors).lower()
        if (
            title_similarity(o_title, title) >= TITLE_THRESHOLD
            and (year is None or o_year == year)
            and (not expected_last or not o_last or expected_last == o_last)
        ):
            hits.append("openalex")
            break

    if len(hits) >= 2:
        return {"status": "LIKELY_REAL", "details": {"matched_sources": hits}}
    return {"status": "UNVERIFIED", "details": {"matched_sources": hits}}


def verify_paper(paper: dict) -> dict:
    """主入口：DOI 优先；无 DOI 或 DOI 验证失败则尝试交叉验证。"""
    doi = paper.get("doi")
    title = paper.get("title", "")
    year = paper.get("year")
    authors = paper.get("authors") or []

    out = dict(paper)
    if doi:
        result = verify_by_doi(doi, title, year, authors)
        if result["status"] == "VERIFIED":
            out["verification_status"] = "VERIFIED"
            out["verification_details"] = result["details"]
            return out
        if result["status"] in {"MISMATCH", "NOT_FOUND"}:
            cross = verify_by_cross_check(title, year, authors)
            out["verification_status"] = cross["status"]
            out["verification_details"] = {
                "doi_check": result["details"],
                "cross_check": cross["details"],
                "doi_status": result["status"],
            }
            return out

    cross = verify_by_cross_check(title, year, authors)
    out["verification_status"] = cross["status"]
    out["verification_details"] = cross["details"]
    return out


def batch_verify(
    papers: list[dict],
    max_workers: int = 4,
    log_path: str | None = "verification_log.jsonl",
) -> list[dict]:
    """
    并行批量验证。
    自动丢弃 UNVERIFIED 的文献，只返回 VERIFIED 和 LIKELY_REAL。

    Writes one JSONL record per verification attempt (including UNVERIFIED ones)
    to `log_path`. The audit script reads this log to detect fabricated entries
    in the final bibliography. Pass log_path=None or "" to disable.
    """
    logger.info(f"Verifying {len(papers)} candidate papers (max_workers={max_workers})")
    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(verify_paper, p): p for p in papers}
        for f in as_completed(futs):
            try:
                r = f.result()
                results.append(r)
            except Exception as e:
                logger.warning(f"verify failed for one paper: {e}")

    if log_path:
        ts = utc_now_iso()
        for r in results:
            append_jsonl(
                log_path,
                {
                    "timestamp": ts,
                    "event": "verification",
                    "paper_id": paper_id_hash(r),
                    "title_claimed": r.get("title"),
                    "doi_claimed": r.get("doi"),
                    "year_claimed": r.get("year"),
                    "first_author_claimed": (r.get("authors") or [""])[0],
                    "verdict": r.get("verification_status"),
                    "details": r.get("verification_details", {}),
                },
            )
        logger.info(f"Wrote {len(results)} verification records to {log_path}")

    kept = [p for p in results if p.get("verification_status") in {"VERIFIED", "LIKELY_REAL"}]
    dropped = len(results) - len(kept)
    logger.info(
        f"Verification done: VERIFIED={sum(1 for p in kept if p['verification_status']=='VERIFIED')}, "
        f"LIKELY_REAL={sum(1 for p in kept if p['verification_status']=='LIKELY_REAL')}, "
        f"DROPPED={dropped}"
    )
    return kept


def _cli() -> int:
    p = argparse.ArgumentParser(description="SciPilot-cite paper verifier")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_doi = sub.add_parser("doi", help="verify by DOI")
    p_doi.add_argument("doi")
    p_doi.add_argument("--title", required=True)
    p_doi.add_argument("--year", type=int)
    p_doi.add_argument("--author", action="append", default=[])

    p_title = sub.add_parser("title", help="cross-check by title")
    p_title.add_argument("title")
    p_title.add_argument("--year", type=int)
    p_title.add_argument("--author", action="append", default=[])

    p_json = sub.add_parser("paper", help="verify a paper JSON from stdin")

    p_batch = sub.add_parser("batch", help="verify a JSON array of papers from a file")
    p_batch.add_argument("papers_json")
    p_batch.add_argument("--log", default="verification_log.jsonl")
    p_batch.add_argument("--no-log", action="store_true")
    p_batch.add_argument("--max-workers", type=int, default=4)

    args = p.parse_args()

    if args.cmd == "doi":
        r = verify_by_doi(args.doi, args.title, args.year, args.author)
    elif args.cmd == "title":
        r = verify_by_cross_check(args.title, args.year, args.author)
    elif args.cmd == "batch":
        with open(args.papers_json, encoding="utf-8") as f:
            papers = json.load(f)
        log = None if args.no_log else args.log
        kept = batch_verify(papers, max_workers=args.max_workers, log_path=log)
        json.dump(kept, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    else:
        paper = json.load(sys.stdin)
        r = verify_paper(paper)

    json.dump(r, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
