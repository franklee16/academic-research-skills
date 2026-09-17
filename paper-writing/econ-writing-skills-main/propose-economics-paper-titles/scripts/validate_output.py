#!/usr/bin/env python3
"""Emit mechanical warnings for one-title-per-line economics title candidates.

Usage: python validate_output.py titles.txt
This script cannot validate whether the manuscript fulfills a title promise.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def clean(line: str) -> str:
    line = re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", line.strip())
    line = re.sub(r"^\*\*(?:Recommended title|Strong alternatives?)\*\*\s*[:—-]?\s*", "", line, flags=re.IGNORECASE)
    return line.strip().strip('"“”')


def validate(text: str) -> dict:
    titles = [clean(line) for line in text.splitlines() if clean(line) and not line.lstrip().startswith("#")]
    results = []
    for title in titles:
        count = len(re.findall(r"\b[\w'-]+\b", title, flags=re.UNICODE))
        warnings: list[str] = []
        if count > 14:
            warnings.append("Over the common compression range; verify that each extra word preserves truth or necessary scope.")
        if count < 4:
            warnings.append("Very short; check distinctiveness and research identity.")
        if re.search(r"\b(first|new|novel|important|groundbreaking|unprecedented)\b", title, re.IGNORECASE):
            warnings.append("Promotional or novelty word requires narrow factual support.")
        if re.search(r"\b(impact|effect|causes?|causal)\b", title, re.IGNORECASE):
            warnings.append("Causal wording requires a manuscript-level design check.")
        if re.search(r"\bEvidence from\b", title, re.IGNORECASE):
            warnings.append("Run the Evidence-from deletion test.")
        if title.count(":") > 1:
            warnings.append("Multiple colons usually signal over-structuring.")
        if title.endswith("?"):
            warnings.append("Question title: verify real two-sided tension and a clear answer.")
        results.append({"title": title, "word_count": count, "warnings": warnings})
    return {"candidate_count": len(titles), "titles": results, "semantic_validation": False}


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python validate_output.py TITLE_FILE", file=sys.stderr)
        return 2
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    print(json.dumps(validate(text), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
