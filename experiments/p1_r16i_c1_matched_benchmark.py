"""C1: fail-closed fair-comparator PROTOCOL and exact toy scoring arithmetic.

This does NOT train or run the claimed methods, benchmark real wall time,
measure physical memory, access sealed outcomes, or preregister H1.
Method costs and predictions are *declared demo placeholders*. The code
audits matched-information / compute / split / endpoint requirements and
checks exact per-system Brier aggregation on a manufactured tiny fixture.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import json

PROFILE = "C1_MATCHED_INFO_COMPUTE_PROTOCOL_V1"
BASELINES = (
    "raw", "topology", "resource_reachability",
    "physical_event_cut", "augmented_state_dp",
)
CANDIDATE = "r1_scoped_pair_candidate"
METHODS = BASELINES + (CANDIDATE,)
ALLOWED_OUTCOMES = frozenset(
    ("RESTORED", "NOT_RESTORED", "NOT_AT_RISK", "CENSORED", "UNKNOWN_RISK"))
VALID_PARTITIONS = frozenset(("TRAIN", "TUNE", "TEST"))


def _f(value: str) -> Fraction:
    if not isinstance(value, str):
        raise ValueError("exact rational numbers must be strings")
    number = Fraction(value)
    if number < 0 or number > 1:
        raise ValueError("probability outside [0,1]")
    return number


def _require(ok: bool, why: str) -> None:
    if not ok:
        raise ValueError(why)


def validate_plan(plan: dict) -> dict:
    """Audit contract only: simulated costs are not measurements."""
    _require(plan.get("schema") == PROFILE, "WRONG_SCHEMA")
    _require(plan.get("evidence_class") == "MANUFACTURED_PROTOCOL_FIXTURE",
             "UNVERIFIED_OR_REAL_DATA_NOT_ADMISSIBLE_HERE")
    _require(plan.get("H1_status") == "DRAFT_NOT_PREREGISTERED"
             and plan.get("confirmatory_units") == 0
             and plan.get("sealed_test_families_opened") is False,
             "H1_OR_HOLDOUT_MISREPRESENTED")
    _require(plan.get("primary_feature") == CANDIDATE,
             "PRIMARY_FEATURE_WAS_SWAPPED")
    _require(plan.get("primary_baseline") == "augmented_state_dp",
             "STRONG_CONVENTIONAL_BASELINE_NOT_PRIMARY")
    _require(plan.get("endpoint") ==
             "SAME_HISTORY_STRICT_RESTORATION_AFTER_ACTUAL_LOSS",
             "ENDPOINT_SUBSTITUTED")
    _require(plan.get("computation") == {
        "feature_cost_included": True, "fit_cost_included": True,
        "inference_cost_included": True, "time_limit_is_hard": True,
        "memory_limit_is_hard": True,
        "timeouts_and_abstentions_explicit": True,
    }, "COMPUTE_ACCOUNTING_INCOMPLETE")
    _require(plan.get("actual_method_execution") is False and
             plan.get("actual_wall_time_measured") is False and
             plan.get("actual_peak_memory_measured") is False,
             "SIMULATED_COST_CANNOT_MASQUERADE_AS_MEASURED_BENCHMARK")
    _require(plan.get("fixed_policy_id") not in ("", None)
             and plan.get("raw_pre_fault_information_digest") not in ("", None),
             "SOURCE_INFORMATION_OR_POLICY_NOT_FROZEN")
    _require(plan.get("independent_field_test_units") == 0,
             "DEMO_CANNOT_CLAIM_FIELD_INDEPENDENCE")
    budget = plan.get("budget", {})
    _require(type(budget.get("max_declared_work_units")) is int and
             budget["max_declared_work_units"] > 0
             and type(budget.get("wall_time_ms")) is int
             and budget["wall_time_ms"] > 0
             and type(budget.get("peak_rss_mib")) is int
             and budget["peak_rss_mib"] > 0,
             "HARD_BUDGETS_NOT_DECLARED")

    methods = plan.get("methods", {})
    _require(set(methods) == set(METHODS),
             "MISSING_OR_EXTRA_METHODS")
    for name, spec in methods.items():
        _require(spec.get("implementation") == "PLACEHOLDER_NOT_EXECUTED",
                 "METHOD_EXECUTION_CLAIM_UNVERIFIED")
        _require(spec.get("raw_input_digest") ==
                 plan["raw_pre_fault_information_digest"],
                 "METHOD_INPUT_INFORMATION_MISMATCH")
        _require(spec.get("feature_frozen_before_fault") is True
                 and spec.get("future_case_information_used") is False,
                 "PREFAULT_INFORMATION_LEAKAGE")
        _require(spec.get("learner") == "RIDGE_FIXED_CAPACITY_V1"
                 and spec.get("capacity") == 4,
                 "MODEL_FAMILY_OR_CAPACITY_MISMATCH")
        _require(spec.get("training_partition") == "TRAIN"
                 and spec.get("tuning_partition") == "TUNE"
                 and spec.get("evaluation_partition") == "TEST",
                 "TRAIN_TUNE_TEST_PARTITION_LEAKAGE")
        ledger = spec.get("declared_work_units", {})
        _require(all(type(ledger.get(k)) is int and ledger[k] >= 0
                     for k in ("feature", "fit", "predict")),
                 "MISSING_OR_INVALID_COST_LEDGER")
        _require(sum(ledger.values()) <= budget["max_declared_work_units"],
                 "DECLARED_ALL_IN_WORK_BUDGET_EXCEEDED")
        _require(spec.get("prediction_abstention_contract") ==
                 "NO_SCORE_ON_TIMEOUT_OR_UNRESOLVED_ELIGIBILITY",
                 "TIMEOUT_ABSTENTION_UNSPECIFIED")

    systems = plan.get("systems", [])
    _require(type(systems) is list and len(systems) >= 4,
             "TOY_PARTITIONS_INCOMPLETE")
    identities = [s.get("system_id") for s in systems]
    _require(all(isinstance(s, str) and s for s in identities)
             and len(set(identities)) == len(identities),
             "SYSTEM_ID_DUPLICATION")
    sigs = [s.get("source_signature") for s in systems]
    _require(all(isinstance(s, str) and s for s in sigs)
             and len(set(sigs)) == len(sigs),
             "STRUCTURAL_GROUP_LEAKAGE")
    partitions = {s.get("partition") for s in systems}
    _require(partitions == VALID_PARTITIONS, "TRAIN_TUNE_TEST_MISSING")

    for system in systems:
        _require(system["partition"] in VALID_PARTITIONS
                 and system.get("policy_id") == plan["fixed_policy_id"],
                 "POLICY_OR_PARTITION_DRIFT")
        _require(system.get("pre_fault_digest") ==
                 plan["raw_pre_fault_information_digest"],
                 "RAW_PRE_FAULT_INFORMATION_DRIFT")
        episodes = system.get("episodes")
        _require(type(episodes) is list and bool(episodes),
                 "UNDEFINED_RISK_RECORD")
        episode_ids = []
        for ep in episodes:
            episode_ids.append(ep.get("episode_id"))
            _require(ep.get("status") in ALLOWED_OUTCOMES,
                     "INVALID_STRICT_RESTORATION_ENDPOINT")
            _require(type(ep.get("weight")) is str
                     and Fraction(ep["weight"]) > 0,
                     "INVALID_EPISODE_WEIGHT")
        _require(len(episode_ids) == len(set(episode_ids)),
                 "DUPLICATE_EPISODE_WITHIN_SYSTEM")
        predictions = system.get("predictions", {})
        _require(set(predictions) == set(METHODS), "MISSING_PAIRED_FORECAST")
        for _, p in predictions.items():
            _f(p)
        _require(system.get("future_case_data_seen_by_feature") is False,
                 "FUTURE_CASE_LEAKAGE")

    return {
        "result": "PASS_MANUFACTURED_COMPARISON_PROTOCOL_ONLY",
        "required_conventional_baselines": list(BASELINES),
        "primary_feature": CANDIDATE,
        "actual_comparator_algorithms_run": False,
        "measured_wall_time_or_memory": False,
        "independent_field_H1_units": 0,
        "H1_preregistered": False,
        "H1_confirmatory_samples": 0,
    }


def toy_paired_brier(plan: dict) -> dict:
    """Exact per-eligible-*system* mean of trial-weighted Brier, TEST only.

    Each TEST system contributes AT MOST ONE score irrespective of its
    number of synthetic eligible episodes. Censored/no-loss/unknown-risk
    episodes are excluded and counted; their missingness is not inferred.
    """
    validate_plan(plan)
    scores: dict[str, list[Fraction]] = {k: [] for k in METHODS}
    total_test, zero_eligible, unresolved = 0, 0, 0
    for system in plan["systems"]:
        if system["partition"] != "TEST":
            continue
        total_test += 1
        eligible = [e for e in system["episodes"]
                    if e["status"] in ("RESTORED", "NOT_RESTORED")]
        unresolved += sum(e["status"] in ("CENSORED", "UNKNOWN_RISK")
                          for e in system["episodes"])
        if not eligible:
            zero_eligible += 1
            continue
        denom = sum((Fraction(e["weight"]) for e in eligible), Fraction())
        for method in METHODS:
            p = _f(system["predictions"][method])
            score = sum(
                (Fraction(e["weight"]) *
                 (p - int(e["status"] == "RESTORED")) ** 2
                 for e in eligible), Fraction()) / denom
            scores[method].append(score)
    _require(total_test > zero_eligible, "NO_ELIGIBLE_SYSTEM_LEVEL_SCORE")
    _require(all(len(v) == total_test - zero_eligible
                 for v in scores.values()), "PAIRED_UNIT_SCORE_MISSING")
    mean = {method: sum(v, Fraction()) / len(v)
            for method, v in scores.items()}
    advantage = mean["augmented_state_dp"] - mean[CANDIDATE]
    return {
        "classification": "SYNTHETIC_ARITHMETIC_CHECK_NOT_EVIDENCE",
        "toy_test_systems": total_test,
        "toy_eligible_systems": total_test - zero_eligible,
        "toy_zero_eligible_systems": zero_eligible,
        "toy_censored_or_unknown_episodes_excluded": unresolved,
        "method_mean_brier": {m: str(v) for m, v in mean.items()},
        "toy_paired_gain_DP_minus_R1": str(advantage),
        "confidence_interval": None,
        "novelty_or_performance_inference_permitted": False,
        "H1_confirmatory_samples": 0,
    }


def demo_plan() -> dict:
    raw = "DEMO-PREFAULT-X-SAME-FOR-EVERY-ARM"
    method = {
        "implementation": "PLACEHOLDER_NOT_EXECUTED",
        "raw_input_digest": raw,
        "feature_frozen_before_fault": True,
        "future_case_information_used": False,
        "learner": "RIDGE_FIXED_CAPACITY_V1",
        "capacity": 4,
        "training_partition": "TRAIN",
        "tuning_partition": "TUNE",
        "evaluation_partition": "TEST",
        "declared_work_units": {"feature": 10, "fit": 20, "predict": 5},
        "prediction_abstention_contract":
            "NO_SCORE_ON_TIMEOUT_OR_UNRESOLVED_ELIGIBILITY",
    }
    def system(name, partition, labels):
        return {
            "system_id": name, "source_signature": "STRUCTURE-" + name,
            "partition": partition, "policy_id": "DEMO-FIXED-POLICY",
            "pre_fault_digest": raw,
            "future_case_data_seen_by_feature": False,
            "episodes": [
                {"episode_id": name + "-EP-" + str(i),
                 "status": label, "weight": "1"} for i, label in enumerate(labels)
            ],
            "predictions": {method: "1/2" for method in METHODS},
        }
    return {
        "schema": PROFILE,
        "evidence_class": "MANUFACTURED_PROTOCOL_FIXTURE",
        "H1_status": "DRAFT_NOT_PREREGISTERED",
        "confirmatory_units": 0,
        "sealed_test_families_opened": False,
        "independent_field_test_units": 0,
        "primary_feature": CANDIDATE,
        "primary_baseline": "augmented_state_dp",
        "endpoint": "SAME_HISTORY_STRICT_RESTORATION_AFTER_ACTUAL_LOSS",
        "raw_pre_fault_information_digest": raw,
        "fixed_policy_id": "DEMO-FIXED-POLICY",
        "actual_method_execution": False,
        "actual_wall_time_measured": False,
        "actual_peak_memory_measured": False,
        "budget": {"max_declared_work_units": 100,
                   "wall_time_ms": 1000, "peak_rss_mib": 256},
        "computation": {
            "feature_cost_included": True, "fit_cost_included": True,
            "inference_cost_included": True, "time_limit_is_hard": True,
            "memory_limit_is_hard": True,
            "timeouts_and_abstentions_explicit": True,
        },
        "methods": {name: deepcopy(method) for name in METHODS},
        "systems": [
            system("TRAIN-A", "TRAIN", ["RESTORED", "NOT_RESTORED"]),
            system("TUNE-A", "TUNE", ["RESTORED", "NOT_RESTORED"]),
            system("TEST-A", "TEST", ["RESTORED", "NOT_RESTORED"]),
            system("TEST-B", "TEST", ["NOT_RESTORED", "RESTORED"]),
            system("TEST-C", "TEST", ["NOT_AT_RISK", "CENSORED"]),
        ],
    }


def audit() -> dict:
    p = demo_plan()
    check = validate_plan(p)
    math = toy_paired_brier(p)
    contaminated = deepcopy(p)
    contaminated["methods"][CANDIDATE]["future_case_information_used"] = True
    try:
        validate_plan(contaminated)
        raise AssertionError("C1 failed to reject future-case leakage")
    except ValueError as exc:
        if str(exc) != "PREFAULT_INFORMATION_LEAKAGE":
            raise
    if not (
        check["actual_comparator_algorithms_run"] is False
        and math["toy_paired_gain_DP_minus_R1"] == "0"
        and math["toy_eligible_systems"] == 2
        and math["toy_zero_eligible_systems"] == 1
        and math["toy_censored_or_unknown_episodes_excluded"] == 1
    ):
        raise AssertionError("C1 benchmark protocol diagnostic changed")
    return {
        "gate": "C1",
        "result": "PASS_MATCHED_BENCHMARK_DESIGN_AUDIT_ONLY",
        "synthetic_development_negative_control_gain": "0",
        "all_in_compute_ledger_required": True,
        "independent_real_comparator_runs": 0,
        "actual_wall_and_memory_measurements": False,
        "trained_models": 0,
        "field_H1_confirmatory_samples": 0,
        "H1_preregistered": False,
        "C1_actual_benchmark_status": "NOT_EXECUTED",
        "next": "C1_RUNNER_WITH_REAL_MEASURED_BUDGETS_AFTER_REVIEW",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
