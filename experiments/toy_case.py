"""Reproduces archived illustrative toy case v0.1; Python 3.9+, stdlib only."""
from dataclasses import dataclass
from itertools import combinations
import json

@dataclass(frozen=True)
class Plan:
    name: str
    dependencies: frozenset[str]
    steps: int
    kit_cost: int
    creates_capability: bool

BASE = frozenset({"power", "sensor", "wire_tx", "led", "timer", "assembly"})
SHOCK_EXPOSED = frozenset({"wire_tx", "led", "timer", "assembly"})
PLANS = (
    Plan("wired_existing", frozenset({"power","sensor","wire_tx"}), 1, 0, False),
    Plan("optical_newly_composed",
         frozenset({"power","sensor","led","timer","assembly"}), 2, 1, True),
)

def feasible_plans(caps: frozenset[str], *, generative: bool,
                   horizon: int = 2, kits: int = 1) -> tuple[Plan, ...]:
    """Plans feasible individually, not necessarily executable simultaneously."""
    return tuple(p for p in PLANS if p.dependencies <= caps
                 and p.steps <= horizon and p.kit_cost <= kits
                 and (generative or not p.creates_capability))

def goal_reachable(caps: frozenset[str], *, generative: bool) -> bool:
    return bool(feasible_plans(caps, generative=generative))

def has_disjoint_backup(plans: tuple[Plan, ...]) -> bool:
    """Disjoint ONLY relative to the explicitly shock-exposed set."""
    return any(not ((p.dependencies & SHOCK_EXPOSED)
                    & (q.dependencies & SHOCK_EXPOSED))
               for p, q in combinations(plans, 2))

def gop(caps: frozenset[str]) -> int:
    return int(goal_reachable(caps, generative=True)
               and not goal_reachable(caps, generative=False))

def gbr(caps: frozenset[str]) -> int:
    """Increment in binary backup indicator caused by construction."""
    return (int(has_disjoint_backup(feasible_plans(caps, generative=True)))
            - int(has_disjoint_backup(feasible_plans(caps, generative=False))))

def run() -> dict:
    after = BASE - {"wire_tx"}
    result = {
        "initial": {
            "fixed_goal_reachable": goal_reachable(BASE, generative=False),
            "generative_goal_reachable": goal_reachable(BASE, generative=True),
            "gop": gop(BASE), "gbr": gbr(BASE),
            "fixed_plans": [p.name for p in feasible_plans(BASE, generative=False)],
            "generative_plans": [p.name for p in feasible_plans(BASE, generative=True)]
        },
        "after_wire_failure": {
            "fixed_goal_reachable": goal_reachable(after, generative=False),
            "generative_goal_reachable": goal_reachable(after, generative=True),
            "gop": gop(after), "gbr": gbr(after),
            "generative_plans": [p.name for p in feasible_plans(after, generative=True)]
        }
    }
    assert result["initial"]["gop"] == 0 and result["initial"]["gbr"] == 1
    assert result["after_wire_failure"]["fixed_goal_reachable"] is False
    assert result["after_wire_failure"]["generative_goal_reachable"] is True
    assert result["after_wire_failure"]["gbr"] == 0
    return result

if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
