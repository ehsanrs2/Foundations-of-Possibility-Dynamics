"""R5 development-only exploratory pilot; H1 NOT tested.

Enumerate four stipulated R4 shock cases per system under THREE fixed
non-anticipative policy variants. These are not trained prediction models,
statistically independent shock observations, or held-out test families.

Output contains per-case eligibility, actual strict restoration, kit usage,
policy sensitivity and a separate G3 *clairvoyant* feasibility diagnostic.
A G3 bound is never presented as a fair policy or predictive baseline.
"""
from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from time import perf_counter
import argparse
import json

from experiments.p1_gate3 import augmented_solver
from experiments.p1_r3_policy_rollout import (
    FixedPolicy, Trial, execute, independent_history_oracle,
)
from experiments.p1_r4_development_families import (
    TRAIN, TUNE, SEALED, make_instance,
)

POLICIES = ("R3_original", "prepare_first_after_fault", "construction_disabled")


def _variants(trial: Trial) -> dict[str, Trial]:
    return {
        "R3_original": trial,
        "prepare_first_after_fault": replace(trial, policy=FixedPolicy(
            trial.policy.before_priority, trial.policy.before_priority, True)),
        "construction_disabled": replace(trial, policy=replace(
            trial.policy, construction=False)),
    }


def _ratio(value: Fraction) -> str:
    return str(value)


def _case_entry(trial: Trial, case) -> dict:
    history = execute(trial, case)
    reference = independent_history_oracle(trial, case)
    if history != reference:
        raise AssertionError("R3 full trajectory reference mismatch")
    goal = "service"
    result = history.result(goal)
    if result is not None:
        g3 = augmented_solver(replace(trial.base, fault=case.fault),
                              construction=trial.policy.construction)
        # G3 existential feasibility is ONLY a diagnostic upper bound
        # for this particular scenario; not an equal-information policy.
        upper = int(goal in g3.restored)
        if result > upper:
            raise AssertionError("executed policy exceeds G3 feasibility")
    else:
        upper = None
    actions = {a.name: a for a in trial.base.actions}
    kit_consumed = sum(
        actions[s.action].consumes[0] for s in history.steps
        if s.action in actions
    )
    kit_destroyed = 0
    for step in history.steps:
        if step.tick == case.fault.tick:
            kit_destroyed = step.start_stock[0] - step.observed_stock[0]
            break
    return {
        "case": case.name,
        "probability": _ratio(case.probability),
        "fault_tick": case.fault.tick,
        "eligible": result is not None,
        "strict_restoration": result,
        "clairvoyant_feasibility_only": upper,
        "kit_consumed_by_actions": kit_consumed,
        "kit_destroyed_by_fault": kit_destroyed,
        "policy_steps": len(history.steps) - 1,
        "selected_actions": sum(s.action not in ("WAIT", None) for s in history.steps),
    }


def _summarize_rows(rows: list[dict]) -> dict:
    total = Fraction()
    loss = Fraction()
    recovered = Fraction()
    g3 = Fraction()
    consumed = Fraction()
    destroyed = Fraction()
    actions = Fraction()
    steps = Fraction()
    for row in rows:
        w = Fraction(row["probability"])
        total += w
        loss += w * row["eligible"]
        if row["eligible"]:
            recovered += w * row["strict_restoration"]
            g3 += w * row["clairvoyant_feasibility_only"]
        consumed += w * row["kit_consumed_by_actions"]
        destroyed += w * row["kit_destroyed_by_fault"]
        actions += w * row["selected_actions"]
        steps += w * row["policy_steps"]
    if total != 1:
        raise AssertionError("every system needs normalized scenario probabilities")
    return {
        "eligible_mass": _ratio(loss),
        "restored_mass": _ratio(recovered),
        "strict_restoration_given_loss": _ratio(recovered / loss) if loss else None,
        "clairvoyant_eligible_feasibility_mass": _ratio(g3),
        "mean_kit_consumed": _ratio(consumed),
        "mean_kit_destroyed": _ratio(destroyed),
        "mean_selected_actions": _ratio(actions),
        "mean_decision_ticks": _ratio(steps),
    }


