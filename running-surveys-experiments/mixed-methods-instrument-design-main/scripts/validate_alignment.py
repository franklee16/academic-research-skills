#!/usr/bin/env python3
"""Validate the structural alignment of a mixed-methods instrument map."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


DESIGNS = {
    "convergent",
    "explanatory-sequential",
    "exploratory-sequential",
    "embedded",
    "multiphase",
}
STRANDS = {"QUAN", "QUAL", "MIXED"}
POPULATION_STRANDS = {"QUAN", "QUAL", "BOTH"}
SOURCE_STATUSES = {"validated", "adapted", "official", "new"}
INTERVIEW_ROLES = {"warmup", "transition", "core", "closing"}
INTEGRATION_STRATEGIES = {
    "compare",
    "explain",
    "build",
    "connect",
    "embed",
    "transform",
    "triangulate",
    "complement",
}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def index_records(
    records: Any, section: str, report: Report
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    if not isinstance(records, list):
        report.error(f"{section} must be a list")
        return [], {}

    clean: list[dict[str, Any]] = []
    index: dict[str, dict[str, Any]] = {}
    for position, raw in enumerate(records, start=1):
        if not isinstance(raw, dict):
            report.error(f"{section}[{position}] must be an object")
            continue
        record_id = raw.get("id")
        if not nonempty_text(record_id):
            report.error(f"{section}[{position}] has no non-empty id")
            continue
        if record_id in index:
            report.error(f"duplicate id {record_id!r} in {section}")
            continue
        clean.append(raw)
        index[record_id] = raw
    return clean, index


def check_references(
    owner: str,
    values: Any,
    target: dict[str, dict[str, Any]],
    field: str,
    report: Report,
    required: bool = True,
) -> list[str]:
    refs = as_list(values)
    if required and not refs:
        report.error(f"{owner}.{field} must contain at least one id")
    for ref in refs:
        if ref not in target:
            report.error(f"{owner}.{field} references unknown id {ref!r}")
    return [ref for ref in refs if isinstance(ref, str)]


def validate(data: Any) -> Report:
    report = Report()
    if not isinstance(data, dict):
        report.error("root must be a JSON object")
        return report

    study = data.get("study")
    if not isinstance(study, dict):
        report.error("study must be an object")
        study = {}
    if not nonempty_text(study.get("title")):
        report.error("study.title is required")
    design = study.get("mixed_methods_design")
    if design not in DESIGNS:
        report.error(
            "study.mixed_methods_design must be one of: " + ", ".join(sorted(DESIGNS))
        )
    if not as_list(study.get("integration_purposes")):
        report.error("study.integration_purposes must contain at least one purpose")
    if not nonempty_text(study.get("timing")):
        report.error("study.timing is required")
    if not nonempty_text(study.get("priority")):
        report.error("study.priority is required")

    rqs, rq_index = index_records(data.get("research_questions"), "research_questions", report)
    populations, population_index = index_records(
        data.get("populations"), "populations", report
    )
    constructs, construct_index = index_records(data.get("constructs"), "constructs", report)
    survey_items, survey_index = index_records(
        data.get("survey_items"), "survey_items", report
    )
    interview_questions, interview_index = index_records(
        data.get("interview_questions"), "interview_questions", report
    )
    integration_links, integration_index = index_records(
        data.get("integration_links"), "integration_links", report
    )

    if not rqs:
        report.error("at least one research question is required")
    if not populations:
        report.error("at least one population is required")
    if not survey_items:
        report.error("at least one survey item is required")
    if not interview_questions:
        report.error("at least one interview question is required")

    for rq in rqs:
        owner = f"research_question {rq['id']}"
        if not nonempty_text(rq.get("text")):
            report.error(f"{owner}.text is required")
        if rq.get("strand_intent") not in STRANDS:
            report.error(f"{owner}.strand_intent must be QUAN, QUAL, or MIXED")

    for population in populations:
        owner = f"population {population['id']}"
        if not nonempty_text(population.get("label")):
            report.error(f"{owner}.label is required")
        if population.get("strand") not in POPULATION_STRANDS:
            report.error(f"{owner}.strand must be QUAN, QUAL, or BOTH")
        if not nonempty_text(population.get("unit_of_analysis")):
            report.error(f"{owner}.unit_of_analysis is required")

    for construct in constructs:
        owner = f"construct {construct['id']}"
        if not nonempty_text(construct.get("label")):
            report.error(f"{owner}.label is required")
        if not nonempty_text(construct.get("definition")):
            report.error(f"{owner}.definition is required")
        check_references(owner, construct.get("rq_ids"), rq_index, "rq_ids", report)

    variable_names: dict[str, str] = {}
    survey_coverage: defaultdict[str, set[str]] = defaultdict(set)
    for item in survey_items:
        owner = f"survey_item {item['id']}"
        rq_ids = check_references(owner, item.get("rq_ids"), rq_index, "rq_ids", report)
        construct_ids = check_references(
            owner, item.get("construct_ids"), construct_index, "construct_ids", report
        )
        population_ids = check_references(
            owner, item.get("population_ids"), population_index, "population_ids", report
        )
        for rq_id in rq_ids:
            survey_coverage[rq_id].add(item["id"])
        if not nonempty_text(item.get("question_text")):
            report.error(f"{owner}.question_text is required")
        if not nonempty_text(item.get("response_type")):
            report.error(f"{owner}.response_type is required")
        if not nonempty_text(item.get("validation_status")):
            report.error(f"{owner}.validation_status is required")
        for population_id in population_ids:
            population = population_index.get(population_id, {})
            if population.get("strand") == "QUAL":
                report.error(
                    f"{owner} uses QUAL-only population {population_id!r} for a survey item"
                )
        for construct_id in construct_ids:
            construct_rqs = set(as_list(construct_index.get(construct_id, {}).get("rq_ids")))
            if construct_rqs and construct_rqs.isdisjoint(rq_ids):
                report.error(
                    f"{owner} and construct {construct_id!r} do not share a research question"
                )
        variable_name = item.get("variable_name")
        if not nonempty_text(variable_name):
            report.error(f"{owner}.variable_name is required")
        elif variable_name in variable_names:
            report.error(
                f"duplicate variable_name {variable_name!r} in {owner} and "
                f"survey_item {variable_names[variable_name]}"
            )
        else:
            variable_names[variable_name] = item["id"]

        source_status = item.get("source_status")
        if source_status not in SOURCE_STATUSES:
            report.error(
                f"{owner}.source_status must be one of: "
                + ", ".join(sorted(SOURCE_STATUSES))
            )
        if source_status in {"validated", "adapted", "official"} and not nonempty_text(
            item.get("source")
        ):
            report.error(f"{owner}.source is required for source_status={source_status}")
        if source_status == "validated" and item.get("wording_changed") is True:
            report.error(f"{owner} changed wording and must be marked adapted, not validated")
        if source_status == "new" and item.get("validation_status") != "draft-unvalidated":
            report.error(
                f"{owner} is new and validation_status must be 'draft-unvalidated'"
            )

    interview_coverage: defaultdict[str, set[str]] = defaultdict(set)
    for question in interview_questions:
        owner = f"interview_question {question['id']}"
        rq_ids = check_references(
            owner, question.get("rq_ids"), rq_index, "rq_ids", report
        )
        population_ids = check_references(
            owner,
            question.get("population_ids"),
            population_index,
            "population_ids",
            report,
        )
        for rq_id in rq_ids:
            interview_coverage[rq_id].add(question["id"])
        for population_id in population_ids:
            population = population_index.get(population_id, {})
            if population.get("strand") == "QUAN":
                report.error(
                    f"{owner} uses QUAN-only population {population_id!r} "
                    "for an interview question"
                )
        role = question.get("question_role")
        if role not in INTERVIEW_ROLES:
            report.error(
                f"{owner}.question_role must be one of: "
                + ", ".join(sorted(INTERVIEW_ROLES))
            )
        if not nonempty_text(question.get("main_question")):
            report.error(f"{owner}.main_question is required")
        if role == "core":
            if not as_list(question.get("follow_ups")):
                report.error(f"{owner}.follow_ups must be non-empty for a core question")
            if not as_list(question.get("probes")):
                report.error(f"{owner}.probes must be non-empty for a core question")

    link_coverage: defaultdict[str, set[str]] = defaultdict(set)
    direct_link_coverage: defaultdict[str, set[str]] = defaultdict(set)
    for link in integration_links:
        owner = f"integration_link {link['id']}"
        rq_id = link.get("rq_id")
        if rq_id not in rq_index:
            report.error(f"{owner}.rq_id references unknown id {rq_id!r}")
        elif isinstance(rq_id, str):
            link_coverage[rq_id].add(link["id"])
        survey_item_ids = check_references(
            owner,
            link.get("survey_item_ids"),
            survey_index,
            "survey_item_ids",
            report,
            required=False,
        )
        interview_question_ids = check_references(
            owner,
            link.get("interview_question_ids"),
            interview_index,
            "interview_question_ids",
            report,
            required=False,
        )
        if link.get("strategy") not in INTEGRATION_STRATEGIES:
            report.error(
                f"{owner}.strategy must be one of: "
                + ", ".join(sorted(INTEGRATION_STRATEGIES))
            )
        if not nonempty_text(link.get("integration_level")):
            report.error(f"{owner}.integration_level is required")
        if isinstance(rq_id, str) and survey_item_ids and interview_question_ids:
            direct_link_coverage[rq_id].add(link["id"])
        for item_id in survey_item_ids:
            if item_id in survey_index and rq_id not in as_list(
                survey_index[item_id].get("rq_ids")
            ):
                report.error(
                    f"{owner} links survey item {item_id!r}, but both do not map to {rq_id!r}"
                )
        for question_id in interview_question_ids:
            if question_id in interview_index and rq_id not in as_list(
                interview_index[question_id].get("rq_ids")
            ):
                report.error(
                    f"{owner} links interview question {question_id!r}, "
                    f"but both do not map to {rq_id!r}"
                )

    for rq in rqs:
        rq_id = rq["id"]
        intent = rq.get("strand_intent")
        has_survey = bool(survey_coverage[rq_id])
        has_interview = bool(interview_coverage[rq_id])
        has_link = bool(link_coverage[rq_id])
        has_direct_link = bool(direct_link_coverage[rq_id])
        if intent == "QUAN" and not has_survey:
            report.error(f"{rq_id} is QUAN but has no survey item")
        elif intent == "QUAL" and not has_interview:
            report.error(f"{rq_id} is QUAL but has no interview question")
        elif intent == "MIXED":
            if not has_survey:
                report.error(f"{rq_id} is MIXED but has no survey item")
            if not has_interview:
                report.error(f"{rq_id} is MIXED but has no interview question")
            if not has_link:
                report.error(f"{rq_id} is MIXED but has no integration link")
            elif not has_direct_link:
                report.error(
                    f"{rq_id} is MIXED but no integration link connects both strands"
                )
        if not has_survey and not has_interview:
            report.error(f"{rq_id} has no data-collection coverage")

    linked_survey = {
        item_id
        for link in integration_links
        for item_id in as_list(link.get("survey_item_ids"))
    }
    linked_interview = {
        item_id
        for link in integration_links
        for item_id in as_list(link.get("interview_question_ids"))
    }
    for item in survey_items:
        if not set(as_list(item.get("rq_ids"))).isdisjoint(
            {rq["id"] for rq in rqs if rq.get("strand_intent") == "MIXED"}
        ) and item["id"] not in linked_survey:
            report.warn(f"survey_item {item['id']} maps to a MIXED RQ but is not in a link")
    for question in interview_questions:
        if not set(as_list(question.get("rq_ids"))).isdisjoint(
            {rq["id"] for rq in rqs if rq.get("strand_intent") == "MIXED"}
        ) and question["id"] not in linked_interview:
            report.warn(
                f"interview_question {question['id']} maps to a MIXED RQ but is not in a link"
            )

    if integration_index and not any(
        as_list(link.get("survey_item_ids")) and as_list(link.get("interview_question_ids"))
        for link in integration_links
    ):
        report.warn("no integration link directly connects survey and interview items")

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("map_file", type=Path, help="instrument-map JSON file")
    parser.add_argument("--json", action="store_true", help="emit a JSON report")
    args = parser.parse_args()

    try:
        data = json.loads(args.map_file.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.map_file}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        return 2

    report = validate(data)
    if args.json:
        print(
            json.dumps(
                {"errors": report.errors, "warnings": report.warnings},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for message in report.errors:
            print(f"ERROR: {message}")
        for message in report.warnings:
            print(f"WARNING: {message}")
        print(
            f"SUMMARY: {len(report.errors)} error(s), "
            f"{len(report.warnings)} warning(s)"
        )
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
