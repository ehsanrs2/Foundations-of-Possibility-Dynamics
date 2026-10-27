"""R4: development families and sealed-holdout guards. No H1 inference."""
from dataclasses import replace
from fractions import Fraction
import unittest

from experiments.p1_r4_development_families import (
    TRAIN,TUNE,SEALED,make_instance,audit,
)
from experiments.p1_r3_policy_rollout import execute, independent_history_oracle


class DevelopmentFamiliesTests(unittest.TestCase):
    def test_four_dev_families_are_distinct_and_registered(self):
        self.assertEqual(len(set(TRAIN+TUNE+SEALED)),6)
        self.assertEqual(len(TRAIN),3)
        self.assertEqual(len(TUNE),1)

    def test_no_sealed_family_can_generate_even_with_valid_seed(self):
        for family in SEALED:
            with self.assertRaises(PermissionError):
                make_instance(family,20261027,0)

    def test_unregistered_family_fails(self):
        with self.assertRaises(ValueError):
            make_instance("new_hidden_family",123,0)

    def test_negative_index_and_non_integer_seed_rejected(self):
        for seed,index in ((123,-1),(1.5,0),(True,0),(1,1.0)):
            with self.assertRaises(ValueError):
                make_instance(TRAIN[0],seed,index)

    def test_same_seed_produces_exactly_same_trial_and_digest(self):
        for family in TRAIN+TUNE:
            a=make_instance(family,42,1)
            b=make_instance(family,42,1)
            self.assertEqual(a,b)

    def test_seed_streams_unique_across_family_and_instance(self):
        ids=[make_instance(f,123,i).seed_id for f in TRAIN+TUNE for i in range(4)]
        self.assertEqual(len(ids),len(set(ids)))

    def test_different_master_seed_changes_fingerprint(self):
        a=make_instance(TRAIN[0],10,0)
        b=make_instance(TRAIN[0],11,0)
        self.assertNotEqual(a.seed_id,b.seed_id)

    def test_four_family_grammars_have_distinguishable_rule_sets(self):
        rules=[{a.name for a in make_instance(f,9,0).trial.base.actions}
               for f in TRAIN+TUNE]
        self.assertEqual(len(set(frozenset(r) for r in rules)),4)

    def test_family_stresses_are_present(self):
        temporal=make_instance(TUNE[0],12,0).trial.base.actions
        self.assertIn("stage_two",{a.name for a in temporal})
        self.assertIn("prepare_fast",{a.name for a in temporal})
        hub=make_instance(TRAIN[2],12,0).trial.base.actions
        self.assertIn("rebuild_hub",{a.name for a in hub})
        modular=make_instance(TRAIN[1],12,0).trial.base.actions
        self.assertIn("prepare_bridge",{a.name for a in modular})

    def test_fixed_priority_policy_covers_each_action_once(self):
        for family in TRAIN+TUNE:
            trial=make_instance(family,20261027,0).trial
            names={a.name for a in trial.base.actions}
            self.assertEqual(set(trial.policy.before_priority),names)
            self.assertEqual(set(trial.policy.after_priority),names)
            self.assertEqual(len(trial.policy.before_priority),len(names))

    def test_scenarios_exactly_normalized_and_vary_fault_time(self):
        for family in TRAIN+TUNE:
            trial=make_instance(family,20261027,0).trial
            self.assertEqual(sum((c.probability for c in trial.cases),Fraction()),1)
            self.assertEqual(len(trial.cases),4)
            self.assertGreaterEqual(len({c.fault.tick for c in trial.cases}),1)
            self.assertIn("retained",{c.name for c in trial.cases})

    def test_no_loss_scenario_has_undefined_restoration(self):
        for family in TRAIN+TUNE:
            trial=make_instance(family,20261027,0).trial
            c=next(x for x in trial.cases if x.name=="retained")
            self.assertIsNone(execute(trial,c).result("service"))

    def test_lost_goal_was_present_before_fault(self):
        for family in TRAIN+TUNE:
            trial=make_instance(family,20261027,0).trial
            for c in trial.cases:
                outcome=execute(trial,c)
                if outcome.result("service") is not None:
                    self.assertIn("service",outcome.held_before_fault)
                    self.assertIn("service",outcome.lost_at_fault)

    def test_repaired_label_is_single_real_history(self):
        for family in TRAIN+TUNE:
            trial=make_instance(family,20261027,1).trial
            for case in trial.cases:
                self.assertEqual(execute(trial,case),
                                 independent_history_oracle(trial,case))

    def test_future_scenario_names_not_used_by_policy(self):
        trial=make_instance(TRAIN[0],333,0).trial
        original=trial.cases[0]
        renamed=replace(original,name="blinded_fault")
        changed=replace(trial,cases=(renamed,)+trial.cases[1:])
        first=execute(trial,original)
        blind=execute(changed,renamed)
        self.assertEqual(first.steps,blind.steps)
        self.assertEqual(first.eligible_results,blind.eligible_results)

    def test_development_audit_never_generates_holdout(self):
        result=audit(20261027,2)
        self.assertEqual(result["heldout_generated"],0)
        self.assertEqual(result["instances"],8)
        self.assertEqual(result["trace_checks"],32)
        self.assertEqual(result["status"],"DEVELOPMENT_DIAGNOSTICS_NOT_H1")
        self.assertTrue(all(x["independent_dev_instances"]==2
                            for x in result["families"]))

    def test_developer_count_is_bounded(self):
        with self.assertRaises(ValueError):
            audit(20261027,0)
        with self.assertRaises(ValueError):
            audit(20261027,100)


if __name__=="__main__":
    unittest.main()
