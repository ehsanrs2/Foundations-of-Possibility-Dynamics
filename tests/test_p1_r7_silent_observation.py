"""R7 event detection tests: real observable changes vs a silent boundary."""
from dataclasses import replace
from fractions import Fraction
import unittest

from experiments.p1_gate2 import Action, Fault, Model
from experiments.p1_r3_policy_rollout import Case, FixedPolicy, Trial, execute
from experiments.p1_r6_fault_risk_dev import HazardLaw, develop_trial
from experiments.p1_r4_development_families import TRAIN, TUNE, SEALED
from experiments.p1_r7_silent_observation import (
    execute_observable, independent_observable_oracle, audit, public_summary,
)


def counterexample(fault: Fault | None = None) -> Trial:
    """At t=1, a false boundary signal swaps a meaningful action decision."""
    actions = (
        Action("prepare1",frozenset({"base"}),"ready1",(),()),
        Action("prepare2",frozenset({"ready1"}),"ready2",(),()),
        Action("alternate",frozenset({"base"}),"alternative",(),()),
    )
    f = fault or Fault(1,frozenset(),())
    base=Model(frozenset({"service","base"}),frozenset({"service"}),
               (),(),actions,3,f)
    policy=FixedPolicy(("prepare1","prepare2","alternate"),
                       ("alternate","prepare1","prepare2"))
    return Trial(base,policy,(Case("case",Fraction(1),f),))


