"""R12 out-of-grammar synthetic transfer and known-model negative controls."""
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import json
import sys
import unittest

from experiments.p1_r7_silent_observation import execute_observable
from experiments.p1_r10_executable_backup import ProcessCaps
from experiments.p1_r12_cross_grammar_transfer import (
    ALL_FAMILIES,TRAIN_FAMILIES,TUNE_FAMILIES,TRAIN_PRIORS,TUNE_PRIORS,
    METHODS,CAPS,MAX_STATES,
    family_trial,structure_signature,conventional_joint_dp,
    independent_joint_history,readiness,system_record,evaluate,
    capped_run,audit,stable_archive,
)


class R12TransferChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not sys.platform.startswith("linux"):
            raise unittest.SkipTest("R12 hard process-cap tests require Linux")
        cls.data=audit()

    def test_grammars_are_not_sealed_or_R4_h1_generators(self):
        self.assertEqual(TRAIN_FAMILIES,("direct",))
        self.assertEqual(TUNE_FAMILIES,("shared_stage","asymmetric_stage"))
        self.assertEqual(set(TRAIN_FAMILIES)&set(TUNE_FAMILIES),set())
        self.assertNotIn("spatial_lattice",ALL_FAMILIES)
        self.assertNotIn("hierarchical_common_cause",ALL_FAMILIES)

    def test_new_structural_grammars_distinct_precondition_topology(self):
        t=family_trial("direct","independent",2,Fraction(1,2))
        x=family_trial("shared_stage","independent",2,Fraction(1,2))
        y=family_trial("asymmetric_stage","independent",2,Fraction(1,2))
        self.assertEqual(len(t.base.actions),4)
        self.assertEqual(len(x.base.actions),5)
        self.assertEqual(len(y.base.actions),5)
        xa=next(a for a in x.base.actions if a.name=="prepare_a")
        ya=next(a for a in y.base.actions if a.name=="prepare_a")
        yb=next(a for a in y.base.actions if a.name=="prepare_b")
        self.assertEqual(xa.requires,frozenset({"armed"}))
        self.assertEqual(ya.requires,frozenset({"port_a"}))
        self.assertEqual(yb.requires,frozenset({"base"}))
        self.assertNotEqual(structure_signature(t,"independent"),
                            structure_signature(x,"independent"))
        self.assertNotEqual(structure_signature(x,"independent"),
                            structure_signature(y,"independent"))

    def test_no_duplicate_train_tune_structural_signatures(self):
        data=evaluate("raw")
        self.assertEqual(data["train_unique_graph_signatures"],9)
        self.assertEqual(data["tune_unique_graph_signatures"],18)
        self.assertEqual(data["graph_signature_overlap"],0)
        self.assertEqual(data["train_hazard_parameter_rows"],27)
        self.assertEqual(data["tune_hazard_parameter_rows"],36)

    def test_time_hazards_are_unknown_to_executing_policy(self):
        t=family_trial("shared_stage","independent",2,Fraction(1,2))
        a=next(c for c in t.cases if c.name=="tau2_a0_b0_common0")
        b=next(c for c in t.cases if c.name=="tau3_a0_b0_common0")
        self.assertEqual(execute_observable(t,a).steps[:2],
                         execute_observable(t,b).steps[:2])
        self.assertEqual(execute_observable(t,a).steps[0].action,"unlock")

    def test_no_anticipation_of_hidden_future_event_identity(self):
        t=family_trial("asymmetric_stage","common",2,Fraction(1,4))
        original=t.cases[0]
        renamed=replace(original,name="blind")
        changed=replace(t,cases=tuple(
            renamed if z==original else z for z in t.cases))
        self.assertEqual(execute_observable(t,original).steps,
                         execute_observable(changed,renamed).steps)

    def test_one_and_only_one_real_service_loss_per_case(self):
        for family in ALL_FAMILIES:
            for mode in ("independent","alias","common"):
                t=family_trial(family,mode,2,Fraction(1,4))
                self.assertEqual(sum((c.probability for c in t.cases),
                                     Fraction()),1)
                self.assertTrue(all(execute_observable(t,c).lost_at_fault
                                    ==frozenset({"service"}) for c in t.cases))
                self.assertEqual(t.base.horizon,4)

    def test_good_joint_preparation_requires_two_stock_and_three_ticks_when_staged(self):
        for family in TUNE_FAMILIES:
            t=family_trial(family,"independent",2,Fraction(1,2))
            self.assertEqual(conventional_joint_dp(t,"independent",2),0)
            self.assertEqual(conventional_joint_dp(t,"independent",3),1)
            self.assertEqual(readiness(family,"independent",2,Fraction(1,4),
                                       "state_dp"),Fraction(3,4))

    def test_direct_preparation_needs_two_ticks_and_two_kits(self):
        t=family_trial("direct","independent",2,Fraction(1,2))
        self.assertEqual(conventional_joint_dp(t,"independent",2),1)
        self.assertEqual(conventional_joint_dp(t,"independent",3),1)
        self.assertEqual(readiness("direct","independent",2,Fraction(1,4),
                                   "state_dp"),1)

    def test_alias_and_common_cause_always_fail_physical_pair_independence(self):
        for family in ALL_FAMILIES:
            for mode in ("alias","common"):
                t=family_trial(family,mode,2,Fraction(1,4))
                for tau in (2,3):
                    self.assertEqual(conventional_joint_dp(t,mode,tau),0)
                    self.assertEqual(independent_joint_history(t,mode,tau),0)

    def test_all_DP_DFS_structure_times_agree(self):
        self.assertEqual(self.data["structural_DP_DFS_checks"],54)

    def test_distinct_training_family_and_tuning_family_is_not_external_validity(self):
        self.assertEqual(self.data["train_unique_synthetic_structures"],9)
        self.assertEqual(self.data["tune_unique_synthetic_structures"],18)
        self.assertEqual(self.data["graph_signature_overlap"],0)
        self.assertFalse(self.data["external_physical_data"])

    def test_two_route_algorithms_produce_identical_predictions(self):
        a=self.data["runs"]["state_dp"]["result"]
        b=self.data["runs"]["history"]["result"]
        self.assertEqual(a["tune_results"],b["tune_results"])
        self.assertEqual(a["mean_expected_brier"],b["mean_expected_brier"])

    def test_exact_standard_full_model_oracle_is_optimal_under_synthetic_target(self):
        m=self.data["runs"]["known_model"]["result"]
        self.assertEqual(m["mean_expected_brier"],m["mean_ideal_brier"])
        for method in METHODS:
            b=self.data["runs"][method]["result"]
            self.assertGreaterEqual(b["mean_expected_brier"]+1e-9,
                                    m["mean_expected_brier"])

    def test_all_models_predict_same_targets_on_same_tune_structures(self):
        reference=self.data["runs"]["raw"]["result"]["tune_results"]
        expected=[(r["family"],r["mode"],r["kits"],r["early_prior"],
                   r["model_target"],r["structure_sha256"]) for r in reference]
        for method in METHODS:
            v=self.data["runs"][method]["result"]["tune_results"]
            self.assertEqual(
                [(r["family"],r["mode"],r["kits"],r["early_prior"],
                  r["model_target"],r["structure_sha256"]) for r in v],
                expected)

    def test_worker_budgets_same_and_enforced_for_same_prediction_task(self):
        self.assertTrue(self.data["same_enforced_process_caps"])
        self.assertEqual(self.data["process_caps"],{
            "wall_seconds":10.0,"cpu_seconds":10,
            "virtual_address_space_mb":256})
        for m in METHODS:
            run=self.data["runs"][m]
            self.assertEqual(run["status"],"PASS")
            self.assertGreater(run["worker_peak_rss_kib"],0)
            self.assertGreaterEqual(run["worker_cpu_ms"],0)
            self.assertGreaterEqual(run["worker_wall_ms"],0)

    def test_no_equal_actual_work_or_dimensionality_claim(self):
        self.assertFalse(self.data["same_actual_compute_or_model_dimension"])
        self.assertTrue(self.data["known_model_is_oracle_not_fitted"])

    def test_oracle_history_validation_separate_from_work_budget(self):
        self.assertGreater(self.data["R7_independent_history_checks"],0)
        self.assertEqual(self.data["runs"]["raw"]["result"]["full_history_checks"],0)

    def test_future_failure_probability_not_learned_from_tune_labels(self):
        raw,_=system_record("asymmetric_stage","independent",2,
                            Fraction(1,4),"raw")
        dp,_=system_record("asymmetric_stage","independent",2,
                           Fraction(1,4),"state_dp")
        self.assertEqual(raw.x,dp.x)
        self.assertEqual(raw.outcome,dp.outcome)
        self.assertEqual(dp.engineered,0.75)
        self.assertEqual(raw.engineered,0.0)

    def test_reject_heldout_and_invalid_inputs_without_leak(self):
        for family in ("spatial_lattice","hierarchical_common_cause","new"):
            with self.assertRaises(ValueError):
                family_trial(family,"independent",2,Fraction(1,2))
        for kwargs in (
            {"family":"direct","mode":"wrong","kits":2,"early":Fraction(1,2)},
            {"family":"direct","mode":"independent","kits":True,"early":Fraction(1,2)},
            {"family":"direct","mode":"independent","kits":2,"early":1.5},
        ):
            with self.assertRaises(ValueError):
                family_trial(**kwargs)
        with self.assertRaises(ValueError):
            evaluate("fake")
        with self.assertRaises(ValueError):
            capped_run("fake")

    def test_same_caps_do_not_mean_externally_independent_results(self):
        self.assertFalse(self.data["external_physical_data"])
        self.assertTrue(self.data["R8_unchanged"])
        self.assertEqual(self.data["sealed_H1_test_samples"],0)
        self.assertIn("NOT_H1",self.data["classification"])

    def test_stable_output_strips_only_environment_performance_fields(self):
        archive=stable_archive(self.data)
        for worker in archive["runs"].values():
            for field in ("worker_wall_ms","worker_cpu_ms",
                          "worker_peak_rss_kib"):
                self.assertNotIn(field,worker)
            self.assertEqual(worker["status"],"PASS")

    def test_archived_full_R12_scientific_comparison_is_reproduced(self):
        source=Path(__file__).parents[1]/"research"/(
            "R12-cross-grammar-results-20261102.json")
        self.assertEqual(
            stable_archive(self.data),
            json.loads(source.read_text(encoding="utf-8")))

    def test_archived_R8_development_failure_unmodified(self):
        path=Path(__file__).parents[1]/"research"/(
            "R8-development-summary-seed20261101.json")
        r=json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(r["r1_non_discriminating"])
        self.assertEqual(r["mean_paired_improvement_baseline_minus_augmented"],0)

    def test_repeated_synthetic_run_predictions_are_deterministic(self):
        self.assertEqual(evaluate("raw"),evaluate("raw"))


if __name__=="__main__":
    unittest.main()
