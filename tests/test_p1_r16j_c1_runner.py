"""Measured C1-Runner developer rehearsal: actual algorithms, NOT H1."""
from copy import deepcopy
from fractions import Fraction
import sys
import unittest

from experiments.p1_r10_executable_backup import ProcessCaps
from experiments.p1_r16j_c1_runner import (
    PROFILE, METHODS, _raw, _extra, _one_channel_reachable,
    compute, capped_run, summarize_runs, audit, caps_as_dict,
)


class C1RunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = {name: compute(name) for name in METHODS}
        cls.mock_measured = {
            name: {
                "method": name, "status": "PASS",
                "budget": caps_as_dict(ProcessCaps()),
                "prediction": cls.results[name],
            } for name in METHODS
        }

    def test_all_six_arms_are_genuine_feature_executors(self):
        self.assertEqual(len(METHODS), 6)
        self.assertEqual(set(self.results), set(METHODS))
        self.assertEqual(self.results["raw"]["feature_value_distinct_count"], 1)
        self.assertGreater(self.results["augmented_state_dp"][
            "feature_value_distinct_count"], 1)

    def test_raw_features_identical_independent_of_method(self):
        self.assertEqual(len(_raw("alias", 1, Fraction(1, 4))), 7)
        for name in METHODS:
            self.assertEqual(self.results[name][
                "fixed_feature_slots_excluding_intercept"], 8)

    def test_actual_scoped_r1_is_pre_fault_and_event_aware(self):
        self.assertEqual(_extra("r1_scoped_pair_candidate",
                                "independent", 2, Fraction(1, 2)), 1)
        self.assertEqual(_extra("r1_scoped_pair_candidate",
                                "alias", 2, Fraction(1, 2)), 0)
        self.assertEqual(_extra("r1_scoped_pair_candidate",
                                "common", 2, Fraction(1, 2)), 0)

    def test_resource_reachability_is_real_bounded_state_search(self):
        self.assertEqual(_one_channel_reachable(
            "independent", 0, Fraction(1, 2)), 0)
        self.assertEqual(_one_channel_reachable(
            "independent", 1, Fraction(1, 2)), 1)

    def test_single_route_vs_joint_dp_is_different_estimand(self):
        self.assertEqual(_extra("resource_reachability",
                                "independent", 1, Fraction(1, 2)), 1)
        self.assertEqual(_extra("augmented_state_dp",
                                "independent", 1, Fraction(1, 2)), 0)

    def test_modeled_training_task_is_repeated_structure(self):
        for r in self.results.values():
            self.assertEqual(r["train_parameter_settings"], 27)
            self.assertEqual(r["tune_parameter_settings"], 18)
            self.assertEqual(r["shared_train_and_tune_structure_groups"], 9)
            self.assertEqual(r["independent_test_systems"], 0)
            self.assertEqual(r["H1_confirmatory_samples"], 0)

    def test_paired_identity_hash_and_exact_targets(self):
        self.assertEqual(len({r["tune_identity_sha256"]
                              for r in self.results.values()}), 1)
        truth = {
            tuple((x["key"], x["known_model_probability"])
                  for x in r["tune_records"])
            for r in self.results.values()
        }
        self.assertEqual(len(truth), 1)

    def test_output_probabilities_and_brier_are_bounded(self):
        for record in self.results.values():
            for row in record["tune_records"]:
                self.assertGreaterEqual(row["forecast"], 0)
                self.assertLessEqual(row["forecast"], 1)
                self.assertGreaterEqual(row["expected_brier"], 0)
            phases = record["worker_phases_ms"]
            self.assertEqual(set(phases), {
                "feature", "synthetic_target_generation", "fit", "predict"})
            self.assertTrue(all(v >= 0 for v in phases.values()))

    def test_runner_can_summarize_valid_results_without_promotion(self):
        result = summarize_runs(self.mock_measured)
        self.assertEqual(result["status"],
                         "PASS_MEASURED_DEV_REHEARSAL_NOT_CONFIRMATION")
        self.assertEqual(result["independent_test_systems"], 0)
        self.assertFalse(result["H1_preregistered"])
        self.assertEqual(result["H1_confirmatory_samples"], 0)

    def test_failed_method_produces_no_score_or_claim(self):
        bad = deepcopy(self.mock_measured)
        bad["augmented_state_dp"] = {
            "method": "augmented_state_dp", "status": "WALL_TIMEOUT"}
        r = summarize_runs(bad)
        self.assertEqual(r["status"], "NO_COMPARATIVE_SCORE")
        self.assertNotIn("descriptive_DP_minus_R1", r)
        self.assertEqual(r["H1_confirmatory_samples"], 0)

    def test_missing_method_fails_closed(self):
        bad = deepcopy(self.mock_measured)
        bad.pop("physical_event_cut")
        with self.assertRaisesRegex(ValueError, "MISSING_METHOD_RESULTS"):
            summarize_runs(bad)

    def test_mismatched_target_is_detected(self):
        bad = deepcopy(self.mock_measured)
        bad["r1_scoped_pair_candidate"]["prediction"]["tune_records"][0][
            "known_model_probability"] = "99/100"
        with self.assertRaisesRegex(ValueError, "DIFFERENT_OUTCOME_LABELS"):
            summarize_runs(bad)

    def test_mismatched_prediction_identity_is_detected(self):
        bad = deepcopy(self.mock_measured)
        bad["physical_event_cut"]["prediction"]["tune_identity_sha256"] = "wrong"
        with self.assertRaisesRegex(ValueError, "PAIRED_TASK_OR_CAPACITY_MISMATCH"):
            summarize_runs(bad)

    def test_unequal_actual_compute_limits_are_rejected(self):
        bad = deepcopy(self.mock_measured)
        bad["raw"]["budget"]["wall_seconds"] = 50
        with self.assertRaisesRegex(ValueError, "UNEQUAL_ENFORCED_PROCESS_CAPS"):
            summarize_runs(bad)

    def test_worker_method_mislabeled_is_rejected(self):
        bad = deepcopy(self.mock_measured)
        bad["raw"]["prediction"]["method"] = "r1_scoped_pair_candidate"
        with self.assertRaisesRegex(ValueError, "METHOD_IDENTITY_MISMATCH"):
            summarize_runs(bad)

    def test_mismatched_feature_capacity_is_detected(self):
        bad = deepcopy(self.mock_measured)
        bad["raw"]["prediction"][
            "fixed_feature_slots_excluding_intercept"] = 300
        with self.assertRaisesRegex(ValueError, "PAIRED_TASK_OR_CAPACITY_MISMATCH"):
            summarize_runs(bad)

    def test_unknown_feature_or_method_is_rejected(self):
        with self.assertRaises(ValueError):
            compute("clairvoyant_oracle")
        with self.assertRaises(ValueError):
            _extra("unknown", "alias", 1, Fraction(1, 2))
        with self.assertRaises(ValueError):
            capped_run("unregistered")

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires Linux caps")
    def test_actual_subprocess_enforces_identical_limits(self):
        caps = ProcessCaps(wall_seconds=8, cpu_seconds=8, address_space_mb=256)
        run = capped_run("raw", caps)
        self.assertEqual(run["status"], "PASS", run)
        self.assertGreater(run["all_in_process_wall_ms"], 0)
        self.assertGreater(run["worker_cpu_ms"], 0)
        self.assertGreater(run["peak_rss_kib_linux"], 0)
        self.assertEqual(run["budget"], caps_as_dict(caps))

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires Linux caps")
    def test_hard_timeout_does_not_become_an_accuracy_win(self):
        tiny = ProcessCaps(wall_seconds=0.00001, cpu_seconds=1,
                           address_space_mb=256)
        x = capped_run("augmented_state_dp", tiny)
        self.assertNotEqual(x["status"], "PASS")
        self.assertNotIn("prediction", x)

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires Linux caps")
    def test_all_method_processes_run_real_learner_under_caps(self):
        report = audit()
        self.assertEqual(report["profile"], PROFILE)
        self.assertEqual(report["status"],
                         "PASS_MEASURED_DEV_REHEARSAL_NOT_CONFIRMATION")
        self.assertEqual(report["H1_confirmatory_samples"], 0)
        self.assertEqual(len(report["method_runs"]), 6)
        self.assertTrue(all(v["status"] == "PASS"
                            for v in report["method_runs"].values()))
        self.assertTrue(all(v["all_in_process_wall_ms"] > 0
                            for v in report["method_runs"].values()))
        self.assertTrue(all(v["peak_rss_kib_linux"] > 0
                            for v in report["method_runs"].values()))


if __name__ == "__main__":
    unittest.main()
