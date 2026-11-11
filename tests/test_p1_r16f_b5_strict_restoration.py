"""B5: synthetic actual-loss, delayed-sensing and censoring safeguards."""
from dataclasses import replace
from fractions import Fraction
import unittest

from experiments.p1_gate2 import Action, Fault
from experiments.p1_r16e_b4_hidden_fault_policy import Scenario, World
from experiments.p1_r16f_b5_strict_restoration import (
    PROFILE, CENSORED, RESTORED, NOT_AT_RISK, NOT_RESTORED,
    audit, execute, independent_history_oracle, summarize, fixture,
)


class B5StrictRestorationTests(unittest.TestCase):
    def setUp(self):
        self.world = fixture()
        self.early, self.late, self.unaffected = self.world.scenarios

    def test_scientific_boundary(self):
        report = audit()
        self.assertEqual(report["profile"], PROFILE)
        self.assertEqual(report["result"],
                         "PASS_PROVISIONAL_SYNTHETIC_STRICT_RESTORATION_CONFORMANCE")
        self.assertEqual(report["confirmatory_H1_samples"], 0)
        self.assertEqual(report["sealed_family_calls"], 0)
        self.assertFalse(report["H1_preregistered"])
        self.assertFalse(report["real_physical_source_authenticated"])

    def test_fault_must_actually_remove_previous_goal(self):
        lost = execute(self.world, self.early)
        self.assertTrue(lost.held_before_fault)
        self.assertTrue(lost.lost_at_fault)
        self.assertEqual(lost.status, RESTORED)
        self.assertEqual(lost.first_regained_tick, 2)

    def test_unaffected_goal_is_not_a_restoration_success(self):
        r = execute(self.world, self.unaffected)
        self.assertTrue(r.held_before_fault)
        self.assertFalse(r.lost_at_fault)
        self.assertTrue(r.held_at_deadline)
        self.assertIsNone(r.first_regained_tick)
        self.assertEqual(r.status, NOT_AT_RISK)
        self.assertEqual(r.commands, ("WAIT", "WAIT", "WAIT"))

    def test_late_loss_does_not_fake_early_restoration(self):
        r = execute(self.world, self.late, lag=0)
        self.assertEqual(r.fault_tick, 2)
        self.assertEqual(r.first_regained_tick, 3)
        self.assertEqual(r.status, RESTORED)

    def test_delay_zero_all_actual_losses_recover(self):
        r = summarize(self.world, lag=0)
        self.assertEqual(r["status_mass"][RESTORED], "3/4")
        self.assertEqual(r["status_mass"][NOT_AT_RISK], "1/4")
        self.assertEqual(r["observed_case_success_fraction"], "1")

    def test_delay_one_misses_late_event(self):
        r = summarize(self.world, lag=1)
        self.assertEqual(r["status_mass"][RESTORED], "1/2")
        self.assertEqual(r["status_mass"][NOT_RESTORED], "1/4")
        self.assertEqual(r["observed_case_success_fraction"], "2/3")

    def test_delay_two_misses_both_losses(self):
        r = summarize(self.world, lag=2)
        self.assertEqual(r["status_mass"][NOT_RESTORED], "3/4")
        self.assertEqual(r["status_mass"][NOT_AT_RISK], "1/4")
        self.assertEqual(r["observed_case_success_fraction"], "0")

    def test_policy_never_receives_actual_fault_id(self):
        a = execute(self.world, self.early, lag=1)
        b = execute(self.world, self.late, lag=1)
        self.assertEqual(a.delivered_goal_signals, (True, True, False))
        self.assertEqual(b.delivered_goal_signals, (True, True, True))
        self.assertEqual(a.commands, ("WAIT", "WAIT", "repair"))
        self.assertEqual(b.commands, ("WAIT", "WAIT", "WAIT"))

    def test_same_lost_goal_after_fault_requires_full_execution_tick(self):
        r = execute(self.world, self.early, lag=0)
        self.assertEqual(r.first_regained_tick, r.fault_tick + 1)
        self.assertNotEqual(r.first_regained_tick, r.fault_tick)

    def test_followup_cutoff_censors_late_success_not_failure(self):
        r = execute(self.world, self.late, lag=0, followup_until=2)
        self.assertEqual(r.first_regained_tick, 3)
        self.assertTrue(r.held_at_deadline)
        self.assertEqual(r.status, CENSORED)

    def test_early_recovery_observed_before_cutoff(self):
        r = execute(self.world, self.early, lag=0, followup_until=2)
        self.assertEqual(r.status, RESTORED)
        self.assertEqual(r.first_regained_tick, 2)

    def test_censoring_changes_composition_not_true_effect(self):
        r = summarize(self.world, lag=0, followup_until=2)
        self.assertEqual(r["status_mass"][RESTORED], "1/2")
        self.assertEqual(r["status_mass"][CENSORED], "1/4")
        self.assertEqual(r["observed_eligible_mass"], "1/2")
        self.assertEqual(r["true_loss_risk_mass"], "3/4")
        self.assertEqual(r["observed_case_success_fraction"], "1")
        self.assertFalse(r["conditional_inference_validated"])

    def test_zero_observed_denominator_is_null(self):
        r = summarize(self.world, lag=1, followup_until=2)
        self.assertEqual(r["status_mass"][CENSORED], "3/4")
        self.assertEqual(r["observed_eligible_mass"], "0")
        self.assertIsNone(r["observed_case_success_fraction"])

    def test_no_actual_loss_yields_zero_risk_not_zero_recovery_rate(self):
        inert = World(self.world.base, (
            Scenario("only_inert", Fraction(1), self.unaffected.fault),))
        r = summarize(inert)
        self.assertEqual(r["status_mass"][NOT_AT_RISK], "1")
        self.assertEqual(r["true_loss_risk_mass"], "0")
        self.assertIsNone(r["observed_case_success_fraction"])

    def test_goal_never_active_is_not_at_risk_even_if_fault_removes_it(self):
        base = replace(self.world.base, initial=frozenset({"seed"}),
                       actions=(Action("repair", frozenset({"absent"}),
                                       "service", (0,), (0,)),))
        never = World(base, self.world.scenarios)
        r = execute(never, never.scenarios[0])
        self.assertFalse(r.held_before_fault)
        self.assertFalse(r.lost_at_fault)
        self.assertFalse(r.held_at_deadline)
        self.assertEqual(r.status, NOT_AT_RISK)

    def test_disabled_repair_is_negative_only_when_followed_to_deadline(self):
        case = replace(self.early, fault=replace(
            self.early.fault, disable=frozenset({"repair"})))
        world = World(self.world.base, (Scenario(
            "blocked", Fraction(1), case.fault),))
        self.assertEqual(execute(world, world.scenarios[0]).status, NOT_RESTORED)
        self.assertEqual(execute(
            world, world.scenarios[0], followup_until=2).status, CENSORED)

    def test_exact_independent_oracle_agrees_across_lags_and_cutoffs(self):
        comparisons = 0
        for lag in (0, 1, 2):
            for until in (0, 1, 2, 3):
                for case in self.world.scenarios:
                    self.assertEqual(
                        execute(self.world, case, lag=lag, followup_until=until),
                        independent_history_oracle(
                            self.world, case, lag=lag, followup_until=until))
                    comparisons += 1
        self.assertEqual(comparisons, 36)

    def test_observer_projection_can_hide_unrelated_capability(self):
        world = self.world
        base = replace(world.base, initial=world.base.initial | {"secret"})
        altered = World(base, world.scenarios)
        self.assertEqual(execute(altered, altered.scenarios[0]),
                         execute(world, world.scenarios[0]))

    def test_wrong_goal_or_undeclared_goal_fails(self):
        with self.assertRaises(ValueError):
            execute(self.world, self.early, goal="unknown")

    def test_missing_goal_sensor_fails(self):
        with self.assertRaises(ValueError):
            execute(self.world, self.early, visible={"seed": "seed"})

    def test_bad_observer_alias_fails(self):
        with self.assertRaises(ValueError):
            execute(self.world, self.early,
                    visible={"service": "x", "seed": "x"})

    def test_non_integer_or_invalid_delay_rejected(self):
        for lag in (-1, 3, 1.0, True):
            with self.subTest(lag=lag), self.assertRaises(ValueError):
                execute(self.world, self.early, lag=lag)

    def test_non_integer_and_future_followup_rejected(self):
        for value in (-1, 4, 2.5, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                execute(self.world, self.early, followup_until=value)

    def test_unregistered_scenario_rejected(self):
        fake = Scenario("unregistered", Fraction(1), self.early.fault)
        with self.assertRaises(ValueError):
            execute(self.world, fake)

    def test_repair_action_must_be_exact_same_goal(self):
        base = replace(self.world.base, actions=(
            Action("repair", frozenset({"seed"}), "different", (0,), (0,)),))
        altered = World(base, self.world.scenarios)
        with self.assertRaises(ValueError):
            execute(altered, altered.scenarios[0])

    def test_unvalidated_generator_or_multiple_rules_rejected(self):
        base = self.world.base
        generated = replace(base, actions=(replace(base.actions[0], generative=True),))
        with self.assertRaises(ValueError):
            execute(World(generated, self.world.scenarios),
                    self.world.scenarios[0])
        many = replace(base, actions=base.actions + (
            Action("other", frozenset({"seed"}), "service", (0,), (0,)),))
        with self.assertRaises(ValueError):
            execute(World(many, self.world.scenarios),
                    self.world.scenarios[0])

    def test_censor_does_not_override_known_no_loss(self):
        r = execute(self.world, self.unaffected, followup_until=0)
        self.assertEqual(r.status, NOT_AT_RISK)

    def test_no_data_used_for_confirmatory_inference(self):
        r = summarize(self.world)
        self.assertFalse(r["conditional_inference_validated"])
        self.assertFalse(r["H1_confirmatory_result"])


if __name__ == "__main__":
    unittest.main()
