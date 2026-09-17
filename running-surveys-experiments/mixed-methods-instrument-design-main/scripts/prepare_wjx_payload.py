#!/usr/bin/env python3
"""Convert validated questionnaire specs into Wenjuanxing JSONL draft payloads.

The script never calls Wenjuanxing and never publishes anything. It prepares one
JSONL file per questionnaire form plus a manifest that records optional titles,
blocking fidelity issues, and the exact draft-creation command shape.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


MISSING_LABELS = {
    "dont_know": "不知道",
    "not_applicable": "不适用",
    "refused": "不愿回答",
}

CHOICE_TYPES = {"single-choice", "multiple-choice", "ordinal-rating"}
ROW_OPTION_TYPES = {"ranking", "constant-sum"}
SUPPORTED_TYPES = CHOICE_TYPES | ROW_OPTION_TYPES | {"numeric", "date-or-time", "open-text"}
PLACEHOLDER = re.compile(r"\[[^\]]+\]")


def text(value: Any, fallback: str = "") -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return fallback


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z._-]+", "-", value.strip()).strip("-.")
    return cleaned or "questionnaire"


def visible_missing_labels(item: dict[str, Any]) -> list[str]:
    display = item.get("missing_display")
    if not isinstance(display, list):
        return []
    return [MISSING_LABELS[key] for key in display if key in MISSING_LABELS]


def item_title(item: dict[str, Any]) -> str:
    item_id = text(item.get("id"))
    question = text(item.get("question_text"), "[题面待填写]")
    return f"{item_id}. {question}" if item_id else question


def is_placeholder(value: Any) -> bool:
    return bool(PLACEHOLDER.search(text(value)))


def map_item(item: dict[str, Any], blockers: list[str], warnings: list[str]) -> dict[str, Any] | None:
    item_id = text(item.get("id"), "[未知题号]")
    response_type = text(item.get("response_type"))
    if not text(item.get("question_text")) or is_placeholder(item.get("question_text")):
        blockers.append(f"{item_id}: 题面仍为空或包含模板占位符")
    if response_type not in SUPPORTED_TYPES:
        blockers.append(f"{item_id}: 不支持自动映射的题型 {response_type!r}")
        return None

    display_logic = text(item.get("display_logic"), "always")
    skip_logic = text(item.get("skip_logic"), "next")
    if display_logic != "always" or skip_logic != "next":
        blockers.append(
            f"{item_id}: 含显示/跳转逻辑（display={display_logic!r}, skip={skip_logic!r}），"
            "必须在问卷星草稿中人工配置并完成全路径测试"
        )

    randomization = text(item.get("randomization"), "none")
    if randomization != "none":
        blockers.append(f"{item_id}: 含随机化设置 {randomization!r}，不得在自动转换时静默省略")

    result: dict[str, Any] = {
        "qtype": "",
        "title": item_title(item),
        "requir": bool(item.get("required", False)),
    }
    instruction_parts = [text(item.get("instruction")), text(item.get("help_text"))]
    instruction = "；".join(part for part in instruction_parts if part)
    if instruction:
        result["ins"] = instruction

    options = [text(option.get("label")) for option in item.get("response_options", []) if isinstance(option, dict)]
    options = [option for option in options if option]
    missing = visible_missing_labels(item)

    if response_type in CHOICE_TYPES:
        if len(options) < 2:
            blockers.append(f"{item_id}: 选择/量表题少于两个实质选项")
        result["qtype"] = {
            "single-choice": "单选",
            "multiple-choice": "多选",
            "ordinal-rating": "量表题",
        }[response_type]
        result["select"] = options + [label for label in missing if label not in options]
    elif response_type in ROW_OPTION_TYPES:
        if len(options) < 2:
            blockers.append(f"{item_id}: 排序/比重题少于两个项目")
        result["qtype"] = "排序" if response_type == "ranking" else "比重题"
        key = "select" if response_type == "ranking" else "rowtitle"
        result[key] = options
        if response_type == "constant-sum":
            result["total"] = "100"
        if missing and result["requir"]:
            blockers.append(
                f"{item_id}: 必答的排序/比重题同时要求显示 {', '.join(missing)}；"
                "需重设拒答机制或改为非必答后人工复核"
            )
    elif response_type == "numeric":
        result.update({"qtype": "单项填空", "verify": "数字"})
    elif response_type == "date-or-time":
        result["qtype"] = "日期"
    elif response_type == "open-text":
        result["qtype"] = "简答题"

    if response_type not in CHOICE_TYPES and missing and result["requir"]:
        blockers.append(
            f"{item_id}: 必答的非选择题要求显示 {', '.join(missing)}，"
            "当前自动映射无法同时保留缺失选项编码"
        )
    elif response_type not in CHOICE_TYPES and missing:
        warnings.append(f"{item_id}: 非选择题的缺失选项不会作为可点击选项显示；该题保持非必答")

    return result


def consent_block(spec: dict[str, Any], form: dict[str, Any]) -> dict[str, Any]:
    materials = spec.get("participant_materials", {})
    parts = [
        f"研究机构/团队：{text(materials.get('organization'), '[待填写]')}",
        text(materials.get("study_purpose")),
        text(form.get("introduction")),
        text(materials.get("voluntary_statement")),
        text(materials.get("privacy_statement")),
        f"联系方式：{text(materials.get('contact'), '[待填写]')}",
        text(materials.get("consent_prompt")),
    ]
    return {"qtype": "知情同意书", "content": "\n\n".join(part for part in parts if part)}


def build_form(spec: dict[str, Any], form: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str], list[str], list[str]]:
    instrument = spec.get("instrument", {})
    materials = spec.get("participant_materials", {})
    form_id = text(form.get("id"), "F1")
    population_id = text(form.get("population_id"))
    title = text(form.get("title"), text(instrument.get("title"), "问卷草稿"))
    language = text(form.get("language"), "zh-CN")
    introduction = "\n".join(
        part for part in [text(materials.get("study_purpose")), text(form.get("introduction")), text(form.get("instructions"))] if part
    )
    end_message = text(materials.get("completion_message"), "感谢您的参与。")

    blockers: list[str] = []
    warnings: list[str] = []
    if not title or is_placeholder(title):
        blockers.append(f"{form_id}: 问卷标题为空或仍包含模板占位符")
    required_participant_fields = {
        "organization": "研究机构/团队",
        "study_purpose": "研究目的",
        "privacy_statement": "隐私说明",
        "consent_prompt": "参与同意",
        "contact": "联系方式",
    }
    for field, label in required_participant_fields.items():
        if not text(materials.get(field)) or is_placeholder(materials.get(field)):
            blockers.append(f"{form_id}: {label}为空或仍包含模板占位符")

    jsonl: list[dict[str, Any]] = [{
        "qtype": "问卷基础信息",
        "title": title,
        "atype": 1,
        "introduction": introduction,
        "endpageinformation": end_message,
        "language": "zh" if language.lower().startswith("zh") else language,
    }]
    if materials:
        jsonl.append(consent_block(spec, form))

    relevant = [
        item for item in spec.get("items", [])
        if isinstance(item, dict) and population_id in item.get("population_ids", [])
    ]
    by_section: dict[str, list[dict[str, Any]]] = {}
    for item in relevant:
        by_section.setdefault(text(item.get("section_id"), "__unsectioned__"), []).append(item)

    optional_titles: list[str] = []
    rendered_ids: set[str] = set()
    sections = [section for section in spec.get("sections", []) if isinstance(section, dict)]
    for section in sections:
        allowed = section.get("population_ids")
        if isinstance(allowed, list) and population_id not in allowed:
            continue
        section_id = text(section.get("id"))
        section_items = by_section.get(section_id, [])
        if not section_items:
            continue
        jsonl.append({
            "qtype": "段落说明",
            "title": text(section.get("title"), "问卷部分"),
            "ins": text(section.get("introduction")),
        })
        for item in section_items:
            mapped = map_item(item, blockers, warnings)
            if mapped is not None:
                jsonl.append(mapped)
                if mapped.get("requir") is False:
                    optional_titles.append(str(mapped["title"]))
            rendered_ids.add(text(item.get("id")))

    leftovers = [item for item in relevant if text(item.get("id")) not in rendered_ids]
    if leftovers:
        jsonl.append({"qtype": "段落说明", "title": "其他题目"})
        for item in leftovers:
            mapped = map_item(item, blockers, warnings)
            if mapped is not None:
                jsonl.append(mapped)
                if mapped.get("requir") is False:
                    optional_titles.append(str(mapped["title"]))

    if not relevant:
        blockers.append(f"{form_id}: 没有适用于 population_id={population_id!r} 的题目")
    return jsonl, optional_titles, blockers, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare Wenjuanxing JSONL payloads without creating or publishing surveys")
    parser.add_argument("spec", type=Path, help="Validated questionnaire specification JSON")
    parser.add_argument("output_dir", type=Path, help="Directory for internal JSONL payloads and manifest")
    args = parser.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    forms = spec.get("forms")
    if not isinstance(forms, list) or not forms:
        raise SystemExit("ERROR: questionnaire spec must contain at least one form")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {
        "schema": "mixed-methods-instrument-design/wjx-draft-manifest/v1",
        "source_spec": str(args.spec.resolve()),
        "publish_default": False,
        "forms": [],
    }
    total_blockers = 0
    for form in forms:
        if not isinstance(form, dict):
            continue
        form_id = text(form.get("id"), f"F{len(manifest['forms']) + 1}")
        payload, optional_titles, blockers, warnings = build_form(spec, form)
        payload_path = args.output_dir / f"{safe_name(form_id)}.wjx.jsonl"
        payload_path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in payload), encoding="utf-8")
        total_blockers += len(blockers)
        manifest["forms"].append({
            "form_id": form_id,
            "population_id": text(form.get("population_id")),
            "title": text(form.get("title"), text(spec.get("instrument", {}).get("title"))),
            "payload": str(payload_path.resolve()),
            "optional_titles": optional_titles,
            "status": "manual-review-required" if blockers else "ready-for-draft",
            "blockers": blockers,
            "warnings": warnings,
            "draft_command": [
                "wjx", "survey", "create-by-json", "--file", str(payload_path.resolve()),
                "--type", "1", "--optional_titles", json.dumps(optional_titles, ensure_ascii=False),
            ],
        })

    manifest["status"] = "manual-review-required" if total_blockers else "ready-for-draft"
    manifest_path = args.output_dir / "wjx-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "manifest": str(manifest_path.resolve()),
        "status": manifest["status"],
        "forms": len(manifest["forms"]),
        "blockers": total_blockers,
    }, ensure_ascii=False))
    return 2 if total_blockers else 0


if __name__ == "__main__":
    sys.exit(main())
