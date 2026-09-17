#!/usr/bin/env python3
"""Validate, migrate, and deterministically merge Research Defense Radar state."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
import unicodedata
from datetime import date
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


SCHEMA_VERSION = "1.1"
CATEGORIES = {"A", "B", "C", "D", "E"}
EVIDENCE_LEVELS = {"M", "A", "F"}
EVIDENCE_RANK = {"M": 0, "A": 1, "F": 2}
CONFIDENCE_LEVELS = {"low", "medium", "high"}
CHANGE_KINDS = {
    "identity_update",
    "metadata_update",
    "evidence_upgrade",
    "substantive_revision",
    "novelty_impact_change",
}
MATERIAL_CHANGE_KINDS = {"substantive_revision", "novelty_impact_change"}
COVERAGE_STATUSES = {"completed", "partial", "inaccessible", "not_applicable"}
RUN_STATUSES = {"completed", "partial", "failed"}
OVERLAP_FACTORS = {0, 0.25, 0.5, 0.75, 1.0}
TRACKING_QUERY_PREFIXES = ("utm_",)
TRACKING_QUERY_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid"}
LIST_FIELDS = {"authors", "source_urls", "identity_keys", "secondary_tags"}
SUBSTANTIVE_FIELDS = {
    "claim_summary",
    "question",
    "mechanism",
    "data_setting",
    "unit",
    "measurement",
    "identification",
    "method_model",
    "outcome",
}
NOVELTY_IMPACT_FIELDS = {
    "category",
    "overlap_score",
    "overlap_dimensions",
    "threat_help_level",
    "affected_fingerprint_fields",
    "recommended_action",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_doi(value: Optional[str]) -> str:
    doi = (value or "").strip().lower()
    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi)
    return doi.removeprefix("doi:").strip().rstrip(".,;)")


def canonical_url(value: Optional[str]) -> str:
    raw = (value or "").strip()
    if not raw:
        return ""
    parts = urlsplit(raw)
    query = [
        (key, item)
        for key, item in parse_qsl(parts.query, keep_blank_values=True)
        if key.lower() not in TRACKING_QUERY_KEYS
        and not key.lower().startswith(TRACKING_QUERY_PREFIXES)
    ]
    path = parts.path.rstrip("/") or "/"
    return urlunsplit(
        (parts.scheme.lower(), parts.netloc.lower(), path, urlencode(sorted(query)), "")
    )


def normalize_text(value: Optional[str]) -> str:
    text = unicodedata.normalize("NFKD", value or "").lower()
    return " ".join(re.findall(r"[\w]+", text, flags=re.UNICODE))


def normalize_repository_id(value: Optional[str]) -> str:
    return normalize_text(value)


def first_author(observation: dict) -> str:
    authors = observation.get("authors", [])
    if isinstance(authors, str):
        authors = [authors]
    return normalize_text(authors[0]) if authors else ""


def identity_keys(observation: dict) -> set[str]:
    """Return durable strong and weak identity aliases for one paper lineage."""
    keys = {
        str(item).strip()
        for item in observation.get("identity_keys", []) or []
        if str(item).strip()
    }

    def add_identifiers(item: dict) -> None:
        doi = normalize_doi(item.get("doi"))
        if doi:
            keys.add(f"doi:{doi}")
        repository_id = normalize_repository_id(item.get("repository_id"))
        if repository_id:
            keys.add(f"repository:{repository_id}")
        for field in ("canonical_url", "url"):
            url = canonical_url(item.get(field))
            if url:
                keys.add(f"url:{url}")

    add_identifiers(observation)
    for url_value in observation.get("source_urls", []) or []:
        url = canonical_url(str(url_value))
        if url:
            keys.add(f"url:{url}")
    for version in observation.get("versions", []) or []:
        if isinstance(version, dict):
            add_identifiers(version)

    title = normalize_text(observation.get("title"))
    author = first_author(observation)
    if title and author:
        keys.add(f"title-author:{title}|{author}")
    return keys


def key_rank(key: str) -> tuple[int, str]:
    prefixes = ("doi:", "repository:", "url:", "title-author:")
    for index, prefix in enumerate(prefixes):
        if key.startswith(prefix):
            return index, key
    return len(prefixes), key


def paper_key(observation: dict) -> str:
    keys = identity_keys(observation)
    if not keys:
        raise ValueError(
            "each observation needs a DOI, repository_id, canonical/source URL, "
            "or title plus author"
        )
    return min(keys, key=key_rank)


def stable_id(key: str) -> str:
    return "paper-" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def validate_dateish(value: object, field: str) -> None:
    text = str(value or "").strip()
    if not re.match(r"^\d{4}-\d{2}-\d{2}(?:$|T)", text):
        raise ValueError(f"{field} must start with an ISO date (YYYY-MM-DD)")
    try:
        date.fromisoformat(text[:10])
    except ValueError as exc:
        raise ValueError(f"{field} has an invalid ISO date") from exc


def validate_observation(observation: dict) -> None:
    if not isinstance(observation, dict):
        raise ValueError("each observation must be a JSON object")
    if not str(observation.get("title", "")).strip():
        raise ValueError("each observation needs a title")
    category = observation.get("category")
    if category not in CATEGORIES:
        raise ValueError(f"invalid or missing category: {category}")
    evidence = observation.get("evidence_level")
    if evidence not in EVIDENCE_LEVELS:
        raise ValueError(f"invalid or missing evidence_level: {evidence}")
    confidence = observation.get("confidence")
    if confidence not in CONFIDENCE_LEVELS:
        raise ValueError(f"invalid or missing confidence: {confidence}")
    validate_dateish(observation.get("verified_at"), "verified_at")
    for field in ("earliest_public_date", "current_version_date"):
        if observation.get(field):
            validate_dateish(observation[field], field)
    score = observation.get("overlap_score")
    if score is not None and (
        isinstance(score, bool)
        or not isinstance(score, (int, float))
        or not 0 <= score <= 100
    ):
        raise ValueError("overlap_score must be null or a number from 0 to 100")
    if evidence == "M" and score is not None:
        raise ValueError("metadata-only evidence cannot support a numeric overlap_score")
    dimensions = observation.get("overlap_dimensions")
    if dimensions is not None:
        if not isinstance(dimensions, dict):
            raise ValueError("overlap_dimensions must be an object")
        for dimension, factor in dimensions.items():
            if factor is not None and factor not in OVERLAP_FACTORS:
                raise ValueError(
                    f"invalid overlap factor for {dimension}: use 0, 0.25, 0.5, 0.75, 1, or null"
                )
    change_kind = observation.get("change_kind")
    if change_kind is not None and change_kind not in CHANGE_KINDS:
        raise ValueError(f"invalid change_kind: {change_kind}")
    paper_key(observation)


def apply_priority_cutoff(observation: dict, project: dict) -> dict:
    """Annotate whether a paper predates the project's first public working paper."""
    result = dict(observation)
    cutoff = project.get("public_disclosure_date")
    paper_date = result.get("earliest_public_date")
    if cutoff:
        validate_dateish(cutoff, "project.public_disclosure_date")
    if not cutoff or not paper_date:
        result["chronology_relation"] = "unknown"
        result["priority_effect"] = "uncertain"
        return result
    validate_dateish(paper_date, "earliest_public_date")
    cutoff_date, candidate_date = str(cutoff)[:10], str(paper_date)[:10]
    if candidate_date < cutoff_date:
        result["chronology_relation"] = "pre_disclosure"
        result.setdefault("priority_effect", "assess_as_prior_work")
    elif candidate_date > cutoff_date:
        result["chronology_relation"] = "post_disclosure"
        result["priority_effect"] = "no_preemption_post_disclosure"
    else:
        result["chronology_relation"] = "same_day"
        result["priority_effect"] = "chronology_uncertain_same_day"
    return result


