"""G1 verification tests. No inference about research hypothesis H1."""
from dataclasses import replace
import unittest
from experiments.p1_gate1 import (Rule, Model, example, shocked, measures,
    enumerate_dfs, enumerate_subsets, generated, audit)


class G1PlanSupportTests(unittest.TestCase):
    def compare(self, model):
        for enabled in (True, False):
            self.assertEqual(enumerate_dfs(model, construction=enabled),
                             enumerate_subsets(model, construction=enabled))
        self.assertEqual(measures(model, enumerator=enumerate_dfs),
                         measures(model, enumerator=enumerate_subsets))

    def test_initial_gog_zero_and_gbr_gain_one(self):
        model = example()
        self.compare(model)
        self.assertEqual(measures(model)["gog"], 0)
        self.assertEqual(measures(model)["gbr_gain"], 1)
        plans = enumerate_dfs(model, construction=True)
        optical = next(p for p in plans if p.generative)
        self.assertIn("rule:build_optical", optical.support)
        for component in ("led", "timer", "assembly", "power", "sensor"):
            self.assertIn("cap:" + component, optical.support)

    def test_single_source_failure_and_post_shock_replanning(self):
        damaged = shocked(example(), "cap:wire_tx")
        self.compare(damaged)
        self.assertEqual(measures(damaged)["static_goals"], 0)
        self.assertEqual(measures(damaged)["generative_goals"], 1)
        self.assertEqual(measures(damaged)["gog"], 1)
        self.assertEqual(measures(damaged)["gbr_gain"], 0)

    def test_shared_power_and_sensor_failures(self):
        for component in ("power", "sensor"):
            damaged = shocked(example(), "cap:" + component)
            self.compare(damaged)
            self.assertEqual(measures(damaged)["generative_goals"], 0)

    def test_rule_failure_and_constructed_route(self):
        damaged = shocked(example(), "cap:wire_tx", "rule:build_optical")
        self.compare(damaged)
        self.assertEqual(measures(damaged)["generative_goals"], 0)

    def test_exposure_scope_changes_backup_interpretation(self):
        model = example()
        self.assertEqual(measures(model)["gbr_gain"], 1)
        broader = replace(model, exposed=model.exposed | {"cap:power"})
        self.compare(broader)
        self.assertEqual(measures(broader)["gbr_gain"], 0)

    def test_cost_and_deadline_constraints(self):
        model = example()
        for variant in (replace(model, budget=0), replace(model, horizon=1)):
            self.compare(variant)
            self.assertEqual(measures(variant)["gbr_gain"], 0)

    def test_two_static_routes_mean_no_incremental_gbr(self):
        model = example()
        static_optical = tuple(replace(r, generative=False)
                               if r.name == "build_optical" else r for r in model.rules)
        amended = replace(model, rules=static_optical)
        self.compare(amended)
        self.assertEqual(measures(amended)["gbr_gain"], 0)
        self.assertEqual(measures(amended)["static_plans"], 2)

    def test_rebuild_removed_initial_source(self):
        model = Model(frozenset({"tool", "part"}),
                      frozenset({"goal"}),
                      (Rule("rebuild", frozenset({"tool", "part"}), "wire", 1, 1, True),
                       Rule("use", frozenset({"wire", "tool"}), "goal")),
                      2, 1, frozenset({"cap:wire", "rule:rebuild"}))
        self.compare(model)
        self.assertEqual(measures(model)["generative_goals"], 1)
        self.assertEqual(measures(model)["static_goals"], 0)

    def test_multiple_producers_and_irrelevant_steps(self):
        model = Model(frozenset({"a", "b", "junk"}), frozenset({"goal"}),
                      (Rule("a_path", frozenset({"a"}), "goal"),
                       Rule("b_path", frozenset({"b"}), "goal"),
                       Rule("unused", frozenset({"junk"}), "x")),
                      3, 0, frozenset({"cap:a", "cap:b", "cap:junk"}))
        self.compare(model)
        self.assertEqual(len(enumerate_dfs(model, construction=False)), 2)
        self.assertEqual(measures(model)["gbr_gain"], 0)

    def test_cyclic_rules_do_not_create_goals(self):
        model = Model(frozenset({"a"}), frozenset({"goal"}),
                      (Rule("cycle_a", frozenset({"x"}), "y"),
                       Rule("cycle_b", frozenset({"y"}), "x"),
                       Rule("goal_rule", frozenset({"x"}), "goal")),
                      5, 0, frozenset({"cap:a", "rule:cycle_a"}))
        self.compare(model)
        self.assertEqual(measures(model)["generative_goals"], 0)

    def test_invalid_contracts(self):
        with self.assertRaises(ValueError):
            Rule("", frozenset({"a"}), "b")
        with self.assertRaises(ValueError):
            Rule("x", frozenset({"a"}), "a")
        with self.assertRaises(ValueError):
            Model(frozenset(), frozenset(), tuple(), -1, 0, frozenset({"cap:a"}))
        with self.assertRaises(ValueError):
            Model(frozenset(), frozenset(), tuple(), 1, 0, frozenset())
        with self.assertRaises(ValueError):
            Model(frozenset(), frozenset(), (Rule("r", frozenset({"a"}), "x"),
                                             Rule("r", frozenset({"a"}), "y")),
                  2, 0, frozenset({"cap:a"}))
        with self.assertRaises(ValueError):
            shocked(example(), "power")

    def test_seeded_oracle_agreement_and_nonnegative_gain(self):
        out = audit()
        self.assertEqual(out["plan_set_comparisons"], 192)
        self.assertEqual(out["mismatches"], 0)
        for item in generated(count=6):
            self.assertGreaterEqual(measures(item)["gbr_gain"], 0)
            self.compare(item)


if __name__ == "__main__":
    unittest.main()
