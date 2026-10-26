"""G3 regression and small-system equivalence tests (software only)."""
import json
from dataclasses import replace
from pathlib import Path
import unittest

from experiments.p1_gate2 import Action, Fault, Model, alarm_example, generated
from experiments.p1_gate3 import (augmented_solver, history_oracle, verify,
                                  shared_kit_example, audit)


class G3Tests(unittest.TestCase):
    def both(self, model, *, construction=True):
        verify(model)
        a = augmented_solver(model, construction=construction)
        self.assertEqual(a, history_oracle(model, construction=construction))
        return a

    def test_alarm_available_earlier_than_strictly_restored(self):
        result = self.both(alarm_example())
        self.assertEqual(result.available, {"alarm": 2})
        self.assertEqual(result.restored, {"alarm": 3})
        self.assertEqual(result.retained, frozenset())
        self.assertEqual(result.joint, 2)

    def test_only_nonconstructive_route_is_lost(self):
        result = self.both(alarm_example(), construction=False)
        self.assertEqual(result.available, {})
        self.assertEqual(result.restored, {})
        self.assertIsNone(result.joint)

    def test_horizon_two_allows_availability_but_not_restoration(self):
        model = replace(alarm_example(), horizon=2)
        result = self.both(model)
        self.assertEqual(result.available, {"alarm": 2})
        self.assertEqual(result.restored, {})

    def test_retention_not_strict_restoration(self):
        model = Model(frozenset({"goal"}), frozenset({"goal"}), (),
                      (), (), 1, Fault(1, frozenset(), ()))
        result = self.both(model)
        self.assertEqual(result.retained, frozenset({"goal"}))
        self.assertEqual(result.available, {"goal": 1})
        self.assertEqual(result.restored, {})

    def test_pre_fault_presence_and_loss_required(self):
        model = Model(frozenset({"source"}), frozenset({"goal"}), (), (),
                      (Action("make", frozenset({"source"}), "goal", (), ()),),
                      2, Fault(0, frozenset({"goal"}), ()))
        result = self.both(model)
        self.assertEqual(result.available, {"goal": 1})
        self.assertEqual(result.restored, {})  # goal absent at t=0- 

    def test_loss_at_zero_and_subsequent_recovery(self):
        model = Model(frozenset({"source","goal"}), frozenset({"goal"}), (), (),
                      (Action("remake", frozenset({"source"}), "goal", (), ()),),
                      1, Fault(0, frozenset({"goal"}), ()))
        result = self.both(model)
        self.assertEqual(result.restored, {"goal": 1})
        self.assertEqual(result.retained, frozenset())

    def test_destroy_kit_early_build_preserves_access_not_restoration(self):
        model = alarm_example()
        result = self.both(replace(model, fault=replace(model.fault, destroy=(1,))))
        self.assertEqual(result.available, {"alarm": 2})
        self.assertEqual(result.restored, {})

    def test_shock_removing_shared_sensor_prevents_access(self):
        model = alarm_example()
        fault = replace(model.fault, remove=model.fault.remove | {"sensor"})
        result = self.both(replace(model, fault=fault))
        self.assertEqual(result.available, {})
        self.assertEqual(result.restored, {})

    def test_one_kit_individual_goals_not_joint(self):
        result = self.both(shared_kit_example(kits=1))
        self.assertEqual(result.available, {"g1":1, "g2":1})
        self.assertIsNone(result.joint)

    def test_two_kits_joint_goal_possible(self):
        result = self.both(shared_kit_example(kits=2))
        self.assertEqual(result.joint, 2)

    def test_one_kit_replenished_yields_joint_goals(self):
        model = shared_kit_example(kits=1)
        model = replace(model, horizon=3, actions=model.actions + (
            Action("refill", frozenset({"base"}), "refill_done", (0,), (1,)),
        ))
        result = self.both(model)
        self.assertEqual(result.joint, 3)

    def test_fault_at_horizon_discards_prior_goal(self):
        model = Model(frozenset({"goal"}), frozenset({"goal"}), (), (), (),
                      2, Fault(2, frozenset({"goal"}), ()))
        result = self.both(model)
        self.assertEqual(result.available, {})
        self.assertEqual(result.restored, {})
        self.assertIsNone(result.joint)

    def test_disabled_actions_after_fault_only(self):
        model = Model(frozenset({"source"}), frozenset({"goal"}), (), (),
                      (Action("make", frozenset({"source"}), "goal", (), ()),),
                      2, Fault(1, frozenset(), (), frozenset({"make"})))
        result = self.both(model)
        self.assertEqual(result.available, {"goal":1})
        self.assertEqual(result.retained, frozenset({"goal"}))

    def test_random_models_have_no_search_disagreement(self):
        for model in generated(n=12):
            self.both(model)

    def test_fixed_seed_audit_matches_archived_manifest(self):
        actual = audit()
        expected = json.loads((Path(__file__).parents[1] /
            "experiments" / "g3_expected.json").read_text(encoding="utf-8"))
        self.assertEqual(actual, expected)
        self.assertEqual(actual["solver_pair_comparisons"], 256)


if __name__ == "__main__":
    unittest.main()
