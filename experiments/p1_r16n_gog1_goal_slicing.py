"""GOG-1a: exact, ordinary planning optimizations; developer comparison only."""
from dataclasses import dataclass, asdict, replace
from itertools import product
from pathlib import Path
from time import perf_counter_ns, process_time_ns
import argparse
import json
import subprocess
import sys

from experiments.p1_gate2 import Action, Fault, Model, bfs_postfault, dfs_postfault, generated
from experiments.p1_r10_executable_backup import ProcessCaps, _preexec_limits

METHODS = ("state_layers", "pareto", "shared_slice", "goalwise_slice")
CAPS = ProcessCaps(wall_seconds=12, cpu_seconds=12, address_space_mb=256)


@dataclass
class Work:
    expanded: int = 0
    action_checks: int = 0
    dominance_checks: int = 0
    slice_action_checks: int = 0
    retained_actions: int = 0
    search_calls: int = 0


def validate(m):
    if (m.fault.tick != 0 or m.fault.remove or m.fault.disable
            or any(m.fault.destroy)):
        raise ValueError("zero-effect tick-zero fault required")
    if (not m.goals or not all(m.goals) or not 0 <= m.horizon <= 5
            or type(m.horizon) is not int or len(m.actions) > 14
            or len(m.goals) > 8 or len(m.resources) > 2):
        raise ValueError("outside bounded GOG-1a profile")
    values = m.stock + tuple(v for a in m.actions for v in a.consumes + a.yields)
    if any(type(v) is not int or not 0 <= v <= 4 for v in values):
        raise ValueError("bounded nonnegative integer stock/cost/yield required")


def backward_slice(actions, goals, work):
    """Conservative AND/OR relevance closure, retaining resource producers."""
    relevant = set(goals)
    for a in actions:
        work.slice_action_checks += 1
        if any(a.yields):
            relevant.update(a.requires)
    while True:
        before = len(relevant)
        for a in actions:
            work.slice_action_checks += 1
            if a.produces in relevant:
                relevant.update(a.requires)
        if len(relevant) == before:
            break
    kept = []
    for a in actions:
        work.slice_action_checks += 1
        if a.produces in relevant or any(a.yields):
            kept.append(a)
    return frozenset(relevant), tuple(kept)


def pareto(states, work):
    """Same-layer monotone state dominance; no cross-time pruning.

    The ordering ensures a possible dominator is considered first.
    """
    ordered = sorted(states, key=lambda s: (-len(s[0]), -sum(s[1]),
                                           tuple(sorted(s[0])), s[1]))
    kept = []
    for held, stock in ordered:
        for other, units in kept:
            work.dominance_checks += 1
            if held <= other and all(x <= y for x,y in zip(stock,units)):
                break
        else:
            kept.append((held, stock))
    return set(kept)


def search(model, actions, goals, relevant, dominance, work):
    work.search_calls += 1
    work.retained_actions += len(actions)
    frontier = {(model.initial if relevant is None else
                 model.initial & relevant, model.stock)}
    earliest = {}
    for tick in range(model.horizon + 1):
        for held, _ in frontier:
            for g in goals & held:
                earliest.setdefault(g, tick)
        if tick == model.horizon:
            break
        nxt = set(frontier)
        for held, units in frontier:
            work.expanded += 1
            for a in actions:
                work.action_checks += 1
                if not a.requires <= held or any(x < y for x,y in zip(units,a.consumes)):
                    continue
                updated = held | {a.produces}
                if relevant is not None:
                    updated &= relevant
                nxt.add((updated, tuple(x-y+z for x,y,z in
                                         zip(units,a.consumes,a.yields))))
        frontier = pareto(nxt, work) if dominance else nxt
    return earliest


def solve(model, method, construction):
    validate(model)
    if method not in METHODS:
        raise ValueError("unknown method")
    work = Work()
    actions = tuple(a for a in model.actions if construction or not a.generative)
    groups = ([frozenset({g}) for g in sorted(model.goals)]
              if method == "goalwise_slice" else [model.goals])
    found = {}
    for goals in groups:
        relevant, kept = (backward_slice(actions, goals, work)
                          if method in ("shared_slice","goalwise_slice")
                          else (None, actions))
        found.update(search(model, kept, goals, relevant,
                            method != "state_layers", work))
    return found, asdict(work)


def _action(name, requires, output, cost=0, reward=0, generative=False):
    return Action(name, frozenset(requires), output, (cost,), (reward,), generative)


def _model(actions, goals, stock=2, horizon=3):
    return Model(frozenset({"seed"}), frozenset(goals), ("kit",), (stock,),
                 tuple(actions), horizon, Fault(0,frozenset(),(0,)))


