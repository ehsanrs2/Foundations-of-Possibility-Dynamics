# R8 — Development-only predictive baselines versus a physical-scope R1 feature

**Status: exploratory TRAIN/TUNE comparison, NOT preregistered, not H1 validation, not proof of novel science.**

## Scientific question

The long-standing H1 question is whether a physically grounded backup feature adds *held-out, bounded-compute predictive utility* beyond ordinary network, fault-cut, stock, and dynamic-model features. Prior R0–R7 audits verified parts of simulation logic but did not actually train an equal-input predictor or evaluate the candidate against a conventional predictive learner.

R8 makes a cautious **developer-only** first comparison. It is designed to expose feature degeneracy, missing physical coverage, and whether a deterministic extra feature yields any *incremental development-side* Brier reduction. Negative or zero effects must be reported. It does not use the two proposed sealed generator families.

## Population, risk set and endpoint

- Three small R4 **TRAIN** grammars with 24 independently seeded artificial system instances each; one temporal-bottleneck **TUNE** grammar with 12 instances. Source seed 20261101; no construction of spatial_lattice or hierarchical_common_cause sealed families.
- The same stipulated R6 per-system hazard law and the same R7 perfectly observed (but not event-announced) fixed evaluation policy are used for both learner arms.
- Each system's conditional label is the **exact model-known probability of reacquiring service after actual fault-caused loss on that same R7 history**, marginalized before knowing the realized future shock, not an observed empirical label.
- Systems with zero loss probability have an **undefined** conditional label and are excluded from conditional model fitting/scoring, with their count reported.
- The sampling unit is a **system**. Multiple fault cases are only integration points nested within it, not independent observations.

The exact per-system pre-shock conditional target is

\[
p^*(X)=
\frac{\sum_{\omega}w_{\omega}L_\omega R_\omega}
{\sum_{\omega}w_{\omega}L_\omega},\quad \sum_\omega w_\omega L_\omega>0.
\]

The expected Brier score of a prediction q on that *known model* is exactly

\[
p^*(1-p^*) + (q-p^*)^2.
\]

This avoids Monte Carlo noise but also means the experiment is **synthetic-model approximation**, not empirical predictive validation.

## Baseline, candidate and provenance

The conventional baseline uses identical source model and prior hazard inputs X: horizon; initial kit inventory; action and prerequisite counts; generative/repair rule counts; source capability count; *individually feasible* causal plan count with and without construction; scope-aware standard **minimum event hitting/cut size**; indicators of missing event coverage; and prior probabilities of the three stipulated R6 basic events.

A naive R1 feature based on two "independent named routes" is not acceptable. R8 restricts a declared [R1 physical fault ontology](../experiments/fault_ontology_r1.py) to **one modeled common upstream-dependency event**, which deletes base or hub in the relevant R6 grammar. This incident is shared by all routes needing that mechanism. All other action/source elements are **assumed protected only within this narrow synthetic event scope**; no fabricated distinct-channel failure events are introduced. In particular, R6 service loss and kit destruction are **not** quietly renamed as individual route failures.

An R1 support computed from a static G1 causal plan in this single-event ontology gives a binary **scoped backup pair** only if fault-event incidence is adequately covered; unassessable event-free paths remain **missing**, with an explicit coverage flag already present in the baseline. The static G1 model removes initially held service before enumerating potential re-construction routes, and uses G2 action requirements, one-tick durations and *individual* kit costs. **It is not an executable post-fault plan under simultaneous shared resources**; R2's warning still applies.

The baseline **already includes** physical min-event-cut and independent-plan-count summaries from the same model; the augmented arm receives *those same inputs* plus only the proposed binary R1 indicator. This tests representational utility rather than hidden extra source information.

## Fitting and evaluation

Both arms use the **same deterministic Gaussian-elimination ridge linear-probability learner**, penalty 1.0, training-only standardization, identical eligible TRAIN systems and the same 12 designated TUNE systems. Predictions are clipped to [0,1]. These are fixed *developer implementation* choices, not a registered H1 learner. We do not tune penalty/architecture on TUNE outcomes and do not report p-values or confidence intervals for H1.

The expected conditional Brier scores of each arm are paired **by TUNE system**. The system-level mean of baseline minus augmented loss is the descriptive incremental value (positive favors R1). The exact full-known-model p*(X) is always shown as a separate theoretical lower bound, **not** a resource-budget-matched competitor. All features are constructed from the same pre-event source and declared hazard priors, never the realized shock ID or future policy trajectory.

