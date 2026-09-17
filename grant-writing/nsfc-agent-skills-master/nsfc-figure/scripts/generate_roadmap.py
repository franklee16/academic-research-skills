#!/usr/bin/env python3
"""Generate an editable, uncompressed Draw.io technical-roadmap document.

The input schema intentionally stays small: a title, a subtitle, two to four
research stages, and a final outcome. Stable geometry and explicit cell IDs
make the generated XML suitable for code review and later manual refinement in
diagrams.net.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path
from typing import Any

from validate_drawio import validate_file

PAGE_WIDTH = 1200
PAGE_HEIGHT = 780
PALETTE = ("#E67E22", "#2E9D50", "#2F80ED", "#8E5CC7")
HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")


@dataclass
class IdFactory:
    """Create deterministic, human-readable cell IDs for stable diffs."""

    counter: int = 0

    def new(self, prefix: str) -> str:
        self.counter += 1
        return f"{prefix}-{self.counter}"


def _required_text(mapping: dict[str, Any], key: str, context: str) -> str:
    """Return a normalized required string or raise an actionable error."""

    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{context}.{key} must be a non-empty string")
    return value.strip()


def validate_config(config: dict[str, Any]) -> None:
    """Validate content constraints that protect the fixed roadmap layout."""

    _required_text(config, "title", "config")
    _required_text(config, "subtitle", "config")
    _required_text(config, "final_outcome", "config")

    stages = config.get("stages")
    if not isinstance(stages, list) or not 2 <= len(stages) <= 4:
        raise ValueError("config.stages must contain two to four stages")

    for stage_index, stage in enumerate(stages, start=1):
        context = f"config.stages[{stage_index - 1}]"
        if not isinstance(stage, dict):
            raise TypeError(f"{context} must be an object")
        for key in ("title", "summary", "output"):
            _required_text(stage, key, context)
        tasks = stage.get("tasks")
        if not isinstance(tasks, list) or not 1 <= len(tasks) <= 4:
            raise ValueError(f"{context}.tasks must contain one to four tasks")
        for task_index, task in enumerate(tasks):
            task_context = f"{context}.tasks[{task_index}]"
            if not isinstance(task, dict):
                raise TypeError(f"{task_context} must be an object")
            _required_text(task, "title", task_context)
            _required_text(task, "detail", task_context)

        color = stage.get("color", PALETTE[(stage_index - 1) % len(PALETTE)])
        if not isinstance(color, str) or not HEX_COLOR.fullmatch(color):
            raise ValueError(f"{context}.color must use #RRGGBB notation")


def _style(*parts: str, **values: object) -> str:
    """Build a Draw.io style string without silently dropping zero values."""

    tokens = [part.strip(";") for part in parts if part]
    tokens.extend(f"{key}={value}" for key, value in values.items())
    return ";".join(tokens) + ";"


def _tint(color: str, white_ratio: float = 0.90) -> str:
    """Blend a #RRGGBB accent toward white for a restrained panel fill."""

    rgb = [int(color[index : index + 2], 16) for index in (1, 3, 5)]
    mixed = [round(channel * (1 - white_ratio) + 255 * white_ratio) for channel in rgb]
    return "#" + "".join(f"{channel:02X}" for channel in mixed)


def _safe_text(value: str) -> str:
    """Escape user content before placing it inside Draw.io HTML labels."""

    return html.escape(value, quote=True).replace("\n", "<br>")


def _rich_label(title: str, detail: str, accent: str | None = None) -> str:
    """Return a compact two-level HTML label supported by diagrams.net."""

    title_color = accent or "#243746"
    return (
        f'<div style="color:{title_color};font-weight:700;">{_safe_text(title)}</div>'
        f'<div style="margin-top:5px;color:#52616B;line-height:1.35;">'
        f"{_safe_text(detail)}</div>"
    )


