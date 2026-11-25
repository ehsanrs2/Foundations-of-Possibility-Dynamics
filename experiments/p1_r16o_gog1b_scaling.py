"""GOG-1b: bounded factorial scaling, standard indexed backward closure."""
from collections import defaultdict, deque
from dataclasses import asdict, dataclass, replace
from itertools import product
from pathlib import Path
from random import Random
from statistics import median
from time import perf_counter_ns, process_time_ns
import argparse
import json
import subprocess
import sys

from experiments.p1_gate2 import bfs_postfault
from experiments.p1_r10_executable_backup import _preexec_limits
from experiments.p1_r16n_gog1_goal_slicing import (
    CAPS, Work, _action, _model, backward_slice, search, suite, validate,
)

METHODS = ("state_layers", "shared_scan", "goalwise_scan",
           "shared_index", "goalwise_index")
REPETITIONS = 3
ORDER_SEED = 161125


@dataclass
class IndexedWork(Work):
    index_action_checks: int = 0


def index_actions(actions, work):
    """One index per arm, counted even when there is only one goal."""
    by_output = defaultdict(list)
    producers = set()
    for i, action in enumerate(actions):
        work.index_action_checks += 1
        by_output[action.produces].append(i)
        if any(action.yields):
            producers.add(i)
    return by_output, frozenset(producers)


def indexed_slice(actions, goals, index, work):
    by_output, producers = index
    kept = set(producers)
    relevant = set(goals)
    # Every resource producer is retained, regardless of capability output.
    for i in sorted(producers):
        work.slice_action_checks += 1
        relevant.update(actions[i].requires)
    pending = deque(sorted(relevant))
    while pending:
        token = pending.popleft()
        for i in by_output.get(token, ()):
            work.slice_action_checks += 1
            kept.add(i)
            for prereq in sorted(actions[i].requires):
                if prereq not in relevant:
                    relevant.add(prereq)
                    pending.append(prereq)
    return frozenset(relevant), tuple(actions[i] for i in sorted(kept))


def solve(model, method, construction):
    validate(model)
    if method not in METHODS:
        raise ValueError("unregistered method")
    work = IndexedWork()
    actions = tuple(a for a in model.actions if construction or not a.generative)
    index = index_actions(actions, work) if method.endswith("_index") else None
    groups = ([frozenset({g}) for g in sorted(model.goals)]
              if method.startswith("goalwise_") else [model.goals])
    found = {}
    for goals in groups:
        if index is not None:
            relevant, kept = indexed_slice(actions, goals, index, work)
        elif method.endswith("_scan"):
            relevant, kept = backward_slice(actions, goals, work)
        else:
            relevant, kept = None, actions
        found.update(search(model, kept, goals, relevant,
                            method != "state_layers", work))
    return found, asdict(work)


def query(model, method):
    a, wa = solve(model, method, False)
    b, wb = solve(model, method, True)
    if not a.keys() <= b.keys():
        raise AssertionError("permission nesting broken")
    return {"ordinary":a,"constructive":b,
            "new_goals":sorted(b.keys()-a.keys()),
            "gog":len(b.keys()-a.keys()),
            "work":{k:wa[k]+wb[k] for k in wa}}


def factorial():
    result = {}
    for n, overlap, stock, distractors in product(
            (2,4,6), ("disjoint","shared"), (1,3), (0,2)):
        goals = [f"g{i}" for i in range(n)]
        if overlap == "shared":
            actions = [_action("build", ["seed"], "bus", 1, generative=True)]
            actions += [_action(f"serve{i}", ["bus"], g)
                        for i,g in enumerate(goals)]
        else:
            actions = []
            for i,g in enumerate(goals):
                actions += [
                    _action(f"build{i}", ["seed"], f"b{i}", 1, generative=True),
                    _action(f"serve{i}", [f"b{i}"], g)]
        actions += [_action(f"noise{i}", ["seed"], f"unused{i}")
                    for i in range(distractors)]
        model = replace(_model(actions, goals, stock=stock,horizon=4),
                        initial=frozenset({"seed","g0"}))
        name = f"{overlap}_g{n}_stock{stock}_noise{distractors}"
        result[name] = (model, {"overlap":overlap,"goals":n,
                                "stock":stock,"distractors":distractors})
    controls = suite()
    for name in ("resource_yield","resource_tight_time","resource_tight_stock"):
        result[name] = (controls[name], {"overlap":"resource_control"})
    return result


def expected_cases():
    return {name:{"ordinary":bfs_postfault(m,construction=False),
                  "constructive":bfs_postfault(m,construction=True)}
            for name,(m,_) in factorial().items()}


