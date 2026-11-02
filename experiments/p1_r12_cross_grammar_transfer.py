"""R12: distinct-grammar synthetic development transfer, NOT external validation.

R11 reused the SAME nine handmade structures for TRAIN and TUNE. R12 makes
TRAIN (direct-channel preparation) and TUNE (shared-stage / asymmetric-stage
preparation) structurally DISJOINT synthetic grammar families. These are
engineered by the same researchers and ARE NOT independently sampled physical
systems, observational data or P1/H1 sealed outcomes.

All methods predict the same nonanticipative R7 strict actual-loss recovery
under an unknown shock time tau=2 or 3 and stipulated fault-event law. The
policy knows current state and event-time prior, never realized future time.

Conventional competitors: raw+cut/reachability summaries, raw+interactions,
raw+standard augmented-state joint readiness, an independently implemented
history-based equivalent, and full-known-model exact scenario integration
as the unattainable-in-general Bayes reference. Fixed ridge training and
same Linux resource CAPS; no equal *actual* work or real-world inference.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
from time import perf_counter_ns,process_time_ns
import argparse
import json
import subprocess
import sys

from experiments.p1_gate2 import Action, Fault, Model
from experiments.p1_r3_policy_rollout import Case, FixedPolicy, Trial
from experiments.p1_r8_dev_predictive_baselines import _standardize,_solve_ridge
from experiments.p1_r9_physical_controls import MODES,route_scope,static_pair,fixture
from experiments.p1_r10_executable_backup import (
    ProcessCaps,_preexec_limits,physical_event_independent,
)
from experiments.p1_r11_unknown_time_prediction import exact_model_target

TRAIN_FAMILIES=("direct",)
TUNE_FAMILIES=("shared_stage","asymmetric_stage")
ALL_FAMILIES=TRAIN_FAMILIES+TUNE_FAMILIES
KITS=(0,1,2)
TRAIN_PRIORS=(Fraction(0),Fraction(1,2),Fraction(1))
TUNE_PRIORS=(Fraction(1,4),Fraction(3,4))
METHODS=("raw","interaction","state_dp","history","known_model")
CAPS=ProcessCaps(wall_seconds=10.0,cpu_seconds=10,address_space_mb=256)
MAX_STATES=128


def family_trial(family: str,mode: str,kits: int,early: Fraction) -> Trial:
    """Explicit physical-event law reused across disjoint architecture grammars."""
    if family not in ALL_FAMILIES:
        raise ValueError("R12 forbids unregistered/SEALED families")
    if mode not in MODES or type(kits) is not int or kits not in KITS:
        raise ValueError("unregistered synthetic mode/stock")
    if not isinstance(early,Fraction) or not Fraction(0)<=early<=Fraction(1):
        raise ValueError("invalid exact early-event prior")
    original=fixture(mode=mode,kits=kits,preparation_ticks=2)
    existing={a.name:a for a in original.base.actions}
    prep_a=existing["prepare_a"]
    prep_b=existing["prepare_b"]
    stages=()
    if family=="shared_stage":
        stages=(Action("unlock",frozenset({"base"}),"armed",(0,),(0,),True),)
        prep_a=replace(prep_a,requires=frozenset({"armed"}))
        prep_b=replace(prep_b,requires=frozenset({"armed"}))
    elif family=="asymmetric_stage":
        stages=(Action("open_a",frozenset({"base"}),"port_a",(0,),(0,),True),)
        prep_a=replace(prep_a,requires=frozenset({"port_a"}))
    actions=stages+(prep_a,prep_b,existing["serve_a"],existing["serve_b"])
    before=tuple(a.name for a in actions)
    after=("serve_a","serve_b")+tuple(
        a.name for a in actions if a.name not in ("serve_a","serve_b"))
    policy=FixedPolicy(before,after,True)
    cases=[]
    for tau,prob in ((2,early),(3,Fraction(1)-early)):
        if not prob:
            continue
        for c in original.cases:
            cases.append(Case(
                f"tau{tau}_{c.name}",
                c.probability*prob,
                replace(c.fault,tick=tau),
            ))
    base=Model(
        initial=frozenset({"base","service"}),
        goals=frozenset({"service"}),
        resources=("kit",),
        stock=(kits,),
        actions=actions,
        horizon=4,
        fault=cases[0].fault,
    )
    return Trial(base,policy,tuple(cases))


def structure_signature(trial: Trial,mode: str) -> str:
    """Hash semantics, NOT scenario labels or training/tune partition tags."""
    scope=route_scope(mode)
    spec={
        "initial":sorted(trial.base.initial),
        "goals":sorted(trial.base.goals),
        "resource":list(trial.base.resources),
        "stock":list(trial.base.stock),
        "horizon":trial.base.horizon,
        "actions":sorted([
            [a.name,sorted(a.requires),a.produces,list(a.consumes),
             list(a.yields),a.generative] for a in trial.base.actions]),
        "physical":[
            [key,scope.mechanisms[key],
             sorted(scope.incidence.get(key,frozenset()))]
            for key in sorted(scope.mechanisms)],
    }
    return sha256(json.dumps(spec,sort_keys=True).encode()).hexdigest()


def _legal_options(held: frozenset[str],stock: tuple[int,...],
                   actions: tuple[Action,...]):
    yield "WAIT",held,stock
    for a in actions:
        if (not a.requires<=held or
            any(stock[j]<a.consumes[j] for j in range(len(stock))) or
            (a.produces in held and not any(a.yields))):
            continue
        yield a.name,held|{a.produces},tuple(
            stock[j]-a.consumes[j]+a.yields[j] for j in range(len(stock)))


def conventional_joint_dp(trial: Trial,mode: str,tau: int) -> int:
    """Plain augmented-state reachability, one legal prefix for both channels."""
    if not 1<=tau<=3 or trial.base.horizon!=4:
        raise ValueError("bounded R12 scenario-time contract")
    frontier={(trial.base.initial,trial.base.stock)}
    for _ in range(tau):
        nxt=set()
        for held,stock in frontier:
            for _,caps,newstock in _legal_options(held,stock,trial.base.actions):
                nxt.add((caps,newstock))
        if len(nxt)>MAX_STATES:
            raise RuntimeError("R12 state cap exceeded; do not return false zero")
        frontier=nxt
    return int(
        physical_event_independent(mode) and any(
            {"channel_a","channel_b"}<=held for held,_ in frontier))


def independent_joint_history(trial: Trial,mode: str,tau: int) -> int:
    """Separate mutable inventory DFS: no calls to state DP/helper transitions."""
    if not 1<=tau<=3 or trial.base.horizon!=4:
        raise ValueError("bounded R12 history-time contract")
    found=False
    calls=0
    def walk(t,held: set[str],kit: int):
        nonlocal found,calls
        calls+=1
        if calls>1000:
            raise RuntimeError("bounded independent history cap exceeded")
        if t==tau:
            found=found or {"channel_a","channel_b"}.issubset(held)
            return
        walk(t+1,set(held),kit)
        for a in trial.base.actions:
            if not a.requires.issubset(held):
                continue
            if kit<a.consumes[0]:
                continue
            if a.produces in held and a.yields[0]==0:
                continue
            walk(t+1,set(held)|{a.produces},
                 kit-a.consumes[0]+a.yields[0])
    walk(0,set(trial.base.initial),trial.base.stock[0])
    return int(physical_event_independent(mode) and found)


def readiness(family: str,mode: str,kits: int,alpha: Fraction,
              method: str) -> Fraction:
    if method not in ("state_dp","history"):
        raise ValueError("only conventional state or history readiness")
    trial=family_trial(family,mode,kits,alpha)
    score=Fraction()
    for tau,w in ((2,alpha),(3,Fraction(1)-alpha)):
        if not w:
            continue
        if method=="state_dp":
            result=conventional_joint_dp(trial,mode,tau)
        else:
            result=independent_joint_history(trial,mode,tau)
        score+=w*result
    return score


@dataclass(frozen=True)
class Record:
    family: str
    mode: str
    kits: int
    prior: Fraction
    signature: str
    x: tuple[float,...]
    outcome: Fraction
    engineered: float


def system_record(family: str,mode: str,kits: int,alpha: Fraction,
                  method: str,*,verify: bool=False) -> tuple[Record,int]:
    if method not in METHODS:
        raise ValueError("unknown R12 prediction arm")
    trial=family_trial(family,mode,kits,alpha)
    p,checks=exact_model_target(trial,verify=verify)
    static=static_pair(mode,kits)
    # Equal raw pre-event source summaries to each learned arm. This is NOT
    # the complete state model; the known-model arm sees all declared rules.
    stages=sum(a.name in ("unlock","open_a") for a in trial.base.actions)
    features=(
        float(kits),float(alpha),
        float(mode=="independent"),float(mode=="alias"),
        float(mode=="common"),float(len(trial.base.actions)),
        float(stages),float(static["scoped_pair"]),
        float(static["event_min_cut"]),
        float(kits>=1),float(kits>=2),
        float(sum(len(a.requires) for a in trial.base.actions)),
    )
    independent_stock=int(mode=="independent" and kits>=2)
    if method=="interaction":
        augment=float(independent_stock*(1-float(alpha)))
    elif method in ("state_dp","history"):
        augment=float(readiness(family,mode,kits,alpha,method))
    else:
        augment=0.0
    return Record(family,mode,kits,alpha,structure_signature(trial,mode),
                  features,p,augment),checks


def evaluate(method: str, *,verify: bool=False) -> dict:
    if method not in METHODS:
        raise ValueError("unregistered R12 predictive operation")
    train=[]
    tune=[]
    fullchecks=0
    for family in ALL_FAMILIES:
        for mode,kits in product(MODES,KITS):
            for alpha in (TRAIN_PRIORS if family in TRAIN_FAMILIES
                          else TUNE_PRIORS):
                record,checked=system_record(family,mode,kits,alpha,
                                             method,verify=verify)
                fullchecks+=checked
                (train if family in TRAIN_FAMILIES else tune).append(record)
    train_sigs={x.signature for x in train}
    tune_sigs={x.signature for x in tune}
    if train_sigs & tune_sigs:
        raise AssertionError("train/tune STRUCTURAL fingerprint leakage")
    if (len(train_sigs)!=9 or len(tune_sigs)!=18 or
        len(train)!=27 or len(tune)!=36):
        raise AssertionError("independent-grammar size contract broken")
    def feature(s):
        if method in ("raw","known_model"):
            return s.x
        return s.x+(s.engineered,)
    if method!="known_model":
        xt,xv=_standardize([feature(s) for s in train],
                            [feature(s) for s in tune])
        weights=_solve_ridge(xt,[float(s.outcome) for s in train],penalty=1.0)
        forecasts=[min(1.0,max(0.0,sum(w*v for w,v in zip(weights,row))))
                   for row in xv]
    else:
        # Explicitly an exact known-model pre-event reference, NOT a trained
        # representation and NOT an unknown-model deployable forecast.
        forecasts=[float(s.outcome) for s in tune]
    rows=[]
    for s,q in zip(tune,forecasts):
        p=float(s.outcome)
        ideal=p*(1-p)
        expected=ideal+(q-p)**2
        if expected+1e-12<ideal:
            raise AssertionError("Brier below mathematical Bayes risk")
        rows.append({
            "family":s.family,"mode":s.mode,"kits":s.kits,
            "early_prior":str(s.prior),"structure_sha256":s.signature,
            "model_target":str(s.outcome),
            "feature":str(s.engineered) if method!="raw" else None,
            "predicted":round(q,12),
            "expected_brier":round(expected,12),
            "ideal_brier":round(ideal,12),
        })
    means=lambda field:round(sum(z[field] for z in rows)/len(rows),12)
    return {
        "gate":"R12",
        "classification":"CROSS_GRAMMAR_SYNTHETIC_DEV_ONLY_NOT_H1",
        "method":method,
        "train_family":"direct",
        "tune_families":list(TUNE_FAMILIES),
        "train_unique_graph_signatures":len(train_sigs),
        "tune_unique_graph_signatures":len(tune_sigs),
        "graph_signature_overlap":len(train_sigs&tune_sigs),
        "train_hazard_parameter_rows":len(train),
        "tune_hazard_parameter_rows":len(tune),
        "independent_real_world_systems":0,
        "real_hazard_measurements":0,
        "sealed_test_family_calls":0,
        "fixed_policy_observes_future_fault":False,
        "same_loss_conditional_brier":True,
        "full_history_checks":fullchecks,
        "mean_expected_brier":means("expected_brier"),
        "mean_ideal_brier":means("ideal_brier"),
        "tune_results":rows,
    }


def _worker(method: str) -> None:
    import resource
    start=process_time_ns()
    out=evaluate(method)
    res=resource.getrusage(resource.RUSAGE_SELF)
    print(json.dumps({
        "model":out,
        "worker_cpu_ms":round((process_time_ns()-start)/1e6,4),
        "worker_peak_rss_kib":res.ru_maxrss,
    },sort_keys=True))


def capped_run(method: str,caps: ProcessCaps=CAPS) -> dict:
    if method not in METHODS:
        raise ValueError("R12 method not registered")
    if not sys.platform.startswith("linux"):
        raise RuntimeError("Linux process caps are required")
    if not isinstance(caps,ProcessCaps):
        raise TypeError("ProcessCaps required")
    started=perf_counter_ns()
    try:
        child=subprocess.run(
            [sys.executable,"-m","experiments.p1_r12_cross_grammar_transfer",
             "--worker-method",method],
            capture_output=True,text=True,check=False,
            timeout=caps.wall_seconds,
            cwd=str(Path(__file__).resolve().parents[1]),
            preexec_fn=lambda: _preexec_limits(caps),
        )
    except subprocess.TimeoutExpired:
        return {"method":method,"status":"WALL_TIMEOUT"}
    if child.returncode:
        return {"method":method,"status":"CHILD_FAILURE",
                "code":child.returncode,"stderr":child.stderr[-1200:]}
    output=json.loads(child.stdout)
    if output["model"]["method"]!=method:
        raise AssertionError("worker output method mismatch")
    return {
        "method":method,"status":"PASS",
        "worker_wall_ms":round((perf_counter_ns()-started)/1e6,4),
        "worker_cpu_ms":output["worker_cpu_ms"],
        "worker_peak_rss_kib":output["worker_peak_rss_kib"],
        "result":output["model"],
    }


def audit(*, caps: ProcessCaps=CAPS) -> dict:
    if not isinstance(caps,ProcessCaps):
        raise TypeError("ProcessCaps required")
    verified=evaluate("state_dp",verify=True)
    # Every out-of-grammar structure needs independent prefix equivalence
    # under both possible event times, not just equal final predictive score.
    comparisons=0
    for family in ALL_FAMILIES:
        for mode,kits in product(MODES,KITS):
            trial=family_trial(family,mode,kits,Fraction(1,2))
            for tau in (2,3):
                if conventional_joint_dp(trial,mode,tau)!=(
                    independent_joint_history(trial,mode,tau)):
                    raise AssertionError("independent prefix algorithms disagree")
                comparisons+=1
    workers={}
    for m in METHODS:
        z=capped_run(m,caps)
        if z["status"]!="PASS":
            raise RuntimeError(("R12 bounded worker error",z))
        workers[m]=z
    dp=workers["state_dp"]["result"]
    history=workers["history"]["result"]
    if dp["tune_results"]!=history["tune_results"]:
        raise AssertionError("ordinary DP and history predictions should match")
    if verified["tune_results"]!=dp["tune_results"]:
        raise AssertionError("R7 independent full-history checks changed results")
    reference=workers["known_model"]["result"]
    if any(workers[m]["result"]["mean_expected_brier"]+1e-10<
           reference["mean_expected_brier"] for m in METHODS):
        raise AssertionError("finite predictor beat exact model-known ideal")
    return {
        "gate":"R12",
        "classification":"STRUCTURALLY_DISJOINT_SYNTHETIC_TRANSFER_NOT_H1",
        "train_unique_synthetic_structures":9,
        "tune_unique_synthetic_structures":18,
        "graph_signature_overlap":0,
        "train_parameter_rows":27,
        "tune_parameter_rows":36,
        "structural_DP_DFS_checks":comparisons,
        "R7_independent_history_checks":verified["full_history_checks"],
        "same_known_raw_model":True,
        "same_pre_event_prediction_target":True,
        "same_enforced_process_caps":True,
        "process_caps":{"wall_seconds":caps.wall_seconds,
                        "cpu_seconds":caps.cpu_seconds,
                        "virtual_address_space_mb":caps.address_space_mb},
        "same_actual_compute_or_model_dimension":False,
        "known_model_is_oracle_not_fitted":True,
        "sealed_H1_test_samples":0,
        "external_physical_data":False,
        "R8_unchanged":True,
        "runs":workers,
        "result":"PASS",
    }


def stable_archive(result: dict) -> dict:
    answer=json.loads(json.dumps(result))
    for worker in answer["runs"].values():
        for f in ("worker_wall_ms","worker_cpu_ms","worker_peak_rss_kib"):
            worker.pop(f,None)
    return answer


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--worker-method",choices=METHODS)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    if args.worker_method:
        _worker(args.worker_method)
        return
    result=audit()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",
                               encoding="utf-8")
    print(json.dumps(stable_archive(result),sort_keys=True,indent=2))


if __name__=="__main__":
    main()
