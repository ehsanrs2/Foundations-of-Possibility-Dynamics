"""Review-driven negative controls for candidate GBR; NOT P1 validation.

The "physical_ids" map is declared externally. A program cannot infer whether
two names mean separate physical failure units or aliases of one unit. This
module does NOT silently replace the existing G1 metric.
"""
from __future__ import annotations

from dataclasses import replace
from itertools import combinations
import json

from experiments.p1_gate1 import (
    Model, Plan, Rule, _backup, enumerate_dfs, example, measures,
)


def alias_fixture() -> Model:
    """One physical route written twice (second name is a bookkeeping alias)."""
    return Model(
        initial=frozenset({"source"}), goals=frozenset({"goal"}),
        rules=(
            Rule("ordinary", frozenset({"source"}), "goal"),
            Rule("alias", frozenset({"source"}), "goal", generative=True),
        ), horizon=1, budget=0,
        exposed=frozenset({"rule:ordinary", "rule:alias"}),
    )


def split_source_fixture() -> Model:
    """Two source tokens that MAY represent one physical unit, by declaration."""
    return Model(
        initial=frozenset({"power_a", "power_b"}), goals=frozenset({"goal"}),
        rules=(
            Rule("route_a", frozenset({"power_a"}), "goal"),
            Rule("route_b", frozenset({"power_b"}), "goal", generative=True),
        ), horizon=1, budget=0,
        exposed=frozenset({"cap:power_a", "cap:power_b"}),
    )


def deadline_fixture() -> Model:
    return Model(
        initial=frozenset({"fast_src", "slow_src"}),
        goals=frozenset({"goal"}),
        rules=(
            Rule("fast", frozenset({"fast_src"}), "goal", duration=1),
            Rule("late_backup", frozenset({"slow_src"}), "goal",
                 duration=4, generative=True),
        ), horizon=4, budget=0,
        exposed=frozenset({"cap:fast_src", "cap:slow_src"}),
    )


def physical_signatures(plans: frozenset[Plan], goal: str,
                        exposed: frozenset[str],
                        physical_ids: dict[str, str]) -> frozenset[tuple]:
    """Only an *illustrative* canonicalization under externally declared IDs.

    Unmapped tokens retain their names. Within this bounded diagnostic, equal
    outcome + full causal physical support + duration + cost means duplicate
    plan descriptions. This is not a universal semantic-equivalence decision.
    """
    out = set()
    for plan in plans:
        if plan.goal != goal:
            continue
        full = frozenset(physical_ids.get(x, x) for x in plan.support)
        vulnerable = frozenset(physical_ids.get(x, x)
                              for x in plan.support if x in exposed)
        out.add((plan.goal, plan.duration, plan.cost, full, vulnerable))
    return frozenset(out)


def canonical_backup(plans: frozenset[Plan], goal: str,
                     exposed: frozenset[str],
                     physical_ids: dict[str, str]) -> int:
    sigs = sorted(physical_signatures(plans, goal, exposed, physical_ids),
                  key=lambda x: (x[0], x[1], x[2],
                                 tuple(sorted(x[3])), tuple(sorted(x[4]))))
    return int(any(not (a[4] & b[4]) for a, b in combinations(sigs, 2)))


def min_failure_hitting_set(plans: frozenset[Plan], goal: str,
                            exposed: frozenset[str],
                            physical_ids: dict[str, str]) -> int | None:
    """Small-set baseline: fewest exposed physical failure IDs hitting ALL plans.

    None = no finite cut within declared F, e.g. some feasible plan has
    zero modeled exposed dependencies. Not a probabilistic reliability score.
    This is exponential and is deliberately restricted to tiny diagnostics.
    """
    sigs = physical_signatures(plans, goal, exposed, physical_ids)
    if not sigs:
        return 0
    deps = [s[4] for s in sigs]
    if any(not d for d in deps):
        return None
    tokens = sorted(set().union(*deps))
    if len(tokens) > 12:
        raise ValueError("review audit supports at most 12 exposed physical IDs")
    for count in range(1, len(tokens) + 1):
        for choice in combinations(tokens, count):
            if all(set(choice) & set(dep) for dep in deps):
                return count
    return None


def audit() -> dict:
    aliases = alias_fixture()
    alias_plans = enumerate_dfs(aliases, construction=True)
    alias_ids = {"rule:ordinary": "physical:one_channel",
                 "rule:alias": "physical:one_channel"}
    split = split_source_fixture()
    split_plans = enumerate_dfs(split, construction=True)
    split_ids = {"cap:power_a": "physical:one_power",
                 "cap:power_b": "physical:one_power"}
    alarm = example()
    alarm_common_cause = replace(
        alarm, exposed=alarm.exposed | {"cap:power"})
    deadline = deadline_fixture()
    deadline_plans = enumerate_dfs(deadline, construction=True)
    slow = next(p for p in deadline_plans if
                "rule:late_backup" in p.support)

    output = {
        "classification": "deterministic_counterexamples_not_H1_evidence",
        "alias_raw_gbr_gain": measures(aliases)["gbr_gain"],
        "alias_raw_gog": measures(aliases)["gog"],
        "alias_physical_pair": canonical_backup(
            alias_plans, "goal", aliases.exposed, alias_ids),
        "alias_min_physical_hitting_set": min_failure_hitting_set(
            alias_plans, "goal", aliases.exposed, alias_ids),
        "alias_expose_shared_source_gbr": measures(replace(
            aliases, exposed=aliases.exposed | {"cap:source"}))["gbr_gain"],
        "empty_scope_pair": _backup(alias_plans, "goal", frozenset()),
        "split_raw_gbr_gain": measures(split)["gbr_gain"],
        "split_declared_shared_physical_pair": canonical_backup(
            split_plans, "goal", split.exposed, split_ids),
        "alarm_original_exposure_gbr_gain": measures(alarm)["gbr_gain"],
        "alarm_shared_power_exposure_gbr_gain":
            measures(alarm_common_cause)["gbr_gain"],
        "deadline_zero_slack_gbr_gain": measures(deadline)["gbr_gain"],
        "deadline_backup_slack_ticks": deadline.horizon - slow.duration,
        "deadline_one_tick_short_gbr_gain":
            measures(replace(deadline, horizon=3))["gbr_gain"],
        "result": "EXPECTED_METRIC_FAILURES_REPRODUCED",
    }
    expected = {
        "alias_raw_gbr_gain": 1, "alias_raw_gog": 0,
        "alias_physical_pair": 0, "alias_min_physical_hitting_set": 1,
        "alias_expose_shared_source_gbr": 0, "empty_scope_pair": 1,
        "split_raw_gbr_gain": 1, "split_declared_shared_physical_pair": 0,
        "alarm_original_exposure_gbr_gain": 1,
        "alarm_shared_power_exposure_gbr_gain": 0,
        "deadline_zero_slack_gbr_gain": 1, "deadline_backup_slack_ticks": 0,
        "deadline_one_tick_short_gbr_gain": 0,
    }
    for key, value in expected.items():
        assert output[key] == value, (key, output[key], value)
    return output


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
