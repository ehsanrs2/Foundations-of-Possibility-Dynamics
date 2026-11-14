"""B7: structural testbed dry-run admission controls, NOT field evidence."""
from copy import deepcopy
from hashlib import sha256
import unittest

from experiments.p1_r16h_b7_testbed_feasibility import (
    PROFILE, audit, synthetic_demo, validate_structure,
)


class B7TestbedFeasibilityTests(unittest.TestCase):
    def setUp(self):
        self.demo = synthetic_demo()

    def check_invalid(self, mutation, code):
        candidate = deepcopy(self.demo)
        mutation(candidate)
        outcome = validate_structure(candidate)
        self.assertFalse(outcome["field_evidence_admitted"])
        self.assertEqual(outcome["H1_confirmatory_samples"], 0)
        self.assertIn(code, outcome["reason_codes"])

    def test_audit_never_promotes_field_evidence(self):
        x = audit()
        self.assertEqual(x["gate"], "B7")
        self.assertEqual(x["H1_confirmatory_samples"], 0)
        self.assertFalse(x["real_testbed_operated"])
        self.assertFalse(x["source_signatures_cryptographically_verified"])

    def test_synthetic_demo_passes_only_structure(self):
        x = validate_structure(self.demo)
        self.assertEqual(x["structural_status"], "PASS_SYNTHETIC_STRUCTURE_ONLY")
        self.assertEqual(x["endpoint_dry_run"], "RESTORED")
        self.assertEqual(x["field_evidence_status"],
                         "BLOCKED_INDEPENDENT_SOURCE_VERIFICATION")
        self.assertFalse(x["local_checksum_is_independent_signature"])

    def test_service_mismatch_rejected(self):
        self.check_invalid(lambda r: r["assessor"].update(service_id="OTHER"),
                           "SERVICE_ID_MISMATCH")

    def test_trajectory_mismatch_rejected(self):
        self.check_invalid(lambda r: r["controller"].update(trajectory_id="OTHER"),
                           "TRAJECTORY_LINK_INVALID")

    def test_wrong_policy_identity_rejected(self):
        self.check_invalid(lambda r: r["controller"].update(policy_id="OTHER"),
                           "POLICY_LINK_INVALID")

    def test_incompatible_physical_fault_id_rejected(self):
        self.check_invalid(lambda r: r["assessor"].update(fault_id="OTHER"),
                           "PHYSICAL_FAULT_LINK_NOT_DOCUMENTED")

    def test_fault_before_snapshot_rejected(self):
        self.check_invalid(lambda r: r["assessor"].update(
            held_before_at="2026-01-01T00:00:04Z"), "EVENT_CHRONOLOGY_INVALID")

    def test_no_future_observation_for_controller(self):
        self.check_invalid(lambda r: r["controller"]["actions"][0].update(
            delivered_at="2026-01-01T00:00:08Z"),
            "ACTION_USES_UNAVAILABLE_OBSERVATION")

    def test_misaligned_clock_calibration_rejected(self):
        self.check_invalid(lambda r: r["clock"].update(max_error_ms=4000),
                           "CLOCK_BOUND_NOT_ESTABLISHED")

    def test_undocumented_safety_rejected(self):
        self.check_invalid(lambda r: r["safety"].update(
            authorized_fault_injection=False),
            "SAFETY_OR_AUTHORIZATION_UNDOCUMENTED")

    def test_unverified_attestation_cannot_be_self_declared(self):
        self.check_invalid(lambda r: r["provenance"].update(
            custodian_signature="MADE_UP"),
            "CLAIMED_EXTERNAL_ATTESTATION_NOT_VERIFIED")

    def test_falsified_payload_detected_by_existing_local_digest(self):
        self.check_invalid(lambda r: r["provenance"]["synthetic_payload"].update(
            version=99), "LOCALLY_STORED_CHECKSUM_CHANGED")

    def test_check_executable_failure_at_complete_deadline(self):
        case = deepcopy(self.demo)
        case["assessor"]["regained_at"] = None
        x = validate_structure(case)
        self.assertEqual(x["endpoint_dry_run"], "NOT_RESTORED")
        self.assertFalse(x["field_evidence_admitted"])

    def test_short_followup_censors_even_if_later_truth_is_known(self):
        case = deepcopy(self.demo)
        case["trial"]["followup_until"] = "2026-01-01T00:00:06Z"
        x = validate_structure(case)
        self.assertEqual(x["endpoint_dry_run"], "CENSORED")

    def test_before_event_followup_does_not_fake_no_loss(self):
        case = deepcopy(self.demo)
        case["trial"]["followup_until"] = "2026-01-01T00:00:01Z"
        x = validate_structure(case)
        self.assertEqual(x["endpoint_dry_run"], "UNKNOWN_RISK")

    def test_no_fault_caused_loss_does_not_become_success(self):
        case = deepcopy(self.demo)
        case["assessor"]["held_after"] = True
        x = validate_structure(case)
        self.assertEqual(x["endpoint_dry_run"], "NOT_AT_RISK")

    def test_primary_h1_cannot_be_claimed_registered(self):
        self.check_invalid(lambda r: r["research_state"].update(
            H1_preregistered=True), "H1_STATE_CANNOT_BE_PROMOTED")

    def test_sealed_data_access_cannot_be_claimed(self):
        self.check_invalid(lambda r: r["research_state"].update(
            sealed_families_accessed=True), "SEALED_DATA_FORBIDDEN")

    def test_synthetically_replacing_source_type_does_not_admit_real(self):
        self.check_invalid(lambda r: r.update(origin="REAL_TESTBED"),
                           "NON_SYNTHETIC_SOURCE_UNVERIFIED")

    def test_untrusted_truth_disclosure_rejected(self):
        self.check_invalid(lambda r: r["assessor"].update(
            truth_not_exposed_to_controller=False),
            "PRIVILEGED_TRUTH_LEAKAGE_UNRESOLVED")

    def test_missing_evidence_fails_closed(self):
        case = deepcopy(self.demo)
        del case["controller"]
        x = validate_structure(case)
        self.assertEqual(x["structural_status"], "BLOCKED_MALFORMED_RECORD")
        self.assertIsNone(x["endpoint_dry_run"])
        self.assertEqual(x["H1_confirmatory_samples"], 0)


if __name__ == "__main__":
    unittest.main()
