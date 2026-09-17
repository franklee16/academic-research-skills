#!/usr/bin/env python3
"""Emit mechanical warnings for a draft economics conclusion.

Usage: python validate_output.py conclusion.txt
This script cannot verify manuscript support, mechanisms, limits, citations, or policy logic.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def validate(text: str) -> dict:
    tokens = re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE)
    count = len(tokens)
    warnings: list[str] = []
    if count < 100:
        warnings.append("Very short: verify that the central takeaway and essential boundary remain clear.")
    if count > 600:
        warnings.append("Long conclusion: confirm that added words perform interpretation rather than recap.")
    patterns = {
        "placeholder": r"\b(TODO|TBD|XXX)\b|\[[^\]]*(?:insert|author input|placeholder)[^\]]*\]",
        "generic limitation": r"\b(?:this study|the paper) has (?:some|several) limitations\b|\bdata limitations\b",
        "generic future research": r"\b(?:more|further) research is (?:needed|required|warranted)\b",
        "strong policy command": r"\b(?:policymakers|governments?) (?:must|should|need to|required to)\b",
        "novelty claim": r"\b(first|novel|groundbreaking|unprecedented|fills? (?:an? )?gap)\b",
        "strong causal or proof wording": r"\b(causes?|proves?|establishes? once and for all|definitively demonstrates?)\b",
        "mechanism ranking or upgrade": r"\b(?:principal|main|primary) (?:channel|mechanism)\b|\b(?:drives?|explains?|accounts? for|operates? through)\b",
        "unbenchmarked evaluation": r"\b(?:low-cost|inexpensive|cost-effective|substantial|large|meaningful)\b",
        "possibly inferred denominator": r"\b(?:of|relative to) baseline\b",
    }
    for label, pattern in patterns.items():
        if re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
            warnings.append(f"Check {label} against the evidence ledger and calibrated-language rules.")
    paragraphs = [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    return {"word_count": count, "paragraph_count": len(paragraphs), "warnings": warnings, "semantic_validation": False}


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python validate_output.py CONCLUSION_FILE", file=sys.stderr)
        return 2
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    print(json.dumps(validate(text), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
