#!/usr/bin/env python3
"""Snapshot and compare high-risk invariants in a LaTeX manuscript.

The guard is conservative and intentionally produces review-required findings
for ambiguous drift. Passing it is necessary but never proves semantic or
scientific equivalence.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Callable, Iterable


GUARD_VERSION = 2
SOURCE_EXTENSIONS = {
    ".tex", ".bib", ".sty", ".cls", ".bst", ".bbx", ".cbx", ".def", ".cfg", ".clo"
}
GRAPHICS_EXTENSIONS = ("", ".pdf", ".png", ".jpg", ".jpeg", ".eps", ".svg")
MATH_ENVS = (
    "equation", "equation*", "align", "align*", "gather", "gather*",
    "multline", "multline*", "eqnarray", "eqnarray*",
)
CODE_ENVS = ("algorithm", "algorithm*", "algorithmic", "lstlisting", "verbatim", "minted")
TABLE_ENVS = ("tabular", "tabular*", "longtable", "array")
DIRECTION_TERMS = re.compile(
    r"\b(?:outperform(?:s|ed|ing)?|underperform(?:s|ed|ing)?|"
    r"increase(?:s|d|ing)?|decrease(?:s|d|ing)?|higher|lower|"
    r"positive|negative|improve(?:s|d|ment|ments|ing)?|"
    r"worsen(?:s|ed|ing)?|significant|insignificant|"
    r"affect(?:s|ed|ing)?|cause(?:s|d|ing)?|change(?:s|d|ing)?|"
    r"produce(?:s|d|ing)?|determine(?:s|d|ing)?|"
    r"drive|drives|drove|driven|driving|shape(?:s|d|ing)?|"
    r"isolate(?:s|d|ing)?|associate(?:s|d|ing)?|"
    r"correlate(?:s|d|ing)?|depend(?:s|ed|ing)?|yield(?:s|ed|ing)?)\b",
    flags=re.IGNORECASE,
)
NUMBER_PATTERN = re.compile(
    r"(?<![A-Za-z\\])[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)"
    r"(?:\.\d+)?(?:[eE][-+]?\d+)?%?"
)
COMMAND_PATTERN = re.compile(r"\\([A-Za-z@]+)")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def counter(values: Iterable[str]) -> dict[str, int]:
    return dict(sorted(collections.Counter(values).items()))


def is_escaped(text: str, position: int) -> bool:
    slashes = 0
    position -= 1
    while position >= 0 and text[position] == "\\":
        slashes += 1
        position -= 1
    return slashes % 2 == 1


def strip_comments(text: str) -> str:
    output: list[str] = []
    for line in text.splitlines(keepends=True):
        cut = len(line)
        for index, char in enumerate(line):
            if char == "%" and not is_escaped(line, index):
                cut = index
                break
        kept = line[:cut]
        if line.endswith("\n") and not kept.endswith("\n"):
            kept += "\n"
        output.append(kept)
    return "".join(output)


def skip_space(text: str, position: int) -> int:
    while position < len(text) and text[position].isspace():
        position += 1
    return position


def read_balanced(
    text: str, position: int, opener: str, closer: str
) -> tuple[str, int] | None:
    if position >= len(text) or text[position] != opener:
        return None
    depth = 0
    index = position
    while index < len(text):
        char = text[index]
        if char == opener and not is_escaped(text, index):
            depth += 1
        elif char == closer and not is_escaped(text, index):
            depth -= 1
            if depth == 0:
                return text[position:index + 1], index + 1
        index += 1
    return None


def canonical(text: str) -> str:
    return re.sub(r"\s+", " ", strip_comments(text)).strip()


def canonical_math(text: str) -> str:
    return re.sub(r"\s+", "", strip_comments(text))


def scan_command_groups(
    text: str,
    accept: Callable[[str], bool],
    required_groups: int,
) -> list[tuple[str, list[str], list[str]]]:
    results: list[tuple[str, list[str], list[str]]] = []
    for match in COMMAND_PATTERN.finditer(text):
        name = match.group(1)
        if not accept(name):
            continue
        position = match.end()
        if position < len(text) and text[position] == "*":
            position += 1
        optional: list[str] = []
        required: list[str] = []
        while True:
            position = skip_space(text, position)
            group = read_balanced(text, position, "[", "]")
            if not group:
                break
            body, position = group
            optional.append(body[1:-1])
        for _ in range(required_groups):
            position = skip_space(text, position)
            group = read_balanced(text, position, "{", "}")
            if not group:
                required = []
                break
            body, position = group
            required.append(body[1:-1])
        if len(required) == required_groups:
            results.append((name, optional, required))
    return results


def command_values(text: str, names: set[str]) -> list[str]:
    calls = scan_command_groups(text, lambda value: value in names, 1)
    return [required[0].strip() for _, _, required in calls]


def citation_keys(text: str) -> list[str]:
    calls = scan_command_groups(text, lambda value: value.startswith("cite"), 1)
    return [
        key.strip()
        for _, _, required in calls
        for key in required[0].split(",")
        if key.strip()
    ]


def extract_environments(
    text: str,
    names: Iterable[str],
    normalizer: Callable[[str], str] = canonical,
) -> list[str]:
    blocks: list[str] = []
    for name in names:
        pattern = re.compile(
            rf"\\begin\{{{re.escape(name)}\}}.*?\\end\{{{re.escape(name)}\}}",
            flags=re.DOTALL,
        )
        blocks.extend(normalizer(match.group(0)) for match in pattern.finditer(text))
    return blocks


def extract_inline_math(text: str) -> list[str]:
    spans: list[str] = []
    index = 0
    while index < len(text):
        if text.startswith(r"\(", index) and not is_escaped(text, index):
            end = text.find(r"\)", index + 2)
            if end >= 0:
                spans.append(canonical_math(text[index:end + 2]))
                index = end + 2
                continue
        if text.startswith(r"\[", index) and not is_escaped(text, index):
            end = text.find(r"\]", index + 2)
            if end >= 0:
                spans.append(canonical_math(text[index:end + 2]))
                index = end + 2
                continue
        if text[index] == "$" and not is_escaped(text, index):
            delimiter = "$$" if text.startswith("$$", index) else "$"
            cursor = index + len(delimiter)
            while cursor < len(text):
                if text.startswith(delimiter, cursor) and not is_escaped(text, cursor):
                    spans.append(canonical_math(text[index:cursor + len(delimiter)]))
                    index = cursor + len(delimiter)
                    break
                cursor += 1
            else:
                index += len(delimiter)
            continue
        index += 1
    return spans


def extract_macro_definitions(text: str) -> dict[str, str]:
    definitions: dict[str, str] = {}
    definition_names = {
        "newcommand", "renewcommand", "providecommand", "DeclareRobustCommand",
        "DeclareMathOperator",
    }
    for match in COMMAND_PATTERN.finditer(text):
        if match.group(1) not in definition_names:
            continue
        position = match.end()
        if position < len(text) and text[position] == "*":
            position += 1
        position = skip_space(text, position)
        macro_name = ""
        macro_piece = ""
        grouped = read_balanced(text, position, "{", "}")
        if grouped:
            macro_piece, position = grouped
            name_match = re.search(r"\\([A-Za-z@]+)", macro_piece)
            macro_name = name_match.group(1) if name_match else ""
        elif position < len(text) and text[position] == "\\":
            name_match = COMMAND_PATTERN.match(text, position)
            if name_match:
                macro_name = name_match.group(1)
                macro_piece = name_match.group(0)
                position = name_match.end()
        if not macro_name:
            continue
        pieces = [match.group(0), macro_piece]
        while True:
            position = skip_space(text, position)
            optional = read_balanced(text, position, "[", "]")
            if not optional:
                break
            body, position = optional
            pieces.append(body)
        position = skip_space(text, position)
        replacement = read_balanced(text, position, "{", "}")
        if replacement:
            body, _ = replacement
            pieces.append(body)
        definitions[macro_name] = canonical("".join(pieces))
    return definitions


def extract_macro_calls(text: str, macro_names: set[str]) -> list[str]:
    calls: list[str] = []
    definition_commands = {
        "newcommand", "renewcommand", "providecommand", "DeclareRobustCommand",
        "DeclareMathOperator",
    }
    for match in COMMAND_PATTERN.finditer(text):
        name = match.group(1)
        if name not in macro_names or name in definition_commands:
            continue
        position = match.end()
        pieces = [match.group(0)]
        if position < len(text) and text[position] == "*":
            pieces.append("*")
            position += 1
        groups_found = 0
        while True:
            position = skip_space(text, position)
            if position >= len(text) or text[position] not in "[{":
                break
            opener = text[position]
            closer = "]" if opener == "[" else "}"
            group = read_balanced(text, position, opener, closer)
            if not group:
                break
            body, position = group
            pieces.append(body)
            groups_found += 1
        if groups_found:
            calls.append(canonical("".join(pieces)))
    return calls


def tex_snapshot(path: Path, macro_names: set[str]) -> dict[str, object]:
    raw_text = path.read_text(encoding="utf-8", errors="replace")
    text = strip_comments(raw_text)
    href_calls = scan_command_groups(text, lambda value: value == "href", 2)
    urls = command_values(text, {"url"}) + [required[0].strip() for _, _, required in href_calls]
    numbers = [match.group(0) for match in NUMBER_PATTERN.finditer(text)]
    directions = [match.group(0).lower() for match in DIRECTION_TERMS.finditer(text)]
    return {
        "citations": counter(citation_keys(text)),
        "labels": counter(command_values(text, {"label"})),
        "references": counter(command_values(text, {"ref", "eqref", "autoref", "cref", "Cref", "pageref"})),
        "urls": counter(urls),
        "graphics": counter(command_values(text, {"includegraphics"})),
        "inputs": counter(command_values(text, {"input", "include", "subfile"})),
        "bibliographies": counter(command_values(text, {"bibliography", "addbibresource"})),
        "numbers": counter(numbers),
        "number_sequence": numbers,
        "directional_terms": counter(directions),
        "math_environments": counter(extract_environments(text, MATH_ENVS, canonical_math)),
        "code_environments": counter(
            extract_environments(text, CODE_ENVS, lambda block: block.replace("\r\n", "\n"))
        ),
        "table_evidence_blocks": counter(extract_environments(text, TABLE_ENVS)),
        "inline_math": counter(extract_inline_math(text)),
        "custom_macro_calls": counter(extract_macro_calls(text, macro_names)),
    }


def resolve_graphic(root: Path, tex_path: Path, raw_path: str) -> str:
    if "\\" in raw_path or "#" in raw_path:
        return "unresolved-macro-path"
    candidates: list[Path] = []
    for base in (tex_path.parent, root):
        for extension in GRAPHICS_EXTENSIONS:
            candidate = (base / f"{raw_path}{extension}").resolve()
            if candidate.is_file() and root in candidate.parents:
                candidates.append(candidate)
    unique = sorted(set(candidates))
    if not unique:
        return "missing"
    if len(unique) > 1:
        return "ambiguous:" + ",".join(str(path.relative_to(root)) for path in unique)
    path = unique[0]
    return f"{path.relative_to(root)}:{sha256_bytes(path.read_bytes())}"


def snapshot(root: Path) -> dict[str, object]:
    root = root.resolve()
    source_files = sorted(
        path for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in SOURCE_EXTENSIONS
    )
    tex_files = [path for path in source_files if path.suffix.lower() == ".tex"]
    bib_files = [path for path in source_files if path.suffix.lower() == ".bib"]
    support_files = [path for path in source_files if path.suffix.lower() not in {".tex", ".bib"}]

    combined = "\n".join(
        strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        for path in source_files
        if path.suffix.lower() in {".tex", ".sty", ".cls"}
    )
    definitions = extract_macro_definitions(combined)
    tex_data = {str(path.relative_to(root)): tex_snapshot(path, set(definitions)) for path in tex_files}

    graphics_assets: dict[str, str] = {}
    for path in tex_files:
        rel = str(path.relative_to(root))
        for raw_path in tex_data[rel]["graphics"]:
            graphics_assets[f"{rel}::{raw_path}"] = resolve_graphic(root, path, raw_path)

    return {
        "guard_version": GUARD_VERSION,
        "file_set": [str(path.relative_to(root)) for path in source_files],
        "tex": tex_data,
        "bib_sha256": {str(path.relative_to(root)): sha256_bytes(path.read_bytes()) for path in bib_files},
        "support_sha256": {str(path.relative_to(root)): sha256_bytes(path.read_bytes()) for path in support_files},
        "graphics_assets": graphics_assets,
        "custom_macro_definitions": definitions,
    }


def append_diff(
    findings: list[dict[str, object]],
    before: dict[str, object],
    after: dict[str, object],
    field_prefix: str,
    severity: str,
    file: str | None = None,
) -> None:
    for key in sorted(set(before) | set(after)):
        if before.get(key) != after.get(key):
            item: dict[str, object] = {
                "field": f"{field_prefix}.{key}" if field_prefix else key,
                "severity": severity,
                "before": before.get(key),
                "after": after.get(key),
            }
            if file:
                item["file"] = file
            findings.append(item)


def compare(baseline: dict[str, object], current: dict[str, object]) -> dict[str, object]:
    findings: list[dict[str, object]] = []
    if baseline.get("guard_version") != GUARD_VERSION:
        findings.append({
            "field": "guard_version", "severity": "blocking",
            "before": baseline.get("guard_version"), "after": GUARD_VERSION,
        })
    if baseline.get("file_set") != current.get("file_set"):
        findings.append({
            "field": "file_set", "severity": "blocking",
            "before": baseline.get("file_set"), "after": current.get("file_set"),
        })

    for field in ("bib_sha256", "support_sha256", "graphics_assets", "custom_macro_definitions"):
        append_diff(
            findings,
            baseline.get(field, {}),
            current.get(field, {}),
            field,
            "blocking",
        )

    before_tex = baseline.get("tex", {})
    after_tex = current.get("tex", {})
    review_fields = {"numbers", "number_sequence", "directional_terms"}
    for filename in sorted(set(before_tex) & set(after_tex)):
        before_file = before_tex[filename]
        after_file = after_tex[filename]
        for key in sorted(set(before_file) | set(after_file)):
            if before_file.get(key) == after_file.get(key):
                continue
            findings.append({
                "field": key,
                "file": filename,
                "severity": "review_required" if key in review_fields else "blocking",
                "before": before_file.get(key),
                "after": after_file.get(key),
            })

    blocking_count = sum(item["severity"] == "blocking" for item in findings)
    review_count = sum(item["severity"] == "review_required" for item in findings)
    return {
        "ok": not findings,
        "blocking_count": blocking_count,
        "review_required_count": review_count,
        "finding_count": len(findings),
        "findings": findings,
        "note": "No detected drift is not proof of semantic equivalence; review-required findings need independent semantic adjudication.",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    snap = sub.add_parser("snapshot", help="Record protected LaTeX invariants")
    snap.add_argument("project", type=Path)
    snap.add_argument("--output", required=True, type=Path)
    comp = sub.add_parser("compare", help="Compare a project with a snapshot")
    comp.add_argument("project", type=Path)
    comp.add_argument("--baseline", required=True, type=Path)
    comp.add_argument("--report", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.project.is_dir():
        print(f"Project directory not found: {args.project}", file=sys.stderr)
        return 2
    if args.command == "snapshot":
        data = snapshot(args.project)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote baseline guard v{GUARD_VERSION}: {args.output}")
        return 0
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    report = compare(baseline, snapshot(args.project))
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
