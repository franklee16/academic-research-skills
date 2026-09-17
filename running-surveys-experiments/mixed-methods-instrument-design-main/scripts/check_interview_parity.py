#!/usr/bin/env python3
"""Check that the bundled interview baseline matches the standalone skill."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


EXCLUDED = {"README.md", ".gitignore"}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def inventory(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): digest(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.name not in EXCLUDED
    }


def main() -> int:
    skill_root = Path(__file__).resolve().parents[1]
    default_original = skill_root.parent / "interview-guide-design"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", type=Path, default=default_original)
    parser.add_argument("--require-original", action="store_true")
    args = parser.parse_args()

    bundled = skill_root / "references" / "interview-guide-design"
    if not args.original.is_dir():
        if args.require_original:
            print(f"ERROR: original skill not found: {args.original}")
            return 2
        print(f"SKIP: original skill not found: {args.original}")
        return 0

    original_files = inventory(args.original)
    bundled_files = inventory(bundled)
    missing = sorted(set(original_files) - set(bundled_files))
    extra = sorted(set(bundled_files) - set(original_files))
    changed = sorted(
        path
        for path in set(original_files) & set(bundled_files)
        if original_files[path] != bundled_files[path]
    )

    for path in missing:
        print(f"MISSING: {path}")
    for path in extra:
        print(f"EXTRA: {path}")
    for path in changed:
        print(f"CHANGED: {path}")
    if missing or extra or changed:
        print(
            f"FAIL: {len(missing)} missing, {len(extra)} extra, "
            f"{len(changed)} changed"
        )
        return 1
    print(f"PASS: {len(original_files)} interview baseline files are identical")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