def _add_vertex(
    root: ET.Element,
    cell_id: str,
    value: str,
    style: str,
    x: float,
    y: float,
    width: float,
    height: float,
) -> str:
    """Append an absolute-positioned vertex and return its ID."""

    cell = ET.SubElement(
        root,
        "mxCell",
        {"id": cell_id, "value": value, "style": style, "vertex": "1", "parent": "1"},
    )
    ET.SubElement(
        cell,
        "mxGeometry",
        {
            "x": f"{x:.2f}",
            "y": f"{y:.2f}",
            "width": f"{width:.2f}",
            "height": f"{height:.2f}",
            "as": "geometry",
        },
    )
    return cell_id


def _add_edge(
    root: ET.Element,
    cell_id: str,
    source: str,
    target: str,
    *,
    dashed: bool = False,
    exit_x: float | None = None,
    exit_y: float | None = None,
    entry_x: float | None = None,
    entry_y: float | None = None,
    waypoints: list[tuple[float, float]] | None = None,
) -> str:
    """Append a source/target edge with a predictable orthogonal route."""

    anchors = []
    if exit_x is not None and exit_y is not None:
        anchors.extend((f"exitX={exit_x:.3f}", f"exitY={exit_y:.3f}", "exitDx=0", "exitDy=0"))
    if entry_x is not None and entry_y is not None:
        anchors.extend(
            (f"entryX={entry_x:.3f}", f"entryY={entry_y:.3f}", "entryDx=0", "entryDy=0")
        )
    style = _style(
        "edgeStyle=orthogonalEdgeStyle",
        "rounded=1",
        "orthogonalLoop=1",
        "jettySize=auto",
        "html=1",
        "endArrow=block",
        "endFill=1",
        "strokeWidth=2",
        "strokeColor=#AAB7C4",
        f"dashed={1 if dashed else 0}",
        *anchors,
    )
    cell = ET.SubElement(
        root,
        "mxCell",
        {
            "id": cell_id,
            "style": style,
            "edge": "1",
            "parent": "1",
            "source": source,
            "target": target,
        },
    )
    geometry = ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
    if waypoints:
        points = ET.SubElement(geometry, "Array", {"as": "points"})
        for x, y in waypoints:
            ET.SubElement(points, "mxPoint", {"x": f"{x:.2f}", "y": f"{y:.2f}"})
    return cell_id


