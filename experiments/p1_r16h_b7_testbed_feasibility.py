"""B7 prospective testbed FEASIBILITY / source-admission dry run only.

This module never operates physical equipment or authenticates a third-party
signature. It validates a minimal separated controller/assessor episode
envelope, then explicitly BLOCKS promotion to field or H1 evidence.
Synthetic demo records are generated in-process and are NOT field episodes.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone, timedelta
from hashlib import sha256
import json

PROFILE = "B7_INSTRUMENTED_TESTBED_FEASIBILITY_V1"
REQUIRED_ATTESTATION = (
    "custodian_signature", "trusted_public_key_id",
    "immutable_origin_uri", "independent_verification_report",
)
REQUIRED_SAFETY = (
    "authorized_fault_injection", "isolation_confirmed",
    "rollback_documented", "independent_observer_assigned",
)
VALID_COMMANDS = frozenset(("WAIT", "repair"))


def _timestamp(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamps must be ISO strings")
    t = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if t.utcoffset() is None:
        raise ValueError("all clocks require explicit offset")
    return t.astimezone(timezone.utc)


def _digest(payload: dict) -> str:
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=True).encode("utf-8")).hexdigest()


def validate_structure(bundle: dict) -> dict:
    """Mechanical checks only. No evidence is admitted even if PASS."""
    errors: list[str] = []
    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        require(bundle["schema"] == PROFILE, "WRONG_SCHEMA")
        require(bundle["origin"] == "SYNTHETIC_DEMONSTRATION",
                "NON_SYNTHETIC_SOURCE_UNVERIFIED")
        require(bundle["research_state"]["H1_preregistered"] is False,
                "H1_STATE_CANNOT_BE_PROMOTED")
        require(bundle["research_state"]["sealed_families_accessed"] is False,
                "SEALED_DATA_FORBIDDEN")
        require(bundle["trial"]["service_id"] == bundle["assessor"]["service_id"],
                "SERVICE_ID_MISMATCH")
        require(bundle["trial"]["service_id"] == bundle["controller"]["service_id"],
                "CONTROLLER_SERVICE_MISMATCH")
        require(bundle["trial"]["trajectory_id"] ==
                bundle["assessor"]["trajectory_id"] ==
                bundle["controller"]["trajectory_id"],
                "TRAJECTORY_LINK_INVALID")
        require(bundle["trial"]["policy_id"] == bundle["controller"]["policy_id"],
                "POLICY_LINK_INVALID")
        require(bundle["trial"]["prediction_freeze_id"] != "",
                "PREDICTION_TIME_NOT_FROZEN")
        require(bundle["assessor"]["source_role"] == "INDEPENDENT_ASSESSOR"
                and bundle["controller"]["source_role"] == "CONTROLLER_LOGGER",
                "INDEPENDENT_ROLES_NOT_SEPARATED")
        safety = bundle["safety"]
        require(all(safety[k] is True for k in REQUIRED_SAFETY),
                "SAFETY_OR_AUTHORIZATION_UNDOCUMENTED")

        clock = bundle["clock"]
        require(type(clock["max_error_ms"]) is int and
                0 <= clock["max_error_ms"] <= 100,
                "CLOCK_BOUND_NOT_ESTABLISHED")
        require(bool(clock["calibration_reference"]),
                "CLOCK_CALIBRATION_MISSING")
        freeze = _timestamp(bundle["trial"]["prediction_at"])
        before = _timestamp(bundle["assessor"]["held_before_at"])
        fault = _timestamp(bundle["assessor"]["fault_at"])
        after = _timestamp(bundle["assessor"]["held_after_at"])
        deadline = _timestamp(bundle["trial"]["deadline_at"])
        followup = _timestamp(bundle["trial"]["followup_until"])
        require(freeze < before < fault < after <= deadline,
                "EVENT_CHRONOLOGY_INVALID")
        require(freeze <= followup <= deadline,
                "FOLLOWUP_OUT_OF_RANGE")
        require(bundle["assessor"]["fault_id"] ==
                bundle["trial"]["injected_fault_id"],
                "PHYSICAL_FAULT_LINK_NOT_DOCUMENTED")
        require(type(bundle["assessor"]["held_before"]) is bool
                and type(bundle["assessor"]["held_after"]) is bool,
                "ASSESSOR_GOAL_STATE_MISSING")
        regained = bundle["assessor"]["regained_at"]
        if regained is not None:
            reg = _timestamp(regained)
            require(after < reg <= deadline, "RECOVERY_CLOCK_INVALID")
        else:
            reg = None

        logs = bundle["controller"]["actions"]
        require(type(logs) is list and bool(logs),
                "ACTION_LOG_MISSING")
        previous = freeze
        for action in logs:
            sensed = _timestamp(action["observed_at"])
            delivered = _timestamp(action["delivered_at"])
            commanded = _timestamp(action["command_at"])
            require(freeze <= sensed <= delivered <= commanded <= deadline,
                    "ACTION_USES_UNAVAILABLE_OBSERVATION")
            require(previous <= commanded, "ACTION_LOG_NONMONOTONIC")
            require(action["command"] in VALID_COMMANDS,
                    "UNKNOWN_COMMAND_OR_UNDECLARED_ACTION")
            require(type(action["received_goal"]) is bool,
                    "OBSERVED_GOAL_BOOLEAN_MISSING")
            previous = commanded

        require(bundle["trial"]["raw_policy_inputs_frozen"] is True,
                "POLICY_INPUT_CONTRACT_NOT_LOCKED")
        require(bundle["assessor"]["truth_not_exposed_to_controller"] is True,
                "PRIVILEGED_TRUTH_LEAKAGE_UNRESOLVED")
        require(bundle["provenance"]["local_sha256"] ==
                _digest(bundle["provenance"]["synthetic_payload"]),
                "LOCALLY_STORED_CHECKSUM_CHANGED")
        require(all(bundle["provenance"][k] is None
                    for k in REQUIRED_ATTESTATION),
                "CLAIMED_EXTERNAL_ATTESTATION_NOT_VERIFIED")

        # Endpoint from the trusted evaluator's claimed values for this
        # STRUCTURAL DRY RUN, never treated as real independent fact.
        actual_loss = (bundle["assessor"]["held_before"] is True and
                       bundle["assessor"]["held_after"] is False)
        if followup < fault:
            endpoint = "UNKNOWN_RISK"
        elif not actual_loss:
            endpoint = "NOT_AT_RISK"
        elif reg is not None and reg <= followup:
            endpoint = "RESTORED"
        elif followup < deadline:
            endpoint = "CENSORED"
        else:
            endpoint = "NOT_RESTORED"
    except (KeyError, ValueError, TypeError, AttributeError, OverflowError):
        return {
            "structural_status": "BLOCKED_MALFORMED_RECORD",
            "reason_codes": sorted(set(errors + ["MISSING_OR_INVALID_INPUT"])),
            "endpoint_dry_run": None,
            "field_evidence_admitted": False,
            "H1_confirmatory_samples": 0,
        }

    return {
        "structural_status": ("PASS_SYNTHETIC_STRUCTURE_ONLY" if not errors
                              else "BLOCKED_STRUCTURAL_CONTRACT"),
        "reason_codes": sorted(set(errors)),
        "endpoint_dry_run": endpoint if not errors else None,
        "field_evidence_status": "BLOCKED_INDEPENDENT_SOURCE_VERIFICATION",
        "field_evidence_admitted": False,
        "H1_confirmatory_samples": 0,
        "H1_status": "DRAFT_NOT_PREREGISTERED",
        "local_checksum_is_independent_signature": False,
    }


def synthetic_demo() -> dict:
    """Local placeholders are NOT a field collector or proof of independence."""
    payload = {"synthetic_demo": True, "schema": PROFILE, "version": 1}
    return {
        "schema": PROFILE,
        "origin": "SYNTHETIC_DEMONSTRATION",
        "research_state": {"H1_preregistered": False,
                           "sealed_families_accessed": False},
        "trial": {
            "service_id": "DEMO-SERVICE",
            "trajectory_id": "DEMO-T0",
            "policy_id": "DEMO-P0",
            "prediction_freeze_id": "DEMO-FROZEN-CONTRACT",
            "prediction_at": "2026-01-01T00:00:00Z",
            "deadline_at": "2026-01-01T00:00:10Z",
            "followup_until": "2026-01-01T00:00:10Z",
            "injected_fault_id": "DEMO-F0",
            "raw_policy_inputs_frozen": True,
        },
        "assessor": {
            "source_role": "INDEPENDENT_ASSESSOR",
            "service_id": "DEMO-SERVICE", "trajectory_id": "DEMO-T0",
            "fault_id": "DEMO-F0",
            "held_before_at": "2026-01-01T00:00:02Z",
            "fault_at": "2026-01-01T00:00:03Z",
            "held_after_at": "2026-01-01T00:00:04Z",
            "held_before": True, "held_after": False,
            "regained_at": "2026-01-01T00:00:07Z",
            "truth_not_exposed_to_controller": True,
        },
        "controller": {
            "source_role": "CONTROLLER_LOGGER",
            "service_id": "DEMO-SERVICE", "trajectory_id": "DEMO-T0",
            "policy_id": "DEMO-P0",
            "actions": [
                {"observed_at": "2026-01-01T00:00:04Z",
                 "delivered_at": "2026-01-01T00:00:05Z",
                 "command_at": "2026-01-01T00:00:06Z",
                 "received_goal": False, "command": "repair"},
            ],
        },
        "clock": {"max_error_ms": 20,
                  "calibration_reference": "DEMO-CALIBRATION-NOT-REAL"},
        "safety": {k: True for k in REQUIRED_SAFETY},
        "provenance": {
            "synthetic_payload": payload,
            "local_sha256": _digest(payload),
            **{k: None for k in REQUIRED_ATTESTATION},
        },
    }


def audit() -> dict:
    base = synthetic_demo()
    good = validate_structure(base)
    bad = deepcopy(base)
    bad["controller"]["actions"][0]["delivered_at"] = "2026-01-01T00:00:08Z"
    leaked = validate_structure(bad)
    if not (
        good["structural_status"] == "PASS_SYNTHETIC_STRUCTURE_ONLY"
        and good["endpoint_dry_run"] == "RESTORED"
        and not good["field_evidence_admitted"]
        and "ACTION_USES_UNAVAILABLE_OBSERVATION" in leaked["reason_codes"]
    ):
        raise AssertionError("B7 fail-closed structural controls changed")
    return {
        "gate": "B7",
        "result": "PASS_DEVELOPER_FEASIBILITY_CONTRACT_ONLY",
        "synthetic_demo_structural": good["structural_status"],
        "invalid_future_observation_rejected": True,
        "independent_real_assessor_connected": False,
        "real_testbed_operated": False,
        "source_signatures_cryptographically_verified": False,
        "external_field_episodes_admitted": 0,
        "H1_confirmatory_samples": 0,
        "H1_preregistered": False,
        "status": "FIELD_EVIDENCE_BLOCKED_UNTIL_INDEPENDENT_ATTESTATION",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
