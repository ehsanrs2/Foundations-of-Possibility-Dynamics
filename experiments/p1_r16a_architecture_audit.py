"""R16-A: fail-closed architectural decision and evidence-preservation audit.

Reads existing published synthetic/real-data admission summaries ONLY.
Never generates sealed families, authenticates a source, or unlocks H1.
This is a proposal-consistency check, NOT peer review or preregistration.
"""
from __future__ import annotations

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research" / "R16A-decision-manifest.json"
P1 = ROOT / "research" / "p1_h1_design_candidate_v0_1.json"
R8 = ROOT / "research" / "R8-development-summary-seed20261101.json"
R11 = ROOT / "research" / "R11-unknown-time-prediction-results-20261102.json"
R12 = ROOT / "research" / "R12-cross-grammar-results-20261102.json"
R15 = ROOT / "research" / "R15-node-job-lineage-results-20261108.json"


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_inputs() -> tuple[dict, dict, dict, dict, dict, dict]:
    """Read a pinned snapshot of the scientific decision context, no network."""
    return tuple(_read(p) for p in (MANIFEST, P1, R8, R11, R12, R15))


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(plan: dict, p1: dict, r8: dict, r11: dict,
             r12: dict, r15: dict) -> dict:
    _require(plan.get("schema") == "R16A_DECISION_MANIFEST_V1",
             "unknown R16-A manifest schema")
    _require(plan.get("status") == "ARCHITECTURE_REVIEW_PROPOSED",
             "a proposed architecture cannot self-approve")
    _require(p1.get("status") == "DRAFT_NOT_PREREGISTERED"
             and p1.get("confirmatory_data_collected") is False,
             "H1 protocol was not registered or tested")
    _require(p1["design"]["confirmatory_test_data_access"] == "PROHIBITED_BEFORE_FREEZE"
             and p1["design"]["development_generator_status"]["sealed_test_examples_generated"] == 0,
             "held-out family protection changed")

    tracks = plan.get("claim_tracks", [])
    _require([t["id"] for t in tracks] ==
             ["P1_H1_PREDICTIVE", "GOG_GENERATIVITY", "CONSTRUCTION_CAUSAL"],
             "H1, GOG and causal estimands must remain separate")
    _require(tracks[0]["role"] == "PRIMARY_DRAFT"
             and tracks[0]["status"] == p1["status"]
             and tracks[0]["feature"] == p1["feature"]["id"]
             and tracks[0]["target"] == "conditional_strict_restoration_after_actual_goal_loss",
             "the R1/H1 primary candidate cannot be replaced by plan")
    _require(all(t["role"] == "SEPARATE_EXPLORATORY"
                 and t["status"] == "NOT_PREREGISTERED" for t in tracks[1:]),
             "GOG or intervention track promoted without a separate protocol")

    guard = plan.get("safeguards", {})
    required_false = ("preregistration_complete", "confirmatory_testing_permitted",
                      "sealed_family_generation_permitted", "r11_r12_promoted_to_h1",
                      "r10_readiness_replaces_r1_without_new_protocol",
                      "gog_is_h1", "claim_of_independent_new_science")
    _require(all(guard.get(x) is False for x in required_false),
             "proposal would promote unverified evidence or touch sealed families")
    _require(guard.get("confirmatory_h1_samples") == 0
             and type(guard.get("confirmatory_h1_samples")) is int
             and guard.get("r8_negative_preserved") is True,
             "confirmatory count or R8 negative history changed")

    gates = plan.get("gates", [])
    _require([g["id"] for g in gates] == list("ABCDEFG"),
             "milestone registry must be stable and uniquely ordered")
    expected_deps = {"A": [], "B": ["A"], "C": ["B"], "D": ["A"],
                     "E": ["B", "C"], "F": ["E"], "G": ["F"]}
    for gate in gates:
        _require(gate["depends_on"] == expected_deps[gate["id"]],
                 "milestone dependency graph changed")
        _require(gate["status"] == ("UNDER_REVIEW" if gate["id"] == "A"
                                    else "PLANNED"), "future gates not complete")
        _require(bool(gate.get("exit")), "milestone has no acceptance criterion")
    _require(plan.get("field_claim_requires_gate_D") is True,
             "field generalization cannot bypass independently obtained evidence")
    _require(plan.get("next_execution", {}).get("id") == "B1",
             "next implementation must establish a semantic contract")

    archive = plan.get("development_evidence", [])
    _require([x["gate"] for x in archive] == ["R8", "R11", "R12"],
             "development results were dropped or misordered")
    _require([x["classification"] for x in archive] ==
             ["DEVELOPMENT_NEGATIVE_R1", "DEVELOPMENT_ONLY_JOINT_READINESS",
              "DEVELOPMENT_ONLY_CROSS_GRAMMAR"],
             "development evidence cannot be renamed H1")

    _require(r8.get("gate") == "R8"
             and r8["r1_distinct_defined_values"] == [0]
             and r8["mean_paired_improvement_baseline_minus_augmented"] == 0
             and r8["confirmatory_h1_samples"] == 0
             and r8["sealed_test_families_generated"] == 0,
             "R8 negative developer result must remain intact")
    _require(r11.get("gate") == "R11"
             and r11["independent_heldout_systems"] == 0
             and r11["H1_confirmatory_test"] is False
             and r11["standard_DP_equals_independent_history_feature"] is True,
             "R11 is a repeated-structure developer comparison, not H1")
    _require(r12.get("gate") == "R12"
             and r12["external_physical_data"] is False
             and r12["sealed_H1_test_samples"] == 0
             and r12["graph_signature_overlap"] == 0,
             "R12 is separate-grammar synthetic development, not a field test")

    observed = [
        r8["mean_paired_improvement_baseline_minus_augmented"],
        r11["results"]["raw"]["prediction"]["mean_expected_brier"]
        - r11["results"]["standard_dp"]["prediction"]["mean_expected_brier"],
        r12["runs"]["raw"]["result"]["mean_expected_brier"]
        - r12["runs"]["state_dp"]["result"]["mean_expected_brier"],
    ]
    for declared, actual in zip(archive, observed):
        _require(abs(declared["brier_gain"] - actual) <= 2e-12,
                 "development Brier outcome altered or misquoted")
    _require(r11["results"]["standard_dp"]["prediction"]["mean_expected_brier"]
             == r11["results"]["independent_history"]["prediction"]["mean_expected_brier"]
             and r12["runs"]["state_dp"]["result"]["mean_expected_brier"]
             == r12["runs"]["history"]["result"]["mean_expected_brier"],
             "ordinary DP/history equivalence record altered")

    physical = plan.get("real_evidence", {})
    join = r15["source_join_evidence"]
    _require(r15["gate"] == "R15"
             and r15["full_H1_evaluation_performed"] is False
             and r15["physical_service_restoration_labels"] == 0
             and join["new_confirmatory_h1_samples"] == 0
             and join["direct_publisher_original_file_authenticated"] is False
             and join["all_required_conditions_met"] is False,
             "R15 did not independently authenticate physical H1 observations")
    _require(physical.get("verified_publisher_original") is False
             and physical.get("verified_job_restart_lineage") is False
             and physical.get("real_h1_labels") == 0
             and physical.get("lanl_node_fix_is_goal_restoration") is False
             and physical.get("r16_source_protocol_pr") == 31
             and physical.get("source_protocol_pr_state") == "DRAFT",
             "physical provenance/job lineage was falsely promoted")

    return {
        "gate": "R16-A",
        "result": "PASS_PROPOSAL_CONSISTENCY_ONLY",
        "status": plan["status"],
        "confirmatory_H1_permitted": False,
        "independent_field_H1_labels": 0,
        "development_brier_gains": dict(zip(("R8", "R11", "R12"), observed)),
        "next_implementation": "B1",
        "classification": "ARCHITECTURE_AND_ROADMAP_ONLY_NOT_H1",
    }


def audit() -> dict:
    return validate(*load_inputs())


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
