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
