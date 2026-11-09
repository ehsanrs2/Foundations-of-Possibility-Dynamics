"""R16-A decision contract regression tests. No H1 outcomes generated."""
from copy import deepcopy
import unittest

from experiments.p1_r16a_architecture_audit import load_inputs, validate, audit


class R16AArchitectureReviewTests(unittest.TestCase):
    def setUp(self):
        self.source = load_inputs()

    def check_rejected(self, index, mutate):
        data = [deepcopy(d) for d in self.source]
        mutate(data[index])
        with self.assertRaises(ValueError):
            validate(*data)

    def test_proposal_does_not_unlock_H1(self):
        result = audit()
        self.assertEqual(result["result"], "PASS_PROPOSAL_CONSISTENCY_ONLY")
        self.assertFalse(result["confirmatory_H1_permitted"])
        self.assertEqual(result["independent_field_H1_labels"], 0)
        self.assertEqual(result["development_brier_gains"]["R8"], 0)

    def test_cannot_self_approve_architecture(self):
        self.check_rejected(0, lambda p: p.update(status="APPROVED"))

    def test_cannot_promote_draft_H1(self):
        self.check_rejected(1, lambda p: p.update(status="PREREGISTERED"))

    def test_cannot_relabel_GOG_as_H1(self):
        self.check_rejected(
            0, lambda p: p["claim_tracks"][1].update(role="PRIMARY_DRAFT"))

    def test_cannot_swap_primary_R1_for_R10_posthoc(self):
        self.check_rejected(
            0, lambda p: p["claim_tracks"][0].update(feature="R10_joint_ready"))

    def test_cannot_promote_development_gain_into_H1(self):
        self.check_rejected(
            0, lambda p: p["development_evidence"][2].update(
                classification="CONFIRMATORY_H1"))

    def test_cannot_erase_R8_null(self):
        self.check_rejected(
            2, lambda r: r.update(
                mean_paired_improvement_baseline_minus_augmented=0.01))

    def test_cannot_change_R12_effect_size(self):
        self.check_rejected(
            0, lambda p: p["development_evidence"][2].update(brier_gain=0.05))

    def test_cannot_skip_core_semantics_before_preregistration(self):
        self.check_rejected(
            0, lambda p: p["gates"][4].update(depends_on=["A"]))

    def test_cannot_skip_real_evidence_for_field_claim(self):
        self.check_rejected(
            0, lambda p: p.update(field_claim_requires_gate_D=False))

    def test_cannot_mark_future_gate_complete(self):
        self.check_rejected(
            0, lambda p: p["gates"][3].update(status="PASS"))

    def test_cannot_relabel_node_fix_as_service_recovery(self):
        self.check_rejected(
            0, lambda p: p["real_evidence"].update(
                lanl_node_fix_is_goal_restoration=True))

    def test_cannot_admit_fabricated_H1_field_rows(self):
        self.check_rejected(
            0, lambda p: p["real_evidence"].update(real_h1_labels=1))

    def test_cannot_use_sealed_test_families(self):
        self.check_rejected(
            0, lambda p: p["safeguards"].update(
                sealed_family_generation_permitted=True))


if __name__ == "__main__":
    unittest.main()
