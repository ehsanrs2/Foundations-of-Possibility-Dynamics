"""B1 developer GOG contract controls. No field, H1 or held-out generation."""
from dataclasses import replace
import unittest

from experiments.p1_gate2 import Action, Fault
from experiments.p1_gate3 import augmented_solver
from experiments.p1_r16a_architecture_audit import audit as architecture_audit
from experiments.p1_r16b_semantic_conformance import (
    PROFILE, audit, evaluate_gog, constructive_goal_fixture,
    backup_only_fixture, mutually_exclusive_goals_fixture, renamed_fixture,
)


class B1OperationalSemanticsTests(unittest.TestCase):
    def setUp(self):
        self.base = constructive_goal_fixture()

    def test_audit_is_software_only_and_provisional(self):
        a = audit()
        self.assertEqual(a["profile"], PROFILE)
        self.assertEqual(a["status"], "PASS_PROVISIONAL_DEVELOPER_CONFORMANCE")
        self.assertFalse(a["primary_H1_test"])
        self.assertEqual(a["confirmatory_H1_samples"], 0)
        self.assertEqual(a["sealed_family_calls"], 0)

    def test_constructible_goal_is_newly_reachable(self):
        r = evaluate_gog(self.base)
        self.assertEqual(r.ordinary, ())
        self.assertEqual(r.constructive, ("service",))
        self.assertEqual(r.newly_reachable, ("service",))
        self.assertEqual(r.gog, 1)

    def test_constructed_backup_to_old_goal_is_not_gog(self):
        r = evaluate_gog(backup_only_fixture())
        self.assertEqual(r.ordinary, ("service",))
        self.assertEqual(r.constructive, ("service",))
        self.assertEqual(r.gog, 0)

    def test_time_window_makes_construction_nonfeasible(self):
        self.assertEqual(evaluate_gog(replace(self.base, horizon=1)).gog, 0)

    def test_inventory_makes_construction_nonfeasible(self):
        self.assertEqual(evaluate_gog(replace(self.base, stock=(0,))).gog, 0)

    def test_individual_gog_does_not_assert_joint_attainability(self):
        one = mutually_exclusive_goals_fixture(stock=1)
        two = mutually_exclusive_goals_fixture(stock=2)
        self.assertEqual(evaluate_gog(one).gog, 2)
        self.assertEqual(augmented_solver(one, construction=True).joint, None)
        self.assertEqual(augmented_solver(two, construction=True).joint, 2)

    def test_semantics_preserving_alias_does_not_inflate_gog(self):
        alt = replace(self.base, actions=self.base.actions + (
            Action("alias", frozenset({"seed"}), "bridge", (1,), (0,), True),
            Action("inert", frozenset({"seed"}), "seed", (0,), (0,)),
        ))
        self.assertEqual(evaluate_gog(alt), evaluate_gog(self.base))

    def test_goal_vocabulary_change_must_be_declared(self):
        altered_query = replace(self.base, goals=frozenset({"bridge", "service"}))
        self.assertEqual(evaluate_gog(self.base).gog, 1)
        self.assertEqual(evaluate_gog(altered_query).gog, 2)

    def test_bijective_capability_renaming_does_not_change_gog(self):
        mapping = {"seed": "root", "bridge": "relay", "service": "objective"}
        renamed = renamed_fixture(self.base, mapping)
        self.assertEqual(evaluate_gog(renamed).gog, evaluate_gog(self.base).gog)
        self.assertEqual(evaluate_gog(renamed).newly_reachable, ("objective",))

    def test_incomplete_or_colliding_mapping_fails(self):
        with self.assertRaises(ValueError):
            renamed_fixture(self.base, {"seed": "root", "bridge": "relay"})
        with self.assertRaises(ValueError):
            renamed_fixture(self.base, {"seed": "same", "bridge": "same", "service": "x"})

    def test_faulted_profile_must_not_masquerade_as_prefault_gog(self):
        with self.assertRaises(ValueError):
            evaluate_gog(replace(self.base,
                fault=Fault(1, frozenset({"service"}), (0,))))

    def test_resource_destroying_fault_must_be_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_gog(replace(self.base,
                fault=Fault(0, frozenset(), (1,))))

    def test_disabled_action_fault_must_be_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_gog(replace(self.base,
                fault=Fault(0, frozenset(), (0,), frozenset({"provide"}))))

    def test_empty_target_query_must_be_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_gog(replace(self.base, goals=frozenset()))

    def test_bounded_oracle_refuses_unbounded_workload(self):
        with self.assertRaises(ValueError):
            evaluate_gog(replace(self.base, horizon=7))
        with self.assertRaises(ValueError):
            evaluate_gog(replace(self.base, stock=(5,)))

    def test_nongenerative_only_model_cannot_have_gog(self):
        only = replace(self.base, actions=tuple(
            replace(a, generative=False) for a in self.base.actions))
        self.assertEqual(evaluate_gog(only).gog, 0)

    def test_B1_does_not_promote_architecture_to_preregistered_H1(self):
        result = architecture_audit()
        self.assertEqual(result["result"], "PASS_PROPOSAL_CONSISTENCY_ONLY")
        self.assertFalse(result["confirmatory_H1_permitted"])


if __name__ == "__main__":
    unittest.main()
