#!/usr/bin/env python3
"""Profile CSV files and XLSX workbooks for data-analysis-router."""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
import zipfile
from collections import Counter, defaultdict
from datetime import datetime
from xml.etree import ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


MAX_ROWS_DEFAULT = 5000
SAMPLE_VALUES = 5


def is_blank(value: Any) -> bool:
    return value is None or str(value).strip() == ""


def normalize(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def parse_float(value: Any) -> Optional[float]:
    text = normalize(value).replace(",", "")
    if text.endswith("%"):
        text = text[:-1]
    if text == "":
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return number


def looks_like_date(value: Any) -> bool:
    text = normalize(value)
    if not text:
        return False
    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%Y%m%d",
    ]
    for fmt in formats:
        try:
            datetime.strptime(text[:19], fmt)
            return True
        except ValueError:
            pass
    return False


def infer_column_type(name: str, values: Sequence[Any], row_count: int) -> str:
    lowered = name.lower()
    present = [v for v in values if not is_blank(v)]
    if not present:
        return "empty"

    numeric_count = sum(parse_float(v) is not None for v in present)
    date_count = sum(looks_like_date(v) for v in present)
    unique_count = len({normalize(v) for v in present})
    avg_len = statistics.mean([len(normalize(v)) for v in present])

    if "id" in lowered or lowered.endswith("_no") or "编号" in name or "单号" in name:
        return "id"
    if date_count / len(present) >= 0.7 or any(token in lowered for token in ["date", "time", "created", "updated"]):
        return "time"
    if numeric_count / len(present) >= 0.8:
        return "numeric"
    if avg_len >= 30 or any(token in lowered for token in ["comment", "content", "text", "review", "feedback"]):
        return "text"
    if unique_count <= max(20, row_count * 0.2):
        return "category"
    return "mixed"


