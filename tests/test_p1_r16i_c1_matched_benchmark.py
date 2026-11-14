"""C1: matched-information and all-in cost benchmark ADMISSION contract."""
from copy import deepcopy
import unittest

from experiments.p1_r16i_c1_matched_benchmark import (
    BASELINES, CANDIDATE, audit, demo_plan, validate_plan, toy_paired_brier,
)


class C1MatchedBenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.p = demo_plan()

    def deny(self, mutate, code):
        p = deepcopy(self.p)
        mutate(p)
        with self.assertRaisesRegex(ValueError, code):
            validate_plan(p)

    def test_gate_is_proposal_not_results(self):
        s = audit()
        self.assertEqual(s["result"], "PASS_MATCHED_BENCHMARK_DESIGN_AUDIT_ONLY")
        self.assertEqual(s["trained_models"], 0)
        self.assertEqual(s["independent_real_comparator_runs"], 0)
        self.assertFalse(s["H1_preregistered"])
        self.assertEqual(s["field_H1_confirmatory_samples"], 0)

    def test_strong_standard_comparators_required(self):
        check = validate_plan(self.p)
        self.assertEqual(check["required_conventional_baselines"], list(BASELINES))
        self.assertEqual(check["primary_feature"], CANDIDATE)
        self.assertFalse(check["actual_comparator_algorithms_run"])

    def test_per_system_brier_is_paired_not_pseudoreplication(self):
        r = toy_paired_brier(self.p)
        self.assertEqual(r["toy_test_systems"], 3)
        self.assertEqual(r["toy_eligible_systems"], 2)
        self.assertEqual(r["toy_zero_eligible_systems"], 1)
        self.assertEqual(r["method_mean_brier"][CANDIDATE], "1/4")
        self.assertEqual(r["toy_paired_gain_DP_minus_R1"], "0")
        self.assertIsNone(r["confidence_interval"])

    def test_no_loss_and_censored_are_not_false_negatives(self):
        p = deepcopy(self.p)
        p["systems"][-1]["episodes"] = [
            {"episode_id":"X1","status":"NOT_AT_RISK","weight":"1"},
            {"episode_id":"X2","status":"CENSORED","weight":"1"},
            {"episode_id":"X3","status":"UNKNOWN_RISK","weight":"1"},
        ]
        r = toy_paired_brier(p)
        self.assertEqual(r["toy_eligible_systems"], 2)
        self.assertEqual(r["toy_zero_eligible_systems"], 1)
        self.assertEqual(r["toy_censored_or_unknown_episodes_excluded"], 2)

    def test_more_episodes_do_not_make_more_independent_systems(self):
        p = deepcopy(self.p)
        extra = {"episode_id":"new","status":"RESTORED","weight":"1"}
        p["systems"][2]["episodes"].append(extra)
        r = toy_paired_brier(p)
        self.assertEqual(r["toy_eligible_systems"], 2)
        self.assertEqual(r["toy_test_systems"], 3)

    def test_duplicate_system_id_refused(self):
        self.deny(lambda p: p["systems"][3].update(system_id="TEST-A"),
                  "SYSTEM_ID_DUPLICATION")

    def test_leaked_structural_signatures_refused(self):
        self.deny(lambda p: p["systems"][3].update(
            source_signature="STRUCTURE-TRAIN-A"),
            "STRUCTURAL_GROUP_LEAKAGE")

    def test_future_case_feature_leak_refused(self):
        self.deny(lambda p: p["methods"][CANDIDATE].update(
            future_case_information_used=True), "PREFAULT_INFORMATION_LEAKAGE")

    def test_method_raw_information_digest_must_match(self):
        self.deny(lambda p: p["methods"][CANDIDATE].update(
            raw_input_digest="A DIFFERENT INPUT"), "METHOD_INPUT_INFORMATION_MISMATCH")

    def test_system_raw_information_must_match(self):
        self.deny(lambda p: p["systems"][2].update(
            pre_fault_digest="LATER-OBSERVATION"), "RAW_PRE_FAULT_INFORMATION_DRIFT")

    def test_primary_r1_feature_cannot_be_swapped_after_development(self):
        self.deny(lambda p: p.update(primary_feature="R10_READINESS"),
                  "PRIMARY_FEATURE_WAS_SWAPPED")

    def test_primary_conventional_dp_baseline_mandatory(self):
        self.deny(lambda p: p.update(primary_baseline="weak_constant"),
                  "STRONG_CONVENTIONAL_BASELINE_NOT_PRIMARY")

    def test_missing_cut_baseline_rejected(self):
        self.deny(lambda p: p["methods"].pop("physical_event_cut"),
                  "MISSING_OR_EXTRA_METHODS")

    def test_clairvoyant_full_model_not_fair_extra_primary_method(self):
        self.deny(lambda p: p["methods"].update(
            full_information_oracle=deepcopy(p["methods"][CANDIDATE])),
            "MISSING_OR_EXTRA_METHODS")

    def test_learner_capacity_cannot_be_different(self):
        self.deny(lambda p: p["methods"][CANDIDATE].update(capacity=100),
                  "MODEL_FAMILY_OR_CAPACITY_MISMATCH")

    def test_feature_cost_always_part_of_all_in_budget(self):
        self.deny(lambda p: p["computation"].update(feature_cost_included=False),
                  "COMPUTE_ACCOUNTING_INCOMPLETE")

    def test_large_feature_extraction_over_budget_rejected(self):
        self.deny(lambda p: p["methods"][CANDIDATE]
                  ["declared_work_units"].update(feature=100),
                  "DECLARED_ALL_IN_WORK_BUDGET_EXCEEDED")

    def test_negative_compute_ledger_rejected(self):
        self.deny(lambda p: p["methods"]["raw"]
                  ["declared_work_units"].update(predict=-1),
                  "MISSING_OR_INVALID_COST_LEDGER")

    def test_missing_timeout_abstention_contract_rejected(self):
        self.deny(lambda p: p["methods"][CANDIDATE].update(
            prediction_abstention_contract="ZERO_ON_TIMEOUT"),
            "TIMEOUT_ABSTENTION_UNSPECIFIED")

    def test_actual_algorithm_execution_claim_not_allowed_without_proof(self):
        self.deny(lambda p: p.update(actual_method_execution=True),
                  "SIMULATED_COST_CANNOT_MASQUERADE_AS_MEASURED_BENCHMARK")

    def test_claiming_actual_wall_measurement_is_refused(self):
        self.deny(lambda p: p.update(actual_wall_time_measured=True),
                  "SIMULATED_COST_CANNOT_MASQUERADE_AS_MEASURED_BENCHMARK")

    def test_preregistered_or_sealed_families_cannot_be_claimed(self):
        self.deny(lambda p: p.update(H1_status="PREREGISTERED"),
                  "H1_OR_HOLDOUT_MISREPRESENTED")
        self.deny(lambda p: p.update(sealed_test_families_opened=True),
                  "H1_OR_HOLDOUT_MISREPRESENTED")

    def test_wrong_endpoint_rejected(self):
        self.deny(lambda p: p.update(endpoint="NODE_ADMINISTRATIVE_FIX"),
                  "ENDPOINT_SUBSTITUTED")

    def test_changed_policy_id_rejected(self):
        self.deny(lambda p: p["systems"][2].update(policy_id="UNFAIR_POLICY"),
                  "POLICY_OR_PARTITION_DRIFT")

    def test_missing_forecast_for_one_arm_rejected(self):
        self.deny(lambda p: p["systems"][2]["predictions"].pop(CANDIDATE),
                  "MISSING_PAIRED_FORECAST")

    def test_out_of_range_forecast_rejected(self):
        self.deny(lambda p: p["systems"][2]["predictions"].update(
            **{CANDIDATE:"9/8"}), "probability outside")

    def test_same_system_duplicate_episode_rejected(self):
        self.deny(lambda p: p["systems"][2]["episodes"].append(
            deepcopy(p["systems"][2]["episodes"][0])),
            "DUPLICATE_EPISODE_WITHIN_SYSTEM")

    def test_all_zero_loss_eligibility_cannot_be_falsely_scored(self):
        p = deepcopy(self.p)
        for s in p["systems"]:
            if s["partition"] == "TEST":
                for e in s["episodes"]:
                    e["status"] = "NOT_AT_RISK"
        with self.assertRaisesRegex(ValueError, "NO_ELIGIBLE_SYSTEM_LEVEL_SCORE"):
            toy_paired_brier(p)


if __name__ == "__main__":
    unittest.main()
