import argparse
import difflib
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path


CROSSREF_WORKS = "https://api.crossref.org/works"


def normalize_title(value):
    value = (value or "").lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def title_similarity(a, b):
    a_norm = normalize_title(a)
    b_norm = normalize_title(b)
    if not a_norm or not b_norm:
        return 0.0
    return difflib.SequenceMatcher(None, a_norm, b_norm).ratio()


def request_json(url, timeout=20, mailto="unknown@example.com"):
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": f"econometric-research-writing-skill/1.0 (mailto:{mailto})",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def crossref_by_doi(doi, mailto="unknown@example.com"):
    url = f"{CROSSREF_WORKS}/{urllib.parse.quote(doi.strip())}"
    return request_json(url, mailto=mailto).get("message", {})


def crossref_by_title(title, rows=3, mailto="unknown@example.com"):
    params = urllib.parse.urlencode({"query.title": title, "rows": rows})
    url = f"{CROSSREF_WORKS}?{params}"
    return request_json(url, mailto=mailto).get("message", {}).get("items", [])


def authors_from_crossref(item):
    authors = []
    for author in item.get("author", []):
        family = author.get("family")
        given = author.get("given")
        if family and given:
            authors.append(f"{given} {family}")
        elif family:
            authors.append(family)
    return authors


def year_from_crossref(item):
    for key in ["published-print", "published-online", "published", "issued"]:
        parts = item.get(key, {}).get("date-parts", [])
        if parts and parts[0]:
            return parts[0][0]
    return None


def summarize_crossref_item(item):
    titles = item.get("title") or []
    return {
        "title": titles[0] if titles else "",
        "authors": authors_from_crossref(item),
        "year": year_from_crossref(item),
        "container_title": (item.get("container-title") or [""])[0],
        "doi": item.get("DOI", ""),
        "url": item.get("URL", ""),
        "type": item.get("type", ""),
    }


def verify_reference(ref, sleep_seconds=0.25, mailto="unknown@example.com"):
    title = ref.get("title", "")
    doi = ref.get("doi") or ref.get("DOI")
    result = {
        "input": ref,
        "status": "not_checked",
        "match_score": None,
        "matched": None,
        "warning": None,
    }

    try:
        if doi:
            item = crossref_by_doi(doi, mailto=mailto)
            matched = summarize_crossref_item(item)
            score = title_similarity(title, matched["title"]) if title else None
            result.update({"status": "verified_by_doi", "match_score": score, "matched": matched})
            if title and score is not None and score < 0.80:
                result["status"] = "metadata_mismatch"
                result["warning"] = "DOI resolved, but title similarity is below 0.80."
            time.sleep(sleep_seconds)
            return result

        if title:
            items = crossref_by_title(title, rows=3, mailto=mailto)
            candidates = [summarize_crossref_item(item) for item in items]
            scored = [(title_similarity(title, item["title"]), item) for item in candidates]
            scored.sort(key=lambda pair: pair[0], reverse=True)
            if scored and scored[0][0] >= 0.85:
                result.update({"status": "verified_by_title", "match_score": scored[0][0], "matched": scored[0][1]})
            else:
                result.update({"status": "needs_manual_review", "match_score": scored[0][0] if scored else 0.0})
                result["warning"] = "No high-confidence Crossref title match found."
            time.sleep(sleep_seconds)
            return result

        result["status"] = "insufficient_metadata"
        result["warning"] = "Reference has neither DOI nor title."
        return result
    except Exception as exc:
        result["status"] = "verification_error"
        result["warning"] = str(exc)
        return result


def load_references(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("references", [])
    if not isinstance(data, list):
        raise ValueError("Input JSON must be a list or an object with a 'references' list.")
    return data


def write_markdown(results, out_path):
    lines = [
        "# Reference Verification Report",
        "",
        "| # | Status | Input title | Matched title | DOI | Warning |",
        "|---:|---|---|---|---|---|",
    ]
    for index, item in enumerate(results, start=1):
        ref = item.get("input", {})
        matched = item.get("matched") or {}
        lines.append(
            "| {idx} | {status} | {input_title} | {matched_title} | {doi} | {warning} |".format(
                idx=index,
                status=item.get("status", ""),
                input_title=(ref.get("title") or "").replace("|", "\\|"),
                matched_title=(matched.get("title") or "").replace("|", "\\|"),
                doi=(matched.get("doi") or ref.get("doi") or ref.get("DOI") or "").replace("|", "\\|"),
                warning=(item.get("warning") or "").replace("|", "\\|"),
            )
        )
    Path(out_path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def enriched_reference(result):
    ref = dict(result.get("input", {}))
    matched = result.get("matched") or {}
    status = result.get("status")
    if matched and status in {"verified_by_doi", "verified_by_title"}:
        return {
            "title": matched.get("title") or ref.get("title"),
            "authors": matched.get("authors") or ref.get("authors", []),
            "year": matched.get("year") or ref.get("year"),
            "container_title": matched.get("container_title") or ref.get("container_title") or ref.get("journal"),
            "doi": matched.get("doi") or ref.get("doi") or ref.get("DOI"),
            "url": matched.get("url") or ref.get("url"),
            "type": matched.get("type") or ref.get("type"),
            "verification_status": status,
            "match_score": result.get("match_score"),
        }

    ref["verification_status"] = status
    ref["match_score"] = result.get("match_score")
    if result.get("warning"):
        ref["warning"] = result["warning"]
    return ref


def main():
    parser = argparse.ArgumentParser(description="Verify reference metadata against Crossref by DOI or title.")
    parser.add_argument("references_json", help="JSON list of references or {'references': [...]} object.")
    parser.add_argument("--out-md", help="Write a Markdown verification report.")
    parser.add_argument("--out-json", help="Write raw JSON verification results.")
    parser.add_argument("--out-enriched-json", help="Write normalized reference metadata for verified items.")
    parser.add_argument("--mailto", help="Contact email to include in the Crossref API User-Agent for polite pool access.")
    args = parser.parse_args()

    mailto = args.mailto or os.environ.get("CROSSREF_MAILTO") or "unknown@example.com"
    refs = load_references(args.references_json)
    results = [verify_reference(ref, mailto=mailto) for ref in refs]

    if args.out_json:
        Path(args.out_json).write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    if args.out_md:
        write_markdown(results, args.out_md)
    if args.out_enriched_json:
        enriched = [enriched_reference(item) for item in results]
        Path(args.out_enriched_json).write_text(json.dumps(enriched, indent=2, ensure_ascii=False), encoding="utf-8")
    if not args.out_json and not args.out_md and not args.out_enriched_json:
        print(json.dumps(results, indent=2, ensure_ascii=False))

    bad_statuses = {"metadata_mismatch", "needs_manual_review", "insufficient_metadata", "verification_error"}
    if any(item.get("status") in bad_statuses for item in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