def suite():
    models = {}
    for n in (0,4,8):
        a = []
        for i in range(3):
            a += [_action(f"build{i}", ["seed"], f"bridge{i}", 1, generative=True),
                  _action(f"serve{i}", [f"bridge{i}"], f"goal{i}")]
        a += [_action(f"noise{i}", ["seed"], f"unused{i}") for i in range(n)]
        models[f"branches_noise{n}"] = _model(a, [f"goal{i}" for i in range(3)])
    for n in (2,4):
        a = [_action("prepare", ["seed"], "stage", 1, generative=True),
             _action("common", ["stage"], "bus")]
        a += [_action(f"serve{i}", ["bus"], f"goal{i}") for i in range(n)]
        models[f"shared_{n}"] = _model(a, [f"goal{i}" for i in range(n)],
                                       stock=1, horizon=4)
    resource = _model([
        _action("collect", ["seed"], "unrelated", reward=1),
        _action("build", ["seed"], "bridge", 2, generative=True),
        _action("serve", ["bridge"], "goal"),
    ], ["goal"], stock=1, horizon=3)
    models["resource_yield"] = resource
    models["resource_tight_time"] = replace(resource, horizon=2)
    models["resource_tight_stock"] = replace(resource, stock=(0,))
    models["exclusive_goals"] = _model([
        _action("a", ["seed"], "a", 1, generative=True),
        _action("b", ["seed"], "b", 1, generative=True)
    ], ["a","b"], stock=1, horizon=1)
    return models


def query(model, method):
    ordinary, w0 = solve(model, method, False)
    constructive, w1 = solve(model, method, True)
    if not set(ordinary) <= set(constructive):
        raise AssertionError("nested actions do not preserve reachability")
    return {"ordinary":ordinary, "constructive":constructive,
            "new_goals":sorted(set(constructive)-set(ordinary)),
            "gog":len(set(constructive)-set(ordinary)),
            "work":{k:w0[k]+w1[k] for k in w0}}


def reference():
    return {name:{arm:bfs_postfault(m,construction=enabled)
                  for arm,enabled in (("ordinary",False),("constructive",True))}
            for name,m in suite().items()}


def worker(method):
    import resource
    t = process_time_ns()
    result = {name:query(m,method) for name,m in suite().items()}
    return {"method":method, "cases":result,
            "worker_cpu_ms":(process_time_ns()-t)/1e6,
            "peak_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


def audit():
    if not sys.platform.startswith("linux"):
        raise RuntimeError("Linux cap enforcement required")
    runs = {}
    for method in METHODS:
        start = perf_counter_ns()
        try:
            p = subprocess.run([sys.executable,"-m",
                "experiments.p1_r16n_gog1_goal_slicing","--worker",method],
                cwd=Path(__file__).resolve().parents[1],
                capture_output=True,text=True,timeout=CAPS.wall_seconds,
                preexec_fn=lambda:_preexec_limits(CAPS))
            wall=(perf_counter_ns()-start)/1e6
            if p.returncode:
                runs[method]={"status":"CHILD_FAILURE","exit":p.returncode,
                              "wall_ms":wall,"stderr":p.stderr[-1000:]}
            else:
                runs[method]={"status":"PASS","wall_ms":wall,**json.loads(p.stdout)}
        except subprocess.TimeoutExpired:
            runs[method]={"status":"TIMEOUT"}
    result={"gate":"GOG-1a","classification":"DEVELOPER_EXACT_SEARCH_NOT_H1",
            "caps":{"cpu_s":12,"wall_s":12,"address_space_mib":256},
            "comparison":None,"runs":runs,"H1_confirmatory_samples":0,
            "sealed_families_accessed":False,"algorithmic_novelty_claimed":False}
    if any(r["status"]!="PASS" for r in runs.values()):
        return result
    # Independent existing G2 implementation, outside timed worker runs.
    oracle=reference()
    summary={}
    for method,r in runs.items():
        if r["method"]!=method or set(r["cases"])!=set(oracle):
            raise AssertionError("unpaired methods")
        for name,expected in oracle.items():
            actual=r["cases"][name]
            if any(actual[arm]!=v for arm,v in expected.items()):
                raise AssertionError((method,name,"earliest goal mismatch"))
            if actual["new_goals"]!=sorted(set(expected["constructive"])-set(expected["ordinary"])):
                raise AssertionError("goal difference mismatch")
        summary[method]={k:sum(c["work"][k] for c in r["cases"].values())
                         for k in Work.__dataclass_fields__}
    result["comparison"]=summary
    result["exact_suite_cases"]=len(oracle)
    return result


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--worker",choices=METHODS)
    args=p.parse_args()
    print(json.dumps(worker(args.worker) if args.worker else audit(),
                     indent=2,sort_keys=True))
