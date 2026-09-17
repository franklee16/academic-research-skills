#!/usr/bin/env python3
"""Emit mechanical warnings for an economics-paper introduction.

Usage:
    python validate_output.py INTRODUCTION_FILE [--bib REFERENCES_BIB]

This validator cannot verify factual truth, citation meaning, contribution claims,
or whether the argument is well organized. Those require the ledgers and audits in
the Skill.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


WORD_RE = re.compile(r"\b[\w'-]+\b", flags=re.UNICODE)
CITE_KEY_RE = re.compile(r"\\cite[a-zA-Z*]*\{([^}]+)\}")
BIB_KEY_RE = re.compile(r"^\s*@\w+\s*\{\s*([^,\s]+)", flags=re.MULTILINE)


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def paragraph_count(text: str) -> int:
    return len([p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()])


def extract_cite_keys(text: str) -> set[str]:
    keys: set[str] = set()
    for group in CITE_KEY_RE.findall(text):
        keys.update(k.strip() for k in group.split(",") if k.strip())
    return keys


def validate(text: str, bib_text: str | None = None) -> dict:
    count = word_count(text)
    paragraphs = paragraph_count(text)
    warnings: list[str] = []
    hard_failures: list[str] = []

    if count < 900:
        warnings.append(
            "Short introduction: verify that the question, answer, credibility, results, and positioning are genuinely complete."
        )
    if count > 3200:
        warnings.append(
            "Long introduction: run the deletion test; sample ranges are calibration, not permission to retain redundant material."
        )
    if paragraphs < 5:
        warnings.append(
            "Few paragraphs: inspect whether distinct reader questions have been compressed into overloaded paragraphs."
        )
    if paragraphs > 35:
        warnings.append(
            "Many paragraphs: inspect for choppy exposition, result inventory, or fragmented literature discussion."
        )

    warning_patterns = {
        "generic importance opening": r"^\s*(?:In recent years|Recently|It is well known that|[A-Z][^.]{0,80} is (?:very |extremely )?important)",
        "strong novelty or gap claim": r"\b(?:first|only study|novel|unprecedented|little is known|nothing is known|fills? (?:an? |the )?gap|has not been studied)\b",
        "promotional language": r"\b(?:groundbreaking|revolutionary|game-changing|transformative contribution)\b",
        "possible causal language": r"\b(?:causes?|causal impact|leads? to|drives?|explains?|accounts for|operates through|effect of|impact of)\b",
        "placeholder": r"\b(?:TODO|TBD|XXX)\b|\[[^\]]*(?:insert|placeholder|author input|citation needed)[^\]]*\]",
        "mechanical literature listing": r"(?:[A-Z][A-Za-z-]+(?: et al\.)? \((?:19|20)\d{2}\)[,;]\s*){3,}",
        "formulaic roadmap": r"\bThe rest of (?:the|this) paper (?:is organized|proceeds) as follows\b",
    }
    for label, pattern in warning_patterns.items():
        if re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
            warnings.append(f"Check {label} against the manuscript, literature evidence, and Skill rules.")

    if re.search(r"^\s*```|```\s*$|^\s*>|^\s*#{1,6}\s", text.strip(), re.MULTILINE):
        hard_failures.append("Draft contains a code fence, block quote, or Markdown heading wrapper.")
    if re.search(r"\b(?:TODO|TBD|XXX)\b|\[[^\]]*(?:insert|placeholder|author input)[^\]]*\]", text, re.IGNORECASE):
        hard_failures.append("Draft contains an unresolved placeholder.")

    citation_keys = sorted(extract_cite_keys(text))
    missing_keys: list[str] = []
    if bib_text is not None:
        bib_keys = set(BIB_KEY_RE.findall(bib_text))
        missing_keys = sorted(set(citation_keys) - bib_keys)
        if missing_keys:
            hard_failures.append("LaTeX citation keys are absent from the supplied bibliography.")
    elif citation_keys:
        warnings.append("LaTeX citation keys found, but no bibliography was supplied for a mechanical key check.")

    return {
        "passed_mechanical_checks": not hard_failures,
        "word_count": count,
        "paragraph_count": paragraphs,
        "citation_keys": citation_keys,
        "missing_bibliography_keys": missing_keys,
        "hard_failures": hard_failures,
        "warnings": warnings,
        "semantic_validation": False,
        "note": "A pass does not establish factual, citation-semantic, positioning, or prose quality.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("introduction", type=Path)
    parser.add_argument("--bib", type=Path)
    args = parser.parse_args()

    text = args.introduction.read_text(encoding="utf-8")
    bib_text = args.bib.read_text(encoding="utf-8") if args.bib else None
    print(json.dumps(validate(text, bib_text), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
