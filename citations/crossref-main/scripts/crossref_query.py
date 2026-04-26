#!/usr/bin/env python3
"""Thin Crossref REST API wrapper. Returns raw JSON; does no parsing."""
import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.crossref.org"
USER_AGENT = "crossref-skill/0.1 (mailto:your@email.com)"
TIMEOUT = 20
RETRY_CAP = 10


def fetch(url: str, attempt: int = 1) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code in (429, 503) and attempt == 1:
            wait = e.headers.get("Retry-After", "1")
            try:
                wait_s = min(int(wait), RETRY_CAP)
            except ValueError:
                wait_s = 1
            time.sleep(wait_s)
            return fetch(url, attempt=2)
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")[:500]
        except Exception:
            pass
        raise SystemExit(f"HTTP {e.code} for {url}\n{body}")
    except urllib.error.URLError as e:
        raise SystemExit(f"Network error for {url}: {e.reason}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"Invalid JSON from {url}: {e}")
    except TimeoutError:
        raise SystemExit(f"Timeout after {TIMEOUT}s for {url}")


def build_url(args: argparse.Namespace) -> str:
    if args.doi:
        doi = urllib.parse.quote(args.doi.strip(), safe="/")
        url = f"{BASE}/works/{doi}"
        if args.select:
            url += "?" + urllib.parse.urlencode({"select": args.select})
        return url
    params = {"query": args.query, "rows": str(args.rows)}
    if args.select:
        params["select"] = args.select
    return f"{BASE}/works?{urllib.parse.urlencode(params)}"


def _year(it: dict):
    for k in ("issued", "published-print", "published-online", "published"):
        parts = (it.get(k) or {}).get("date-parts") or [[None]]
        if parts and parts[0] and parts[0][0]:
            return parts[0][0]
    return None


def extract_candidate(it: dict) -> dict:
    """Normalize a Crossref work object into the compact fields Claude needs for matching."""
    authors = [[a.get("family"), a.get("given")] for a in (it.get("author") or [])]
    title = (it.get("title") or [None])[0]
    subtitle = (it.get("subtitle") or [None])[0]
    return {
        "score": it.get("score"),
        "type": it.get("type"),
        "year": _year(it),
        "authors": authors,
        "title": title,
        "subtitle": subtitle,
        "container": (it.get("container-title") or [None])[0],
        "volume": it.get("volume"),
        "issue": it.get("issue"),
        "page": it.get("page"),
        "doi": it.get("DOI"),
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Query Crossref REST API. Returns raw JSON, or compact candidate array with --extract.")
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--doi", help="Exact DOI lookup via /works/{doi}")
    mode.add_argument("--query", help="Free-text metadata query via /works?query=")
    p.add_argument("--rows", type=int, default=3, help="Rows to return in query mode (default 3)")
    p.add_argument("--select", help="Comma-separated fields to include")
    p.add_argument("--extract", action="store_true",
                   help="Emit a compact JSON array of normalized candidate records instead of the raw response. "
                        "DOI mode yields one element; query mode yields up to --rows elements.")
    args = p.parse_args()
    data = fetch(build_url(args))
    if args.extract:
        msg = data.get("message") or {}
        items = msg.get("items") if isinstance(msg.get("items"), list) else [msg]
        out = [extract_candidate(it) for it in items]
        # ASCII-safe output avoids Windows cp1252 UnicodeEncodeError on stdout.
        json.dump(out, sys.stdout, ensure_ascii=True)
    else:
        json.dump(data, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
