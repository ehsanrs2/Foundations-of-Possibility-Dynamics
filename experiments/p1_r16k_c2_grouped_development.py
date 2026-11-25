"""C2a: grouped synthetic DEVELOPMENT transfer, never sealed H1 families.

Fixed R12 grammars plus a fourth, separately staged developer grammar.
No claim of randomly sampled independent systems or isomorphism invariance.
"""
from dataclasses import replace
from fractions import Fraction
from collections import defaultdict
from itertools import product
from time import perf_counter_ns, process_time_ns
import argparse
import json
import subprocess
import sys
from pathlib import Path

from experiments.p1_gate1 import Model as StaticModel, Rule, enumerate_dfs, enumerate_subsets
from experiments.p1_gate2 import Action, Fault, bfs_postfault
from experiments.fault_ontology_r1 import assess
from experiments.p1_r9_physical_controls import MODES, route_scope
from experiments.p1_r12_cross_grammar_transfer import (
    KITS, family_trial, structure_signature, conventional_joint_dp,
    independent_joint_history,
)
from experiments.p1_r11_unknown_time_prediction import exact_model_target
from experiments.p1_r8_dev_predictive_baselines import _standardize, _solve_ridge
from experiments.p1_r10_executable_backup import ProcessCaps, _preexec_limits

FAMILIES = {"direct": "TRAIN", "shared_stage": "TRAIN",
            "asymmetric_stage": "TUNE", "dual_stage_dev": "DEV_EVAL"}
PRIORS = (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4))
METHODS = ("raw", "topology", "non_generative_reachability",
           "physical_event_cut", "augmented_state_dp", "r1_scoped_pair")
CAPS = ProcessCaps(wall_seconds=12, cpu_seconds=12, address_space_mb=256)


def trial_for(family, mode, kits, prior):
    if family not in FAMILIES:
        raise ValueError("only registered developer families allowed")
    if family != "dual_stage_dev":
        return family_trial(family, mode, kits, prior)
    t = family_trial("asymmetric_stage", mode, kits, prior)
    # Separate real extra preparation step for B, not mere renaming.
    actions = (t.base.actions[0],
               Action("open_b", frozenset({"base"}), "port_b",
                      (0,), (0,), True)) + tuple(
        replace(a, requires=frozenset({"port_b"}))
        if a.name == "prepare_b" else a for a in t.base.actions[1:])
    before = tuple(a.name for a in actions)
    after = ("serve_a", "serve_b") + tuple(
        a.name for a in actions if a.name not in ("serve_a", "serve_b"))
    return replace(t, base=replace(t.base, actions=actions),
                   policy=replace(t.policy, before_priority=before,
                                  after_priority=after))


def static_metrics(t, mode):
    """Historical static individual-plan semantics, now using actual grammar.

    One kit budget; 3-tick per-route window (same as R9 static contract).
    New staging operations explicitly protected only in the stipulated toy law.
    """
    b = t.base
    if any(len(a.consumes) != 1 or any(a.yields) for a in b.actions):
        raise ValueError("static projection not valid for this grammar")
    model = StaticModel(frozenset({"base"}), b.goals, tuple(
        Rule(a.name, a.requires, a.produces, a.consumes[0], 1, a.generative)
        for a in b.actions), 3, b.stock[0],
        frozenset({"rule:serve_a", "rule:serve_b"}))
    scope = route_scope(mode)
    added = {"rule:" + a.name: "procedure:" + a.name
             for a in b.actions if "rule:" + a.name not in scope.mechanisms}
    scope = replace(scope, mechanisms={**scope.mechanisms, **added},
                    protected={**scope.protected, **{
                        k: "Protected staging operation in stipulated toy law"
                        for k in added}})
    plans = enumerate_dfs(model, construction=True)
    if plans != enumerate_subsets(model, construction=True):
        raise AssertionError("static plan oracles disagree")
    result = assess(plans, "service", scope)
    if result.status not in ("SCOPED", "NO_FEASIBLE_PLAN"):
        raise ValueError("unknown static feature, never impute zero")
    return result.indicator, result.min_event_cut


def features(t, mode, prior, method):
    if method not in METHODS:
        raise ValueError("unknown method")
    b = t.base
    kits = b.stock[0]
    raw = (float(kits), float(prior), float(mode == "independent"),
           float(mode == "alias"), float(mode == "common"),
           float(len(b.actions)), float(kits >= 1), float(kits >= 2))
    if method == "raw":
        extra = 0
    elif method == "topology":
        extra = sum(len(a.requires) for a in b.actions)
    elif method == "non_generative_reachability":
        # Exclude initially active service: count reachable backup channels.
        q = replace(b, goals=frozenset({"channel_a", "channel_b"}),
                    horizon=3, fault=Fault(0, frozenset(), (0,)))
        extra = len(bfs_postfault(q, construction=False))
    elif method in ("physical_event_cut", "r1_scoped_pair"):
        pair, cut = static_metrics(t, mode)
        extra = cut if method == "physical_event_cut" else pair
    else:
        extra = Fraction()
        for tick, weight in ((2, prior), (3, 1-prior)):
            value = conventional_joint_dp(t, mode, tick)
            if value != independent_joint_history(t, mode, tick):
                raise AssertionError("DP and history disagree")
            extra += weight * value
    return raw + (float(extra),)