def worker(method):
    import resource
    start = process_time_ns()
    cases = {}
    for name,(model,meta) in factorial().items():
        tick = perf_counter_ns()
        result = query(model,method)
        cases[name] = {**result,"metadata":meta,
                       "query_wall_ms":(perf_counter_ns()-tick)/1e6}
    return {"method":method,"cases":cases,
            "worker_cpu_ms":(process_time_ns()-start)/1e6,
            "peak_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


def orders():
    rng = Random(ORDER_SEED)
    for _ in range(REPETITIONS):
        order = list(METHODS)
        rng.shuffle(order)
        yield order


def run_one(method):
    started = perf_counter_ns()
    try:
        p = subprocess.run([sys.executable,"-m",
            "experiments.p1_r16o_gog1b_scaling","--worker",method],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True,text=True,timeout=CAPS.wall_seconds,
            preexec_fn=lambda:_preexec_limits(CAPS))
    except subprocess.TimeoutExpired:
        return {"status":"WALL_TIMEOUT"}
    except (OSError,subprocess.SubprocessError) as exc:
        return {"status":"SPAWN_FAILURE","error":type(exc).__name__}
    wall = (perf_counter_ns()-started)/1e6
    if p.returncode:
        return {"status":"CHILD_FAILURE","code":p.returncode,
                "wall_ms":wall,"stderr":p.stderr[-1200:]}
    try:
        result = json.loads(p.stdout)
        if result["method"] != method:
            raise ValueError("wrong method")
        return {"status":"PASS","wall_ms":wall,**result}
    except (ValueError,KeyError,TypeError):
        return {"status":"INVALID_OUTPUT","wall_ms":wall}


def compare_runs(runs, oracle):
    if set(runs) != set(METHODS) or any(
            len(v)!=REPETITIONS or any(x["status"]!="PASS" for x in v)
            for v in runs.values()):
        return None
    summary = {}
    for method,repeats in runs.items():
        for r in repeats:
            if r["method"]!=method or set(r["cases"])!=set(oracle):
                raise AssertionError("unpaired runs")
            for name,expected in oracle.items():
                actual = r["cases"][name]
                for arm,value in expected.items():
                    if actual[arm]!=value:
                        raise AssertionError((method,name,arm,"earliest mismatch"))
                new=sorted(expected["constructive"].keys()-expected["ordinary"].keys())
                if actual["new_goals"]!=new or actual["gog"]!=len(new):
                    raise AssertionError("goal difference mismatch")
        first=repeats[0]["cases"]
        if any(r["cases"][name]["work"]!=first[name]["work"]
               for r in repeats for name in first):
            raise AssertionError("nondeterministic work counts")
        classes={}
        for overlap in ("shared","disjoint","resource_control"):
            names=[n for n,c in first.items() if c["metadata"]["overlap"]==overlap]
            classes[overlap]={
                "cases":len(names),
                "work":{k:sum(first[n]["work"][k] for n in names)
                        for k in IndexedWork.__dataclass_fields__},
                "median_sum_query_wall_ms":median(
                    sum(r["cases"][n]["query_wall_ms"] for n in names)
                    for r in repeats),
            }
        summary[method] = {
            "median_process_wall_ms":median(r["wall_ms"] for r in repeats),
            "median_worker_cpu_ms":median(r["worker_cpu_ms"] for r in repeats),
            "median_peak_rss_kib":median(r["peak_rss_kib"] for r in repeats),
            "classes":classes,
            "by_goal_count":{str(n):{
                overlap:sum(c["work"]["action_checks"] for c in first.values()
                    if c["metadata"].get("goals")==n and
                       c["metadata"]["overlap"]==overlap)
                for overlap in ("shared","disjoint")} for n in (2,4,6)},
        }
    return summary


def audit():
    if not sys.platform.startswith("linux"):
        raise RuntimeError("Linux required")
    runs={m:[] for m in METHODS}
    order_list=list(orders())
    for order in order_list:
        for method in order:
            runs[method].append(run_one(method))
    complete=all(x["status"]=="PASS" for v in runs.values() for x in v)
    oracle=expected_cases() if complete else {}
    return {"gate":"GOG-1b","classification":"BOUNDED_DEVELOPMENT_NOT_H1",
            "repetitions":REPETITIONS,"orders":order_list,
            "caps":{"cpu_s":12,"wall_s":12,"address_space_mib":256},
            "exact_cases":len(oracle),"comparison":compare_runs(runs,oracle),
            "runs":runs,"H1_confirmatory_samples":0,
            "sealed_families_accessed":False,"algorithmic_novelty_claimed":False}


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--worker",choices=METHODS)
    args=p.parse_args()
    print(json.dumps(worker(args.worker) if args.worker else audit(),indent=2))
