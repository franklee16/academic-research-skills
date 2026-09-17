#!/usr/bin/env python3
"""Validate structural, provenance, and validation honesty in questionnaire specs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


INSTRUMENT_TYPES = {
    "fact-behavior-survey",
    "attitude-item-set",
    "latent-scale",
    "knowledge-or-ability-test",
    "screening-or-decision-tool",
    "registration-or-service-form",
}
STATUSES = {"draft", "cognitive-test", "pilot", "production", "retired"}
SAMPLING = {
    "probability",
    "nonprobability",
    "census",
    "mixed-source",
    "to-be-determined",
}
PRIVACY = {"anonymous", "confidential-identifiable", "confidential-deidentified"}
CONSTRUCT_KINDS = {"observed-variable", "reflective-latent", "formative-index", "test-domain"}
RESPONSE_TYPES = {
    "single-choice",
    "multiple-choice",
    "ordinal-rating",
    "numeric",
    "date-or-time",
    "open-text",
    "ranking",
    "constant-sum",
}
CHOICE_TYPES = {"single-choice", "multiple-choice", "ordinal-rating", "ranking"}
SOURCE_STATUSES = {"validated", "adapted", "official", "new"}
LICENSE_STATUSES = {"open", "permission-obtained", "permission-required", "unknown", "self-authored"}
TEST_STATUSES = {"planned", "in-progress", "completed", "not-applicable-with-rationale"}
CONSENT_MODES = {"explicit", "implied-by-submission", "waived-with-approval"}
SYSTEM_ONLY_MISSING = {"not_shown"}


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def list_of(value: Any, expected: type | tuple[type, ...] | None = None) -> list[Any]:
    if not isinstance(value, list):
        return []
    if expected is None:
        return value
    return [item for item in value if isinstance(item, expected)]


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def index(records: Any, section: str, report: Report) -> dict[str, dict[str, Any]]:
    if not isinstance(records, list):
        report.error(f"{section} must be a list")
        return {}
    result: dict[str, dict[str, Any]] = {}
    for number, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            report.error(f"{section}[{number}] must be an object")
            continue
        record_id = record.get("id")
        if not text(record_id):
            report.error(f"{section}[{number}].id is required")
        elif record_id in result:
            report.error(f"duplicate {section} id {record_id!r}")
        else:
            result[record_id] = record
    return result


def refs(owner: str, values: Any, targets: dict[str, Any], field: str, report: Report) -> list[str]:
    clean = list_of(values, str)
    if not clean:
        report.error(f"{owner}.{field} must contain at least one id")
    for value in clean:
        if value not in targets:
            report.error(f"{owner}.{field} references unknown id {value!r}")
    return clean


def validate(data: Any) -> Report:
    report = Report()
    if not isinstance(data, dict):
        report.error("root must be a JSON object")
        return report

    instrument = data.get("instrument")
    if not isinstance(instrument, dict):
        report.error("instrument must be an object")
        instrument = {}
    for field in ("title", "version", "inference_scope", "ethics_review_status"):
        if not text(instrument.get(field)):
            report.error(f"instrument.{field} is required")
    instrument_type = instrument.get("instrument_type")
    if instrument_type not in INSTRUMENT_TYPES:
        report.error("instrument.instrument_type is invalid")
    status = instrument.get("status")
    if status not in STATUSES:
        report.error("instrument.status is invalid")
    if instrument.get("sampling_approach") not in SAMPLING:
        report.error("instrument.sampling_approach is invalid")
    if instrument.get("privacy_model") not in PRIVACY:
        report.error("instrument.privacy_model is invalid")
    if not list_of(instrument.get("languages"), str):
        report.error("instrument.languages must be non-empty")
    if not list_of(instrument.get("modes"), str):
        report.error("instrument.modes must be non-empty")

    participant_materials = data.get("participant_materials")
    if not isinstance(participant_materials, dict):
        report.error("participant_materials must be an object")
        participant_materials = {}
    for field in (
        "organization",
        "study_purpose",
        "estimated_minutes",
        "voluntary_statement",
        "privacy_statement",
        "consent_prompt",
        "contact",
        "completion_message",
    ):
        if not text(participant_materials.get(field)):
            report.error(f"participant_materials.{field} is required")
    if participant_materials.get("consent_mode") not in CONSENT_MODES:
        report.error("participant_materials.consent_mode is invalid")

    rqs = index(data.get("research_questions"), "research_questions", report)
    populations = index(data.get("populations"), "populations", report)
    constructs = index(data.get("constructs"), "constructs", report)
    forms = index(data.get("forms"), "forms", report)
    sections = index(data.get("sections"), "sections", report)
    items = index(data.get("items"), "items", report)
    for population_id in list_of(instrument.get("target_population_ids"), str):
        if population_id not in populations:
            report.error(f"instrument.target_population_ids references unknown id {population_id!r}")
    if not list_of(instrument.get("target_population_ids"), str):
        report.error("instrument.target_population_ids must be non-empty")

    for rq_id, rq in rqs.items():
        if not text(rq.get("text")):
            report.error(f"research_question {rq_id}.text is required")
    for population_id, population in populations.items():
        owner = f"population {population_id}"
        for field in ("label", "respondent_role", "observation_unit", "analysis_unit"):
            if not text(population.get(field)):
                report.error(f"{owner}.{field} is required")
    languages = set(list_of(instrument.get("languages"), str))
    modes = set(list_of(instrument.get("modes"), str))
    form_populations: set[str] = set()
    for form_id, form in forms.items():
        owner = f"form {form_id}"
        for field in ("title", "introduction", "instructions"):
            if not text(form.get(field)):
                report.error(f"{owner}.{field} is required")
        population_id = form.get("population_id")
        if population_id not in populations:
            report.error(f"{owner}.population_id references unknown id {population_id!r}")
        else:
            form_populations.add(population_id)
        if form.get("language") not in languages:
            report.error(f"{owner}.language is not declared in instrument.languages")
        if form.get("mode") not in modes:
            report.error(f"{owner}.mode is not declared in instrument.modes")
    for population_id in list_of(instrument.get("target_population_ids"), str):
        if population_id not in form_populations:
            report.error(f"target population {population_id!r} has no implementation form")
    for section_id, section in sections.items():
        owner = f"section {section_id}"
        for field in ("title", "introduction"):
            if not text(section.get(field)):
                report.error(f"{owner}.{field} is required")
        refs(owner, section.get("population_ids"), populations, "population_ids", report)
    for construct_id, construct in constructs.items():
        owner = f"construct {construct_id}"
        for field in ("label", "definition"):
            if not text(construct.get(field)):
                report.error(f"{owner}.{field} is required")
        if construct.get("kind") not in CONSTRUCT_KINDS:
            report.error(f"{owner}.kind is invalid")
        refs(owner, construct.get("rq_ids"), rqs, "rq_ids", report)

    variable_names: set[str] = set()
    rq_coverage: set[str] = set()
    for item_id, item in items.items():
        owner = f"item {item_id}"
        rq_ids = refs(owner, item.get("rq_ids"), rqs, "rq_ids", report)
        refs(owner, item.get("construct_ids"), constructs, "construct_ids", report)
        refs(owner, item.get("population_ids"), populations, "population_ids", report)
        section_id = item.get("section_id")
        if section_id not in sections:
            report.error(f"{owner}.section_id references unknown id {section_id!r}")
        if not isinstance(item.get("required"), bool):
            report.error(f"{owner}.required must be boolean")
        rq_coverage.update(rq_ids)
        for field in (
            "question_text",
            "recall_period",
            "referent",
            "universe",
            "display_logic",
            "skip_logic",
            "validation_status",
            "analysis_use",
        ):
            if not text(item.get(field)):
                report.error(f"{owner}.{field} is required")
        variable_name = item.get("variable_name")
        if not text(variable_name):
            report.error(f"{owner}.variable_name is required")
        elif variable_name in variable_names:
            report.error(f"duplicate variable_name {variable_name!r}")
        else:
            variable_names.add(variable_name)

        response_type = item.get("response_type")
        if response_type not in RESPONSE_TYPES:
            report.error(f"{owner}.response_type is invalid")
        options = list_of(item.get("response_options"), dict)
        if response_type in CHOICE_TYPES and len(options) < 2:
            report.error(f"{owner}.response_options needs at least two options")
        option_codes: list[Any] = []
        for number, option in enumerate(options, start=1):
            if "code" not in option or not text(option.get("label")):
                report.error(f"{owner}.response_options[{number}] needs code and label")
            else:
                option_codes.append(option["code"])
        if len(option_codes) != len(set(map(str, option_codes))):
            report.error(f"{owner}.response_options contains duplicate codes")

        missing = item.get("missing_codes")
        if not isinstance(missing, dict) or not missing:
            report.error(f"{owner}.missing_codes must be a non-empty object")
            missing = {}
        else:
            missing_codes = list(missing.values())
            if len(missing_codes) != len(set(map(str, missing_codes))):
                report.error(f"{owner}.missing_codes must be distinct")
            if set(map(str, missing_codes)) & set(map(str, option_codes)):
                report.error(f"{owner}.missing_codes overlap substantive response codes")
        missing_display = list_of(item.get("missing_display"), str)
        if not isinstance(item.get("missing_display"), list):
            report.error(f"{owner}.missing_display must be a list")
        for key in missing_display:
            if key not in missing:
                report.error(f"{owner}.missing_display references unknown missing code {key!r}")
            if key in SYSTEM_ONLY_MISSING:
                report.error(f"{owner}.missing_display cannot expose system-only code {key!r}")
        if item.get("required") is True and "refused" in missing and "refused" not in missing_display:
            report.warn(f"{owner} is required but does not visibly offer the permitted refusal response")

        source_status = item.get("source_status")
        if source_status not in SOURCE_STATUSES:
            report.error(f"{owner}.source_status is invalid")
        if source_status in {"validated", "adapted", "official"} and not text(item.get("source")):
            report.error(f"{owner}.source is required for {source_status}")
        if source_status == "validated" and item.get("wording_changed") is True:
            report.error(f"{owner} changed wording and must be adapted, not validated")
        if source_status == "new" and item.get("validation_status") != "draft-unvalidated":
            report.error(f"{owner} is new and must be draft-unvalidated")
        if item.get("license_status") not in LICENSE_STATUSES:
            report.error(f"{owner}.license_status is invalid")
        if item.get("license_status") in {"permission-required", "unknown"}:
            report.warn(f"{owner} has unresolved permission status")

    for rq_id in rqs:
        if rq_id not in rq_coverage:
            report.error(f"research_question {rq_id} has no questionnaire item")

    testing = data.get("testing")
    if not isinstance(testing, dict):
        report.error("testing must be an object")
        testing = {}
    for field in ("expert_review", "cognitive_interviewing", "usability_testing", "field_pilot"):
        if testing.get(field) not in TEST_STATUSES:
            report.error(f"testing.{field} has invalid status")
    if not list_of(testing.get("path_test_cases"), str):
        report.error("testing.path_test_cases must be non-empty")
    if status == "production":
        for field in ("cognitive_interviewing", "usability_testing", "field_pilot"):
            if testing.get(field) not in {"completed", "not-applicable-with-rationale"}:
                report.error(f"production instrument requires resolved testing.{field}")

    validation = data.get("measurement_validation")
    if not isinstance(validation, dict):
        report.error("measurement_validation must be an object")
        validation = {}
    if not isinstance(validation.get("required"), bool):
        report.error("measurement_validation.required must be boolean")
    if not text(validation.get("rationale")):
        report.error("measurement_validation.rationale is required")
    evidence = list_of(validation.get("planned_evidence"), str)
    if instrument_type in {"latent-scale", "knowledge-or-ability-test", "screening-or-decision-tool"}:
        if validation.get("required") is not True:
            report.error(f"{instrument_type} requires a measurement validation plan")
        if not evidence:
            report.error(f"{instrument_type} requires planned_evidence")

    data_quality = data.get("data_quality")
    if not isinstance(data_quality, dict):
        report.error("data_quality must be an object")
    else:
        if not list_of(data_quality.get("predefined_rules"), str):
            report.error("data_quality.predefined_rules must be non-empty")
        if not text(data_quality.get("sensitivity_analysis")):
            report.error("data_quality.sensitivity_analysis is required")

    governance = data.get("governance")
    if not isinstance(governance, dict):
        report.error("governance must be an object")
    else:
        if not text(governance.get("data_minimization_review")):
            report.error("governance.data_minimization_review is required")
        if not isinstance(governance.get("contact_data_separated"), bool):
            report.error("governance.contact_data_separated must be boolean")
        if not text(governance.get("retention_plan")):
            report.error("governance.retention_plan is required")

    if instrument.get("privacy_model") == "anonymous" and governance.get("contact_data_separated") is False:
        report.error("anonymous instrument cannot retain linked contact data")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.spec.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read questionnaire spec: {exc}")
        return 2
    report = validate(data)
    for message in report.errors:
        print(f"ERROR: {message}")
    for message in report.warnings:
        print(f"WARNING: {message}")
    print(f"SUMMARY: {len(report.errors)} error(s), {len(report.warnings)} warning(s)")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
