"""G2 bounded recovery with consumable stock and an in-run boundary shock.

Independent exhaustive DFS and time-layer state-set DP implementations.
Each operation takes exactly ONE tick. Fault is applied at an integer tick,
BEFORE goal evaluation or action selection, and never during an action.
This is SOFTWARE verification, not evidence for the P1/GBR hypothesis.
"""
from dataclasses import dataclass, replace
from random import Random
import json


@dataclass(frozen=True)
class Action:
    name: str
    requires: frozenset[str]
    produces: str
    consumes: tuple[int, ...]
    yields: tuple[int, ...]
    generative: bool = False


@dataclass(frozen=True)
class Fault:
    tick: int
    remove: frozenset[str]
    destroy: tuple[int, ...]
    disable: frozenset[str] = frozenset()


@dataclass(frozen=True)
class Model:
    initial: frozenset[str]
    goals: frozenset[str]
    resources: tuple[str, ...]
    stock: tuple[int, ...]
    actions: tuple[Action, ...]
    horizon: int
    fault: Fault

    def __post_init__(self):
        size = len(self.resources)
        if (len(set(self.resources)) != size or not all(self.resources)
            or len(self.stock) != size or any(x < 0 for x in self.stock)):
            raise ValueError("resources must be unique and stocks nonnegative")
        if not (0 <= self.fault.tick <= self.horizon):
            raise ValueError("fault tick must be within horizon")
        if len(self.fault.destroy) != size or any(x < 0 for x in self.fault.destroy):
            raise ValueError("invalid fault stock loss vector")
        if len(set(a.name for a in self.actions)) != len(self.actions):
            raise ValueError("action names must be unique")
        for a in self.actions:
            if (not a.name or not a.produces or
                len(a.consumes) != size or len(a.yields) != size or
                any(x < 0 for x in a.consumes + a.yields)):
                raise ValueError("malformed action or nonnegative stock vectors")


def bfs_postfault(model: Model, *, construction: bool) -> dict[str, int]:
    """State-layer reachability: deduplicate (durables, inventory) each tick."""
    frontier = {(model.initial, model.stock)}
    earliest: dict[str, int] = {}
    for t in range(model.horizon + 1):
        if t == model.fault.tick:
            frontier = {
                (held - model.fault.remove,
                 tuple(max(0, qty - loss) for qty, loss in zip(stock, model.fault.destroy)))
                for held, stock in frontier
            }
        if t >= model.fault.tick:
            for held, _ in frontier:
                for goal in model.goals & held:
                    earliest.setdefault(goal, t)
        if t == model.horizon:
            break
        next_frontier = set(frontier)  # voluntary wait for one tick
        for held, units in frontier:
            for action in model.actions:
                if (action.generative and not construction or
                    t >= model.fault.tick and action.name in model.fault.disable or
                    not action.requires <= held or
                    any(have < cost for have, cost in zip(units, action.consumes))):
                    continue
                after_units = tuple(have - spent + earned
                                    for have, spent, earned in
                                    zip(units, action.consumes, action.yields))
                next_frontier.add((held | {action.produces}, after_units))
        frontier = next_frontier
    return earliest


def dfs_postfault(model: Model, *, construction: bool) -> dict[str, int]:
    """Exhaustive chronological execution oracle, without DP or memoization.

    Implemented via mutable per-path stock dictionaries rather than BFS vectors.
    """
    found: dict[str, int] = {}
    start_stock = dict(zip(model.resources, model.stock))

    def visit(t: int, held: frozenset[str], inventory: dict[str, int]):
        if t == model.fault.tick:
            held = held.difference(model.fault.remove)
            inventory = {
                name: max(0, inventory[name] - model.fault.destroy[i])
                for i, name in enumerate(model.resources)
            }
        if t >= model.fault.tick:
            for goal in held:
                if goal in model.goals:
                    found[goal] = min(found.get(goal, t), t)
        if t == model.horizon:
            return

        visit(t + 1, held, inventory.copy())  # one-tick idle
        for action in model.actions:
            if action.generative and not construction:
                continue
            if t >= model.fault.tick and action.name in model.fault.disable:
                continue
            if not action.requires.issubset(held):
                continue
            if any(inventory[name] < action.consumes[i]
                   for i, name in enumerate(model.resources)):
                continue
            advanced = inventory.copy()
            for i, name in enumerate(model.resources):
                advanced[name] -= action.consumes[i]
                advanced[name] += action.yields[i]
            visit(t + 1, held.union((action.produces,)), advanced)

    visit(0, model.initial, start_stock)
    return found


