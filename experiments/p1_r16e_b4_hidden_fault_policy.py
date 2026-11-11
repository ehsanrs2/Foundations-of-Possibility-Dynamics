"""B4: finite hidden-fault observation-based policy gate. SYNTHETIC ONLY.

All scenario names / realized fault times remain hidden from the controller.
A fault is applied before the command at its own unknown tick. Only a
declared projection of capabilities, stock, command acceptance and outcomes
is observable. The tester uses the G2/B3 one-tick construction grammar.

Equality of all finite OPEN-LOOP command-response laws implies equality of
the observable-history law for each common history-reactive controller on
this finite exogenous model. This does NOT establish physical identity,
nontrivial novelty, infinite-horizon stochastic bisimulation or H1.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from collections import defaultdict
from functools import lru_cache
from fractions import Fraction
from itertools import product
from typing import Mapping
import json

from experiments.p1_gate2 import Model, Action, Fault
from experiments.p1_r16d_b3_policy_response import (
    WAIT, _profile, _commands, _projection, _snapshot, compare as b3_compare,
)

PROFILE = "B4_HIDDEN_FAULT_OBSERVABLE_POLICY_V1"
MAX_SCENARIOS = 3
MAX_WORDS = 625
Snapshot = tuple[tuple[str, ...], tuple[int, ...]]
Reply = tuple[Snapshot, bool, Snapshot]  # pre-command, accepted, post-command
Response = tuple[Snapshot, tuple[Reply, ...]]
Word = tuple[str, ...]
Branch = tuple[int, frozenset[str], tuple[int, ...], frozenset[str], Fraction]


@dataclass(frozen=True)
class Scenario:
    name: str
    probability: Fraction
    fault: Fault


@dataclass(frozen=True)
class World:
    base: Model
    scenarios: tuple[Scenario, ...]


@dataclass(frozen=True)
class Comparison:
    ordinary_equal: bool
    constructive_equal: bool
    no_fault_b3_ordinary_equal: bool
    no_fault_b3_constructive_equal: bool
    first_ordinary_disagreement: Word | None
    first_constructive_disagreement: Word | None

    def as_dict(self) -> dict:
        return {
            "ordinary_equal": self.ordinary_equal,
            "constructive_equal": self.constructive_equal,
            "no_fault_b3_ordinary_equal": self.no_fault_b3_ordinary_equal,
            "no_fault_b3_constructive_equal": self.no_fault_b3_constructive_equal,
            "first_ordinary_disagreement": (
                list(self.first_ordinary_disagreement)
                if self.first_ordinary_disagreement is not None else None),
            "first_constructive_disagreement": (
                list(self.first_constructive_disagreement)
                if self.first_constructive_disagreement is not None else None),
            "physical_fault_identity_proven": False,
            "general_stochastic_bisimulation_proven": False,
            "H1_confirmatory_result": False,
        }


def _validate(world: World) -> None:
    _profile(world.base)  # G2/B3 one-tick, inert base fault and work ceilings
    if not 2 <= world.base.horizon <= 3:
        raise ValueError("B4 needs at least one possible hidden fault tick")
    if not 1 <= len(world.scenarios) <= MAX_SCENARIOS:
        raise ValueError("B4 permits 1..3 declared scenarios")
    if (len({s.name for s in world.scenarios}) != len(world.scenarios)
            or any(not isinstance(s.name, str) or not s.name
                   or type(s.probability) is not Fraction or s.probability <= 0
                   for s in world.scenarios)
            or sum((s.probability for s in world.scenarios), Fraction()) != 1):
        raise ValueError("scenario names and exact positive law must be valid")
    action_names = {a.name for a in world.base.actions}
    for s in world.scenarios:
        f = s.fault
        if not 1 <= f.tick < world.base.horizon:
            raise ValueError("B4 fault time must be a hidden decision-time tick")
        if (len(f.destroy) != len(world.base.resources)
                or any(x < 0 for x in f.destroy)
                or not f.disable <= action_names):
            raise ValueError("invalid scenario effect vector or action identity")


def _fault_state(held: frozenset[str], stock: tuple[int, ...],
                 disabled: frozenset[str], fault: Fault
                 ) -> tuple[frozenset[str], tuple[int, ...], frozenset[str]]:
    return (held - fault.remove,
            tuple(max(0, x - y) for x, y in zip(stock, fault.destroy)),
            disabled | fault.disable)


def _command_step(held: frozenset[str], stock: tuple[int, ...],
                  disabled: frozenset[str], command: str,
                  actions: Mapping[str, Action], construction: bool
                  ) -> tuple[bool, frozenset[str], tuple[int, ...]]:
    if command == WAIT:
        return True, held, stock
    if command not in actions:
        raise ValueError("unknown canonical tester command")
    a = actions[command]
    if (a.name in disabled or (a.generative and not construction)
            or not a.requires <= held
            or any(x < y for x, y in zip(stock, a.consumes))):
        return False, held, stock
    return (True, held | {a.produces},
            tuple(x - y + z for x, y, z in
                  zip(stock, a.consumes, a.yields)))


def _run_one(world: World, scenario: Scenario, word: Word,
             visible: Mapping[str, str], actions: Mapping[str, Action],
             construction: bool) -> tuple[Response, frozenset[str]]:
    if len(word) > world.base.horizon:
        raise ValueError("command prefix exceeds B4 horizon")
    held, stock = world.base.initial, world.base.stock
    disabled = frozenset()
    initial = _snapshot(held, stock, visible)
    replies: list[Reply] = []
    for tick, cmd in enumerate(word):
        if tick == scenario.fault.tick:
            held, stock, disabled = _fault_state(
                held, stock, disabled, scenario.fault)
        pre = _snapshot(held, stock, visible)
        accepted, held, stock = _command_step(
            held, stock, disabled, cmd, actions, construction)
        replies.append((pre, accepted, _snapshot(held, stock, visible)))
    return (initial, tuple(replies)), held


def response_law(world: World, *, construction: bool,
                 visible_aliases: Mapping[str, str] | None = None,
                 action_aliases: Mapping[str, str] | None = None
                 ) -> dict[Word, dict[Response, Fraction]]:
    """Exact scenario-marginal observed histories for EVERY fixed command word.

    Neither scenario name nor fault occurrence is inserted into responses.
    A null-effect fault therefore provides no artificial notification.
    """
    _validate(world)
    visible = _projection(world.base, visible_aliases)
    actions = _commands(world.base, action_aliases)
    alphabet = tuple(sorted((*actions, WAIT)))
    if len(alphabet) ** world.base.horizon > MAX_WORDS:
        raise ValueError("B4 exact enumeration cap exceeded")
    result = {}
    for word in product(alphabet, repeat=world.base.horizon):
        distribution: dict[Response, Fraction] = defaultdict(Fraction)
        for sc in world.scenarios:
            response, _ = _run_one(
                world, sc, word, visible, actions, construction)
            distribution[response] += sc.probability
        if sum(distribution.values(), Fraction()) != 1:
            raise AssertionError("scenario mass lost")
        result[word] = dict(distribution)
    return result


def compare_worlds(left: World, right: World, *,
                   left_visible: Mapping[str, str] | None = None,
                   right_visible: Mapping[str, str] | None = None,
                   left_actions: Mapping[str, str] | None = None,
                   right_actions: Mapping[str, str] | None = None
                   ) -> Comparison:
    _validate(left)
    _validate(right)
    if (left.base.horizon != right.base.horizon
            or left.base.resources != right.base.resources
            or left.base.stock != right.base.stock):
        raise ValueError("same horizon, resource axes and initial stock required")
    # Both experiments face EXACTLY the same stipulated exogenous event law.
    # A scenario may have a DIFFERENT physical effect map in the two models.
    external = lambda w: sorted(
        (s.name, s.probability, s.fault.tick) for s in w.scenarios)
    if external(left) != external(right):
        raise ValueError("scenario identity, timing and prior law differ")
    lv, rv = _projection(left.base, left_visible), _projection(right.base, right_visible)
    if (set(lv.values()) != set(rv.values())
            or {lv[g] for g in left.base.goals}
               != {rv[g] for g in right.base.goals}):
        raise ValueError("canonical observer and goal vocabulary differ")
    la, ra = _commands(left.base, left_actions), _commands(right.base, right_actions)
    if set(la) != set(ra):
        raise ValueError("canonical command alphabets differ")
    b3 = b3_compare(
        left.base, right.base, left_visible=lv, right_visible=rv,
        left_actions=left_actions, right_actions=right_actions)
    outcomes = []
    for enabled in (False, True):
        l = response_law(
            left, construction=enabled, visible_aliases=lv,
            action_aliases=left_actions)
        r = response_law(
            right, construction=enabled, visible_aliases=rv,
            action_aliases=right_actions)
        mismatch = next((word for word in sorted(l) if l[word] != r[word]), None)
        outcomes.append((mismatch is None, mismatch))
    return Comparison(outcomes[0][0], outcomes[1][0],
                      b3.ordinary_equal, b3.constructive_equal,
                      outcomes[0][1], outcomes[1][1])


def _prepared(held: frozenset[str], stock: tuple[int, ...],
              disabled: frozenset[str], sc: Scenario, tick: int
              ) -> tuple[frozenset[str], tuple[int, ...], frozenset[str]]:
    if tick == sc.fault.tick:
        return _fault_state(held, stock, disabled, sc.fault)
    return held, stock, disabled


def belief_dp_value(world: World, goal: str, *,
                    construction: bool = False,
                    visible_aliases: Mapping[str, str] | None = None,
                    action_aliases: Mapping[str, str] | None = None) -> Fraction:
    """Conventional finite belief-state DP for optimal OBSERVATION-based policy.

    Branch probabilities are unnormalized joint masses. Before each command
    the controller can distinguish only the declared pre-action observation;
    after the command it receives acceptance and visible state. It never
    conditions its chosen action on scenario identity or future fault time.
    """
    _validate(world)
    if goal not in world.base.goals:
        raise ValueError("target must be in prespecified goal vocabulary")
    visible = _projection(world.base, visible_aliases)
    actions = _commands(world.base, action_aliases)
    commands = tuple(sorted((*actions, WAIT)))
    base = world.base
    start: tuple[Branch, ...] = tuple(
        (i, base.initial, base.stock, frozenset(), sc.probability)
        for i, sc in enumerate(world.scenarios))

    @lru_cache(maxsize=None)
    def solve(tick: int, group: tuple[Branch, ...]) -> Fraction:
        if tick == base.horizon:
            return sum((weight for _, held, _, _, weight in group if goal in held),
                       Fraction())
        pre_groups: dict[Snapshot, list[Branch]] = defaultdict(list)
        for i, held, stock, disabled, weight in group:
            held, stock, disabled = _prepared(
                held, stock, disabled, world.scenarios[i], tick)
            pre_groups[_snapshot(held, stock, visible)].append(
                (i, held, stock, disabled, weight))
        total = Fraction()
        for subset in pre_groups.values():
            candidate_values = []
            for command in commands:
                post_groups: dict[tuple[bool, Snapshot], list[Branch]] = defaultdict(list)
                for i, held, stock, disabled, weight in subset:
                    accepted, next_held, next_stock = _command_step(
                        held, stock, disabled, command, actions, construction)
                    marker = (accepted, _snapshot(next_held, next_stock, visible))
                    post_groups[marker].append(
                        (i, next_held, next_stock, disabled, weight))
                candidate_values.append(sum(
                    (solve(tick + 1, tuple(choices))
                     for choices in post_groups.values()), Fraction()))
            total += max(candidate_values)
        return total

    return solve(0, start)


def history_oracle_value(world: World, goal: str, *,
                         construction: bool = False,
                         visible_aliases: Mapping[str, str] | None = None,
                         action_aliases: Mapping[str, str] | None = None) -> Fraction:
    """Independent explicit scenario-history replay and policy-tree search.

    Each branch stores (scenario index, its own chosen command prefix).
    At every leaf, histories are replayed from tick 0 without DP state
    sharing. No pre-shock decisions inspect future scenario identity.
    """
    _validate(world)
    if goal not in world.base.goals:
        raise ValueError("unregistered target")
    visible = _projection(world.base, visible_aliases)
    actions = _commands(world.base, action_aliases)
    commands = tuple(sorted((*actions, WAIT)))
    horizon = world.base.horizon

    def search(tick: int, histories: tuple[tuple[int, Word], ...]) -> Fraction:
        if tick == horizon:
            return sum(
                (world.scenarios[i].probability for i, word in histories
                 if goal in _run_one(
                     world, world.scenarios[i], word, visible, actions,
                     construction)[1]), Fraction())
        groups: dict[Snapshot, list[tuple[int, Word]]] = defaultdict(list)
        for i, word in histories:
            if len(word) != tick:
                raise AssertionError("oracle chronology mismatch")
            # Reconstruct state *before* current fault, independently using
            # a plain per-scenario history. No hidden event is an observation.
            held = set(world.base.initial)
            inventory = dict(zip(world.base.resources, world.base.stock))
            banned: set[str] = set()
            sc = world.scenarios[i]
            for past_tick, past_cmd in enumerate(word):
                if past_tick == sc.fault.tick:
                    held.difference_update(sc.fault.remove)
                    for k, key in enumerate(world.base.resources):
                        inventory[key] = max(0, inventory[key] - sc.fault.destroy[k])
                    banned.update(sc.fault.disable)
                if past_cmd != WAIT:
                    a = actions[past_cmd]
                    if (past_cmd not in banned and
                            (construction or not a.generative) and
                            a.requires <= held and
                            all(inventory[key] >= need for key, need in
                                zip(world.base.resources, a.consumes))):
                        held.add(a.produces)
                        for k, key in enumerate(world.base.resources):
                            inventory[key] += a.yields[k] - a.consumes[k]
            if tick == sc.fault.tick:
                held.difference_update(sc.fault.remove)
                for k, key in enumerate(world.base.resources):
                    inventory[key] = max(0, inventory[key] - sc.fault.destroy[k])
            pre = (tuple(sorted(label for key, label in visible.items()
                                if key in held)),
                   tuple(inventory[key] for key in world.base.resources))
            groups[pre].append((i, word))
        total = Fraction()
        for subset in groups.values():
            best = Fraction(-1)
            for cmd in commands:
                replies: dict[Reply, list[tuple[int, Word]]] = defaultdict(list)
                for i, old in subset:
                    extended = old + (cmd,)
                    response, _ = _run_one(
                        world, world.scenarios[i], extended,
                        visible, actions, construction)
                    replies[response[1][-1]].append((i, extended))
                value = sum((search(tick + 1, tuple(items))
                             for items in replies.values()), Fraction())
                if value > best:
                    best = value
            total += best
        return total

    return search(0, tuple((i, ()) for i in range(len(world.scenarios))))


def hidden_repair_fixture(*, reveal_sensors: bool = False) -> World:
    """Two equiprobable failures: only one of two repair actions survives.

    The service is active initially and genuinely lost at the hidden t=1
    event. With only the service goal visible, this one-tick-repair model
    permits optimal restoration probability 1/2, not clairvoyant 1.
    """
    initially = {"seed", "service"}
    if reveal_sensors:
        initially.update({"sensor_a", "sensor_b"})
    base = Model(
        initial=frozenset(initially), goals=frozenset({"service"}),
        resources=("kit",), stock=(1,),
        actions=(
            Action("a", frozenset({"seed"}), "service", (0,), (0,)),
            Action("b", frozenset({"seed"}), "service", (0,), (0,)),
        ),
        horizon=2, fault=Fault(0, frozenset(), (0,)))
    cases = (
        Scenario("fault_a", Fraction(1, 2),
                 Fault(1, frozenset({"service", "sensor_a"}
                                   if reveal_sensors else {"service"}),
                       (0,), frozenset({"a"}))),
        Scenario("fault_b", Fraction(1, 2),
                 Fault(1, frozenset({"service", "sensor_b"}
                                   if reveal_sensors else {"service"}),
                       (0,), frozenset({"b"}))),
    )
    return World(base, cases)


def unknown_time_fixture() -> World:
    """Fault time 1 vs 2 is not announced; it may change observable state."""
    base = Model(
        initial=frozenset({"seed", "service"}),
        goals=frozenset({"service"}), resources=("kit",), stock=(1,),
        actions=(Action("repair", frozenset({"seed"}), "service",
                        (0,), (0,)),),
        horizon=3, fault=Fault(0, frozenset(), (0,)))
    return World(base, (
        Scenario("early", Fraction(1, 2),
                 Fault(1, frozenset({"service"}), (0,))),
        Scenario("late", Fraction(1, 2),
                 Fault(2, frozenset({"service"}), (0,))),
    ))


def audit() -> dict:
    hidden = hidden_repair_fixture()
    protected = World(hidden.base, tuple(
        replace(s, fault=replace(s.fault, disable=frozenset()))
        for s in hidden.scenarios))
    comparison = compare_worlds(hidden, protected)
    hidden_dp = belief_dp_value(hidden, "service")
    hidden_oracle = history_oracle_value(hidden, "service")
    revealed = hidden_repair_fixture(reveal_sensors=True)
    visible_map = {"service": "service", "sensor_a": "sa", "sensor_b": "sb"}
    visible_dp = belief_dp_value(revealed, "service",
                                visible_aliases=visible_map)
    visible_oracle = history_oracle_value(revealed, "service",
                                         visible_aliases=visible_map)
    timed = unknown_time_fixture()
    timed_dp = belief_dp_value(timed, "service")
    timed_oracle = history_oracle_value(timed, "service")
    # A no-effect event is not an observed "fault happened" message.
    silent = World(timed.base, tuple(
        replace(s, fault=replace(s.fault, remove=frozenset({"absent"})))
        for s in timed.scenarios))
    inert = World(timed.base, tuple(
        replace(s, fault=replace(s.fault, remove=frozenset()))
        for s in timed.scenarios))
    silent_eq = compare_worlds(silent, inert)
    if not (
        comparison.no_fault_b3_ordinary_equal
        and comparison.no_fault_b3_constructive_equal
        and not comparison.ordinary_equal
        and not comparison.constructive_equal
        and hidden_dp == hidden_oracle == Fraction(1, 2)
        and visible_dp == visible_oracle == 1
        and timed_dp == timed_oracle
        and silent_eq.ordinary_equal and silent_eq.constructive_equal
        and all(sum(d.values(), Fraction()) == 1
                for d in response_law(timed, construction=False).values())
    ):
        raise AssertionError("B4 no-lookahead/hidden-fault contracts disagree")
    return {
        "gate": "B4", "profile": PROFILE,
        "result": "PASS_PROVISIONAL_HIDDEN_FAULT_POLICY_CONFORMANCE",
        "known_model_no_fault_b3_equal_but_b4_unequal": True,
        "hidden_fault_optimal_terminal_service": str(hidden_dp),
        "sensor_revealed_optimal_terminal_service": str(visible_dp),
        "unknown_event_time_dp_equals_history_oracle": timed_dp == timed_oracle,
        "silent_null_event_cannot_signal_policy": True,
        "clairvoyant_reference_not_a_fair_policy": "1",
        "outcome": "TERMINAL_SERVICE_PRESENT_NOT_STRICT_H1_RESTORATION",
        "physical_fault_provenance": False,
        "confirmatory_H1_samples": 0,
        "sealed_family_calls": 0,
        "H1_preregistered": False,
        "classification": "SYNTHETIC_BOUNDED_BELIEF_POLICY_SOFTWARE_NOT_H1",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
