"""B1 developer-only GOG semantic conformance over the EXISTING G2 finite model.

This is a no-shock / one-tick / finite-goal operational profile. GOG is a
reachability-set *difference*, not a backup, recovery, causal or H1 score.
Three EXISTING ordinary augmented-state/history solvers cross-check
the same declared toy model; these are not independent field measurements
or a new mathematical reachability formalism.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
import json

from experiments.p1_gate2 import Action, Fault, Model, bfs_postfault, dfs_postfault
from experiments.p1_gate3 import augmented_solver

PROFILE = "B1_GOG_G2_NO_SHOCK_V1"


@dataclass(frozen=True)
class GOGResult:
    """The fixed query vocabulary is model.goals, never inferred from outputs."""
    ordinary: tuple[str, ...]
    constructive: tuple[str, ...]
    newly_reachable: tuple[str, ...]
    gog: int

    def as_dict(self) -> dict:
        return {
            "ordinary": list(self.ordinary),
            "constructive": list(self.constructive),
            "newly_reachable": list(self.newly_reachable),
            "gog": self.gog,
        }


def _require_no_shock_profile(model: Model) -> None:
    """Reject accidental use of post-shock G2 data as pre-shock GOG."""
    if (model.fault.tick != 0 or model.fault.remove or
            model.fault.disable or any(model.fault.destroy)):
        raise ValueError("B1 GOG requires a declared zero-effect boundary event at tick 0")
    if not model.goals or not all(model.goals):
        raise ValueError("B1 GOG requires a nonempty externally fixed goal vocabulary")
    if model.horizon > 6 or len(model.actions) > 8 or len(model.resources) > 2:
        raise ValueError("B1 developer oracle bounded to horizon<=6, actions<=8, resources<=2")
    if any(x > 4 for x in model.stock):
        raise ValueError("B1 developer oracle bounded to initial resource stock<=4")


def evaluate_gog(model: Model) -> GOGResult:
    """Compare *only* disabling versus optionally allowing generative actions.

    One initial model, goal vocabulary, resource budget, horizon and
    non-generative action grammar are shared. No sample or model fitting.
    """
    _require_no_shock_profile(model)
    reachable: dict[bool, set[str]] = {}
    for enabled in (False, True):
        state_dp = bfs_postfault(model, construction=enabled)
        chronological = dfs_postfault(model, construction=enabled)
        ordinary_augmented = augmented_solver(model, construction=enabled)
        if state_dp != chronological or state_dp != ordinary_augmented.available:
            raise AssertionError("G2 DP, G2 history, G3 ordinary augmented-state disagree")
        if not set(state_dp) <= model.goals:
            raise AssertionError("unregistered goals were admitted")
        reachable[enabled] = set(state_dp)
    if not reachable[False] <= reachable[True]:
        raise AssertionError("optional-action nesting violated")
    new = reachable[True] - reachable[False]
    return GOGResult(tuple(sorted(reachable[False])),
                     tuple(sorted(reachable[True])),
                     tuple(sorted(new)), len(new))


def _model(actions: tuple[Action, ...], goals: frozenset[str],
           *, stock: int = 1, horizon: int = 2,
           initial: frozenset[str] = frozenset({"seed"})) -> Model:
    return Model(
        initial=initial, goals=goals, resources=("kit",), stock=(stock,),
        actions=actions, horizon=horizon,
        fault=Fault(tick=0, remove=frozenset(), destroy=(0,)),
    )


def constructive_goal_fixture() -> Model:
    """One constructed intermediate creates a newly reachable service."""
    return _model((
        Action("build_bridge", frozenset({"seed"}), "bridge", (1,), (0,), True),
        Action("provide", frozenset({"bridge"}), "service", (0,), (0,)),
    ), frozenset({"service"}))


def backup_only_fixture() -> Model:
    """Additional constructed *route* to an already reachable service."""
    base = constructive_goal_fixture()
    direct = Action("direct", frozenset({"seed", "wire"}), "service",
                    (0,), (0,))
    return replace(base, initial=frozenset({"seed", "wire"}),
                   actions=base.actions + (direct,))


def mutually_exclusive_goals_fixture(*, stock: int = 1) -> Model:
    """Each goal individually feasible, but shared kit can block the pair."""
    return _model((
        Action("build_a", frozenset({"seed"}), "g1", (1,), (0,), True),
        Action("build_b", frozenset({"seed"}), "g2", (1,), (0,), True),
    ), frozenset({"g1", "g2"}), stock=stock)


def renamed_fixture(model: Model, mapping: dict[str, str]) -> Model:
    """Bijection of capability labels only; action names are also renamed."""
    vocab = (set(model.initial) | set(model.goals) |
             {a.produces for a in model.actions} |
             set().union(*(a.requires for a in model.actions)))
    if set(mapping) != vocab or len(set(mapping.values())) != len(mapping):
        raise ValueError("renaming requires a bijection of all capability tokens")
    return replace(
        model, initial=frozenset(mapping[x] for x in model.initial),
        goals=frozenset(mapping[x] for x in model.goals),
        actions=tuple(replace(a, name="renamed_" + a.name,
                              requires=frozenset(mapping[x] for x in a.requires),
                              produces=mapping[a.produces])
                      for a in model.actions),
    )


def audit() -> dict:
    base = constructive_goal_fixture()
    new = evaluate_gog(base)
    short = evaluate_gog(replace(base, horizon=1))
    no_stock = evaluate_gog(replace(base, stock=(0,)))
    backup = evaluate_gog(backup_only_fixture())
    two = mutually_exclusive_goals_fixture(stock=1)
    two_result = evaluate_gog(two)
    joint = augmented_solver(two, construction=True).joint
    two_stock_joint = augmented_solver(
        mutually_exclusive_goals_fixture(stock=2), construction=True).joint
    other_goals = evaluate_gog(replace(base, goals=frozenset({"bridge", "service"})))
    aliased = evaluate_gog(replace(base, actions=base.actions + (
        Action("same_build_alias", frozenset({"seed"}), "bridge",
               (1,), (0,), True),
        Action("inert", frozenset({"seed"}), "seed", (0,), (0,)),
    )))
    mapping = {"seed": "root", "bridge": "relay", "service": "objective"}
    renamed = evaluate_gog(renamed_fixture(base, mapping))

    if not (new.gog == 1 and new.newly_reachable == ("service",)
            and short.gog == 0 and no_stock.gog == 0
            and backup.gog == 0 and backup.ordinary == ("service",)
            and two_result.gog == 2 and joint is None and two_stock_joint == 2
            and other_goals.gog == 2 and aliased == new
            and renamed.gog == new.gog
            and renamed.newly_reachable == ("objective",)):
        raise AssertionError("B1 GOG semantics or counterexample changed")
    return {
        "gate": "B1",
        "status": "PASS_PROVISIONAL_DEVELOPER_CONFORMANCE",
        "profile": PROFILE,
        "no_shock": True,
        "outcome": "EXISTENTIAL_EACH_GOAL_NOT_JOINT_OR_RESTORATION",
        "primary_H1_test": False,
        "confirmatory_H1_samples": 0,
        "sealed_family_calls": 0,
        "oracle_engines": ["G2_state_layers", "G2_independent_history",
                           "G3_augmented_state"],
        "checked_profile_variants": 9,
        "new_goal_example_gog": new.gog,
        "backup_only_gog": backup.gog,
        "resource_exclusive_individual_gog": two_result.gog,
        "resource_exclusive_joint_attainable": joint is not None,
        "expanded_goal_vocabulary_gog": other_goals.gog,
        "renaming_preserved_gog": renamed.gog == new.gog,
        "alias_preserved_gog": aliased == new,
        "classification": "GOG_SEMANTIC_SOFTWARE_CONTROL_NOT_NOVELTY_NOT_H1",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True, indent=2))
