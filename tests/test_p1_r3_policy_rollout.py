"""R3 non-anticipative same-history strict-loss checks; no H1 statistics."""
from dataclasses import replace
from fractions import Fraction
import json
import unittest

from experiments.p1_gate2 import Action, Fault, Model
from experiments.p1_r3_policy_rollout import (
    Case, FixedPolicy, Trial, execute, independent_history_oracle,
    loss_conditioned_probability, demonstrator, verify, audit,
)


class R3RolloutTests(unittest.TestCase):
    def check(self, trial):
        self.assertEqual(verify(trial),len(trial.cases))
        for case in trial.cases:
            self.assertEqual(execute(trial,case),
                             independent_history_oracle(trial,case))

    def test_actual_loss_then_restoration_on_one_trajectory(self):
        trial=demonstrator()
        self.check(trial)
        v=execute(trial,trial.cases[0])
        self.assertEqual(v.held_before_fault,frozenset({"service"}))
        self.assertEqual(v.lost_at_fault,frozenset({"service"}))
        self.assertEqual(v.first_restored_at,(("service",2),))
        self.assertEqual(v.result("service"),1)

    def test_late_shock_at_horizon_is_loss_without_restoration(self):
        trial=demonstrator()
        v=execute(trial,trial.cases[1])
        self.assertEqual(v.lost_at_fault,frozenset({"service"}))
        self.assertEqual(v.result("service"),0)
        self.assertEqual(v.steps[-1].action,None)

    def test_no_actual_loss_is_undefined_not_failure(self):
        trial=demonstrator()
        v=execute(trial,trial.cases[2])
        self.assertEqual(v.lost_at_fault,frozenset())
        self.assertEqual(v.retained_at_fault,frozenset({"service"}))
        self.assertIsNone(v.result("service"))
        self.assertEqual(loss_conditioned_probability(trial)["service"],
                         {"eligible_probability":"2/3","restoration_given_loss":"1/2"})

    def test_goal_absent_before_shock_is_not_strict_restoration(self):
        trial=demonstrator()
        base=replace(trial.base,initial=trial.base.initial-{"service"})
        changed=replace(trial,base=base)
        self.check(changed)
        early=execute(changed,changed.cases[0])
        self.assertIsNone(early.result("service"))  # never held before t=1
        # A later fault can remove a goal CREATED before its own shock.
        late=execute(changed,changed.cases[1])
        self.assertIn("service",late.held_before_fault)
        self.assertEqual(late.result("service"),0)

    def test_future_fault_times_share_preshock_trace(self):
        trial=demonstrator()
        early=execute(trial,trial.cases[0])
        late=execute(trial,trial.cases[1])
        self.assertEqual(early.steps[0],late.steps[0])
        self.assertNotEqual(early.steps[1].observed_caps,late.steps[1].observed_caps)

    def test_policy_cannot_read_future_scenario_identity(self):
        trial=demonstrator()
        case=trial.cases[0]
        swapped=replace(case,name="renamed",probability=Fraction(1,3))
        changed=replace(trial,cases=(swapped,*trial.cases[1:]))
        self.assertEqual(tuple(step.action for step in execute(trial,case).steps),
                         tuple(step.action for step in execute(changed,swapped).steps))

    def test_post_shock_disabled_repair_prevents_recovery(self):
        trial=demonstrator()
        fault=replace(trial.cases[0].fault,disable=frozenset({"restore"}))
        cases=(replace(trial.cases[0],fault=fault),*trial.cases[1:])
        changed=replace(trial,cases=cases)
        self.check(changed)
        self.assertEqual(execute(changed,changed.cases[0]).result("service"),0)

    def test_stock_depletion_prevents_recovery(self):
        trial=demonstrator()
        cases=(replace(trial.cases[0],fault=replace(trial.cases[0].fault,
                        destroy=(1,))),*trial.cases[1:])
        changed=replace(trial,cases=cases)
        self.check(changed)
        self.assertEqual(execute(changed,changed.cases[0]).result("service"),0)

    def test_loss_at_tick_zero_and_recovery_at_tick_one(self):
        trial=demonstrator()
        cases=(Case("time0",Fraction(1),Fault(0,frozenset({"service"}),(0,))),)
        changed=replace(trial,cases=cases)
        self.check(changed)
        self.assertEqual(execute(changed,cases[0]).first_restored_at,(("service",1),))

    def test_no_eligible_failure_conditional_rate_is_undefined(self):
        trial=demonstrator()
        cases=(Case("safe",Fraction(1),Fault(1,frozenset(),(0,))),)
        changed=replace(trial,cases=cases)
        self.assertEqual(loss_conditioned_probability(changed)["service"],
                         {"eligible_probability":"0","restoration_given_loss":None})

    def test_multiple_goals_are_individually_loss_conditioned(self):
        base=Model(initial=frozenset({"a","b","base"}),goals=frozenset({"a","b"}),
              resources=(),stock=(),
              actions=(Action("restore_a",frozenset({"base"}),"a",(),()),),
              horizon=2,fault=Fault(1,frozenset({"a"}),()))
        trial=Trial(base,FixedPolicy(("restore_a",),("restore_a",)),
                    (Case("lossa",Fraction(1),base.fault),))
        self.check(trial)
        outcome=execute(trial,trial.cases[0])
        self.assertEqual(outcome.eligible_results,(("a",1),("b",None)))
        self.assertEqual(outcome.retained_at_fault,frozenset({"b"}))

    def test_policy_priority_and_identifiers_must_be_complete(self):
        trial=demonstrator()
        with self.assertRaises(ValueError):
            replace(trial,policy=FixedPolicy(("restore",),("restore",)))
        with self.assertRaises(ValueError):
            replace(trial,policy=FixedPolicy(("restore","restore"),
                                             ("restore","idle_product")))

    def test_invalid_future_shock_contracts_fail(self):
        trial=demonstrator()
        c=trial.cases[0]
        for fault in (replace(c.fault,tick=99),
                      replace(c.fault,disable=frozenset({"phantom"})),
                      replace(c.fault,destroy=(-1,))):
            with self.assertRaises(ValueError):
                replace(trial,cases=(replace(c,fault=fault),*trial.cases[1:]))

    def test_probability_contract_and_names(self):
        trial=demonstrator()
        with self.assertRaises(ValueError):
            replace(trial,cases=(trial.cases[0],))
        with self.assertRaises(ValueError):
            replace(trial,cases=(trial.cases[0],)*3)

    def test_diagnostic_audit_matches_fixed_contract(self):
        data=audit()
        self.assertEqual(data["small_models"],32)
        self.assertEqual(data["independent_trace_comparisons"],67)
        self.assertEqual(data["mismatches"],0)
        self.assertEqual(data["example_conditional_restoration"],"1/2")


if __name__=="__main__":
    unittest.main()
