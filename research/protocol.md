# Protocol P1 — Testing generative options against resilience baselines

**Status: prospective protocol; no P1 experimental data have been collected.**

## Core estimand

Incremental out-of-sample predictive performance of candidate generative indicators for goal recovery after an intervention, beyond baseline graph topology, redundancy, resources and viable/reachable goal measures.

## Unit and sampling

Unit: independently sampled *system instance* with a capability dependency hypergraph, deterministic production rules, resources, horizon and target predicates. Generate families with controlled node count, prerequisite arity, degree distribution, density, costs and source availability. Split by **instance and generator family** before feature selection or hyperparameter tuning.

## Planned intervention groups

E0: static action/capability set, construction disabled.

E1: construction allowed with prespecified costs and prerequisite rules, otherwise matched to E0.

E2: construction allowed but subjected to ablations (correlated failures, resource bottlenecks, deadline constraints, and construction disabled after shock).

Ablations must avoid changing several confounders at once; explain when perfect matching is impossible.

## Outcomes

Primary: proportion of predefined goals recovered within a fixed horizon and resource cap after failure, across a fixed intervention distribution.

Secondary: time to first recovery, total resource usage, cost-adjusted recovery and reachable-goal retention. Register tie-handling, censoring and impossible-to-recover cases.

## Primary comparison

A baseline model with topology, standard path redundancy, min cuts, initial goals and resource reserves versus baseline plus GBR/GOG. Compare on held-out network families and never use outcomes to design feature computation. State the algorithmic cost of calculating every metric.

## Uncertainty and decision

Report differences in a prespecified predictive score (e.g. MAE for continuous recovery fraction), bootstrap intervals **resampled by independent system**, effect sizes, failure families, and sensitivity to horizon and budget. Publish null findings. Do not interpret a positive held-out score as proof of fundamentally new laws.

## Pre-execution checklist

1. Freeze precise graph/hypergraph semantics and failure units.
2. Freeze train/validation/test generator families and random seeds.
3. Freeze outcome definitions, baseline implementations, and primary metric.
4. Demonstrate that GBR does not look ahead at held-out faults.
5. Validate tiny networks by exhaustive plan enumeration.
6. Record environment, runtime, raw data and checksum manifests.
7. Execute; then publish all results and deviations from protocol.

No power calculation or sample-size justification has been performed yet; these must precede confirmatory claims.

## G0 verification status (completed, nonconfirmatory)

[G0](G0-verification.md) compares exhaustive enumeration with an independent mask/time solver for small bounded systems, including initial-component shocks: 256 comparisons, zero mismatches. The model does not implement GBR and cannot be used to claim H1. Subsequent P1 steps remain unexecuted.

[QuantConnect LEAN](../integrations/lean/README.md) was screened for eventual financial transfer but not used for the core P1 experiment.

## Gate G1 — bounded plan-support verification (software gate completed)

[G1](G1-verification.md) explicitly tracks initial-source and rule support in a sequential monotone production model, including scoped exposures and pre-run loss of initial components or rules. Complete sets of goal plans agreed between action-sequence DFS and rule-subset enumeration in **192 comparisons** from 48 small cases plus a faulted counterpart each; 13 dedicated checks exercise assumptions and counterexamples. **No P1 predictive data, calibration, held-out generalization or H1 testing were performed.**

To advance: independent oracle for causal-support extraction, consumable resources, dynamic shock distributions and fair strong baselines; preregister a meaningful sample size before any confirmatory analysis.

## G2 implementation status: bounded in-run shock and inventory (nonconfirmatory)

[G2](G2-verification.md) models durable capabilities, separately **consumable integer stock**, one discrete fault applied during the horizon at a time boundary, optional generation and post-fault existential goal availability. Exhaustive history DFS and layered state search are compared. The output is **not** a G1 causal-plan score or statistical recovery predictor. The 'post-fault availability' target includes surviving pre-existing goals, so strict recovery after loss will require separate trajectory history variables. Full P1 registration, strong baselines, family holdouts and H1 testing remain pending.

## Gate G3 — distinct outcome labels, not a preregistered P1 result

[G3](G3-verification.md) computes four history-consistent existential queries: post-fault availability, retention, strict restoration *only after actual pre-fault holding and fault-caused loss*, and joint post-fault attainability. The time-layer solver retains goals-lost-at-fault flags to avoid conflating histories with different restoration histories. An independent timed-history oracle and the original G2 full-state baseline provide comparison checks.

**Important confounder:** pre-shock planning has perfect knowledge of the deterministic future fault in these solvers. Results may depend on anticipatory actions that would not be feasible for a policy lacking advance notice. P1 must compare models under identical information sets and non-clairvoyant policies; G3 cannot justify a resilience-prediction claim.

## Gate G4: the pre-shock information boundary

[G4](G4-verification.md) introduces a *shared, non-clairvoyant pre-shock action prefix* and fully observed scenario-adapted recourse after a **known** deterministic shock boundary. Exact probability-weighted joint post-shock success is computed under a finite rational scenario distribution. A clairvoyant full augmented-state comparator provides an information-theoretic **upper bound** within this model. These are exact small-model calculations, **not** a statistical comparison of GBR.

The remaining scientific tasks require explicit uncertainty/observation semantics, resource-sensitive causal support and a frozen full-information/equal-information baseline. The main P1 sample-size justification, held-out family splits and GBR predictor fitting have not yet been performed.


## Reviewer-critical gate before any P1 freeze

The [novelty audit](novelty-audit-v0.3.md) and [metric audit](gbr-metric-audit-v0.3.md) establish why the protocol cannot yet be frozen: GBR depends on an externally evidenced physical-fault identity map, exposed set F, plan-equivalence convention and deadline/resource semantics. Baselines must receive **identical raw inputs** and all feature-computation cost must count within the declared budget. The primary non-clairvoyant policy-trajectory endpoint, strict loss/recovery denominator, generator holdouts, sample size and loss function must be frozen *before* confirmatory data collection.

G1's raw plan metric remains a **candidate under review**, not a validated predictor. This audit adds deterministic counterexamples only; it does not complete #3, #8, #9, #10, #11 or #12.

## R1: physically scoped failures and pre-freeze estimands

The [fault-event contract](../appendices/C-fault-event-ontology.md) requires a justified physical mechanism map, basic fault-event incidence, written assumptions about protected dependencies, and scope sensitivity *before* interpreting structural independence. The [prospective estimand separation](../appendices/D-predictive-estimands.md) distinguishes nested-action reachability, bounded-learning prediction and causal intervention outcomes, with an explicit proposed loss-conditioned restoration target and risk-set selection warnings. The old raw G1 GBR formula is not silently rewritten. **Neither appendix constitutes finalized preregistration**; the physical ontology and a policy-conditioned resource-sensitive feature remain unvalidated.
