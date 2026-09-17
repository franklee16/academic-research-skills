"""Match each gallery recreation raster to its paired original canvas.

The recreation pixels contain no hidden data: this only normalizes the review
canvas so the gallery's side-by-side pair has identical dimensions and scale.
The original image is never modified.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "gallery"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads((GALLERY / "data" / "basics.json").read_text(encoding="utf-8"))
    changed = []
    for sample in manifest["samples"]:
        original_path = GALLERY / sample["assets"]["original"]
        recreated_path = GALLERY / sample["assets"]["recreated"]
        with Image.open(original_path) as original, Image.open(recreated_path) as recreated:
            target_size = original.size
            source_size = recreated.size
            if source_size != target_size:
                normalized = recreated.convert("RGB").resize(target_size, Image.Resampling.LANCZOS)
                normalized.save(recreated_path)
                changed.append(
                    {
                        "id": sample["id"],
                        "original_size": list(target_size),
                        "recreated_size_before": list(source_size),
                        "recreated_size_after": list(target_size),
                    }
                )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "operation": "recreation_canvas_resize_only",
                "changed_cases": changed,
                "unchanged_cases": len(manifest["samples"]) - len(changed),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"REPORT={args.report}")
    print(f"NORMALIZED={len(changed)}")


if __name__ == "__main__":
    main()
