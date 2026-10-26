# Gate G3 — strict restoration, retention, and joint-goal feasibility

**Status: bounded deterministic software/model verification, 2026-10-26. Not an H1 test, empirical finding, or new general law.**

## Problem

G2 reports targets *available after a shock*, conflating retained function, function newly established after the shock, and actual recovery of a function that was available before, then lost. G2 also tests goals individually: two independently reachable goals may be mutually infeasible under one shared consumable inventory.

G3 defines these outcomes separately and checks them against ordinary expanded-state reachability.

## Exact scope and foresight

G3 retains G2's finite durable capabilities, consumable integer inventory, one-tick atomic actions, optional capability construction and *one deterministic shock* at integer time τ within the horizon H. The fault is applied immediately before goal evaluation and action selection at τ; actions completed before that moment have already affected the state. Faults may remove held capabilities, destroy stock and disable future actions. Holding and using durable capabilities does not itself consume them.

**Crucial limitation: the planners know the fault time and effect before choosing their pre-shock actions.** Outputs are perfect-foresight, existential *best-case attainability*, NOT estimates of performance of policies facing an unpredictable disturbance.

## Four operational queries

- **Availability A(g):** earliest time t≥τ on *some* legal history when goal g is present after fault application.
- **Retention T(g):** an existential witness history has g immediately before τ and still has g immediately after applying the fault. This is not a restoration event.
- **Strict restoration R(g):** earliest time t>τ on a single witness history for which g was present immediately before τ, was actually removed *by that event*, and is reacquired by t. Creating g for the first time after τ is not strict restoration.
- **Joint attainment J(G):** earliest t≥τ at which one trajectory holds **every goal in the set G** at once. Individual existential witnesses for different goals may be incompatible.

The individual queries can be witnessed by different histories and cannot be casually combined into one global guarantee.

## Independent computational comparison

1. A **time-layer augmented-state baseline** enumerates a set of reachable states (time, durable capabilities, inventory vector, goals lost at shock). The lost-at-shock component is essential for memory of whether actual restoration occurred.
2. An **explicit action-history oracle** recursively enumerates timed action sequences, with a separate per-history resource dictionary and lost-goal record. It does not call the state-layer transition code.
3. For availability alone, G3 also checks agreement with G2's ordinary full state-space baseline, bfs_postfault.

The two G3 algorithms share G2's domain vocabulary and semantics; they are independent search algorithms rather than independent theories or an exhaustive mathematical proof.

## Reproducible diagnostic

Seed 20261026; 64 tiny synthetic systems plus one worsened-fault variant for each, with construction on and off. Expected comparisons: 256 augmented-state vs explicit-history, and 256 availability checks against the pre-existing G2 solver, with zero mismatches. The expected manifest is at [g3_expected.json](../experiments/g3_expected.json). Fifteen dedicated unit tests cover strict restoration, retention, horizons, lost goals, shared components, consumable inventory, replenishment, simultaneous goals and model equivalence.

Run from the repository root:

    python -m experiments.p1_gate3
    python -m unittest discover -s tests -v

**This is not preregistered P1 evidence**: the sample is restricted to one tiny generator family and lacks uncertainty analysis, held-out prediction or GBR model fitting.

## Counterexamples and findings about model semantics

**Preemptive availability versus strict restoration.** The alarm fixture has one history that constructs an optical transmitter before the wired channel fails, making its alarm available at t=2. On a *different* history, the alarm exists before the fault, is removed by it at τ=1, and must then be re-established. The earliest strictly restored alarm is at t=3. Comparing these times as if they came from one policy would be a category error.

**One shared kit, two individual targets.** Both g1 and g2 may be attainable individually at t=1 with a single kit, while no one execution can hold them together. Two kits, or later replenishment under a longer horizon, permit joint attainability. Thus goal-wise option counts are not a substitute for joint feasibility.

**Retained function is not restored function.** A target surviving τ counts as available and retained, but not strictly restored. A target first built after τ may be available without any pre-shock loss.

## Open gates

This implementation **does not calculate GBR, measure actual recovery probabilities, eliminate information leakage, or establish causal effects.** Structural independence under a chosen failure exposure must still be connected to inventory-aware policies. An important **G4** priority is non-clairvoyant policy evaluation, matched-information strong baselines, and explicit resource-sensitive plan provenance; only then can the preregistered P1 hypothesis testing be designed.
