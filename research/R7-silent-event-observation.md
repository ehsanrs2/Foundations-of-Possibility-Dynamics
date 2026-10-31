# R7 — Silent no-effect fault boundaries and an observation-filtered policy

**Status: developer-only measurement/observation gate, not preregistered P1/H1 or evidence for a new theory.**

## The concrete model defect

[R6](R6-variable-risk-and-exact-baseline.md) independently sampled three *synthetic* basic-event indicators but inherited the G2/R3 representation of **one scheduled boundary**. Even if none of the event indicators materialized, R3 raised the observable Boolean fault_observed from that tick. This leaked an artificial boundary signal into the policy. It was not future shock-type knowledge, but was **an unrealistic indication of an incident with no observable effects**.

R7 implements a NEW opt-in policy executor. Historical R3–R6 executors, published counts and original test contracts remain unchanged.

## R7 physical and observational semantics

Exactly one synthetic fault vector is specified at a hidden time tau; the vector can have no effect. Exogenous event truth is known to the *offline scorer*, not to the policy. The policy sees only its current capabilities, stock, **fully observable disabled-action set**, current clock tick and a persistent disruption-detected flag. It never sees the scenario ID, event vector or hidden boundary time.

The flag switches to true *only if application of the fault causes an actual observable difference*:

\[
D_\tau=\mathbf 1\{C_\tau^+\neq C_\tau^-\ \lor\
r_\tau^+\neq r_\tau^-\ \lor\
A_{\mathrm{disabled},\tau}^+\neq A_{\mathrm{disabled},\tau}^-\}.
\]

It remains true thereafter. Ordinary legal actions do **not** count as fault detection. An ineffective fault vector, removal of an unheld label, or attempted destruction of stock already at zero produces no change and **no notification**.

This remains **perfect-state sensing**, not realistic sensor noise, uncertain event attribution, partial or delayed detection, repeated faults or physical validation. Disabled-action status is assumed observable without probing.

## Strict restoration vs observation

Strict restoration labels still depend on **actual** fault-caused loss: the goal must exist immediately before the event, be removed by the event, and reappear by the deadline on that same trajectory. A no-effect case is never assigned restoration success or failure; it is ineligible for the loss-conditioned outcome.

Detection is not equivalent to goal loss: some kit faults are detected even when service is retained, while removal of an unheld token is not detected. Systems with no positive loss risk continue to have **undefined** conditional restoration.

## Independent verification and controlled counterexample

[R7 code](../experiments/p1_r7_silent_observation.py) contains separate immutable tuple/set and mutable set/dictionary executors. Each checks **complete tick histories**. The latter independently applies fault effects and implements fixed-priority policy selection; it does not call the first evaluator. Historical R3 execution is used only for the sensitivity comparison.

Negative tests cover null events, unheld deleted capabilities, exhausted stock, relabeled scenarios, changing the unobserved null-event time and zero-risk R6 distributions. Positive tests cover deleted goals, real stock destruction, disabled-rule changes, time boundaries and same-history restoration.

In a hand-built example, R3 observes a null event at tick 1 and chooses after-event priority action **alternate**. R7 detects no change and continues with pre-event **prepare2**. The goal is retained in both: the difference is an erroneous policy reaction, not a restoration-performance result.

## Developer-only paired audit

The R7 diagnostic reuses the **same 84 TRAIN/TUNE development systems** and stipulated hazard laws as R6 (seed 20261031; 24 per three training families, 12 tuning), with identical case weights. It reports independent system counts, silent boundary cases, changed policy-action histories and strict-restoration-label differences versus historical R3. All fault cases are **nested** within their system. The opt-in evaluator leaves original R3 and R6 results intact.

The two SEALED H1 families remain unimplemented; no actual held-out samples, physical failure observations, trained predictions, Brier advantage, causal effects or H1 inferences arise.

### Reproduction

    python -m unittest tests.test_p1_r7_silent_observation -v
    python -m experiments.p1_r7_silent_observation --seed 20261031 --train-n 24 --tune-n 12 --output r7_dev_only.json

The [R7 developer workflow](../.github/workflows/r7-silent-observation.yml) uploads developer-only traces. Following a passing audit, a numerical summary may be committed separately to preserve findings beyond artifact expiry.

## Remaining scientific gates

Correctly hiding a null boundary under perfect current-state observation is **necessary but insufficient** for realistic non-anticipative policies. Partial/noisy sensors, latent failures without immediate state changes, real fault ontology, multiple shocks, resource behavior and fixed fair compute baselines remain unresolved. The policy and H1 protocol are not preregistered. Keep Issues #3 and #10 open.


## Executed R7 developer-only diagnostic — observed results (2026-10-31)

The [R7 PR-head Actions run](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/actions/runs/41204329644) passed the 19 R7 tests and the complete paired developer audit. The [exact archived R7 summary](R7-silent-observation-summary-seed20261031.json) has **84** independent artificial systems and **820** complete paired R7-vs-independent-oracle history comparisons. **225** of the 820 positive-weight event-case records had no actual visible change at the scheduled boundary and were therefore silent in R7. These records are nested observations, NOT 225 independently sampled systems.

**A scientifically important negative outcome:** there were **zero action-history changes and zero strict-restoration-label changes** between R3 and R7 on the R6 developer family/priority-policy cases. The new detector *does* differ in the latent event-notification flag for ineffective cases. The fact that actions did not change in these specific tiny grammars is consistent with R4's priority structure: after-event restoration operations are unavailable while service remains held, so both priorities fall through to similar preparation operations. This explanation is model-specific, not a proof of universal behavioral equivalence.

The deliberately constructed [null-boundary counterexample](../tests/test_p1_r7_silent_observation.py) separately confirms that the incorrect R3 alarm **can change actions** in a different admitted model: at t=1 the old policy chooses alternate, but R7 chooses prepare2. Neither example shows an H1 predictive advantage or observed real-world fault-detection performance.

| R6 developer family | Systems | Mean exact probability of *unobserved* event boundary | Mean probability of action-history difference vs R3 |
|---|---:|---:|---:|
| random_AND_OR | 24 | 2653/6144 | 0 |
| modular_clusters | 24 | 359/768 | 0 |
| hub_dependencies | 24 | 695/1536 | 0 |
| temporal_bottleneck | 12 | 39/64 | 0 |

The zero label differences in these developer systems must be **reported**, not suppressed, and the old R6 archive remains valid under its own explicitly stated *boundary-observing* semantics. R7 is the recommended opt-in baseline for a future *perfect-state-observation* pilot, not an empirically validated sensing policy.
