"""B2 bounded observable trace language and explicit non-equivalence controls."""
from dataclasses import replace
import unittest

from experiments.p1_gate2 import Action
from experiments.p1_r16b_semantic_conformance import (
    constructive_goal_fixture, renamed_fixture,
)
from experiments.p1_r16c_bounded_trace_equivalence import (
    audit, compare_profiles, trace_language,
)


class B2BoundedEquivalenceTests(unittest.TestCase):
    def setUp(self):
        self.base = constructive_goal_fixture()

    def test_audit_is_developer_only(self):
        d = audit()
        self.assertEqual(d["comparison_count"], 8)
        self.assertTrue(d["equivalence_depends_on_horizon"])
        self.assertTrue(d["equivalence_depends_on_observation_projection"])
        self.assertEqual(d["confirmatory_h1_samples"], 0)
        self.assertEqual(d["sealed_family_calls"], 0)
        self.assertFalse(d["H1_preregistered"])

    def test_identity_is_reflexive_for_both_arms(self):
        r = compare_profiles(self.base, self.base)
        self.assertTrue(r.ordinary_equal)
        self.assertTrue(r.constructive_equal)

    def test_exact_alias_and_inert_self_loop_leave_language_unchanged(self):
        alias = replace(self.base, actions=self.base.actions + (
            replace(self.base.actions[0], name="alias"),
            Action("inert", frozenset({"seed"}), "seed", (0,), (0,)),
        ))
        r = compare_profiles(self.base, alias)
        self.assertTrue(r.ordinary_equal)
        self.assertTrue(r.constructive_equal)
        self.assertFalse(r.as_dict()["physical_mechanism_identity_proven"])

    def test_declared_capability_bijection_preserves_language(self):
        named = renamed_fixture(self.base, {
            "seed": "root", "bridge": "relay", "service": "objective",
        })
        r = compare_profiles(
            self.base, named,
            left_visible={"service": "goal"},
            right_visible={"objective": "goal"},
        )
        self.assertTrue(r.ordinary_equal)
        self.assertTrue(r.constructive_equal)

    def test_same_gog_different_reach_time_not_equivalent(self):
        fast = replace(self.base, actions=(
            Action("one_tick_goal", frozenset({"seed"}), "service",
                   (1,), (0,), True),
        ))
        r = compare_profiles(fast, self.base)
        self.assertEqual((r.gog_left, r.gog_right), (1, 1))
        self.assertTrue(r.ordinary_equal)
        self.assertFalse(r.constructive_equal)

    def test_same_gog_different_resource_trajectory_not_equivalent(self):
        free = replace(self.base, actions=(
            replace(self.base.actions[0], consumes=(0,)),
            self.base.actions[1],
        ))
        r = compare_profiles(self.base, free)
        self.assertEqual((r.gog_left, r.gog_right), (1, 1))
        self.assertFalse(r.constructive_equal)

    def test_time_horizon_cannot_be_silently_extended(self):
        stalled = replace(self.base, actions=(
            replace(self.base.actions[0], produces="dead_end"),
            self.base.actions[1],
        ))
        short = compare_profiles(
            replace(self.base, horizon=1), replace(stalled, horizon=1))
        long = compare_profiles(self.base, stalled)
        self.assertTrue(short.ordinary_equal)
        self.assertTrue(short.constructive_equal)
        self.assertTrue(long.ordinary_equal)
        self.assertFalse(long.constructive_equal)

    def test_observer_scope_changes_equivalence(self):
        hidden = replace(self.base, actions=self.base.actions + (
            Action("extra", frozenset({"seed"}), "secret",
                   (0,), (0,)),
        ))
        invisible = compare_profiles(self.base, hidden)
        visible = compare_profiles(
            self.base, hidden,
            left_visible={"service": "service", "secret": "secret"},
            right_visible={"service": "service", "secret": "secret"},
        )
        self.assertTrue(invisible.constructive_equal)
        self.assertFalse(visible.constructive_equal)

    def test_equal_trace_language_does_not_prove_fixed_policy_equivalence(self):
        r = compare_profiles(self.base, self.base).as_dict()
        self.assertFalse(r["fixed_policy_equivalence_proven"])
        self.assertFalse(r["unbounded_bisimulation_proven"])

    def test_disallow_different_horizon(self):
        with self.assertRaises(ValueError):
            compare_profiles(self.base, replace(self.base, horizon=1))

    def test_disallow_changed_resource_axis(self):
        bad = replace(self.base, resources=("other_resource",))
        with self.assertRaises(ValueError):
            compare_profiles(self.base, bad)

    def test_disallow_different_target_query(self):
        changed = replace(self.base, goals=frozenset({"bridge", "service"}))
        with self.assertRaises(ValueError):
            compare_profiles(self.base, changed)

    def test_reject_goal_hidden_from_observer(self):
        with self.assertRaises(ValueError):
            trace_language(self.base, construction=True,
                           visible_aliases={"bridge": "bridge"})

    def test_reject_colliding_observer_names(self):
        with self.assertRaises(ValueError):
            trace_language(
                self.base, construction=True,
                visible_aliases={"service": "same", "bridge": "same"})

    def test_reject_different_canonical_observer_vocabulary(self):
        with self.assertRaises(ValueError):
            compare_profiles(
                self.base, self.base,
                left_visible={"service": "one"},
                right_visible={"service": "two"})

    def test_faults_must_not_masquerade_as_b2_equivalence(self):
        with self.assertRaises(ValueError):
            trace_language(
                replace(self.base, fault=replace(
                    self.base.fault, remove=frozenset({"seed"}))),
                construction=True)

    def test_work_caps_are_strict(self):
        with self.assertRaises(ValueError):
            trace_language(replace(self.base, horizon=5), construction=True)
        with self.assertRaises(ValueError):
            trace_language(replace(
                self.base, actions=self.base.actions * 4),
                construction=True)

    def test_all_traces_include_tick_zero_and_exact_horizon(self):
        t = trace_language(self.base, construction=True)
        self.assertGreater(len(t), 0)
        self.assertTrue(all(len(history) == self.base.horizon + 1
                            for history in t))
        self.assertTrue(all(history[0] == ((), (1,)) for history in t))

    def test_constructive_arm_contains_service_goal_trajectory(self):
        lang = trace_language(self.base, construction=True)
        self.assertTrue(any("service" in frame[0] for tr in lang
                            for frame in tr))
        empty = trace_language(self.base, construction=False)
        self.assertFalse(any("service" in frame[0] for tr in empty
                             for frame in tr))


if __name__ == "__main__":
    unittest.main()