def validate_coverage(coverage: list[dict]) -> None:
    if not isinstance(coverage, list):
        raise ValueError("coverage input must be a JSON array")
    for index, item in enumerate(coverage):
        if not isinstance(item, dict):
            raise ValueError(f"coverage item {index} must be an object")
        for field in ("source", "query_family", "checked_at", "status"):
            if not str(item.get(field, "")).strip():
                raise ValueError(f"coverage item {index} needs {field}")
        validate_dateish(item["checked_at"], f"coverage item {index} checked_at")
        if item["status"] not in COVERAGE_STATUSES:
            raise ValueError(f"invalid coverage status: {item['status']}")
        if "required" in item and not isinstance(item["required"], bool):
            raise ValueError(f"coverage item {index} required must be true or false")


def coverage_is_complete(coverage: list[dict]) -> bool:
    required = [item for item in coverage if item.get("required", True)]
    return bool(required) and all(
        item.get("status") in {"completed", "not_applicable"} for item in required
    ) and any(item.get("status") == "completed" for item in required)


def unique_strings(*collections) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    for collection in collections:
        if not collection:
            continue
        if isinstance(collection, str):
            collection = [collection]
        for value in collection:
            text = str(value).strip()
            if text and text not in seen:
                seen.add(text)
                values.append(text)
    return values


