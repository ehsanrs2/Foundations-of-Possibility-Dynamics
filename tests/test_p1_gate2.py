"""G2 deterministic correctness tests, NOT scientific hypothesis tests."""
from dataclasses import replace
import json
from pathlib import Path
import unittest
from experiments.p1_gate2 import (Action, Fault, Model, alarm_example, generated,
                                  dfs_postfault, bfs_postfault, compare, audit)


class G2Tests(unittest.TestCase):
    def run_both(self, model, expected, *, construction=True):
        self.assertEqual(dfs_postfault(model, construction=construction), expected)
        self.assertEqual(bfs_postfault(model, construction=construction), expected)
        compare(model)

    def test_optical_recovery_after_in_run_fault(self):
        example = alarm_example()
        self.run_both(example, {"alarm":2})
        self.run_both(example, {}, construction=False)

    def test_no_kit_blocks_rebuild(self):
        example = replace(alarm_example(), stock=(0,))
        self.run_both(example, {})

    def test_goal_reached_early_but_destroyed_at_fault(self):
        example = alarm_example()
        # Fixed route can attain 'alarm' before t=1, but losing 'alarm' and
        # 'wire' at t=1 prevents any post-fault success without construction.
        self.run_both(example, {}, construction=False)

    def test_common_cause_fault_which_kills_sensor(self):
        example = alarm_example()
        fault = replace(example.fault, remove=example.fault.remove | {"sensor"})
        self.run_both(replace(example, fault=fault), {})

    def test_fault_disables_optical_construction(self):
        example = alarm_example()
        # To avoid pre-building it, additionally delete any pre-built optical.
        fault = replace(example.fault, remove=example.fault.remove | {"optical"},
                        disable=frozenset({"build_optical"}))
        self.run_both(replace(example, fault=fault), {})

    def test_stock_destroyed_at_tick_zero(self):
        example = alarm_example()
        fault = Fault(0, frozenset({"wire","alarm"}), (1,))
        self.run_both(replace(example, fault=fault), {})

    def test_deferred_construction_avoids_stock_loss(self):
        example = alarm_example()
        # Destroying all kit at t=1 makes advance building optimal. Optical
        # capability is NOT destroyed, so the early construction survives.
        fault = replace(example.fault, destroy=(1,))
        self.run_both(replace(example, fault=fault), {"alarm":2})

    def test_fault_at_horizon_prevents_spurious_early_success(self):
        example = alarm_example()
        fault = Fault(1, frozenset({"alarm","wire"}), (0,))
        self.run_both(replace(example, horizon=1, fault=fault), {})

    def test_stock_replenishment_and_repeatability(self):
        model = Model(
            initial=frozenset({"raw","machine"}),
            goals=frozenset({"goal"}), resources=("kit",), stock=(0,),
            actions=(
                Action("make_kit", frozenset({"raw"}), "kit_present", (0,), (1,), True),
                Action("use_kit", frozenset({"machine"}), "goal", (1,), (0,)),
            ),
            horizon=2, fault=Fault(0, frozenset(), (0,)))
        self.run_both(model, {"goal":2})

    def test_inventory_is_not_duplicated_between_action_alternatives(self):
        model = Model(
            initial=frozenset({"source"}),
            goals=frozenset({"g1","g2"}), resources=("kit",), stock=(1,),
            actions=(
                Action("one", frozenset({"source"}), "g1", (1,), (0,)),
                Action("two", frozenset({"source"}), "g2", (1,), (0,)),
            ), horizon=2, fault=Fault(0, frozenset(), (0,)))
        self.run_both(model, {"g1":1, "g2":1})
        # This is existential reachability per goal, not joint feasibility.

    def test_nonnegative_stock_and_valid_model(self):
        example = alarm_example()
        with self.assertRaises(ValueError):
            replace(example, stock=(-1,))
        with self.assertRaises(ValueError):
            replace(example, fault=replace(example.fault, tick=99))
        with self.assertRaises(ValueError):
            replace(example, resources=("kit","kit"))
        with self.assertRaises(ValueError):
            replace(example, fault=replace(example.fault, destroy=(-1,)))
        with self.assertRaises(ValueError):
            replace(example, actions=example.actions + (example.actions[0],))

    def test_seeded_randomized_cross_check(self):
        output = audit()
        self.assertEqual(output["solver_comparisons"],256)
        self.assertEqual(output["mismatches"],0)
        self.assertEqual(output["result"],"PASS")
        for model in generated(n=8):
            compare(model)

    def test_expected_manifest(self):
        expected = json.loads((Path(__file__).parents[1] /
                              "experiments" / "g2_expected.json").read_text(encoding="utf8"))
        self.assertEqual(audit(),expected)


if __name__ == "__main__":
    unittest.main()
