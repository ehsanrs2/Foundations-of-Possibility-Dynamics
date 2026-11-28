"""Offline archive consistency checks, not rerun timing or scientific review."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / "research"
ARCHIVE = json.loads((ROOT / "R16Q-GOG2a-CI-summary-20261128.json").read_text())
MANIFEST = json.loads((ROOT / "R16Q-progress-manifest.json").read_text())

class ReviewArchiveTests(unittest.TestCase):
    def test_source_records(self):
        self.assertEqual([r["run_id"] for r in ARCHIVE["runs"]],
                         [45611438837, 46111841179])
        for r in ARCHIVE["runs"]:
            self.assertEqual(r["job_conclusion"], "success")
            self.assertEqual(r["reported_test_counts"], [10, 655])
            self.assertEqual(r["report"]["exact_cases"], 28)
            self.assertEqual(r["report"]["repetitions"], 3)

    def test_same_deterministic_work_across_reused_suite(self):
        a, b = [r["report"]["comparison"] for r in ARCHIVE["runs"]]
        self.assertEqual(set(a), {"state_layers","shared_index",
                                  "goalwise_index","fixed_pairs","adaptive_components"})
        self.assertEqual({k:v["work"] for k,v in a.items()},
                         {k:v["work"] for k,v in b.items()})
        self.assertEqual(a["adaptive_components"]["work"]["pair_tests"], 516)
        self.assertEqual(a["adaptive_components"]["work"]["search_calls"], 199)
        self.assertEqual(a["goalwise_index"]["work"]["search_calls"], 254)

    def test_recorded_negative_is_not_assertion_about_future_runs(self):
        for run in ARCHIVE["runs"]:
            c = run["report"]["comparison"]
            self.assertGreater(c["adaptive_components"]["cpu_ms"],
                               c["goalwise_index"]["cpu_ms"])
            self.assertGreater(c["adaptive_components"]["wall_ms"],
                               c["goalwise_index"]["wall_ms"])
        self.assertEqual(MANIFEST["decision"],"PROPOSED_NOT_INDEPENDENTLY_ACCEPTED")

    def test_scientific_firewall(self):
        self.assertEqual(MANIFEST["H1"]["status"],"DRAFT_NOT_PREREGISTERED")
        self.assertEqual(MANIFEST["H1"]["confirmatory_samples"],0)
        self.assertEqual(MANIFEST["H1"]["field_labels"],0)
        self.assertFalse(MANIFEST["H1"]["sealed_families_accessed"])
        self.assertFalse(ARCHIVE["sealed_families_accessed"])
        self.assertEqual(ARCHIVE["H1_confirmatory_samples"],0)

if __name__ == "__main__":
    unittest.main()