def unique_objects(*collections) -> list[dict]:
    values: list[dict] = []
    seen: set[str] = set()
    for collection in collections:
        for value in collection or []:
            if not isinstance(value, dict):
                continue
            encoded = json.dumps(value, sort_keys=True, ensure_ascii=False)
            if encoded not in seen:
                seen.add(encoded)
                values.append(value)
    return values


def has_identifier_conflict(left: dict, right: dict) -> bool:
    left_doi, right_doi = normalize_doi(left.get("doi")), normalize_doi(right.get("doi"))
    if left_doi and right_doi and left_doi != right_doi:
        return True
    left_repo = normalize_repository_id(left.get("repository_id"))
    right_repo = normalize_repository_id(right.get("repository_id"))
    return bool(left_repo and right_repo and left_repo != right_repo)


def records_match(left: dict, right: dict) -> bool:
    if has_identifier_conflict(left, right):
        return False
    intersection = identity_keys(left) & identity_keys(right)
    if any(not key.startswith("title-author:") for key in intersection):
        return True
    return bool(intersection)


def combine_existing_records(left: dict, right: dict) -> dict:
    """Coalesce records already present in state without inventing a new revision event."""
    candidates = sorted(
        (dict(left), dict(right)),
        key=lambda item: (item.get("first_seen") or "9999-99-99", item.get("id") or ""),
    )
    record, other = candidates
    for field, value in other.items():
        if field in LIST_FIELDS or field in {"versions", "change_history", "id"}:
            continue
        if record.get(field) in (None, "", [], {}):
            record[field] = value
    for field in LIST_FIELDS:
        record[field] = unique_strings(record.get(field), other.get(field))
    record["versions"] = unique_objects(record.get("versions"), other.get("versions"))
    record["change_history"] = unique_objects(
        record.get("change_history"), other.get("change_history")
    )
    dates = [item for item in (left.get("first_seen"), right.get("first_seen")) if item]
    if dates:
        record["first_seen"] = min(dates)
    dates = [item for item in (left.get("last_seen"), right.get("last_seen")) if item]
    if dates:
        record["last_seen"] = max(dates)
    dates = [
        item
        for item in (left.get("last_material_change_at"), right.get("last_material_change_at"))
        if item
    ]
    if dates:
        record["last_material_change_at"] = max(dates)
    record["identity_keys"] = sorted(identity_keys(record) | identity_keys(other), key=key_rank)
    record["dedupe_key"] = min(record["identity_keys"], key=key_rank)
    record["id"] = record.get("id") or stable_id(record["dedupe_key"])
    return record


