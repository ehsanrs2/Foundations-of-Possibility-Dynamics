# R16-J / C1-Runner v0 — Six actually executed, capped development comparators

**Date:** 2026-11-14. **Status:** MEASURED_DEVELOPER_REHEARSAL. No independent field data, no independent TEST systems, no preregistration or H1 result. This implementation advances [C1 protocol PR #40](R16I-C1-fair-benchmark-design.md) **without claiming to satisfy its full confirmation requirements**.

## 1. What genuinely executes

For all six arms, the worker constructs R9/R11 *actual* synthetic preevent models, computes a real feature rather than returning placeholder ledger entries, generates the identical R7 strict same-history actual-loss conditional target from the known synthetic model, standardizes using TRAIN only, fits a real deterministic ridge regression, predicts 18 tuning parameter settings and calculates conditional expected Brier. There are 27 train settings and 18 tune settings, **repeated from only nine handmade mode×kit structures**. No independent test split or field sampling exists. **TUNE is not TEST** and must not be renamed.

| Arm | Real computed 8th slot | Boundary |
|---|---|---|
| raw | constant zero | shared raw preevent covariates |
| topology | sum of ordinary action prerequisite counts | constant in this single R9 grammar, hence deliberately weak |
| resource_reachability | G2 finite-state resource-limited **constructive** reachability of at least one channel before hypothetical shock, prior-weighted over declared possible times | conventional existential one-channel quantity, **not** non-generative strict restoration or joint readiness |
| physical_event_cut | existing R9 event-min-cut from **stipulated toy physical footprints** | no real physical mechanism attested |
| augmented_state_dp | prior-weighted R10 ordinary augmented-state **joint-readiness** feature | standard DP preparedness, **not** exact best policy outcome probability |
| r1_scoped_pair_candidate | R9's static R1 scoped-pair indicator with declared toy event identity | the original candidate; do not substitute R10 readiness for R1 |

Every arm receives the same seven raw fields (kit stock, early-fault prior, 3 physical-mode dummies, 2 kit-threshold indicators) and **exactly one further feature slot**, with a fixed ridge penalty 1 and training-only standardization. The topology arm is necessarily constant given this one grammar and is not a strong structural baseline. Even if the conventional DP arm is competitive, **this is not the full cross-domain benchmark required by the C1 plan**. Physical fields are toy assumptions, not published fault ontology.

**Information rule:** The features can access the synthetic *pre-shock* grammar, mode/event-incidence assumptions, initial stock and prior for hypothetical fault times. They do not read the realized future event, its outcome, held-out labels or policy rollout. The target is independently generated from R7 synthetic histories for each setting and is only used by the learner for TRAIN labels / by the scorer for TUNE scores. No training on TUNE outcomes.

## 2. Actual cap enforcement and measurement

For **each method**, a parent launches a fresh Python process using Linux \`subprocess.run\` with \`resource.setrlimit\` applied before \`exec\`:

- hard virtual address-space cap (RLIMIT_AS) 256 MiB;
- hard CPU cap (RLIMIT_CPU) 8 seconds;
- parent-enforced wall deadline 8 seconds.

The exact caps are identical. The child includes imports, feature creation, synthetic target generation, standardization, fitting and prediction under those caps. The parent measures **end-to-end process wall ms** including import/startup, while child reports CPU ms counted after worker entry, and \`ru_maxrss\` peak KiB as reported on Linux. The worker also records phase-level feature / synthetic-target / fit / prediction wall timings. These are **actual measured quantities**, but vary with GitHub runner load, interpreter startup, OS, concurrency and hardware; never interpret tiny differences as a stable scientific speed advantage. The virtual address-space cap is not a hard RSS cap; peak RSS is recorded, not directly hard-enforced independently.

All non-PASS outcomes, including WALL_TIMEOUT, CHILD_FAILURE, SPAWN_FAILURE and invalid output, remain explicit. A missing/failed arm yields **NO_COMPARATIVE_SCORE**, not an apparent win for the surviving method. Exact baseline and R1 source/target identity must match across arms, and the parent checks the *same enforced budget*. No unsupported causal/novelty claim is generated. This is **one measured run per arm**, not a statistical timing study.

## 3. Scores and statistical limits

Each TUNE parameter row has the *same* exact R11 model-known conditional restoration probability \`p*\`; the score for forecast q is the expected Brier \`p*(1-p*)+(q-p*)²\`. Positive descriptive \`mean_Brier(DP)-mean_Brier(R1)\` would favor R1 **only on these repeated development parameter settings**. This is not a held-out effect estimate. The nine underlying physical configurations are reused across TRAIN and TUNE and the graph family is researcher-created. Neither 18 tune rows nor 9 base structures are independent physical field systems.

The output includes method-specific actual cost and forecasts; time measurements are deliberately not asserted to equal any fixed value in tests. A synthetic comparison cannot justify confidence intervals, statistical significance or arbitrary scaling. The historical R8 zero-gain result is preserved, even if this different development population gives another descriptive comparison.

## 4. Missing full C1 requirements and stopping conditions

**Full C1 status remains BLOCKED** because we have not:
1. independently sampled systems or a truly untouched TEST partition with group-disjoint structures;
2. externally verified physical fault event identity, resource and policy provenance, and independent time synchronization;
3. a competitive conventional **non-generative** resource reachability/control comparator at matched scope, scalable topology/cut methods and an adequately representative diverse grammar;
4. prospective registered effect floor, clustering/censoring inference and any independent critical review of the locked H1 feature;
5. independent field service-loss/reacquisition logs satisfying B7 rather than assumed synthetic labels.

The R10 DP in this measured rehearsal is a conventional joint-*readiness* feature, not a conventional optimal terminal-goal belief/POMDP outcome oracle. This matters for scientific comparison: an unrestricted exact full-input expected-outcome oracle may perform better and should be a separately labelled diagnostic ceiling.

**Stop on** timeouts, missing arms, changed raw input/target identity, unequal enforced budget, future-case leakage, or silent feature substitution; no score from incomplete comparison. On a reproducible null R1 gain or a stronger conventional method at equal cost, record a negative boundary rather than changing the hypothesis post hoc.

## 5. Reproduce and next work

    python -m unittest tests.test_p1_r16j_c1_runner -v
    python -m experiments.p1_r16j_c1_runner > c1-runner-measured-dev.json
    python -m unittest discover -s tests -v

Linux is required for hard cap execution and the CI workflow. The JSON retains executable scores, process caps and measured machine/environment metadata, but **not** a field-data or signed custodian receipt. Feature computation time is a subset of the end-to-end wall time, not the whole cost by itself.

Next **C2**: develop a genuinely independent structural holdout generator with predeclared non-overlapping families, strong conventional baseline semantics, system-level sample units, all-in cap treatment and negative-control power; freeze the study **before** any confirmatory holdout is generated. In parallel, B7 must obtain authorized instrumented real observations from an independent custodian. H1 remains **DRAFT_NOT_PREREGISTERED**, 0 confirmatory units and sealed test families untouched. Keep scientific Issues #3 and #8–#12 open.
