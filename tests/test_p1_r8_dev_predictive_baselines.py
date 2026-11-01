"""R8: finite development-only predictive baseline contract tests."""
from dataclasses import replace
from fractions import Fraction
import json
import unittest

from experiments.p1_r4_development_families import TRAIN, TUNE, SEALED
from experiments.p1_r6_fault_risk_dev import develop_trial, developer_law, HazardLaw
from experiments.p1_r8_dev_predictive_baselines import (
    FEATURES, R1_EXTRA, RIDGE, _planned_supports,
    structural_features, exact_target, record, _standardize,
    _solve_ridge, _fit_predict, evaluate, public_summary,
)


class R8PredictiveBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pilot=evaluate(seed=20261101,train_n=3,tune_n=3,verify=True)

    def test_no_sealed_generator_or_h1_outcomes(self):
        p=self.pilot
        self.assertEqual(p["sealed_test_families_generated"],0)
        self.assertEqual(p["confirmatory_h1_samples"],0)
        self.assertIn("NOT_H1",p["classification"])
        self.assertEqual(p["train_independent_systems"],9)
        self.assertEqual(p["tune_independent_systems"],3)

    def test_candidate_is_not_a_simulated_physical_measurement(self):
        p=develop_trial(20261101,TRAIN[0],0)
        law=developer_law(20261101,TRAIN[0],0)
        ordinary,candidate,status=structural_features(p.base,TRAIN[0],law)
        self.assertEqual(len(ordinary),len(FEATURES))
        self.assertIn(status,{"SCOPED","NO_FEASIBLE_PLAN","INSUFFICIENT_FAULT_COVERAGE"})
        self.assertIn(candidate,(0.0,1.0,None))

    def test_r8_uses_explicit_common_upstream_fault_not_invented_channel_faults(self):
        for family in TRAIN+TUNE:
            x=develop_trial(20261101,family,0)
            law=developer_law(20261101,family,0)
            f,c,status=structural_features(x.base,family,law)
            self.assertIn(c,(0.0,None))
            # Every construction route that really requires the upstream
            # protected-by-no-one dependency cannot become disjoint in R1.
            if status=="SCOPED":
                self.assertEqual(c,0.0)

    def test_r1_zero_variation_is_not_a_positive_h1_test(self):
        p=self.pilot
        self.assertTrue(p["r1_non_discriminating"])
        self.assertTrue(all(v==0.0 for v in p["r1_distinct_defined_values"]))
        self.assertEqual(p["mean_paired_improvement_baseline_minus_augmented"],0.0)

    def test_no_future_fault_id_or_tick_can_enter_structural_features(self):
        trial=develop_trial(20261101,TRAIN[0],1)
        law=developer_law(20261101,TRAIN[0],1)
        a=structural_features(trial.base,TRAIN[0],law)
        shuffled=replace(trial.base,fault=replace(
            trial.base.fault,tick=0,remove=frozenset({"service","base"}),
            destroy=(999,),disable=frozenset()))
        b=structural_features(shuffled,TRAIN[0],law)
        self.assertEqual(a,b)

    def test_change_in_predeclared_priors_reaches_both_arms(self):
        t=develop_trial(20261101,TRAIN[0],0)
        low=HazardLaw(Fraction(1,8),Fraction(0),Fraction(0))
        high=HazardLaw(Fraction(3,4),Fraction(1,2),Fraction(1,2))
        a=structural_features(t.base,TRAIN[0],low)[0]
        b=structural_features(t.base,TRAIN[0],high)[0]
        self.assertEqual(a[:-3],b[:-3])
        self.assertNotEqual(a[-3:],b[-3:])

    def test_actual_loss_zero_is_missing_not_negative(self):
        t=develop_trial(20261101,TRAIN[0],1,law=HazardLaw(
            Fraction(0),Fraction(1,2),Fraction(1,4)))
        loss,p,checks=exact_target(t,verify=True)
        self.assertEqual(loss,0)
        self.assertIsNone(p)
        self.assertEqual(checks,len(t.cases))

    def test_r7_exact_label_and_independent_histories_match(self):
        t=develop_trial(20261101,TRAIN[1],0,law=HazardLaw(
            Fraction(1,2),Fraction(1,4),Fraction(1,4)))
        loss,p,checked=exact_target(t,verify=True)
        self.assertEqual(loss,Fraction(1,2))
        self.assertIsNotNone(p)
        self.assertEqual(checked,len(t.cases))

    def test_standardization_is_training_only(self):
        a,b=_standardize([(1.0,2.0),(3.0,4.0)],[(5.0,6.0)])
        self.assertEqual(a,[ [1.0,-1.0,-1.0],[1.0,1.0,1.0] ])
        self.assertEqual(b,[[1.0,3.0,3.0]])

    def test_ridge_solver_is_deterministic_and_regularized(self):
        x=[[1.0,0.0],[1.0,1.0],[1.0,2.0]]
        y=[0.0,0.5,1.0]
        w1=_solve_ridge(x,y)
        w2=_solve_ridge(x,y)
        self.assertEqual(w1,w2)
        self.assertEqual(len(w1),2)
        self.assertGreater(w1[1],0)

    def test_learner_has_same_design_and_fixed_hyperparameters(self):
        p=self.pilot
        self.assertEqual(p["prediction_model"],
                         "STANDARDIZED_RIDGE_LINEAR_PROBABILITY_CLIPPED")
        self.assertEqual(p["ridge_penalty_fixed"],RIDGE)
        self.assertTrue(p["identical_raw_pre_event_inputs"])
        self.assertTrue(p["same_train_tune_systems_and_learner"])

    def test_each_tune_system_scores_against_ideal_reference(self):
        for row in self.pilot["tune_system_records"]:
            self.assertGreaterEqual(row["baseline_expected_brier"]+1e-10,
                                    row["ideal_expected_brier"])
            self.assertGreaterEqual(row["baseline_plus_r1_expected_brier"]+1e-10,
                                    row["ideal_expected_brier"])
            self.assertGreaterEqual(row["baseline_probability"],0)
            self.assertLessEqual(row["baseline_probability"],1)

    def test_scoped_pairs_undefined_dont_become_claim_of_independence(self):
        for row in self.pilot["tune_system_records"]:
            if row["r1_candidate"] is None:
                self.assertEqual(row["r1_status"],"INSUFFICIENT_FAULT_COVERAGE")
            else:
                self.assertIn(row["r1_candidate"],(0.0,1.0))

    def test_counts_are_independent_systems_not_rollouts(self):
        p=self.pilot
        self.assertEqual(p["train_eligible_systems"]+
                         p["tune_eligible_systems"]+p["zero_risk_systems"],12)
        self.assertLessEqual(p["verified_full_histories"],16*12)

    def test_no_claim_of_enforced_equal_runtime(self):
        p=self.pilot
        self.assertFalse(p["equal_wall_time_or_memory_caps_enforced"])
        self.assertGreaterEqual(p["feature_wall_ns_total"],0)
        self.assertGreaterEqual(p["baseline_fit_predict_wall_ns"],0)
        self.assertGreaterEqual(p["plus_r1_fit_predict_wall_ns"],0)
        self.assertNotIn("p_value",p)

    def test_tune_record_is_stable_under_duplicate_run(self):
        a=evaluate(seed=20261101,train_n=2,tune_n=2)
        b=evaluate(seed=20261101,train_n=2,tune_n=2)
        self.assertEqual(public_summary(a),public_summary(b))
        # Measured wall-time is instrumentation, not deterministic evidence.
        a.pop("feature_wall_ns_total")
        a.pop("baseline_fit_predict_wall_ns")
        a.pop("plus_r1_fit_predict_wall_ns")
        b.pop("feature_wall_ns_total")
        b.pop("baseline_fit_predict_wall_ns")
        b.pop("plus_r1_fit_predict_wall_ns")
        self.assertEqual(a,b)

    def test_input_validation(self):
        for kw in ({"train_n":0},{"train_n":25},{"tune_n":0},
                   {"tune_n":13},{"seed":True},{"train_n":1.0}):
            with self.assertRaises(ValueError):
                evaluate(**kw)

    def test_sealed_family_feature_request_is_blocked(self):
        t=develop_trial(20261101,TRAIN[0],0)
        for forbidden in SEALED:
            with self.assertRaises(PermissionError):
                structural_features(t.base,forbidden,developer_law(
                    20261101,TRAIN[0],0))


if __name__=="__main__":
    unittest.main()