def coalesce_records(records: list[dict]) -> list[dict]:
    merged: list[dict] = []
    for source in records:
        record = dict(source)
        keys = identity_keys(record)
        if not keys:
            raise ValueError("an existing paper record has no usable identity")
        record["identity_keys"] = sorted(keys, key=key_rank)
        record["dedupe_key"] = min(keys, key=key_rank)
        record["id"] = record.get("id") or stable_id(record["dedupe_key"])
        matches = [index for index, item in enumerate(merged) if records_match(item, record)]
        if not matches:
            merged.append(record)
            continue
        primary = matches[0]
        merged[primary] = combine_existing_records(merged[primary], record)
        for index in reversed(matches[1:]):
            merged[primary] = combine_existing_records(merged[primary], merged[index])
            del merged[index]
    return merged


def infer_change_kind(existing: dict, changed_fields: set[str], explicit: Optional[str]) -> str:
    if explicit:
        return explicit
    if changed_fields & NOVELTY_IMPACT_FIELDS:
        return "novelty_impact_change"
    if changed_fields & SUBSTANTIVE_FIELDS:
        return "substantive_revision"
    old_evidence = existing.get("evidence_level")
    new_evidence = existing.get("_new_evidence_level")
    if old_evidence in EVIDENCE_RANK and new_evidence in EVIDENCE_RANK:
        if EVIDENCE_RANK[new_evidence] > EVIDENCE_RANK[old_evidence]:
            return "evidence_upgrade"
    identity_fields = {"doi", "repository_id", "canonical_url", "authors", "source_urls", "versions"}
    if changed_fields and changed_fields <= identity_fields:
        return "identity_update"
    return "metadata_update"


def merge_record(existing: Optional[dict], observation: dict, run_date: str, run_id: str) -> dict:
    validate_observation(observation)
    record = dict(existing or {})
    was_existing = existing is not None
    changed_fields: set[str] = set()

    for field, value in observation.items():
        if field in LIST_FIELDS or field in {"versions", "materially_changed", "change_kind"}:
            continue
        if field == "earliest_public_date" and record.get(field):
            value = min(str(record[field])[:10], str(value)[:10])
        elif field == "current_version_date" and record.get(field):
            value = max(str(record[field])[:10], str(value)[:10])
        if value not in (None, "", [], {}) and record.get(field) != value:
            changed_fields.add(field)
            record[field] = value

    for field in LIST_FIELDS:
        before = record.get(field, [])
        after = unique_strings(before, observation.get(field))
        if after != before:
            changed_fields.add(field)
        record[field] = after
    before_versions = record.get("versions", [])
    record["versions"] = unique_objects(before_versions, observation.get("versions"))
    if record["versions"] != before_versions:
        changed_fields.add("versions")

    record["doi"] = normalize_doi(record.get("doi")) or None
    record["canonical_url"] = canonical_url(record.get("canonical_url")) or None
    record["source_urls"] = unique_strings(
        record.get("source_urls"), observation.get("canonical_url")
    )
    record["identity_keys"] = sorted(
        identity_keys(record) | identity_keys(observation), key=key_rank
    )
    record["dedupe_key"] = min(record["identity_keys"], key=key_rank)
    record["id"] = record.get("id") or stable_id(record["dedupe_key"])
    record["first_seen"] = record.get("first_seen") or run_date
    record["last_seen"] = run_date

    if was_existing and changed_fields:
        inference_context = dict(existing)
        inference_context["_new_evidence_level"] = record.get("evidence_level")
        explicit = observation.get("change_kind")
        if observation.get("materially_changed") and not explicit:
            explicit = "substantive_revision"
        kind = infer_change_kind(inference_context, changed_fields, explicit)
        history = list(record.get("change_history", []))
        event = {
            "run_id": run_id,
            "run_date": run_date,
            "kind": kind,
            "material": kind in MATERIAL_CHANGE_KINDS,
            "fields": sorted(changed_fields),
        }
        history = [item for item in history if item.get("run_id") != run_id]
        history.append(event)
        record["change_history"] = history
        if event["material"]:
            record["last_material_change_at"] = run_date
    elif not was_existing:
        record.setdefault("change_history", [])
    return record


