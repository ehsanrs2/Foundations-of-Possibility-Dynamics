# G1 verification — causal plan support and first scoped GBR calculation

**Date: 2026-10-26. Status: local formal-model/software check, not preregistered P1, not evidence for H1.**

## Problem G1 resolves

Gate G0 established agreement on *goal reachability* under a restricted production model. Reachability by itself does not distinguish whether the **same goal** has two pathways supported by different components.

Gate G1 attaches **causal support** to each plan. A support comprises every initial component relied on in the causal derivation of the goal and every production/use rule required by that derivation. Plan supports are not just the set of components present anywhere in a system. Unrelated actions performed before reaching the target are excluded.

## Explicit formal restrictions

- Finite, sequential rule executions; every step duration is a **positive integer**.
- Rules require nonempty AND-type prerequisite sets and produce one capability label; different rules may produce the same label, but a plan never produces one label twice.
- Initial source capabilities are available from the beginning. Production adds capabilities; **inputs are never consumed**.
- Budgets are summed over executed causal rules and deadlines over sequential causal steps.
- No probabilistic shock distribution, concurrent commitments, depreciation or failure during a plan.
- Two individually feasible plans need **not** be jointly feasible with a single finite inventory.
- Source faults remove `cap:NAME` from starting holdings before replanning; surviving rules may rebuild that label. A `rule:NAME` fault disables its rule.
- The vulnerability universe `F` is explicitly chosen: both plan supports are projected to the exposure tokens in `F`. All independence claims are **conditional on this projection**.

The code does **not** establish a notion of absolute independence from every possible common cause.

## Two comparison procedures

1. `enumerate_dfs` enumerates legal action sequences under the resource and time constraints, and records goal plans using ancestry supports.
2. `enumerate_subsets` independently enumerates candidate rule **subsets**, rejects duplicate output production, checks whether the chosen rules admit a legal dependency order, and records the resulting goal plans.

The two methods use the same domain model and some plan-normalization conventions. They are therefore *partially independent*, not a proof by entirely separate implementations; this is an important limitation.

Both methods include **ordinary non-generative goal-use rules** and optional capability-generating rules. The first provides a baseline and the second a superset.

## Formula implemented

For feasible baseline and construction-enabled plan sets `P0(g)` and `P+(g)`, the binary backup indicator `b(g,P,F)` equals one if at least two distinct plans have no common support token among the exposure tokens in `F`.

The code calculates `GBR_gain = Σ[g baseline-reachable] (b(g,P+,F)-b(g,P0,F))`.

It also computes GOG as the number of goals newly attainable with construction. These are **candidate definitions**, not claims of original mathematics.

## Deterministic diagnostic

The fixed seed 20261026 generates 48 small AND-rule models (2–7 rules each); one starting-source deletion variant is generated per model. Both algorithms compare their complete **sets of causal plans** with and without optional construction.

- Original instances: **48**
- Pre-simulation shock variants: **48**
- Independent plan-set comparisons: **192**
- Observed mismatches: **0**
- Candidate measure comparisons: **96**, equal by the two enumerators
- Manually constructed alarm example: GOG = **0** before shock, GBR gain = **1** under the originally declared narrow exposure set
- Wire-transmitter shock: GOG = **1** for recovery-only creation, GBR gain = **0** because only one surviving route remains
- Adding shared power to exposure removes the disjoint-backup interpretation.

All of these are **software/formal checks**. They do not measure recovery probability or predictive superiority of GBR.

## Reproduction

Run:

    python -m experiments.p1_gate1
    python -m unittest discover -s tests -v

The deterministic expected audit record is at [g1_expected.json](../experiments/g1_expected.json), and the algorithm at [p1_gate1.py](../experiments/p1_gate1.py). The seed and sample size are selected for diagnostics, not power or empirical representativeness.

## Review findings and next gates

**Passed:** basic causal support trace, AND prerequisites, alternative producers, disjointness relative to a named vulnerability set, static-vs-generative distinction, pre-planning shocks, costs, deadlines and two independent enumeration strategies for small systems.

**Still missing:** independently implemented provenance-tracing oracle, consumption of shared inventory, runtime/interdependent faults, simultaneous multi-goal policies, validated generative-redundancy baselines, held-out generator families, sample-size calculation and confirmatory testing of H1.

G1 therefore **closes only the bounded plan-support software gate**, not the P1 scientific validation protocol.
