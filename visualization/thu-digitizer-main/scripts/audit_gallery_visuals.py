"""Create review sheets and coarse geometry checks for gallery image pairs.

This is an audit aid, not a numeric validation gate.  It keeps each original
and recreation in equally sized canvases so a reviewer can judge visual
similarity without a browser layout affecting the comparison.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "gallery"


def foreground_mask(image: Image.Image) -> np.ndarray:
    """Mark non-paper pixels, tolerating JPEG/antialiased white backgrounds."""
    pixels = np.asarray(image.convert("RGB"), dtype=np.int16)
    near_white = np.all(pixels >= 244, axis=2)
    return ~near_white


def bbox(mask: np.ndarray) -> list[int] | None:
    rows, columns = np.where(mask)
    if not len(rows):
        return None
    return [int(columns.min()), int(rows.min()), int(columns.max()) + 1, int(rows.max()) + 1]


def fit_to_canvas(image: Image.Image, width: int, height: int) -> Image.Image:
    canvas = Image.new("RGB", (width, height), "white")
    copy = ImageOps.contain(image.convert("RGB"), (width, height), Image.Resampling.LANCZOS)
    canvas.paste(copy, ((width - copy.width) // 2, (height - copy.height) // 2))
    return canvas


def pair_metrics(original: Image.Image, recreated: Image.Image) -> dict:
    if original.size != recreated.size:
        return {
            "same_dimensions": False,
            "original_size": list(original.size),
            "recreated_size": list(recreated.size),
            "foreground_iou": None,
            "original_foreground_bbox": bbox(foreground_mask(original)),
            "recreated_foreground_bbox": bbox(foreground_mask(recreated)),
        }
    first = foreground_mask(original)
    second = foreground_mask(recreated)
    union = int(np.count_nonzero(first | second))
    overlap = int(np.count_nonzero(first & second))
    return {
        "same_dimensions": True,
        "original_size": list(original.size),
        "recreated_size": list(recreated.size),
        "foreground_iou": round(overlap / union, 4) if union else 1.0,
        "original_foreground_bbox": bbox(first),
        "recreated_foreground_bbox": bbox(second),
    }


def draw_pair(
    sheet: Image.Image,
    *,
    origin: tuple[int, int],
    sample_id: str,
    original: Image.Image,
    recreated: Image.Image,
    metrics: dict,
    cell_width: int,
    image_height: int,
) -> None:
    x, y = origin
    draw = ImageDraw.Draw(sheet)
    draw.text((x, y), sample_id, fill="#111")
    draw.text((x + cell_width // 2, y), "original", fill="#555")
    draw.text((x + cell_width + 18, y), "recreated", fill="#555")
    first = fit_to_canvas(original, cell_width, image_height)
    second = fit_to_canvas(recreated, cell_width, image_height)
    top = y + 22
    sheet.paste(first, (x, top))
    sheet.paste(second, (x + cell_width + 18, top))
    draw.rectangle((x, top, x + cell_width - 1, top + image_height - 1), outline="#bdbdbd")
    draw.rectangle((x + cell_width + 18, top, x + cell_width * 2 + 17, top + image_height - 1), outline="#bdbdbd")
    iou = metrics["foreground_iou"]
    note = f"ink IoU {iou:.2f}" if iou is not None else "different native canvas"
    draw.text((x, top + image_height + 4), note, fill="#666")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--per-sheet", type=int, default=4)
    parser.add_argument("--cell-width", type=int, default=420)
    parser.add_argument("--image-height", type=int, default=230)
    args = parser.parse_args()
    if args.per_sheet < 1:
        raise SystemExit("--per-sheet must be positive")
    manifest = json.loads((GALLERY / "data" / "basics.json").read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    audit = []
    pairs = []
    for sample in manifest["samples"]:
        original_path = GALLERY / sample["assets"]["original"]
        recreated_path = GALLERY / sample["assets"]["recreated"]
        with Image.open(original_path) as source, Image.open(recreated_path) as reconstruction:
            original = source.convert("RGB")
            recreated = reconstruction.convert("RGB")
        metrics = pair_metrics(original, recreated)
        audit.append({"id": sample["id"], **metrics})
        pairs.append((sample["id"], original, recreated, metrics))

    row_height = args.image_height + 48
    sheet_width = args.cell_width * 2 + 54
    for start in range(0, len(pairs), args.per_sheet):
        chunk = pairs[start : start + args.per_sheet]
        sheet = Image.new("RGB", (sheet_width, 14 + len(chunk) * row_height), "white")
        for row, (sample_id, original, recreated, metrics) in enumerate(chunk):
            draw_pair(
                sheet,
                origin=(14, 14 + row * row_height),
                sample_id=sample_id,
                original=original,
                recreated=recreated,
                metrics=metrics,
                cell_width=args.cell_width,
                image_height=args.image_height,
            )
        sheet.save(args.output_dir / f"audit-{start // args.per_sheet + 1:02d}.png")

    report = {"schema_version": 1, "purpose": "visual_review_aid_not_numeric_validation", "cases": audit}
    (args.output_dir / "audit-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    same = sum(case["same_dimensions"] for case in audit)
    print(f"REPORT={args.output_dir / 'audit-report.json'}")
    print(f"SHEETS={(len(pairs) + args.per_sheet - 1) // args.per_sheet} SAME_DIMENSIONS={same}/{len(audit)}")


if __name__ == "__main__":
    main()
