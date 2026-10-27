"""Contract tests for P1 draft; no scientific outcomes are generated."""
from copy import deepcopy
import unittest

from experiments.p1_protocol_audit import (
    load, validate, strict_restoration, audit,
)


class P1ProtocolAuditTests(unittest.TestCase):
    def setUp(self):
        self.design = load()

    def test_draft_is_explicitly_not_registered(self):
        result = validate(self.design)
        self.assertFalse(result["confirmatory_testing_permitted"])
        self.assertGreaterEqual(result["freeze_blockers"], 8)

    def test_cannot_relabel_draft_as_preregistered(self):
        bad = deepcopy(self.design)
        bad["status"] = "PREREGISTERED"
        with self.assertRaises(ValueError):
            validate(bad)

    def test_no_shock_label_leakage(self):
        bad = deepcopy(self.design)
        bad["feature"]["from_pre_fault_only"] = False
        with self.assertRaises(ValueError):
            validate(bad)
        bad = deepcopy(self.design)
        bad["design"]["heldout_shock_draws_visible_to_features"] = True
        with self.assertRaises(ValueError):
            validate(bad)

    def test_missing_ontology_not_zero(self):
        bad = deepcopy(self.design)
        bad["feature"]["insufficient_coverage"] = "ZERO"
        with self.assertRaises(ValueError):
            validate(bad)

    def test_cannot_use_future_in_primary_endpoint(self):
        bad = deepcopy(self.design)
        bad["outcome"]["pre_fault_shock_realization_hidden"] = False
        with self.assertRaises(ValueError):
            validate(bad)

    def test_undefined_denominator_must_be_reported(self):
        bad = deepcopy(self.design)
        bad["outcome"]["missing_eligible_rollouts"] = "ZERO"
        with self.assertRaises(ValueError):
            validate(bad)

    def test_equal_information_and_compute_fairness(self):
        for key, value in (
            ("input_access", "FEATURE_MODEL_ONLY"),
            ("feature_computation_included", False),
        ):
            bad = deepcopy(self.design)
            bad["baselines"][key] = value
            with self.assertRaises(ValueError):
                validate(bad)

    def test_heldout_family_names_are_disjoint(self):
        bad = deepcopy(self.design)
        bad["design"]["heldout_families"].append(bad["design"]["train_families"][0])
        with self.assertRaises(ValueError):
            validate(bad)

    def test_independent_sampling_unit_cannot_be_rollout(self):
        bad = deepcopy(self.design)
        bad["analysis"]["resampling_unit"] = "shock_rollout"
        with self.assertRaises(ValueError):
            validate(bad)

    def test_actual_loss_outcome_not_missing_as_zero(self):
        self.assertIsNone(strict_restoration(False, False, False))
        self.assertIsNone(strict_restoration(True, False, False))
        self.assertEqual(strict_restoration(True, True, False), 0)
        self.assertEqual(strict_restoration(True, True, True), 1)
        with self.assertRaises(ValueError):
            strict_restoration(False, True, True)

    def test_audit_is_specification_only(self):
        self.assertEqual(audit()["classification"], "SPECIFICATION_ONLY_NOT_H1")


if __name__ == "__main__":
    unittest.main()
