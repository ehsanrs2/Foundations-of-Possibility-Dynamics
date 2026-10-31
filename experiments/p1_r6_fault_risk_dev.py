"""R6: DEVELOPMENT-ONLY variable fault-risk model and exact full-input baseline.

This fixes R5's forced 3/4 *design eligibility*, not physical realism.
There are three externally stipulated INDEPENDENT Bernoulli basic events:
service loss, shared infrastructure loss, and one-kit destruction.
Fault time is early/late with equal chance. Every scenario, including the
no-effect case, triggers R3's observable scheduled boundary flag (limitation).
The outcome is one fixed R3 policy's strict restoration given ACTUAL loss.
No H1 feature, fit, sealed test family or confirmatory inference is involved.

The full-model marginal predictor receives all pre-fault model inputs and
the hazard law but NOT the realized future fault. It is a standard exact
equal-information Bayes baseline in this tiny known simulator; no deterministic
feature of the same X can improve its expected proper score.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
from random import Random
import argparse
import json

from experiments.p1_gate2 import Fault
from experiments.p1_r3_policy_rollout import (
    Case, Trial, execute, independent_history_oracle,
)
from experiments.p1_r4_development_families import (
    TRAIN, TUNE, SEALED, make_instance,
)

SERVICE_RISKS = (Fraction(0), Fraction(1, 8), Fraction(1, 4),
                 Fraction(1, 2), Fraction(3, 4))
SHARED_RISKS = (Fraction(0), Fraction(1, 4), Fraction(1, 2))
STOCK_RISKS = (Fraction(0), Fraction(1, 4), Fraction(1, 2))


@dataclass(frozen=True)
class HazardLaw:
    service_loss: Fraction
    shared_loss: Fraction
    stock_loss: Fraction

    def __post_init__(self) -> None:
        if any(not isinstance(p, Fraction) or not Fraction(0) <= p <= Fraction(1)
               for p in (self.service_loss, self.shared_loss, self.stock_loss)):
            raise ValueError("all event probabilities must be exact rationals in [0,1]")


def developer_law(master_seed: int, family: str, index: int) -> HazardLaw:
    # Guard family FIRST. The sealed families have no generator or risk draws.
    if family in SEALED:
        raise PermissionError("SEALED test family not available before registration")
    if family not in TRAIN + TUNE:
        raise ValueError("unknown development family")
    if type(master_seed) is not int or type(index) is not int or index < 0:
        raise ValueError("integer seed and nonnegative integer index required")
    digest = sha256(f"R6-DEV-RISK-V1|{master_seed}|{family}|{index}".encode()).digest()
    rng = Random(int.from_bytes(digest[:8], "big"))
    return HazardLaw(rng.choice(SERVICE_RISKS), rng.choice(SHARED_RISKS),
                     rng.choice(STOCK_RISKS))


def _event_probability(event_occurs: bool, p: Fraction) -> Fraction:
    return p if event_occurs else 1 - p


def develop_trial(master_seed: int, family: str, index: int,
                  *, law: HazardLaw | None = None) -> Trial:
    """Replace R4's four hard-coded faults without using R4's fault outcomes."""
    if family in SEALED:
        raise PermissionError("SEALED test family blocked before model construction")
    dev = make_instance(family, master_seed, index)
    event_law = law if law is not None else developer_law(master_seed, family, index)
    if not isinstance(event_law, HazardLaw):
        raise TypeError("explicit HazardLaw required")
    base = dev.trial.base
    shared = "hub" if family == "hub_dependencies" else "base"
    # Known fault-time distribution with two possible *future* times.
    # This is not a hidden-time partially observed stochastic process.
    early, late = 1, base.horizon
    cases = []
    for stage, tick in (("early", early), ("late", late)):
        for loss_service, loss_shared, lose_kit in product((False, True), repeat=3):
            w = Fraction(1, 2)
            for active, p in zip((loss_service, loss_shared, lose_kit),
                                 (event_law.service_loss,
                                  event_law.shared_loss,
                                  event_law.stock_loss)):
                w *= _event_probability(active, p)
            if not w:
                continue
            remove = set()
            if loss_service:
                remove.add("service")
            if loss_shared:
                remove.add(shared)
            cases.append(Case(
                f"{stage}_s{int(loss_service)}_c{int(loss_shared)}_k{int(lose_kit)}",
                w, Fault(tick, frozenset(remove),
                         (1 if lose_kit else 0,)),
            ))
    if sum((c.probability for c in cases), Fraction()) != 1:
        raise AssertionError("independent fault-event scenario law not normalized")
    return Trial(replace(base, fault=cases[0].fault), dev.trial.policy, tuple(cases))


def exact_pre_fault_policy_baseline(trial: Trial, *, verify_history: bool = True) -> dict:
    """Marginalize known cases BEFORE observing the realized case; no foresight.

    This exact full-input baseline has access to all declared model rules,
    fixed policy, scenario probabilities and horizon, as must any competing
    deterministic feature. It is expensive but a fair *information* reference.
    """
    loss_weight = Fraction()
    restored_weight = Fraction()
    n_checked = 0
    for case in trial.cases:
        realized = execute(trial, case)
        if verify_history and realized != independent_history_oracle(trial, case):
            raise AssertionError("independently implemented R3 trajectories disagree")
        outcome = realized.result("service")
        if outcome is not None:
            loss_weight += case.probability
            restored_weight += case.probability * outcome
        n_checked += 1
    p = restored_weight / loss_weight if loss_weight else None
    return {
        "eligible_mass": str(loss_weight),
        "restored_mass": str(restored_weight),
        "conditional_restoration_probability": str(p) if p is not None else None,
        "model_optimal_expected_brier_conditional":
            str(p * (1 - p)) if p is not None else None,
        "constant_half_expected_brier_excess":
            str((Fraction(1, 2) - p)**2) if p is not None else None,
        "complete_history_checks": n_checked if verify_history else 0,
        "scenario_count": len(trial.cases),
    }


def run(*, seed: int = 20261031, train_n: int = 24,
        tune_n: int = 12) -> dict:
    if type(seed) is not int:
        raise ValueError("master seed must be integer")
    if type(train_n) is not int or not 1 <= train_n <= 24:
        raise ValueError("training count restricted to 1..24 per family")
    if type(tune_n) is not int or not 1 <= tune_n <= 12:
        raise ValueError("tuning count restricted to 1..12")
    records, profiles = [], []
    checks = 0
    fingerprints = set()
    for family in TRAIN + TUNE:
        n = train_n if family in TRAIN else tune_n
        family_rows = []
        for index in range(n):
            dev = make_instance(family, seed, index)
            if dev.seed_id in fingerprints:
                raise AssertionError("duplicate system seed fingerprint")
            fingerprints.add(dev.seed_id)
            law = developer_law(seed, family, index)
            trial = develop_trial(seed, family, index, law=law)
            out = exact_pre_fault_policy_baseline(trial)
            if Fraction(out["eligible_mass"]) != law.service_loss:
                # This checks R3's actual pre-fault service bookkeeping.
                raise AssertionError("designed service loss differs from actual eligibility")
            checks += out["complete_history_checks"]
            item = {
                "family": family, "index": index,
                "system_seed_id": dev.seed_id,
                "structure_sha256": dev.fingerprint,
                "risk_law": {
                    "service_loss": str(law.service_loss),
                    "shared_loss": str(law.shared_loss),
                    "stock_loss": str(law.stock_loss),
                },
                **out,
            }
            family_rows.append(item)
            records.append(item)
        eligible = [x for x in family_rows
                    if x["conditional_restoration_probability"] is not None]
        profiles.append({
            "family": family,
            "independent_developer_systems": n,
            "positive_loss_risk_systems": len(eligible),
            "zero_loss_risk_systems": n - len(eligible),
            "mean_design_loss_risk":
                str(sum((Fraction(x["eligible_mass"]) for x in family_rows),
                        Fraction()) / n),
            "mean_model_conditional_restoration_given_eligible":
                str(sum((Fraction(x["conditional_restoration_probability"])
                         for x in eligible), Fraction()) / len(eligible))
                if eligible else None,
            "mean_exact_full_input_brier_given_eligible":
                str(sum((Fraction(x["model_optimal_expected_brier_conditional"])
                         for x in eligible), Fraction()) / len(eligible))
                if eligible else None,
            "mean_half_predictor_excess_brier_given_eligible":
                str(sum((Fraction(x["constant_half_expected_brier_excess"])
                         for x in eligible), Fraction()) / len(eligible))
                if eligible else None,
            "event_law_ontology": "THREE_STIPULATED_INDEPENDENT_BASIC_EVENTS",
        })
    return {
        "gate":"R6",
        "classification":"DEVELOPMENT_ONLY_RISK_LAW_AND_EXACT_BASELINE_NOT_H1",
        "seed":seed,
        "independent_developer_systems":len(fingerprints),
        "full_history_oracle_checks":checks,
        "heldout_generated":0,
        "confirmatory_samples":0,
        "known_model_oracle":"PREFAULT_EXPECTED_STRICT_RESTORATION_NOT_CLAIRVOYANT_SCENARIO",
        "zero_risk_not_zero_outcome":True,
        "null_event_boundary_observed":True,
        "family_profiles":profiles,
        "system_records":records,
        "result":"PASS",
    }


def summary(result: dict) -> dict:
    return {k:v for k,v in result.items() if k != "system_records"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed",type=int,default=20261031)
    parser.add_argument("--train-n",type=int,default=24)
    parser.add_argument("--tune-n",type=int,default=12)
    parser.add_argument("--output",type=Path)
    args = parser.parse_args()
    result = run(seed=args.seed,train_n=args.train_n,tune_n=args.tune_n)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",
                               encoding="utf-8")
    print(json.dumps(summary(result),sort_keys=True,indent=2))


if __name__ == "__main__":
    main()