def validate_split(rows):
    by_group = {}
    by_signature = {}
    for row in rows:
        partition = row["partition"]
        if partition != FAMILIES[row["family"]]:
            raise ValueError("wrong family partition")
        for table, key in ((by_group, row["group"]),
                           (by_signature, row["signature"])):
            if key in table and table[key] != partition:
                raise ValueError("cross-partition leakage")
            table[key] = partition
    if set(by_group.values()) != set(FAMILIES.values()):
        raise ValueError("missing partition")


def grouped_brier(rows):
    groups = defaultdict(list)
    for row in rows:
        p, q = float(Fraction(row["truth"])), row["prediction"]
        groups[row["group"]].append(p*(1-p)+(q-p)**2)
    if not groups:
        raise ValueError("no eligible groups")
    return sum(sum(v)/len(v) for v in groups.values())/len(groups)


def evaluate(method):
    rows = []
    start = perf_counter_ns()
    for family, mode, kits, prior in product(FAMILIES, MODES, KITS, PRIORS):
        t = trial_for(family, mode, kits, prior)
        x = features(t, mode, prior, method)
        truth, _ = exact_model_target(t, verify=True)
        rows.append({"family": family, "partition": FAMILIES[family],
                     "group": f"{family}:{mode}:{kits}", "prior": str(prior),
                     "signature": structure_signature(t, mode),
                     "x": x, "truth": str(truth)})
    validate_split(rows)
    train = [r for r in rows if r["partition"] == "TRAIN"]
    others = [r for r in rows if r["partition"] != "TRAIN"]
    tx, ox = _standardize([r["x"] for r in train], [r["x"] for r in others])
    coef = _solve_ridge(tx, [float(Fraction(r["truth"])) for r in train],
                        penalty=1)
    for row, x in zip(others, ox):
        row["prediction"] = min(1., max(0., sum(a*b for a,b in zip(coef,x))))
    return {"method": method, "groups": {
        part: len({r["group"] for r in rows if r["partition"] == part})
        for part in set(FAMILIES.values())},
        "feature_distinct_values": len({r["x"][-1] for r in rows}),
        "scores": {part: grouped_brier([r for r in others
                                       if r["partition"] == part])
                   for part in ("TUNE", "DEV_EVAL")},
        "rows": others, "worker_wall_ms": (perf_counter_ns()-start)/1e6,
        "confirmatory_samples": 0}


def audit():
    if not sys.platform.startswith("linux"):
        raise RuntimeError("Linux cap enforcement required")
    runs = {}
    for method in METHODS:
        start = perf_counter_ns()
        try:
            p = subprocess.run([sys.executable, "-m",
                "experiments.p1_r16k_c2_grouped_development", "--worker", method],
                cwd=Path(__file__).resolve().parents[1], text=True,
                capture_output=True, timeout=CAPS.wall_seconds,
                preexec_fn=lambda: _preexec_limits(CAPS))
            if p.returncode:
                runs[method] = {"status": "CHILD_FAILURE", "code": p.returncode,
                                "stderr": p.stderr[-1500:]}
            else:
                runs[method] = {"status": "PASS", **json.loads(p.stdout),
                                "process_wall_ms": (perf_counter_ns()-start)/1e6}
        except subprocess.TimeoutExpired:
            runs[method] = {"status": "WALL_TIMEOUT"}
    result = {"classification": "GROUP_DISJOINT_DEVELOPMENT_ONLY_NOT_H1",
              "H1_preregistered": False, "confirmatory_samples": 0,
              "sealed_families_accessed": False, "runs": runs,
              "comparison": None,
              "caps": {"cpu_s": 12, "wall_s": 12, "address_space_mib": 256}}
    if all(r["status"] == "PASS" for r in runs.values()):
        identities = {tuple((x["group"], x["prior"], x["signature"], x["truth"])
                            for x in r["result"]["rows"]) for r in runs.values()}
        if len(identities) != 1:
            raise AssertionError("unpaired outcomes")
        result["comparison"] = {m: r["result"]["scores"] for m,r in runs.items()}
        result["DP_minus_R1_dev_eval"] = (
            result["comparison"]["augmented_state_dp"]["DEV_EVAL"] -
            result["comparison"]["r1_scoped_pair"]["DEV_EVAL"])
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", choices=METHODS)
    args = parser.parse_args()
    if args.worker:
        import resource
        start = process_time_ns()
        r = evaluate(args.worker)
        print(json.dumps({"result": r, "cpu_ms": (process_time_ns()-start)/1e6,
                          "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
    else:
        print(json.dumps(audit(), indent=2, sort_keys=True))
