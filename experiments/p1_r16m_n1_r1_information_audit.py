"""N1: information-loss and redundancy audit on existing C2a DEVELOPMENT rows.

No new population, no training/tuning, no sealed generator, no H1 decision
based on a held-out experiment. Exact model targets are used only for an
explicit retrospective diagnostic. A separate event-hypergraph counterexample
limits the observed equivalence of R1 and the event cut.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import product
import json

from experiments.p1_gate1 import Plan
from experiments.fault_ontology_r1 import FaultOntology, assess
from experiments.p1_r16k_c2_grouped_development import (
    FAMILIES, PRIORS, KITS, MODES, trial_for, static_metrics, features,
)
from experiments.p1_r11_unknown_time_prediction import exact_model_target


def triangle_counterexample():
    """Three pairwise-intersecting event supports with empty total intersection.

    These are abstract static causal supports, not an instrumented system.
    The minimum event hitting set has size two but no two supports are disjoint.
    """
    scope = FaultOntology("N1_ABSTRACT_TRIANGLE",
        {"rule:ab":"path:ab", "rule:bc":"path:bc", "rule:ac":"path:ac"},
        {"rule:ab":frozenset({"a","b"}), "rule:bc":frozenset({"b","c"}),
         "rule:ac":frozenset({"a","c"})}, {}, frozenset({"a","b","c"}))
    plans = frozenset(Plan("goal",frozenset({token}),0,1,True)
                      for token in scope.mechanisms)
    result = assess(plans,"goal",scope)
    if (result.status,result.indicator,result.min_event_cut) != ("SCOPED",0,2):
        raise AssertionError("triangle negative control changed")
    return {"R1":result.indicator,"minimum_event_cut":result.min_event_cut}


def rows():
    for family,mode,kits,prior in product(FAMILIES,MODES,KITS,PRIORS):
        t = trial_for(family,mode,kits,prior)
        r1,cut = static_metrics(t,mode)
        truth,_ = exact_model_target(t,verify=True)
        raw = features(t,mode,prior,"raw")[:-1]
        yield {"family":family,"partition":FAMILIES[family],"mode":mode,
               "kits":kits,"prior":str(prior),"raw":raw,"R1":r1,"cut":cut,
               "p":truth}


def _serialize(row):
    return {k:str(v) if isinstance(v,Fraction) else v
            for k,v in row.items() if k!="raw"}


def _mean(values):
    return sum(values,Fraction())/len(values)


def _oracle_compression_penalty(data, key):
    """In-sample descriptive best group-constant forecast excess Brier.

    For equal row weights, sum of within-cell squared deviations of exact
    target p from its cell mean. Not a deployable fitted predictor or
    out-of-sample estimate; does NOT imply R1 augmentation harms all learners.
    """
    cells=defaultdict(list)
    for row in data:
        cells[key(row)].append(row["p"])
    return sum((sum((p-_mean(v))**2 for p in v) for v in cells.values()),
               Fraction())/len(data)


def audit():
    data=list(rows())
    if len(data)!=108:
        raise AssertionError("C2a population changed")
    if not all(x["R1"] == int(x["cut"]>=2) ==
               int(x["mode"]=="independent" and x["kits"]>=1) for x in data):
        raise AssertionError("restricted C2a redundancy relation changed")
    # Compare different preparation grammars with the SAME mode, kit stock,
    # time prior, R1 and cut. Only structural staging / fixed-policy ordering
    # changes; no new hazard data are generated.
    cells=defaultdict(list)
    for x in data:
        cells[(x["mode"],x["kits"],x["prior"],x["R1"],x["cut"])].append(x)
    differing=[v for v in cells.values() if len({x["p"] for x in v})>1]
    if not differing:
        raise AssertionError("expected temporal/resource information loss missing")
    widest=max(differing,key=lambda v:max(x["p"] for x in v)-min(x["p"] for x in v))
    lo=min(widest,key=lambda x:x["p"])
    hi=max(widest,key=lambda x:x["p"])
    raw_loss=_oracle_compression_penalty(data,lambda x:x["raw"])
    raw_r1_loss=_oracle_compression_penalty(data,lambda x:(x["raw"],x["R1"]))
    if raw_loss!=raw_r1_loss:
        raise AssertionError("deterministic raw feature refined equivalence classes")
    return {
        "gate":"N1","classification":"RETROSPECTIVE_C2A_DEVELOPMENT_ONLY",
        "rows":len(data),"structure_groups":36,
        "R1_equals_cut_at_least_two_on_C2a":True,
        "R1_equals_independent_times_positive_stock_on_C2a":True,
        "general_cut_equivalence_false":triangle_counterexample(),
        "fixed_mode_stock_prior_pair_cut_cells":len(cells),
        "cells_with_different_exact_recovery":len(differing),
        "widest_matched_cell_gap":str(hi["p"]-lo["p"]),
        "witness_low":_serialize(lo),"witness_high":_serialize(hi),
        "in_sample_R1_only_excess_brier":str(_oracle_compression_penalty(data,lambda x:x["R1"])),
        "in_sample_raw_excess_brier":str(raw_loss),
        "in_sample_raw_plus_R1_excess_brier":str(raw_r1_loss),
        "decision":"PAUSE_R1_CONFIRMATORY_PREPARATION_PENDING_INDEPENDENT_REVIEW",
        "H1_preregistered":False,"H1_confirmatory_samples":0,
        "sealed_families_accessed":False,"field_labels":0,
    }


if __name__=="__main__":
    print(json.dumps(audit(),indent=2,sort_keys=True))
