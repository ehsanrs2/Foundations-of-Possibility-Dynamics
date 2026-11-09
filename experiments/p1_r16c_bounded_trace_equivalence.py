"""B2: bounded observational *trace-language* equivalence for a G2/GOG subset.

No shock, unit-tick durable actions, finite resource stock and finite horizon.
The full language records every tick's DECLARED visible capability set and
stock. It hides action identity, unobserved capabilities, policies and physical
failure mechanisms. Therefore equality is NOT bisimulation, causal or policy
equivalence, nor proof of physical equivalence or novelty.

All inputs are developer-only; no sealed families or observed H1 outcomes.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Mapping
import json

from experiments.p1_gate2 import Action, Model
from experiments.p1_r16b_semantic_conformance import (
    constructive_goal_fixture, renamed_fixture, evaluate_gog,
    _require_no_shock_profile,
)

MAX_HORIZON = 4
MAX_ACTIONS = 6
MAX_PARTIAL_TRACES = 20000
# snapshot := (canonical visible capabilities held, remaining stock)
Snapshot = tuple[tuple[str, ...], tuple[int, ...]]
Trace = tuple[Snapshot, ...]


@dataclass(frozen=True)
class TraceComparison:
    ordinary_equal: bool
    constructive_equal: bool
    ordinary_left_count: int
    ordinary_right_count: int
    constructive_left_count: int
    constructive_right_count: int
    gog_left: int
    gog_right: int

    def as_dict(self) -> dict:
        return {
            "ordinary_equal": self.ordinary_equal,
            "constructive_equal": self.constructive_equal,
            "ordinary_left_count": self.ordinary_left_count,
            "ordinary_right_count": self.ordinary_right_count,
            "constructive_left_count": self.constructive_left_count,
            "constructive_right_count": self.constructive_right_count,
            "gog_left": self.gog_left,
            "gog_right": self.gog_right,
            # Explicit nonclaims: action choice and unobserved mechanisms are hidden.
            "fixed_policy_equivalence_proven": False,
            "physical_mechanism_identity_proven": False,
            "unbounded_bisimulation_proven": False,
        }


def _projection(model: Model, visible_aliases: Mapping[str, str] | None
                ) -> dict[str, str]:
    """Declare exactly which capability indicators are visible.

    Source keys need not occur in actual state: an absent but observable
    capability is FALSE. Canonical labels are injective within each source.
    Every declared goal is required to be observable (a B2/GOG restriction).
    """
    visible = (dict(visible_aliases) if visible_aliases is not None
               else {g: g for g in model.goals})
    if not model.goals <= visible.keys():
        raise ValueError("each registered goal must be visible")
    if (not visible or any(not isinstance(k, str) or not k or
                           not isinstance(v, str) or not v
                           for k, v in visible.items()) or
            len(set(visible.values())) != len(visible)):
        raise ValueError("observable capability map must be nonempty and injective")
    return visible


def trace_language(model: Model, *, construction: bool,
                   visible_aliases: Mapping[str, str] | None = None
                   ) -> frozenset[Trace]:
    """Exact finite trace language, preserving chronology and stock at every tick.

    Actions are existentially selected (including WAIT), not a shared fixed
    policy. A comparison of these languages cannot validate a controller.
    """
    _require_no_shock_profile(model)
    if (model.horizon > MAX_HORIZON or len(model.actions) > MAX_ACTIONS or
            len(model.goals) > 3):
        raise ValueError("B2 fixed work profile exceeded")
    visible = _projection(model, visible_aliases)

    def snapshot(held: frozenset[str], stock: tuple[int, ...]) -> Snapshot:
        return (tuple(sorted(canonical for original, canonical in visible.items()
                             if original in held)), stock)

    frontier: set[tuple[frozenset[str], tuple[int, ...], Trace]] = {
        (model.initial, model.stock, (snapshot(model.initial, model.stock),))
    }
    for _tick in range(model.horizon):
        next_layer: set[tuple[frozenset[str], tuple[int, ...], Trace]] = set()
        for held, stock, prefix in frontier:
            successors = {(held, stock)}  # one legal tick of voluntary WAIT
            for action in model.actions:
                if action.generative and not construction:
                    continue
                if not action.requires <= held:
                    continue
                if any(have < cost for have, cost in
                       zip(stock, action.consumes)):
                    continue
                units = tuple(have - used + gained for have, used, gained
                              in zip(stock, action.consumes, action.yields))
                successors.add((held | {action.produces}, units))
            for next_held, next_stock in successors:
                next_layer.add((next_held, next_stock,
                                prefix + (snapshot(next_held, next_stock),)))
                if len(next_layer) > MAX_PARTIAL_TRACES:
                    raise ValueError("B2 trace enumeration exceeded work cap")
        frontier = next_layer
    return frozenset(prefix for _, _, prefix in frontier)


def compare_profiles(
    left: Model, right: Model, *,
    left_visible: Mapping[str, str] | None = None,
    right_visible: Mapping[str, str] | None = None,
) -> TraceComparison:
    """Check two legal query arms; reject mismatched query/time/resource contracts."""
    if left.horizon != right.horizon or left.resources != right.resources:
        raise ValueError("time horizon and ordered resource axes must match")
    la, ra = _projection(left, left_visible), _projection(right, right_visible)
    if set(la.values()) != set(ra.values()):
        raise ValueError("canonical observable vocabulary differs")
    if ({la[g] for g in left.goals} != {ra[g] for g in right.goals}):
        raise ValueError("target goal query differs; not an equivalence question")
    ordinary_left = trace_language(left, construction=False, visible_aliases=la)
    ordinary_right = trace_language(right, construction=False, visible_aliases=ra)
    expanded_left = trace_language(left, construction=True, visible_aliases=la)
    expanded_right = trace_language(right, construction=True, visible_aliases=ra)
    return TraceComparison(
        ordinary_left == ordinary_right,
        expanded_left == expanded_right,
        len(ordinary_left), len(ordinary_right),
        len(expanded_left), len(expanded_right),
        evaluate_gog(left).gog, evaluate_gog(right).gog,
    )


def _clone_action(action: Action, *, name: str | None = None,
                  produces: str | None = None,
                  consumes: tuple[int, ...] | None = None) -> Action:
    return replace(action,
                   name=action.name if name is None else name,
                   produces=action.produces if produces is None else produces,
                   consumes=action.consumes if consumes is None else consumes)


def audit() -> dict:
    source = constructive_goal_fixture()
    name_alias = replace(source, actions=source.actions + (
        _clone_action(source.actions[0], name="duplicate_build"),
        Action("inert_self_loop", frozenset({"seed"}), "seed", (0,), (0,)),
    ))
    alias = compare_profiles(source, name_alias)

    renamed = renamed_fixture(source,
        {"seed": "root", "bridge": "relay", "service": "objective"})
    renaming = compare_profiles(
        source, renamed,
        left_visible={"service": "public_goal"},
        right_visible={"objective": "public_goal"},
    )

    direct = replace(source, actions=(
        Action("direct_construct", frozenset({"seed"}), "service",
               (1,), (0,), True),
    ))
    latency = compare_profiles(direct, source)
    free_kit = replace(source, actions=(
        _clone_action(source.actions[0], consumes=(0,)), source.actions[1],
    ))
    resource = compare_profiles(source, free_kit)

    missing_bridge = replace(source, actions=(
        _clone_action(source.actions[0], produces="unusable"),
        source.actions[1],
    ))
    short = compare_profiles(replace(source, horizon=1),
                             replace(missing_bridge, horizon=1))
    long = compare_profiles(source, missing_bridge)

    with_hidden = replace(source, actions=source.actions + (
        Action("unseen_production", frozenset({"seed"}), "secret",
               (0,), (0,)),
    ))
    restricted_view = compare_profiles(source, with_hidden)
    widened_view = compare_profiles(
        source, with_hidden,
        left_visible={"service": "service", "secret": "secret"},
        right_visible={"service": "service", "secret": "secret"},
    )
    if not (
        alias.ordinary_equal and alias.constructive_equal and
        renaming.ordinary_equal and renaming.constructive_equal and
        latency.gog_left == latency.gog_right == 1 and
        latency.ordinary_equal and not latency.constructive_equal and
        resource.gog_left == resource.gog_right == 1 and
        not resource.constructive_equal and
        short.ordinary_equal and short.constructive_equal and
        long.ordinary_equal and not long.constructive_equal and
        restricted_view.ordinary_equal and restricted_view.constructive_equal and
        not widened_view.ordinary_equal and
        not widened_view.constructive_equal and
        not alias.as_dict()["fixed_policy_equivalence_proven"]
    ):
        raise AssertionError("bounded behavioral equivalence examples changed")
    return {
        "gate": "B2",
        "profile": "B2_BOUNDED_VISIBLE_GOAL_STOCK_TRACE_V1",
        "result": "PASS_PROVISIONAL_OBSERVABLE_TRACE_CONFORMANCE",
        "comparison_count": 8,
        "renaming_and_inert_alias_equivalent": True,
        "same_gog_but_different_timing": True,
        "same_gog_but_different_resource_trace": True,
        "equivalence_depends_on_horizon": True,
        "equivalence_depends_on_observation_projection": True,
        "full_policy_or_physical_equivalence_claimed": False,
        "confirmatory_h1_samples": 0,
        "sealed_family_calls": 0,
        "H1_preregistered": False,
        "classification": "SYNTHETIC_BOUNDED_SEMANTIC_DIAGNOSTIC_NOT_H1",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
