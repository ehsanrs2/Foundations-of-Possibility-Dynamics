"""R7: silent null-effect boundary and observation-filtered fixed policy.

This is a NEW opt-in developer evaluator. Historical G2-G4/R3-R6 code and
their archived results remain unchanged and reproducible.

One exogenous fault vector may be applied at the hidden tick, but the policy
observes only actual changes in its fully observable capabilities, integer
inventory, or known disabled operations. It does not receive a clock signal
announcing a fault. An ineffective event is observationally indistinguishable
from no event. This is perfect state sensing, NOT partial/noisy observation.

Strict loss/restoration is separately labelled from the hidden ground-truth
event, never exposed to the policy during action selection. NOT an H1 test.
"""
from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import argparse
import json

from experiments.p1_r3_policy_rollout import (
    Case, Observation, Outcome, Step, Trial, execute,
)
from experiments.p1_r4_development_families import TRAIN, TUNE, SEALED
from experiments.p1_r6_fault_risk_dev import develop_trial


def execute_observable(trial: Trial, case: Case) -> Outcome:
    """Immutable state/stock executor; an unobservable no-op never alerts policy."""
    if case not in trial.cases:
        raise ValueError("scenario not registered in the trial")
    held = trial.base.initial
    stock = trial.base.stock
    disabled = frozenset()
    detected = False
    before = lost = retained = frozenset()
    first: dict[str, int] = {}
    steps: list[Step] = []
    for t in range(trial.base.horizon + 1):
        old_caps, old_stock, old_disabled = held, stock, disabled
        if t == case.fault.tick:
            before = held & trial.base.goals
            held = held - case.fault.remove
            stock = tuple(max(0, amount - loss)
                          for amount, loss in zip(stock, case.fault.destroy))
            disabled = disabled | case.fault.disable
            lost = before - held
            retained = before & held
            detected = detected or (
                held != old_caps or stock != old_stock or disabled != old_disabled
            )
        if t > case.fault.tick:
            for g in sorted(lost & held):
                first.setdefault(g, t)
        visible_caps, visible_stock = held, stock
        action_name: str | None = None
        if t < trial.base.horizon:
            observation = Observation(t, held, stock, disabled, detected)
            action_name = trial.policy.choose(observation, trial.base.actions)
            if action_name != "WAIT":
                action = next(a for a in trial.base.actions
                              if a.name == action_name)
                if (action.name in disabled or
                    (action.generative and not trial.policy.construction) or
                    not action.requires <= held or
                    any(have < need for have, need
                        in zip(stock, action.consumes))):
                    raise AssertionError("policy selected a forbidden or infeasible action")
                held = held | {action.produces}
                stock = tuple(have - need + added for have, need, added
                              in zip(stock, action.consumes, action.yields))
        steps.append(Step(t, old_caps, visible_caps, old_stock,
                          visible_stock, disabled, detected, action_name,
                          held, stock))
    results = tuple((g, int(g in first) if g in lost else None)
                    for g in sorted(trial.base.goals))
    return Outcome(case.name, case.fault.tick, before, lost, retained,
                   tuple(sorted(first.items())), results, tuple(steps))


def independent_observable_oracle(trial: Trial, case: Case) -> Outcome:
    """Separate sequential mutable-set/dict implementation of same observation law.

    Does not invoke execute_observable() or policy.choose(). Its comparison
    checks complete recorded histories, not just final loss/restoration labels.
    """
    if case not in trial.cases:
        raise ValueError("unregistered case")
    caps = set(trial.base.initial)
    inventory = dict(zip(trial.base.resources, trial.base.stock))
    switched_off: set[str] = set()
    sensed = False
    before: set[str] = set()
    removed: set[str] = set()
    surviving: set[str] = set()
    first: dict[str, int] = {}
    log: list[Step] = []
    actions = {a.name: a for a in trial.base.actions}
    for clock in range(trial.base.horizon + 1):
        caps_at_start = frozenset(caps)
        stock_at_start = tuple(inventory[key] for key in trial.base.resources)
        disabled_at_start = frozenset(switched_off)
        if clock == case.fault.tick:
            before = caps & trial.base.goals
            caps.difference_update(case.fault.remove)
            for idx, key in enumerate(trial.base.resources):
                inventory[key] = max(0, inventory[key] - case.fault.destroy[idx])
            switched_off.update(case.fault.disable)
            removed = before - caps
            surviving = before & caps
            if (caps != set(caps_at_start) or
                any(inventory[k] != stock_at_start[idx]
                    for idx, k in enumerate(trial.base.resources)) or
                switched_off != set(disabled_at_start)):
                sensed = True
        if clock > case.fault.tick:
            for goal in sorted(removed):
                if goal in caps and goal not in first:
                    first[goal] = clock
        visible = frozenset(caps)
        visible_stock = tuple(inventory[k] for k in trial.base.resources)
        chosen: str | None = None
        if clock < trial.base.horizon:
            chosen = "WAIT"
            priority = (trial.policy.after_priority if sensed
                        else trial.policy.before_priority)
            for name in priority:
                a = actions[name]
                if name in switched_off:
                    continue
                if a.generative and not trial.policy.construction:
                    continue
                if not a.requires.issubset(caps):
                    continue
                if any(inventory[k] < a.consumes[idx]
                       for idx, k in enumerate(trial.base.resources)):
                    continue
                if a.produces in caps and not any(a.yields):
                    continue
                chosen = name
                for idx, k in enumerate(trial.base.resources):
                    inventory[k] = (inventory[k] - a.consumes[idx]
                                    + a.yields[idx])
                caps.add(a.produces)
                break
        log.append(Step(clock, caps_at_start, visible, stock_at_start,
                        visible_stock, frozenset(switched_off), sensed,
                        chosen, frozenset(caps),
                        tuple(inventory[k] for k in trial.base.resources)))
    labels = tuple((g, int(g in first) if g in removed else None)
                   for g in sorted(trial.base.goals))
    return Outcome(case.name, case.fault.tick, frozenset(before),
                   frozenset(removed), frozenset(surviving),
                   tuple(sorted(first.items())), labels, tuple(log))