def normalize_legacy_coverage(coverage: list, run_date: str) -> list[dict]:
    normalized = []
    for item in coverage or []:
        if not isinstance(item, dict):
            continue
        entry = dict(item)
        entry.setdefault("query_family", "legacy")
        entry.setdefault("checked_at", run_date)
        entry.setdefault("required", True)
        normalized.append(entry)
    return normalized


def migrate_state(state: dict) -> dict:
    version = state.get("schema_version")
    if version == SCHEMA_VERSION:
        return dict(state)
    if version != "1.0":
        raise ValueError(f"unsupported state schema_version: {version}")
    migrated = dict(state)
    migrated["schema_version"] = SCHEMA_VERSION
    project = dict(migrated.get("project") or {})
    project.setdefault("fingerprint_revision", None)
    project.setdefault("fingerprint_sha256", None)
    project.setdefault("fingerprint_updated_at", None)
    project.setdefault("public_disclosure_date", None)
    project.setdefault("public_disclosure_url", None)
    project.setdefault("public_disclosure_provenance", "unknown")
    migrated["project"] = project
    runs = []
    for source in migrated.get("runs", []):
        item = dict(source)
        run_date = item.get("run_date") or migrated.get("last_scan_at")
        item["coverage"] = normalize_legacy_coverage(item.get("coverage", []), run_date)
        item["coverage_complete"] = coverage_is_complete(item["coverage"])
        item.setdefault("run_status", "completed" if item["coverage_complete"] else "partial")
        item.setdefault("literature_cutoff_at", run_date)
        item.setdefault("fingerprint_sha256", project.get("fingerprint_sha256"))
        runs.append(item)
    migrated["runs"] = runs
    attempted = migrated.pop("last_scan_at", None)
    migrated["last_attempted_scan_at"] = attempted
    successful_dates = [
        item.get("run_date")
        for item in runs
        if item.get("run_status") == "completed" and item.get("coverage_complete")
    ]
    migrated["last_successful_scan_at"] = max(successful_dates) if successful_dates else None
    migrated["papers"] = coalesce_records(migrated.get("papers", []))
    return migrated


def validate_state(state: dict) -> None:
    if state.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"state schema_version must be {SCHEMA_VERSION}")
    project = state.get("project")
    if not isinstance(project, dict) or not str(project.get("slug", "")).strip():
        raise ValueError("state.project must be an object with a non-empty slug")
    if project.get("public_disclosure_date"):
        validate_dateish(project["public_disclosure_date"], "project.public_disclosure_date")
    if not isinstance(state.get("papers"), list) or not isinstance(state.get("runs"), list):
        raise ValueError("state.papers and state.runs must be arrays")


def resolve_run_status(requested: str, complete: bool, coverage: list[dict]) -> str:
    if requested == "auto":
        if complete:
            return "completed"
        if coverage and all(item.get("status") == "inaccessible" for item in coverage):
            return "failed"
        return "partial"
    if requested == "completed" and not complete:
        raise ValueError("a run cannot be completed until required coverage is complete")
    return requested


