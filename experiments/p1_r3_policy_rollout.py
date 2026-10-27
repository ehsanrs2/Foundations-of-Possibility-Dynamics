"""R3: execute a FIXED policy with no access to future fault realization.

G2 one-tick, durable-capability and integer-consumable-stock semantics;
a single fault at an arbitrary unknown tick in [0,H]. A policy sees only its
current held capabilities, inventory, observed disabled actions and whether
a fault has occurred. Outcome is strict actual-loss restoration on ONE
executed history. This is a software/methods gate, not an H1 test.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from random import Random
import json

from experiments.p1_gate2 import Action, Fault, Model, generated
from experiments.p1_gate3 import augmented_solver


@dataclass(frozen=True)
class Observation:
    tick: int
    held: frozenset[str]
    stock: tuple[int, ...]
    disabled: frozenset[str]
    fault_observed: bool


@dataclass(frozen=True)
class FixedPolicy:
    before_priority: tuple[str, ...]
    after_priority: tuple[str, ...]
    construction: bool = True

    def choose(self, observed: Observation, actions: tuple[Action, ...]) -> str:
        """May NOT receive scenario identity, failure time or future event."""
        order = self.after_priority if observed.fault_observed else self.before_priority
        options = {a.name: a for a in actions}
        for name in order:
            a = options[name]
            if a.name in observed.disabled or (a.generative and not self.construction):
                continue
            if not a.requires <= observed.held:
                continue
            if any(x < y for x, y in zip(observed.stock, a.consumes)):
                continue
            if a.produces in observed.held and not any(a.yields):
                continue
            return name
        return "WAIT"


@dataclass(frozen=True)
class Case:
    name: str
    probability: Fraction
    fault: Fault


@dataclass(frozen=True)
class Trial:
    base: Model
    policy: FixedPolicy
    cases: tuple[Case, ...]

    def __post_init__(self):
        names = {a.name for a in self.base.actions}
        if len(names) != len(self.base.actions) or "WAIT" in names:
            raise ValueError("action identifiers must be unique and reserve WAIT")
        if set(self.policy.before_priority) != names or set(self.policy.after_priority) != names:
            raise ValueError("policy must specify each action once for both phases")
        if len(set(self.policy.before_priority)) != len(names) or len(set(self.policy.after_priority)) != len(names):
            raise ValueError("policy priority must not duplicate actions")
        if not self.cases or len({c.name for c in self.cases}) != len(self.cases):
            raise ValueError("nonempty uniquely named scenario set needed")
        if any(not c.name or not isinstance(c.probability, Fraction) or c.probability <= 0
               for c in self.cases):
            raise ValueError("positive exact rational probabilities required")
        if sum((c.probability for c in self.cases), Fraction()) != 1:
            raise ValueError("scenario probabilities must sum exactly to 1")
        for c in self.cases:
            f = c.fault
            if (not 0 <= f.tick <= self.base.horizon
                or len(f.destroy) != len(self.base.resources)
                or any(x < 0 for x in f.destroy)
                or not f.disable <= names):
                raise ValueError("invalid fault tick, inventory loss or action identity")


@dataclass(frozen=True)
class Step:
    tick: int
    start_caps: frozenset[str]
    observed_caps: frozenset[str]
    start_stock: tuple[int, ...]
    observed_stock: tuple[int, ...]
    disabled_seen: frozenset[str]
    event_seen: bool
    action: str | None
    end_caps: frozenset[str]
    end_stock: tuple[int, ...]


@dataclass(frozen=True)
class Outcome:
    case_name: str
    fault_tick: int
    held_before_fault: frozenset[str]
    lost_at_fault: frozenset[str]
    retained_at_fault: frozenset[str]
    first_restored_at: tuple[tuple[str, int], ...]
    eligible_results: tuple[tuple[str, int | None], ...]
    steps: tuple[Step, ...]

    def result(self, goal: str) -> int | None:
        return dict(self.eligible_results)[goal]


def execute(trial: Trial, case: Case) -> Outcome:
    if case not in trial.cases:
        raise ValueError("case must be registered in trial")
    held, stock = trial.base.initial, trial.base.stock
    disabled = frozenset()
    before, lost, retained = frozenset(), frozenset(), frozenset()
    restored: dict[str, int] = {}
    trace = []
    for tick in range(trial.base.horizon + 1):
        start_caps, start_stock = held, stock
        if tick == case.fault.tick:
            before = held & trial.base.goals
            held = held - case.fault.remove
            stock = tuple(max(0, x - d) for x, d in zip(stock, case.fault.destroy))
            disabled = disabled | case.fault.disable
            lost = before - held
            retained = before & held
        seen = tick >= case.fault.tick
        if tick > case.fault.tick:
            for goal in sorted(lost & held):
                restored.setdefault(goal, tick)
        chosen: str | None = None
        observed_caps, observed_stock = held, stock
        if tick < trial.base.horizon:
            observation = Observation(tick, held, stock, disabled, seen)
            chosen = trial.policy.choose(observation, trial.base.actions)
            if chosen != "WAIT":
                action = next(a for a in trial.base.actions if a.name == chosen)
                if not action.requires <= held or any(x < y for x,y in zip(stock,action.consumes)):
                    raise AssertionError("policy issued an infeasible action")
                held = held | {action.produces}
                stock = tuple(x-y+z for x,y,z in zip(stock,action.consumes,action.yields))
        trace.append(Step(tick, start_caps, observed_caps, start_stock, observed_stock,
                          disabled, seen, chosen, held, stock))
    labels = tuple((g, int(g in restored) if g in lost else None)
                   for g in sorted(trial.base.goals))
    return Outcome(case.name,case.fault.tick,before,lost,retained,
                   tuple(sorted(restored.items())),labels,tuple(trace))


def independent_history_oracle(trial: Trial, case: Case) -> Outcome:
    """Separate chronological dictionary-inventory reference; not execute()."""
    caps = set(trial.base.initial)
    inv = dict(zip(trial.base.resources, trial.base.stock))
    disabled: set[str] = set()
    before: set[str] = set()
    lost: set[str] = set()
    kept: set[str] = set()
    restored: dict[str,int] = {}
    log = []
    for time in range(trial.base.horizon + 1):
        start_caps, start_stock = frozenset(caps),tuple(inv[k] for k in trial.base.resources)
        if time == case.fault.tick:
            before = caps & set(trial.base.goals)
            caps.difference_update(case.fault.remove)
            for idx,key in enumerate(trial.base.resources):
                inv[key] = max(0,inv[key] - case.fault.destroy[idx])
            disabled.update(case.fault.disable)
            lost = before - caps
            kept = before & caps
        seen = time >= case.fault.tick
        if time > case.fault.tick:
            for g in sorted(lost & caps):
                restored.setdefault(g,time)
        visible_caps=frozenset(caps)
        visible_stock=tuple(inv[k] for k in trial.base.resources)
        action_name: str|None=None
        if time < trial.base.horizon:
            chosen_order = (trial.policy.after_priority if seen
                            else trial.policy.before_priority)
            action_name="WAIT"
            for name in chosen_order:
                act=next(a for a in trial.base.actions if a.name==name)
                if name in disabled or (act.generative and not trial.policy.construction):
                    continue
                if not act.requires.issubset(caps):
                    continue
                if any(inv[k]<act.consumes[i] for i,k in enumerate(trial.base.resources)):
                    continue
                if act.produces in caps and not any(act.yields):
                    continue
                action_name=name
                for i,k in enumerate(trial.base.resources):
                    inv[k]+=act.yields[i]-act.consumes[i]
                caps.add(act.produces)
                break
        log.append(Step(time,start_caps,visible_caps,start_stock,visible_stock,
                        frozenset(disabled),seen,action_name,
                        frozenset(caps),tuple(inv[k] for k in trial.base.resources)))
    labels=tuple((g, int(g in restored) if g in lost else None)
                 for g in sorted(trial.base.goals))
    return Outcome(case.name,case.fault.tick,frozenset(before),frozenset(lost),
                   frozenset(kept),tuple(sorted(restored.items())),labels,tuple(log))


def loss_conditioned_probability(trial: Trial) -> dict[str, dict[str, str | None]]:
    """Per-goal conditional P(restore | actual loss), not policy success overall."""
    output = {}
    for goal in sorted(trial.base.goals):
        eligibility = Fraction()
        success = Fraction()
        for case in trial.cases:
            result = execute(trial,case).result(goal)
            if result is not None:
                eligibility += case.probability
                success += case.probability * result
        output[goal] = {
            "eligible_probability":str(eligibility),
            "restoration_given_loss":str(success/eligibility) if eligibility else None,
        }
    return output


def verify(trial: Trial) -> int:
    count=0
    for case in trial.cases:
        value = execute(trial,case)
        other = independent_history_oracle(trial,case)
        if value != other:
            raise AssertionError(("independent execution traces disagree",trial,case,value,other))
        g3 = augmented_solver(replace(trial.base,fault=case.fault),
                              construction=trial.policy.construction)
        for goal,tick in value.first_restored_at:
            if goal not in g3.restored or g3.restored[goal] > tick:
                raise AssertionError("actual policy restoration exceeds G3 existential bound")
        count+=1
    return count


def demonstrator() -> Trial:
    """Unknown fault time, deterministic heuristic repair; goal initially held."""
    base=Model(
        initial=frozenset({"service","base","spare"}),
        goals=frozenset({"service"}),resources=("kit",),stock=(1,),
        actions=(
            Action("restore",frozenset({"base","spare"}),"service",(1,),(0,),True),
            Action("idle_product",frozenset({"base"}),"unused",(0,),(0,)),
        ),
        horizon=4,fault=Fault(2,frozenset({"service"}),(0,)),
    )
    policy=FixedPolicy(("idle_product","restore"),("restore","idle_product"))
    cases=(
        Case("early_loss",Fraction(1,3),Fault(1,frozenset({"service"}),(0,))),
        Case("late_loss",Fraction(1,3),Fault(4,frozenset({"service"}),(0,))),
        Case("no_loss",Fraction(1,3),Fault(2,frozenset(),(0,))),
    )
    return Trial(base,policy,cases)


def audit(seed: int=20261027, n: int=32) -> dict:
    rng=Random(seed)
    comparisons=0
    for model in generated(seed,n):
        names=tuple(sorted(a.name for a in model.actions))
        fixed=FixedPolicy(names,tuple(reversed(names)))
        alt_tick=rng.randint(0,model.horizon)
        cases=(
            Case("specified",Fraction(1,2),model.fault),
            Case("alternative",Fraction(1,2),
                 replace(model.fault,tick=alt_tick,remove=frozenset())),
        )
        comparisons+=verify(Trial(model,fixed,cases))
    example=demonstrator()
    comparisons+=verify(example)
    outcomes={c.name:execute(example,c).result("service") for c in example.cases}
    assert outcomes=={"early_loss":1,"late_loss":0,"no_loss":None}, outcomes
    assert loss_conditioned_probability(example)["service"]=={
        "eligible_probability":"2/3","restoration_given_loss":"1/2"
    }
    return {"gate":"R3","classification":"policy_execution_software_checks_not_H1",
            "seed":seed,"small_models":n,"independent_trace_comparisons":comparisons,
            "example_labels":{"early_loss":1,"late_loss":0,"no_loss":None},
            "example_eligibility":"2/3","example_conditional_restoration":"1/2",
            "mismatches":0,"result":"PASS"}


if __name__=="__main__":
    print(json.dumps(audit(),indent=2,sort_keys=True))
