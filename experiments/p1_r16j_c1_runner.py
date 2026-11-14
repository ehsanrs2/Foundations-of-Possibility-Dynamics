"""C1-Runner v0: actual, resource-capped SIX-ARM developer benchmark.

Reuses R9/R11's SAME tiny modeled systems, R7 actual-loss strict-restoration
target, conventional G2 reachability and R10 standard augmented-state DP.
Fitting is an actual shared ridge learner; each arm has exactly the same
seven raw input slots plus ONE method-specific slot (zero for raw).
Feature construction, synthetic target generation, fit and inference occur
within one separately capped Linux worker process per method. Parent measures
whole-process wall; child measures CPU, peak RSS and feature/fit/predict time.

Crucial limits: TRAIN and TUNE REPEAT the same nine handmade structures.
There is NO independent TEST partition, field observation, H1 preregistration,
or matched-scale inference. A green run demonstrates a measured rehearsal,
NOT a completed C1 confirmatory benchmark. Do NOT use timing as science.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from fractions import Fraction
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from time import perf_counter_ns, process_time_ns

from experiments.p1_gate2 import Fault, bfs_postfault
from experiments.p1_r8_dev_predictive_baselines import _standardize, _solve_ridge
from experiments.p1_r9_physical_controls import MODES, fixture, static_pair
from experiments.p1_r10_executable_backup import ProcessCaps, _preexec_limits
from experiments.p1_r11_unknown_time_prediction import (
    KITS, TRAIN_PRIORS, TUNE_PRIORS, RIDGE, exact_model_target,
    unknown_time_trial, readiness_prior,
)

PROFILE = "C1_RUNNER_MEASURED_DEVELOPMENT_V0"
METHODS = (
    "raw", "topology", "resource_reachability",
    "physical_event_cut", "augmented_state_dp", "r1_scoped_pair_candidate",
)
CAPS = ProcessCaps(wall_seconds=8.0, cpu_seconds=8, address_space_mb=256)
PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Record:
    identity: tuple[str, int, Fraction]
    partition: str
    preevent: tuple[float, ...]
    outcome: Fraction
    extended: float


def _raw(mode: str, kits: int, alpha: Fraction) -> tuple[float, ...]:
    """Exactly the same information to all arms; no realized shock identity."""
    return (float(kits), float(alpha), float(mode == "independent"),
            float(mode == "alias"), float(mode == "common"),
            float(kits >= 1), float(kits >= 2))


def _one_channel_reachable(mode: str, kits: int, alpha: Fraction) -> float:
    """Standard G2 finite resource-limited constructive reachability.

    This is an *existential one-channel* conventional baseline, NOT a
    non-generative reachability/repair policy or field mechanism validation.
    """
    weighted = Fraction()
    for tau, prior in ((1, alpha), (2, 1 - alpha)):
        if not prior:
            continue
        old = fixture(mode=mode, kits=kits, preparation_ticks=tau).base
        declared = replace(
            old, horizon=tau,
            goals=frozenset(("channel_a", "channel_b")),
            fault=Fault(0, frozenset(), (0,)),
        )
        reachable = bfs_postfault(declared, construction=True)
        weighted += prior * bool(reachable)
    return float(weighted)


def _extra(method: str, mode: str, kits: int,
           alpha: Fraction) -> float:
    if method == "raw":
        return 0.0
    if method == "topology":
        # Exact ordinary pre-fault action/prerequisite count; intentionally
        # constant on this R9 grammar, an important limitation.
        trial = unknown_time_trial(mode, kits, alpha)
        return float(sum(len(a.requires) for a in trial.base.actions))
    if method == "resource_reachability":
        return _one_channel_reachable(mode, kits, alpha)
    if method == "physical_event_cut":
        return float(static_pair(mode, kits)["event_min_cut"])
    if method == "augmented_state_dp":
        return float(readiness_prior(
            mode, kits, alpha, implementation="standard_dp"))
    if method == "r1_scoped_pair_candidate":
        return float(static_pair(mode, kits)["scoped_pair"])
    raise ValueError("unregistered C1 runner method")


def compute(method: str) -> dict:
    """Run actual feature extractor, identical fixed-size ridge and forecasts.

    Evaluation labels are generated with a known synthetic model strictly
    for TRAIN/TUNE scores; they never enter any pre-fault feature function.
    """
    if method not in METHODS:
        raise ValueError("unknown candidate arm")
    records = []
    measured_feature_ns = 0
    measured_truth_ns = 0
    for mode in MODES:
        for kits in KITS:
            for alpha in TRAIN_PRIORS + TUNE_PRIORS:
                start = perf_counter_ns()
                x = _raw(mode, kits, alpha)
                z = _extra(method, mode, kits, alpha)
                measured_feature_ns += perf_counter_ns() - start
                before_target = perf_counter_ns()
                trial = unknown_time_trial(mode, kits, alpha)
                actual, _ = exact_model_target(trial)
                measured_truth_ns += perf_counter_ns() - before_target
                part = "TRAIN" if alpha in TRAIN_PRIORS else "TUNE"
                records.append(Record((mode, kits, alpha), part, x, actual, z))
    train = [r for r in records if r.partition == "TRAIN"]
    tune = [r for r in records if r.partition == "TUNE"]
    if len(train) != 27 or len(tune) != 18:
        raise AssertionError("historical R11 repeated-structure partitions changed")
    if len({(r.identity[0], r.identity[1]) for r in train}) != 9:
        raise AssertionError("R11 source structure count changed")

    start_fit = perf_counter_ns()
    # EIGHT columns in every arm. Standardization uses TRAIN ONLY, and
    # zero-variance features are automatically regularized by ridge.
    train_x, tune_x = _standardize(
        [r.preevent + (r.extended,) for r in train],
        [r.preevent + (r.extended,) for r in tune],
    )
    coefficients = _solve_ridge(
        train_x, [float(r.outcome) for r in train], penalty=RIDGE)
    fit_ns = perf_counter_ns() - start_fit
    if any(len(x) != 9 for x in train_x + tune_x):  # 8 + intercept
        raise AssertionError("different effective feature-slot capacity")

    start_infer = perf_counter_ns()
    forecasts = [
        min(1.0, max(0.0, sum(w * a for w, a in zip(coefficients, x))))
        for x in tune_x
    ]
    inference_ns = perf_counter_ns() - start_infer
    tests = []
    for r, pred in zip(tune, forecasts):
        truth = float(r.outcome)
        expected = truth * (1 - truth) + (pred - truth) ** 2
        tests.append({
            "key": f"{r.identity[0]}:{r.identity[1]}:{r.identity[2]}",
            "forecast": round(pred, 12),
            "known_model_probability": str(r.outcome),
            "expected_brier": round(expected, 12),
        })
    ids = [item["key"] for item in tests]
    digest = sha256(json.dumps(ids, sort_keys=True).encode()).hexdigest()
    return {
        "method": method,
        "classification": "ACTUALLY_EXECUTED_REPEATED_TOY_NOT_INDEPENDENT_TEST",
        "train_parameter_settings": 27,
        "tune_parameter_settings": 18,
        "independent_test_systems": 0,
        "shared_train_and_tune_structure_groups": 9,
        "fixed_feature_slots_excluding_intercept": 8,
        "fixed_ridge_penalty": RIDGE,
        "tune_identity_sha256": digest,
        "feature_value_distinct_count": len({r.extended for r in records}),
        "mean_expected_brier": round(
            sum(t["expected_brier"] for t in tests) / len(tests), 12),
        "tune_records": tests,
        "worker_phases_ms": {
            "feature": round(measured_feature_ns / 1e6, 4),
            "synthetic_target_generation": round(measured_truth_ns / 1e6, 4),
            "fit": round(fit_ns / 1e6, 4),
            "predict": round(inference_ns / 1e6, 4),
        },
        "H1_confirmatory_samples": 0,
    }


def worker(method: str) -> None:
    import resource
    started = process_time_ns()
    result = compute(method)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(json.dumps({
        "result": result,
        "cpu_ms_from_worker_start": round(
            (process_time_ns() - started) / 1e6, 4),
        "peak_rss_kib_linux": rss,
    }, sort_keys=True))


def capped_run(method: str, caps: ProcessCaps = CAPS) -> dict:
    """One hard-capped child per arm; never score timeout as negative Brier."""
    if method not in METHODS:
        raise ValueError("unknown benchmark arm")
    if not isinstance(caps, ProcessCaps):
        raise TypeError("ProcessCaps required")
    if not sys.platform.startswith("linux"):
        raise RuntimeError("hard-cap runner requires Linux")
    started = perf_counter_ns()
    try:
        p = subprocess.run(
            [sys.executable, "-m",
             "experiments.p1_r16j_c1_runner",
             "--worker-method", method],
            cwd=str(PROJECT_ROOT), capture_output=True, text=True,
            timeout=caps.wall_seconds, check=False,
            preexec_fn=lambda: _preexec_limits(caps),
        )
    except subprocess.TimeoutExpired:
        return {"method": method, "status": "WALL_TIMEOUT",
                "budget": caps_as_dict(caps)}
    except OSError as error:
        return {"method": method, "status": "SPAWN_FAILURE",
                "error_type": type(error).__name__,
                "budget": caps_as_dict(caps)}
    wall = round((perf_counter_ns() - started) / 1e6, 4)
    if p.returncode != 0:
        return {
            "method": method, "status": "CHILD_FAILURE",
            "exit_code": p.returncode, "wall_ms": wall,
            "stderr_tail": p.stderr[-1000:], "budget": caps_as_dict(caps),
        }
    try:
        payload = json.loads(p.stdout)
        if payload["result"]["method"] != method:
            raise ValueError("worker output method mismatch")
    except (ValueError, KeyError, TypeError):
        return {"method": method, "status": "INVALID_WORKER_OUTPUT",
                "wall_ms": wall, "budget": caps_as_dict(caps)}
    return {
        "method": method, "status": "PASS",
        "all_in_process_wall_ms": wall,
        "worker_cpu_ms": payload["cpu_ms_from_worker_start"],
        "peak_rss_kib_linux": payload["peak_rss_kib_linux"],
        "budget": caps_as_dict(caps),
        "prediction": payload["result"],
    }


def caps_as_dict(caps: ProcessCaps) -> dict:
    return {
        "wall_seconds": caps.wall_seconds, "cpu_seconds": caps.cpu_seconds,
        "address_space_mb_RLIMIT_AS": caps.address_space_mb,
    }


def summarize_runs(runs: dict[str, dict]) -> dict:
    """Refuse to compute a winner or gain from missing, failed or unmatched arms."""
    if set(runs) != set(METHODS):
        raise ValueError("MISSING_METHOD_RESULTS")
    if any(runs[m].get("status") != "PASS" for m in METHODS):
        return {
            "gate": "C1-Runner-v0", "classification": "BLOCKED_INCOMPLETE_METHOD_COVERAGE",
            "status": "NO_COMPARATIVE_SCORE",
            "failures": {m: runs[m].get("status") for m in METHODS
                         if runs[m].get("status") != "PASS"},
            "H1_confirmatory_samples": 0,
        }
    predictions = {m: runs[m]["prediction"] for m in METHODS}
    keys = {v["tune_identity_sha256"] for v in predictions.values()}
    counts = {(v["train_parameter_settings"], v["tune_parameter_settings"],
               v["fixed_feature_slots_excluding_intercept"])
              for v in predictions.values()}
    if len(keys) != 1 or counts != {(27, 18, 8)}:
        raise ValueError("PAIRED_TASK_OR_CAPACITY_MISMATCH")
    true_labels = {tuple((row["key"], row["known_model_probability"])
                         for row in v["tune_records"])
                   for v in predictions.values()}
    if len(true_labels) != 1:
        raise ValueError("DIFFERENT_OUTCOME_LABELS")
    brier = {m: predictions[m]["mean_expected_brier"] for m in METHODS}
    return {
        "gate": "C1-Runner-v0",
        "classification": "ACTUAL_EXECUTED_DEVELOPMENT_ONLY_REPEATED_STRUCTURE",
        "status": "PASS_MEASURED_DEV_REHEARSAL_NOT_CONFIRMATION",
        "actual_learner_and_feature_extraction_executed": True,
        "same_total_process_caps": len(
            {json.dumps(runs[m]["budget"], sort_keys=True) for m in METHODS}) == 1,
        "developer_tune_mean_expected_brier": brier,
        "descriptive_DP_minus_R1": round(
            brier["augmented_state_dp"] - brier["r1_scoped_pair_candidate"], 12),
        "paired_tune_parameter_settings": 18,
        "independent_test_systems": 0,
        "train_tune_structures_overlap": True,
        "field_physical_identity_authenticated": False,
        "all_six_comparators_measured_in_subprocesses": True,
        "H1_preregistered": False,
        "H1_confirmatory_samples": 0,
    }


def audit(caps: ProcessCaps = CAPS) -> dict:
    """Report measurements; never assert speed ordering or a positive gain."""
    if not isinstance(caps, ProcessCaps):
        raise TypeError("ProcessCaps required")
    measured = {m: capped_run(m, caps) for m in METHODS}
    summary = summarize_runs(measured)
    return {
        **summary,
        "profile": PROFILE,
        "environment": {
            "platform": platform.platform(),
            "python": sys.version.split()[0],
            "process_limits": caps_as_dict(caps),
        },
        "method_runs": measured,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--worker-method", choices=METHODS)
    a = p.parse_args()
    if a.worker_method:
        worker(a.worker_method)
    else:
        print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