def merge_state(
    state: dict,
    observations: list[dict],
    run_id: str,
    run_date: str,
    coverage: list[dict],
    run_status: str = "auto",
    literature_cutoff: Optional[str] = None,
    fingerprint_revision: Optional[str] = None,
    fingerprint_sha256: Optional[str] = None,
    public_disclosure_date: Optional[str] = None,
    public_disclosure_url: Optional[str] = None,
    public_disclosure_provenance: Optional[str] = None,
) -> dict:
    state = migrate_state(state)
    validate_state(state)
    validate_dateish(run_date, "run_date")
    cutoff = literature_cutoff or run_date
    validate_dateish(cutoff, "literature_cutoff")
    validate_coverage(coverage)
    complete = coverage_is_complete(coverage)
    status = resolve_run_status(run_status, complete, coverage)

    result = dict(state)
    project = dict(result["project"])
    if fingerprint_revision is not None:
        project["fingerprint_revision"] = fingerprint_revision
    if fingerprint_sha256 is not None:
        project["fingerprint_sha256"] = fingerprint_sha256
        project["fingerprint_updated_at"] = run_date
    if public_disclosure_date is not None:
        validate_dateish(public_disclosure_date, "public_disclosure_date")
        project["public_disclosure_date"] = public_disclosure_date
    if public_disclosure_url is not None:
        project["public_disclosure_url"] = canonical_url(public_disclosure_url) or None
    if public_disclosure_provenance is not None:
        if public_disclosure_provenance not in {"user_stated", "public_record", "unknown"}:
            raise ValueError("invalid public_disclosure_provenance")
        project["public_disclosure_provenance"] = public_disclosure_provenance
    result["project"] = project

    records = coalesce_records(state["papers"])
    for raw_observation in observations:
        matches = [index for index, item in enumerate(records) if records_match(item, raw_observation)]
        dated_observation = dict(raw_observation)
        known_dates = [
            item.get("earliest_public_date")
            for index, item in enumerate(records)
            if index in matches and item.get("earliest_public_date")
        ]
        if raw_observation.get("earliest_public_date"):
            known_dates.append(raw_observation["earliest_public_date"])
        if known_dates:
            dated_observation["earliest_public_date"] = min(str(item)[:10] for item in known_dates)
        observation = apply_priority_cutoff(dated_observation, project)
        if matches:
            primary = matches[0]
            for index in reversed(matches[1:]):
                records[primary] = combine_existing_records(records[primary], records[index])
                del records[index]
            records[primary] = merge_record(records[primary], observation, run_date, run_id)
        else:
            records.append(merge_record(None, observation, run_date, run_id))
        records = coalesce_records(records)

    result["papers"] = sorted(
        records, key=lambda item: (item.get("title", "").lower(), item["id"])
    )
    existing_runs = {item.get("run_id"): item for item in result["runs"]}
    existing_runs[run_id] = {
        "run_id": run_id,
        "run_date": run_date,
        "run_status": status,
        "literature_cutoff_at": cutoff,
        "fingerprint_sha256": project.get("fingerprint_sha256"),
        "observations_seen": len(observations),
        "coverage_complete": complete,
        "coverage": coverage,
    }
    result["runs"] = sorted(
        existing_runs.values(),
        key=lambda item: (item.get("run_date", ""), item.get("run_id", "")),
    )
    result["last_attempted_scan_at"] = run_date
    if status == "completed" and complete:
        result["last_successful_scan_at"] = run_date
    return result


