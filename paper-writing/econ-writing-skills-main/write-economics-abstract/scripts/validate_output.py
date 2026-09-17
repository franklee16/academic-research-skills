#!/usr/bin/env python3
"""Emit mechanical warnings for a draft economics abstract.

Usage: python validate_output.py abstract.txt
This script cannot establish factual correctness; use the evidence ledger for that.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def words(text: str) -> list[str]:
    return re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE)


def validate(text: str) -> dict:
    count = len(words(text))
    warnings: list[str] = []
    hard_failures: list[str] = []
    if count < 80:
        warnings.append("Very short: verify that task, answer method, main finding, and closure are all recoverable.")
    if count > 200:
        hard_failures.append("Abstract exceeds 200 words without an explicit external override.")
    patterns = {
        "internal reference": r"\b(section|table|figure|appendix|equation)\s+[A-Z]?\d+",
        "citation-like parenthesis": r"\([A-Z][A-Za-z-]+(?:\s+(?:and|&|et al\.?)\s+[A-Z][A-Za-z-]+)?,?\s+(?:19|20)\d{2}\)",
        "placeholder": r"\b(TODO|TBD|XXX)\b|\[[^\]]*(?:insert|author input|placeholder)[^\]]*\]",
        "generic opening": r"^\s*(?:Recently|In recent years|It is well known that|This paper studies an important)",
        "empty process phrase": r"\b(?:data (?:are|were) analyzed|theorems? (?:are|were) proved|policy implications? (?:are|were) discussed)\b",
        "novelty claim": r"\b(first|novel|groundbreaking|unprecedented|fills? (?:an? )?gap)\b",
        "strong causal wording": r"\b(causes?|proves?|establishes? that|leads? to|impact of|effect of)\b",
    }
    for label, pattern in patterns.items():
        if re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
            warnings.append(f"Check {label} against the manuscript and Skill rules.")
    paragraph_count = len([p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()])
    if paragraph_count != 1:
        hard_failures.append("Abstract is not exactly one paragraph.")
    stripped = text.strip()
    quote_pairs = [('"', '"'), ('“', '”'), ("'", "'")]
    if any(stripped.startswith(a) and stripped.endswith(b) and len(stripped) > 1 for a, b in quote_pairs):
        hard_failures.append("Abstract is wrapped in external quotation marks.")
    if re.search(r"^\s*```|```\s*$|^\s*>|^\s*#{1,6}\s|^\s*Abstract\s*:", stripped, re.IGNORECASE | re.MULTILINE):
        hard_failures.append("Abstract contains a heading, block quote, code fence, or label wrapper.")
    return {"passed": not hard_failures, "word_count": count, "paragraph_count": paragraph_count, "hard_failures": hard_failures, "warnings": warnings, "semantic_validation": False}


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python validate_output.py ABSTRACT_FILE", file=sys.stderr)
        return 2
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    print(json.dumps(validate(text), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
