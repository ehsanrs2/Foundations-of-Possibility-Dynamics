"""Regression tests for hand-specified scenario, NOT confirmatory hypothesis tests."""
import json
from pathlib import Path
import unittest
from experiments.toy_case import (BASE, Plan, SHOCK_EXPOSED, feasible_plans,
    goal_reachable, gbr, gop, run, has_disjoint_backup)

class ToyCaseTests(unittest.TestCase):
    def test_pre_shock_metrics(self):
        self.assertEqual(gop(BASE), 0)
        self.assertEqual(gbr(BASE), 1)

    def test_wire_shock(self):
        after = BASE - {"wire_tx"}
        self.assertFalse(goal_reachable(after, generative=False))
        self.assertTrue(goal_reachable(after, generative=True))
        self.assertEqual(gbr(after), 0)

    def test_shared_component_failure(self):
        for item in ("power", "sensor"):
            self.assertFalse(goal_reachable(BASE - {item}, generative=True))

    def test_resource_and_horizon_limits(self):
        self.assertEqual(len(feasible_plans(BASE, generative=True, horizon=1)), 1)
        self.assertEqual(len(feasible_plans(BASE, generative=True, kits=0)), 1)

    def test_shared_shock_exposed_component(self):
        a = Plan("a", frozenset({"wire_tx","led"}), 1, 0, False)
        b = Plan("b", frozenset({"wire_tx","timer"}), 1, 0, True)
        self.assertFalse(has_disjoint_backup((a,b)))

    def test_archived_output(self):
        path = Path(__file__).parents[1] / "experiments" / "toy_case_results_v0_1.json"
        self.assertEqual(run(), json.loads(path.read_text(encoding="utf-8")))

    def test_shock_scope_is_explicit(self):
        self.assertEqual(SHOCK_EXPOSED, frozenset({"wire_tx","led","timer","assembly"}))

if __name__ == "__main__":
    unittest.main()