def _summary(records: list[dict], family: str, policy: str) -> dict:
    matching = [item for item in records if item["family"] == family
                and item["policy"] == policy]
    if not matching:
        raise AssertionError("missing development family/policy")
    losses = sum((Fraction(item["summary"]["eligible_mass"]) for item in matching),
                 Fraction())
    restored = sum((Fraction(item["summary"]["restored_mass"]) for item in matching),
                   Fraction())
    eligible_systems = sum(Fraction(item["summary"]["eligible_mass"]) > 0
                           for item in matching)
    per_system_conditional = [
        Fraction(item["summary"]["strict_restoration_given_loss"])
        for item in matching
        if item["summary"]["strict_restoration_given_loss"] is not None
    ]
    return {
        "family": family,
        "policy": policy,
        "independent_dev_systems": len(matching),
        "systems_with_eligible_loss": eligible_systems,
        "mean_loss_eligibility_mass": _ratio(losses / len(matching)),
        "pooled_descriptive_restoration_given_loss":
            _ratio(restored / losses) if losses else None,
        "mean_of_system_conditional_restoration":
            _ratio(sum(per_system_conditional, Fraction()) /
                   len(per_system_conditional)) if per_system_conditional else None,
        "total_eligible_case_records": sum(
            sum(x["eligible"] for x in item["cases"]) for item in matching),
        "total_case_records": sum(len(item["cases"]) for item in matching),
        "mean_kit_consumed": _ratio(
            sum((Fraction(item["summary"]["mean_kit_consumed"])
                 for item in matching), Fraction()) / len(matching)),
        "mean_selected_actions": _ratio(
            sum((Fraction(item["summary"]["mean_selected_actions"])
                 for item in matching), Fraction()) / len(matching)),
    }


def run(*, seed: int = 20261030, train_n: int = 24,
        tune_n: int = 12) -> dict:
    if type(seed) is not int:
        raise ValueError("seed must be an integer")
    if type(train_n) is not int or not 1 <= train_n <= 24:
        raise ValueError("training DEV pilot per-family n must be 1..24")
    if type(tune_n) is not int or not 1 <= tune_n <= 12:
        raise ValueError("tuning DEV pilot per-family n must be 1..12")
    if set(TRAIN + TUNE).intersection(SEALED):
        raise AssertionError("sealed families cannot overlap development sets")
    start = perf_counter()
    rows = []
    seen = set()
    for family in TRAIN + TUNE:
        n = train_n if family in TRAIN else tune_n
        for index in range(n):
            dev = make_instance(family, seed, index)
            if dev.seed_id in seen:
                raise AssertionError("duplicate instance seed")
            seen.add(dev.seed_id)
            for policy, trial in _variants(dev.trial).items():
                cases = [_case_entry(trial, case) for case in trial.cases]
                rows.append({
                    "family": family, "index": index, "policy": policy,
                    "seed_fingerprint": dev.seed_id,
                    "structure_fingerprint": dev.fingerprint,
                    "summary": _summarize_rows(cases),
                    "cases": cases,
                })
    if len(seen) != 3 * train_n + tune_n:
        raise AssertionError("unexpected independent development system count")
    if any(item["family"] in SEALED for item in rows):
        raise AssertionError("SEALED leakage")
    summaries = [_summary(rows, family, policy)
                 for family in TRAIN + TUNE for policy in POLICIES]
    # Our developer cases are deliberately 3 losses + 1 no-loss, each
    # with probability 1/4; 3/4 is BY DESIGN, not inferred from real faults.
    if any(s["mean_loss_eligibility_mass"] != "3/4" for s in summaries):
        raise AssertionError("developer eligibility design unexpectedly changed")
    return {
        "gate": "R5",
        "classification": "DEVELOPMENT_ONLY_DESCRIPTIVE_PILOT_NOT_H1",
        "seed": seed,
        "train_instances_per_family": train_n,
        "tune_instances": tune_n,
        "independent_dev_systems": len(seen),
        "case_evaluations": len(rows) * 4,
        "full_trace_oracle_comparisons": len(rows) * 4,
        "sealed_family_generation": 0,
        "confirmatory_outcomes": 0,
        "policy_variants": list(POLICIES),
        "scope_warning": "eligibility is designed as three losses of four cases; policies are developer heuristics",
        "family_policy_summaries": summaries,
        "raw_development_rows": rows,
        "wall_clock_profile_seconds": round(perf_counter() - start, 6),
    }


def _public_summary(pilot: dict) -> dict:
    return {k:v for k,v in pilot.items()
            if k not in ("raw_development_rows", "wall_clock_profile_seconds")}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed",type=int,default=20261030)
    parser.add_argument("--train-n",type=int,default=24)
    parser.add_argument("--tune-n",type=int,default=12)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    pilot = run(seed=args.seed, train_n=args.train_n, tune_n=args.tune_n)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(pilot,indent=2,sort_keys=True)+"\n",
                               encoding="utf-8")
    print(json.dumps(_public_summary(pilot),indent=2,sort_keys=True))


if __name__=="__main__":
    main()
