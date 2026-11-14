"""B6 synthetic sensor error, exact risk label and evidence segregation."""
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction
import unittest

from experiments.p1_gate2 import Action, Fault
from experiments.p1_r16e_b4_hidden_fault_policy import Scenario, World
from experiments.p1_r16g_b6_noisy_sensor_evidence import (
    PROFILE, Sensor, RESTORED, NOT_RESTORED, NOT_AT_RISK, CENSORED,
    UNKNOWN_RISK, audit, execute, independent_replay,
    exact_distribution, evidence_record, verify_record, fixture,
)


class B6NoiseAndEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.world = fixture()
        self.loss, self.no_loss = self.world.scenarios
        self.perfect = Sensor(Fraction(1), Fraction(1))

    def test_scientific_gate_never_admits_H1(self):
        r = audit()
        self.assertEqual(r["profile"], PROFILE)
        self.assertEqual(r["H1_confirmatory_samples"], 0)
        self.assertEqual(r["physical_field_episodes_admitted"], 0)
        self.assertEqual(r["sealed_test_families_generated"], 0)
        self.assertFalse(r["H1_preregistered"])

    def test_perfect_observation_recovery_is_loss_conditional(self):
        x = exact_distribution(self.world, self.perfect)
        self.assertEqual(x["status_mass"][RESTORED], "1/2")
        self.assertEqual(x["status_mass"][NOT_AT_RISK], "1/2")
        self.assertEqual(x["status_mass"][NOT_RESTORED], "0")
        self.assertEqual(x["privileged_true_loss_mass"], "1/2")
        self.assertFalse(x["population_inference_validated"])

    def test_false_alarm_uses_up_resource_before_true_loss(self):
        sensor = Sensor(Fraction(1, 2), Fraction(1))
        r = exact_distribution(self.world, sensor)
        self.assertEqual(r["status_mass"][RESTORED], "1/4")
        self.assertEqual(r["status_mass"][NOT_RESTORED], "1/4")
        first = execute(self.world, self.loss, sensor, (False, True, True))
        self.assertEqual(first.policy_log[0][2], "repair")
        self.assertEqual(first.policy_log[1][2], "repair")
        self.assertFalse(first.policy_log[1][3])
        self.assertEqual(first.status, NOT_RESTORED)

    def test_false_presence_can_miss_late_recovery(self):
        sensor = Sensor(Fraction(1), Fraction(1, 2))
        r = exact_distribution(self.world, sensor)
        self.assertEqual(r["status_mass"][RESTORED], "3/8")
        self.assertEqual(r["status_mass"][NOT_RESTORED], "1/8")

    def test_delayed_perfect_observation_can_still_recover_by_horizon(self):
        r = exact_distribution(
            self.world, Sensor(Fraction(1), Fraction(1), 1))
        self.assertEqual(r["status_mass"][RESTORED], "1/2")
        z = execute(self.world, self.loss,
                    Sensor(Fraction(1), Fraction(1), 1), (True,) * 3)
        self.assertEqual(z.first_regained_tick, 3)
        self.assertEqual(z.policy_log[0][1], None)
        self.assertEqual(z.policy_log[1][1], True)
        self.assertEqual(z.policy_log[2][1], False)

    def test_delay_two_misses_terminal_deadline(self):
        r = exact_distribution(
            self.world, Sensor(Fraction(1), Fraction(1), 2))
        self.assertEqual(r["status_mass"][NOT_RESTORED], "1/2")

    def test_without_actual_loss_terminal_presence_is_not_a_success(self):
        z = execute(self.world, self.no_loss, self.perfect, (True,) * 3)
        self.assertEqual(z.status, NOT_AT_RISK)
        self.assertFalse(z.lost_at_fault)
        self.assertTrue(z.held_at_horizon)
        self.assertIsNone(z.first_regained_tick)

    def test_censor_before_observed_recovery(self):
        z = execute(self.world, self.loss, self.perfect, (True,) * 3,
                    followup_until=1)
        self.assertTrue(z.lost_at_fault)
        self.assertEqual(z.first_regained_tick, 2)
        self.assertEqual(z.status, CENSORED)
        r = exact_distribution(self.world, self.perfect, followup_until=1)
        self.assertEqual(r["status_mass"][CENSORED], "1/2")
        self.assertIsNone(r["observed_case_fraction_descriptive_only"])

    def test_cutoff_before_event_has_unknown_risk_not_not_at_risk(self):
        z = execute(self.world, self.no_loss, self.perfect, (True,) * 3,
                    followup_until=0)
        self.assertEqual(z.status, UNKNOWN_RISK)
        r = exact_distribution(self.world, self.perfect, followup_until=0)
        self.assertEqual(r["status_mass"][UNKNOWN_RISK], "1")
        self.assertEqual(r["observed_determinate_loss_mass"], "0")

    def test_full_followup_has_true_negative_label(self):
        z = execute(self.world, self.loss,
                    Sensor(Fraction(1), Fraction(1), 2),
                    (True,) * 3)
        self.assertTrue(z.lost_at_fault)
        self.assertEqual(z.status, NOT_RESTORED)

    def test_sensor_reports_are_not_true_goal_truth(self):
        z = execute(self.world, self.loss,
                    Sensor(Fraction(1, 2), Fraction(1)),
                    (False, True, True))
        self.assertTrue(z.true_samples[0])
        self.assertFalse(z.collected[0])
        self.assertFalse(z.policy_log[0][1])

    def test_sensor_lag_never_delivers_future_sample(self):
        z = execute(self.world, self.loss,
                    Sensor(Fraction(1), Fraction(1), 2),
                    (True, True, True))
        self.assertIsNone(z.policy_log[0][1])
        self.assertIsNone(z.policy_log[1][1])
        self.assertTrue(z.policy_log[2][1])

    def test_oracle_agreement_every_case_noise_word_lag_cutoff(self):
        count = 0
        for lag in range(3):
            sensor = Sensor(Fraction(1, 2), Fraction(2, 3), lag)
            for F in range(4):
                for case in self.world.scenarios:
                    for i in range(8):
                        bits = tuple(bool(i & (1 << j)) for j in range(3))
                        a = execute(self.world, case, sensor, bits,
                                    followup_until=F)
                        b = independent_replay(self.world, case, sensor, bits,
                                               followup_until=F)
                        self.assertEqual(a, b)
                        count += 1
        self.assertEqual(count, 192)

    def test_stipulated_joint_probability_mass_is_exact(self):
        r = exact_distribution(self.world,
                               Sensor(Fraction(2, 3), Fraction(3, 4), 1))
        weights = sum((Fraction(s) for s in r["status_mass"].values()),
                      Fraction())
        self.assertEqual(weights, 1)
        self.assertEqual(r["all_noise_scenario_pairs_crosschecked"], 16)

    def test_independent_sensor_noise_words_can_have_zero_probability(self):
        r = exact_distribution(self.world, self.perfect)
        self.assertEqual(r["all_noise_scenario_pairs_crosschecked"], 16)
        self.assertEqual(r["nonzero_weight_paths"], 2)

    def test_record_segregates_public_controller_from_privileged_truth(self):
        record = evidence_record(self.world, self.loss, self.perfect,
                                 (True,) * 3)
        self.assertTrue(verify_record(record))
        public = record["payload"]["public_controller_log"]
        self.assertEqual(len(public), 3)
        for frame in public:
            self.assertEqual(
                set(frame), {"tick", "reported_goal", "command", "accepted"})
            self.assertNotIn("fault", frame)
            self.assertNotIn("true_goal_precommand", frame)
        truth = record["payload"]["privileged_evaluator_log"]
        self.assertTrue(truth["actually_lost_at_fault"])
        self.assertEqual(truth["first_same_goal_regained_tick"], 2)

    def test_record_hash_is_repeatable_not_external_publisher_attestation(self):
        x = evidence_record(self.world, self.loss, self.perfect, (True,) * 3)
        y = evidence_record(self.world, self.loss, self.perfect, (True,) * 3)
        self.assertEqual(x["payload_sha256"], y["payload_sha256"])
        self.assertEqual(len(x["payload_sha256"]), 64)
        self.assertEqual(x["digest_role"], "LOCAL_REPRODUCIBILITY_ONLY")
        self.assertFalse(x["payload"]["external_publisher_attested"])
        self.assertFalse(x["payload"]["H1_admissible"])

    def test_mutated_controller_log_invalidates_stored_hash(self):
        z = evidence_record(self.world, self.loss, self.perfect, (True,) * 3)
        changed = deepcopy(z)
        changed["payload"]["public_controller_log"][0]["command"] = "repair"
        self.assertFalse(verify_record(changed))

    def test_mutated_privileged_truth_invalidates_stored_hash(self):
        z = evidence_record(self.world, self.loss, self.perfect, (True,) * 3)
        changed = deepcopy(z)
        changed["payload"]["privileged_evaluator_log"]["actually_lost_at_fault"] = False
        self.assertFalse(verify_record(changed))

    def test_fake_publisher_attestation_does_not_validate(self):
        z = evidence_record(self.world, self.loss, self.perfect, (True,) * 3)
        changed = deepcopy(z)
        changed["payload"]["external_publisher_attested"] = True
        self.assertFalse(verify_record(changed))

    def test_sensor_probabilities_must_be_exact_and_bounded(self):
        for sensor in (
            Sensor(0.9, Fraction(1)),
            Sensor(Fraction(1), 0.9),
            Sensor(Fraction(-1, 2), Fraction(1)),
            Sensor(Fraction(1), Fraction(3, 2)),
        ):
            with self.subTest(sensor=sensor), self.assertRaises(ValueError):
                execute(self.world, self.loss, sensor, (True,) * 3)

    def test_lag_and_followup_are_validated(self):
        for bad in (-1, 3, 1.0, True):
            with self.subTest(lag=bad), self.assertRaises(ValueError):
                execute(self.world, self.loss,
                        Sensor(Fraction(1), Fraction(1), bad), (True,) * 3)
        for bad in (-1, 4, 1.0, True):
            with self.subTest(F=bad), self.assertRaises(ValueError):
                execute(self.world, self.loss, self.perfect, (True,) * 3,
                        followup_until=bad)

    def test_wrong_length_or_nonboolean_noise_rejected(self):
        for bad in ((), (True, True), (True, False, 0)):
            with self.subTest(bits=bad), self.assertRaises(ValueError):
                execute(self.world, self.loss, self.perfect, bad)

    def test_unregistered_scenario_rejected(self):
        other = Scenario("not_registered", Fraction(1), self.loss.fault)
        with self.assertRaises(ValueError):
            execute(self.world, other, self.perfect, (True,) * 3)

    def test_reject_wrong_repair_goal(self):
        base = replace(self.world.base, actions=(
            Action("repair", frozenset({"seed"}), "wrong", (1,), (0,)),))
        altered = World(base, self.world.scenarios)
        with self.assertRaises(ValueError):
            execute(altered, altered.scenarios[0], self.perfect, (True,) * 3)

    def test_reject_extra_undeclared_actions(self):
        extra = replace(self.world.base, actions=self.world.base.actions + (
            Action("bonus", frozenset(), "service", (0,), (0,)),))
        altered = World(extra, self.world.scenarios)
        with self.assertRaises(ValueError):
            execute(altered, altered.scenarios[0], self.perfect, (True,) * 3)

    def test_cannot_turn_synthetic_traces_into_field_validation(self):
        rec = evidence_record(self.world, self.loss, self.perfect, (True,) * 3)
        self.assertEqual(rec["payload"]["evidence_class"],
                         "SELF_GENERATED_SYNTHETIC_NOT_FIELD_EVIDENCE")
        self.assertFalse(rec["payload"]["physical_incident_identity_verified"])
        self.assertEqual(audit()["physical_field_episodes_admitted"], 0)


if __name__ == "__main__":
    unittest.main()
