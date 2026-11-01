"""R8: tiny TRAIN/TUNE prediction baselines vs R1 scoped-pair feature.

DEVELOPMENT ONLY, no H1 test, no sealed families, no physical measurement.

Both predictive learners receive the SAME pre-event raw system inputs and
hazard priors. A fixed standard ridge linear-probability learner uses the same
train/tune systems and feature normalization. All baseline topology, resource
and conventional fault-cut features are also supplied in the plus-R1 arm.
The static R1 feature is restricted to the ONE declared synthetic common-cause
event; service loss and stock loss are NOT spuriously declared route faults.

Ground-truth *conditional* expected Brier is calculated by exact R7 policy
marginalization under the stipulated model, separate from any learner.
This complete-model Bayes reference is an unconstrained diagnostic bound,
NOT a budget-matched competitor. Record observed feature/fit/predict runtime
but do not falsely claim platform-independent equal wall-time/RAM budgets.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from math import sqrt
from pathlib import Path
from time import perf_counter_ns
import argparse
import json

from experiments.p1_gate1 import Model as PlanModel, Rule, enumerate_dfs
from experiments.fault_ontology_r1 import FaultOntology, assess
from experiments.p1_r4_development_families import TRAIN, TUNE, SEALED
from experiments.p1_r6_fault_risk_dev import develop_trial, developer_law
from experiments.p1_r7_silent_observation import (
    execute_observable, independent_observable_oracle,
)

SEED = 20261101
RIDGE = 1.0  # Developer-only choice; NOT a selected confirmatory hyperparameter.
MAX_ACTIONS = 10
MAX_PLANS = 256
FEATURES = (
    "horizon", "stock", "actions", "generative_rules",
    "restoration_rules", "sum_prerequisites", "number_of_sources",
    "individual_supports", "nongen_supports", "min_event_cut",
    "event_cut_undefined", "scope_missing", "service_risk",
    "shared_cause_risk", "stock_loss_risk",
)
R1_EXTRA = ("r1_scoped_backup_pair",)


@dataclass(frozen=True)
class Record:
    family: str
    index: int
    features: tuple[float, ...]
    candidate: float | None
    conditional: Fraction | None
    eligible_mass: Fraction
    model_fingerprint: str
    scope_status: str


def _planned_supports(base):
    """Translate ONLY pre-event action prerequisites; no future shocks or labels."""
    if len(base.actions) > MAX_ACTIONS:
        raise ValueError("R8 explicit static enumeration complexity bound exceeded")
    names = base.initial - base.goals
    model = PlanModel(
        initial=names, goals=base.goals,
        rules=tuple(Rule(a.name, a.requires, a.produces,
                         a.consumes[0], 1, a.generative)
                    for a in base.actions),
        horizon=base.horizon, budget=base.stock[0],
        exposed=frozenset({"cap:base"}),
    )
    all_plans = enumerate_dfs(model, construction=True)
    plain = enumerate_dfs(model, construction=False)
    if len(all_plans) > MAX_PLANS or len(plain) > MAX_PLANS:
        raise ValueError("R8 explicit plan-count complexity bound exceeded")
    return all_plans, plain, names


def structural_features(base, family: str, law) -> tuple[tuple[float, ...], float | None, str]:
    """Inputs are base system and PRIOR hazard law; never a future scenario.

    The R1 physical event scope is explicitly limited to the shared upstream
    dependency. All other tokens are *assumed protected in this toy scope*.
    In particular no fabricated independent service-channel failure events
    are added to the physical ontology.
    """
    if family not in TRAIN + TUNE:
        if family in SEALED:
            raise PermissionError("sealed family features are prohibited")
        raise ValueError("unrecognized development family")
    plans, plain, sources = _planned_supports(base)
    shared = "hub" if family == "hub_dependencies" else "base"
    tokens = {"cap:" + name for name in sources}
    tokens.update("rule:" + a.name for a in base.actions)
    shared_token = "cap:" + shared
    if shared_token not in tokens:
        raise ValueError("missing required synthetic upstream mechanism")
    scope = FaultOntology(
        scope_id="R8_SYNTHETIC_COMMON_CAUSE_ONLY_" + family,
        mechanisms={token: "toy-mechanism:" + token for token in tokens},
        incidence={shared_token: frozenset({"event:shared_upstream"})},
        protected={
            token: "Protected for the narrow synthetic shared-upstream event scope only"
            for token in tokens if token != shared_token
        },
        event_universe=frozenset({"event:shared_upstream"}),
    )
    metric = assess(plans, "service", scope)
    count = metric.canonical_plan_count
    mincut = metric.min_event_cut
    missing = int(metric.status == "INSUFFICIENT_FAULT_COVERAGE")
    candidate = None if metric.indicator is None else float(metric.indicator)
    ordinary = (
        float(base.horizon), float(base.stock[0]), float(len(base.actions)),
        float(sum(a.generative for a in base.actions)),
        float(sum(a.produces=="service" for a in base.actions)),
        float(sum(len(a.requires) for a in base.actions)),
        float(len(sources)), float(count), float(len(plain)),
        float(mincut if mincut is not None else 0),
        float(mincut is None), float(missing),
        float(law.service_loss), float(law.shared_loss),
        float(law.stock_loss),
    )
    if len(ordinary) != len(FEATURES):
        raise AssertionError("feature schema not declared")
    return ordinary, candidate, metric.status


def exact_target(trial, *, verify: bool = False) -> tuple[Fraction, Fraction | None, int]:
    """Exact p(restore | actual loss), with no realized scenario passed to learner.

    This is the ideal model-known R7 policy value (not the R6 old-boundary
    oracle). It is used to construct synthetic TRAIN labels and exact TUNE
    expected scores; no claim of independent empirical outcome is possible.
    """
    loss = restored = Fraction()
    checks = 0
    for case in trial.cases:
        out = execute_observable(trial, case)
        if verify:
            other = independent_observable_oracle(trial, case)
            if out != other:
                raise AssertionError("R7 independent full-history disagreement")
            checks += 1
        y = out.result("service")
        if y is not None:
            loss += case.probability
            restored += case.probability*y
    return loss, restored/loss if loss else None, checks


def record(family: str, seed: int, index: int, *, verify: bool = False) -> tuple[Record, int, int]:
    if family in SEALED:
        raise PermissionError("no sealed test generation in R8")
    if family not in TRAIN + TUNE:
        raise ValueError("unknown development family")
    # Identical known *pre-event* model/hazard input supplied to both arms.
    trial = develop_trial(seed,family,index)
    law = developer_law(seed,family,index)
    start = perf_counter_ns()
    features, candidate, status = structural_features(trial.base,family,law)
    feature_ns = perf_counter_ns()-start
    loss, probability, checks = exact_target(trial,verify=verify)
    return Record(family,index,features,candidate,probability,loss,
                  str(seed)+":"+family+":"+str(index),status),feature_ns,checks


def _standardize(train: list[tuple[float, ...]],
                 test: list[tuple[float, ...]]
                 ) -> tuple[list[list[float]], list[list[float]]]:
    if not train or not test:
        raise ValueError("both train and test must contain eligible systems")
    width=len(train[0])
    if any(len(x)!=width for x in train+test):
        raise ValueError("feature length mismatch")
    means=[sum(row[j] for row in train)/len(train) for j in range(width)]
    scales=[sqrt(sum((row[j]-means[j])**2 for row in train)/len(train))
            for j in range(width)]
    scales=[s if s>1e-12 else 1.0 for s in scales]
    def tx(rows):
        return [[1.0]+[(x[j]-means[j])/scales[j] for j in range(width)]
                for x in rows]
    return tx(train),tx(test)


def _solve_ridge(train: list[list[float]], y: list[float],
                 penalty: float = RIDGE) -> list[float]:
    """Deterministic full-rank Gaussian elimination with ridge regularization.

    Intercept is not penalized. The same fixed solver and shrinkage strength
    are used in both arms; no hyperparameter selection from tuning labels.
    """
    n=len(train)
    d=len(train[0])
    if n!=len(y) or any(len(row)!=d for row in train):
        raise ValueError("linear-system dimensions mismatched")
    a=[[sum(x[i]*x[j] for x in train)+(penalty if i==j and i>0 else 0.0)
        for j in range(d)] for i in range(d)]
    b=[sum(x[i]*z for x,z in zip(train,y)) for i in range(d)]
    for k in range(d):
        pivot=max(range(k,d),key=lambda i:abs(a[i][k]))
        a[k],a[pivot]=a[pivot],a[k]
        b[k],b[pivot]=b[pivot],b[k]
        diag=a[k][k]
        if abs(diag)<1e-12:
            raise ArithmeticError("unexpected singular regularized system")
        for j in range(k,d):
            a[k][j]/=diag
        b[k]/=diag
        for i in range(d):
            if i==k:
                continue
            coeff=a[i][k]
            for j in range(k,d):
                a[i][j]-=coeff*a[k][j]
            b[i]-=coeff*b[k]
    return b


def _clip(x: float) -> float:
    return min(1.0,max(0.0,x))


def _fit_predict(train: list[Record], test: list[Record],
                 *, add_r1: bool) -> tuple[list[float], int]:
    t0=perf_counter_ns()
    def features(row: Record) -> tuple[float, ...]:
        if not add_r1:
            return row.features
        # Missingness is NOT silently imputed as an actual 0 feature:
        # baseline already has a scope_missing flag.
        return row.features+(row.candidate if row.candidate is not None else 0.0,)
    xt,xv=_standardize([features(r) for r in train],
                       [features(r) for r in test])
    coef=_solve_ridge(xt,[float(r.conditional) for r in train])
    pred=[_clip(sum(w*x for w,x in zip(coef,row))) for row in xv]
    return pred,perf_counter_ns()-t0


def evaluate(*, seed: int = SEED, train_n: int = 24, tune_n: int = 12,
             verify: bool = False) -> dict:
    if type(seed) is not int or type(train_n) is not int or type(tune_n) is not int:
        raise ValueError("integer seed and bounded family sample counts required")
    if not 1<=train_n<=24 or not 1<=tune_n<=12:
        raise ValueError("R8 development-only bounded sample counts required")
    records=[]
    feature_ns=checks=0
    for family in TRAIN+TUNE:
        for index in range(train_n if family in TRAIN else tune_n):
            row,ns,seen=record(family,seed,index,verify=verify)
            records.append(row)
            feature_ns+=ns
            checks+=seen
    train=[r for r in records if r.family in TRAIN and r.conditional is not None]
    tune=[r for r in records if r.family in TUNE and r.conditional is not None]
    if not train or not tune:
        raise ValueError("at-risk conditional training/tune set is empty")
    baseline,base_ns=_fit_predict(train,tune,add_r1=False)
    augmented,aug_ns=_fit_predict(train,tune,add_r1=True)
    items=[]
    for r,p0,p1 in zip(tune,baseline,augmented):
        truth=float(r.conditional)
        ideal=truth*(1-truth)
        e0=ideal+(p0-truth)**2
        e1=ideal+(p1-truth)**2
        if min(e0,e1)<ideal-1e-12:
            raise AssertionError("prediction beat known-model expected Bayes risk")
        items.append({"family":r.family,"index":r.index,
                      "r1_candidate":r.candidate,"r1_status":r.scope_status,
                      "model_exact_conditional_probability":str(r.conditional),
                      "baseline_probability":round(p0,12),
                      "baseline_plus_r1_probability":round(p1,12),
                      "ideal_expected_brier":round(ideal,12),
                      "baseline_expected_brier":round(e0,12),
                      "baseline_plus_r1_expected_brier":round(e1,12),
                      "paired_improvement":round(e0-e1,12)})
    def mean(k):
        return sum(r[k] for r in items)/len(items)
    scoped=[r for r in records if r.candidate is not None]
    indicator_values=sorted(set(r.candidate for r in scoped))
    r1_statuses={s:sum(r.scope_status==s for r in records)
                 for s in sorted(set(r.scope_status for r in records))}
    return {
        "gate":"R8",
        "classification":"TRAIN_TUNE_DEVELOPMENT_PREDICTIVE_COMPARISON_NOT_H1",
        "seed":seed,
        "train_independent_systems":train_n*len(TRAIN),
        "tune_independent_systems":tune_n,
        "train_eligible_systems":len(train),
        "tune_eligible_systems":len(tune),
        "zero_risk_systems":len(records)-len(train)-len(tune),
        "scoped_r1_status_counts":r1_statuses,
        "r1_defined_systems":len(scoped),
        "r1_distinct_defined_values":indicator_values,
        "r1_non_discriminating":len(indicator_values)<=1,
        "baseline_brier_expected_mean":round(mean("baseline_expected_brier"),12),
        "baseline_plus_r1_brier_expected_mean":
            round(mean("baseline_plus_r1_expected_brier"),12),
        "mean_paired_improvement_baseline_minus_augmented":
            round(mean("paired_improvement"),12),
        "exact_known_model_ideal_brier_expected_mean":
            round(mean("ideal_expected_brier"),12),
        "prediction_model":"STANDARDIZED_RIDGE_LINEAR_PROBABILITY_CLIPPED",
        "ridge_penalty_fixed":RIDGE,
        "identical_raw_pre_event_inputs":True,
        "same_train_tune_systems_and_learner":True,
        "feature_enumeration_limit_actions":MAX_ACTIONS,
        "feature_enumeration_limit_paths":MAX_PLANS,
        "feature_wall_ns_total":feature_ns,
        "baseline_fit_predict_wall_ns":base_ns,
        "plus_r1_fit_predict_wall_ns":aug_ns,
        "exact_full_model_is_unbounded_reference":True,
        "equal_wall_time_or_memory_caps_enforced":False,
        "verified_full_histories":checks,
        "sealed_test_families_generated":0,
        "confirmatory_h1_samples":0,
        "tune_system_records":items,
        "result":"PASS",
    }


def public_summary(out: dict) -> dict:
    return {k:v for k,v in out.items()
            if k not in ("tune_system_records","feature_wall_ns_total",
                         "baseline_fit_predict_wall_ns",
                         "plus_r1_fit_predict_wall_ns")}


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--seed",type=int,default=SEED)
    parser.add_argument("--train-n",type=int,default=24)
    parser.add_argument("--tune-n",type=int,default=12)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    out=evaluate(seed=args.seed,train_n=args.train_n,tune_n=args.tune_n,
                 verify=True)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",
                               encoding="utf-8")
    print(json.dumps(public_summary(out),indent=2,sort_keys=True))


if __name__=="__main__":
    main()
