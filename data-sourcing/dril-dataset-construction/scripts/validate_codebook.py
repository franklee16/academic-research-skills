#!/usr/bin/env python3
"""
Validate a DRIL codebook (YAML) for structural correctness.
Run before implementation to catch instrument errors early.

Usage:
    python validate_codebook.py path/to/codebook.yaml
"""
import sys
import yaml


REQUIRED_VAR_FIELDS = {"id", "name", "question", "value_type", "coding_rules", "field_kind"}
VALID_FIELD_KINDS = {
    "coded_scalar",
    "coded_multivalue",
    "narrative_summary",
    "extractive_note",
    "entity_list",
    "tabular_extract",
}
VALID_UNCERTAINTY_STATUSES = {
    "answered",
    "not_found_after_search",
    "not_applicable",
    "proxy_used",
    "inferred",
    "conflict_unresolved",
}
VALID_GAP_REASONS = {
    "not_found_after_search",
    "not_applicable",
    "unclear_definition",
    "conflict_unresolved",
    "out_of_scope",
}


def validate_codebook(path: str) -> list[str]:
    errors = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return [f"Failed to parse YAML: {e}"]

    if not isinstance(data, dict):
        return ["Codebook root must be a YAML mapping."]

    # Metadata
    if "metadata" not in data:
        errors.append("Missing 'metadata' section.")
    else:
        meta = data["metadata"]
        for field in ("title", "version"):
            if field not in meta:
                errors.append(f"metadata.{field} is required.")

    # Unit space
    if "unit_space" not in data:
        errors.append("Missing 'unit_space' section.")
    else:
        us = data["unit_space"]
        if "dimensions" not in us or not us["dimensions"]:
            errors.append("unit_space.dimensions must be a non-empty list.")
        else:
            for i, dim in enumerate(us["dimensions"]):
                if "name" not in dim:
                    errors.append(f"unit_space.dimensions[{i}] missing 'name'.")

    # Variables
    if "variables" not in data or not data["variables"]:
        errors.append("Missing or empty 'variables' list.")
    else:
        seen_ids = set()
        seen_names = set()
        for i, var in enumerate(data["variables"]):
            prefix = f"variables[{i}]"
            missing = REQUIRED_VAR_FIELDS - set(var.keys())
            if missing:
                errors.append(f"{prefix} missing required fields: {missing}")
                continue

            if var["id"] in seen_ids:
                errors.append(f"{prefix} duplicate id: {var['id']}")
            seen_ids.add(var["id"])

            if var["name"] in seen_names:
                errors.append(f"{prefix} duplicate name: {var['name']}")
            seen_names.add(var["name"])

            if var["field_kind"] not in VALID_FIELD_KINDS:
                errors.append(
                    f"{prefix} invalid field_kind '{var['field_kind']}'. "
                    f"Valid: {VALID_FIELD_KINDS}"
                )

            vt = var.get("value_type", {})
            if "kind" not in vt:
                errors.append(f"{prefix} value_type missing 'kind'.")
            elif vt["kind"] == "categorical":
                if "values" not in vt or not vt["values"]:
                    errors.append(f"{prefix} categorical value_type requires 'values' list.")
            elif vt["kind"] == "continuous":
                if "units" not in vt:
                    errors.append(f"{prefix} continuous value_type requires 'units'.")

    # Cross-cutting policies
    if "cross_cutting_policies" not in data:
        errors.append("Missing 'cross_cutting_policies' section (can be empty but should be present).")

    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python validate_codebook.py <codebook.yaml>")
        return 1

    path = sys.argv[1]
    errors = validate_codebook(path)

    if not errors:
        print(f"OK: {path} is valid.")
        return 0
    else:
        print(f"FAILED: {path} has {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
