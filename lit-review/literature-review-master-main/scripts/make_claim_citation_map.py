#!/usr/bin/env python3
"""Create a lightweight claim-citation map scaffold from a Markdown manuscript.

This script does not verify claims. It only extracts candidate citation-bearing
sentences and high-risk wording for manual or agentic Mode E review.
"""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

CITATION_PATTERNS = [
    re.compile(r"\([A-Z][A-Za-z'\-]+(?:\s+and\s+[A-Z][A-Za-z'\-]+)?[, ]+\d{4}[a-z]?\)"),
    re.compile(r"[A-Z][A-Za-z'\-]+\s+et\s+al\.\s*\(\d{4}[a-z]?\)"),
    re.compile(r"[A-Z][A-Za-z'\-]+\s+and\s+[A-Z][A-Za-z'\-]+\s*\(\d{4}[a-z]?\)"),
]
HIGH_RISK_TERMS = [
    "first", "novel", "few studies", "no prior work", "always", "robust",
    "validate", "empirical", "proves", "demonstrates", "primarily focused",
    "has not examined", "underexplored", "seminal", "canonical",
]

def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", text) if s.strip()]

def has_citation(sentence: str) -> bool:
    return any(p.search(sentence) for p in CITATION_PATTERNS)

def risk_terms(sentence: str) -> list[str]:
    lower = sentence.lower()
    return [term for term in HIGH_RISK_TERMS if term in lower]

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Markdown or text manuscript file")
    parser.add_argument("output", help="CSV output path")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    rows = []
    claim_id = 1
    for sent in split_sentences(text):
        terms = risk_terms(sent)
        cited = has_citation(sent)
        if cited or terms:
            rows.append({
                "claim_id": f"C{claim_id:03d}",
                "claim_text": sent,
                "claim_type_guess": "citation-bearing" if cited else "high-risk uncited",
                "attached_citation_or_evidence": "present" if cited else "missing",
                "risk_terms": "; ".join(terms),
                "verification_target": "external_source",
                "status": "unverified",
            })
            claim_id += 1

    with Path(args.output).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "claim_id", "claim_text", "claim_type_guess", "attached_citation_or_evidence",
            "risk_terms", "verification_target", "status"
        ])
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    main()
