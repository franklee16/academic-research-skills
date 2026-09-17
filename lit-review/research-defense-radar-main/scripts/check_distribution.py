#!/usr/bin/env python3
"""Validate the standalone Research Defense Radar distribution."""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME = "research-defense-radar"


def frontmatter() -> dict[str, str]:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        raise ValueError("SKILL.md has no YAML frontmatter")
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip()
    return values


def main() -> None:
    errors: list[str] = []
    values = frontmatter()
    if values.get("name") != SKILL_NAME:
        errors.append("SKILL.md has the wrong skill name")
    description = values.get("description", "")
    if not description or len(description) > 1024:
        errors.append(f"description must be 1-1024 characters; got {len(description)}")

    required_paths = [
        "SKILL.md",
        "SKILL.zh-CN.md",
        "README.md",
        "LICENSE",
        "agents/openai.yaml",
        "assets/RESEARCH_PROFILE_TEMPLATE.md",
        "assets/RADAR_STATE_TEMPLATE.json",
        "assets/RADAR_STATE_SCHEMA.json",
        "assets/OBSERVATION_TEMPLATE.json",
        "assets/OBSERVATION_SCHEMA.json",
        "assets/COVERAGE_TEMPLATE.json",
        "assets/COVERAGE_SCHEMA.json",
        "assets/SEARCH_LOG_TEMPLATE.jsonl",
        "references/INSTALL.md",
        "references/AUTOMATION.md",
        "references/SEARCH_PLAYBOOK.md",
        "references/OUTPUT_SCHEMA.md",
        "references/DOMAIN_ADAPTATION.md",
        "references/STATE_SCHEMA.md",
        "scripts/package_skill.py",
        "scripts/update_radar_state.py",
        "scripts/test_update_radar_state.py",
        "evals/evals.json",
        "evals/trigger-evals.json",
        "packages/research-defense-radar.zip",
    ]
    for relative in required_paths:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    for relative in (
        "assets/RADAR_STATE_TEMPLATE.json",
        "assets/RADAR_STATE_SCHEMA.json",
        "assets/OBSERVATION_TEMPLATE.json",
        "assets/OBSERVATION_SCHEMA.json",
        "assets/COVERAGE_TEMPLATE.json",
        "assets/COVERAGE_SCHEMA.json",
        "evals/evals.json",
        "evals/trigger-evals.json",
    ):
        try:
            json.loads((ROOT / relative).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON in {relative}: {exc}")

    try:
        for line_number, line in enumerate(
            (ROOT / "assets/SEARCH_LOG_TEMPLATE.jsonl").read_text(encoding="utf-8").splitlines(), 1
        ):
            if line.strip():
                json.loads(line)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSONL in assets/SEARCH_LOG_TEMPLATE.jsonl: {exc}")

    try:
        eval_data = json.loads((ROOT / "evals/evals.json").read_text(encoding="utf-8"))
        for item in eval_data.get("evals", []):
            if not item.get("expectations"):
                errors.append(f"eval {item.get('id')} has no executable expectations")
            for relative in item.get("files", []):
                if not (ROOT / relative).is_file():
                    errors.append(f"eval {item.get('id')} references missing fixture: {relative}")
    except (OSError, json.JSONDecodeError, AttributeError) as exc:
        errors.append(f"could not validate eval fixtures: {exc}")

    package = ROOT / "packages/research-defense-radar.zip"
    if package.is_file():
        with zipfile.ZipFile(package) as archive:
            names = archive.namelist()
        if f"{SKILL_NAME}/SKILL.md" not in names:
            errors.append("upload package is missing its root SKILL.md")
        for relative in (
            "assets/OBSERVATION_TEMPLATE.json",
            "assets/COVERAGE_TEMPLATE.json",
            "assets/SEARCH_LOG_TEMPLATE.jsonl",
            "references/STATE_SCHEMA.md",
        ):
            if f"{SKILL_NAME}/{relative}" not in names:
                errors.append(f"upload package is missing {relative}")
        skill_files = [name for name in names if name.endswith("/SKILL.md")]
        if skill_files != [f"{SKILL_NAME}/SKILL.md"]:
            errors.append(f"upload package must contain exactly one SKILL.md: {skill_files}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for marker in (
        "SuperJayLiu/research-defense-radar",
        "~/.agents/skills/research-defense-radar",
        "~/.claude/skills/research-defense-radar",
        "$research-defense-radar",
        "/research-defense-radar",
    ):
        if marker not in readme and marker not in (ROOT / "references/INSTALL.md").read_text(encoding="utf-8"):
            errors.append(f"deployment documentation is missing {marker}")

    if errors:
        print("distribution checks failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("distribution checks: ok")


if __name__ == "__main__":
    main()
