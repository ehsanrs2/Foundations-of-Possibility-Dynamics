"""G4: bounded non-clairvoyant decisions under observed boundary shocks.

Decision at t<tau cannot inspect the realized future scenario. The scenario is
observed at tau, after the shock is applied. Two implementations independently
evaluate an ex-ante optimal deterministic prefix followed by scenario-adaptive
continuation. All results are EXACT small-model calculations, not empirical
P1/GBR predictive evidence.

G2/G3 action semantics: integer consumable inventory, one-tick atomic actions,
durable capabilities, voluntary waiting, exactly one fault at fixed tau.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from random import Random
import json

from experiments.p1_gate2 import Action, Fault, Model
from experiments.p1_gate3 import augmented_solver


@dataclass(frozen=True)
class Scenario:
    name: str
    probability: Fraction
    fault: Fault


@dataclass(frozen=True)
class Problem:
    base: Model
    scenarios: tuple[Scenario, ...]

    def __post_init__(self):
        if not self.base.goals or not self.scenarios:
            raise ValueError("at least one goal and one shock scenario required")
        if len(set(s.name for s in self.scenarios)) != len(self.scenarios):
            raise ValueError("scenario labels must be distinct")
        if any(not s.name or not isinstance(s.probability, Fraction) or
               s.probability <= 0 for s in self.scenarios):
            raise ValueError("scenario probabilities must be positive Fractions")
        if sum((s.probability for s in self.scenarios), Fraction(0)) != 1:
            raise ValueError("scenario probabilities must sum to exactly one")
        if any(s.fault.tick != self.base.fault.tick or
               len(s.fault.destroy) != len(self.base.resources)
               for s in self.scenarios):
            raise ValueError("all scenarios must share one known fault boundary")


@dataclass(frozen=True)
class Choice:
    value: Fraction
    prefix: tuple[str, ...]

    def as_dict(self):
        return {"expected_success": str(self.value),
                "prefix_actions": list(self.prefix)}


def _dp_transitions(base: Model, held: frozenset[str], stock: tuple[int, ...],
                    construction: bool, disabled: frozenset[str]):
    yield "WAIT", held, stock
    for action in base.actions:
        if (action.name in disabled or (action.generative and not construction)
            or not action.requires <= held
            or any(have < cost for have, cost in zip(stock, action.consumes))):
            continue
        units = tuple(have - cost + reward for have, cost, reward in
                      zip(stock, action.consumes, action.yields))
        yield action.name, held | {action.produces}, units


def _dp_after(base: Model, prefix_state: tuple, fault: Fault,
              construction: bool) -> bool:
    """Full post-shock state-set reachability conditional on observed scenario."""
    held, stock = prefix_state
    now = {(held - fault.remove,
            tuple(max(0, x - d) for x, d in zip(stock, fault.destroy)))}
    for t in range(fault.tick, base.horizon + 1):
        if any(base.goals <= capabilities for capabilities, _ in now):
            return True
        if t == base.horizon:
            break
        next_states = set()
        for caps, units in now:
            for _, c, s in _dp_transitions(base, caps, units, construction,
                                            fault.disable):
                next_states.add((c, s))
        now = next_states
    return False


def optimal_state_dp(problem: Problem, *, construction: bool) -> Choice:
    """DP over non-clairvoyant prefix states; recourse after observing the shock."""
    base = problem.base
    current = {(base.initial, base.stock): ()}
    for _ in range(base.fault.tick):
        candidates = {}
        for (caps, stock), prefix in current.items():
            for name, c, s in _dp_transitions(base, caps, stock, construction,
                                              frozenset()):
                key = (c, s)
                proposed = prefix + (name,)
                if key not in candidates or proposed < candidates[key]:
                    candidates[key] = proposed
        current = candidates

    best = Choice(Fraction(-1), ())
    for pre_state, prefix in current.items():
        value = sum((scenario.probability for scenario in problem.scenarios
                     if _dp_after(base, pre_state, scenario.fault, construction)),
                    Fraction(0))
        if value > best.value or (value == best.value and prefix < best.prefix):
            best = Choice(value, prefix)
    assert 0 <= best.value <= 1
    return best


def _history_after(base: Model, capabilities: frozenset[str],
                   stock: dict[str, int], scenario: Scenario,
                   construction: bool) -> bool:
    """Independent post-shock recursive history search; no DP transition reuse."""
    fault = scenario.fault
    capabilities = capabilities.difference(fault.remove)
    stock = {key: max(0, stock[key] - fault.destroy[i])
             for i, key in enumerate(base.resources)}

    def walk(t: int, owned: frozenset[str], money: dict[str, int]) -> bool:
        if base.goals.issubset(owned):
            return True
        if t == base.horizon:
            return False
        if walk(t + 1, owned, money.copy()):
            return True  # one-step wait
        for action in base.actions:
            if action.name in fault.disable or (action.generative and not construction):
                continue
            if not action.requires.issubset(owned):
                continue
            if any(money[key] < action.consumes[i]
                   for i, key in enumerate(base.resources)):
                continue
            updated = money.copy()
            for i, key in enumerate(base.resources):
                updated[key] = updated[key] - action.consumes[i] + action.yields[i]
            if walk(t + 1, owned.union((action.produces,)), updated):
                return True
        return False

    return walk(fault.tick, capabilities, stock)


def optimal_history_oracle(problem: Problem, *, construction: bool) -> Choice:
    """Exhaustive prefix action-history enumeration, branched recourse at tau."""
    base = problem.base
    best = Choice(Fraction(-1), ())

    def before(t: int, owned: frozenset[str], money: dict[str, int],
               prefix: tuple[str, ...]):
        nonlocal best
        if t == base.fault.tick:
            value = sum((s.probability for s in problem.scenarios
                         if _history_after(base, owned, money.copy(), s, construction)),
                        Fraction(0))
            if value > best.value or (value == best.value and prefix < best.prefix):
                best = Choice(value, prefix)
            return

        before(t + 1, owned, money.copy(), prefix + ("WAIT",))
        for action in base.actions:
            if action.generative and not construction:
                continue
            if not action.requires.issubset(owned):
                continue
            if any(money[key] < action.consumes[i]
                   for i, key in enumerate(base.resources)):
                continue
            updated = money.copy()
            for i, key in enumerate(base.resources):
                updated[key] += action.yields[i] - action.consumes[i]
            before(t + 1, owned.union((action.produces,)), updated,
                   prefix + (action.name,))

    before(0, base.initial, dict(zip(base.resources, base.stock)), ())
    assert 0 <= best.value <= 1
    return best


def clairvoyant_upper_bound(problem: Problem, *, construction: bool) -> Fraction:
    """Strong full-information comparator: optimize BEFORE tau per scenario.

    Uses the established G3 augmented state-space solver, with its own fault
    realization known. The result is an upper bound, not an implementable
    non-clairvoyant policy.
    """
    return sum((s.probability for s in problem.scenarios
                if augmented_solver(replace(problem.base, fault=s.fault),
                                    construction=construction).joint is not None),
               Fraction(0))


def verify(problem: Problem) -> None:
    computed = {}
    for setting in (False, True):
        dp = optimal_state_dp(problem, construction=setting)
        oracle = optimal_history_oracle(problem, construction=setting)
        if dp.value != oracle.value:
            raise AssertionError(("nonclairvoyant solver mismatch", problem, setting,
                                  dp, oracle))
        upper = clairvoyant_upper_bound(problem, construction=setting)
        if dp.value > upper:
            raise AssertionError(("nonclairvoyant exceeds clairvoyant", dp, upper))
        computed[setting] = dp.value
    if computed[False] > computed[True]:
        raise AssertionError("optional construction reduced best achievable value")


def information_gap_example() -> Problem:
    """One pre-fault kit; scenario-dependent permitted backup channel."""
    base = Model(
        initial=frozenset({"base"}), goals=frozenset({"service"}),
        resources=("kit",), stock=(1,),
        actions=(
            Action("prepare_a", frozenset({"base"}), "channel_a", (1,), (0,), True),
            Action("prepare_b", frozenset({"base"}), "channel_b", (1,), (0,), True),
            Action("serve_a", frozenset({"channel_a"}), "service", (0,), (0,)),
            Action("serve_b", frozenset({"channel_b"}), "service", (0,), (0,)),
        ), horizon=2, fault=Fault(1, frozenset(), (1,)),
    )
    return Problem(base, (
        Scenario("A", Fraction(1, 2), Fault(1, frozenset(), (1,),
                                            frozenset({"serve_b"}))),
        Scenario("B", Fraction(1, 2), Fault(1, frozenset(), (1,),
                                            frozenset({"serve_a"}))),
    ))


def generated(seed: int = 20261026, n: int = 40) -> tuple[Problem, ...]:
    """Tiny seeded developer diagnostics; NOT independent P1 system families."""
    rng = Random(seed)
    output = []
    for _ in range(n):
        initial = frozenset({"base", "part"})
        possibilities = sorted(initial)
        actions = []
        for i in range(rng.randint(1, 3)):
            target = rng.choice([f"c{i}", "service"])
            prerequisites = frozenset(rng.sample(possibilities, rng.randint(0, 2)))
            actions.append(Action(f"a{i}", prerequisites, target,
                                  (rng.randint(0, 1),), (rng.randint(0, 1),),
                                  bool(rng.getrandbits(1))))
            if target not in possibilities:
                possibilities.append(target)
        horizon = rng.randint(1, 4)
        tau = rng.randint(0, horizon)
        base = Model(initial, frozenset({"service"}), ("kit",),
                     (rng.randint(0, 2),), tuple(actions), horizon,
                     Fault(tau, frozenset(), (0,)))
        scenarios = []
        for j in range(2):
            lost = frozenset({rng.choice(["base", "part", "service"])}) if rng.getrandbits(1) else frozenset()
            disable = frozenset({rng.choice(actions).name}) if rng.getrandbits(1) else frozenset()
            scenarios.append(Scenario(str(j), Fraction(1, 2),
                                      Fault(tau, lost, (rng.randint(0, 2),), disable)))
        output.append(Problem(base, tuple(scenarios)))
    return tuple(output)


def audit(seed: int = 20261026, n: int = 40) -> dict:
    comparisons = 0
    for problem in generated(seed, n):
        stressed = replace(problem, scenarios=tuple(
            replace(s, fault=replace(s.fault, destroy=(s.fault.destroy[0] + 1,)))
            for s in problem.scenarios))
        for p in (problem, stressed):
            verify(p)
            comparisons += 2  # generation off and on
    example = information_gap_example()
    verify(example)
    assert optimal_state_dp(example, construction=True).value == Fraction(1, 2)
    assert optimal_history_oracle(example, construction=True).value == Fraction(1, 2)
    assert clairvoyant_upper_bound(example, construction=True) == Fraction(1)
    assert optimal_state_dp(example, construction=False).value == Fraction(0)
    return {
        "gate": "G4", "classification": "software_verification_not_H1",
        "seed": seed, "instances": n, "stressed_variants": n,
        "oracle_dp_comparisons": comparisons, "mismatches": 0,
        "example_nonclairvoyant_success": "1/2",
        "example_clairvoyant_upper": "1",
        "result": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True, indent=2))
