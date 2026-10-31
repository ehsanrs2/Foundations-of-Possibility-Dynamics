"""R6 risk-law and exact pre-fault reference oracle — developer-only."""
from dataclasses import replace
from fractions import Fraction
import unittest

from experiments.p1_r3_policy_rollout import (
    execute, independent_history_oracle,
)
from experiments.p1_r4_development_families import TRAIN, TUNE, SEALED
from experiments.p1_r6_fault_risk_dev import (
    HazardLaw, developer_law, develop_trial,
    exact_pre_fault_policy_baseline, run, summary, SERVICE_RISKS,
)


class R6RiskLawTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pilot = run(seed=20261031,train_n=2,tune_n=1)

    def test_no_sealed_family_is_instantiated_or_randomized(self):
        for f in SEALED:
            with self.assertRaises(PermissionError):
                developer_law(20261031,f,0)
            with self.assertRaises(PermissionError):
                develop_trial(20261031,f,0)
        self.assertEqual(self.pilot["heldout_generated"],0)

    def test_stipulated_hazard_law_is_strictly_validated(self):
        for invalid in (Fraction(-1, 8), Fraction(9,8), 0.5):
            with self.assertRaises(ValueError):
                HazardLaw(invalid,Fraction(0),Fraction(0))
        self.assertEqual(HazardLaw(Fraction(0),Fraction(1),Fraction(0)).shared_loss,1)

    def test_independent_scenario_weights_sum_exactly_one(self):
        for family in TRAIN+TUNE:
            p=develop_trial(7,family,0,law=HazardLaw(
                Fraction(1,4),Fraction(1,2),Fraction(1,8)))
            self.assertEqual(sum((c.probability for c in p.cases),Fraction()),1)
            self.assertEqual(len(p.cases),16)
            self.assertEqual(len(set(c.name for c in p.cases)),16)

    def test_two_distinct_possible_fault_times(self):
        for family in TRAIN+TUNE:
            t=develop_trial(77,family,0,law=HazardLaw(
                Fraction(1,4),Fraction(1,4),Fraction(1,4)))
            self.assertEqual({c.fault.tick for c in t.cases},
                             {1,t.base.horizon})

    def test_zero_loss_risk_produces_missing_conditional_outcome(self):
        p=develop_trial(22,TRAIN[0],0,law=HazardLaw(
            Fraction(0),Fraction(1,2),Fraction(1,2)))
        a=exact_pre_fault_policy_baseline(p)
        self.assertEqual(a["eligible_mass"],"0")
        self.assertIsNone(a["conditional_restoration_probability"])
        self.assertIsNone(a["model_optimal_expected_brier_conditional"])
        self.assertEqual(a["complete_history_checks"],len(p.cases))

    def test_full_loss_risk_produces_no_undefined_outcome(self):
        p=develop_trial(22,TRAIN[0],0,law=HazardLaw(
            Fraction(1),Fraction(0),Fraction(0)))
        self.assertEqual(len(p.cases),2)
        self.assertTrue(all(execute(p,c).result("service") is not None
                            for c in p.cases))
        self.assertEqual(exact_pre_fault_policy_baseline(p)["eligible_mass"],"1")

    def test_independent_events_change_loss_risk_from_fixed_75_percent(self):
        for probability in (Fraction(0),Fraction(1,8),Fraction(1,4),
                            Fraction(1,2),Fraction(3,4),Fraction(1)):
            p=develop_trial(13,TRAIN[0],1,law=HazardLaw(
                probability,Fraction(1,2),Fraction(1,4)))
            a=exact_pre_fault_policy_baseline(p)
            self.assertEqual(Fraction(a["eligible_mass"]),probability)

    def test_boundary_event_without_effect_is_visible_only_after_tick(self):
        p=develop_trial(9,TRAIN[0],0,law=HazardLaw(
            Fraction(0),Fraction(0),Fraction(0)))
        early=next(c for c in p.cases if c.name.startswith("early_"))
        v=execute(p,early)
        self.assertFalse(v.steps[0].event_seen)
        self.assertTrue(v.steps[1].event_seen)
        self.assertEqual(v.lost_at_fault,frozenset())
        # This is an explicit R3 observation-model limitation, not realism.

    def test_early_pre_fault_history_equal_under_different_future_events(self):
        p=develop_trial(15,TRAIN[1],0,law=HazardLaw(
            Fraction(1,2),Fraction(1,2),Fraction(0)))
        early=[c for c in p.cases if c.name.startswith("early_")]
        traces=[execute(p,c).steps[0] for c in early]
        self.assertTrue(all(t==traces[0] for t in traces))

    def test_scenario_labels_cannot_change_exact_pre_fault_prediction(self):
        p=develop_trial(20261031,TUNE[0],0,law=HazardLaw(
            Fraction(1,2),Fraction(1,4),Fraction(1,4)))
        q=replace(p,cases=tuple(replace(c,name="blind_"+c.name)
                                for c in reversed(p.cases)))
        self.assertEqual(
            exact_pre_fault_policy_baseline(p),
            exact_pre_fault_policy_baseline(q))

    def test_full_history_independent_reference_agrees_for_every_case(self):
        p=develop_trial(104,TRAIN[2],0,law=HazardLaw(
            Fraction(1,2),Fraction(1,2),Fraction(1,2)))
        self.assertEqual(len(p.cases),16)
        for c in p.cases:
            self.assertEqual(execute(p,c),independent_history_oracle(p,c))

    def test_optimal_model_score_cannot_be_improved_in_expectation(self):
        q=Fraction(1,4)
        optimal=q*(1-q)
        half=Fraction(1,4)
        excess=(Fraction(1,2)-q)**2
        self.assertEqual(optimal,Fraction(3,16))
        self.assertEqual(half-optimal,excess)
        self.assertEqual(excess,Fraction(1,16))

    def test_no_learned_model_or_h1_evidence(self):
        d=self.pilot
        self.assertIn("NOT_H1",d["classification"])
        self.assertEqual(d["confirmatory_samples"],0)
        self.assertEqual(d["independent_developer_systems"],7)
        self.assertNotIn("brier_improvement_of_GBR",d)

    def test_systems_not_repeated_fault_rollouts_are_units(self):
        d=self.pilot
        self.assertEqual(len(d["system_records"]),7)
        self.assertGreater(d["full_history_oracle_checks"],7)
        self.assertEqual(len(d["family_profiles"]),4)
        for row in d["family_profiles"]:
            self.assertEqual(row["positive_loss_risk_systems"]+
                row["zero_loss_risk_systems"],row["independent_developer_systems"])

    def test_result_is_seed_reproducible(self):
        other=run(seed=20261031,train_n=2,tune_n=1)
        self.assertEqual(other,self.pilot)

    def test_risk_law_is_independently_derived_from_system_family_index(self):
        laws=[developer_law(20261031,TRAIN[0],i) for i in range(15)]
        self.assertGreater(len(set(laws)),1)
        self.assertTrue(all(law.service_loss in SERVICE_RISKS for law in laws))
        self.assertEqual(developer_law(20261031,TRAIN[0],2),
                         developer_law(20261031,TRAIN[0],2))

    def test_no_invalid_dev_count_or_seed(self):
        for args in ({"train_n":0},{"train_n":25},{"tune_n":0},
                     {"tune_n":13},{"seed":1.2},{"train_n":True}):
            with self.assertRaises(ValueError):
                run(**args)

    def test_summary_separates_system_records_from_family_results(self):
        public=summary(self.pilot)
        self.assertNotIn("system_records",public)
        self.assertEqual(len(public["family_profiles"]),4)
        self.assertEqual(public["heldout_generated"],0)


if __name__ == "__main__":
    unittest.main()
