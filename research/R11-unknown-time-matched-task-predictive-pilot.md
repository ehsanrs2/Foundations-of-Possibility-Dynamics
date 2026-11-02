# R11 — Unknown fault time, identical predictive objective and enforced limits

**Status: exploratory synthetic parameter-grid development, not H1 preregistration, not independent held-out validation. 2026-11-02.**

## Motivation

R8 produced a negative developer result: physical-scope R1=0 across 84 tiny systems and no incremental expected Brier improvement. R9 proved that static individually feasible routes can fail joint kit/deadline readiness, and R10 built an exploratory executable readiness indicator **exactly equivalent to ordinary augmented-state reachability**. R10 enforced per-process Linux limits but compared methods that calculated *different quantities*, so it could not support a predictive claim.

R11 moves the comparison to an **identical forecast target, same synthetic training/evaluation settings, same fixed learning algorithm, same source information, and the same enforced process ceilings**. It also removes the assumption that the controller knows the future event time, but remains a small model with a **known event-time prior**. A fair predictive comparison is possible as a *software exercise*, not as an independent scientific H1 test.

## One non-anticipating task with unknown event time

Every model initially holds a service. At **one unknown future time** tau=1 or tau=2, the modeled fault genuinely deletes service. The system's fixed R7 policy sees current capabilities, stock, known disabled actions and an observed state-change latch **only after** the fault; it does not see tau or event identity beforehand. The declared probability of tau=1, alpha, is known to all predictors *before* either event. Tau=2 has probability 1-alpha. A shared final horizon of tick 3 provides a consistent endpoint regardless of which event time occurs.

For each synthetic physical mode (independent channels, aliased identity, common-cause), each kit count (0,1,2) and each alpha in {0,1/4,1/2,3/4,1}, run the ordinary stipulated R9 basic-fault distribution and fixed R7 policy. Each world has **actual** goal loss, and conditional strict restoration on that same executed policy history is scored exactly using rational case weights. There is NO no-loss denominator ambiguity *within this restricted R11 set*; broader natural risk populations still need a different design.

The resulting grid has just **nine distinct base physical configurations**, each repeated at **five pre-event time priors**. The 27 training settings are the same nine configurations at alpha {0,1/2,1}; the 18 tuning settings reuse those same configurations at alpha {1/4,3/4}. Consequently **there are ZERO independent held-out systems**. The number 18 is NOT the number of independent scientific test units. Treating this grid as external generalization evidence would be invalid.

## Same fixed predictive objective and three model arms

All methods receive the identical pre-fault declared source information: kit stock, physical mode identity, event cut, static R1 backup count, and the early-event probability alpha. All use the **same training-only feature standardization**, same deterministic Ridge linear-probability model with fixed penalty 1.0, and same training/tuning partition; no hyperparameter or event ontology is tuned to improve outcomes.

The three actual prediction tasks have a common label and expected conditional Brier endpoint:

1. **raw**: familiar model structure, hazard and basic fault-cut features without the new R10 candidate.
2. **standard_dp**: exactly the same raw inputs plus *prior-weighted joint preparedness* computed by conventional augmented-state DP under the declared hypothetical event times.
3. **independent_history**: exactly the same raw inputs plus an *identical* prior-weighted preparedness feature computed by an independently implemented exhaustive action-history algorithm. This is an alternative conventional algorithm, **not** extra physical information.

All three estimators face identical expected Brier loss on the same 18 repeated toy parameter settings. The standard DP and independent-history columns are expected to be identical; this direct **negative novelty control** tests whether the candidate is anything more than familiar finite reachability.

For every setting the added feature is computed before knowing the realized tau or channel failure: it averages the readiness of one feasible shared-stock prefix at tau=1 or tau=2 using the pre-declared prior weights. For an independent two-kit system, readiness is exactly 1-alpha; for one kit, aliases and common-cause worlds, the event-disjoint jointly ready indicator is zero. Note that the feature reflects a **known prior and a fixed known action grammar**, not observed physical sensor data.

No learner gets future case identity, future simulated event truth or the model-derived exact conditional answer as an input feature.

## Scoring and comparator

The synthetic exact R7 target p*(X) is obtained by full scenario marginalization under the common unknown-time distribution. A predictor q receives the mathematically exact **model-expected Brier**

\[
p^*(1-p^*) + (q-p^*)^2.
\]

It is computed using declared simulator mechanics and serves as an unbiased deterministic scoring reference **within this model**, not as an independently observed field outcome. The exact known-model ideal p*(1-p*) is also shown as a **separate, not resource-matched Bayes reference**. No uncertainty interval, p-value or claims about real systems can be generated from these heavily reused toy configurations.

## Enforced all-in computing limits

