import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AdaptiveExecutionContractTests(unittest.TestCase):
    def test_skill_exposes_adaptive_policy_and_strong_profiles(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/adaptive-execution.md", skill)
        self.assertIn("GPT-5.6 Sol", skill)
        self.assertIn("Terra", skill)
        self.assertIn("model_assisted_candidate", skill)
        self.assertNotIn("only the registered implementation may emit candidate numeric values", skill)

    def test_adaptive_policy_keeps_evidence_and_non_invention_invariants(self):
        policy = (ROOT / "references" / "adaptive-execution.md").read_text(encoding="utf-8")
        for required in (
            "original coordinate space",
            "at least two anchors",
            "never fill them from an expected count",
            "original-canvas overlay",
            "model_assisted_candidate",
            "does not rewrite that flag",
        ):
            self.assertIn(required, policy)

    def test_binding_references_and_ui_prompt_match_the_policy(self):
        baseline = (ROOT / "references" / "research-quality-baseline.md").read_text(
            encoding="utf-8"
        )
        report_protocol = (ROOT / "references" / "report-and-evolution.md").read_text(
            encoding="utf-8"
        )
        ui = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("model_assisted_candidate", baseline)
        self.assertIn("model-assisted runs", report_protocol)
        self.assertIn("evidence-bound adaptive execution", ui)
        self.assertNotIn("registered deterministic implementation", ui)


if __name__ == "__main__":
    unittest.main()
