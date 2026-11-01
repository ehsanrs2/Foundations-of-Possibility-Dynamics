"""R9 adversarial scope, inventory and deterministic bounded work tests."""
from dataclasses import replace
from fractions import Fraction
import json
import unittest

from experiments.p1_gate2 import Fault
from experiments.p1_r3_policy_rollout import Case
from experiments.p1_r7_silent_observation import (
    execute_observable, independent_observable_oracle,
)
from experiments.p1_r9_physical_controls import (
    MODES, WorkBudget, route_scope, fixture, static_pair,
    bounded_standard_reference, audit,
)


class R9PhysicsAndBudgetTests(unittest.TestCase):
    def test_exact_expected_independent_one_kit_half(self):
        t=fixture(mode="independent",kits=1)
        q=bounded_standard_reference(t,WorkBudget(16),verify=True)
        self.assertEqual(q["exact_conditional_restoration"],"1/2")
        self.assertEqual(q["independent_history_checks_outside_budget"],4)

    def test_two_kit_preparation_three_quarters(self):
        t=fixture(mode="independent",kits=2)
        q=bounded_standard_reference(t,WorkBudget(16),verify=True)
        self.assertEqual(q["exact_conditional_restoration"],"3/4")
        self.assertEqual(q["coverage_probability"],"1")

    def test_static_individual_backup_same_despite_real_stock_bottleneck(self):
        a=static_pair("independent",1)
        b=static_pair("independent",2)
        self.assertEqual(a["scoped_pair"],1)
        self.assertEqual(b["scoped_pair"],1)
        self.assertEqual(a["event_min_cut"],2)
        self.assertEqual(b["event_min_cut"],2)
        self.assertEqual(
            bounded_standard_reference(fixture(mode="independent",kits=1),
                                       WorkBudget(16))["exact_conditional_restoration"],
            "1/2",
        )
        self.assertEqual(
            bounded_standard_reference(fixture(mode="independent",kits=2),
                                       WorkBudget(16))["exact_conditional_restoration"],
            "3/4",
        )

    def test_deadline_bottleneck_one_preparation_tick(self):
        self.assertEqual(static_pair("independent",2)["scoped_pair"],1)
        t=fixture(mode="independent",kits=2,preparation_ticks=1)
        self.assertEqual(bounded_standard_reference(t,WorkBudget(12))[
            "exact_conditional_restoration"],"1/2")

    def test_alias_same_mechanism_is_not_independent(self):
        s=route_scope("alias")
        self.assertEqual(s.mechanisms["rule:serve_a"],
                         s.mechanisms["rule:serve_b"])
        self.assertEqual(s.incidence["rule:serve_a"],
                         s.incidence["rule:serve_b"])
        m=static_pair("alias",2)
        self.assertEqual(m["scoped_pair"],0)
        self.assertEqual(m["event_min_cut"],1)
        t=fixture(mode="alias",kits=2)
        self.assertEqual(bounded_standard_reference(t,WorkBudget(16))[
            "exact_conditional_restoration"],"1/2")

    def test_common_cause_prevents_event_disjoint_support(self):
        s=route_scope("common")
        self.assertNotEqual(s.mechanisms["rule:serve_a"],
                            s.mechanisms["rule:serve_b"])
        self.assertIn("event:common",s.incidence["rule:serve_a"])
        self.assertIn("event:common",s.incidence["rule:serve_b"])
        m=static_pair("common",2)
        self.assertEqual(m["scoped_pair"],0)
        self.assertEqual(m["event_min_cut"],1)
        t=fixture(mode="common",kits=2)
        q=bounded_standard_reference(t,WorkBudget(32),verify=True)
        self.assertEqual(q["exact_conditional_restoration"],"9/16")
        self.assertEqual(len(t.cases),8)

    def test_zero_kits_can_still_have_stipulated_faults_but_no_repair(self):
        m=static_pair("independent",0)
        self.assertEqual(m["scoped_pair"],0)
        self.assertEqual(m["event_min_cut"],0)
        t=fixture(mode="independent",kits=0)
        self.assertEqual(bounded_standard_reference(t,WorkBudget(16))[
            "exact_conditional_restoration"],"0")

    def test_all_cases_have_true_loss_and_stipulated_exact_weights(self):
        for mode in MODES:
            for kits in (0,1,2):
                t=fixture(mode=mode,kits=kits)
                self.assertEqual(sum((c.probability for c in t.cases),
                                     Fraction()),1)
                self.assertTrue(all("service" in c.fault.remove for c in t.cases))
                for c in t.cases:
                    o=execute_observable(t,c)
                    self.assertEqual(o.lost_at_fault,frozenset({"service"}))
                    self.assertIn(o.result("service"),(0,1))

    def test_independent_reference_agrees_on_every_designed_mode(self):
        for mode in MODES:
            t=fixture(mode=mode,kits=2)
            for c in t.cases:
                self.assertEqual(execute_observable(t,c),
                                 independent_observable_oracle(t,c))

    def test_no_work_budget_yields_only_wide_credible_interval(self):
        t=fixture(mode="independent",kits=2)
        q=bounded_standard_reference(t,WorkBudget(0))
        self.assertEqual(q["lower_conditional_restoration"],"0")
        self.assertEqual(q["upper_conditional_restoration"],"1")
        self.assertIsNone(q["exact_conditional_restoration"])
        self.assertEqual(q["scenarios_enumerated"],0)

    def test_budget_one_tick_cannot_fake_a_complete_episode(self):
        t=fixture(mode="independent",kits=2)
        q=bounded_standard_reference(t,WorkBudget(1))
        self.assertEqual(q["used_ticks"],0)
        self.assertEqual(q["coverage_probability"],"0")
        self.assertIsNone(q["exact_conditional_restoration"])

    def test_partial_work_bounds_contain_full_exact_result(self):
        for mode,kits,tau in (("independent",1,2),("independent",2,2),
                              ("alias",2,2),("common",2,2),
                              ("independent",2,1)):
            t=fixture(mode=mode,kits=kits,preparation_ticks=tau)
            total=(t.base.horizon+1)*len(t.cases)
            exact=bounded_standard_reference(t,WorkBudget(total))
            value=Fraction(exact["exact_conditional_restoration"])
            for budget in (0,1,t.base.horizon+1,2*(t.base.horizon+1),
                           total-1,total):
                result=bounded_standard_reference(t,WorkBudget(budget))
                self.assertLessEqual(result["used_ticks"],budget)
                self.assertLessEqual(
                    Fraction(result["lower_conditional_restoration"]),value)
                self.assertGreaterEqual(
                    Fraction(result["upper_conditional_restoration"]),value)
                self.assertEqual(result["exact_conditional_restoration"] is not None,
                                 result["coverage_probability"]=="1")

    def test_complete_budget_counts_one_unit_per_timeline_tick(self):
        t=fixture(mode="common",kits=2)
        q=bounded_standard_reference(t,WorkBudget(32))
        self.assertEqual(q["used_ticks"],32)
        self.assertEqual(q["scenarios_enumerated"],8)
        self.assertFalse(q["equal_CPU_WALLTIME_RAM_budget_claim"])

    def test_control_oracle_not_charged_or_claimed_equal_cpu(self):
        t=fixture(mode="independent",kits=2)
        a=bounded_standard_reference(t,WorkBudget(16),verify=False)
        b=bounded_standard_reference(t,WorkBudget(16),verify=True)
        self.assertEqual(a["used_ticks"],b["used_ticks"])
        self.assertEqual(a["independent_history_checks_outside_budget"],0)
        self.assertEqual(b["independent_history_checks_outside_budget"],4)

    def test_hidden_case_name_does_not_change_actual_policy_trace(self):
        t=fixture(mode="independent",kits=2)
        original=t.cases[1]
        renamed=replace(original,name="blind_name")
        altered=replace(t,cases=tuple(
            renamed if c==original else c for c in t.cases))
        self.assertEqual(execute_observable(t,original).steps,
                         execute_observable(altered,renamed).steps)

    def test_invalid_physical_identity_and_resource_inputs_fail(self):
        with self.assertRaises(ValueError):
            route_scope("fabricated")
        for data in ({"mode":"wrong","kits":1},
                     {"mode":"independent","kits":True},
                     {"mode":"independent","kits":3},
                     {"mode":"alias","kits":1,"preparation_ticks":0}):
            with self.assertRaises(ValueError):
                fixture(**data)
        for budget in (-1,True,1.0):
            with self.assertRaises(ValueError):
                WorkBudget(budget)

    def test_reject_bounded_target_if_actual_loss_not_guaranteed(self):
        t=fixture(mode="independent",kits=2)
        first=replace(t.cases[0],fault=replace(t.cases[0].fault,
                                                 remove=frozenset()))
        changed=replace(t,cases=(first,)+t.cases[1:])
        with self.assertRaises(ValueError):
            bounded_standard_reference(changed,WorkBudget(16))

    def test_audit_has_only_predeclared_cases_and_no_h1(self):
        result=audit()
        self.assertEqual(result["toy_conditions"],6)
        self.assertEqual(result["R7_independent_full_trace_checks"],28)
        self.assertEqual(result["test_family_generators_called"],0)
        self.assertEqual(result["observed_real_physical_failures"],0)
        self.assertEqual(result["confirmatory_H1_samples"],0)
        self.assertFalse(result["identical_computation_budget_across_algorithms"])
        self.assertEqual(result["result"],"PASS")

    def test_r9_report_is_deterministically_reproducible(self):
        self.assertEqual(audit(),audit())


if __name__=="__main__":
    unittest.main()
