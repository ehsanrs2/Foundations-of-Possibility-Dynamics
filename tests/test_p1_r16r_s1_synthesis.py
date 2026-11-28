"""S1 source and status consistency only; not scientific validation."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"
SYNTHESIS = RESEARCH / "R16R-S1-scientific-synthesis.md"
STATUS = RESEARCH / "R16R-S1-status.json"


def load(name):
    return json.loads((RESEARCH / name).read_text(encoding="utf-8"))


class S1SynthesisTests(unittest.TestCase):
    def test_synthesis_local_sources_exist(self):
        for link in re.findall(r"\]\(([^)]+)\)", SYNTHESIS.read_text(encoding="utf-8")):
            target = link.split("#")[0]
            if target and not target.startswith(("https://", "http://")):
                self.assertTrue((RESEARCH / target).is_file(), target)

    def test_no_change_to_primary_or_scientific_gates(self):
        s = load(STATUS.name)
        prior = load("R16Q-progress-manifest.json")
        self.assertEqual(s["H1"], prior["H1"])
        self.assertFalse(s["external_literature_search_completed"])
        self.assertFalse(s["independent_review_completed"])
        self.assertFalse(s["scientific_novelty_established"])
        self.assertEqual(s["tracks"]["R1"], "PAUSED_PENDING_INDEPENDENT_REVIEW")
        self.assertEqual(s["tracks"]["causal"], "NOT_EVALUATED")

    def test_development_scores_match_archives(self):
        text = SYNTHESIS.read_text(encoding="utf-8")
        r8 = load("R8-development-summary-seed20261101.json")
        self.assertEqual(r8["baseline_brier_expected_mean"],
                         r8["baseline_plus_r1_brier_expected_mean"])
        self.assertIn(f'{r8["baseline_brier_expected_mean"]:.12f}', text)
        self.assertEqual(r8["r1_distinct_defined_values"], [0])
        r11 = load("R11-unknown-time-prediction-results-20261102.json")
        for arm in ("raw", "standard_dp"):
            score = r11["results"][arm]["prediction"]["mean_expected_brier"]
            self.assertIn(f"{score:.12f}", text)
        r12 = load("R12-cross-grammar-results-20261102.json")
        for arm in ("raw", "interaction", "state_dp"):
            score = r12["runs"][arm]["result"]["mean_expected_brier"]
            self.assertIn(f"{score:.12f}", text)
        self.assertEqual(r12["sealed_H1_test_samples"], 0)

    def test_gog_negative_and_field_block_preserved(self):
        archive = load("R16Q-GOG2a-CI-summary-20261128.json")
        for run in archive["runs"]:
            c = run["report"]["comparison"]
            for key in ("cpu_ms", "wall_ms"):
                self.assertGreater(c["adaptive_components"][key],
                                   c["goalwise_index"][key])
        r15 = load("R15-node-job-lineage-results-20261108.json")
        self.assertEqual(r15["physical_service_restoration_labels"], 0)
        self.assertFalse(r15["source_join_evidence"]["direct_publisher_original_file_authenticated"])

    def test_readmes_and_claims_link_current_synthesis(self):
        for path in (ROOT / "README.md", ROOT / "README.fa.md",
                     RESEARCH / "claims.md"):
            self.assertIn(SYNTHESIS.name, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
