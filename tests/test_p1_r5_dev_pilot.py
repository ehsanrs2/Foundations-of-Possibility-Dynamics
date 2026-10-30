"""R5 development-only pilot contracts, never a confirmatory H1 test."""
from collections import Counter
from fractions import Fraction
import unittest

from experiments.p1_r5_dev_pilot import (
    POLICIES, _public_summary, _summarize_rows, run,
)
from experiments.p1_r4_development_families import TRAIN, TUNE, SEALED


class R5PilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pilot = run(seed=20261030, train_n=2, tune_n=1)

    def test_holdouts_are_never_generated(self):
        p=self.pilot
        self.assertEqual(p["sealed_family_generation"],0)
        self.assertEqual(p["confirmatory_outcomes"],0)
        self.assertTrue(all(x["family"] not in SEALED
                            for x in p["raw_development_rows"]))

    def test_diagnostic_counts_not_pseudoreplication(self):
        p=self.pilot
        self.assertEqual(p["independent_dev_systems"],7)
        self.assertEqual(p["case_evaluations"],7*3*4)
        self.assertEqual(p["full_trace_oracle_comparisons"],7*3*4)
        self.assertEqual(len(p["raw_development_rows"]),21)
        self.assertEqual(len(p["family_policy_summaries"]),12)

    def test_three_policy_variants_are_explicit(self):
        self.assertEqual(set(self.pilot["policy_variants"]),set(POLICIES))
        self.assertEqual(len(POLICIES),3)
        self.assertTrue(all(p in POLICIES for p in self.pilot["policy_variants"]))

    def test_all_dev_families_have_three_policy_rows(self):
        p=self.pilot
        names=Counter((x["family"],x["policy"]) for x in p["raw_development_rows"])
        for family in TRAIN:
            for policy in POLICIES:
                self.assertEqual(names[(family,policy)],2)
        for policy in POLICIES:
            self.assertEqual(names[(TUNE[0],policy)],1)

    def test_eligibility_is_stipulated_not_statistically_inferred(self):
        for x in self.pilot["raw_development_rows"]:
            self.assertEqual(x["summary"]["eligible_mass"],"3/4")
            self.assertEqual(sum(c["eligible"] for c in x["cases"]),3)
            self.assertEqual([c["case"] for c in x["cases"]],
                             ["early_loss","main_loss","shared_cause","retained"])
        for row in self.pilot["family_policy_summaries"]:
            self.assertEqual(row["mean_loss_eligibility_mass"],"3/4")

    def test_nonloss_is_undefined_not_failed(self):
        for x in self.pilot["raw_development_rows"]:
            nonloss=x["cases"][-1]
            self.assertFalse(nonloss["eligible"])
            self.assertIsNone(nonloss["strict_restoration"])
            self.assertIsNone(nonloss["clairvoyant_feasibility_only"])

    def test_loss_label_never_exceeds_standard_feasibility(self):
        for x in self.pilot["raw_development_rows"]:
            for c in x["cases"]:
                if c["eligible"]:
                    self.assertIn(c["strict_restoration"],(0,1))
                    self.assertIn(c["clairvoyant_feasibility_only"],(0,1))
                    self.assertLessEqual(c["strict_restoration"],
                                         c["clairvoyant_feasibility_only"])

    def test_each_family_summary_is_rational_and_bounded(self):
        for s in self.pilot["family_policy_summaries"]:
            self.assertTrue(0 <= Fraction(
                s["pooled_descriptive_restoration_given_loss"]) <= 1)
            self.assertTrue(0 <= Fraction(
                s["mean_of_system_conditional_restoration"]) <= 1)
            self.assertEqual(s["total_case_records"], 4*s["independent_dev_systems"])
            self.assertEqual(s["total_eligible_case_records"],
                             3*s["independent_dev_systems"])

    def test_resource_accounting_separates_action_consumption_and_fault(self):
        for x in self.pilot["raw_development_rows"]:
            for c in x["cases"]:
                self.assertGreaterEqual(c["kit_consumed_by_actions"],0)
                self.assertGreaterEqual(c["kit_destroyed_by_fault"],0)
                self.assertGreaterEqual(c["selected_actions"],0)
                self.assertLessEqual(c["selected_actions"],c["policy_steps"])

    def test_same_structure_under_each_policy_variant(self):
        by_identity={}
        for x in self.pilot["raw_development_rows"]:
            key=(x["family"],x["index"])
            by_identity.setdefault(key,[]).append(x)
        for records in by_identity.values():
            self.assertEqual(len(records),3)
            self.assertEqual(len({r["seed_fingerprint"] for r in records}),1)
            self.assertEqual(len({r["structure_fingerprint"] for r in records}),1)
            self.assertEqual(len({r["policy"] for r in records}),3)
            self.assertEqual(len({tuple(c["fault_tick"] for c in r["cases"])
                                  for r in records}),1)

    def test_separate_instance_seeds_and_fingerprints(self):
        base=[x for x in self.pilot["raw_development_rows"]
              if x["policy"]=="R3_original"]
        self.assertEqual(len(set(x["seed_fingerprint"] for x in base)),7)
        self.assertEqual(len(set(x["family"] for x in base)),4)

    def test_no_future_failure_can_be_used_as_a_predictor_feature(self):
        # R5 contains only realized outcomes and oracle outcomes for a
        # DEV pilot: it must never be mistaken for pre-fault feature vectors.
        self.assertIn("NOT_H1", self.pilot["classification"])
        self.assertIn("DESCRIPTIVE", self.pilot["classification"])
        self.assertEqual(self.pilot["confirmatory_outcomes"],0)
        self.assertNotIn("H1_confirmed",self.pilot)

    def test_summary_excludes_raw_cases_but_preserves_family_reporting(self):
        summary=_public_summary(self.pilot)
        self.assertNotIn("raw_development_rows",summary)
        self.assertNotIn("wall_clock_profile_seconds",summary)
        self.assertEqual(len(summary["family_policy_summaries"]),12)

    def test_invalid_pilot_sizes_fail_closed(self):
        for train,tune in ((0,1),(25,1),(1,0),(1,13),(True,1),(1,1.2)):
            with self.assertRaises(ValueError):
                run(seed=123,train_n=train,tune_n=tune)

    def test_invalid_seed_fails_closed(self):
        with self.assertRaises(ValueError):
            run(seed="123",train_n=1,tune_n=1)

    def test_missing_cases_cannot_normalize(self):
        with self.assertRaises(AssertionError):
            _summarize_rows([{"probability":"1/4","eligible":False,
                "strict_restoration":None,"clairvoyant_feasibility_only":None,
                "kit_consumed_by_actions":0,"kit_destroyed_by_fault":0,
                "selected_actions":0,"policy_steps":1}])

    def test_small_pilot_can_be_reproduced(self):
        other=run(seed=20261030,train_n=2,tune_n=1)
        self.assertEqual(_public_summary(other),_public_summary(self.pilot))
        self.assertEqual(other["raw_development_rows"],
                         self.pilot["raw_development_rows"])

    def test_measured_wall_clock_is_not_asserted_as_performance_claim(self):
        self.assertGreaterEqual(self.pilot["wall_clock_profile_seconds"],0)


if __name__=="__main__":
    unittest.main()