def profile_rows(name: str, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not rows:
        return {"name": name, "rows": 0, "columns": 0, "fields": []}

    fieldnames = list(rows[0].keys())
    row_count = len(rows)
    profile: Dict[str, Any] = {
        "name": name,
        "rows_profiled": row_count,
        "columns": len(fieldnames),
        "fields": [],
    }

    for field in fieldnames:
        values = [row.get(field) for row in rows]
        present = [v for v in values if not is_blank(v)]
        normalized_present = [normalize(v) for v in present]
        unique_values = set(normalized_present)
        numeric_values = [parse_float(v) for v in present]
        numeric_values = [v for v in numeric_values if v is not None]
        samples = []
        for value in normalized_present:
            if value not in samples:
                samples.append(value)
            if len(samples) >= SAMPLE_VALUES:
                break

        item: Dict[str, Any] = {
            "name": field,
            "type": infer_column_type(field, values, row_count),
            "missing": row_count - len(present),
            "missing_rate": round((row_count - len(present)) / row_count, 4),
            "unique": len(unique_values),
            "samples": samples,
        }

        if numeric_values:
            item["numeric_summary"] = {
                "min": min(numeric_values),
                "max": max(numeric_values),
                "mean": round(statistics.mean(numeric_values), 4),
            }

        profile["fields"].append(item)

    profile["likely_table_role"] = infer_table_role(name, fieldnames)
    return profile


def infer_table_role(table_name: str, fields: Sequence[str]) -> str:
    text = " ".join([table_name] + list(fields)).lower()
    rules = [
        ("orders", ["order", "订单", "payment", "gmv", "refund"]),
        ("products", ["sku", "product", "商品", "category", "price", "stock"]),
        ("users", ["user", "customer", "member", "用户", "会员"]),
        ("traffic", ["traffic", "visit", "pv", "uv", "click", "曝光", "流量"]),
        ("advertising_performance", ["campaign", "creative", "spend", "impression", "ctr", "cpa", "roas"]),
        ("content_performance", ["post", "video", "title", "likes", "shares", "comments", "完播"]),
        ("store_operation", ["store", "branch", "shop", "门店", "客流", "排班"]),
        ("finance", ["revenue", "cost", "profit", "expense", "cash", "收入", "成本", "利润"]),
        ("feedback", ["review", "rating", "complaint", "feedback", "comment", "评论", "投诉"]),
    ]
    for role, tokens in rules:
        if any(token in text for token in tokens):
            return role
    return "unknown"


def read_csv(path: Path, max_rows: int) -> List[Dict[str, Any]]:
    encodings = ["utf-8-sig", "utf-8", "gb18030"]
    last_error: Optional[Exception] = None
    for encoding in encodings:
        try:
            with path.open("r", encoding=encoding, newline="") as handle:
                reader = csv.DictReader(handle)
                return [row for _, row in zip(range(max_rows), reader)]
        except UnicodeDecodeError as exc:
            last_error = exc
    raise RuntimeError(f"Could not decode CSV {path}: {last_error}")


def read_xlsx(path: Path, max_rows: int) -> List[Tuple[str, List[Dict[str, Any]]]]:
    ns = {
        "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
        "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        "pkgrel": "http://schemas.openxmlformats.org/package/2006/relationships",
    }

    with zipfile.ZipFile(path) as archive:
        shared_strings = read_shared_strings(archive, ns)
        workbook_xml = ET.fromstring(archive.read("xl/workbook.xml"))
        rels_xml = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        rel_targets = {
            rel.attrib["Id"]: rel.attrib["Target"]
            for rel in rels_xml.findall("pkgrel:Relationship", ns)
        }

        result = []
        for sheet in workbook_xml.findall("main:sheets/main:sheet", ns):
            sheet_name = sheet.attrib.get("name", "Sheet")
            rel_id = sheet.attrib.get(f"{{{ns['rel']}}}id")
            if not rel_id or rel_id not in rel_targets:
                continue
            target = rel_targets[rel_id]
            sheet_path = "xl/" + target.lstrip("/")
            if sheet_path not in archive.namelist():
                sheet_path = "xl/worksheets/" + Path(target).name
            rows = read_xlsx_sheet(archive, sheet_path, shared_strings, ns, max_rows)
            result.append((sheet_name, rows))
        return result


def read_shared_strings(archive: zipfile.ZipFile, ns: Dict[str, str]) -> List[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    strings = []
    for item in root.findall("main:si", ns):
        parts = [node.text or "" for node in item.findall(".//main:t", ns)]
        strings.append("".join(parts))
    return strings


def read_xlsx_sheet(
    archive: zipfile.ZipFile,
    sheet_path: str,
    shared_strings: Sequence[str],
    ns: Dict[str, str],
    max_rows: int,
) -> List[Dict[str, Any]]:
    root = ET.fromstring(archive.read(sheet_path))
    raw_rows = []
    for row in root.findall("main:sheetData/main:row", ns):
        values: Dict[int, Any] = {}
        for cell in row.findall("main:c", ns):
            ref = cell.attrib.get("r", "")
            index = column_index(ref)
            values[index] = read_xlsx_cell(cell, shared_strings, ns)
        raw_rows.append(values)

    if not raw_rows:
        return []

    header_row = raw_rows[0]
    max_col = max(header_row.keys()) if header_row else 0
    fields = [normalize(header_row.get(idx)) or f"column_{idx}" for idx in range(1, max_col + 1)]
    rows = []
    for raw_row in raw_rows[1 : max_rows + 1]:
        rows.append({fields[idx - 1]: raw_row.get(idx) for idx in range(1, len(fields) + 1)})
    return rows


def column_index(cell_ref: str) -> int:
    letters = "".join(ch for ch in cell_ref if ch.isalpha()).upper()
    if not letters:
        return 1
    index = 0
    for char in letters:
        index = index * 26 + (ord(char) - ord("A") + 1)
    return index


def read_xlsx_cell(cell: ET.Element, shared_strings: Sequence[str], ns: Dict[str, str]) -> Any:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        parts = [node.text or "" for node in cell.findall(".//main:t", ns)]
        return "".join(parts)
    value_node = cell.find("main:v", ns)
    if value_node is None:
        return ""
    raw_value = value_node.text or ""
    if cell_type == "s":
        try:
            return shared_strings[int(raw_value)]
        except (ValueError, IndexError):
            return raw_value
    return raw_value
    result = []
    for sheet in workbook.worksheets:
        rows_iter = sheet.iter_rows(values_only=True)
        try:
            header = next(rows_iter)
        except StopIteration:
            result.append((sheet.title, []))
            continue
        fields = [normalize(value) or f"column_{idx + 1}" for idx, value in enumerate(header)]
        rows = []
        for idx, row in enumerate(rows_iter):
            if idx >= max_rows:
                break
            rows.append({fields[col_idx]: value for col_idx, value in enumerate(row[: len(fields)])})
        result.append((sheet.title, rows))
    return result


def find_candidate_relationships(tables: Sequence[Dict[str, Any]]) -> List[Dict[str, str]]:
    by_field: Dict[str, List[str]] = defaultdict(list)
    for table in tables:
        for field in table.get("fields", []):
            field_name = field["name"]
            lowered = field_name.lower()
            if field["type"] == "id" or lowered.endswith("_id") or lowered in {"id", "sku", "sku_id"}:
                by_field[lowered].append(f"{table['name']}.{field_name}")

    relationships = []
    for key, locations in by_field.items():
        if len(locations) >= 2:
            relationships.append({"candidate_key": key, "tables": ", ".join(locations)})
    return relationships


def profile_file(path: Path, max_rows: int) -> Dict[str, Any]:
    suffix = path.suffix.lower()
    tables = []
    if suffix == ".csv":
        rows = read_csv(path, max_rows)
        tables.append(profile_rows(path.name, rows))
    elif suffix == ".xlsx":
        for sheet_name, rows in read_xlsx(path, max_rows):
            tables.append(profile_rows(f"{path.name}::{sheet_name}", rows))
    else:
        raise RuntimeError(f"Unsupported file type: {path}")

    return {
        "file": str(path),
        "tables": tables,
    }


def infer_domains(all_tables: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    domain_tokens = {
        "ecommerce": ["order", "sku", "gmv", "payment", "refund", "product", "cart", "复购", "退款"],
        "content-operation": ["post", "video", "title", "exposure", "likes", "saves", "comments", "share", "完播"],
        "advertising": ["campaign", "creative", "spend", "impression", "ctr", "cvr", "cpa", "cpm", "roas"],
        "store-operation": ["store", "branch", "shop", "traffic", "shift", "member", "门店", "客流"],
        "finance": ["revenue", "cost", "profit", "expense", "cash", "budget", "收入", "成本", "利润"],
        "user-feedback": ["review", "rating", "complaint", "feedback", "comment", "sentiment", "评论", "投诉"],
    }
    text_parts = []
    for table in all_tables:
        text_parts.append(table.get("name", ""))
        text_parts.extend(field.get("name", "") for field in table.get("fields", []))
        for field in table.get("fields", []):
            text_parts.extend(field.get("samples", [])[:2])
    text = " ".join(text_parts).lower()

    scored = []
    for domain, tokens in domain_tokens.items():
        hits = [token for token in tokens if token.lower() in text]
        if hits:
            scored.append({"domain": domain, "score": len(hits), "matched_signals": hits})
    return sorted(scored, key=lambda item: item["score"], reverse=True)


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(description="Profile CSV/XLSX datasets for routing analysis.")
    parser.add_argument("files", nargs="+", help="CSV or XLSX files to profile")
    parser.add_argument("--max-rows", type=int, default=MAX_ROWS_DEFAULT, help="Rows to read per file/sheet")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    args = parser.parse_args(argv)

    results = []
    all_tables = []
    for raw_path in args.files:
        path = Path(raw_path).expanduser()
        if not path.exists():
            raise RuntimeError(f"File not found: {path}")
        result = profile_file(path, args.max_rows)
        results.append(result)
        all_tables.extend(result["tables"])

    output = {
        "files": results,
        "candidate_relationships": find_candidate_relationships(all_tables),
        "likely_domains": infer_domains(all_tables),
    }

    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print_markdown(output)
    return 0


def print_markdown(output: Dict[str, Any]) -> None:
    print("# Dataset Profile")
    for file_result in output["files"]:
        print(f"\n## File: {file_result['file']}")
        for table in file_result["tables"]:
            print(f"\n### Table: {table['name']}")
            print(f"- Rows profiled: {table.get('rows_profiled', 0)}")
            print(f"- Columns: {table.get('columns', 0)}")
            print(f"- Likely table role: {table.get('likely_table_role', 'unknown')}")
            print("\n| Field | Type | Missing % | Unique | Samples |")
            print("| --- | --- | ---: | ---: | --- |")
            for field in table.get("fields", []):
                samples = ", ".join(field.get("samples", []))
                print(
                    f"| {field['name']} | {field['type']} | "
                    f"{field['missing_rate'] * 100:.1f}% | {field['unique']} | {samples} |"
                )

    if output["candidate_relationships"]:
        print("\n## Candidate Relationships")
        for relation in output["candidate_relationships"]:
            print(f"- `{relation['candidate_key']}`: {relation['tables']}")

    if output["likely_domains"]:
        print("\n## Likely Domains")
        for item in output["likely_domains"]:
            signals = ", ".join(item["matched_signals"])
            print(f"- {item['domain']} (score {item['score']}): {signals}")
    else:
        print("\n## Likely Domains")
        print("- general-analysis: no strong domain signals found")


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
