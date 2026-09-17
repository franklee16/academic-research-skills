"""Shared status and completeness helpers for visible-geometry extraction.

The helpers deliberately audit declared visual slots only.  They never accept
an expected data count, source workbook row count, or target statistic.
"""
from __future__ import annotations

from collections import Counter
from typing import Any, Iterable, Sequence


CONTRACT_VERSION = 1

REASON_CODES = {
    "visible_geometry_supported",
    "visible_label_verified",
    "no_supported_geometry",
    "ambiguous_geometry",
    "calibration_geometry_conflict",
    "occluded",
    "fused",
    "below_resolution",
    "not_drawn",
    "unsupported_route",
    "detector_residual",
    "source_contract_mismatch",
}


def validate_reason_code(reason_code: str) -> str:
    if reason_code not in REASON_CODES:
        raise ValueError(
            f"reason_code must be one of {sorted(REASON_CODES)}; got {reason_code!r}"
        )
    return reason_code


def build_coverage_ledger(
    records: Iterable[dict[str, Any]],
    *,
    slot_fields: Sequence[str],
    status_field: str = "status",
    authorized_field: str = "numeric_output_authorized",
) -> dict[str, Any]:
    """Summarize caller-declared visual slots without inventing missing rows."""

    rows = list(records)
    seen: set[tuple[Any, ...]] = set()
    status_counts: Counter[str] = Counter()
    reason_counts: Counter[str] = Counter()
    authorized_count = 0
    slots = []
    for row in rows:
        key = tuple(row.get(field) for field in slot_fields)
        if None in key:
            raise ValueError(f"coverage slot is missing one of {list(slot_fields)}: {key}")
        if key in seen:
            raise ValueError(f"duplicate coverage slot: {key}")
        seen.add(key)
        status = str(row.get(status_field, ""))
        if status not in {"extracted", "not_extracted", "low_confidence"}:
            raise ValueError(f"unsupported coverage status {status!r} for slot {key}")
        reason_code = validate_reason_code(str(row.get("reason_code", "")))
        authorized = bool(row.get(authorized_field, status == "extracted"))
        if authorized and status != "extracted":
            raise ValueError(f"non-extracted slot cannot authorize numeric output: {key}")
        status_counts[status] += 1
        reason_counts[reason_code] += 1
        authorized_count += int(authorized)
        slots.append(
            {
                "slot": {field: row[field] for field in slot_fields},
                "status": status,
                "reason_code": reason_code,
                "numeric_output_authorized": authorized,
            }
        )

    declared = len(rows)
    return {
        "schema_version": CONTRACT_VERSION,
        "scope": "declared_visual_slots_only",
        "expected_data_count_used": False,
        "slot_fields": list(slot_fields),
        "declared_slot_count": declared,
        "authorized_slot_count": authorized_count,
        "coverage_fraction": authorized_count / declared if declared else 0.0,
        "status_counts": dict(sorted(status_counts.items())),
        "reason_code_counts": dict(sorted(reason_counts.items())),
        "slots": slots,
    }
