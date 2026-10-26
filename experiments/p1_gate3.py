"""G3: time-consistent post-shock availability, retention, strict restoration and joint goals.

Correctness study only. The full time-indexed state-space solver is a strong
baseline, NOT a novel Possibility Dynamics prediction or P1 finding.

Uses G2's single boundary fault, one-tick actions, durable capabilities,
consumable integer stock, and optional generative actions. Two independent
search *algorithms* share this declared domain semantics.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import json

from experiments.p1_gate2 import Model, Fault, generated, alarm_example, bfs_postfault


@dataclass(frozen=True)
class Outcomes:
    available: dict[str, int]
    retained: frozenset[str]
    restored: dict[str, int]
    joint: int | None

    def as_dict(self) -> dict:
        return {
            "available": dict(sorted(self.available.items())),
            "retained": sorted(self.retained),
            "restored": dict(sorted(self.restored.items())),
            "joint": self.joint,
        }


def augmented_solver(model: Model, *, construction: bool) -> Outcomes:
    """Canonical time-layer DP over (capabilities, stock, lost-at-fault flags).

    Tracking lost-at-fault flags prevents conflating distinct histories with
    equal current holdings and stock when calculating strict restoration.
    """
    states = {(model.initial, model.stock, frozenset())}
    available: dict[str, int] = {}
    restored: dict[str, int] = {}
    retained: set[str] = set()
    joint: int | None = None
    fault = model.fault

    for t in range(model.horizon + 1):
        if t == fault.tick:
            changed = set()
            for caps, stock, _ in states:
                retained.update((caps & model.goals) - fault.remove)
                lost = caps & model.goals & fault.remove
                new_stock = tuple(max(0, x - z) for x, z in zip(stock, fault.destroy))
                changed.add((caps - fault.remove, new_stock, lost))
            states = changed

        if t >= fault.tick:
            for caps, stock, lost in states:
                for goal in caps & model.goals:
                    available[goal] = min(available.get(goal, t), t)
                if t > fault.tick:
                    for goal in caps & lost:
                        restored[goal] = min(restored.get(goal, t), t)
                if model.goals <= caps:
                    joint = t if joint is None else min(joint, t)

        if t == model.horizon:
            break
        next_states = set(states)  # choose a one-tick wait
        for caps, stock, lost in states:
            for action in model.actions:
                if action.generative and not construction:
                    continue
                if t >= fault.tick and action.name in fault.disable:
                    continue
                if not action.requires <= caps:
                    continue
                if any(x < y for x, y in zip(stock, action.consumes)):
                    continue
                new_stock = tuple(x - y + z for x, y, z in
                                  zip(stock, action.consumes, action.yields))
                next_states.add((caps | {action.produces}, new_stock, lost))
        states = next_states

    return Outcomes(available, frozenset(retained), restored, joint)


def history_oracle(model: Model, *, construction: bool) -> Outcomes:
    """Independent history-recursion oracle. No state caching or bitmask DP."""
    earliest: dict[str, int] = {}
    restored: dict[str, int] = {}
    retained: set[str] = set()
    joint: int | None = None
    names = model.resources
    fault = model.fault

    def explore(t: int, held: frozenset[str], inventory: dict[str, int],
                lost: frozenset[str]) -> None:
        nonlocal joint
        if t == fault.tick:
            retained.update((held & model.goals) - fault.remove)
            lost = held & model.goals & fault.remove
            held = held.difference(fault.remove)
            inventory = {
                name: max(0, inventory[name] - fault.destroy[i])
                for i, name in enumerate(names)
            }

        if t >= fault.tick:
            for goal in held:
                if goal in model.goals:
                    earliest[goal] = min(earliest.get(goal, t), t)
                if t > fault.tick and goal in lost:
                    restored[goal] = min(restored.get(goal, t), t)
            if model.goals.issubset(held):
                joint = t if joint is None else min(joint, t)

        if t >= model.horizon:
            return

        explore(t + 1, held, inventory.copy(), lost)  # idle
        for action in model.actions:
            if action.generative and not construction:
                continue
            if t >= fault.tick and action.name in fault.disable:
                continue
            if not action.requires.issubset(held):
                continue
            if any(inventory[name] < action.consumes[i]
                   for i, name in enumerate(names)):
                continue
            remaining = inventory.copy()
            for i, name in enumerate(names):
                remaining[name] += action.yields[i] - action.consumes[i]
            explore(t + 1, held | {action.produces}, remaining, lost)

    explore(0, model.initial, dict(zip(names, model.stock)), frozenset())
    return Outcomes(earliest, frozenset(retained), restored, joint)


def verify(model: Model) -> None:
    """Check two solvers, G2 baseline, and optional-construction nesting."""
    compared = {}
    for construction in (False, True):
        exact = augmented_solver(model, construction=construction)
        oracle = history_oracle(model, construction=construction)
        if exact != oracle:
            raise AssertionError(("G3 mismatch", model, construction, exact, oracle))
        baseline = bfs_postfault(model, construction=construction)
        if exact.available != baseline:
            raise AssertionError(("G2 full-state baseline mismatch", model, construction,
                                  exact.available, baseline))
        compared[construction] = exact
    fixed, optional = compared[False], compared[True]
    for field in ("available", "restored"):
        for goal, time in getattr(fixed, field).items():
            if goal not in getattr(optional, field) or getattr(optional, field)[goal] > time:
                raise AssertionError(("optional actions removed a reachable witness", field, goal))
    if not fixed.retained <= optional.retained:
        raise AssertionError("optional actions removed retention witness")
    if fixed.joint is not None and (optional.joint is None or optional.joint > fixed.joint):
        raise AssertionError("optional actions removed joint goal witness")


def shared_kit_example(*, kits: int) -> Model:
    """Two individually feasible goals share finite consumable inventory."""
    from experiments.p1_gate2 import Action
    return Model(
        initial=frozenset({"base"}), goals=frozenset({"g1", "g2"}),
        resources=("kit",), stock=(kits,),
        actions=(
            Action("route1", frozenset({"base"}), "g1", (1,), (0,)),
            Action("route2", frozenset({"base"}), "g2", (1,), (0,)),
        ),
        horizon=2, fault=Fault(0, frozenset(), (0,)),
    )


def audit(seed: int = 20261026, n: int = 64) -> dict:
    count = 0
    for model in generated(seed=seed, n=n):
        # Use exactly G2's deterministic stressed model construction.
        stressed = replace(model, fault=replace(
            model.fault, remove=model.fault.remove | {"a"},
            destroy=tuple(x + 1 for x in model.fault.destroy),
            disable=model.fault.disable | {model.actions[0].name}))
        for variant in (model, stressed):
            verify(variant)
            count += 2  # construction off and construction on

    example = alarm_example()
    verify(example)
    assert augmented_solver(example, construction=True).as_dict() == {
        "available": {"alarm": 2}, "retained": [],
        "restored": {"alarm": 3}, "joint": 2,
    }
    kit1 = shared_kit_example(kits=1)
    kit2 = shared_kit_example(kits=2)
    verify(kit1)
    verify(kit2)
    assert augmented_solver(kit1, construction=True).joint is None
    assert augmented_solver(kit2, construction=True).joint == 2
    return {
        "gate": "G3", "classification": "bounded_software_verification_not_H1",
        "seed": seed, "original_instances": n, "stressed_variants": n,
        "solver_pair_comparisons": count, "g2_baseline_checks": count,
        "mismatches": 0, "result": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True, indent=2))
