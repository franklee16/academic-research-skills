"""
SciPilot-cite :: audit_no_hallucination.py
末端真实性审计 — Gate 8（物理幻觉门控）

Re-verifies 100% of the final bibliography against live academic APIs and
cross-checks every entry against the verification_log.jsonl written during
Stages 2-3. Designed to catch papers that an LLM may have fabricated or
silently slipped past the prompt-level IRON RULES.

Exit codes:
  0  All papers PASS — bibliography may be delivered.
  2  At least one paper FAIL — bibliography MUST NOT be delivered until fixed.
  3  Operational error (missing files, malformed input).

Usage:
  python audit_no_hallucination.py final_papers.json \
         --log verification_log.jsonl \
         --report audit_report.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

from utils import logger, paper_id_hash, utc_now_iso
from verify_paper import verify_paper


def load_papers(path: str) -> list[dict]:
    """Accept either a bare list or a {'papers': [...]} envelope."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("papers"), list):
        return data["papers"]
    raise ValueError(f"Cannot extract a paper list from {path}")


def load_verification_log(path: str) -> dict[str, dict]:
    """paper_id -> most-recent verification record (last-write wins)."""
    out: dict[str, dict] = {}
    if not os.path.exists(path):
        logger.warning(f"verification log not found: {path}")
        return out
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("event") != "verification":
                continue
            pid = rec.get("paper_id")
            if pid:
                out[pid] = rec
    return out


def _fail_reasons(has_log: bool, verdict_ok: bool, live_ok: bool, drift: bool) -> list[str]:
    reasons: list[str] = []
    if not has_log:
        reasons.append("no verification_log entry — paper may be fabricated or never went through Stage 3")
    if has_log and not verdict_ok:
        reasons.append("log verdict not in {VERIFIED, LIKELY_REAL}")
    if not live_ok:
        reasons.append("live re-verification against Crossref/S2/OpenAlex returned UNVERIFIED")
    if drift:
        reasons.append("verdict drift between Stage 3 log and live re-check")
    return reasons


def audit(
    papers: list[dict],
    verification_log: dict[str, dict],
    allow_likely_real: bool = True,
) -> dict:
    """
    Independently re-verify every paper against live APIs.
    Cross-check the per-paper verdict against the verification_log.

    Returns a structured report dict with overall verdict ("PASS" | "FAIL").
    """
    acceptable = {"VERIFIED", "LIKELY_REAL"} if allow_likely_real else {"VERIFIED"}

    per_paper: list[dict] = []
    fail_count = no_log_count = drift_count = 0

    for i, paper in enumerate(papers):
        pid = paper_id_hash(paper)
        log_entry = verification_log.get(pid)
        has_log = log_entry is not None
        log_verdict = log_entry.get("verdict") if log_entry else None

        if not has_log:
            no_log_count += 1

        verdict_ok = log_verdict in acceptable

        # Live re-verification (100% — not the 20% sample).
        live = verify_paper(paper)
        live_verdict = live.get("verification_status")
        live_ok = live_verdict in acceptable

        drift = bool(log_verdict) and (log_verdict != live_verdict)
        if drift:
            drift_count += 1

        paper_pass = has_log and verdict_ok and live_ok
        if not paper_pass:
            fail_count += 1

        per_paper.append(
            {
                "index": i,
                "paper_id": pid,
                "title": paper.get("title"),
                "doi": paper.get("doi"),
                "year": paper.get("year"),
                "first_author": (paper.get("authors") or [""])[0],
                "log_verdict": log_verdict,
                "live_verdict": live_verdict,
                "has_log_entry": has_log,
                "drift": drift,
                "pass": paper_pass,
                "reasons": _fail_reasons(has_log, verdict_ok, live_ok, drift) if not paper_pass else [],
            }
        )

    return {
        "schema": "scipilot-cite/audit/1.0",
        "timestamp": utc_now_iso(),
        "policy": {"allow_likely_real": allow_likely_real},
        "summary": {
            "total_papers": len(papers),
            "passed": len(papers) - fail_count,
            "failed": fail_count,
            "missing_log_entries": no_log_count,
            "drift_detected": drift_count,
        },
        "overall": "PASS" if fail_count == 0 else "FAIL",
        "per_paper": per_paper,
    }


def _print_human_summary(report: dict) -> None:
    s = report["summary"]
    print(f"\n=== SciPilot-cite hallucination gate: {report['overall']} ===")
    print(
        f"  total={s['total_papers']}  pass={s['passed']}  fail={s['failed']}  "
        f"missing_log={s['missing_log_entries']}  drift={s['drift_detected']}"
    )
    if report["overall"] != "PASS":
        print("\nSuspect papers — DO NOT include in final bibliography:")
        for r in report["per_paper"]:
            if r["pass"]:
                continue
            title = (r.get("title") or "")[:72]
            print(f"  [{r['index']}] {title}")
            print(f"       doi: {r.get('doi')}")
            print(f"       log_verdict: {r['log_verdict']}  live_verdict: {r['live_verdict']}")
            for reason in r["reasons"]:
                print(f"       reason: {reason}")


def _cli() -> int:
    parser = argparse.ArgumentParser(description="SciPilot-cite hallucination audit (Gate 8)")
    parser.add_argument("papers_json", help="final bibliography JSON (list or {'papers': [...]})")
    parser.add_argument("--log", default="verification_log.jsonl", help="path to verification log")
    parser.add_argument("--report", default="audit_report.json", help="path to write audit report")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat LIKELY_REAL as FAIL (default: accept VERIFIED + LIKELY_REAL)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.papers_json):
        logger.error(f"Bibliography file not found: {args.papers_json}")
        return 3

    try:
        papers = load_papers(args.papers_json)
    except Exception as e:
        logger.error(f"Failed to parse {args.papers_json}: {e}")
        return 3

    if not papers:
        logger.error("Bibliography is empty; nothing to audit")
        return 3

    vlog = load_verification_log(args.log)
    logger.info(
        f"Auditing {len(papers)} papers against {len(vlog)} verification log entries from {args.log}"
    )

    report = audit(papers, vlog, allow_likely_real=not args.strict)
    with open(args.report, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    logger.info(f"Wrote audit report to {args.report}")

    _print_human_summary(report)
    return 0 if report["overall"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(_cli())
