"""R11 development-only unknown-shock-time predictive task with matched caps.

A shock occurs at tick 1 or 2 with a pre-event disclosed probability law,
but the fixed R7 controller sees only realized state changes, never future
time or failure identity. Every scenario genuinely deletes held service.

Nine HAND-DEFINED synthetic physical configurations (3 modes x 3 kit stocks)
are repeatedly evaluated at five risk priors. TRAIN/TUNE are repetitions of
the SAME nine configurations: no independent test populations or H1 result.

All three learner arms have identical pre-event raw features, target,
synthetic cases, ridge learner, and Linux CPU/wall/AS caps:
  raw: conventional topology, event cut, stock and time-prior inputs;
  standard_dp: raw + conventional augmented-state prior-weighted joint readiness;
  independent_history: raw + the SAME readiness, constructed by an independent
      exhaustive chronology (this is NOT new information or a novel theory).
Ideal known-model pre-event p* is a separate diagnostic lower bound.

Exact loss-conditioned expected Brier is from model-known R7 histories,
not samples of independently observed outcomes. No sealed generator is used.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path
from time import perf_counter_ns, process_time_ns
import argparse
import json
import os
import subprocess
import sys

from experiments.p1_r3_policy_rollout import Case, Trial
from experiments.p1_r7_silent_observation import (
    execute_observable, independent_observable_oracle,
)
from experiments.p1_r8_dev_predictive_baselines import _standardize, _solve_ridge
from experiments.p1_r9_physical_controls import fixture, static_pair, MODES
from experiments.p1_r10_executable_backup import (
    ProcessCaps, _preexec_limits, standard_joint_state_dp,
    independent_prefix_history_oracle,
)

TRAIN_PRIORS = (Fraction(0), Fraction(1, 2), Fraction(1))
TUNE_PRIORS = (Fraction(1, 4), Fraction(3, 4))
METHODS = ("raw", "standard_dp", "independent_history")
KITS = (0, 1, 2)
MAX_CASES = 16
RIDGE = 1.0
DEFAULT_CAPS = ProcessCaps(wall_seconds=5.0, cpu_seconds=5, address_space_mb=256)


def unknown_time_trial(mode: str, kits: int, early_probability: Fraction) -> Trial:
    """One fixed horizon, event at tau=1 or tau=2 (unseen before occurrence)."""
    if mode not in MODES:
        raise ValueError("unknown predeclared mechanism mode")
    if type(kits) is not int or kits not in KITS:
        raise ValueError("kit count must be a predeclared integer")
    if not isinstance(early_probability, Fraction) or not 0 <= early_probability <= 1:
        raise ValueError("early hazard prior must be an exact fraction in [0,1]")
    original=fixture(mode=mode,kits=kits,preparation_ticks=2)
    cases=[]
    for tick,weight in ((1,early_probability),(2,1-early_probability)):
        if not weight:
            continue
        for c in original.cases:
            cases.append(Case(
                name=f"tau{tick}_{c.name}",
                probability=c.probability*weight,
                fault=replace(c.fault,tick=tick),
            ))
    if not cases or len(cases)>MAX_CASES:
        raise ValueError("R11 bounded scenario count violated")
    if sum((x.probability for x in cases),Fraction())!=1:
        raise AssertionError("marginal shock-time law is not normalized")
    # The fixed-policy execution reads only Case.fault when the event occurs.
    # The base model's historical fault field is never a policy observation.
    return Trial(original.base,original.policy,tuple(cases))


def exact_model_target(trial: Trial, *, verify: bool = False) -> tuple[Fraction,int]:
    """Strict restoration after ACTUAL fault-caused loss under one R7 policy."""
    restored=Fraction()
    lost=Fraction()
    checked=0
    for c in trial.cases:
        outcome=execute_observable(trial,c)
        if verify:
            if outcome!=independent_observable_oracle(trial,c):
                raise AssertionError("R11 R7 full-trace oracle mismatch")
            checked+=1
        status=outcome.result("service")
        if status is None or outcome.lost_at_fault!=frozenset({"service"}):
            raise AssertionError("R11 always-loss risk-set contract violated")
        lost+=c.probability
        restored+=c.probability*status
    if lost!=1:
        raise AssertionError("incorrect conditional denominator")
    return restored/lost,checked


def readiness_prior(mode: str, kits: int, early_probability: Fraction,
                    *, implementation: str) -> Fraction:
    """Compute BEFORE the realized event, using hypothetical boundary times.

    This is a deterministic function of the same raw declared input available
    to all arms. Independent-history is an ordinary exhaustive conventional
    algorithm, not an independent physical phenomenon.
    """
    if implementation not in ("standard_dp","independent_history"):
        raise ValueError("unknown readiness implementation")
    result=Fraction()
    for tau,weight in ((1,early_probability),(2,1-early_probability)):
        if not weight:
            continue
        t=fixture(mode=mode,kits=kits,preparation_ticks=tau)
        if implementation=="standard_dp":
            indicator=standard_joint_state_dp(t,mode)["scoped_joint_ready_indicator"]
        else:
            indicator=independent_prefix_history_oracle(
                t,mode)["scoped_joint_ready_indicator"]
        result+=weight*indicator
    return result


@dataclass(frozen=True)
class Setting:
    mode: str
    kits: int
    early_probability: Fraction
    x: tuple[float,...]
    target: Fraction
    candidate: Fraction | None
    partition: str


def make_setting(mode: str, kits: int, alpha: Fraction,
                 method: str, *, verify: bool = False) -> tuple[Setting,int]:
    if method not in METHODS:
        raise ValueError("unknown predictive method")
    if alpha not in TRAIN_PRIORS+TUNE_PRIORS:
        raise ValueError("unregistered toy development time prior")
    t=unknown_time_trial(mode,kits,alpha)
    y,checks=exact_model_target(t,verify=verify)
    static=static_pair(mode,kits)
    # Mode, stock, hazard prior, familiar event cut and individual-path
    # redundancy: identical pre-event inputs to ALL trained arms.
    x=(float(kits),float(alpha),float(mode=="independent"),
       float(mode=="alias"),float(mode=="common"),
       float(static["scoped_pair"]),float(static["event_min_cut"]),
       float(kits>=2),float(kits>=1))
    candidate=None if method=="raw" else readiness_prior(
        mode,kits,alpha,implementation=method)
    partition="TRAIN" if alpha in TRAIN_PRIORS else "TUNE"
    return Setting(mode,kits,alpha,x,y,candidate,partition),checks


def compare(method: str, *, verify: bool = False) -> dict:
    if method not in METHODS:
        raise ValueError("unregistered prediction method")
    settings=[]
    checked=0
    for mode in MODES:
        for kits in KITS:
            for alpha in TRAIN_PRIORS+TUNE_PRIORS:
                record,checks=make_setting(mode,kits,alpha,method,verify=verify)
                settings.append(record)
                checked+=checks
    train=[s for s in settings if s.partition=="TRAIN"]
    tune=[s for s in settings if s.partition=="TUNE"]
    if len(train)!=27 or len(tune)!=18:
        raise AssertionError("developer parameter design changed")
    def x(s):
        return s.x if method=="raw" else s.x+(float(s.candidate),)
    train_x,tune_x=_standardize([x(s) for s in train],[x(s) for s in tune])
    coef=_solve_ridge(train_x,[float(s.target) for s in train],penalty=RIDGE)
    forecasts=[max(0.0,min(1.0,sum(c*z for c,z in zip(coef,row))))
               for row in tune_x]
    cases=[]
    for record,q in zip(tune,forecasts):
        p=float(record.target)
        expected_ideal=p*(1-p)
        score=expected_ideal+(q-p)**2
        if score+1e-12<expected_ideal:
            raise AssertionError("forecast beat exact model-known Bayes lower bound")
        cases.append({
            "mode":record.mode,"kits":record.kits,
            "early_probability":str(record.early_probability),
            "exact_model_conditional_probability":str(record.target),
            "prior_joint_ready":str(record.candidate)
                if record.candidate is not None else None,
            "forecast":round(q,12),
            "conditional_expected_brier":round(score,12),
            "ideal_model_brier":round(expected_ideal,12),
        })
    avg=lambda key:round(sum(c[key] for c in cases)/len(cases),12)
    return {
        "gate":"R11","method":method,
        "classification":"REPEATED_TOY_PARAMETER_DESIGN_NOT_H1",
        "unique_physical_structure_configs":len(MODES)*len(KITS),
        "train_parameter_settings":len(train),
        "tune_parameter_settings":len(tune),
        "train_hazard_priors":[str(x) for x in TRAIN_PRIORS],
        "tune_hazard_priors":[str(x) for x in TUNE_PRIORS],
        "known_event_time_disclosed_to_policy":False,
        "all_scenarios_real_loss":True,
        "fully_model_known_synthetic_outcome":True,
        "full_history_oracle_comparisons":checked,
        "fixed_ridge_penalty":RIDGE,
        "mean_expected_brier":avg("conditional_expected_brier"),
        "mean_model_ideal_brier":avg("ideal_model_brier"),
        "tune_records":cases,
        "no_sealed_family_calls":True,
        "confirmatory_H1_samples":0,
    }


def _worker(method: str) -> None:
    import resource
    started=process_time_ns()
    result=compare(method)
    stat=resource.getrusage(resource.RUSAGE_SELF)
    print(json.dumps({
        "result":result,
        "worker_cpu_ms":round((process_time_ns()-started)/1_000_000,4),
        "worker_peak_rss_kib":stat.ru_maxrss,
    },sort_keys=True))


def capped_compare(method: str, caps: ProcessCaps = DEFAULT_CAPS) -> dict:
    """Enforced SAME all-in limits for an identical prediction task.

    Python interpreter, module imports, feature computation, known-model
    synthetic target generation, model fitting, and prediction are all
    inside the child limit and parent wall deadline. CPU and RSS measurements
    are not used as deterministic performance test assertions.
    """
    if method not in METHODS:
        raise ValueError("unregistered prediction arm")
    if not sys.platform.startswith("linux"):
        raise RuntimeError("R11 process cap workflow requires Linux")
    if not isinstance(caps,ProcessCaps):
        raise TypeError("ProcessCaps required")
    start=perf_counter_ns()
    try:
        child=subprocess.run(
            [sys.executable,"-m","experiments.p1_r11_unknown_time_prediction",
             "--worker-method",method],
            cwd=str(Path(__file__).resolve().parents[1]),
            capture_output=True,text=True,check=False,timeout=caps.wall_seconds,
            preexec_fn=lambda: _preexec_limits(caps),
        )
    except subprocess.TimeoutExpired:
        return {"method":method,"status":"WALL_TIMEOUT"}
    if child.returncode:
        return {"method":method,"status":"CHILD_FAILED",
                "returncode":child.returncode,"stderr":child.stderr[-2000:]}
    obj=json.loads(child.stdout)
    if obj["result"]["method"]!=method:
        raise AssertionError("wrong child prediction arm")
    return {
        "method":method,"status":"PASS",
        "wall_ms":round((perf_counter_ns()-start)/1_000_000,4),
        "worker_cpu_ms":obj["worker_cpu_ms"],
        "worker_peak_rss_kib":obj["worker_peak_rss_kib"],
        "prediction":obj["result"],
    }


def audit(*, caps: ProcessCaps = DEFAULT_CAPS) -> dict:
    if not isinstance(caps,ProcessCaps):
        raise TypeError("ProcessCaps required")
    reference=compare("standard_dp",verify=True)
    results={}
    for method in METHODS:
        run=capped_compare(method,caps)
        if run["status"]!="PASS":
            raise RuntimeError(("R11 method failed its resource cap",method,run))
        if run["prediction"]!=compare(method):
            raise AssertionError("bounded child changed deterministic prediction")
        results[method]=run
    dp=results["standard_dp"]["prediction"]
    history=results["independent_history"]["prediction"]
    if dp["tune_records"]!=history["tune_records"] or (
        dp["mean_expected_brier"]!=history["mean_expected_brier"]):
        raise AssertionError("standard and independent readiness are unequal")
    if dp["tune_records"]!=reference["tune_records"]:
        raise AssertionError("R7 trace verification changed predictions")
    return {
        "gate":"R11",
        "classification":"UNKNOWN_TIME_EQUAL_OBJECTIVE_TOY_DEVELOPMENT_NOT_H1",
        "unique_physical_structure_configs":9,
        "train_parameter_settings":27,
        "tune_parameter_settings":18,
        "full_history_oracle_comparisons":reference["full_history_oracle_comparisons"],
        "same_source_inputs_frozen_ridge_and_expected_brier":True,
        "same_enforced_process_caps":True,
        "process_caps":{"wall_seconds":caps.wall_seconds,
                        "cpu_seconds":caps.cpu_seconds,
                        "virtual_address_space_mb":caps.address_space_mb},
        "standard_DP_equals_independent_history_feature":True,
        "same_structure_repeated_across_train_tune":True,
        "independent_heldout_systems":0,
        "physical_event_calibration":False,
        "R8_negative_archive_unchanged":True,
        "H1_confirmatory_test":False,
        "results":results,
        "result":"PASS",
    }


def deterministic_archive(data: dict) -> dict:
    answer=json.loads(json.dumps(data))
    for v in answer["results"].values():
        for field in ("wall_ms","worker_cpu_ms","worker_peak_rss_kib"):
            v.pop(field,None)
    return answer


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--worker-method",choices=METHODS)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    if args.worker_method:
        _worker(args.worker_method)
        return
    report=audit()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n",
                               encoding="utf-8")
    print(json.dumps(deterministic_archive(report),indent=2,sort_keys=True))


if __name__=="__main__":
    main()
