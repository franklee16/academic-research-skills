#!/usr/bin/env python3
"""Build a clean Agent Skills ZIP for ChatGPT/Codex and Claude."""

from __future__ import annotations

import argparse
import tempfile
import zipfile
from pathlib import Path


SKILL_NAME = "research-defense-radar"
SKILL_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = SKILL_ROOT
BUNDLE_DIRS = ("assets", "references", "scripts", "agents")
ROOT_FILES = ("SKILL.md", "SKILL.zh-CN.md", "README.md")
EXCLUDED_PARTS = {"__pycache__", ".DS_Store"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


def iter_files():
    for name in ROOT_FILES:
        path = SKILL_ROOT / name
        if path.is_file():
            yield path, Path(name)
    license_path = REPO_ROOT / "LICENSE"
    if license_path.is_file():
        yield license_path, Path("LICENSE")
    for dirname in BUNDLE_DIRS:
        base = SKILL_ROOT / dirname
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            if any(part in EXCLUDED_PARTS for part in path.parts):
                continue
            if path.suffix in EXCLUDED_SUFFIXES:
                continue
            yield path, path.relative_to(SKILL_ROOT)


def build_archive(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source, relative in iter_files():
            archive_name = (Path(SKILL_NAME) / relative).as_posix()
            info = zipfile.ZipInfo(archive_name, date_time=ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes())


def validate_archive(path: Path) -> None:
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
    required = {
        f"{SKILL_NAME}/SKILL.md",
        f"{SKILL_NAME}/SKILL.zh-CN.md",
        f"{SKILL_NAME}/assets/RESEARCH_PROFILE_TEMPLATE.md",
        f"{SKILL_NAME}/assets/RADAR_STATE_TEMPLATE.json",
        f"{SKILL_NAME}/assets/OBSERVATION_TEMPLATE.json",
        f"{SKILL_NAME}/assets/COVERAGE_TEMPLATE.json",
        f"{SKILL_NAME}/assets/SEARCH_LOG_TEMPLATE.jsonl",
        f"{SKILL_NAME}/references/INSTALL.md",
        f"{SKILL_NAME}/references/STATE_SCHEMA.md",
        f"{SKILL_NAME}/scripts/update_radar_state.py",
    }
    missing = sorted(required - names)
    if missing:
        raise ValueError("archive is missing: " + ", ".join(missing))
    skill_files = [name for name in names if name.endswith("/SKILL.md")]
    if skill_files != [f"{SKILL_NAME}/SKILL.md"]:
        raise ValueError(f"archive must contain exactly one SKILL.md; found {skill_files}")
    if any(name.startswith(".git/") or "/.git/" in name for name in names):
        raise ValueError("archive contains Git metadata")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="dist/research-defense-radar.zip")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / f"{SKILL_NAME}.zip"
            build_archive(output)
            validate_archive(output)
        print("research-defense-radar package self-test: ok")
        return

    output = Path(args.out).expanduser().resolve()
    build_archive(output)
    validate_archive(output)
    print(output)


if __name__ == "__main__":
    main()