def compare(model: Model) -> None:
    for setting in (False, True):
        a = bfs_postfault(model, construction=setting)
        b = dfs_postfault(model, construction=setting)
        if a != b:
            raise AssertionError(("independent solvers disagree", model, setting, a, b))
    fixed = bfs_postfault(model, construction=False)
    optional = bfs_postfault(model, construction=True)
    assert all(goal in optional and optional[goal] <= t for goal, t in fixed.items())


def alarm_example() -> Model:
    """Wired signal fails at t=1; optical construction consumes one kit."""
    return Model(
        initial=frozenset({"power", "sensor", "wire", "led", "timer", "assembly"}),
        goals=frozenset({"alarm"}), resources=("kit",), stock=(1,),
        actions=(
            Action("wired", frozenset({"power","sensor","wire"}), "alarm", (0,), (0,)),
            Action("build_optical", frozenset({"led","timer","assembly"}),
                   "optical", (1,), (0,), True),
            Action("optical_alarm", frozenset({"power","sensor","optical"}),
                   "alarm", (0,), (0,)),
        ),
        horizon=3,
        fault=Fault(1, frozenset({"wire", "alarm"}), (0,)),
    )


def generated(seed: int = 20261026, n: int = 64) -> tuple[Model, ...]:
    rng = Random(seed)
    out = []
    for _ in range(n):
        start = frozenset({"a", "b", "c"})
        available = ["a", "b", "c"]
        actions = []
        for i in range(rng.randint(1, 4)):
            output = rng.choice([f"n{i}", "goal"])
            deps = frozenset(rng.sample(available, rng.randint(0, min(2, len(available)))))
            actions.append(Action(f"r{i}", deps, output,
                                  (rng.randint(0, 1), rng.randint(0, 1)),
                                  (rng.randint(0, 1), rng.randint(0, 1)),
                                  bool(rng.getrandbits(1))))
            if output not in available:
                available.append(output)
        horizon = rng.randint(0, 5)
        out.append(Model(
            start, frozenset({"goal", rng.choice(available)}), ("kit","fuel"),
            (rng.randint(0, 2), rng.randint(0, 2)), tuple(actions), horizon,
            Fault(rng.randint(0, horizon),
                  frozenset(rng.sample(list(sorted(start)) + ["goal"], rng.randint(0, 2))),
                  (rng.randint(0, 2), rng.randint(0, 2)),
                  frozenset({rng.choice(actions).name}) if rng.getrandbits(1) else frozenset())
        ))
    return tuple(out)


def audit(seed: int = 20261026, n: int = 64) -> dict:
    comparisons = 0
    for model in generated(seed, n):
        stressed = replace(model, fault=replace(
            model.fault,
            remove=model.fault.remove | {"a"},
            destroy=tuple(x + 1 for x in model.fault.destroy),
            disable=model.fault.disable | {model.actions[0].name}))
        for variant in (model, stressed):
            compare(variant)
            comparisons += 2  # construction off and on
    example = alarm_example()
    compare(example)
    assert bfs_postfault(example, construction=False) == {}
    assert bfs_postfault(example, construction=True) == {"alarm": 2}
    return {"gate": "G2", "status": "software_verification_not_P1",
            "seed":seed, "instances":n, "stressed_variants":n,
            "solver_comparisons":comparisons, "mismatches":0,
            "result":"PASS"}


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True, indent=2))
