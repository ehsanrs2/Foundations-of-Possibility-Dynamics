"""R1 fault-event ontology audit: strict coverage, physical mechanisms, and exact tiny baselines.

NOT a replacement for historical G1 GBR and NOT P1/H1 evidence.

Physical mechanism assignments, protected-component assumptions, and the
event incidence table must be independently justified by domain evidence.
The implementation fails closed on missing/ambiguous incidence rather than
converting unknown components to artificially disjoint paths.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from typing import Mapping

from experiments.p1_gate1 import Plan, enumerate_dfs, example
from experiments.gbr_review_counterexamples import alias_fixture, split_source_fixture


@dataclass(frozen=True)
class FaultOntology:
    scope_id: str
    mechanisms: Mapping[str, str]
    incidence: Mapping[str, frozenset[str]]
    protected: Mapping[str, str]
    event_universe: frozenset[str]

    def __post_init__(self) -> None:
        if not self.scope_id.strip() or not self.event_universe:
            raise ValueError("scope ID and event universe must be declared")
        if any(not x.strip() for x in self.event_universe):
            raise ValueError("blank failure event")
        known = set(self.incidence) | set(self.protected)
        if (set(self.incidence) & set(self.protected)
            or set(self.mechanisms) != known
            or not known):
            raise ValueError("mechanism labels and exposed/protected partition must agree")
        if any(not x or not x.strip() for x in self.mechanisms.values()):
            raise ValueError("mechanism identities must be explicit")
        if any(not reason.strip() for reason in self.protected.values()):
            raise ValueError("protected components require written justification")
        for values in self.incidence.values():
            if not values or not values <= self.event_universe:
                raise ValueError("each exposed component requires known failure events")
        # An assertion of one physical mechanism with incompatible failure
        # incidence is contradictory in this *restricted* ontology.
        seen: dict[str, frozenset[str]] = {}
        for token, mechanism in self.mechanisms.items():
            footprint = self.incidence.get(token, frozenset())
            if mechanism in seen and seen[mechanism] != footprint:
                raise ValueError("same physical mechanism has conflicting event incidence")
            seen[mechanism] = footprint


@dataclass(frozen=True)
class Support:
    goal: str
    physical_mechanisms: frozenset[str]
    failure_events: frozenset[str]
    duration: int
    cost: int


@dataclass(frozen=True)
class Assessment:
    status: str
    indicator: int | None
    canonical_plan_count: int
    min_event_cut: int | None


def normalized_supports(plans: frozenset[Plan], goal: str,
                        scope: FaultOntology) -> frozenset[Support]:
    result = set()
    for plan in plans:
        if plan.goal != goal:
            continue
        missing = plan.support - scope.mechanisms.keys()
        if missing:
            raise ValueError("unmapped causal support; cannot score: " +
                             ", ".join(sorted(missing)))
        physical = frozenset(scope.mechanisms[t] for t in plan.support)
        events = frozenset().union(
            *(scope.incidence.get(t, frozenset()) for t in plan.support))
        result.add(Support(goal, physical, events, plan.duration, plan.cost))
    return frozenset(result)


def minimum_event_cut(supports: frozenset[Support]) -> int | None:
    """Size of smallest set of fault EVENTS intersecting every plan.

    Empty plan set => 0; any path without modeled exposed events => None,
    signifying that the declared faults cannot disable all paths.
    This is not a dynamic causal-repair min-cut.
    """
    if not supports:
        return 0
    if any(not p.failure_events for p in supports):
        return None
    events = sorted(set().union(*(p.failure_events for p in supports)))
    if len(events) > 12:
        raise ValueError("exact cut audit limited to at most 12 event IDs")
    for count in range(1, len(events) + 1):
        for failed in combinations(events, count):
            if all(p.failure_events.intersection(failed) for p in supports):
                return count
    raise AssertionError("cut exists for finite nonempty event supports")


def assess(plans: frozenset[Plan], goal: str, scope: FaultOntology) -> Assessment:
    paths = normalized_supports(plans, goal, scope)
    if not paths:
        return Assessment("NO_FEASIBLE_PLAN", 0, 0, 0)
    if any(not p.failure_events for p in paths):
        # Fail closed: no independence assertion when at least one path has
        # no failure exposure in the specified event universe.
        return Assessment("INSUFFICIENT_FAULT_COVERAGE", None, len(paths), None)
    backed = int(any(not (a.failure_events & b.failure_events)
                     for a, b in combinations(paths, 2)))
    return Assessment("SCOPED", backed, len(paths), minimum_event_cut(paths))


def exact_static_survival_probability(
        plans: frozenset[Plan], goal: str, scope: FaultOntology,
        probabilities: Mapping[str, Fraction]) -> Fraction:
    """P(at least one listed plan survives one simultaneous event draw).

    ASSUMES distinct basic fault EVENT indicators are independent; shared
    event IDs encode the modeled common-cause effect. Not post-shock recovery.
    The calculation deliberately enumerates at most twelve event variables.
    """
    result = assess(plans, goal, scope)
    if result.status != "SCOPED":
        raise ValueError("survival calculation requires informative fault scope")
    if set(probabilities) != set(scope.event_universe):
        raise ValueError("all and only registered event probabilities required")
    if any(not isinstance(p, Fraction) or not 0 <= p <= 1
           for p in probabilities.values()):
        raise ValueError("use exact rational probabilities between 0 and 1")
    names = sorted(scope.event_universe)
    if len(names) > 12:
        raise ValueError("tiny exact reliability oracle limited to 12 events")
    paths = normalized_supports(plans, goal, scope)
    survival = Fraction()
    for occurred in product((False, True), repeat=len(names)):
        failed = frozenset(n for n, bit in zip(names, occurred) if bit)
        weight = Fraction(1)
        for name, bit in zip(names, occurred):
            p = probabilities[name]
            weight *= p if bit else 1 - p
        if any(not (route.failure_events & failed) for route in paths):
            survival += weight
    return survival


def alias_scope(*, physically_distinct: bool) -> FaultOntology:
    mechanisms = {"cap:source": "source:shared",
                  "rule:ordinary": "device:channel_a",
                  "rule:alias": ("device:channel_b" if physically_distinct
                                 else "device:channel_a")}
    incidence = {"rule:ordinary": frozenset({"event:failure_a"}),
                 "rule:alias": frozenset({"event:failure_b"} if physically_distinct
                                          else {"event:failure_a"})}
    events = frozenset({"event:failure_a", "event:failure_b"}) if physically_distinct else frozenset({"event:failure_a"})
    return FaultOntology(
        "ALIAS_TWO_PHYSICAL" if physically_distinct else "ALIAS_ONE_PHYSICAL",
        mechanisms, incidence, {"cap:source": "Assumed operationally available during mission"},
        events)


def split_source_scope() -> FaultOntology:
    return FaultOntology(
        "DECLARED_SINGLE_POWER_SOURCE",
        {"cap:power_a": "unit:power", "cap:power_b": "unit:power",
         "rule:route_a": "procedure:a", "rule:route_b": "procedure:b"},
        {"cap:power_a": frozenset({"event:grid"}),
         "cap:power_b": frozenset({"event:grid"})},
        {"rule:route_a": "Procedure assumed not subject to modeled failures",
         "rule:route_b": "Procedure assumed not subject to modeled failures"},
        frozenset({"event:grid"}))


def alarm_scope(*, common_power_exposed: bool) -> FaultOntology:
    mechanisms = {
        **{"cap:" + c: "component:" + c for c in
           ("power", "sensor", "wire_tx", "led", "timer", "assembly")},
        **{"rule:" + r.name: "implementation:" + r.name
           for r in example().rules},
    }
    incidence = {"cap:" + c: frozenset({"event:" + c})
                 for c in ("wire_tx", "led", "timer", "assembly")}
    protected = {
        "cap:sensor": "Sensor protected ONLY within declared toy fault scope",
        **{"rule:" + r.name:
           "Action implementations held reliable ONLY in this toy scope"
           for r in example().rules},
    }
    if common_power_exposed:
        incidence["cap:power"] = frozenset({"event:power"})
    else:
        protected["cap:power"] = "Shared power protected ONLY in narrow toy scope"
    return FaultOntology(
        "ALARM_POWER_EXPOSED" if common_power_exposed else "ALARM_NARROW",
        mechanisms, incidence, protected,
        frozenset(x for es in incidence.values() for x in es))


def audit() -> dict:
    aliases = enumerate_dfs(alias_fixture(), construction=True)
    distinct = alias_scope(physically_distinct=True)
    same = alias_scope(physically_distinct=False)
    single = assess(aliases, "goal", same)
    multiple = assess(aliases, "goal", distinct)
    assert single.indicator == 0 and single.min_event_cut == 1
    assert multiple.indicator == 1 and multiple.min_event_cut == 2
    scope = alarm_scope(common_power_exposed=False)
    broad = alarm_scope(common_power_exposed=True)
    alarm = enumerate_dfs(example(), construction=True)
    narrow = assess(alarm, "alarm", scope)
    expanded = assess(alarm, "alarm", broad)
    assert narrow.indicator == 1 and expanded.indicator == 0
    split = assess(enumerate_dfs(split_source_fixture(), construction=True),
                   "goal", split_source_scope())
    assert split.indicator == 0
    vulnerable = exact_static_survival_probability(
        aliases, "goal", same, {"event:failure_a": Fraction(1, 2)})
    separate = exact_static_survival_probability(
        aliases, "goal", distinct, {"event:failure_a": Fraction(1, 2),
                                    "event:failure_b": Fraction(1, 2)})
    assert vulnerable == Fraction(1, 2) and separate == Fraction(3, 4)
    return {
        "gate": "R1", "classification": "declared_ontology_negative_controls_not_H1",
        "same_physical_pair": single.indicator,
        "same_min_event_cut": single.min_event_cut,
        "independent_physical_pair": multiple.indicator,
        "independent_min_event_cut": multiple.min_event_cut,
        "alarm_narrow_pair": narrow.indicator,
        "alarm_with_common_power_pair": expanded.indicator,
        "split_source_single_unit_pair": split.indicator,
        "one_event_static_survival": str(vulnerable),
        "two_independent_events_static_survival": str(separate),
        "result": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