def build_document(config: dict[str, Any]) -> ET.ElementTree:
    """Build the complete editable Draw.io document for a roadmap config."""

    validate_config(config)
    ids = IdFactory()
    stages: list[dict[str, Any]] = config["stages"]
    # Four-stage routes need more horizontal space to preserve readable cards.
    page_width = 1440 if len(stages) == 4 else PAGE_WIDTH

    mxfile = ET.Element(
        "mxfile",
        {"host": "app.diagrams.net", "type": "device", "compressed": "false"},
    )
    diagram = ET.SubElement(mxfile, "diagram", {"id": "roadmap", "name": "Page-1"})
    model = ET.SubElement(
        diagram,
        "mxGraphModel",
        {
            "dx": str(page_width),
            "dy": "780",
            "grid": "1",
            "gridSize": "10",
            "guides": "1",
            "tooltips": "1",
            "connect": "1",
            "arrows": "1",
            "fold": "1",
            "page": "1",
            "pageScale": "1",
            "pageWidth": str(page_width),
            "pageHeight": str(PAGE_HEIGHT),
            "math": "0",
            "shadow": "0",
        },
    )
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    title_style = _style(
        "rounded=1",
        "whiteSpace=wrap",
        "html=1",
        "shadow=1",
        "arcSize=8",
        "fillColor=#FFFFFF",
        "strokeColor=#AAB7C4",
        "strokeWidth=1.5",
        "align=center",
        "verticalAlign=middle",
        "fontFamily=Microsoft YaHei",
        "fontSize=20",
        "fontColor=#243746",
        "spacing=8",
    )
    title_value = (
        f'<div style="font-size:20px;font-weight:700;">{_safe_text(config["title"])}</div>'
        f'<div style="margin-top:6px;font-size:13px;color:#60717E;">'
        f'{_safe_text(config["subtitle"])}</div>'
    )
    title_width = 960.0 if page_width == 1440 else 840.0
    title_x = (page_width - title_width) / 2
    _add_vertex(root, ids.new("title"), title_value, title_style, title_x, 20, title_width, 76)

    margin = 30.0
    gap = 24.0
    lane_y = 130.0
    lane_height = 520.0
    lane_width = (page_width - 2 * margin - gap * (len(stages) - 1)) / len(stages)
    # Each tuple keeps the source header route and the numbered chip used as
    # the next stage's visible arrow target. Targeting the chip avoids placing
    # an arrowhead over the first character of the stage title after export.
    stage_flow_nodes: list[tuple[str, float, str, float]] = []
    stage_outputs: list[str] = []

    for stage_index, stage in enumerate(stages, start=1):
        accent = stage.get("color", PALETTE[(stage_index - 1) % len(PALETTE)])
        tint = _tint(accent)
        lane_x = margin + (stage_index - 1) * (lane_width + gap)

        panel_style = _style(
            "rounded=1",
            "whiteSpace=wrap",
            "html=1",
            "arcSize=10",
            f"fillColor={tint}",
            f"strokeColor={accent}",
            "strokeWidth=1.5",
            "fontFamily=Microsoft YaHei",
        )
        _add_vertex(root, ids.new("panel"), "", panel_style, lane_x, lane_y, lane_width, lane_height)

        chip_size = 34.0
        chip_style = _style(
            "ellipse",
            "whiteSpace=wrap",
            "html=1",
            f"fillColor={accent}",
            f"strokeColor={accent}",
            "fontColor=#FFFFFF",
            "fontFamily=Arial",
            "fontSize=16",
            "fontStyle=1",
            "align=center",
            "verticalAlign=middle",
        )
        chip_id = _add_vertex(
            root,
            ids.new("number"),
            str(stage_index),
            chip_style,
            lane_x + 16,
            lane_y + 18,
            chip_size,
            chip_size,
        )

        header_style = _style(
            "rounded=0",
            "whiteSpace=wrap",
            "html=1",
            "fillColor=none",
            "strokeColor=none",
            "align=left",
            "verticalAlign=middle",
            "fontFamily=Microsoft YaHei",
            "fontSize=17",
            "fontStyle=1",
            f"fontColor={accent}",
        )
        header_id = _add_vertex(
            root,
            ids.new("stage"),
            _safe_text(stage["title"]),
            header_style,
            lane_x + 60,
            lane_y + 15,
            lane_width - 76,
            40,
        )
        stage_flow_nodes.append(
            (
                header_id,
                lane_x + lane_width - 16,
                chip_id,
                lane_x + 16 + chip_size / 2,
            )
        )

        summary_style = _style(
            "rounded=1",
            "whiteSpace=wrap",
            "html=1",
            "arcSize=8",
            "fillColor=#FFFFFF",
            f"strokeColor={_tint(accent, 0.55)}",
            "strokeWidth=1",
            "align=left",
            "verticalAlign=middle",
            "fontFamily=Microsoft YaHei",
            "fontSize=13",
            "fontColor=#3C4B55",
            "spacing=10",
            "overflow=hidden",
        )
        _add_vertex(
            root,
            ids.new("summary"),
            _rich_label("阶段目标", stage["summary"], accent),
            summary_style,
            lane_x + 16,
            lane_y + 68,
            lane_width - 32,
            82,
        )

        tasks: list[dict[str, str]] = stage["tasks"]
        task_top = lane_y + 168
        task_area_height = 250.0
        task_gap = 10.0
        task_height = min(88.0, (task_area_height - task_gap * (len(tasks) - 1)) / len(tasks))
        task_style = _style(
            "rounded=1",
            "whiteSpace=wrap",
            "html=1",
            "arcSize=8",
            "fillColor=#FFFFFF",
            "strokeColor=#D6DEE3",
            "strokeWidth=1",
            "align=left",
            "verticalAlign=middle",
            "fontFamily=Microsoft YaHei",
            "fontSize=12",
            "fontColor=#243746",
            "spacing=10",
            "overflow=hidden",
        )
        for task_index, task in enumerate(tasks):
            task_y = task_top + task_index * (task_height + task_gap)
            _add_vertex(
                root,
                ids.new("task"),
                _rich_label(task["title"], task["detail"]),
                task_style,
                lane_x + 16,
                task_y,
                lane_width - 32,
                task_height,
            )

        output_style = _style(
            "rounded=1",
            "whiteSpace=wrap",
            "html=1",
            "arcSize=10",
            f"fillColor={_tint(accent, 0.78)}",
            f"strokeColor={accent}",
            "strokeWidth=1.5",
            "align=center",
            "verticalAlign=middle",
            "fontFamily=Microsoft YaHei",
            "fontSize=13",
            "fontStyle=1",
            f"fontColor={accent}",
            "spacing=8",
            "overflow=hidden",
        )
        output_id = _add_vertex(
            root,
            ids.new("output"),
            f"阶段产出｜{_safe_text(stage['output'])}",
            output_style,
            lane_x + 16,
            lane_y + lane_height - 70,
            lane_width - 32,
            52,
        )
        stage_outputs.append(output_id)

    for (source, source_right, _, _), (_, _, target, target_center) in pairwise(
        stage_flow_nodes
    ):
        _add_edge(
            root,
            ids.new("sequence"),
            source,
            target,
            exit_x=1,
            exit_y=0.5,
            entry_x=0.5,
            entry_y=0,
            # Route above the panels and land on the numbered chip. The source
            # segment is hidden by the panel until it reaches the top border,
            # so the sequence reads as panel-to-next-stage without crossing text.
            waypoints=[(source_right, 112), (target_center, 112)],
        )

    final_style = _style(
        "rounded=1",
        "whiteSpace=wrap",
        "html=1",
        "shadow=1",
        "arcSize=10",
        "fillColor=#FFFFFF",
        "strokeColor=#4F6475",
        "strokeWidth=2",
        "align=center",
        "verticalAlign=middle",
        "fontFamily=Microsoft YaHei",
        "fontSize=15",
        "fontStyle=1",
        "fontColor=#243746",
        "spacing=10",
        "overflow=hidden",
    )
    final_id = _add_vertex(
        root,
        ids.new("final"),
        f"综合目标｜{_safe_text(config['final_outcome'])}",
        final_style,
        title_x,
        690,
        title_width,
        62,
    )
    for output_index, output_id in enumerate(stage_outputs, start=1):
        # Distinct target anchors keep converging evidence lines from stacking.
        final_entry_x = output_index / (len(stage_outputs) + 1)
        _add_edge(
            root,
            ids.new("converge"),
            output_id,
            final_id,
            dashed=True,
            exit_x=0.5,
            exit_y=1,
            entry_x=final_entry_x,
            entry_y=0,
        )

    ET.indent(mxfile, space="  ")
    return ET.ElementTree(mxfile)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate an editable Draw.io technical-roadmap document"
    )
    parser.add_argument("--config", required=True, type=Path, help="Roadmap JSON config")
    parser.add_argument("--output", required=True, type=Path, help="Output .drawio path")
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Write without post-generation structural validation",
    )
    args = parser.parse_args()

    try:
        with args.config.open(encoding="utf-8") as handle:
            config = json.load(handle)
        if not isinstance(config, dict):
            raise TypeError("top-level JSON value must be an object")
        tree = build_document(config)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        tree.write(args.output, encoding="utf-8", xml_declaration=True)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if not args.skip_validation:
        report = validate_file(args.output)
        if report.errors:
            for error in report.errors:
                print(f"Error: {error}", file=sys.stderr)
            return 1
        for warning in report.warnings:
            print(f"Warning: {warning}", file=sys.stderr)

    print(f"Generated editable Draw.io document: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
