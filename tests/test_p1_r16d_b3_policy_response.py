"""B3 bounded action-observation response and fixed policy controls."""
from dataclasses import replace
import unittest

from experiments.p1_gate2 import Action, Fault
from experiments.p1_r16b_semantic_conformance import constructive_goal_fixture
from experiments.p1_r16c_bounded_trace_equivalence import compare_profiles
from experiments.p1_r16d_b3_policy_response import (
    PROFILE, ReactivePolicy, audit, compare, execute_reactive,
    response_language, _ambiguous_routes_fixture, _stock_alias_fixture,
)


class B3CommandResponseTests(unittest.TestCase):
    def setUp(self):
        self.left, self.right = _ambiguous_routes_fixture()

    def test_audit_stays_provisional_and_sealed(self):
        d = audit()
        self.assertEqual(d["profile"], PROFILE)
        self.assertEqual(d["result"],
                         "PASS_PROVISIONAL_COMMAND_RESPONSE_CONFORMANCE")
        self.assertFalse(d["H1_preregistered"])
        self.assertEqual(d["confirmatory_H1_samples"], 0)
        self.assertEqual(d["sealed_family_calls"], 0)

    def test_reflexivity_for_both_arms(self):
        x = compare(self.left, self.left)
        self.assertTrue(x.ordinary_equal)
        self.assertTrue(x.constructive_equal)

    def test_b2_equal_while_canonical_commands_differ(self):
        weak = compare_profiles(self.left, self.right)
        strong = compare(self.left, self.right)
        self.assertTrue(weak.ordinary_equal)
        self.assertTrue(weak.constructive_equal)
        self.assertTrue(strong.b2_ordinary_equal)
        self.assertTrue(strong.b2_constructive_equal)
        self.assertFalse(strong.ordinary_equal)
        self.assertFalse(strong.constructive_equal)
        self.assertIsNotNone(strong.first_ordinary_mismatch)

    def test_same_stock_trace_language_different_action_cost(self):
        left, right = _stock_alias_fixture()
        result = compare(left, right)
        self.assertTrue(result.b2_ordinary_equal)
        self.assertTrue(result.b2_constructive_equal)
        self.assertFalse(result.ordinary_equal)
        self.assertFalse(result.constructive_equal)

    def test_same_nonanticipative_controller_can_diverge(self):
        policy = ReactivePolicy(probe="probe", fallback="primary",
                                goal="service")
        left = execute_reactive(self.left, policy, construction=False)
        right = execute_reactive(self.right, policy, construction=False)
        self.assertEqual(left[0], ("probe", "WAIT"))
        self.assertEqual(right[0], ("probe", "primary"))
        self.assertNotEqual(left[1], right[1])
        self.assertEqual(left[1][1][0][0], True)
        self.assertEqual(right[1][1][0][0], True)

    def test_reactive_controller_gets_public_history_only(self):
        policy = ReactivePolicy("probe", "primary", "service")
        self.assertEqual(policy.choose((((), (1,)),)), "probe")
        self.assertEqual(policy.choose((((), (1,)), ((), (1,)))),
                         "primary")
        self.assertEqual(policy.choose((((), (1,)),
                                        (("service",), (1,)))), "WAIT")

    def test_command_rejection_is_visible_and_does_not_consume_stock(self):
        model = constructive_goal_fixture()
        out = response_language(model, construction=False)
        response = out[("build_bridge", "provide")]
        self.assertEqual(response[0], ((), (1,)))
        self.assertFalse(response[1][0][0])
        self.assertFalse(response[1][1][0])
        self.assertEqual(response[1][1][1], ((), (1,)))

    def test_construction_enabled_produces_service_on_one_history(self):
        model = constructive_goal_fixture()
        out = response_language(model, construction=True)
        response = out[("build_bridge", "provide")]
        self.assertEqual(response[1][0], (True, ((), (0,))))
        self.assertEqual(response[1][1], (True, (("service",), (0,))))

    def test_canonical_action_renaming_supported_only_if_explicit(self):
        model = constructive_goal_fixture()
        renamed = replace(model, actions=(
            replace(model.actions[0], name="create"),
            replace(model.actions[1], name="deliver"),
        ))
        with self.assertRaises(ValueError):
            compare(model, renamed)
        matched = compare(
            model, renamed,
            left_actions={"build_bridge": "build", "provide": "serve"},
            right_actions={"create": "build", "deliver": "serve"},
        )
        self.assertTrue(matched.ordinary_equal)
        self.assertTrue(matched.constructive_equal)

    def test_absent_action_map_entry_is_rejected(self):
        with self.assertRaises(ValueError):
            response_language(self.left, construction=True,
                              action_aliases={"primary": "one"})

    def test_colliding_or_wait_action_mapping_is_rejected(self):
        for mapping in (
            {"primary": "same", "probe": "same"},
            {"primary": "WAIT", "probe": "probe"},
        ):
            with self.assertRaises(ValueError):
                response_language(self.left, construction=True,
                                  action_aliases=mapping)

    def test_mismatched_command_alphabet_is_not_equivalence_query(self):
        mismatch = replace(self.right, actions=self.right.actions + (
            Action("new", frozenset({"seed"}), "service", (0,), (0,)),
        ))
        with self.assertRaises(ValueError):
            compare(self.left, mismatch)

    def test_different_initial_resource_stock_rejected(self):
        with self.assertRaises(ValueError):
            compare(self.left, replace(self.right, stock=(0,)))

    def test_different_resource_axis_rejected(self):
        with self.assertRaises(ValueError):
            compare(self.left, replace(self.right, resources=("fuel",)))

    def test_different_horizon_rejected(self):
        with self.assertRaises(ValueError):
            compare(self.left, replace(self.right, horizon=1))

    def test_changed_goal_query_rejected(self):
        with self.assertRaises(ValueError):
            compare(self.left, replace(self.right, goals=frozenset({"seed"})))

    def test_observable_alias_collision_rejected(self):
        with self.assertRaises(ValueError):
            response_language(
                self.left, construction=True,
                visible_aliases={"service": "x", "seed": "x"})

    def test_faulted_model_cannot_be_relabeled_no_shock(self):
        with self.assertRaises(ValueError):
            response_language(
                replace(self.left, fault=Fault(1, frozenset({"seed"}), (0,))),
                construction=True)

    def test_unbounded_horizon_is_rejected(self):
        with self.assertRaises(ValueError):
            response_language(replace(self.left, horizon=4),
                              construction=True)

    def test_no_fabricated_physical_or_stochastic_equivalence(self):
        result = compare(self.left, self.left).as_dict()
        self.assertFalse(result["proves_physical_identity"])
        self.assertFalse(result["proves_unbounded_bisimulation"])
        self.assertFalse(result["proves_stochastic_nonanticipative_equivalence"])

    def test_unregistered_controller_command_rejected(self):
        with self.assertRaises(ValueError):
            execute_reactive(self.left,
                             ReactivePolicy("unknown", "primary", "service"),
                             construction=False)

    def test_unregistered_controller_goal_rejected(self):
        with self.assertRaises(ValueError):
            execute_reactive(self.left,
                             ReactivePolicy("probe", "primary", "secret"),
                             construction=False)

    def test_result_covers_all_bounded_command_words(self):
        x = response_language(self.left, construction=True)
        self.assertEqual(len(x), 9)
        self.assertEqual(set(len(word) for word in x), {2})
        self.assertTrue(all(len(v[1]) == 2 for v in x.values()))


if __name__ == "__main__":
    unittest.main()