A bounded complexity control rejects models with more than 10 actions or more than 256 enumerated static support plans. The program measures wall time for shared static feature derivation and separately for each model's fitting/prediction. **These are measurements, NOT enforced equal wall-time/RAM caps.** It would be false to claim a definitive equal-computation H1 comparison. Likewise, an ordinary ridge learner is not an adequate substitute for the entire conventional enhanced state-space baseline suite in the prospective P1 protocol.

## Reproducibility

    python -m unittest tests.test_p1_r8_dev_predictive_baselines -v
    python -m experiments.p1_r8_dev_predictive_baselines --seed 20261101 --train-n 24 --tune-n 12 --output r8_dev_only.json

The [R8 workflow](../.github/workflows/r8-development-baselines.yml) produces a short-lived **development-only** raw JSON artifact and a public summary. Any release archived summary must separate stable scientific descriptors from environment-dependent runtime measurements.

## What to conclude from this gate

If the R1 feature is constant or missing across these small grammars, a standard learner cannot derive a meaningful incremental signal from it. The correct conclusion is then **feature/ontology non-discrimination in the available developer populations**, not empirical disproof of a repaired or differently scoped feature on other systems. Inventing new independent route failures to produce a favorable R1 score is forbidden.

If a development gain appears, it must not be described as H1 validation: TUNE families were viewed during code and feature development, risk-law probabilities are human-chosen, and stronger standard baselines (bounded full augmented-state policy/reliability learners) remain absent. The final confirmation requires fixed domain evidence for physical identities, independent test units, a frozen policy and model family, training/feature compute budget, learning/tuning protocol and preregistration.

Reviewer Issues #3 and #8–#12 remain open regardless of R8 development results. No changes to the original R3–R7 reports or their archived numerical results are necessary.


## Executed R8 developer-only comparison (2026-11-01)

The [R8 workflow run](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/actions/runs/41296607466) completed successfully, including the dedicated regression suite and exact R7 full-history checks. The stable [R8 summary JSON](R8-development-summary-seed20261101.json) retains the measured numerical results; raw, environment-timed per-system outputs remain in the workflow artifact (short retention).

**Independent developer system units:** 72 TRAIN systems (24 each from three training grammars) and 12 TUNE temporal-bottleneck systems. Exactly **63 TRAIN** and **9 TUNE** systems had positive goal-loss eligibility; **12** systems in total had zero risk and are NOT counted as failures. There were **858** whole-history R7-vs-independent-oracle comparisons across nested scenarios, not 858 independent samples. Sealed-family generation remained zero.

**Principal descriptive result on the 9 eligible TUNE systems:**

| Predictor / reference | Mean exact conditional expected Brier |
|---|---:|
| Standard ridge probability model, ordinary topology/stock/fault-cut features | **0.182841176250** |
| Identical ridge model + narrowly scoped R1 pair | **0.182841176250** |
| Known full-model R7 marginalized probability (unbounded ideal reference) | **0.126302083333** |
| Difference, standard minus augmented | **0.000000000000** |

The baseline and augmented arm were trained on exactly the same eligible TRAIN systems, with identical learner, prior hazard distribution inputs, topology/resource context and feature scaling. The R1 indicator was **defined and equal to zero in ALL 84 development systems**: 79 assessed as SCOPED with no two event-disjoint causal supports, and 5 with NO_FEASIBLE_PLAN in the translated *individual-route static G1 representation*. Therefore it has **no empirical variation** here, so a deterministic linear learner cannot extract an incremental R1 effect. This is a model/ontology construct-validity failure in the current synthetic grammar, **not** a confirmation of H1 and not a formal refutation of all possible constructive-option representations.

**Do not change the physical fault-event scope post hoc to manufacture independent paths.** The one upstream event modeled by R6 applies to every restoration route's common prerequisite in these grammars. An invented independent repair-channel fault would contradict the stipulated experimental semantics.

**Limits:** only nine eligible TUNE systems, fully artificial label probabilities computed from known model rules, no real observed outcomes, no confidence interval or external replication. An exact *full-model* Bayes marginal is an ideal reference and has not been given the same runtime/memory cap. Ridge comparison records computation times, but **there is still NO enforced equality of CPU, wall-time or memory budgets across the required advanced baselines**. No conclusion that GBR is redundant in every system is warranted.

**Practical next gate:** the current development-family generators and independent physical failure scopes must be re-evaluated *prospectively* for meaningful and independently justified feature variation, while simultaneously implementing time-/resource-matched conventional dynamic state and reliability predictors. This should be a new exploratory design revision, never a retrofit of the R8 negative result into a positive H1 claim. P1 remains DRAFT_NOT_PREREGISTERED.
