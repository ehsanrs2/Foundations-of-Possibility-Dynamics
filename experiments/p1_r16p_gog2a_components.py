"""GOG-2a: exact dependency-component grouping, developer rehearsal only."""
from dataclasses import asdict, dataclass, replace
from itertools import combinations, product
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
from experiments.p1_r16n_gog1_goal_slicing import CAPS, _action, _model, search, suite, validate
from experiments.p1_r16o_gog1b_scaling import IndexedWork, index_actions, indexed_slice

METHODS = ("state_layers", "shared_index", "goalwise_index", "fixed_pairs", "adaptive_components")
REPETITIONS = 3
ORDER_SEED = 161126


@dataclass
class GroupWork(IndexedWork):
    pair_tests: int = 0
    merge_operations: int = 0
    union_action_memberships: int = 0
    union_capability_memberships: int = 0


def components(slices, work):
    """Connect goals sharing any retained action, then transitive closure."""
    parent = {g:g for g in sorted(slices)}
    def root(g):
        while parent[g] != g:
            g = parent[g]
        return g
    action_sets = {g:frozenset(a) for g,(_,a) in slices.items()}
    for a,b in combinations(sorted(slices),2):
        work.pair_tests += 1
        if not action_sets[a].isdisjoint(action_sets[b]):
            x,y = root(a),root(b)
            if x != y:
                parent[max(x,y)] = min(x,y)
                work.merge_operations += 1
    groups = {}
    for g in sorted(slices):
        groups.setdefault(root(g),set()).add(g)
    return [frozenset(v) for v in groups.values()]


def union_slice(actions, group, slices, work):
    relevant, kept = set(),set()
    for g in sorted(group):
        r,a = slices[g]
        work.union_action_memberships += len(a)
        work.union_capability_memberships += len(r)
        relevant.update(r)
        kept.update(a)
    # Preserve original order, and do not silently coalesce action aliases.
    work.union_action_memberships += len(actions)
    return frozenset(relevant),tuple(a for a in actions if a in kept)


def solve(model, method, construction):
    validate(model)
    if method not in METHODS:
        raise ValueError("unknown method")
    work=GroupWork()
    actions=tuple(a for a in model.actions if construction or not a.generative)
    goals=sorted(model.goals)
    slices=None
    index=None
    if method=="state_layers":
        groups=[model.goals]
    else:
        index=index_actions(actions,work)
        if method=="adaptive_components":
            slices={g:indexed_slice(actions,frozenset({g}),index,work) for g in goals}
            groups=components(slices,work)
        elif method=="shared_index":
            groups=[model.goals]
        elif method=="fixed_pairs":
            groups=[frozenset(goals[i:i+2]) for i in range(0,len(goals),2)]
        else:
            groups=[frozenset({g}) for g in goals]
    if set().union(*groups)!=model.goals or sum(map(len,groups))!=len(goals):
        raise AssertionError("not an exact goal partition")
    found={}
    for group in groups:
        if slices is not None:
            relevant,kept=union_slice(actions,group,slices,work)
        elif index is not None:
            relevant,kept=indexed_slice(actions,group,index,work)
        else:
            relevant,kept=None,actions
        found.update(search(model,kept,group,relevant,
                            method!="state_layers",work))
    return found,asdict(work),[sorted(g) for g in groups]


def query(model,method):
    a,wa,ga=solve(model,method,False)
    b,wb,gb=solve(model,method,True)
    if not a.keys()<=b.keys():
        raise AssertionError("permission nesting broken")
    return {"ordinary":a,"constructive":b,
            "new_goals":sorted(b.keys()-a.keys()),
            "gog":len(b.keys()-a.keys()),
            "groups":{"ordinary":ga,"constructive":gb},
            "work":{k:wa[k]+wb[k] for k in wa}}


