"""B3: deterministic, bounded, command-response conformance (NOT H1).

The B2 G2 no-shock semantics are kept. This gate exposes *canonical action
commands* and whether each command is legal under the current state, plus
the resulting observer-projected capability set and resource stock at each
unit tick. An attempted infeasible action emits a diagnostic REJECT and
advances one tick without a state change. This rejection is a TESTER
INTERFACE, not an automatically executed real-world control policy.

Exhaustive command-word equality is sufficient, within this exact
deterministic profile, for identical visible histories under any common
deterministic controller that chooses canonical commands solely from
its previous observable response history. It is NOT a stochastic/fault
policy equivalence, bisimulation, or physical mechanism identity test.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import product
from typing import Mapping
import json

from experiments.p1_gate2 import Action, Model, Fault
from experiments.p1_r16b_semantic_conformance import (
    _require_no_shock_profile, constructive_goal_fixture,
)
from experiments.p1_r16c_bounded_trace_equivalence import (
    _projection, compare_profiles,
)

PROFILE = "B3_DETERMINISTIC_COMMAND_RESPONSE_V1"
MAX_HORIZON = 3
MAX_ACTIONS = 4
MAX_COMMAND_WORDS = 625
WAIT = "WAIT"

# Exact public state at the start/end of each tick.
Snapshot = tuple[tuple[str, ...], tuple[int, ...]]
# (command accepted, public state afterwards); rejected commands leave state.
Reply = tuple[bool, Snapshot]
# Initial observer state plus the sequence of command replies.
Response = tuple[Snapshot, tuple[Reply, ...]]
Word = tuple[str, ...]


@dataclass(frozen=True)
class Comparison:
    ordinary_equal: bool
    constructive_equal: bool
    b2_ordinary_equal: bool
    b2_constructive_equal: bool
    ordinary_command_words: int
    constructive_command_words: int
    first_ordinary_mismatch: Word | None
    first_constructive_mismatch: Word | None

    def as_dict(self) -> dict:
        return {
            "ordinary_equal": self.ordinary_equal,
            "constructive_equal": self.constructive_equal,
            "b2_ordinary_equal": self.b2_ordinary_equal,
            "b2_constructive_equal": self.b2_constructive_equal,
            "ordinary_command_words": self.ordinary_command_words,
            "constructive_command_words": self.constructive_command_words,
            "first_ordinary_mismatch":
                list(self.first_ordinary_mismatch)
                if self.first_ordinary_mismatch is not None else None,
            "first_constructive_mismatch":
                list(self.first_constructive_mismatch)
                if self.first_constructive_mismatch is not None else None,
            "proves_physical_identity": False,
            "proves_stochastic_nonanticipative_equivalence": False,
            "proves_unbounded_bisimulation": False,
        }


def _profile(model: Model) -> None:
    _require_no_shock_profile(model)
    if model.horizon > MAX_HORIZON or len(model.actions) > MAX_ACTIONS:
        raise ValueError("B3 exact command-word profile exceeds its fixed limits")
    if len(model.goals) > 3:
        raise ValueError("B3 fixed goal-vocabulary limit exceeded")


def _commands(model: Model, names: Mapping[str, str] | None) -> dict[str, Action]:
    """Map one-to-one canonical commands to existing *syntactic* action IDs.

    No physical component identity is inferred from this mapping.
    """
    original = {a.name: a for a in model.actions}
    if not all(original) or WAIT in original or len(original) != len(model.actions):
        raise ValueError("action IDs must be unique, nonempty and reserve WAIT")
    mapping = ({name: name for name in original} if names is None
               else dict(names))
    if set(mapping) != set(original):
        raise ValueError("all action identifiers require explicit canonical mapping")
    if any(not isinstance(n, str) or not n or n == WAIT
           for n in mapping.values()) or len(set(mapping.values())) != len(mapping):
        raise ValueError("canonical action names must be nonempty and injective")
    return {mapping[name]: action for name, action in original.items()}


def _snapshot(held: frozenset[str], stock: tuple[int, ...],
              projection: Mapping[str, str]) -> Snapshot:
    return (tuple(sorted(label for capability, label in projection.items()
                         if capability in held)), stock)


def _advance(
    held: frozenset[str], stock: tuple[int, ...],
    command: str, actions: Mapping[str, Action], *,
    construction: bool,
) -> tuple[bool, frozenset[str], tuple[int, ...]]:
    """G2 legal unit-tick action, plus explicit diagnostic rejection."""
    if command == WAIT:
        return True, held, stock
    if command not in actions:
        raise ValueError("command not in declared canonical action alphabet")
    a = actions[command]
    if ((a.generative and not construction) or
        not a.requires <= held or
        any(x < y for x, y in zip(stock, a.consumes))):
        return False, held, stock
    return (True, held | {a.produces},
            tuple(x - y + z for x, y, z in
                  zip(stock, a.consumes, a.yields)))


def _response(
    model: Model, word: Word, actions: Mapping[str, Action],
    visible: Mapping[str, str], *, construction: bool,
) -> Response:
    if len(word) != model.horizon:
        raise ValueError("command word must have exactly H ticks")
    held, stock = model.initial, model.stock
    initial = _snapshot(held, stock, visible)
    replies: list[Reply] = []
    for command in word:
        accepted, held, stock = _advance(
            held, stock, command, actions, construction=construction)
        replies.append((accepted, _snapshot(held, stock, visible)))
    return initial, tuple(replies)


def response_language(
    model: Model, *, construction: bool,
    visible_aliases: Mapping[str, str] | None = None,
    action_aliases: Mapping[str, str] | None = None,
) -> dict[Word, Response]:
    """A deterministic response for EVERY possible bounded command word."""
    _profile(model)
    visible = _projection(model, visible_aliases)
    actions = _commands(model, action_aliases)
    alphabet = tuple(sorted((*actions, WAIT)))
    count = len(alphabet) ** model.horizon
    if count > MAX_COMMAND_WORDS:
        raise ValueError("B3 command-word enumeration budget exceeded")
    return {word: _response(model, word, actions, visible,
                            construction=construction)
            for word in product(alphabet, repeat=model.horizon)}


def compare(
    left: Model, right: Model, *,
    left_visible: Mapping[str, str] | None = None,
    right_visible: Mapping[str, str] | None = None,
    left_actions: Mapping[str, str] | None = None,
    right_actions: Mapping[str, str] | None = None,
) -> Comparison:
    _profile(left)
    _profile(right)
    if (left.horizon != right.horizon or
        left.resources != right.resources or left.stock != right.stock):
        raise ValueError("horizon, ordered resource axes and initial stock must match")
    lvis, rvis = _projection(left, left_visible), _projection(right, right_visible)
    if (set(lvis.values()) != set(rvis.values()) or
        {lvis[g] for g in left.goals} != {rvis[g] for g in right.goals}):
        raise ValueError("observable and goal vocabularies must have the same labels")
    la, ra = _commands(left, left_actions), _commands(right, right_actions)
    if set(la) != set(ra):
        raise ValueError("common mapped command alphabet required")

    # B2's existential comparison is deliberately weaker than B3's I/O test.
    b2 = compare_profiles(
        left, right, left_visible=lvis, right_visible=rvis)
    def compare_one(enabled: bool) -> tuple[bool, int, Word | None]:
        left_output = response_language(
            left, construction=enabled, visible_aliases=lvis,
            action_aliases=left_actions)
        right_output = response_language(
            right, construction=enabled, visible_aliases=rvis,
            action_aliases=right_actions)
        first = next((word for word in sorted(left_output)
                      if left_output[word] != right_output[word]), None)
        return first is None, len(left_output), first

    ordinary_eq, ordinary_n, ordinary_first = compare_one(False)
    expanded_eq, expanded_n, expanded_first = compare_one(True)
    if ordinary_n != expanded_n:
        raise AssertionError("command alphabet changed between E0 and E+")
    if ((ordinary_eq and not b2.ordinary_equal) or
        (expanded_eq and not b2.constructive_equal)):
        raise AssertionError("B3 command-response equality cannot contradict B2")
    return Comparison(
        ordinary_eq, expanded_eq,
        b2.ordinary_equal, b2.constructive_equal,
        ordinary_n, expanded_n, ordinary_first, expanded_first,
    )


@dataclass(frozen=True)
class ReactivePolicy:
    """A small nonanticipative controller, parameterized only by public IDs."""
    probe: str
    fallback: str
    goal: str

    def choose(self, visible_history: tuple[Snapshot, ...]) -> str:
        if not visible_history:
            raise ValueError("policy needs observed history")
        if self.goal in visible_history[-1][0]:
            return WAIT
        # No latent model state, future fault or incident ID is supplied.
        return self.probe if len(visible_history) == 1 else self.fallback


def execute_reactive(
    model: Model, policy: ReactivePolicy, *,
    construction: bool,
    visible_aliases: Mapping[str, str] | None = None,
    action_aliases: Mapping[str, str] | None = None,
) -> tuple[Word, Response]:
    """One actual history for a fixed observation-reactive controller."""
    _profile(model)
    visible = _projection(model, visible_aliases)
    actions = _commands(model, action_aliases)
    if policy.probe not in actions or policy.fallback not in actions:
        raise ValueError("policy commands must exist in canonical alphabet")
    if policy.goal not in {visible[g] for g in model.goals}:
        raise ValueError("policy target must be a declared canonical goal")
    held, stock = model.initial, model.stock
    initial = _snapshot(held, stock, visible)
    observations = [initial]
    replies: list[Reply] = []
    words: list[str] = []
    for _ in range(model.horizon):
        cmd = policy.choose(tuple(observations))
        accepted, held, stock = _advance(
            held, stock, cmd, actions, construction=construction)
        observed = _snapshot(held, stock, visible)
        observations.append(observed)
        words.append(cmd)
        replies.append((accepted, observed))
    return tuple(words), (initial, tuple(replies))


def _ambiguous_routes_fixture() -> tuple[Model, Model]:
    """Two systems with identical B2 trace languages but different commands."""
    base = Model(
        initial=frozenset({"seed"}), goals=frozenset({"service"}),
        resources=("kit",), stock=(1,),
        actions=(
            Action("primary", frozenset({"seed"}), "service", (0,), (0,)),
            Action("probe", frozenset({"seed"}), "service", (0,), (0,)),
        ),
        horizon=2, fault=Fault(0, frozenset(), (0,)),
    )
    altered = replace(base, actions=(
        base.actions[0],
        replace(base.actions[1], produces="seed"),
    ))
    return base, altered


def _stock_alias_fixture() -> tuple[Model, Model]:
    base, _ = _ambiguous_routes_fixture()
    left = replace(base, actions=(
        replace(base.actions[0], consumes=(1,)),
        base.actions[1],
    ))
    right = replace(base, actions=(
        base.actions[0],
        replace(base.actions[1], consumes=(1,)),
    ))
    return left, right


def audit() -> dict:
    left, right = _ambiguous_routes_fixture()
    reflexive = compare(left, left)
    different = compare(left, right)
    stock_left, stock_right = _stock_alias_fixture()
    swapped_stock = compare(stock_left, stock_right)
    original = constructive_goal_fixture()
    renamed = replace(
        original,
        initial=frozenset({"root"}), goals=frozenset({"objective"}),
        actions=(
            Action("make", frozenset({"root"}), "relay", (1,), (0,), True),
            Action("deliver", frozenset({"relay"}), "objective", (0,), (0,)),
        ),
    )
    renamed_equivalent = compare(
        original, renamed,
        left_visible={"service": "goal"},
        right_visible={"objective": "goal"},
        left_actions={"build_bridge": "build", "provide": "serve"},
        right_actions={"make": "build", "deliver": "serve"},
    )
    policy = ReactivePolicy("probe", "primary", "service")
    run_left = execute_reactive(left, policy, construction=False)
    run_right = execute_reactive(right, policy, construction=False)
    if not (
        reflexive.ordinary_equal and reflexive.constructive_equal
        and different.b2_ordinary_equal and different.b2_constructive_equal
        and not different.ordinary_equal and not different.constructive_equal
        and swapped_stock.b2_ordinary_equal
        and swapped_stock.b2_constructive_equal
        and not swapped_stock.ordinary_equal
        and not swapped_stock.constructive_equal
        and renamed_equivalent.ordinary_equal
        and renamed_equivalent.constructive_equal
        and run_left != run_right
        and run_left[0] == ("probe", WAIT)
        and run_right[0] == ("probe", "primary")
        and not different.as_dict()["proves_stochastic_nonanticipative_equivalence"]
    ):
        raise AssertionError("B3 action/observation counterexample changed")
    return {
        "gate": "B3",
        "profile": PROFILE,
        "result": "PASS_PROVISIONAL_COMMAND_RESPONSE_CONFORMANCE",
        "synthetic_fixture_comparisons": 5,
        "b2_equal_but_b3_unequal_actions": True,
        "b2_equal_but_b3_unequal_stock_assignment": True,
        "mapped_action_and_goal_renaming_preserves_B3": True,
        "same_nonanticipative_reactive_policy_diverges": True,
        "stochastic_fault_equivalence_claimed": False,
        "physical_mechanism_identity_claimed": False,
        "confirmatory_H1_samples": 0,
        "sealed_family_calls": 0,
        "H1_preregistered": False,
        "classification": "BOUNDED_SYNTHETIC_IO_CONFORMANCE_NOT_H1",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
