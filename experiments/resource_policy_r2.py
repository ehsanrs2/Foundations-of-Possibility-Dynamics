"""R2: static physical-backup witnesses vs implementable preparation policies.

A DELIBERATE NEGATIVE CONTROL. It does not introduce a new predictive metric.
The same pair of fault-event-disjoint individual routes can have different
non-clairvoyant success given consumable inventory and preparation deadlines.

Reuses independent policy-state and history solvers from G4 as strong standard
controls; no financial simulation or P1/H1 statistical test is performed.
"""
from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
import json

from experiments.p1_gate1 import Model as StaticModel, Rule, enumerate_dfs
from experiments.p1_gate2 import Action, Fault, Model
from experiments.p1_gate4 import (
    Problem, Scenario, optimal_state_dp, optimal_history_oracle,
    clairvoyant_upper_bound,
)
from experiments.fault_ontology_r1 import (
    FaultOntology, assess, exact_static_survival_probability,
)


def physical_route_scope() -> FaultOntology:
    """Independent physical failure mechanisms are ASSUMED for the toy only."""
    return FaultOntology(
        "R2_TWO_INDEPENDENT_CHANNEL_EVENTS",
        mechanisms={
            "cap:base": "physical:assembly_base",
            "rule:prepare_a": "procedure:prepare_a",
            "rule:prepare_b": "procedure:prepare_b",
            "rule:serve_a": "physical:channel_a",
            "rule:serve_b": "physical:channel_b",
        },
        incidence={
            "rule:serve_a": frozenset({"event:loss_a"}),
            "rule:serve_b": frozenset({"event:loss_b"}),
        },
        protected={
            "cap:base": "Assumed protected in this narrow synthetic experiment",
            "rule:prepare_a": "Preparation operation assumed reliable in toy",
            "rule:prepare_b": "Preparation operation assumed reliable in toy",
        },
        event_universe=frozenset({"event:loss_a", "event:loss_b"}),
    )


def individual_plan_model(*, kits: int = 1) -> StaticModel:
    """G1's per-route budgets allow each route separately, not both together.

    Constructible G1 plans are static causal supports; this cannot establish
    the existence of one non-clairvoyant pre-fault execution covering both.
    """
    if kits < 0:
        raise ValueError("kit count must be nonnegative")
    return StaticModel(
        initial=frozenset({"base"}), goals=frozenset({"service"}),
        rules=(
            Rule("prepare_a", frozenset({"base"}), "channel_a",
                 cost=1, duration=1, generative=True),
            Rule("prepare_b", frozenset({"base"}), "channel_b",
                 cost=1, duration=1, generative=True),
            Rule("serve_a", frozenset({"channel_a"}), "service",
                 duration=1),
            Rule("serve_b", frozenset({"channel_b"}), "service",
                 duration=1),
        ),
        horizon=3,
        budget=kits,
        exposed=frozenset({"rule:serve_a", "rule:serve_b"}),
    )


def bounded_policy_problem(*, kits: int, fault_tick: int = 2) -> Problem:
    """Four independent-event draws at a known boundary, no advance identity.

    Each channel must be prepared before the shock: all remaining kits are
    destroyed at the shock. The service is also removed at the boundary to
    force a *post-fault* operation rather than falsely rewarding early service.
    Exactly one post-shock tick is available.

    Failure events disable the corresponding channel's service operation;
    they do not delete already prepared channel capability.
    """
    if kits < 0 or fault_tick < 0:
        raise ValueError("kits and shock time must be nonnegative")
    actions = (
        Action("prepare_a", frozenset({"base"}), "channel_a",
               (1,), (0,), True),
        Action("prepare_b", frozenset({"base"}), "channel_b",
               (1,), (0,), True),
        Action("serve_a", frozenset({"channel_a"}), "service",
               (0,), (0,)),
        Action("serve_b", frozenset({"channel_b"}), "service",
               (0,), (0,)),
    )
    scenarios = []
    for name, disabled in (
        ("none", frozenset()),
        ("loss_a", frozenset({"serve_a"})),
        ("loss_b", frozenset({"serve_b"})),
        ("both", frozenset({"serve_a", "serve_b"})),
    ):
        scenarios.append(Scenario(
            name, Fraction(1, 4),
            Fault(tick=fault_tick, remove=frozenset({"service"}),
                  destroy=(kits,), disable=disabled)))
    base = Model(
        initial=frozenset({"base"}),
        goals=frozenset({"service"}), resources=("kit",),
        stock=(kits,), actions=actions, horizon=fault_tick + 1,
        fault=Fault(fault_tick, frozenset({"service"}), (kits,)),
    )
    return Problem(base, tuple(scenarios))


def compare(kits: int, tick: int) -> dict:
    problem = bounded_policy_problem(kits=kits, fault_tick=tick)
    dp = optimal_state_dp(problem, construction=True)
    oracle = optimal_history_oracle(problem, construction=True)
    if dp.value != oracle.value:
        raise AssertionError(("non-clairvoyant policy solvers disagree", kits,
                              tick, dp, oracle))
    perfect = clairvoyant_upper_bound(problem, construction=True)
    if dp.value > perfect:
        raise AssertionError("non-clairvoyant result exceeds foresight bound")
    off = optimal_state_dp(problem, construction=False)
    if off.value != optimal_history_oracle(problem, construction=False).value:
        raise AssertionError("baseline solver disagreement")
    static = individual_plan_model(kits=kits)
    plans = enumerate_dfs(static, construction=True)
    scope = physical_route_scope()
    r1 = assess(plans, "service", scope)
    result = {
        "kits": kits, "preparation_ticks": tick,
        "individually_feasible_plans": r1.canonical_plan_count,
        "scoped_backup_pair": r1.indicator,
        "event_min_cut": r1.min_event_cut,
        "nonclairvoyant_policy_success": str(dp.value),
        "clairvoyant_upper_success": str(perfect),
        "no_construction_policy_success": str(off.value),
    }
    if kits >= 1:
        expected = exact_static_survival_probability(
            plans, "service", scope, {
                "event:loss_a": Fraction(1, 2),
                "event:loss_b": Fraction(1, 2),
            })
        result["static_plan_survival"] = str(expected)
    else:
        result["static_plan_survival"] = "0"
    return result


def audit() -> dict:
    one_kit = compare(1, 2)
    two_kits = compare(2, 2)
    too_soon = compare(2, 1)
    no_kits = compare(0, 2)
    assert one_kit["scoped_backup_pair"] == 1
    assert two_kits["scoped_backup_pair"] == 1
    assert one_kit["static_plan_survival"] == "3/4"
    assert one_kit["nonclairvoyant_policy_success"] == "1/2"
    assert one_kit["clairvoyant_upper_success"] == "3/4"
    assert two_kits["nonclairvoyant_policy_success"] == "3/4"
    assert too_soon["nonclairvoyant_policy_success"] == "1/2"
    assert no_kits["scoped_backup_pair"] == 0
    assert no_kits["nonclairvoyant_policy_success"] == "0"
    return {
        "gate": "R2",
        "classification": "constructed_counterexample_not_H1",
        "same_physical_fault_scope": physical_route_scope().scope_id,
        "conditions": [one_kit, two_kits, too_soon, no_kits],
        "result": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