def fixture(n,kind,stock,noise):
    if kind not in ("singleton","pairs","all","chain"):
        raise ValueError("unknown fixture")
    goals=[f"g{i}" for i in range(n)]
    actions=[]
    for i,g in enumerate(goals):
        leader={"singleton":i,"pairs":i%(n//2),"all":0,
                "chain":max(0,i-1)}[kind]
        req=["b"+str(i),"seed" if leader==i else "b"+str(leader)]
        actions.extend([_action(f"build{i}",["seed"],f"b{i}",1,generative=True),
                        _action(f"serve{i}",req,g)])
    actions.extend(_action(f"noise{i}",["seed"],f"unused{i}") for i in range(noise))
    return replace(_model(actions,goals,stock=stock,horizon=4),
                   initial=frozenset({"seed","g0"}))


def cases():
    result={}
    for n,kind,stock,noise in product((4,6),("singleton","pairs","all"),(1,3),(0,2)):
        result[f"{kind}_g{n}_stock{stock}_noise{noise}"]=(
            fixture(n,kind,stock,noise),{"class":kind,"goals":n,"stock":stock,"noise":noise})
    result["chain_g4"]=(fixture(4,"chain",3,0),{"class":"chain","goals":4})
    for name in ("resource_yield","resource_tight_time","resource_tight_stock"):
        result[name]=(suite()[name],{"class":"resource_control"})
    return result


def reference():
    return {name:{"ordinary":bfs_postfault(m,construction=False),
                  "constructive":bfs_postfault(m,construction=True)}
            for name,(m,_) in cases().items()}


def worker(method):
    import resource
    t=process_time_ns()
    results={}
    for name,(model,meta) in cases().items():
        start=perf_counter_ns()
        results[name]={**query(model,method),"metadata":meta,
                       "query_wall_ms":(perf_counter_ns()-start)/1e6}
    return {"method":method,"cases":results,
            "worker_cpu_ms":(process_time_ns()-t)/1e6,
            "peak_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


def orders():
    rng=Random(ORDER_SEED)
    for _ in range(REPETITIONS):
        order=list(METHODS)
        rng.shuffle(order)
        yield order


def run_one(method):
    t=perf_counter_ns()
    try:
        p=subprocess.run([sys.executable,"-m",
            "experiments.p1_r16p_gog2a_components","--worker",method],
            cwd=Path(__file__).resolve().parents[1],capture_output=True,text=True,
            timeout=CAPS.wall_seconds,preexec_fn=lambda:_preexec_limits(CAPS))
    except subprocess.TimeoutExpired:
        return {"status":"WALL_TIMEOUT"}
    except (OSError,subprocess.SubprocessError) as exc:
        return {"status":"SPAWN_FAILURE","error":type(exc).__name__}
    wall=(perf_counter_ns()-t)/1e6
    if p.returncode:
        return {"status":"CHILD_FAILURE","code":p.returncode,"wall_ms":wall,
                "stderr":p.stderr[-1200:]}
    try:
        result=json.loads(p.stdout)
        if result["method"]!=method:
            raise ValueError("wrong method")
        return {"status":"PASS","wall_ms":wall,**result}
    except (ValueError,KeyError,TypeError):
        return {"status":"INVALID_OUTPUT","wall_ms":wall}


def compare(runs,oracle):
    if set(runs)!=set(METHODS) or any(len(v)!=REPETITIONS or
            any(r.get("status")!="PASS" for r in v) for v in runs.values()):
        return None
    if not oracle:
        raise ValueError("empty reference")
    summary={}
    for method,repeats in runs.items():
        first=repeats[0]["cases"]
        for r in repeats:
            if r["method"]!=method or set(r["cases"])!=set(oracle):
                raise AssertionError("unpaired runs")
            for name,e in oracle.items():
                x=r["cases"][name]
                if any(x[k]!=v for k,v in e.items()):
                    raise AssertionError((method,name,"earliest mismatch"))
                new=sorted(e["constructive"].keys()-e["ordinary"].keys())
                if x["new_goals"]!=new or x["gog"]!=len(new):
                    raise AssertionError("goal difference mismatch")
                if x["work"]!=first[name]["work"] or x["groups"]!=first[name]["groups"]:
                    raise AssertionError("nondeterministic work or groups")
        by_class={}
        for kind in ("singleton","pairs","all","chain","resource_control"):
            names=[n for n,c in first.items() if c["metadata"]["class"]==kind]
            by_class[kind]={"cases":len(names),"work":{
                k:sum(first[n]["work"][k] for n in names)
                for k in GroupWork.__dataclass_fields__},
                "median_sum_query_ms":median(sum(r["cases"][n]["query_wall_ms"]
                                                  for n in names) for r in repeats)}
        summary[method]={"median_process_wall_ms":median(r["wall_ms"] for r in repeats),
                         "median_worker_cpu_ms":median(r["worker_cpu_ms"] for r in repeats),
                         "median_peak_rss_kib":median(r["peak_rss_kib"] for r in repeats),
                         "classes":by_class}
    return summary


def audit():
    if not sys.platform.startswith("linux"):
        raise RuntimeError("Linux required")
    runs={m:[] for m in METHODS}
    order_list=list(orders())
    for order in order_list:
        for m in order:
            runs[m].append(run_one(m))
    complete=all(r["status"]=="PASS" for v in runs.values() for r in v)
    oracle=reference() if complete else {}
    return {"gate":"GOG-2a","classification":"BOUNDED_DEVELOPMENT_NOT_H1",
            "orders":order_list,"repetitions":REPETITIONS,
            "caps":{"cpu_s":12,"wall_s":12,"address_space_mib":256},
            "exact_cases":len(oracle),"comparison":compare(runs,oracle),"runs":runs,
            "H1_confirmatory_samples":0,"sealed_families_accessed":False,
            "algorithmic_novelty_claimed":False}


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--worker",choices=METHODS)
    args=p.parse_args()
    print(json.dumps(worker(args.worker) if args.worker else audit(),indent=2))