class R7SilentObservationTests(unittest.TestCase):
    def check(self,trial):
        for c in trial.cases:
            self.assertEqual(execute_observable(trial,c),
                             independent_observable_oracle(trial,c))

    def test_silent_noop_does_not_switch_policy_at_boundary(self):
        trial=counterexample()
        case=trial.cases[0]
        new=execute_observable(trial,case)
        old=execute(trial,case)
        self.check(trial)
        self.assertFalse(new.steps[1].event_seen)
        self.assertTrue(old.steps[1].event_seen)
        self.assertEqual(new.steps[1].action,"prepare2")
        self.assertEqual(old.steps[1].action,"alternate")
        self.assertIsNone(new.result("service"))

    def test_hidden_noop_is_observationally_invariant_to_its_time(self):
        a=counterexample()
        moved=Fault(2,frozenset(),())
        b=counterexample(moved)
        actions_a=tuple(s.action for s in execute_observable(a,a.cases[0]).steps)
        actions_b=tuple(s.action for s in execute_observable(b,b.cases[0]).steps)
        self.assertEqual(actions_a,actions_b)
        self.assertTrue(all(not s.event_seen for s in execute_observable(a,a.cases[0]).steps))
        self.assertTrue(all(not s.event_seen for s in execute_observable(b,b.cases[0]).steps))

    def test_removing_unheld_component_does_not_trigger_alarm(self):
        t=counterexample(Fault(1,frozenset({"unheld"}),()))
        self.check(t)
        self.assertFalse(execute_observable(t,t.cases[0]).steps[1].event_seen)

    def test_removing_held_component_is_observed(self):
        t=counterexample(Fault(1,frozenset({"base"}),()))
        self.check(t)
        self.assertTrue(execute_observable(t,t.cases[0]).steps[1].event_seen)

    def test_goal_loss_is_detected_and_not_mistaken_for_retention(self):
        t=counterexample(Fault(1,frozenset({"service"}),()))
        new=execute_observable(t,t.cases[0])
        self.check(t)
        self.assertEqual(new.lost_at_fault,frozenset({"service"}))
        self.assertEqual(new.result("service"),0)
        self.assertTrue(new.steps[1].event_seen)

    def test_stock_damage_detected_only_if_actual_stock_changes(self):
        actions=(Action("a",frozenset({"base"}),"new",(0,),(0,)),)
        def build(qty):
            f=Fault(1,frozenset(),(1,))
            base=Model(frozenset({"base","service"}),
                       frozenset({"service"}),("kit",),(qty,),actions,2,f)
            return Trial(base,FixedPolicy(("a",),("a",)),
                         (Case("stock",Fraction(1),f),))
        empty=build(0)
        stock=build(2)
        self.check(empty)
        self.check(stock)
        self.assertFalse(execute_observable(empty,empty.cases[0]).steps[1].event_seen)
        self.assertTrue(execute_observable(stock,stock.cases[0]).steps[1].event_seen)

    def test_disable_action_is_observable_under_perfect_sensing(self):
        f=Fault(1,frozenset(),(),frozenset({"alternate"}))
        t=counterexample(f)
        self.check(t)
        v=execute_observable(t,t.cases[0])
        self.assertTrue(v.steps[1].event_seen)
        self.assertEqual(v.steps[1].disabled_seen,frozenset({"alternate"}))

    def test_detected_observable_change_remains_latched(self):
        t=counterexample(Fault(1,frozenset({"base"}),()))
        v=execute_observable(t,t.cases[0])
        self.assertTrue(all(s.event_seen for s in v.steps[1:]))

    def test_future_fault_label_cannot_change_actions(self):
        t=counterexample()
        original=t.cases[0]
        replaced=replace(original,name="hidden_renaming")
        q=replace(t,cases=(replaced,))
        a=execute_observable(t,original)
        b=execute_observable(q,replaced)
        self.assertEqual(a.steps,b.steps)
        self.assertEqual(a.eligible_results,b.eligible_results)

    def test_never_pass_future_event_time_to_policy(self):
        t=counterexample(Fault(2,frozenset({"base"}),()))
        q=counterexample(Fault(1,frozenset({"base"}),()))
        self.assertEqual(execute_observable(t,t.cases[0]).steps[0],
                         execute_observable(q,q.cases[0]).steps[0])

    def test_fault_at_tick_zero_is_observed_before_first_action(self):
        t=counterexample(Fault(0,frozenset({"base"}),()))
        new=execute_observable(t,t.cases[0])
        self.check(t)
        self.assertTrue(new.steps[0].event_seen)

    def test_fault_at_final_tick_without_effect_is_silent(self):
        t=counterexample(Fault(3,frozenset(),()))
        new=execute_observable(t,t.cases[0])
        self.check(t)
        self.assertFalse(new.steps[-1].event_seen)
        self.assertIsNone(new.steps[-1].action)

    def test_true_loss_then_repair_same_history(self):
        actions=(
            Action("prepare",frozenset({"base"}),"ready",(),()),
            Action("restore",frozenset({"base"}),"service",(),()),
        )
        f=Fault(1,frozenset({"service"}),())
        m=Model(frozenset({"base","service"}),frozenset({"service"}),
                (),(),actions,3,f)
        t=Trial(m,FixedPolicy(("prepare","restore"),
                              ("restore","prepare")),
                (Case("loss",Fraction(1),f),))
        self.check(t)
        out=execute_observable(t,t.cases[0])
        self.assertEqual(out.first_restored_at,(("service",2),))
        self.assertEqual(out.result("service"),1)
        self.assertEqual(out,execute(t,t.cases[0]))

    def test_r6_zero_events_are_silent(self):
        t=develop_trial(20261031,TRAIN[0],0,law=HazardLaw(
            Fraction(0),Fraction(0),Fraction(0)))
        self.check(t)
        for c in t.cases:
            v=execute_observable(t,c)
            self.assertTrue(all(not s.event_seen for s in v.steps))
            self.assertIsNone(v.result("service"))
            self.assertEqual(c.probability,Fraction(1,2))

    def test_r6_all_events_positive_weight_reproducible(self):
        t=develop_trial(7,TUNE[0],1,law=HazardLaw(
            Fraction(1,2),Fraction(1,4),Fraction(1,4)))
        self.assertEqual(len(t.cases),16)
        self.check(t)

    def test_r6_systems_with_no_eligible_loss_stay_undefined(self):
        t=develop_trial(7,TRAIN[0],0,law=HazardLaw(
            Fraction(0),Fraction(1,2),Fraction(1,2)))
        self.assertTrue(all(execute_observable(t,c).result("service") is None
                            for c in t.cases))

    def test_developer_audit_is_distinct_from_h1_and_nonleaking(self):
        result=audit(seed=20261031,train_n=2,tune_n=1)
        self.assertEqual(result["independent_development_systems"],7)
        self.assertGreater(result["complete_trace_oracle_comparisons"],7)
        self.assertGreater(result["silent_event_case_count"],0)
        self.assertEqual(result["sealed_family_cases"],0)
        self.assertEqual(result["confirmatory_samples"],0)
        self.assertIn("NOT_H1",result["classification"])
        self.assertNotIn("developer_system_rows",public_summary(result))

    def test_developer_audit_seed_is_reproducible(self):
        a=audit(seed=20261031,train_n=1,tune_n=1)
        b=audit(seed=20261031,train_n=1,tune_n=1)
        self.assertEqual(a,b)

    def test_archived_R7_developer_summary_is_exactly_reproducible(self):
        import json
        from pathlib import Path
        archive=Path(__file__).parents[1] / "research" / (
            "R7-silent-observation-summary-seed20261031.json")
        self.assertEqual(
            public_summary(audit(seed=20261031,train_n=24,tune_n=12)),
            json.loads(archive.read_text(encoding="utf-8")))

    def test_reject_bad_case_or_developer_parameters(self):
        t=counterexample()
        wrong=replace(t.cases[0],name="not_registered")
        with self.assertRaises(ValueError):
            execute_observable(t,wrong)
        with self.assertRaises(ValueError):
            independent_observable_oracle(t,wrong)
        for kw in ({"train_n":0},{"tune_n":0},{"train_n":25},
                   {"tune_n":13},{"seed":True}):
            with self.assertRaises(ValueError):
                audit(**kw)


if __name__=="__main__":
    unittest.main()
