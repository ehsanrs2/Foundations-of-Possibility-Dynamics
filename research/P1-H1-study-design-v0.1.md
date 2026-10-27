# P1/H1 prospective predictive study: design candidate v0.1

**Date:** 2026-10-27. **Status: DRAFT — NOT PREREGISTERED.** There is no confirmatory P1 outcome and no test of H1.  
[Machine-readable specification](p1_h1_design_candidate_v0_1.json) · [pre-execution audit](../experiments/p1_protocol_audit.py) · [power sensitivity code](../experiments/p1_sample_size_sensitivity.py).

This is a design response to the open scientific Issues #3, #8, #9, #10, #11 and #12. It does not close any of them. It preserves the criticism that raw GBR may encode a false physical backup and that exact deterministic GBR contains no new information beyond its full input model.

## 1. Central falsifiable claim

**Prospective H1:** a physically scoped, strictly pre-failure structural constructible-backup feature improves **held-out prediction** of actual strict restoration under a non-anticipative executable policy, above ordinary topology, dynamic reachability and fault-event cut/redundancy features, within identical input, model-capacity and computation budgets.

**H0:** no positive mean held-out reduction in primary prediction loss under these conditions. Even a positive result would show bounded predictive feature utility **on the tested families**, not a new mathematical object, an independent natural law or a causal intervention effect. See the [novelty audit](novelty-audit-v0.3.md).

## 2. Pre-shock prediction and strict restoration endpoint

Unit of independent sampling: **system instance i**, not repeated failure outcomes within one system. Specify the initial resource stock, capability/action dependency structure, legitimate basic-fault ontology, target set and one common evaluation policy **before fault realizations are drawn**.

Each rollout j records whether the goal was held just BEFORE its realized shock, removed BY that shock, and reestablished by the fixed deadline on the **same policy trajectory**. Candidate binary outcome Y_ij equals 1 if a genuinely lost goal is regained, 0 if genuinely lost but not regained, and **undefined** if no such loss took place. A surviving or never-before-reached goal does not count as restored. Retention, availability, cost and recovery duration are separately descriptive.

A predictor p_i must be emitted **before observing which shock occurs**. It may use the same predeclared scenario prior and raw pre-shock data as its baseline, but not any realized shock ID, future action or outcome. The evaluation policy and its observation filter must be identically fixed for both predictors; otherwise policy-dependent selection into actual loss can contaminate the prediction comparison.

The proposed primary per-instance score is **mean Brier loss over eligible fault rollouts**, then paired between candidate and baseline and averaged across independent eligible system instances. Systems with zero eligible actual losses have an **undefined conditional target**: report their frequency by family and never silently score them 0 or 1. If selection is excessive or eligibility depends strongly on policy, revise the design BEFORE using confirmatory holdouts.

## 3. Candidate feature has NOT been certified

One proposed primary candidate feature is **R1 scoped pair before shock**, based on two individually feasible causal plans whose *declared* physical basic-event footprints are disjoint. This is a descriptive candidate, NOT a validated replacement for raw GBR.

- Mechanism identities, physical failure events, exposed vs protected components and their justification must be specified before examining outcomes. Two rule names never suffice as evidence of independent equipment.
- A path with incomplete event coverage is **unassessable**, never automatically zero or independent.
- Individual path feasibility is not simultaneous resource-feasible preparation. [R2](R2-resource-policy-bridge.md) demonstrates this by construction.
- Exact feature computation, rule equivalence, consumable inventory semantics and versioned source must pass independent review before any primary H1 study. GOG and feature repairs stay exploratory unless preregistered separately.

## 4. Equal-information strong baselines

Both feature arms receive identical full pre-shock raw input models X, physical fault event incidence, distributions, stock, deadlines and resource limits. The candidate feature is a deterministic function of X; therefore its potential advantage is **only** a finite-data, finite-capacity or time-limited representation advantage.

At minimum the baseline suite must include: topology/AND-OR arity and resource reserves; non-generative resource-bounded reachability; physical event minimal cut/hitting set and redundant path measures; and when computationally feasible **standard augmented-state non-anticipative control**. Keep full-information *clairvoyant* results labeled as diagnostic bounds, not fair equal-information baselines.

The same learner family, fitting/test data, hyperparameter budget, raw inputs and total wall time/RAM must be offered to the baseline and plus-feature arms. Feature-computation cost counts. An exact full-information model that computes expected restoration optimally may leave no theoretical information gain for R1; a null result against it is informative.

## 5. Proposed separated generator families — names, NOT datasets

| Partition | Proposed family | Designed stress |
|---|---|---|
| Train | Random AND/OR | prerequisite arity and candidate recipes |
| Train | Modular clusters | within/between-cluster alternatives |
| Train | Hub dependencies | shared critical prerequisites |
| Tune | Temporal bottleneck | deadlines and constrained preparation |
| **Sealed test** | Spatial lattice | locality and route distance |
| **Sealed test** | Hierarchical common cause | correlated physical failure units |

These six **labels are placeholders**. Actual generative rules, sizes, costs, physical event construction, independent seeds, inclusion criteria and representative diversity remain unimplemented. Distinct labels do not prove independent real-world domains. Do not inspect sealed-family outcomes or use their seeds during exploratory fitting. Pilot samples must be strictly segregated and never recycled as untouched test cases.

