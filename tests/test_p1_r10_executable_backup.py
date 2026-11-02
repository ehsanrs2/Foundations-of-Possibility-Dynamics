"""R10: jointly executable backup, standard reachability parity and process caps."""
from dataclasses import replace
from fractions import Fraction
import json
import os
from pathlib import Path
import sys
import unittest

from experiments.p1_r9_physical_controls import fixture, static_pair, WorkBudget
from experiments.p1_r10_executable_backup import (
    CONDITIONS, MAX_PREFIX_STATES, ProcessCaps, audit,
    fixed_policy_preparation, independent_prefix_history_oracle,
    limited_process, physical_event_independent, reproducible_summary,
    standard_joint_state_dp, worker_operation,
)


class R10JointPreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not sys.platform.startswith("linux"):
            raise unittest.SkipTest("R10 hard resource limit tests require Linux")
        cls.result = audit()

    def test_six_predeclared_toys_only(self):
        self.assertEqual(len(CONDITIONS),6)
        self.assertEqual(self.result["predeclared_toy_systems"],6)
        self.assertEqual(self.result["result"],"PASS")
        self.assertEqual(self.result["R9_reference_full_traces"],28)

    def test_independent_two_kits_two_ticks_are_joint_ready(self):
        t=fixture(mode="independent",kits=2,preparation_ticks=2)
        out=standard_joint_state_dp(t,"independent")
        self.assertEqual(out["scoped_joint_ready_indicator"],1)
        self.assertEqual(out["executable_prefix_witness"],
                         ["prepare_a","prepare_b"])
        self.assertGreaterEqual(out["action_feasibility_probes"],1)

    def test_one_kit_individual_pair_true_joint_pair_false(self):
        t=fixture(mode="independent",kits=1,preparation_ticks=2)
        self.assertEqual(static_pair("independent",1)["scoped_pair"],1)
        self.assertEqual(standard_joint_state_dp(t,"independent")[
            "scoped_joint_ready_indicator"],0)
        self.assertFalse(standard_joint_state_dp(t,"independent")[
            "jointly_prepared_by_some_prefix"])

    def test_short_window_two_kits_individual_pair_true_joint_false(self):
        t=fixture(mode="independent",kits=2,preparation_ticks=1)
        self.assertEqual(static_pair("independent",2)["scoped_pair"],1)
        self.assertEqual(standard_joint_state_dp(t,"independent")[
            "scoped_joint_ready_indicator"],0)

    def test_alias_disjointness_fail_closed_despite_joint_readiness(self):
        t=fixture(mode="alias",kits=2,preparation_ticks=2)
        out=standard_joint_state_dp(t,"alias")
        self.assertTrue(out["jointly_prepared_by_some_prefix"])
        self.assertFalse(out["physical_event_independent"])
        self.assertEqual(out["scoped_joint_ready_indicator"],0)
        self.assertIsNone(out["executable_prefix_witness"])

    def test_common_cause_is_not_event_disjoint_even_with_two_kits(self):
        t=fixture(mode="common",kits=2,preparation_ticks=2)
        out=standard_joint_state_dp(t,"common")
        self.assertTrue(out["jointly_prepared_by_some_prefix"])
        self.assertFalse(out["physical_event_independent"])
        self.assertEqual(out["scoped_joint_ready_indicator"],0)

    def test_no_kits_no_joint_preparation(self):
        t=fixture(mode="independent",kits=0)
        self.assertFalse(standard_joint_state_dp(t,"independent")[
            "jointly_prepared_by_some_prefix"])

    def test_scope_outcome_mapping_is_predeclared_not_named_path_count(self):
        self.assertTrue(physical_event_independent("independent"))
        self.assertFalse(physical_event_independent("alias"))
        self.assertFalse(physical_event_independent("common"))
        with self.assertRaises(ValueError):
            physical_event_independent("unknown")

    def test_dp_and_independent_history_oracle_match_every_toy(self):
        for _label,mode,kits,tau,expected in CONDITIONS:
            t=fixture(mode=mode,kits=kits,preparation_ticks=tau)
            dp=standard_joint_state_dp(t,mode)
            dfs=independent_prefix_history_oracle(t,mode)
            self.assertEqual(dp["scoped_joint_ready_indicator"],expected)
            self.assertEqual(dp["scoped_joint_ready_indicator"],
                             dfs["scoped_joint_ready_indicator"])
            self.assertEqual(dp["executable_prefix_witness"],
                             dfs["executable_prefix_witness"])
            self.assertEqual(dp["jointly_prepared_by_some_prefix"],
                             dfs["jointly_prepared_by_some_prefix"])

    def test_prefix_does_not_depend_on_realized_future_scenario_identity(self):
        t=fixture(mode="independent",kits=2)
        reverse=replace(t,cases=tuple(
            replace(case,name="blind_"+case.name)
            for case in reversed(t.cases)))
        self.assertEqual(standard_joint_state_dp(t,"independent"),
                         standard_joint_state_dp(reverse,"independent"))
        self.assertEqual(fixed_policy_preparation(t,"independent"),
                         fixed_policy_preparation(reverse,"independent"))

    def test_prefix_does_not_depend_on_future_disabled_actions(self):
        t=fixture(mode="independent",kits=2)
        altered=replace(t,cases=tuple(replace(
            case,fault=replace(case.fault,
                               disable=frozenset({"serve_a","serve_b"})))
            for case in t.cases))
        self.assertEqual(standard_joint_state_dp(t,"independent"),
                         standard_joint_state_dp(altered,"independent"))

    def test_prefix_dp_independent_of_action_tuple_order(self):
        t=fixture(mode="independent",kits=2)
        reordered=replace(t,base=replace(
            t.base,actions=tuple(reversed(t.base.actions))))
        self.assertEqual(standard_joint_state_dp(t,"independent")[
            "scoped_joint_ready_indicator"],
            standard_joint_state_dp(reordered,"independent")[
            "scoped_joint_ready_indicator"])
        self.assertEqual(standard_joint_state_dp(t,"independent")[
            "executable_prefix_witness"],
            standard_joint_state_dp(reordered,"independent")[
            "executable_prefix_witness"])

    def test_fixed_policy_ready_is_distinguished_from_existential(self):
        for _label,mode,kits,tau,expected in CONDITIONS:
            t=fixture(mode=mode,kits=kits,preparation_ticks=tau)
            fp=fixed_policy_preparation(t,mode)
            existential=standard_joint_state_dp(t,mode)
            self.assertEqual(fp["scoped_ready_for_fixed_policy"],expected)
            self.assertEqual(existential["scoped_joint_ready_indicator"],
                             expected)
            self.assertEqual(len(fp["fixed_prefix"]),tau)

    def test_executable_prefix_does_not_predict_exact_restoration(self):
        independent_two=next(x for x in self.result["conditions"]
                             if x["label"]=="separate_two_kits")
        one=next(x for x in self.result["conditions"]
                 if x["label"]=="separate_one_kit")
        self.assertEqual(independent_two["joint_executable_prefix_backup"],1)
        self.assertEqual(independent_two["strict_restoration_known_model"],"3/4")
        self.assertEqual(one["joint_executable_prefix_backup"],0)
        self.assertEqual(one["strict_restoration_known_model"],"1/2")

    def test_shared_rss_cpu_and_wall_caps_enforced_per_child(self):
        caps=self.result["uniform_caps"]
        self.assertEqual(caps,{"wall_seconds":5.0,"cpu_seconds":5,
                               "address_space_mb":256})
        self.assertTrue(self.result["all_methods_have_same_resource_caps"])
        self.assertFalse(self.result["equal_work_or_equal_predictive_objective"])
        for item in self.result["conditions"]:
            for mode,run in item["capped_process_measurements"].items():
                self.assertEqual(run["method"],mode)
                self.assertEqual(run["status"],"PASS")
                self.assertEqual(run["address_space_limit_mb"],256)
                self.assertEqual(run["cpu_limit_seconds"],5)
                self.assertEqual(run["wall_limit_seconds"],5.0)
                self.assertGreaterEqual(run["worker_cpu_ms"],0)
                self.assertGreater(run["worker_peak_rss_kib"],0)

    def test_all_worker_methods_use_same_unaltered_fixture_inputs(self):
        for _name,mode,kits,tau,_expected in CONDITIONS:
            self.assertEqual(
                worker_operation("static_r1",mode,kits,tau)["result"],
                static_pair(mode,kits))
            self.assertEqual(
                worker_operation("joint_state",mode,kits,tau)["result"],
                standard_joint_state_dp(fixture(mode=mode,kits=kits,
                                                 preparation_ticks=tau),mode))

    def test_unknown_worker_and_invalid_caps_refused(self):
        with self.assertRaises(ValueError):
            worker_operation("unknown","independent",1,2)
        for kw in ({"wall_seconds":0.0},{"cpu_seconds":0},
                   {"address_space_mb":64},{"cpu_seconds":True},
                   {"wall_seconds":61},{"address_space_mb":True}):
            with self.assertRaises(ValueError):
                ProcessCaps(**kw)
        with self.assertRaises(ValueError):
            limited_process("unknown","independent",2,2,ProcessCaps())

    def test_work_output_never_becomes_h1_inference(self):
        data=self.result
        self.assertFalse(data["H1_training_or_test"])
        self.assertEqual(data["sealed_family_generator_calls"],0)
        self.assertTrue(data["physical_identities_assumed_not_field_validated"])
        self.assertTrue(data["known_fault_boundary_in_toy_fixtures"])
        self.assertFalse(data["equal_work_or_equal_predictive_objective"])
        self.assertIn("NOT_H1",data["classification"])

    def test_deterministic_archive_omits_runtime_not_scientific_results(self):
        s=reproducible_summary(self.result)
        for row in s["conditions"]:
            for run in row["capped_process_measurements"].values():
                self.assertNotIn("worker_peak_rss_kib",run)
                self.assertNotIn("all_in_worker_wall_ms",run)
                self.assertNotIn("worker_cpu_ms",run)
                self.assertEqual(run["status"],"PASS")
        self.assertEqual(s["predeclared_toy_systems"],6)

    def test_archived_complete_R10_scientific_result_matches(self):
        archive=Path(__file__).parents[1] / "research" / (
            "R10-joint-executable-results-20261102.json")
        self.assertEqual(
            reproducible_summary(self.result),
            json.loads(archive.read_text(encoding="utf-8")))

    def test_archived_R9_negative_result_remains_unchanged(self):
        root=Path(__file__).parents[1] / "research"
        old=json.loads((root/"R8-development-summary-seed20261101.json").
                       read_text(encoding="utf-8"))
        self.assertEqual(old["mean_paired_improvement_baseline_minus_augmented"],0)
        self.assertTrue(old["r1_non_discriminating"])
        self.assertFalse(self.result["H1_training_or_test"])


if __name__=="__main__":
    unittest.main()
