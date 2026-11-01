# R9 — Physical mechanism identity and an explicitly incomplete work budget

**Status:** predeclared, constructed developer controls only. Not H1; not a field validation; not an equal-CPU/RAM benchmark. Date: 2026-11-01.

## The problem after R8

R8 obtained R1=0 across all 84 tiny development systems and exactly zero added expected Brier improvement. Changing fault definitions after observing that result would invalidate the comparison. R9 therefore **preserves R8 unchanged** and builds six new, predeclared synthetic fixtures to separate (a) physically real route independence, (b) falsely separate names, (c) common-cause failure, and (d) stock/time bottlenecks.

All fixtures start with a working service that is **actually deleted** by one fault at a known preparation boundary; the fault identity is unknown to the policy. Exactly one post-fault service-repair tick remains. Before the event, preparation of channel A or B consumes one kit and one tick, and unused kits are destroyed at the event boundary. The deterministic R7 controller sees only the current capability set, stock and visible disabled delivery rules. It does **not** see the future fault realization.

## Three explicitly assumed physical worlds

| Mode | Physical premise | Simulated basic failure events | Static R1 outcome |
|---|---|---|---|
| Independent | Two distinct delivery devices | Channel A and B fail independently with p=1/2 each | 1 if each alternative is individually feasible |
| Alias | Two names, one physical delivery mechanism | Event A disables both actions; event B is inert | 0 |
| Common cause | Two distinct physical channels with shared upstream dependency | A and B fail independently with p=1/2, plus a p=1/4 common event disabling both | 0 |

The event incidence in the [R1 FaultOntology](../experiments/fault_ontology_r1.py) is *identical* to the declared executed fault semantics. No new independently failing mechanisms are invented to force a positive feature result. Physical identity is **assumed**, not established by real-world measurements. The standard minimum event cut is reported alongside the proposed R1 event-disjoint support-pair indicator.

## Exact expected developer-only outcomes

| Predeclared toy fixture | Kits | Preparation ticks | Scoped static R1 | Standard minimum cut | P(strict restoration given actual loss) |
|---|---:|---:|---:|---:|---:|
| Two independent devices | 1 | 2 | 1 | 2 | 1/2 |
| Two independent devices | 2 | 2 | 1 | 2 | 3/4 |
| Independent, rushed preparation | 2 | 1 | 1 | 2 | 1/2 |
| Two aliases of one physical device | 2 | 2 | 0 | 1 | 1/2 |
| Two devices with one common cause | 2 | 2 | 0 | 1 | 9/16 |
| Independent failure events, but no kits | 0 | 2 | 0 | 0 | 0 |

These are *exact fixture calculations*, not sampled field recovery rates. For the one-kit and two-kit systems, the static R1 indicator and minimum cut are identical, even though resource-feasible fixed-policy restoration differs. For the common-cause case, the explicitly independent toy basic events give a success probability of 9/16. This is ordinary reliability arithmetic, not a new physical theory.

R1 uses individually feasible [G1](../experiments/p1_gate1.py) causal plans under a narrow [R1](../experiments/fault_ontology_r1.py) event scope; it does not assert the simultaneous preparability of both plans. The R7 policy execution establishes the separate resource-sensitive strict-restoration result.

## A bounded standard known-model reference — NOT full parity

The R9 standard full-model reference enumerates realized scenarios and applies the same fixed R7 non-anticipative policy. One **abstract work unit** is one evaluated R7 policy time step (including the final observation tick). Full coverage returns the exact rational conditional restoration rate.

With insufficient budget, the evaluator must report a rigorous **lower/upper probability interval**, never a fake exact probability. The lower bound is probability mass already known to restore; the upper bound adds all unexamined mass. These bounds apply only because EVERY fixture scenario removes the initially held target, ensuring the conditional denominator is exactly one. The function rejects a more general risk set, where separate numerator/denominator bounds would be necessary.

**No equal CPU, wall-clock, or RAM budget is enforced across G1/R1 feature enumeration and R7 policy evaluation.** Static plan enumeration, fault ontology assembly, policy rule scans and independent verification are not charged as equivalent work units. The historical independent R7 oracle runs outside the reference budget purely for software auditing. This is a rigorous bounded *partial-enumeration* contract, not yet a fair end-to-end H1 benchmark.

## Reproduction and implications

    python -m unittest tests.test_p1_r9_physical_controls -v
    python -m experiments.p1_r9_physical_controls --output r9_physical_controls.json

[Source](../experiments/p1_r9_physical_controls.py) · [tests](../tests/test_p1_r9_physical_controls.py) · [CI workflow](../.github/workflows/r9-physical-controls.yml). All six fixtures and their expected exact results are predetermined; no TRAIN/TUNE data are refitted and no sealed H1 test examples exist.

**Next gates:** independently defensible physical fault identities and shared causes; a resource-feasible representation that is invariant under legitimate model refinements; an actual all-in common compute/time/memory contract including feature computation and strong conventional augmented-state/reliability baselines; fixed policy, sensors and truly independent validation. Neither H1 nor scientific independence is established by R9. Keep Issues #3 and #8–#12 OPEN.


## Executed fixture verification — 2026-11-01

The initial [R9 fixture CI execution](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/actions/runs/41299575144) **passed** all 19 focused R9 tests and exactly matched the six predeclared fractions in the table above. **28 independent R7 full-history oracle comparisons** were completed across the six fixtures; these are nested synthetic scenario checks, not 28 independent sampled physical systems. The [R9 exact archival results](R9-physical-controls-results-20261101.json) include the individual route measures, full-model exact probabilities and strict lower/upper probability intervals obtained after a two-scenario work budget.

A separate manuscript integrity check initially failed because the PR branch was accidentally built from a tree missing five previously merged R8 files. **That unrelated branch-tree regression was corrected** by rebuilding R9 changes on the complete latest main tree, preserving the R8 source, test, CI workflow, scientific report and numeric archive. The corrected PR is being rechecked before any merge; no loss of historical files is acceptable.

The six constructed results are consistency checks, not evidence that independently verified physical mechanisms exist or that the proposed feature improves out-of-sample predictive performance. The exact work bounds remain charged in artificial R7 timeline-tick units only, without cross-method CPU/RAM parity.