def audit(*, seed: int = 20261031, train_n: int = 24,
          tune_n: int = 12) -> dict:
    """R6-matched development-only exact weighted paired observation diagnostic.

    Reports observable-policy vs old explicit-boundary behavior without claiming
    extra predictive information, causal effect or field-observed failure rates.
    """
    if type(seed) is not int or type(train_n) is not int or type(tune_n) is not int:
        raise ValueError("integer inputs required")
    if not 1 <= train_n <= 24 or not 1 <= tune_n <= 12:
        raise ValueError("bounded training/tuning counts required")
    rows: list[dict] = []
    scenario_checks = 0
    silently_applied = 0
    changed_histories = 0
    changed_strict_labels = 0
    for family in TRAIN + TUNE:
        n = train_n if family in TRAIN else tune_n
        for index in range(n):
            trial = develop_trial(seed, family, index)
            weight_silent = Fraction()
            weight_trace_delta = Fraction()
            eligible = restored = Fraction()
            for case in trial.cases:
                r7 = execute_observable(trial, case)
                other = independent_observable_oracle(trial, case)
                if r7 != other:
                    raise AssertionError(("R7 observation-oracle mismatch", family,
                                          index, case.name, r7, other))
                legacy = execute(trial, case)
                t = case.fault.tick
                if not r7.steps[t].event_seen:
                    weight_silent += case.probability
                    silently_applied += 1
                    if any(step.event_seen for step in r7.steps):
                        raise AssertionError("silent no-effect event became a signal")
                else:
                    if not r7.steps[t].event_seen:
                        raise AssertionError("impactful fault was not sensed")
                # The R7 and R3 policy receive identical histories strictly
                # before the fault; true loss eligibility must be identical.
                if r7.lost_at_fault != legacy.lost_at_fault:
                    raise AssertionError("the two policy modes disagree before event")
                if r7.eligible_results != legacy.eligible_results:
                    changed_strict_labels += 1
                if tuple(s.action for s in r7.steps) != tuple(s.action for s in legacy.steps):
                    changed_histories += 1
                    weight_trace_delta += case.probability
                y = r7.result("service")
                if y is not None:
                    eligible += case.probability
                    restored += case.probability * y
                scenario_checks += 1
            rows.append({
                "family": family,
                "index": index,
                "scenario_count": len(trial.cases),
                "silent_boundary_probability": str(weight_silent),
                "action_history_change_probability_vs_R3": str(weight_trace_delta),
                "actual_loss_probability": str(eligible),
                "strict_restoration_given_loss":
                    str(restored/eligible) if eligible else None,
            })
    profiles = []
    for family in TRAIN + TUNE:
        sub = [r for r in rows if r["family"] == family]
        profiles.append({
            "family": family, "independent_development_systems": len(sub),
            "mean_silent_boundary_probability":
                str(sum((Fraction(r["silent_boundary_probability"]) for r in sub),
                        Fraction()) / len(sub)),
            "mean_history_difference_probability":
                str(sum((Fraction(r["action_history_change_probability_vs_R3"])
                         for r in sub), Fraction()) / len(sub)),
            "zero_actual_loss_risk_systems":
                sum(Fraction(r["actual_loss_probability"]) == 0 for r in sub),
        })
    return {
        "gate":"R7",
        "classification":"OBSERVATION_MODEL_DEVELOPMENT_ONLY_NOT_H1",
        "seed":seed,
        "independent_development_systems":len(rows),
        "complete_trace_oracle_comparisons":scenario_checks,
        "silent_event_case_count":silently_applied,
        "changed_action_history_cases_vs_R3":changed_histories,
        "changed_strict_label_cases_vs_R3":changed_strict_labels,
        "sealed_family_cases":0,
        "confirmatory_samples":0,
        "observation_semantics":"PERFECT_STATE_CHANGE_DETECTION_NO_BOUNDARY_ANNOUNCEMENT",
        "family_profiles":profiles,
        "developer_system_rows":rows,
        "result":"PASS",
    }


def public_summary(result: dict) -> dict:
    return {key: value for key,value in result.items()
            if key != "developer_system_rows"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20261031)
    parser.add_argument("--train-n", type=int, default=24)
    parser.add_argument("--tune-n", type=int, default=12)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(seed=args.seed, train_n=args.train_n, tune_n=args.tune_n)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",
                               encoding="utf-8")
    print(json.dumps(public_summary(result), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
