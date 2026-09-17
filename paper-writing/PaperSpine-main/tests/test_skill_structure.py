from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillStructureTests(unittest.TestCase):
    def test_required_project_files_exist(self) -> None:
        required = [
            "SKILL.md",
            "README.md",
            "LICENSE",
            ".gitignore",
            "agents/openai.yaml",
            "references/task-genre-research.md",
            "references/version-requirements.md",
            "scripts/latex_guard.py",
            "scripts/revision_audit.py",
            "scripts/style_metrics.py",
        ]
        missing = [path for path in required if not (ROOT / path).exists()]
        self.assertEqual(missing, [])

    def test_no_temporary_artifact_directories(self) -> None:
        tmp_dirs = [path.name for path in ROOT.glob("tmp_*_artifacts") if path.is_dir()]
        self.assertEqual(tmp_dirs, [])

    def test_no_obvious_local_private_paths_in_reusable_files(self) -> None:
        reusable_suffixes = {".md", ".py", ".yaml", ".yml", ".txt"}
        blocked_fragments = [
            "C:" + "\\Users\\",
            "/Users/",
            "file:" + "///",
            "Bio" + "informatics",
            "M:" + "\\" + "R" + "BP" + "\\",
            "paper" + "_v",
            "oup-" + "authoring",
        ]
        offenders: list[str] = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in reusable_suffixes:
                continue
            if path.name == "test_skill_structure.py":
                continue
            if ".git" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for fragment in blocked_fragments:
                if fragment in text:
                    offenders.append(str(path.relative_to(ROOT)))
                    break
        self.assertEqual(offenders, [])

    def test_frontmatter_description_is_portable(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        lines = text.splitlines()
        description = next(line for line in lines if line.startswith("description: "))
        value = description.removeprefix("description: ").strip()
        self.assertLessEqual(len(value), 200)


if __name__ == "__main__":
    unittest.main()
