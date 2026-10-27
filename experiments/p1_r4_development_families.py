"""R4 developer-only family generators. NOT confirmatory P1 or H1.

Training/tuning families only. Two sealed families deliberately cannot be
generated. Stable SHA-256 per-family, per-instance seeds; no built-in hash().
A code-level guard is not a security access-control mechanism.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from random import Random
import json
from experiments.p1_gate2 import Action, Fault, Model
from experiments.p1_r3_policy_rollout import Case, FixedPolicy, Trial, execute, verify

TRAIN = ("random_AND_OR", "modular_clusters", "hub_dependencies")
TUNE = ("temporal_bottleneck",)
SEALED = ("spatial_lattice", "hierarchical_common_cause")


@dataclass(frozen=True)
class DeveloperInstance:
    family: str
    index: int
    seed_id: str
    fingerprint: str
    trial: Trial


def _rule(name, prerequisites, output, kits=0, generative=False):
    return Action(name, frozenset(prerequisites), output, (kits,), (0,), generative)


def _grammar(family, rng):
    start = {"service", "base", "sensor", "spare", "left", "right", "hub"}
    if family == "random_AND_OR":
        for k in range(rng.randint(0, 2)):
            start.add("part_" + str(k))
        a, b = {"base","sensor"}, {"base","spare"}
        for name in sorted(start):
            if name.startswith("part_"):
                (a if rng.getrandbits(1) else b).add(name)
        rules = [
            _rule("prepare_a",a,"ready_a",1,True),
            _rule("prepare_b",b,"ready_b",1,True),
            _rule("restore_a",{"base","ready_a"},"service"),
            _rule("restore_b",{"base","ready_b"},"service"),
        ]
        shared = "base"
    elif family == "modular_clusters":
        rules = [
            _rule("prepare_left",{"left","base"},"ready_left",1,True),
            _rule("prepare_right",{"right","base"},"ready_right",1,True),
            _rule("restore_left",{"left","ready_left"},"service"),
            _rule("restore_right",{"right","ready_right"},"service"),
            _rule("prepare_bridge",{"left","right"},"ready_bridge",1,True),
            _rule("restore_bridge",{"base","ready_bridge"},"service"),
        ]
        shared = "base"
    elif family == "hub_dependencies":
        rules = [
            _rule("prepare_a",{"hub","sensor"},"ready_a",1,True),
            _rule("prepare_b",{"hub","spare"},"ready_b",1,True),
            _rule("restore_a",{"hub","ready_a"},"service"),
            _rule("restore_b",{"hub","ready_b"},"service"),
            _rule("rebuild_hub",{"base","spare"},"hub",1,True),
        ]
        shared = "hub"
    elif family == "temporal_bottleneck":
        rules = [
            _rule("stage_one",{"base","sensor"},"stage_1",1,True),
            _rule("stage_two",{"stage_1","spare"},"stage_2",1,True),
            _rule("prepare_long",{"stage_2"},"ready_long",0,True),
            _rule("prepare_fast",{"base","spare"},"ready_fast",2,True),
            _rule("restore_long",{"ready_long"},"service"),
            _rule("restore_fast",{"ready_fast"},"service"),
        ]
        shared = "base"
    else:
        raise ValueError("unknown development family")
    if rng.getrandbits(1):
        rules.append(_rule("decoy",{"sensor"},"decoy_output"))
    return start, tuple(rules), rng.randint(1,3), shared


def make_instance(family: str, seed: int, index: int) -> DeveloperInstance:
    if family in SEALED:
        raise PermissionError("held-out family SEALED until preregistration")
    if family not in TRAIN + TUNE:
        raise ValueError("unregistered family")
    if type(seed) is not int or type(index) is not int or index < 0:
        raise ValueError("integer seed and nonnegative integer index required")
    digest = sha256(f"R4-DEV-V1|{seed}|{family}|{index}".encode()).hexdigest()
    rng = Random(int(digest[:16],16))
    start, actions, kits, shared = _grammar(family,rng)
    tick = rng.randint(1,3)
    horizon = tick + rng.randint(1,2)
    restore_names = sorted(a.name for a in actions if a.name.startswith("restore_"))
    disabled = frozenset({rng.choice(restore_names)})
    cases = (
        Case("early_loss",Fraction(1,4),Fault(max(0,tick-1),frozenset({"service"}),(0,))),
        Case("main_loss",Fraction(1,4),Fault(tick,frozenset({"service"}),(rng.randint(0, min(2,kits)),),disabled)),
        Case("shared_cause",Fraction(1,4),Fault(tick,frozenset({"service",shared}),(min(1,kits),))),
        Case("retained",Fraction(1,4),Fault(tick,frozenset(),(0,))),
    )
    before = tuple(sorted(a.name for a in actions if not a.name.startswith("restore_"))) + tuple(restore_names)
    after = tuple(restore_names) + tuple(sorted(a.name for a in actions if not a.name.startswith("restore_")))
    trial = Trial(Model(frozenset(start),frozenset({"service"}),("kit",),(kits,),
                        actions,horizon,cases[1].fault),
                  FixedPolicy(before,after,True),cases)
    structure = {"start":sorted(start),"stock":kits,"horizon":horizon,
                 "actions":[(a.name,sorted(a.requires),a.produces,a.consumes) for a in actions],
                 "faults":[(c.name,c.fault.tick,sorted(c.fault.remove),
                            sorted(c.fault.disable),c.fault.destroy) for c in cases]}
    signature=sha256(json.dumps(structure,sort_keys=True).encode()).hexdigest()
    return DeveloperInstance(family,index,digest,signature,trial)


def audit(seed: int=20261027, per_family: int=3) -> dict:
    if type(per_family) is not int or not 1 <= per_family <= 8:
        raise ValueError("development smoke limited to 1..8 instances/family")
    rows, seen, checks = [], set(), 0
    for family in TRAIN + TUNE:
        eligible = restored = 0
        for index in range(per_family):
            obj = make_instance(family, seed, index)
            if obj.seed_id in seen:
                raise AssertionError("duplicate seed stream")
            seen.add(obj.seed_id)
            checks += verify(obj.trial)
            for case in obj.trial.cases:
                label=execute(obj.trial,case).result("service")
                if label is not None:
                    eligible += 1
                    restored += label
        rows.append({"family":family,"independent_dev_instances":per_family,
                     "eligible_diagnostic_cases":eligible,
                     "restored_diagnostic_cases":restored})
    return {"gate":"R4","status":"DEVELOPMENT_DIAGNOSTICS_NOT_H1",
            "seed":seed,"instances":len(seen),"trace_checks":checks,
            "heldout_generated":0,"families":rows,"result":"PASS"}


if __name__ == "__main__":
    print(json.dumps(audit(),sort_keys=True,indent=2))
