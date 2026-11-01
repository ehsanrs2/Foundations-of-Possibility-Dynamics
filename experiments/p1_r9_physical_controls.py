"""R9: predeclared physical route fixtures and bounded known-model work accounting.

DEVELOPER-ONLY constructed controls, not H1 or independent physical evidence.

Fixtures distinguish:
(1) genuinely separate channel failure events,
(2) one aliased physical mechanism with two names,
(3) distinct channels subject to a common-cause event.
R1 plan-pair validity is a structural event-footprint statement, not a
claim that both routes can be prepared with one kit before the shock.

The bounded exact R7 policy reference charges ONE abstract work unit per
executed timeline tick, and returns rigorous bounds if budget stops early.
This is NOT equal-wall-time/RAM fairness across different algorithms.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse
import json

from experiments.p1_gate1 import enumerate_dfs
from experiments.p1_gate2 import Action, Fault, Model
from experiments.p1_r3_policy_rollout import Case, FixedPolicy, Trial
from experiments.p1_r7_silent_observation import (
    execute_observable, independent_observable_oracle,
)
from experiments.resource_policy_r2 import individual_plan_model
from experiments.fault_ontology_r1 import FaultOntology, assess

MODES = ("independent", "alias", "common")
MAX_SCENARIOS = 8
MAX_HORIZON = 3


def route_scope(mode: str) -> FaultOntology:
    """Completely declared synthetic physical identity and fault incidence."""
    if mode not in MODES:
        raise ValueError("unknown physical mechanism mode")
    mechanism_a = "physical:channel_a"
    mechanism_b = "physical:channel_a" if mode == "alias" else "physical:channel_b"
    event_a = frozenset({"event:channel_a"})
    if mode == "alias":
        event_b = event_a
    elif mode == "common":
        event_a = event_a | {"event:common"}
        event_b = frozenset({"event:channel_b", "event:common"})
    else:
        event_b = frozenset({"event:channel_b"})
    return FaultOntology(
        scope_id="R9_DECLARED_TOY_" + mode,
        mechanisms={
            "cap:base": "physical:assembly_base",
            "rule:prepare_a": "procedure:prepare_a",
            "rule:prepare_b": "procedure:prepare_b",
            "rule:serve_a": mechanism_a,
            "rule:serve_b": mechanism_b,
        },
        incidence={
            "rule:serve_a": event_a,
            "rule:serve_b": event_b,
        },
        protected={
            "cap:base": "Assumed protected solely in this bounded fault scope",
            "rule:prepare_a": "Preparation operation assumed reliable in toy",
            "rule:prepare_b": "Preparation operation assumed reliable in toy",
        },
        event_universe=(frozenset({"event:channel_a","event:channel_b","event:common"})
                        if mode == "common"
                        else frozenset({"event:channel_a","event:channel_b"})),
    )


def fixture(*, mode: str, kits: int, preparation_ticks: int = 2) -> Trial:
    """An initially working service MUST actually be removed at the shock.

    Known common shock tick, unknown failure identity. All unused kits are
    destroyed after preparation. Exactly ONE post-shock repair tick is left.
    Hazard indicators are stipulated independent, not calibrated.
    """
    if mode not in MODES:
        raise ValueError("invalid declared physical route mode")
    if type(kits) is not int or not 0 <= kits <= 2:
        raise ValueError("kits must be 0, 1 or 2")
    if type(preparation_ticks) is not int or not 1 <= preparation_ticks <= 2:
        raise ValueError("preparation window is one or two ticks")
    actions=(
        Action("prepare_a",frozenset({"base"}),"channel_a",(1,),(0,),True),
        Action("prepare_b",frozenset({"base"}),"channel_b",(1,),(0,),True),
        Action("serve_a",frozenset({"channel_a"}),"service",(0,),(0,)),
        Action("serve_b",frozenset({"channel_b"}),"service",(0,),(0,)),
    )
    policy=FixedPolicy(
        before_priority=("prepare_a","prepare_b","serve_a","serve_b"),
        after_priority=("serve_a","serve_b","prepare_a","prepare_b"),
        construction=True,
    )
    cases=[]
    common_indicators=(False,True) if mode=="common" else (False,)
    for a,b,common in product((False,True),(False,True),common_indicators):
        p=Fraction(1,4)
        if mode=="common":
            p *= Fraction(1,4) if common else Fraction(3,4)
        disabled=set()
        if a:
            disabled.add("serve_a")
            if mode=="alias":
                disabled.add("serve_b")
        if b and mode!="alias":
            disabled.add("serve_b")
        if common:
            disabled.update(("serve_a","serve_b"))
        cases.append(Case(
            f"a{int(a)}_b{int(b)}_common{int(common)}",
            p, Fault(preparation_ticks, frozenset({"service"}),
                     (kits,),frozenset(disabled)),
        ))
    if sum((c.probability for c in cases),Fraction())!=1:
        raise AssertionError("case probability does not normalize")
    first=cases[0].fault
    base=Model(
        initial=frozenset({"base","service"}),
        goals=frozenset({"service"}),resources=("kit",),stock=(kits,),
        actions=actions,horizon=preparation_ticks+1,fault=first,
    )
    return Trial(base,policy,tuple(cases))


def static_pair(mode: str, kits: int) -> dict:
    """Individual G1 plans; intentionally NOT simultaneous preparation."""
    plans=enumerate_dfs(individual_plan_model(kits=kits),construction=True)
    result=assess(plans,"service",route_scope(mode))
    if result.status!="SCOPED" and kits>0:
        raise AssertionError("toy scope must be complete for each route")
    return {"status":result.status,
            "scoped_pair":result.indicator,
            "individual_plans":result.canonical_plan_count,
            "event_min_cut":result.min_event_cut}


@dataclass(frozen=True)
class WorkBudget:
    """Abstract count of R7 episode tick evaluations, NOT elapsed CPU time."""
    max_ticks: int

    def __post_init__(self):
        if type(self.max_ticks) is not int or self.max_ticks<0:
            raise ValueError("work budget must be a nonnegative integer")


def bounded_standard_reference(trial: Trial, budget: WorkBudget,
                               *, verify: bool = False) -> dict:
    """Exact weighted fixed-policy scenario enumeration with rigorous bounds.

    Valid ONLY when the initial goal is held and all cases remove it at
    the same known boundary; every case is an eligible strict-loss case.
    Partial runs cannot pretend to yield an exact point estimate.

    One counted work unit = one policy timeline tick (t=0..H inclusive).
    Verification with a separate oracle is extra audit cost, NOT charged to
    this budget; do not call this a cross-algorithm equal-compute comparison.
    """
    if trial.base.goals != frozenset({"service"}) or "service" not in trial.base.initial:
        raise ValueError("bounded fixture must begin with service held")
    if any(c.fault.tick!=trial.cases[0].fault.tick or
           "service" not in c.fault.remove for c in trial.cases):
        raise ValueError("all scenarios must delete initially held service at one tick")
    per_case=trial.base.horizon+1
    if per_case > MAX_HORIZON+1 or len(trial.cases)>MAX_SCENARIOS:
        raise ValueError("bounded fixture complexity contract exceeded")
    used=0
    covered=success=Fraction()
    checked=0
    for case in sorted(trial.cases,key=lambda x:x.name):
        if used+per_case>budget.max_ticks:
            break
        out=execute_observable(trial,case)
        if out.result("service") not in (0,1):
            raise AssertionError("eligible actual loss contract broken")
        if verify and out!=independent_observable_oracle(trial,case):
            raise AssertionError("R9 independent full-history mismatch")
        covered+=case.probability
        success+=case.probability*out.result("service")
        used+=per_case
        checked+=int(verify)
    lower=success
    upper=success+(Fraction(1)-covered)
    if not 0<=lower<=upper<=1 or used>budget.max_ticks:
        raise AssertionError("computed exact rational bounds invalid")
    return {
        "budget_ticks":budget.max_ticks,
        "used_ticks":used,
        "coverage_probability":str(covered),
        "lower_conditional_restoration":str(lower),
        "upper_conditional_restoration":str(upper),
        "exact_conditional_restoration":str(lower) if covered==1 else None,
        "scenarios_enumerated":int(used/per_case),
        "scenarios_total":len(trial.cases),
        "independent_history_checks_outside_budget":checked,
        "budget_unit":"ONE_R7_POLICY_TIMELINE_TICK",
        "equal_CPU_WALLTIME_RAM_budget_claim":False,
    }


def audit() -> dict:
    """Predeclared positive/negative tests; no training or test populations."""
    conditions=(
        ("separate_one_kit", "independent",1,2,Fraction(1,2),1,2),
        ("separate_two_kits","independent",2,2,Fraction(3,4),1,2),
        ("separate_short_window","independent",2,1,Fraction(1,2),1,2),
        ("aliased_same_mechanism","alias",2,2,Fraction(1,2),0,1),
        ("common_upstream_cause","common",2,2,Fraction(9,16),0,1),
        ("no_kits","independent",0,2,Fraction(0),0,0),
    )
    rows=[]
    checked=0
    for label,mode,kits,tau,expected,pair,cut in conditions:
        trial=fixture(mode=mode,kits=kits,preparation_ticks=tau)
        scoped=static_pair(mode,kits)
        if scoped["scoped_pair"]!=pair or scoped["event_min_cut"]!=cut:
            raise AssertionError(("physical event incidence mismatch",label,scoped))
        exact=bounded_standard_reference(
            trial, WorkBudget((trial.base.horizon+1)*len(trial.cases)),
            verify=True,
        )
        checked+=exact["independent_history_checks_outside_budget"]
        if Fraction(exact["exact_conditional_restoration"])!=expected:
            raise AssertionError(("R7 actual restoration mismatch",label,exact))
        one_tick=bounded_standard_reference(trial,WorkBudget(1))
        if one_tick["exact_conditional_restoration"] is not None:
            raise AssertionError("partial budget exposed a fake exact prediction")
        partial=bounded_standard_reference(
            trial,WorkBudget((trial.base.horizon+1)*2),
        )
        if not (Fraction(partial["lower_conditional_restoration"]) <= expected
                <= Fraction(partial["upper_conditional_restoration"])):
            raise AssertionError("work-limited bounds did not contain true value")
        rows.append({
            "label":label,"mode":mode,"kits":kits,
            "preparation_ticks":tau,
            "structural":scoped,
            "executed_conditional_restoration":str(expected),
            "full_model_budget":exact,
            "two_scenarios_budget":partial,
        })
    return {
        "gate":"R9",
        "classification":"PREDECLARED_CONSTRUCTED_PHYSICAL_CONTROLS_NOT_H1",
        "toy_conditions":len(rows),
        "R7_independent_full_trace_checks":checked,
        "test_family_generators_called":0,
        "observed_real_physical_failures":0,
        "confirmatory_H1_samples":0,
        "identical_computation_budget_across_algorithms":False,
        "paired_structural_degeneracy_exposed":True,
        "results":rows,
        "result":"PASS",
    }


def public_summary(report: dict) -> dict:
    return report


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    data=audit()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",
                               encoding="utf-8")
    print(json.dumps(public_summary(data),indent=2,sort_keys=True))


if __name__=="__main__":
    main()