Unlike R10's different-output comparison, **each of the three R11 worker processes performs the same end-to-end prediction task**: simulate the known synthetic target for its settings, build only that arm's features, fit the same Ridge model and return the forecasts and expected Brier. All three are started in fresh Linux processes with *identical* 5-second wall deadlines, 5-second RLIMIT_CPU and 256-MiB RLIMIT_AS limits.

This is now a meaningful **same-resource-ceiling comparison of these three particular predictors**. However, identical ceilings are NOT identical actual work, identical model size (the extra feature adds a parameter), or a universal proof of equal computational budget. Both augmented methods have more computational work and one more input feature than raw. Importantly, source-known target generation is performed in **every** worker; independent correctness history verification is separately audited *outside* the constrained fit process. All-in wall, CPU and peak RSS are measured but not treated as deterministic cross-machine quantities. RLIMIT_AS limits virtual address space rather than directly capping resident memory.

No sophisticated bounded augmented-state predictor, full policy optimizer or broader conventional reliability learner has been included. The exact model-known p*(X) remains a theoretical lower bound rather than a same-budget competitor.

## Reproduction

    python -m unittest tests.test_p1_r11_unknown_time_prediction -v
    python -m experiments.p1_r11_unknown_time_prediction --output r11_all_in_predictions.json

The [dedicated R11 Actions workflow](../.github/workflows/r11-unknown-time-prediction.yml) runs these tests and the three genuinely capped predictive tasks. It uploads the complete per-setting and timing information as a **development-only** artifact. A separately archived stable JSON removes nondeterministic CPU, wall-time and RSS observations.

## Interpretation constraints

Any improvement of either engineered readiness column over raw is **development-side feature engineering on nine reused synthetic configurations**, NOT confirmation of H1 or a new science. Agreement of the standard-DP and independent-history variants is expected because they calculate precisely the same state-reachability property. A negative result is equally informative; no post hoc change to R8's physical fault scope or the R11 train/tune prior split is permitted.

**Unresolved:** independent physically sourced event ontology; real or calibrated failure observations; partial/noisy sensing; shock-time distributions identified from field evidence; nontrivial resource-aware variation across true independent system families; a strong conventional matched-capacity prediction suite; power/sample-size design; truly untouched sealed families and preregistration. H1 stays DRAFT_NOT_PREREGISTERED; Issues #3 and #8–#12 remain open.


## Executed developer comparison — 2026-11-02

The initial [R11 GitHub Actions run](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/actions/runs/41416005089) passed its 24 focused tests, all three bounded same-objective predictive workers, and **384 complete independent chronological R7 trace comparisons**. The [raw resource and prediction artifact](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/actions/runs/41416005089/artifacts/13127906509) records environment-specific elapsed wall/CPU/RSS as well as per-setting outputs. The [stable archived R11 summary](R11-unknown-time-prediction-results-20261102.json) excludes variable timing/RSS and retains the exact same model scores and cases.

| Fixed learner on 18 *reused* TUNE parameter settings | Mean model-expected Brier |
|---|---:|
| Raw familiar physical mode/stock/mincut/hazard features | **0.163607515992** |
| Raw + prior-weighted joint backup from ordinary augmented-state DP | **0.163115603693** |
| Raw + the SAME backup feature from independently enumerated histories | **0.163115603693** |
| Model-known exact Bayes lower bound, NOT a fitted equal-budget competitor | **0.162407769097** |

The **descriptive raw-minus-augmented gain = +0.000491912299** expected Brier units on the toy TUNE parameter grid. It is not a claim about independent holdout prediction, physical robustness or statistical significance. The standard DP and independent-history augmented arms produced **exactly identical tune-setting forecasts and score**. The alleged feature's finite-model information content is therefore already in a standard augmented-state calculation, so this pilot provides **no evidence of independent scientific novelty**.

The basic model has exactly **nine distinct hand-designed physical structures** repeated at five prior weights; the 27 TRAIN and 18 TUNE rows reuse their structures. Consequently no valid independent-system standard error, generalization estimate or confirmatory H1 claim is available. Every simulated outcome is derived from known synthetic fault mechanics, not measured from a deployment.

**Computational gate:** all three worker jobs successfully completed with the same enforced 5s wall, 5s CPU and 256-MiB virtual-AS ceilings and the same deterministic Ridge setting. This is an equal *resource-ceiling and scoring* comparison of the three specified methods, not equal actual CPU consumption, equal feature dimension or a full contest against sophisticated conventional bounded-state prediction models.

**Next scientific step:** if this feature is worth proposing as an explicit prospective H1 variant, first define physically justified event ontologies and genuinely independent systems; preregister a distinct hypothesis and baseline suite, including strong conventional augmented-state predictors, without relabeling the original R8 null finding. P1 remains DRAFT_NOT_PREREGISTERED.
