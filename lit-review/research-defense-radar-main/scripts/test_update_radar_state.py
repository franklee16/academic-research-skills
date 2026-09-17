#!/usr/bin/env python3
"""Regression tests for the deterministic radar-state engine."""

import unittest

from update_radar_state import merge_state


def state_v11():
    return {
        "schema_version": "1.1",
        "project": {
            "slug": "demo",
            "fingerprint_revision": None,
            "fingerprint_sha256": None,
            "fingerprint_updated_at": None,
            "public_disclosure_date": None,
            "public_disclosure_url": None,
            "public_disclosure_provenance": "unknown",
        },
        "last_attempted_scan_at": None,
        "last_successful_scan_at": None,
        "papers": [],
        "runs": [],
    }


def complete_coverage(run_date="2026-08-24"):
    return [{
        "source": "primary-index",
        "query_family": "question",
        "checked_at": run_date,
        "status": "completed",
        "required": True,
    }]


def observation(**overrides):
    value = {
        "title": "A Shared Paper Title",
        "authors": ["Ada Author", "Ben Author"],
        "canonical_url": "https://working.example/paper",
        "category": "B",
        "evidence_level": "M",
        "verified_at": "2026-08-17",
        "confidence": "low",
    }
    value.update(overrides)
    return value


class RadarStateTests(unittest.TestCase):
    def test_url_record_merges_with_later_doi_version_and_keeps_id(self):
        first = merge_state(
            state_v11(), [observation()], "run-1", "2026-08-17", complete_coverage("2026-08-17")
        )
        original_id = first["papers"][0]["id"]
        later = observation(
            doi="10.1000/shared",
            canonical_url="https://publisher.example/article",
            evidence_level="F",
            verified_at="2026-08-24",
            confidence="high",
            overlap_score=70,
            change_kind="evidence_upgrade",
        )
        merged = merge_state(first, [later], "run-2", "2026-08-24", complete_coverage())
        self.assertEqual(len(merged["papers"]), 1)
        self.assertEqual(merged["papers"][0]["id"], original_id)
        self.assertEqual(merged["papers"][0]["doi"], "10.1000/shared")
        self.assertIn("url:https://working.example/paper", merged["papers"][0]["identity_keys"])
        self.assertIn("doi:10.1000/shared", merged["papers"][0]["identity_keys"])

    def test_conflicting_dois_do_not_merge_on_title_and_author(self):
        first = observation(doi="10.1000/one")
        second = observation(doi="10.1000/two")
        merged = merge_state(
            state_v11(), [first, second], "run-1", "2026-08-24", complete_coverage()
        )
        self.assertEqual(len(merged["papers"]), 2)

    def test_incomplete_coverage_does_not_advance_success_clock(self):
        initial = state_v11()
        initial["last_successful_scan_at"] = "2026-08-17"
        coverage = [{
            "source": "blocked-index",
            "query_family": "question",
            "checked_at": "2026-08-24",
            "status": "inaccessible",
            "required": True,
        }]
        merged = merge_state(initial, [], "run-2", "2026-08-24", coverage)
        self.assertEqual(merged["last_attempted_scan_at"], "2026-08-24")
        self.assertEqual(merged["last_successful_scan_at"], "2026-08-17")
        self.assertEqual(merged["runs"][-1]["run_status"], "failed")
        self.assertFalse(merged["runs"][-1]["coverage_complete"])

    def test_completed_status_requires_complete_coverage(self):
        with self.assertRaisesRegex(ValueError, "required coverage"):
            merge_state(
                state_v11(), [], "run-1", "2026-08-24", [], run_status="completed"
            )

    def test_metadata_only_observation_cannot_have_numeric_score(self):
        with self.assertRaisesRegex(ValueError, "metadata-only"):
            merge_state(
                state_v11(),
                [observation(overlap_score=80)],
                "run-1",
                "2026-08-24",
                complete_coverage(),
            )

    def test_evidence_upgrade_is_recorded_but_not_material(self):
        first = merge_state(
            state_v11(), [observation()], "run-1", "2026-08-17", complete_coverage("2026-08-17")
        )
        upgraded = observation(
            evidence_level="A",
            verified_at="2026-08-24",
            confidence="medium",
            change_kind="evidence_upgrade",
        )
        merged = merge_state(first, [upgraded], "run-2", "2026-08-24", complete_coverage())
        event = merged["papers"][0]["change_history"][-1]
        self.assertEqual(event["kind"], "evidence_upgrade")
        self.assertFalse(event["material"])
        self.assertNotIn("last_material_change_at", merged["papers"][0])

    def test_schema_10_migrates_conservatively(self):
        legacy = {
            "schema_version": "1.0",
            "project": {"slug": "legacy"},
            "last_scan_at": "2026-08-17",
            "papers": [],
            "runs": [{"run_id": "old", "run_date": "2026-08-17", "coverage": []}],
        }
        merged = merge_state(legacy, [], "new", "2026-08-24", complete_coverage())
        self.assertEqual(merged["schema_version"], "1.1")
        self.assertEqual(merged["last_attempted_scan_at"], "2026-08-24")
        self.assertEqual(merged["last_successful_scan_at"], "2026-08-24")
        self.assertEqual(merged["runs"][0]["run_status"], "partial")

    def test_same_run_id_is_idempotent(self):
        first = merge_state(
            state_v11(), [observation()], "same-run", "2026-08-24", complete_coverage()
        )
        second = merge_state(
            first, [observation()], "same-run", "2026-08-24", complete_coverage()
        )
        self.assertEqual(len(second["papers"]), 1)
        self.assertEqual(len(second["runs"]), 1)

    def test_post_disclosure_paper_does_not_preempt_public_time_novelty(self):
        state = state_v11()
        state["project"]["public_disclosure_date"] = "2026-05-01"
        later = observation(
            earliest_public_date="2026-06-15",
            earliest_public_date_provenance="public_record",
        )
        merged = merge_state(
            state, [later], "run-1", "2026-08-24", complete_coverage()
        )
        paper = merged["papers"][0]
        self.assertEqual(paper["chronology_relation"], "post_disclosure")
        self.assertEqual(paper["priority_effect"], "no_preemption_post_disclosure")

    def test_missing_public_date_keeps_priority_uncertain(self):
        state = state_v11()
        state["project"]["public_disclosure_date"] = "2026-05-01"
        merged = merge_state(
            state, [observation()], "run-1", "2026-08-24", complete_coverage()
        )
        self.assertEqual(merged["papers"][0]["chronology_relation"], "unknown")
        self.assertEqual(merged["papers"][0]["priority_effect"], "uncertain")

    def test_later_journal_version_keeps_the_lineages_earliest_public_date(self):
        state = state_v11()
        state["project"]["public_disclosure_date"] = "2026-05-01"
        working_paper = observation(
            doi="10.1000/lineage",
            earliest_public_date="2026-04-01",
            current_version_date="2026-04-01",
        )
        state = merge_state(
            state, [working_paper], "run-1", "2026-04-15", complete_coverage("2026-04-15")
        )
        journal_version = observation(
            doi="10.1000/lineage",
            canonical_url="https://publisher.example/lineage",
            earliest_public_date="2026-08-01",
            current_version_date="2026-08-01",
            evidence_level="F",
            verified_at="2026-08-24",
            confidence="high",
            overlap_score=75,
            change_kind="identity_update",
        )
        merged = merge_state(
            state, [journal_version], "run-2", "2026-08-24", complete_coverage()
        )
        paper = merged["papers"][0]
        self.assertEqual(paper["earliest_public_date"], "2026-04-01")
        self.assertEqual(paper["current_version_date"], "2026-08-01")
        self.assertEqual(paper["chronology_relation"], "pre_disclosure")


if __name__ == "__main__":
    unittest.main()
