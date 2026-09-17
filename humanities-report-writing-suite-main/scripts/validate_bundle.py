from __future__ import annotations

import hashlib
import json
import pathlib
import zipfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "humanities-report-writer",
    "humanizer",
    "source-grounded-research",
    "word-report-delivery",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def frontmatter_name(skill_file: pathlib.Path) -> str:
    lines = skill_file.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        fail(f"missing frontmatter: {skill_file}")

    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip()
    fail(f"missing skill name: {skill_file}")


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    manifest_path = ROOT / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    skills = manifest.get("skills", [])
    names = {item.get("name") for item in skills}

    if names != EXPECTED_SKILLS:
        fail(f"unexpected skill set: {sorted(names)}")

    install_order = manifest.get("install_order", [])
    if set(install_order) != EXPECTED_SKILLS or install_order[-1] != "humanities-report-writer":
        fail("invalid install order")

    for item in skills:
        folder = ROOT / item["path"]
        skill_file = folder / "SKILL.md"
        if not skill_file.is_file():
            fail(f"missing {skill_file}")
        if folder.name != item["name"] or frontmatter_name(skill_file) != item["name"]:
            fail(f"skill name mismatch: {folder}")

    humanizer = next(item for item in skills if item["name"] == "humanizer")
    humanizer_root = ROOT / humanizer["path"]
    if sha256(humanizer_root / "SKILL.md") != humanizer["skill_sha256"]:
        fail("humanizer SKILL.md hash mismatch")
    if sha256(humanizer_root / "LICENSE") != humanizer["license_sha256"]:
        fail("humanizer LICENSE hash mismatch")

    template = ROOT / "skills" / "word-report-delivery" / "assets" / "通用人文社科报告模板.docx"
    with zipfile.ZipFile(template) as archive:
        if archive.testzip() is not None or "word/document.xml" not in archive.namelist():
            fail("invalid Word template")

    forbidden_suffixes = {".exe", ".bat", ".cmd", ".ps1", ".sh", ".py", ".js"}
    for path in (ROOT / "skills").rglob("*"):
        if path.is_file() and path.suffix.lower() in forbidden_suffixes:
            fail(f"unexpected executable or script in installable skills: {path}")

    print("bundle validation passed")


if __name__ == "__main__":
    main()