def atomic_write(path: Path, value: dict, backup: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if backup and path.exists():
        shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
    handle, temp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=False)
            stream.write("\n")
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def self_test() -> None:
    state = {
        "schema_version": "1.0",
        "project": {"slug": "demo"},
        "last_scan_at": None,
        "papers": [],
        "runs": [],
    }
    coverage = [{
        "source": "demo-index",
        "query_family": "question",
        "checked_at": "2026-08-17",
        "status": "completed",
        "required": True,
    }]
    first = [{
        "title": "A New Result",
        "authors": ["Ada Example"],
        "canonical_url": "https://example.org/paper?utm_source=alert#abstract",
        "category": "B",
        "evidence_level": "M",
        "confidence": "low",
        "verified_at": "2026-08-17",
        "source_urls": ["https://example.org/paper"],
    }]
    state = merge_state(state, first, "run-1", "2026-08-17", coverage)
    second = [{
        "title": "A New Result",
        "authors": ["Ada Example"],
        "doi": "https://doi.org/10.1000/XYZ",
        "canonical_url": "https://publisher.example/article",
        "category": "B",
        "evidence_level": "F",
        "confidence": "high",
        "verified_at": "2026-08-24",
        "overlap_score": 72,
        "change_kind": "evidence_upgrade",
    }]
    state = merge_state(state, second, "run-2", "2026-08-24", coverage)
    assert state["schema_version"] == SCHEMA_VERSION
    assert len(state["papers"]) == 1
    assert state["papers"][0]["first_seen"] == "2026-08-17"
    assert state["papers"][0]["doi"] == "10.1000/xyz"
    assert state["papers"][0]["evidence_level"] == "F"
    assert state["papers"][0]["change_history"][0]["kind"] == "evidence_upgrade"
    assert state["last_successful_scan_at"] == "2026-08-24"
    partial = merge_state(state, [], "run-3", "2026-08-31", [])
    assert partial["last_attempted_scan_at"] == "2026-08-31"
    assert partial["last_successful_scan_at"] == "2026-08-24"
    print("radar state self-test: ok")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, help="Existing radar-state.json")
    parser.add_argument("--observations", type=Path, help="JSON array or {observations: [...]} file")
    parser.add_argument("--coverage", type=Path, help="JSON array of source/query coverage entries")
    parser.add_argument("--run-id", help="Stable idempotent run identifier")
    parser.add_argument("--run-date", default=date.today().isoformat(), help="ISO date, default: today")
    parser.add_argument("--run-status", choices=["auto", *sorted(RUN_STATUSES)], default="auto")
    parser.add_argument("--literature-cutoff", help="Latest literature date covered, default: run date")
    parser.add_argument("--fingerprint-revision", help="Optional project fingerprint revision label")
    parser.add_argument("--fingerprint-sha256", help="Optional SHA-256 of the fingerprint used")
    parser.add_argument("--public-disclosure-date", help="Earliest verified public date of the project's WP")
    parser.add_argument("--public-disclosure-url", help="Stable public record for the project's WP")
    parser.add_argument(
        "--public-disclosure-provenance",
        choices=["user_stated", "public_record", "unknown"],
        help="How the project's public date was established",
    )
    parser.add_argument("--out", type=Path, help="Output state path; may equal --state")
    parser.add_argument("--backup", action="store_true", help="Back up an existing output to .bak")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print merged state without writing")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return
    if not all((args.state, args.observations, args.run_id)):
        parser.error("--state, --observations, and --run-id are required")

    state = load_json(args.state)
    raw_observations = load_json(args.observations)
    observations = raw_observations.get("observations", []) if isinstance(raw_observations, dict) else raw_observations
    if not isinstance(observations, list):
        raise ValueError("observations input must be an array or {observations: [...]} object")
    coverage = load_json(args.coverage) if args.coverage else []
    if not isinstance(coverage, list):
        raise ValueError("coverage input must be a JSON array")

    merged = merge_state(
        state,
        observations,
        args.run_id,
        args.run_date,
        coverage,
        run_status=args.run_status,
        literature_cutoff=args.literature_cutoff,
        fingerprint_revision=args.fingerprint_revision,
        fingerprint_sha256=args.fingerprint_sha256,
        public_disclosure_date=args.public_disclosure_date,
        public_disclosure_url=args.public_disclosure_url,
        public_disclosure_provenance=args.public_disclosure_provenance,
    )
    if args.dry_run:
        print(json.dumps(merged, ensure_ascii=False, indent=2))
        return
    output = args.out or args.state
    atomic_write(output, merged, backup=args.backup)
    print(output.resolve())


if __name__ == "__main__":
    main()
