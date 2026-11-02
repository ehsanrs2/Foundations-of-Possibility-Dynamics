"""R10: joint executable backup preparation, and all-in subprocess resource caps.

DEVELOPMENT ONLY. These six R9 toy mechanisms and probabilities are assumptions,
not physical validation or independent H1 test systems.

A joint-ready pair means two event-disjoint physical channel delivery mechanisms
can be PREPARED together on ONE legal pre-event action prefix with shared stock,
before the known synthetic event boundary. It does NOT mean recovery succeeds in
all post-event cases. This property is ordinary finite augmented-state
reachability; neither the property nor the algorithms are claimed to be new.

The subprocess comparison enforces the same Linux virtual-address-space,
CPU-time and parent wall-time limits on three *different operations*: static
physical R1, joint-state preparation, and exact finite-model R7 integration.
They do NOT have the same prediction task/representation, and the limits do
not give equal work, equal training data, or predictive evidence for H1.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
from time import perf_counter_ns

from experiments.p1_r3_policy_rollout import Observation, Trial
from experiments.p1_r9_physical_controls import (
    MODES, WorkBudget, audit as r9_audit, bounded_standard_reference,
    fixture, route_scope, static_pair,
)

READY = frozenset({"channel_a", "channel_b"})
MAX_PREFIX_STATES = 512
CONDITIONS = (
    ("separate_one_kit", "independent", 1, 2, 0),
    ("separate_two_kits", "independent", 2, 2, 1),
    ("separate_short_window", "independent", 2, 1, 0),
    ("aliased_same_mechanism", "alias", 2, 2, 0),
    ("common_upstream_cause", "common", 2, 2, 0),
    ("no_kits", "independent", 0, 2, 0),
)


def physical_event_independent(mode: str) -> bool:
    """Checked synthetic identities; never infer physics from action names."""
    scope = route_scope(mode)
    left, right = "rule:serve_a", "rule:serve_b"
    footprint_a = scope.incidence.get(left)
    footprint_b = scope.incidence.get(right)
    if not footprint_a or not footprint_b:
        raise ValueError("undeclared route fault events cannot yield R10 true")
    return (
        scope.mechanisms[left] != scope.mechanisms[right]
        and footprint_a.isdisjoint(footprint_b)
    )


def _validate_fixture(trial: Trial) -> int:
    tau = trial.cases[0].fault.tick
    if len(trial.base.actions) != 4 or len(trial.base.resources) != 1:
        raise ValueError("R10 joint preparation supports only R9 toy grammar")
    if any(c.fault.tick != tau for c in trial.cases):
        raise ValueError("R10 requires a common, predeclared synthetic boundary")
    if not 1 <= tau <= 2 or trial.base.horizon != tau + 1:
        raise ValueError("R10 requires R9 single-repair-tick fixture")
    if not READY.isdisjoint(trial.base.initial):
        raise ValueError("R10 preevent ready channels must not be preloaded")
    return tau


def standard_joint_state_dp(trial: Trial, mode: str) -> dict:
    """Conventional shared-stock augmented-state reachability pre-event.

    Enumerate legal no-lookahead action prefixes, retaining the lexicographically
    smallest witness for each (held capabilities, stock) state. No realized
    future fault, recovery labels or event outcome is supplied to the search.
    """
    tau = _validate_fixture(trial)
    independent = physical_event_independent(mode)
    frontier = {(trial.base.initial, trial.base.stock): ()}
    explored = 0
    layers = [len(frontier)]
    for _tick in range(tau):
        nxt: dict[tuple, tuple[str, ...]] = {}
        for (held, stock), path in sorted(
            frontier.items(), key=lambda pair: (tuple(sorted(pair[0][0])),
                                                pair[0][1], pair[1])):
            options = [("WAIT", held, stock)]
            for a in trial.base.actions:
                explored += 1
                if a.generative and not trial.policy.construction:
                    continue
                if not a.requires <= held:
                    continue
                if any(stock[i] < a.consumes[i]
                       for i in range(len(stock))):
                    continue
                if a.produces in held and not any(a.yields):
                    continue
                after_stock = tuple(stock[i] - a.consumes[i] + a.yields[i]
                                    for i in range(len(stock)))
                options.append((a.name, held | {a.produces}, after_stock))
            for name, new_held, new_stock in options:
                state=(new_held,new_stock)
                proposal=path+(name,)
                if state not in nxt or proposal < nxt[state]:
                    nxt[state]=proposal
        if len(nxt)>MAX_PREFIX_STATES:
            raise RuntimeError("finite state cap exceeded; no false zero permitted")
        frontier=nxt
        layers.append(len(frontier))
    prepared = [path for (caps,_stock),path in frontier.items()
                if READY <= caps]
    witness = min(prepared) if prepared else None
    indicator = int(independent and witness is not None)
    return {
        "scoped_joint_ready_indicator":indicator,
        "physical_event_independent":independent,
        "jointly_prepared_by_some_prefix":witness is not None,
        "executable_prefix_witness":list(witness) if indicator else None,
        "state_layers":layers,
        "action_feasibility_probes":explored,
        "method":"STANDARD_AUGMENTED_STATE_DP",
        "no_future_fault_identity_used":True,
    }


def independent_prefix_history_oracle(trial: Trial, mode: str) -> dict:
    """Separate mutable stock dictionary + exhaustive chronological DFS.

    No calls to the state-DP transition code. This checks the R10 indicator
    and its witness for all bounded R9 cases, not statistical validation.
    """
    tau = _validate_fixture(trial)
    independent = physical_event_independent(mode)
    resources = trial.base.resources
    actions = trial.base.actions
    possible: list[tuple[str,...]] = []
    walks = 0

    def walk(tick: int, owned: set[str], inventory: dict[str,int],
             path: tuple[str,...]) -> None:
        nonlocal walks
        walks += 1
        if tick == tau:
            if READY.issubset(owned):
                possible.append(path)
            return
        walk(tick+1,owned.copy(),inventory.copy(),path+("WAIT",))
        for a in actions:
            if a.generative and not trial.policy.construction:
                continue
            if not a.requires.issubset(owned):
                continue
            if any(inventory[key] < a.consumes[i]
                   for i,key in enumerate(resources)):
                continue
            if a.produces in owned and not any(a.yields):
                continue
            revised=inventory.copy()
            for i,key in enumerate(resources):
                revised[key] += a.yields[i]-a.consumes[i]
            revised_owned=owned.copy()
            revised_owned.add(a.produces)
            walk(tick+1,revised_owned,revised,path+(a.name,))

    walk(0,set(trial.base.initial),
         dict(zip(resources,trial.base.stock)),())
    witness=min(possible) if possible else None
    return {
        "scoped_joint_ready_indicator":int(independent and witness is not None),
        "jointly_prepared_by_some_prefix":witness is not None,
        "executable_prefix_witness":list(witness) if independent and witness else None,
        "independent_history_nodes":walks,
    }


def fixed_policy_preparation(trial: Trial, mode: str) -> dict:
    """Report readiness of ONE fixed policy rather than existential readiness."""
    tau = _validate_fixture(trial)
    held=trial.base.initial
    stock=trial.base.stock
    names={a.name:a for a in trial.base.actions}
    path=[]
    for tick in range(tau):
        chosen=trial.policy.choose(
            Observation(tick,held,stock,frozenset(),False),trial.base.actions)
        path.append(chosen)
        if chosen!="WAIT":
            a=names[chosen]
            held=held | {a.produces}
            stock=tuple(stock[i]-a.consumes[i]+a.yields[i]
                        for i in range(len(stock)))
    return {
        "scoped_ready_for_fixed_policy":int(
            physical_event_independent(mode) and READY <= held),
        "fixed_prefix":path,
        "held_at_boundary":sorted(held),
        "stock_at_boundary":list(stock),
    }


@dataclass(frozen=True)
class ProcessCaps:
    wall_seconds: float = 5.0
    cpu_seconds: int = 5
    address_space_mb: int = 256

    def __post_init__(self):
        if (type(self.wall_seconds) not in (int,float) or
            type(self.cpu_seconds) is not int or
            type(self.address_space_mb) is not int or
            not 0 < self.wall_seconds <= 60 or
            not 1 <= self.cpu_seconds <= 60 or
            not 128 <= self.address_space_mb <= 4096):
            raise ValueError("explicit positive wall, integer CPU, AS caps required")


def worker_operation(method: str, mode: str, kits: int, tau: int) -> dict:
    """One fully bounded method in an isolated process, common R9 raw inputs."""
    trial=fixture(mode=mode,kits=kits,preparation_ticks=tau)
    if method=="static_r1":
        return {"method":method,"result":static_pair(mode,kits)}
    if method=="joint_state":
        return {"method":method,"result":standard_joint_state_dp(trial,mode)}
    if method=="model_reference":
        budget=WorkBudget((trial.base.horizon+1)*len(trial.cases))
        return {"method":method,"result":bounded_standard_reference(trial,budget)}
    raise ValueError("unknown method")


def _preexec_limits(caps: ProcessCaps) -> None:
    """POSIX pre-exec limits cover interpreter imports, feature and evaluation."""
    import resource
    resource.setrlimit(resource.RLIMIT_AS,
                       (caps.address_space_mb*1024*1024,
                        caps.address_space_mb*1024*1024))
    resource.setrlimit(resource.RLIMIT_CPU,
                       (caps.cpu_seconds,caps.cpu_seconds))


def limited_process(method: str, mode: str, kits: int, tau: int,
                    caps: ProcessCaps) -> dict:
    """Same hard caps, measured end-to-end, different output tasks.

    This is a RESOURCE-CAP CONTRACT, not an equal computational-work budget.
    A subprocess failure is exposed and cannot be called a negative feature.
    """
    if os.name!="posix" or not sys.platform.startswith("linux"):
        raise RuntimeError("R10 process limit audit requires Linux")
    if method not in ("static_r1","joint_state","model_reference"):
        raise ValueError("unregistered R10 bounded method")
    _validate_fixture(fixture(mode=mode,kits=kits,preparation_ticks=tau))
    command=[
        sys.executable,"-m","experiments.p1_r10_executable_backup",
        "--worker-method",method,"--mode",mode,"--kits",str(kits),
        "--preparation-ticks",str(tau),
    ]
    started=perf_counter_ns()
    try:
        child=subprocess.run(
            command,cwd=str(Path(__file__).resolve().parents[1]),
            capture_output=True,text=True,timeout=caps.wall_seconds,
            check=False,preexec_fn=lambda: _preexec_limits(caps),
        )
    except subprocess.TimeoutExpired:
        return {"method":method,"status":"WALL_TIMEOUT",
                "wall_limit_seconds":caps.wall_seconds,
                "cpu_limit_seconds":caps.cpu_seconds,
                "address_space_limit_mb":caps.address_space_mb}
    wall_ms=(perf_counter_ns()-started)/1_000_000
    if child.returncode!=0:
        return {"method":method,"status":"CHILD_FAILURE",
                "return_code":child.returncode,
                "stderr_tail":child.stderr[-1500:],
                "wall_limit_seconds":caps.wall_seconds,
                "cpu_limit_seconds":caps.cpu_seconds,
                "address_space_limit_mb":caps.address_space_mb}
    payload=json.loads(child.stdout)
    if payload["method"]!=method:
        raise AssertionError("child method mismatch")
    return {
        "method":method,"status":"PASS",
        "all_in_worker_wall_ms":round(wall_ms,4),
        "worker_cpu_ms":payload["worker_cpu_ms"],
        "worker_peak_rss_kib":payload["worker_peak_rss_kib"],
        "wall_limit_seconds":caps.wall_seconds,
        "cpu_limit_seconds":caps.cpu_seconds,
        "address_space_limit_mb":caps.address_space_mb,
        "result":payload["result"],
    }


def _worker_cli(method: str, mode: str, kits: int, tau: int) -> None:
    import resource
    from time import process_time_ns
    start=process_time_ns()
    answer=worker_operation(method,mode,kits,tau)
    # On GitHub's Linux runner ru_maxrss is KiB (not OS-portable).
    stats=resource.getrusage(resource.RUSAGE_SELF)
    print(json.dumps({
        **answer,
        "worker_cpu_ms":round((process_time_ns()-start)/1_000_000,4),
        "worker_peak_rss_kib":stats.ru_maxrss,
    },sort_keys=True))


def audit(*, caps: ProcessCaps = ProcessCaps()) -> dict:
    """Six predeclared modes, complete independent oracle and capped subprocesses."""
    if not isinstance(caps,ProcessCaps):
        raise TypeError("ProcessCaps instance required")
    r9=r9_audit()
    rows=[]
    independent_checks=0
    for label,mode,kits,tau,expected in CONDITIONS:
        trial=fixture(mode=mode,kits=kits,preparation_ticks=tau)
        dp=standard_joint_state_dp(trial,mode)
        dfs=independent_prefix_history_oracle(trial,mode)
        if (dp["scoped_joint_ready_indicator"] !=
            dfs["scoped_joint_ready_indicator"] or
            dp["executable_prefix_witness"] != dfs["executable_prefix_witness"] or
            dp["jointly_prepared_by_some_prefix"] !=
            dfs["jointly_prepared_by_some_prefix"]):
            raise AssertionError(("joint prefix DP/DFS disagreement",label))
        if dp["scoped_joint_ready_indicator"]!=expected:
            raise AssertionError(("predeclared executable-prefix mismatch",label))
        fixed=fixed_policy_preparation(trial,mode)
        if fixed["scoped_ready_for_fixed_policy"]!=expected:
            raise AssertionError(("fixed policy deviation in R9 grammar",label))
        from_r9=next(item for item in r9["results"] if item["label"]==label)
        outputs={}
        for method in ("static_r1","joint_state","model_reference"):
            item=limited_process(method,mode,kits,tau,caps)
            if item["status"]!="PASS":
                raise RuntimeError(("subprocess resource cap failed",label,item))
            outputs[method]=item
        if (outputs["static_r1"]["result"]!=from_r9["structural"] or
            outputs["joint_state"]["result"]!=dp or
            outputs["model_reference"]["result"]["exact_conditional_restoration"] !=
            from_r9["executed_conditional_restoration"]):
            raise AssertionError(("capped and uncapped computations differ",label))
        independent_checks+=1
        rows.append({
            "label":label,"mode":mode,"kits":kits,
            "preparation_ticks":tau,
            "physical_event_independent":physical_event_independent(mode),
            "static_individually_feasible_backup":
                from_r9["structural"]["scoped_pair"],
            "joint_executable_prefix_backup":
                dp["scoped_joint_ready_indicator"],
            "fixed_policy_ready":fixed["scoped_ready_for_fixed_policy"],
            "joint_prefix_witness":dp["executable_prefix_witness"],
            "standard_duplicated_state_oracle":dfs,
            "fixed_policy_prefix":fixed["fixed_prefix"],
            "strict_restoration_known_model":
                from_r9["executed_conditional_restoration"],
            "capped_process_measurements":outputs,
        })
    return {
        "gate":"R10",
        "classification":"DEVELOPMENT_ONLY_OPERATIONAL_FEASIBILITY_AND_PROCESS_CAPS_NOT_H1",
        "predeclared_toy_systems":len(rows),
        "independently_checked_complete_prefix_systems":independent_checks,
        "R9_reference_full_traces":r9["R7_independent_full_trace_checks"],
        "all_methods_have_same_resource_caps":True,
        "equal_work_or_equal_predictive_objective":False,
        "uniform_caps":{
            "wall_seconds":caps.wall_seconds,
            "cpu_seconds":caps.cpu_seconds,
            "address_space_mb":caps.address_space_mb,
        },
        "physical_identities_assumed_not_field_validated":True,
        "known_fault_boundary_in_toy_fixtures":True,
        "R8_archive_modified":False,
        "H1_training_or_test":False,
        "sealed_family_generator_calls":0,
        "conditions":rows,
        "result":"PASS",
    }


def reproducible_summary(output: dict) -> dict:
    """Drop NONDETERMINISTIC performance measurements before archiving."""
    copy=json.loads(json.dumps(output))
    for row in copy["conditions"]:
        for item in row["capped_process_measurements"].values():
            for field in ("all_in_worker_wall_ms","worker_cpu_ms",
                          "worker_peak_rss_kib"):
                item.pop(field,None)
    return copy


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--worker-method",
                        choices=("static_r1","joint_state","model_reference"))
    parser.add_argument("--mode",choices=MODES)
    parser.add_argument("--kits",type=int)
    parser.add_argument("--preparation-ticks",type=int)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    if args.worker_method:
        if args.mode is None or args.kits is None or args.preparation_ticks is None:
            parser.error("worker requires mode/kits/preparation-ticks")
        _worker_cli(args.worker_method,args.mode,args.kits,
                    args.preparation_ticks)
        return
    data=audit()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(data,sort_keys=True,indent=2)+"\n",
                               encoding="utf-8")
    print(json.dumps(reproducible_summary(data),sort_keys=True,indent=2))


if __name__=="__main__":
    main()
