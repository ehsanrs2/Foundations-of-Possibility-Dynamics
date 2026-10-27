"""Pre-execution audit for the P1/H1 candidate JSON protocol.

Checks consistency only; never authorizes confirmatory data collection.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "research" / "p1_h1_design_candidate_v0_1.json"


def load(path=DRAFT):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate(p):
    if p.get("status") != "DRAFT_NOT_PREREGISTERED":
        raise ValueError("candidate is not registered; cannot promote by renaming status")
    if p.get("confirmatory_data_collected") is not False:
        raise ValueError("no confirmatory data can be reported in planning audit")
    feature = p["feature"]
    if feature["from_pre_fault_only"] is not True or feature["insufficient_coverage"] != "MISSING_NOT_ZERO":
        raise ValueError("candidate feature leaks future fault or disguises missing coverage")
    outcome = p["outcome"]
    for field in ("pre_fault_active_required", "removed_by_fault_required",
                  "reacquired_by_deadline_required", "same_policy_trajectory_required",
                  "policy_frozen_shared_across_predictors",
                  "pre_fault_shock_realization_hidden"):
        if outcome.get(field) is not True:
            raise ValueError("strict-loss endpoint/observation contract broken")
    if outcome["missing_eligible_rollouts"] != "UNDEFINED_EXCLUDE_FROM_CONDITIONAL_ANALYSIS_AND_REPORT_RATE":
        raise ValueError("zero-denominator must be undefined and separately reported")
    base = p["baselines"]
    if (base["input_access"] != "IDENTICAL_FULL_PREFAULT_RAW_MODEL_AND_SCENARIO_DISTRIBUTION"
        or base["feature_computation_included"] is not True
        or "full_augmented_state_nonanticipative_policy_when_feasible" not in base["required"]):
        raise ValueError("matched information, compute or full-state baseline absent")
    split = p["design"]
    groups = [split[k] for k in ("train_families", "tune_families", "heldout_families")]
    if not all(isinstance(g, list) and g for g in groups):
        raise ValueError("each split requires at least one family")
    names = [name for group in groups for name in group]
    if len(names) != len(set(names)):
        raise ValueError("generator family appears in more than one partition")
    if (split["confirmatory_test_data_access"] != "PROHIBITED_BEFORE_FREEZE"
        or split["heldout_shock_draws_visible_to_features"] is not False):
        raise ValueError("test data leakage is prohibited")
    analysis = p["analysis"]
    if (analysis["primary_comparison"] != "one_baseline_vs_plus_R1_feature"
        or analysis["resampling_unit"] != "whole_independent_system_within_test_family"):
        raise ValueError("primary comparison or independent sampling unit changed")
    if len(p["freeze_blockers"]) < 8:
        raise ValueError("unresolved scientific gate inventory must remain explicit")
    return {"protocol_id": p["protocol_id"], "status": p["status"],
            "train_families":len(groups[0]), "tune_families":len(groups[1]),
            "heldout_families":len(groups[2]),
            "freeze_blockers":len(p["freeze_blockers"]),
            "confirmatory_testing_permitted":False,
            "classification":"SPECIFICATION_ONLY_NOT_H1"}


def strict_restoration(held_before, lost_at_fault, regained_before_deadline):
    if lost_at_fault and not held_before:
        raise ValueError("loss cannot occur if goal was not held")
    if not lost_at_fault:
        return None
    return int(bool(regained_before_deadline))


def audit():
    return validate(load())


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
