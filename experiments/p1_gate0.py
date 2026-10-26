"""Gate G0: independent exhaustive/DP solvers for bounded generative reachability.

Not P1 confirmatory evidence. Standard-library only. No input consumption or stochasticity.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, replace
from random import Random
from typing import Iterable
import json


@dataclass(frozen=True)
class Rule:
    requires: frozenset[str]
    produces: str
    cost: int = 0
    duration: int = 1

    def __post_init__(self) -> None:
        if self.cost < 0 or self.duration < 1 or self.produces in self.requires:
            raise ValueError("rules require nonnegative cost, positive duration, and no self-prerequisite")


@dataclass(frozen=True)
class Instance:
    initial: frozenset[str]
    goals: frozenset[str]
    rules: tuple[Rule, ...]
    horizon: int
    budget: int

    def __post_init__(self) -> None:
        if self.horizon < 0 or self.budget < 0:
            raise ValueError("time and money bounds cannot be negative")
        if len({r.produces for r in self.rules}) != len(self.rules):
            raise ValueError("one producer per capability in Gate G0")


def exhaustive_oracle(inst: Instance, *, allow_build: bool = True) -> frozenset[str]:
    """Enumerate every legal action sequence, intentionally WITHOUT memoization."""
    goals = set()

    def walk(held: frozenset[str], time: int, spent: int) -> None:
        goals.update(held & inst.goals)
        if not allow_build:
            return
        for rule in inst.rules:
            if (rule.requires <= held and rule.produces not in held
                and time + rule.duration <= inst.horizon
                and spent + rule.cost <= inst.budget):
                walk(held | {rule.produces}, time + rule.duration, spent + rule.cost)

    walk(inst.initial, 0, 0)
    return frozenset(goals)


def dp_reachability(inst: Instance, *, allow_build: bool = True) -> frozenset[str]:
    """Independent mask/time dynamic program keeping the least expenditure."""
    universe = sorted(inst.initial | inst.goals |
                      {r.produces for r in inst.rules} |
                      set().union(*(r.requires for r in inst.rules))) if inst.rules else sorted(inst.initial | inst.goals)
    bits = {cap: 1 << i for i, cap in enumerate(universe)}
    start = sum(bits[x] for x in inst.initial)
    # Layer (time,mask) stores minimum spent budget, with duration >= 1.
    layers = [dict() for _ in range(inst.horizon + 1)]
    layers[0][start] = 0
    reached = 0
    if not allow_build:
        return inst.initial & inst.goals
    compiled = [(sum(bits[x] for x in r.requires), bits[r.produces],r.duration,r.cost)
                for r in inst.rules]
    for t in range(inst.horizon + 1):
        for mask, spent in list(layers[t].items()):
            reached |= mask
            for need, product, duration, cost in compiled:
                nxt = t + duration
                if nxt > inst.horizon or spent + cost > inst.budget:
                    continue
                if (mask & need) != need or (mask & product):
                    continue
                state = mask | product
                prior = layers[nxt].get(state)
                if prior is None or spent + cost < prior:
                    layers[nxt][state] = spent + cost
    return frozenset(x for x in inst.goals if reached & bits[x])


def shock(inst: Instance, removed: Iterable[str]) -> Instance:
    """Remove INITIAL capabilities only; retained production rules can rebuild them."""
    return replace(inst, initial=inst.initial - frozenset(removed))


def rename(inst: Instance, prefix: str = "z_") -> Instance:
    """A bijective relabeling preserving every rule and all constraints."""
    return Instance(frozenset(prefix + x for x in inst.initial),
                    frozenset(prefix + x for x in inst.goals),
                    tuple(Rule(frozenset(prefix + x for x in r.requires),
                               prefix + r.produces, r.cost, r.duration)
                          for r in inst.rules), inst.horizon, inst.budget)


def generated_instances(seed: int = 20261026, n: int = 64) -> tuple[Instance, ...]:
    """Exploratory random tiny instances; no frozen P1 confirmatory sample."""
    rng = Random(seed)
    instances = []
    for _ in range(n):
        base = frozenset(f"c{i}" for i in range(3))
        count = rng.randint(2, 5)
        rules = []
        known = sorted(base)
        for j in range(count):
            product = f"c{j+3}"
            prereq = frozenset(rng.sample(known, rng.randint(1, min(2, len(known)))))
            rules.append(Rule(prereq, product, rng.randint(0, 2), rng.randint(1, 3)))
            known.append(product)
        targets = frozenset(rng.sample(known, rng.randint(1, min(3, len(known)))))
        instances.append(Instance(base, targets, tuple(rules), rng.randint(0, 7), rng.randint(0, 6)))
    return tuple(instances)


def audit(seed: int = 20261026, n: int = 64) -> dict:
    """Raise on first failed property; aggregate deterministic checks, no P1 inference."""
    count = 0
    shocks = 0
    for inst in generated_instances(seed, n):
        variants = (inst, shock(inst, [sorted(inst.initial)[0]]))
        for var in variants:
            shocks += 1 if var != inst else 0
            for enabled in (False, True):
                expect = exhaustive_oracle(var, allow_build=enabled)
                actual = dp_reachability(var, allow_build=enabled)
                assert actual == expect, (var, enabled, actual, expect)
                count += 1
            assert dp_reachability(var, allow_build=False) <= dp_reachability(var)
            assert len(dp_reachability(rename(var))) == len(dp_reachability(var))
            assert dp_reachability(var) <= dp_reachability(replace(var, horizon=var.horizon+1))
            assert dp_reachability(var) <= dp_reachability(replace(var, budget=var.budget+1))
    return {"gate":"G0", "type":"software_correctness_not_H1_test", "seed":seed,
            "instances":n, "shocked_variants":shocks,
            "solver_pair_comparisons":count, "oracle_mismatches":0,
            "outcome":"PASS"}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
