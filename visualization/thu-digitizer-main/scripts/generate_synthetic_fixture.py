"""Generate a local, non-sensitive line-chart fixture with known truth data."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from PIL import Image, ImageDraw


WIDTH, HEIGHT = 500, 350
LEFT, TOP, RIGHT, BOTTOM = 60, 20, 460, 310
X_VALUES = [0, 1, 2, 3, 4, 5]
SERIES = {
    "biodiversity": {"color": "#e31a1c", "values": [25, 10, 13, 7, 17, 9], "marker": "square"},
    "ecosystem_services": {"color": "#bdbdbd", "values": [27, 13, 19, 20, 35, 21], "marker": "circle"},
    "economic_language": {"color": "#0000dc", "values": [40, 33, 25, 32, 43, 40], "marker": "triangle"},
}
ERROR_BARS = [(11, 51), (5, 31), (4, 28), (5, 33), (6, 39), (8, 42)]


def px_x(value: float) -> int:
    return round(LEFT + (value / 5) * (RIGHT - LEFT))


def px_y(value: float) -> int:
    return round(BOTTOM - (value / 70) * (BOTTOM - TOP))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((LEFT, TOP, RIGHT, BOTTOM), outline="black", width=1)
    for value in range(0, 71, 10):
        y = px_y(value)
        draw.line((LEFT - 4, y, LEFT, y), fill="black", width=1)

    for x, (lower, upper) in zip(X_VALUES, ERROR_BARS):
        cx = px_x(x)
        top = px_y(upper)
        bottom = px_y(lower)
        draw.line((cx, top, cx, bottom), fill="#e6e6e6", width=1)
        draw.line((cx - 4, top, cx + 4, top), fill="#e6e6e6", width=1)
        draw.line((cx - 4, bottom, cx + 4, bottom), fill="#e6e6e6", width=1)

    for definition in SERIES.values():
        color = definition["color"]
        points = [(px_x(x), px_y(y)) for x, y in zip(X_VALUES, definition["values"])]
        draw.line(points, fill=color, width=2)
        for x, y in points:
            if definition["marker"] == "square":
                draw.rectangle((x - 3, y - 3, x + 3, y + 3), fill=color)
            elif definition["marker"] == "circle":
                draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=color)
            else:
                draw.polygon(((x, y - 4), (x - 4, y + 3), (x + 4, y + 3)), fill=color)

    image_path = args.output_dir / "synthetic_line_chart.png"
    image.save(image_path)
    truth_path = args.output_dir / "truth.csv"
    with truth_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["x", *SERIES.keys()])
        writer.writeheader()
        for index, x in enumerate(X_VALUES):
            writer.writerow({"x": x, **{name: data["values"][index] for name, data in SERIES.items()}})
    fixture = {
        "image": image_path.name,
        "calibration": {
            "x": [{"pixel": LEFT, "value": 0}, {"pixel": RIGHT, "value": 5}],
            "y": [{"pixel": TOP, "value": 70}, {"pixel": BOTTOM, "value": 0}],
            "plot_bounds": [LEFT, TOP, RIGHT, BOTTOM],
        },
        "error_bars": [{"x": x, "lower": lower, "upper": upper} for x, (lower, upper) in zip(X_VALUES, ERROR_BARS)],
    }
    (args.output_dir / "fixture.json").write_text(json.dumps(fixture, indent=2), encoding="utf-8")
    print(f"FIXTURE={image_path}")
    print(f"TRUTH={truth_path}")


if __name__ == "__main__":
    main()
