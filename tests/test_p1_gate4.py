"""G4 non-clairvoyant policy correctness checks; NOT empirical P1 evidence."""
from dataclasses import replace
from fractions import Fraction
import json
from pathlib import Path
import unittest

from experiments.p1_gate2 import Action, Fault, Model
from experiments.p1_gate4 import (Problem, Scenario, Choice, audit,
    clairvoyant_upper_bound, information_gap_example, optimal_state_dp,
    optimal_history_oracle, verify, generated)


class G4Tests(unittest.TestCase):
    def assert_agreement(self, problem):
        verify(problem)
        for enabled in (False, True):
            self.assertEqual(optimal_state_dp(problem, construction=enabled).value,
                             optimal_history_oracle(problem, construction=enabled).value)

    def test_known_information_gap_is_one_half(self):
        problem = information_gap_example()
        self.assert_agreement(problem)
        value = optimal_state_dp(problem, construction=True)
        self.assertEqual(value.value, Fraction(1, 2))
        self.assertEqual(len(value.prefix), 1)
        self.assertIn(value.prefix[0], ("prepare_a", "prepare_b"))
        self.assertEqual(clairvoyant_upper_bound(problem, construction=True), 1)

    def test_baseline_cannot_build_backup(self):
        problem = information_gap_example()
        self.assertEqual(optimal_state_dp(problem, construction=False).value, 0)
        self.assertEqual(clairvoyant_upper_bound(problem, construction=False), 0)

    def test_one_scenario_removes_information_gap(self):
        problem = information_gap_example()
        single = replace(problem, scenarios=(
            Scenario("A", Fraction(1), problem.scenarios[0].fault),))
        self.assert_agreement(single)
        self.assertEqual(optimal_state_dp(single, construction=True).value, 1)
        self.assertEqual(clairvoyant_upper_bound(single, construction=True), 1)

    def test_skewed_prior_changes_optimal_prefix(self):
        original = information_gap_example()
        weighted = replace(original, scenarios=(
            replace(original.scenarios[0], probability=Fraction(3, 4)),
            replace(original.scenarios[1], probability=Fraction(1, 4)),
        ))
        self.assert_agreement(weighted)
        result = optimal_state_dp(weighted, construction=True)
        self.assertEqual(result.value, Fraction(3, 4))
        self.assertEqual(result.prefix, ("prepare_a",))

    def test_immediate_observation_allows_scenario_adaptation(self):
        base_problem = information_gap_example()
        immediate = replace(base_problem,
            base=replace(base_problem.base, fault=Fault(0, frozenset(), (0,))),
            scenarios=tuple(replace(s, fault=replace(s.fault, tick=0,
                                                     destroy=(0,)))
                            for s in base_problem.scenarios))
        self.assert_agreement(immediate)
        self.assertEqual(optimal_state_dp(immediate, construction=True).value, 1)
        self.assertEqual(clairvoyant_upper_bound(immediate, construction=True), 1)

    def test_immediate_destruction_prevents_preparation(self):
        base_problem = information_gap_example()
        destroyed = replace(base_problem,
            base=replace(base_problem.base, fault=Fault(0, frozenset(), (1,))),
            scenarios=tuple(replace(s, fault=replace(s.fault, tick=0))
                            for s in base_problem.scenarios))
        self.assert_agreement(destroyed)
        self.assertEqual(optimal_state_dp(destroyed, construction=True).value, 0)

    def test_no_remaining_time_blocks_goal(self):
        original = information_gap_example()
        short = replace(original, base=replace(original.base, horizon=1))
        self.assert_agreement(short)
        self.assertEqual(optimal_state_dp(short, construction=True).value, 0)

    def test_fault_removing_prepared_channel(self):
        original = information_gap_example()
        broken = replace(original, scenarios=tuple(
            replace(s, fault=replace(s.fault,
                remove=frozenset({"channel_a", "channel_b"})))
            for s in original.scenarios))
        self.assert_agreement(broken)
        self.assertEqual(optimal_state_dp(broken, construction=True).value, 0)

    def test_joint_goal_requires_joint_resource_feasibility(self):
        base = Model(frozenset({"base"}), frozenset({"g1", "g2"}),
            ("kit",), (1,),
            (Action("first", frozenset({"base"}), "g1", (1,), (0,)),
             Action("second", frozenset({"base"}), "g2", (1,), (0,))),
            2, Fault(0, frozenset(), (0,)))
        single = Problem(base, (
            Scenario("safe", Fraction(1), base.fault),))
        self.assert_agreement(single)
        self.assertEqual(optimal_state_dp(single, construction=True).value, 0)
        two_kits = replace(single, base=replace(base, stock=(2,)))
        self.assert_agreement(two_kits)
        self.assertEqual(optimal_state_dp(two_kits, construction=True).value, 1)

    def test_probability_and_fault_contracts(self):
        original = information_gap_example()
        with self.assertRaises(ValueError):
            replace(original, scenarios=())
        with self.assertRaises(ValueError):
            replace(original, scenarios=(original.scenarios[0],))
        with self.assertRaises(ValueError):
            replace(original, scenarios=(original.scenarios[0],
                                         original.scenarios[0]))
        with self.assertRaises(ValueError):
            replace(original, scenarios=(Scenario("x", Fraction(0),
                                                   original.scenarios[0].fault),
                                         Scenario("y", Fraction(1),
                                                   original.scenarios[1].fault)))
        with self.assertRaises(ValueError):
            replace(original, scenarios=(Scenario("x", Fraction(1, 2),
                                                   Fault(0, frozenset(), (0,))),
                                         original.scenarios[1]))
        with self.assertRaises(ValueError):
            replace(original, scenarios=(Scenario("x", Fraction(1, 2),
                                                   Fault(1, frozenset(), ())),
                                         original.scenarios[1]))

    def test_invariance_under_scenario_permutation(self):
        original = information_gap_example()
        reordered = replace(original, scenarios=tuple(reversed(original.scenarios)))
        self.assert_agreement(reordered)
        for enabled in (True, False):
            self.assertEqual(optimal_state_dp(original, construction=enabled).value,
                             optimal_state_dp(reordered, construction=enabled).value)

    def test_fixed_seed_diagnostic_and_archived_manifest(self):
        expected = json.loads((Path(__file__).parents[1] /
            "experiments" / "g4_expected.json").read_text(encoding="utf-8"))
        self.assertEqual(audit(), expected)
        self.assertEqual(expected["oracle_dp_comparisons"], 160)
        self.assertEqual(expected["mismatches"], 0)

    def test_seeded_small_extra_models(self):
        for p in generated(n=8):
            self.assert_agreement(p)


if __name__ == "__main__":
    unittest.main()
