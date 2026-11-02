"""R11: unknown event-time policy information and identical prediction tasks."""
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import json
import sys
import unittest

from experiments.p1_r7_silent_observation import execute_observable
from experiments.p1_r8_dev_predictive_baselines import _solve_ridge
from experiments.p1_r9_physical_controls import fixture, MODES
from experiments.p1_r10_executable_backup import ProcessCaps
from experiments.p1_r11_unknown_time_prediction import (
    TRAIN_PRIORS, TUNE_PRIORS, METHODS, DEFAULT_CAPS,
    unknown_time_trial, exact_model_target, readiness_prior,
    make_setting, compare, capped_compare, audit, deterministic_archive,
)


class R11DevelopmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not sys.platform.startswith("linux"):
            raise unittest.SkipTest("R11 resource-bound workers require Linux")
        cls.result=audit()

    def test_two_possible_times_but_no_future_time_policy_input(self):
        t=unknown_time_trial("independent",2,Fraction(1,2))
        self.assertEqual({c.fault.tick for c in t.cases},{1,2})
        self.assertEqual(sum((c.probability for c in t.cases),Fraction()),1)
        self.assertEqual({c.name.split("_",1)[0] for c in t.cases},
                         {"tau1","tau2"})
        self.assertEqual(t.base.horizon,3)

    def test_all_stipulated_scenarios_really_lose_initial_service(self):
        for mode in MODES:
            for kits in (0,1,2):
                t=unknown_time_trial(mode,kits,Fraction(1,4))
                for case in t.cases:
                    outcome=execute_observable(t,case)
                    self.assertEqual(outcome.lost_at_fault,
                                     frozenset({"service"}))
                    self.assertIn(outcome.result("service"),(0,1))

    def test_early_vs_late_shocks_have_same_pre_event_actions(self):
        t=unknown_time_trial("independent",2,Fraction(1,2))
        a=next(c for c in t.cases if c.name=="tau1_a0_b0_common0")
        b=next(c for c in t.cases if c.name=="tau2_a0_b0_common0")
        self.assertEqual(execute_observable(t,a).steps[0],
                         execute_observable(t,b).steps[0])
        self.assertEqual(execute_observable(t,a).steps[0].action,
                         "prepare_a")

    def test_case_name_relabeling_cannot_change_trajectory(self):
        t=unknown_time_trial("independent",2,Fraction(1,2))
        original=t.cases[0]
        changed=replace(original,name="invisible_label")
        q=replace(t,cases=tuple(changed if c==original else c
                                for c in t.cases))
        self.assertEqual(execute_observable(t,original).steps,
                         execute_observable(q,changed).steps)

    def test_exact_risk_mixture_independent_two_kits(self):
        for alpha in TRAIN_PRIORS+TUNE_PRIORS:
            p,checks=exact_model_target(
                unknown_time_trial("independent",2,alpha),verify=True)
            self.assertEqual(p, Fraction(3,4)-alpha*Fraction(1,4))
            self.assertGreater(checks,0)

    def test_one_kit_stays_half_across_time_risks(self):
        for alpha in TRAIN_PRIORS+TUNE_PRIORS:
            p,_=exact_model_target(unknown_time_trial(
                "independent",1,alpha))
            self.assertEqual(p,Fraction(1,2))

    def test_zero_kits_stay_zero_without_faked_restoration(self):
        for alpha in TRAIN_PRIORS+TUNE_PRIORS:
            p,_=exact_model_target(unknown_time_trial(
                "independent",0,alpha))
            self.assertEqual(p,0)

    def test_alias_same_mechanism_never_becomes_independent(self):
        for alpha in TRAIN_PRIORS+TUNE_PRIORS:
            self.assertEqual(readiness_prior(
                "alias",2,alpha,implementation="standard_dp"),0)

    def test_common_cause_never_becomes_independent(self):
        self.assertEqual(readiness_prior(
            "common",2,Fraction(1,4),implementation="standard_dp"),0)

    def test_standard_and_independent_readiness_match_every_prior(self):
        for mode in MODES:
            for kits in (0,1,2):
                for alpha in TRAIN_PRIORS+TUNE_PRIORS:
                    x=readiness_prior(mode,kits,alpha,
                                      implementation="standard_dp")
                    y=readiness_prior(mode,kits,alpha,
                                      implementation="independent_history")
                    self.assertEqual(x,y)

    def test_readiness_prior_no_realized_future_information(self):
        for alpha in TRAIN_PRIORS+TUNE_PRIORS:
            expected=(1-alpha)
            self.assertEqual(readiness_prior(
                "independent",2,alpha,implementation="standard_dp"),expected)

    def test_training_and_tuning_are_repeated_parameter_structures(self):
        p=self.result
        self.assertEqual(p["unique_physical_structure_configs"],9)
        self.assertEqual(p["train_parameter_settings"],27)
        self.assertEqual(p["tune_parameter_settings"],18)
        self.assertTrue(p["same_structure_repeated_across_train_tune"])
        self.assertEqual(p["independent_heldout_systems"],0)

    def test_no_feature_uses_future_case_identity(self):
        a,_=make_setting("independent",2,Fraction(1,4),"raw")
        b,_=make_setting("independent",2,Fraction(1,4),"standard_dp")
        self.assertEqual(a.x,b.x)
        self.assertEqual(a.target,b.target)
        self.assertIsNone(a.candidate)
        self.assertEqual(b.candidate,Fraction(3,4))

    def test_same_prediction_task_for_all_three_arms(self):
        bymethod=self.result["results"]
        keys=[(c["mode"],c["kits"],c["early_probability"])
              for c in bymethod["raw"]["prediction"]["tune_records"]]
        for method in METHODS:
            p=bymethod[method]["prediction"]
            self.assertEqual(p["train_parameter_settings"],27)
            self.assertEqual(p["tune_parameter_settings"],18)
            self.assertEqual(keys,[(c["mode"],c["kits"],c["early_probability"])
                                   for c in p["tune_records"]])
            self.assertEqual(p["confirmatory_H1_samples"],0)

    def test_two_conventional_implementations_produce_identical_forecasts(self):
        result=self.result["results"]
        dp=result["standard_dp"]["prediction"]
        independent=result["independent_history"]["prediction"]
        self.assertEqual(dp["mean_expected_brier"],
                         independent["mean_expected_brier"])
        self.assertEqual(dp["tune_records"],independent["tune_records"])
        self.assertTrue(self.result[
            "standard_DP_equals_independent_history_feature"])

    def test_scores_cannot_beat_full_model_ideal_expected_brier(self):
        for method in METHODS:
            for c in self.result["results"][method]["prediction"]["tune_records"]:
                self.assertGreaterEqual(
                    c["conditional_expected_brier"]+1e-10,
                    c["ideal_model_brier"])

    def test_ridge_penalty_and_risk_prior_split_fixed(self):
        for m in METHODS:
            p=self.result["results"][m]["prediction"]
            self.assertEqual(p["fixed_ridge_penalty"],1.0)
            self.assertEqual(p["train_hazard_priors"],["0","1/2","1"])
            self.assertEqual(p["tune_hazard_priors"],["1/4","3/4"])

    def test_enforced_process_caps_apply_to_all_equal_objectives(self):
        self.assertTrue(self.result["same_enforced_process_caps"])
        self.assertEqual(self.result["process_caps"],{
            "wall_seconds":5.0,"cpu_seconds":5,
            "virtual_address_space_mb":256})
        for method in METHODS:
            run=self.result["results"][method]
            self.assertEqual(run["status"],"PASS")
            self.assertGreater(run["worker_peak_rss_kib"],0)
            self.assertGreaterEqual(run["worker_cpu_ms"],0)
            self.assertGreaterEqual(run["wall_ms"],0)

    def test_exact_ground_truth_oracles_counted_outside_fit_caps(self):
        self.assertGreater(self.result["full_history_oracle_comparisons"],0)
        for m in METHODS:
            self.assertEqual(self.result["results"][m]["prediction"][
                "full_history_oracle_comparisons"],0)

    def test_unrecognized_inputs_are_rejected(self):
        for kw in ({"mode":"not_real","kits":2,"early_probability":Fraction(1,2)},
                   {"mode":"independent","kits":True,"early_probability":Fraction(1,2)},
                   {"mode":"independent","kits":2,"early_probability":Fraction(3,2)},
                   {"mode":"independent","kits":2,"early_probability":0.5}):
            with self.assertRaises(ValueError):
                unknown_time_trial(**kw)
        with self.assertRaises(ValueError):
            readiness_prior("independent",2,Fraction(1,2),implementation="fake")
        with self.assertRaises(ValueError):
            compare("fake")
        with self.assertRaises(ValueError):
            capped_compare("fake")

    def test_outcome_is_scientific_development_not_h1(self):
        p=self.result
        self.assertIn("NOT_H1",p["classification"])
        self.assertFalse(p["H1_confirmatory_test"])
        self.assertFalse(p["physical_event_calibration"])
        self.assertTrue(p["R8_negative_archive_unchanged"])

    def test_runtime_metrics_excluded_from_stable_archive(self):
        stable=deterministic_archive(self.result)
        for value in stable["results"].values():
            for f in ("wall_ms","worker_cpu_ms","worker_peak_rss_kib"):
                self.assertNotIn(f,value)
            self.assertEqual(value["status"],"PASS")

    def test_archived_complete_R11_developer_result_matches(self):
        archive=Path(__file__).parents[1]/"research"/(
            "R11-unknown-time-prediction-results-20261102.json")
        self.assertEqual(
            deterministic_archive(self.result),
            json.loads(archive.read_text(encoding="utf-8")))

    def test_original_R8_zero_gain_archive_preserved(self):
        archive=Path(__file__).parents[1]/"research"/(
            "R8-development-summary-seed20261101.json")
        val=json.loads(archive.read_text(encoding="utf-8"))
        self.assertTrue(val["r1_non_discriminating"])
        self.assertEqual(val["mean_paired_improvement_baseline_minus_augmented"],0)

    def test_identical_synthetic_setting_determinism(self):
        a=compare("raw")
        b=compare("raw")
        self.assertEqual(a,b)


if __name__=="__main__":
    unittest.main()
