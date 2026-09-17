#!/usr/bin/env python3
"""Render a Nan-paper-polish JSON change ledger as a readable Markdown report."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Any


LABELS = {
    "zh": {
        "title": "论文修改说明",
        "diagnosis": "总体诊断",
        "changes": "逐条修改记录",
        "original": "原文",
        "revised": "修改后",
        "reason": "修改理由",
        "criteria": "诊断指标",
        "root_cause": "根本问题",
        "meaning": "含义影响",
        "confirmation": "作者确认",
        "yes": "需要",
        "no": "不需要",
        "questions": "待作者确认的问题",
        "none": "无",
    },
    "en": {
        "title": "Manuscript Revision Report",
        "diagnosis": "Overall diagnosis",
        "changes": "Change-by-change record",
        "original": "Original",
        "revised": "Revised",
        "reason": "Reason",
        "criteria": "Diagnostic criteria",
        "root_cause": "Root cause",
        "meaning": "Effect on meaning",
        "confirmation": "Author confirmation",
        "yes": "Required",
        "no": "Not required",
        "questions": "Questions for the author",
        "none": "None",
    },
}


def load_ledger(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {"changes": data}
    if not isinstance(data, dict):
        raise ValueError("The ledger must be a JSON object or a list of changes.")
    if not isinstance(data.get("changes", []), list):
        raise ValueError("The ledger's 'changes' field must be a list.")
    return data


def blockquote(value: Any) -> str:
    text = "" if value is None else str(value)
    lines = text.splitlines() or [""]
    return "\n".join(">" if line == "" else f"> {line}" for line in lines)


def location_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        preferred = ["section", "paragraph", "sentence", "page", "line"]
        parts = [f"{key}: {value[key]}" for key in preferred if key in value]
        parts.extend(f"{key}: {item}" for key, item in value.items() if key not in preferred)
        return "; ".join(parts)
    if isinstance(value, list):
        return "; ".join(map(str, value))
    return str(value or "unspecified")


def list_text(value: Any) -> str:
    if isinstance(value, list):
        return "; ".join(str(item) for item in value) or "—"
    return str(value or "—")


def diagnostic_text(value: Any) -> str:
    if isinstance(value, list):
        return "\n".join(f"- {item}" for item in value)
    if isinstance(value, dict):
        return "\n".join(f"- **{key}**：{item}" for key, item in value.items())
    return str(value)


def confirmation_needed(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, dict):
        return bool(value.get("required", False))
    return str(value).strip().lower() in {"yes", "true", "required", "需要", "是"}


def render(ledger: dict[str, Any], language: str = "zh") -> str:
    labels = LABELS[language]
    title = str(ledger.get("title") or labels["title"])
    lines = [f"# {title}"]

    metadata = ledger.get("metadata")
    if isinstance(metadata, dict) and metadata:
        lines.extend(["", "| 项目 | 内容 |" if language == "zh" else "| Item | Value |", "|---|---|"])
        for key, value in metadata.items():
            safe_value = str(value).replace("\n", " ").replace("|", "\\|")
            lines.append(f"| {key} | {safe_value} |")

    diagnosis = ledger.get("diagnosis")
    if diagnosis:
        lines.extend(["", f"## {labels['diagnosis']}", "", diagnostic_text(diagnosis)])

    lines.extend(["", f"## {labels['changes']}"])
    changes = ledger.get("changes", [])
    if not changes:
        lines.extend(["", labels["none"]])

    for index, change in enumerate(changes, start=1):
        if not isinstance(change, dict):
            continue
        change_id = change.get("change_id") or f"CH-{index:03d}"
        location = location_text(change.get("location"))
        change_type = str(change.get("change_type") or "unspecified")
        severity = change.get("severity")
        suffix = f"｜{change_type}" + (f"｜{severity}" if severity else "")
        lines.extend(
            [
                "",
                f"### {change_id}｜{location}{suffix}",
                "",
                f"**{labels['original']}**",
                "",
                blockquote(change.get("original")),
                "",
                f"**{labels['revised']}**",
                "",
                blockquote(change.get("revised")),
                "",
                f"**{labels['reason']}**：{change.get('reason') or '—'}",
                "",
                f"**{labels['criteria']}**：{list_text(change.get('criteria') or change.get('tags'))}",
                "",
                f"**{labels['root_cause']}**：{change.get('root_cause') or '—'}",
                "",
                f"**{labels['meaning']}**：{change.get('meaning_effect') or '—'}",
                "",
                f"**{labels['confirmation']}**：{labels['yes'] if confirmation_needed(change.get('author_confirmation')) else labels['no']}",
            ]
        )

    questions = ledger.get("author_questions", [])
    lines.extend(["", f"## {labels['questions']}", ""])
    if questions:
        for question in questions:
            if isinstance(question, dict):
                qid = question.get("question_id") or question.get("change_id") or "Q"
                text = question.get("question") or question.get("text") or str(question)
                lines.append(f"- **{qid}**：{text}")
            else:
                lines.append(f"- {question}")
    else:
        lines.append(labels["none"])

    return "\n".join(lines).rstrip() + "\n"


def self_test() -> None:
    sample = {
        "metadata": {"mode": "standard", "language": "English"},
        "diagnosis": [
            "The paragraph is accurate.",
            "Its topic chain is discontinuous.",
        ],
        "changes": [
            {
                "change_id": "CH-001",
                "location": {"section": "Introduction", "sentence": 2},
                "change_type": "replace",
                "original": "This result proves the mechanism.",
                "revised": "This result is consistent with the proposed mechanism.",
                "reason": "Calibrates the claim to correlational evidence.",
                "criteria": ["EVIDENCE-CLAIM", "CAUSALITY", "HEDGING"],
                "root_cause": "claim_exceeds_observational_evidence",
                "tags": ["HEDGE-EVIDENCE", "CLAIM-STRENGTH"],
                "meaning_effect": "Reduces certainty without changing the proposed explanation.",
                "author_confirmation": False,
            }
        ],
        "author_questions": [],
    }
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "report.md"
        output.write_text(render(sample, "zh"), encoding="utf-8")
        text = output.read_text(encoding="utf-8")
        required = [
            "# 论文修改说明",
            "- The paragraph is accurate.",
            "**原文**",
            "**修改后**",
            "**修改理由**",
            "**诊断指标**",
            "CH-001",
        ]
        missing = [item for item in required if item not in text]
        if missing:
            raise AssertionError(f"Renderer self-test failed; missing: {missing}")
    print("render_change_report.py self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, help="Path to the JSON change ledger")
    parser.add_argument("--output", type=Path, help="Path for the Markdown report")
    parser.add_argument("--language", choices=sorted(LABELS), default="zh")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return 0
    if not args.ledger or not args.output:
        parser.error("--ledger and --output are required unless --self-test is used")

    report = render(load_ledger(args.ledger), args.language)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
