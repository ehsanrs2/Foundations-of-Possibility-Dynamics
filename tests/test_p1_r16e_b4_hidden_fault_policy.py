"""B4 hidden-event and observation-adapted controller conformance tests."""
from dataclasses import replace
from fractions import Fraction
import unittest

from experiments.p1_gate2 import Action, Fault
from experiments.p1_r16e_b4_hidden_fault_policy import (
    Scenario, World, PROFILE, audit, compare_worlds, response_law,
    belief_dp_value, history_oracle_value, hidden_repair_fixture,
    unknown_time_fixture,
)


class B4HiddenFaultTests(unittest.TestCase):
    def setUp(self):
        self.hidden = hidden_repair_fixture()

    def test_scientific_boundary_and_diagnostic(self):
        report = audit()
        self.assertEqual(report["profile"], PROFILE)
        self.assertEqual(report["result"],
                         "PASS_PROVISIONAL_HIDDEN_FAULT_POLICY_CONFORMANCE")
        self.assertEqual(report["outcome"],
                         "TERMINAL_SERVICE_PRESENT_NOT_STRICT_H1_RESTORATION")
        self.assertEqual(report["confirmatory_H1_samples"], 0)
        self.assertEqual(report["sealed_family_calls"], 0)
        self.assertFalse(report["H1_preregistered"])

    def test_same_world_is_reflexive_both_construction_arms(self):
        x = compare_worlds(self.hidden, self.hidden)
        self.assertTrue(x.ordinary_equal)
        self.assertTrue(x.constructive_equal)

    def test_b3_no_fault_equal_b4_hidden_fault_different(self):
        protected = World(self.hidden.base, tuple(
            replace(s, fault=replace(s.fault, disable=frozenset()))
            for s in self.hidden.scenarios))
        x = compare_worlds(self.hidden, protected)
        self.assertTrue(x.no_fault_b3_ordinary_equal)
        self.assertTrue(x.no_fault_b3_constructive_equal)
        self.assertFalse(x.ordinary_equal)
        self.assertFalse(x.constructive_equal)
        self.assertIsNotNone(x.first_ordinary_disagreement)
        self.assertIsNotNone(x.first_constructive_disagreement)

    def test_hidden_fault_optimal_not_clairvoyant(self):
        self.assertEqual(belief_dp_value(self.hidden, "service"),
                         Fraction(1, 2))
        self.assertEqual(history_oracle_value(self.hidden, "service"),
                         Fraction(1, 2))
        self.assertLess(belief_dp_value(self.hidden, "service"), 1)

    def test_both_arms_match_independent_policy_history_oracle(self):
        for enabled in (False, True):
            self.assertEqual(
                belief_dp_value(self.hidden, "service", construction=enabled),
                history_oracle_value(self.hidden, "service",
                                     construction=enabled))

    def test_observable_fault_sensor_enables_recourse(self):
        revealed = hidden_repair_fixture(reveal_sensors=True)
        sensors = {"service": "service", "sensor_a": "a_seen",
                   "sensor_b": "b_seen"}
        self.assertEqual(belief_dp_value(
            revealed, "service", visible_aliases=sensors), 1)
        self.assertEqual(history_oracle_value(
            revealed, "service", visible_aliases=sensors), 1)
        self.assertEqual(belief_dp_value(
            revealed, "service"), Fraction(1, 2))

    def test_unknown_fault_time_never_supplied_as_policy_input(self):
        world = unknown_time_fixture()
        self.assertEqual(belief_dp_value(world, "service"),
                         history_oracle_value(world, "service"))
        self.assertEqual(belief_dp_value(world, "service"), 1)

    def test_null_effect_event_is_not_announced(self):
        world = unknown_time_fixture()
        ghost = World(world.base, tuple(
            replace(s, fault=replace(s.fault, remove=frozenset({"ghost"})))
            for s in world.scenarios))
        inert = World(world.base, tuple(
            replace(s, fault=replace(s.fault, remove=frozenset()))
            for s in world.scenarios))
        x = compare_worlds(ghost, inert)
        self.assertTrue(x.ordinary_equal)
        self.assertTrue(x.constructive_equal)

    def test_open_loop_law_mass_conservation(self):
        for enabled in (False, True):
            distributions = response_law(
                unknown_time_fixture(), construction=enabled)
            self.assertEqual(len(distributions), 8)
            self.assertTrue(all(
                sum(weights.values(), Fraction()) == 1
                for weights in distributions.values()))

    def test_scenario_identity_and_fault_tick_are_hidden_from_response(self):
        dist = response_law(self.hidden, construction=False)
        serialized = repr(dist)
        self.assertNotIn("fault_a", serialized)
        self.assertNotIn("fault_b", serialized)
        self.assertTrue(all(len(word) == self.hidden.base.horizon
                            for word in dist))

    def test_canonical_action_rename_respects_fault_disable(self):
        original = self.hidden.base
        renamed = replace(original, actions=(
            replace(original.actions[0], name="left"),
            replace(original.actions[1], name="right")))
        cases = (
            replace(self.hidden.scenarios[0],
                    fault=replace(self.hidden.scenarios[0].fault,
                                  disable=frozenset({"left"}))),
            replace(self.hidden.scenarios[1],
                    fault=replace(self.hidden.scenarios[1].fault,
                                  disable=frozenset({"right"}))),
        )
        changed = World(renamed, cases)
        x = compare_worlds(
            self.hidden, changed,
            left_actions={"a": "repair_a", "b": "repair_b"},
            right_actions={"left": "repair_a", "right": "repair_b"})
        self.assertTrue(x.ordinary_equal)
        self.assertTrue(x.constructive_equal)
        self.assertEqual(
            belief_dp_value(changed, "service",
                            action_aliases={"left": "repair_a",
                                            "right": "repair_b"}),
            Fraction(1, 2))

    def test_reject_changed_scenario_probabilities_before_comparison(self):
        changed = World(self.hidden.base, (
            replace(self.hidden.scenarios[0], probability=Fraction(3, 4)),
            replace(self.hidden.scenarios[1], probability=Fraction(1, 4))))
        with self.assertRaises(ValueError):
            compare_worlds(self.hidden, changed)

    def test_reject_changed_scenario_names_before_comparison(self):
        changed = World(self.hidden.base, (
            replace(self.hidden.scenarios[0], name="unmatched"),
            self.hidden.scenarios[1]))
        with self.assertRaises(ValueError):
            compare_worlds(self.hidden, changed)

    def test_reject_probabilities_not_summing_to_one(self):
        bad = World(self.hidden.base, (
            replace(self.hidden.scenarios[0], probability=Fraction(1, 3)),
            self.hidden.scenarios[1]))
        with self.assertRaises(ValueError):
            response_law(bad, construction=False)

    def test_reject_non_exact_probabilities(self):
        bad = World(self.hidden.base, (
            replace(self.hidden.scenarios[0], probability=0.5),
            self.hidden.scenarios[1]))
        with self.assertRaises(ValueError):
            belief_dp_value(bad, "service")

    def test_reject_duplicate_scenario_names(self):
        bad = World(self.hidden.base, (
            self.hidden.scenarios[0],
            replace(self.hidden.scenarios[1], name="fault_a")))
        with self.assertRaises(ValueError):
            response_law(bad, construction=False)

    def test_reject_fault_at_unmodelled_terminal_tick(self):
        bad = World(self.hidden.base, (
            replace(self.hidden.scenarios[0], fault=replace(
                self.hidden.scenarios[0].fault, tick=2)),
            self.hidden.scenarios[1]))
        with self.assertRaises(ValueError):
            response_law(bad, construction=False)

    def test_reject_unknown_disabled_action_identifier(self):
        bad = World(self.hidden.base, (
            replace(self.hidden.scenarios[0], fault=replace(
                self.hidden.scenarios[0].fault,
                disable=frozenset({"unknown"}))),
            self.hidden.scenarios[1]))
        with self.assertRaises(ValueError):
            response_law(bad, construction=False)

    def test_reject_inconsistent_resource_damage_vector(self):
        bad = World(self.hidden.base, (
            replace(self.hidden.scenarios[0], fault=replace(
                self.hidden.scenarios[0].fault, destroy=(0, 0))),
            self.hidden.scenarios[1]))
        with self.assertRaises(ValueError):
            belief_dp_value(bad, "service")

    def test_reject_nonidentical_canonical_goal_query(self):
        altered = replace(self.hidden.base, goals=frozenset({"seed"}))
        with self.assertRaises(ValueError):
            compare_worlds(self.hidden, World(altered, self.hidden.scenarios))

    def test_reject_unregistered_goal_optimization(self):
        with self.assertRaises(ValueError):
            belief_dp_value(self.hidden, "not_registered")
        with self.assertRaises(ValueError):
            history_oracle_value(self.hidden, "not_registered")

    def test_reject_invalid_observer_projection(self):
        with self.assertRaises(ValueError):
            response_law(
                self.hidden, construction=False,
                visible_aliases={"seed": "seed"})

    def test_reject_too_large_or_inert_base_model_fault(self):
        future = replace(self.hidden.base, horizon=4)
        with self.assertRaises(ValueError):
            response_law(World(future, self.hidden.scenarios),
                         construction=False)
        corrupted = replace(self.hidden.base, fault=Fault(
            0, frozenset({"seed"}), (0,)))
        with self.assertRaises(ValueError):
            response_law(World(corrupted, self.hidden.scenarios),
                         construction=False)


if __name__ == "__main__":
    unittest.main()
