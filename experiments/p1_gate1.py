"""G1: bounded causal plan supports, shocks, and candidate GOG/GBR-gain.

Two independent enumeration strategies verify tiny instances. Standard library,
deterministic. This is a software verification gate, NOT an H1 statistical test.

Semantics: sequential, monotone capability production; each rule executed at most
once per path; no inputs are consumed; positive integral durations; nonnegative
integral costs; no ongoing faults. Sources and rules are separately shockable.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import combinations
from random import Random
import json


@dataclass(frozen=True)
class Rule:
    name: str
    requires: frozenset[str]
    output: str
    cost: int = 0
    duration: int = 1
    generative: bool = False

    def __post_init__(self):
        if not self.name or not self.output or not self.requires:
            raise ValueError("nonempty rule name, output and prerequisites required")
        if self.output in self.requires or self.duration < 1 or self.cost < 0:
            raise ValueError("no direct self-cycle; duration >=1; cost >=0")


@dataclass(frozen=True)
class Model:
    initial: frozenset[str]
    goals: frozenset[str]
    rules: tuple[Rule, ...]
    horizon: int
    budget: int
    exposed: frozenset[str]

    def __post_init__(self):
        if self.horizon < 0 or self.budget < 0 or not self.exposed:
            raise ValueError("nonnegative bounds and nonempty exposure required")
        if len({r.name for r in self.rules}) != len(self.rules):
            raise ValueError("rule identifiers must be unique")
        if not all(x.startswith(("cap:", "rule:")) for x in self.exposed):
            raise ValueError("exposure tokens must use cap: or rule: prefixes")


@dataclass(frozen=True)
class Plan:
    goal: str
    support: frozenset[str]  # ALL initial source leaves and causal rule IDs
    cost: int
    duration: int
    generative: bool


def _initial_support(initial: frozenset[str]) -> dict[str, frozenset[str]]:
    return {c: frozenset({"cap:" + c}) for c in initial}


def _plan(goal: str, support: frozenset[str], rules: tuple[Rule, ...]) -> Plan:
    used = [r for r in rules if "rule:" + r.name in support]
    return Plan(goal, support, sum(r.cost for r in used),
                sum(r.duration for r in used),
                any(r.generative for r in used))


def enumerate_dfs(model: Model, *, construction: bool) -> frozenset[Plan]:
    """Reference oracle A: depth-first enumeration of all legal action sequences.

    Every output's support is its actual causal ancestry, not every action
    previously executed. Unused prep steps never create spurious backup plans.
    """
    found: set[Plan] = set()
    allowed = tuple(r for r in model.rules if construction or not r.generative)

    def walk(held: dict[str, frozenset[str]], time: int, spent: int) -> None:
        for goal in model.goals & held.keys():
            p = _plan(goal, held[goal], model.rules)
            assert p.duration <= time and p.cost <= spent
            found.add(p)
        for rule in allowed:
            if (rule.output in held or not rule.requires <= held.keys()
                or time + rule.duration > model.horizon
                or spent + rule.cost > model.budget):
                continue
            deps = frozenset({"rule:" + rule.name}).union(
                *(held[x] for x in rule.requires))
            next_held = dict(held)
            next_held[rule.output] = deps
            walk(next_held, time + rule.duration, spent + rule.cost)

    walk(_initial_support(model.initial), 0, 0)
    return frozenset(found)


def enumerate_subsets(model: Model, *, construction: bool) -> frozenset[Plan]:
    """Oracle B: independent power-set search over executed rule sets.

    An action subset is accepted only if all its rules can be topologically
    executed without producing a capability twice. Since production is
    monotone, positive duration, and no prerequisite is consumed, any valid
    ordering respects the same total cost/time. This is intentionally
    exponential and is only a small-network check.
    """
    allowed = tuple(r for r in model.rules if construction or not r.generative)
    if len(allowed) > 16:
        raise ValueError("G1 subset oracle limited to 16 rules")
    found: set[Plan] = set()
    for size in range(len(allowed) + 1):
        for selected in combinations(allowed, size):
            if sum(r.duration for r in selected) > model.horizon:
                continue
            if sum(r.cost for r in selected) > model.budget:
                continue
            outputs = [r.output for r in selected]
            if len(set(outputs)) != len(outputs):
                continue  # at most one producer per produced capability per plan
            if set(outputs) & model.initial:
                continue  # no need to produce already-available initial tokens

            held = _initial_support(model.initial)
            pending = list(selected)
            while pending:
                enabled = next((r for r in pending if r.requires <= held.keys()), None)
                if enabled is None:
                    break
                held[enabled.output] = frozenset({"rule:" + enabled.name}).union(
                    *(held[x] for x in enabled.requires))
                pending.remove(enabled)
            if pending:
                continue
            for goal in model.goals & held.keys():
                p = _plan(goal, held[goal], model.rules)
                assert p.duration <= model.horizon and p.cost <= model.budget
                found.add(p)
    return frozenset(found)


def shocked(model: Model, *failed: str) -> Model:
    """Shock occurs BEFORE planning. Lost sources may be rebuilt by surviving rules.

    'cap:x' removes x from initial stock; 'rule:y' disables rule y.
    A failed rule does not by itself delete an already-held capability.
    """
    removed_sources = {f[4:] for f in failed if f.startswith("cap:")}
    blocked_rules = {f[5:] for f in failed if f.startswith("rule:")}
    invalid = [f for f in failed if not f.startswith(("cap:", "rule:"))]
    if invalid:
        raise ValueError("faults require cap: or rule: prefix")
    return replace(model, initial=model.initial - removed_sources,
                   rules=tuple(r for r in model.rules if r.name not in blocked_rules))


def _backup(plans: frozenset[Plan], goal: str, exposed: frozenset[str]) -> int:
    goal_plans = sorted((p for p in plans if p.goal == goal),
                        key=lambda p: (tuple(sorted(p.support)), p.duration, p.cost))
    return int(any(not ((a.support & exposed) & (b.support & exposed))
                   for a, b in combinations(goal_plans, 2)))


def measures(model: Model, *, enumerator=enumerate_dfs) -> dict:
    static = enumerator(model, construction=False)
    capable = enumerator(model, construction=True)
    static_goals = {p.goal for p in static}
    gained_goals = {p.goal for p in capable} - static_goals
    assert static <= capable, "optional construction must include static plans"
    gain = sum(_backup(capable, g, model.exposed) -
               _backup(static, g, model.exposed) for g in static_goals)
    assert gain >= 0
    return {"gog": len(gained_goals), "gbr_gain": gain,
            "static_goals": len(static_goals),
            "generative_goals": len({p.goal for p in capable}),
            "static_plans": len(static), "all_plans": len(capable)}


def example() -> Model:
    return Model(
        initial=frozenset({"power", "sensor", "wire_tx", "led", "timer", "assembly"}),
        goals=frozenset({"alarm"}),
        rules=(
            Rule("wired_alarm", frozenset({"power","sensor","wire_tx"}), "alarm"),
            Rule("build_optical", frozenset({"led","timer","assembly"}),
                 "optical_tx", 1, 1, True),
            Rule("optical_alarm", frozenset({"power","sensor","optical_tx"}), "alarm"),
        ),
        horizon=2, budget=1,
        exposed=frozenset({"cap:wire_tx", "cap:led", "cap:timer", "cap:assembly"}),
    )


def generated(seed: int = 20261026, count: int = 48) -> tuple[Model, ...]:
    """Small randomized diagnostics only: NOT held-out populations or P1."""
    rng = Random(seed)
    out = []
    for _ in range(count):
        initial = frozenset({"c0", "c1", "c2"})
        known = sorted(initial)
        rules = []
        for k in range(rng.randint(2, 7)):
            possible_outputs = [f"c{k + 3}", "goal"]
            output = rng.choice(possible_outputs)
            choices = [c for c in known if c != output]
            requires = frozenset(rng.sample(choices, rng.randint(1, min(2, len(choices)))))
            rules.append(Rule(f"r{k}", requires, output, rng.randint(0,2),
                              rng.randint(1,2), bool(rng.getrandbits(1))))
            if output not in known:
                known.append(output)
        exposure = {"cap:" + rng.choice(sorted(initial)),
                    "rule:" + rng.choice(rules).name}
        out.append(Model(initial, frozenset({"goal", rng.choice(known)}),
                         tuple(rules), rng.randint(0,7), rng.randint(0,5),
                         frozenset(exposure)))
    return tuple(out)


def audit(seed: int = 20261026, count: int = 48) -> dict:
    comparisons = 0
    for original in generated(seed, count):
        damaged = shocked(original, "cap:" + sorted(original.initial)[0])
        for model in (original, damaged):
            for construct in (False, True):
                a = enumerate_dfs(model, construction=construct)
                b = enumerate_subsets(model, construction=construct)
                assert a == b, ("plan mismatch", model, construct, a ^ b)
                comparisons += 1
            assert measures(model, enumerator=enumerate_dfs) == measures(
                model, enumerator=enumerate_subsets)
    scenario = example()
    assert measures(scenario)["gog"] == 0
    assert measures(scenario)["gbr_gain"] == 1
    assert measures(shocked(scenario, "cap:wire_tx"))["gbr_gain"] == 0
    assert measures(shocked(scenario, "cap:wire_tx"))["gog"] == 1
    return {"gate": "G1", "status":"software_verification_not_H1",
            "seed":seed, "instances":count, "shock_variants":count,
            "plan_set_comparisons":comparisons, "mismatches":0,
            "result":"PASS"}


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True, indent=2))
