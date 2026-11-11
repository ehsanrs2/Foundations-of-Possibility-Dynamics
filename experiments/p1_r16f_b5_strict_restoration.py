"""B5: same-history strict restoration with observation lag and censoring.

PROVISIONAL SYNTHETIC CONFORMANCE ONLY. Uses B4's declared hidden-fault
World and G2 unit-tick model. A SINGLE fixed goal-reactive policy sees a
lagged public capability/stock snapshot; the scenario identity, true loss
flag, future fault time and true post-lag state are NOT policy inputs.

A separate privileged simulator/evaluator records actual before/after
loss and first same-goal reacquisition. Incomplete follow-up is CENSORED,
never a negative outcome. No H1 samples or sealed families are inspected.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from typing import Mapping
import json

from experiments.p1_gate2 import Action, Fault, Model
from experiments.p1_r16e_b4_hidden_fault_policy import (
    Scenario, World, _validate, _fault_state, _command_step,
    _projection, _snapshot,
)

PROFILE = "B5_SAME_HISTORY_LOSS_LAG_CENSOR_V1"
RESTORED = "RESTORED"
NOT_RESTORED = "NOT_RESTORED"
NOT_AT_RISK = "NOT_AT_RISK"
CENSORED = "CENSORED"


@dataclass(frozen=True)
class Outcome:
    """Privileged ground truth; NOT exposed to the acting controller."""
    scenario: str
    probability: Fraction
    fault_tick: int
    held_before_fault: bool
    lost_at_fault: bool
    first_regained_tick: int | None
    held_at_deadline: bool
    followup_until: int
    status: str
    commands: tuple[str, ...]
    delivered_goal_signals: tuple[bool, ...]


def _inputs(world: World, goal: str, lag: int, followup_until: int,
            visible: Mapping[str, str] | None) -> tuple[dict[str, str], str]:
    _validate(world)
    if goal not in world.base.goals or len(world.base.goals) != 1:
        raise ValueError("B5 requires one explicitly registered goal")
    if type(lag) is not int or not 0 <= lag <= 2:
        raise ValueError("B5 observation lag must be exactly 0, 1 or 2 ticks")
    if type(followup_until) is not int or not 0 <= followup_until <= world.base.horizon:
        raise ValueError("follow-up cutoff must be an inclusive integer tick <= horizon")
    if len(world.base.actions) != 1:
        raise ValueError("B5 fixed-policy profile permits exactly one repair action")
    a = world.base.actions[0]
    if a.name != "repair" or a.produces != goal or a.generative:
        raise ValueError("B5 requires a non-generative 'repair' that produces the same goal")
    mapping = _projection(world.base, visible)
    return mapping, mapping[goal]


def _label(lost: bool, first_regained_tick: int | None,
           followup_until: int, horizon: int) -> str:
    if not lost:
        return NOT_AT_RISK
    if first_regained_tick is not None and first_regained_tick <= followup_until:
        return RESTORED
    if followup_until < horizon:
        return CENSORED
    return NOT_RESTORED


def execute(world: World, scenario: Scenario, *, goal: str = "service",
            lag: int = 0, followup_until: int | None = None,
            visible: Mapping[str, str] | None = None) -> Outcome:
    """Canonical B4 transitions; outcome is actual loss then SAME-history recovery.

    Pre-command public snapshots are recorded at each tick; policy sees the
    most recent sample available with the DECLARED lag. The observation does
    NOT disclose hidden event times or the privileged loss flag.
    """
    horizon = world.base.horizon
    until = horizon if followup_until is None else followup_until
    observation, canonical_goal = _inputs(world, goal, lag, until, visible)
    if scenario not in world.scenarios:
        raise ValueError("scenario is not in the registered world")
    held, stock, disabled = world.base.initial, world.base.stock, frozenset()
    pre_samples = []
    words: list[str] = []
    signals: list[bool] = []
    prior = lost = False
    first: int | None = None
    actions = {"repair": world.base.actions[0]}
    for t in range(horizon):
        if t == scenario.fault.tick:
            prior = goal in held
            held, stock, disabled = _fault_state(
                held, stock, disabled, scenario.fault)
            lost = prior and goal not in held
        pre_samples.append(_snapshot(held, stock, observation))
        delayed = pre_samples[max(0, t - lag)]
        seen_goal = canonical_goal in delayed[0]
        signals.append(seen_goal)
        cmd = "WAIT" if seen_goal else "repair"
        _accepted, held, stock = _command_step(
            held, stock, disabled, cmd, actions, False)
        words.append(cmd)
        # An action chosen after a fault at t completes at tick t+1.
        if lost and first is None and t >= scenario.fault.tick and goal in held:
            first = t + 1
    return Outcome(scenario.name, scenario.probability, scenario.fault.tick,
                   prior, lost, first, goal in held, until,
                   _label(lost, first, until, horizon),
                   tuple(words), tuple(signals))


def independent_history_oracle(
        world: World, scenario: Scenario, *, goal: str = "service",
        lag: int = 0, followup_until: int | None = None,
        visible: Mapping[str, str] | None = None) -> Outcome:
    """Independent mutable-set/dictionary replay; no B4 transition calls.

    Deliberately duplicates the unit-tick semantics rather than invoking
    execute(), _fault_state() or _command_step(). It shares only the
    validated observer/goal specification.
    """
    horizon = world.base.horizon
    until = horizon if followup_until is None else followup_until
    mapping, canonical_goal = _inputs(world, goal, lag, until, visible)
    if scenario not in world.scenarios:
        raise ValueError("unregistered scenario")
    caps = set(world.base.initial)
    inventory = dict(zip(world.base.resources, world.base.stock))
    banned: set[str] = set()
    samples: list[tuple[tuple[str, ...], tuple[int, ...]]] = []
    commands: list[str] = []
    delivered: list[bool] = []
    before = was_lost = False
    restored_at = None
    rule = world.base.actions[0]
    for tick in range(horizon):
        if tick == scenario.fault.tick:
            before = goal in caps
            caps.difference_update(scenario.fault.remove)
            for idx, key in enumerate(world.base.resources):
                inventory[key] = max(0, inventory[key] - scenario.fault.destroy[idx])
            banned.update(scenario.fault.disable)
            was_lost = before and goal not in caps
        frame = (
            tuple(sorted(v for k, v in mapping.items() if k in caps)),
            tuple(inventory[k] for k in world.base.resources))
        samples.append(frame)
        signal = canonical_goal in samples[max(0, tick - lag)][0]
        delivered.append(signal)
        chosen = "WAIT" if signal else "repair"
        commands.append(chosen)
        if chosen == "repair" and rule.name not in banned:
            if rule.requires <= caps and all(
                inventory[key] >= use for key, use in
                zip(world.base.resources, rule.consumes)
            ):
                caps.add(rule.produces)
                for i, key in enumerate(world.base.resources):
                    inventory[key] -= rule.consumes[i]
                    inventory[key] += rule.yields[i]
        if was_lost and restored_at is None and tick >= scenario.fault.tick:
            if goal in caps:
                restored_at = tick + 1
    return Outcome(scenario.name, scenario.probability, scenario.fault.tick,
                   before, was_lost, restored_at, goal in caps, until,
                   _label(was_lost, restored_at, until, horizon),
                   tuple(commands), tuple(delivered))


def summarize(world: World, *, goal: str = "service", lag: int = 0,
              followup_until: int | None = None,
              visible: Mapping[str, str] | None = None) -> dict:
    """Report EXACT mass by outcome, never recode CENSORED as failure.

    Observed-case fraction is purely descriptive. Excluding censored cases
    can induce informative-censoring bias and is NOT an H1 estimate.
    """
    mass = {k: Fraction() for k in
            (RESTORED, NOT_RESTORED, NOT_AT_RISK, CENSORED)}
    for scenario in world.scenarios:
        primary = execute(world, scenario, goal=goal, lag=lag,
                          followup_until=followup_until, visible=visible)
        oracle = independent_history_oracle(
            world, scenario, goal=goal, lag=lag,
            followup_until=followup_until, visible=visible)
        if primary != oracle:
            raise AssertionError(("B5 independent replay differs", primary, oracle))
        mass[primary.status] += scenario.probability
    if sum(mass.values(), Fraction()) != 1:
        raise AssertionError("scenario probability mass was lost")
    observed_at_risk = mass[RESTORED] + mass[NOT_RESTORED]
    true_loss_risk = observed_at_risk + mass[CENSORED]
    ratio = (mass[RESTORED] / observed_at_risk if observed_at_risk
             else None)
    return {
        "status_mass": {k: str(v) for k, v in mass.items()},
        "true_loss_risk_mass": str(true_loss_risk),
        "observed_eligible_mass": str(observed_at_risk),
        "observed_case_success_fraction": str(ratio) if ratio is not None else None,
        "conditional_inference_validated": False,
        "sampling_uncertainty_assessed": False,
        "H1_confirmatory_result": False,
    }


def fixture() -> World:
    """Exact loss, late loss and unaffected goal, with known synthetic weights."""
    base = Model(
        initial=frozenset({"seed", "service"}),
        goals=frozenset({"service"}),
        resources=("kit",), stock=(1,),
        actions=(Action("repair", frozenset({"seed"}), "service",
                        (0,), (0,)),),
        horizon=3, fault=Fault(0, frozenset(), (0,)))
    return World(base, (
        Scenario("early_loss", Fraction(1, 2),
                 Fault(1, frozenset({"service"}), (0,))),
        Scenario("late_loss", Fraction(1, 4),
                 Fault(2, frozenset({"service"}), (0,))),
        Scenario("unaffected", Fraction(1, 4),
                 Fault(1, frozenset({"absent"}), (0,))),
    ))


def audit() -> dict:
    world = fixture()
    l0, l1, l2 = [summarize(world, lag=t) for t in (0, 1, 2)]
    cut = summarize(world, lag=0, followup_until=2)
    all_censored = summarize(world, lag=1, followup_until=2)
    no_loss = World(world.base, (world.scenarios[2].__class__(
        "unaffected_only", Fraction(1), world.scenarios[2].fault),))
    empty = summarize(no_loss)
    early = world.scenarios[0]
    delayed = execute(world, early, lag=1)
    withheld = execute(world, early, lag=0, followup_until=2)
    if not (
        l0["status_mass"] == {
            RESTORED:"3/4", NOT_RESTORED:"0", NOT_AT_RISK:"1/4", CENSORED:"0"}
        and l1["status_mass"] == {
            RESTORED:"1/2", NOT_RESTORED:"1/4", NOT_AT_RISK:"1/4", CENSORED:"0"}
        and l2["status_mass"][NOT_RESTORED] == "3/4"
        and l0["observed_case_success_fraction"] == "1"
        and l1["observed_case_success_fraction"] == "2/3"
        and cut["status_mass"][CENSORED] == "1/4"
        and cut["observed_case_success_fraction"] == "1"
        and all_censored["observed_case_success_fraction"] is None
        and empty["observed_case_success_fraction"] is None
        and delayed.first_regained_tick == 3
        and withheld.first_regained_tick == 2
        and withheld.status == RESTORED
        and all(execute(world, sc).status == NOT_AT_RISK
                for sc in world.scenarios if sc.name == "unaffected")
    ):
        raise AssertionError("B5 strict-loss, lag or censor safeguards changed")
    return {
        "gate": "B5",
        "profile": PROFILE,
        "result": "PASS_PROVISIONAL_SYNTHETIC_STRICT_RESTORATION_CONFORMANCE",
        "scenario_masses_lag0": l0["status_mass"],
        "scenario_masses_lag1": l1["status_mass"],
        "censored_mass_cutoff2_lag0": cut["status_mass"][CENSORED],
        "zero_observed_eligible_returns_null": (
            all_censored["observed_case_success_fraction"] is None),
        "no_real_loss_returns_not_at_risk": True,
        "two_implementations_equal_for_all_cases_and_lags": True,
        "policy_sees_fault_identity": False,
        "terminal_presence_is_not_restoration": True,
        "censored_as_failure": False,
        "real_physical_source_authenticated": False,
        "confirmatory_H1_samples": 0,
        "sealed_family_calls": 0,
        "H1_preregistered": False,
        "classification": "BOUNDED_SYNTHETIC_RESTORATION_SOFTWARE_NOT_H1",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True, indent=2))