## 6. One primary statistical comparison

For eligible system i, let L0_i and L1_i be its baseline and augmented mean eligible-rollout Brier losses under the SAME shocks and SAME policy. Set D_i=L0_i−L1_i. A positive held-out mean D favors the candidate. Report family-specific D and the paired mean over the **specified eligible-system test population**.

Repeated rollouts within a system do **not** increase independent sample size. Any clustered uncertainty procedure must resample complete systems within held-out family strata and be preregistered. The chosen CI construction, inference rule, minimum practical improvement, prediction model and timeout treatment remain unfrozen. One primary feature comparison only; all other predictors, endpoints and feature ablations remain exploratory.

Adversarial negative controls must include duplicate physical aliases, missing shared faults, scope sensitivity, deadline/kit bottlenecks, feature access to hidden actual shocks, and training-only feature permutations. Null results, failures and timeout cases must be retained.

## 7. Power and precision: honest sensitivity, NOT sample selection

We have **no observed independent-system paired-loss SD**, no calibrated practical effect threshold and no estimate of eligibility rate. Therefore a final confirmatory sample count **cannot yet be justified**. A purely hypothetical normal approximation for independent paired *system-level* losses, with two-sided alpha .05, target power .80 and known SD s, requires about n = ceil(((z_0.975+z_0.80)*s/delta)^2).

| Hypothetical paired SD | Improvement .01 | Improvement .02 | Improvement .03 |
|---|---:|---:|---:|
| 0.05 | 197 | 50 | 22 |
| 0.10 | 785 | 197 | 88 |
| 0.15 | 1,766 | 442 | 197 |
| 0.20 | 3,140 | 785 | 349 |

These counts are **NOT a preregistered sample size or proof of adequate power**. They ignore family shifts, random eligible denominators, SD estimation, unknown effect and potential within-family heterogeneity. The final n and allocation across independent families require exploratory TRAIN-only pilot dispersion estimates, a scientifically justified improvement threshold, and independently reviewed cluster-stratified power/precision planning.

Reproduce sensitivity table with python -m experiments.p1_sample_size_sensitivity.

## 8. Explicit freeze blockers, all unresolved

1. Evidence-based physical event ontology or carefully declared synthetic ground truth and event correlations;
2. final resource-aware structural feature and equivalence assumptions (or an explicit declared static-feature hypothesis);
3. actual executable policy implementing observation-only non-anticipation and conditional strict restoration;
4. full generator implementations/distributions and sealed seed registry, without test outcome inspection;
5. preplanned handling of no-loss systems, eligible risk-set selection and goal weights;
6. strong standard baselines implemented with identical access and a fixed compute/memory/timeout budget;
7. independent generator-family system count, estimated variability, effect floor, power and family-wise allocation;
8. fixed primary loss/learner, CI, significance, negative controls and treatment of repeated rollouts;
9. independent tiny-system oracle, no-lookahead tests, artifacts and environment checks;
10. critical independent protocol review and immutable protocol lock date/commit **before** generating test outcomes.

The machine-readable design deliberately carries **DRAFT_NOT_PREREGISTERED**, null system counts and explicit blockers. Its audit program refuses a status change made by renaming the JSON field. Passing such checks is **internal specification consistency**, not a scientific preregistration.

## 9. Decision boundary

Only after all blockers are resolved should a versioned, reviewed, hashed P1 registration be created; then can actual held-out tests be run. A positive H1 under these restrictive conditions supports a bounded representation claim, not causal resilience. If the registered study finds no advantage or a trivial effect, document that failure in the book and do not move the goalposts.

See the [claims ledger](claims.md), [protocol history](protocol.md), and [separate predictive vs causal estimands](../appendices/D-predictive-estimands.md). **There are no P1 confirmatory findings in this version.**


## R3 implementation addendum — draft status unchanged

The [R3 policy rollout](R3-nonanticipative-strict-restoration.md) implements **one candidate operational endpoint**: actual loss at a fault boundary and later reacquisition by the same bounded deterministic policy history, with no advance access to the fault time or realized identity. Per-goal no-loss cases remain undefined and their probability mass is reported. R3 compares two separate execution procedures for tiny cases; it does not select a scientifically justified *final* policy, handle delayed observations, establish the physical fault-event ontology, generate independent train/tune/test families, freeze sample size or fit a predictor. **The prospective protocol remains DRAFT_NOT_PREREGISTERED and no H1 analysis is permitted.**


## R4 development implementation addendum — study NOT frozen

[Development-family boundary R4](R4-development-family-boundary.md) now gives small executable generation grammars for the three proposed TRAIN and one TUNE families only. The two SEALED test families remain unimplemented and ungenerated, with API calls explicitly rejected. A fixed seed derivation provides reproducible **developer** system units, four nested synthetic shock cases per system and whole-trace R3 checks. These outcomes are not independent held-out results, training of the H1 learner, estimates of out-of-family predictive advantage or evidence of real-system independence. The final policy, complete generator-family specifications, test seed registry and sampling frame remain open; the prospective protocol stays DRAFT_NOT_PREREGISTERED.
