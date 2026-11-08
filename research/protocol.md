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


## R2 pre-registration warning — physical backup is not an executable policy

A [hand-specified R2 control](R2-resource-policy-bridge.md) fixes physical event incidence and independent basic-event probabilities while varying kit supply and pre-shock time. The guarded R1 pair remains 1 for 1-kit and 2-kit feasible individual alternatives, but G4's optimal non-clairvoyant post-fault service probability varies from 1/2 to 3/4. A structural backup predicate is therefore **not a plug-in prediction of policy robustness**. Future H1 features must be defined *before observing test outcomes*, include their resource/time semantics, and face a resource-aware non-anticipative control baseline under identical information. R2 is NOT a frozen endpoint or an empirical study.


## Candidate P1-H1 study specification — NOT REGISTERED (2026-10-27)

The [new detailed design candidate](P1-H1-study-design-v0.1.md) proposes strict actual-loss restoration (not generic availability) as the binary rollout label, Brier loss nested within independent systems, **one** baseline vs plus-physically-scoped R1 candidate comparison, full augmented-state and failure-event cut-set controls, and matched pre-shock raw inputs/training/feature-computation budgets. A [machine-readable JSON draft](p1_h1_design_candidate_v0_1.json) lists six **unimplemented** generator-family slots and explicit preregistration blockers; its [software audit](../experiments/p1_protocol_audit.py) refuses accidental status promotion. [Hypothetical normal-approximation independent-system sample size sensitivity](../experiments/p1_sample_size_sensitivity.py) is **not an adequately powered final sample plan**. No confirmatory sampling, held-out training/test outcome or real physical failure mapping has occurred. Earlier P1 language calling recovery proportion the primary target is superseded **provisionally** by this stricter proposal, not by a frozen registration. Issue #3 remains open.


## R3 software gate — one non-anticipative executable history, NOT P1 registration

[R3](R3-nonanticipative-strict-restoration.md) supplies a small deterministic, fixed-priority evaluation policy that **does not see future fault time or realization**. It records actual pre-fault goal presence, fault-caused removal and on-the-same-trajectory restoration, with undefined results for no-loss rollouts. A second independently coded history evaluator checks per-tick states/inventory/action and the conventional G3 augmented-state solver supplies a *clairvoyant feasibility upper-bound* when restoration occurs. G2's action and resource assumptions still apply. One illustrative case has eligible mass 2/3 and conditional restoration 1/2; these are designed numbers, not observed H1 data. The **specific scientific evaluation policy is not frozen**, and this software correctness check does not satisfy the study's uncompleted registration/power/family/baseline gates.


## R4 development generator isolation — preregistration STILL OPEN

[R4](R4-development-family-boundary.md) implements only the three TRAIN and one TUNE generator-family placeholders from the [P1 candidate design](P1-H1-study-design-v0.1.md), using R3's fixed priority execution and four fully declared *developer* fault cases per independent system. Stable per-family/instance SHA-256 seed fingerprints permit exact reconstruction; traces cross-check against a separate procedural reference. The two proposed SEALED test families have identifiers but **no generators, random seeds, model instances or realized outcomes** in this software gate. This is a guard against accidental developer peeking, not a reliable security boundary. The design JSON remains DRAFT_NOT_PREREGISTERED with family_definitions_implemented=false. Test-family realization must await review of the outcome policy, feature ontology, sample-size and fixed comparisons.


## R5 developer-pilot gate — descriptive only, not P1 predictive evidence

[R5](R5-development-pilot.md) enumerates four R4 development-only scenario cases under three predeclared fixed non-anticipative policy variants for 24 systems per TRAIN family and 12 TUNE systems. R3 full histories are independently cross-checked, and a G3 augmented-state feasibility result is kept strictly separate as a *clairvoyant diagnostic*. Outputs contain eligibility, conditional strict restoration, resource/action use and nested-instance metadata, with downloadable raw JSON artifacts in CI. **Every instance has 3/4 eligibility by design, not by independent measurement.** The final generator-family distributions, R1 resource-sensitive feature, learning baseline, sampling/power and time/memory budgets remain unfrozen. The P1 JSON remains DRAFT_NOT_PREREGISTERED and no H1 result can be inferred.


## R6 pre-failure risk / baseline design gate — still UNREGISTERED

[R6](R6-variable-risk-and-exact-baseline.md) replaces the constant 3/4 developer-case loss risk with per-system externally **stipulated, independent synthetic** service/shared-infrastructure/kit basic-event indicators and early/late fault times. R3 full-policy histories are cross-checked against its independent implementation. The conditional restoration outcome is undefined when the actual-loss probability is zero. This is **not a sample of real-world hazard rates** and does not by itself justify power, selection or held-out population risk.

The R6 full-model pre-fault exact conditional expectation provides a standard **equal-information Bayes reference** for tiny known synthetic models; it cannot be beaten in population expected Brier loss by any deterministic feature of the same full input without additional information. For prospective H1, bounded computation and model capacity remain possible reasons engineered representations could help; they must be compared under frozen, fair budgets. The workflow produces only TRAIN/TUNE development outputs. The P1 manifest remains DRAFT_NOT_PREREGISTERED.


## R7 optional observation model — NOT a frozen evaluation policy

The [R7 semantics](R7-silent-event-observation.md) intentionally do NOT signal an externally specified fault boundary if it causes no observable change in currently held capabilities, stock or disabled operations. The policy can react only to observed post-event changes and cannot use a future event ID, time or hidden true loss label. In contrast, historical R3/R6 code visibly signaled all scheduled boundaries including no-effect vectors; those results remain recorded rather than overwritten. The strictly conditional restoration outcome is scored from the realized true loss on the same policy trajectory, separately from detection. This developer correction still assumes full and immediate observation; real sensing, preregistration and independent H1 tests remain unresolved.


## R8 developer predictive comparison, still NOT a registered H1 test

[R8](R8-development-predictive-baselines.md) introduces a *bounded synthetic TRAIN/TUNE prediction comparison*: identical complete pre-event source models and prior R6 synthetic hazard laws; a fixed trained ridge probability model; ordinary topology/stock/individually feasible-plan/common-upstream minimum-cut features; and the same model plus only the R1 scoped-pair indicator. Ground truth is exactly marginalized **R7** strict restoration under one fixed developer policy, not independent observed outcomes. R1 exposure is limited to the actually modeled shared-upstream C event; channels are not given fabricated independent failures. Conditional Brier is averaged across independent TUNE systems with positive loss risk. Exact full-input marginalization is explicitly a separate, not runtime-matched lower bound. The implementation measures wall-time but has no fixed parity cap. No SEALED family, confirmatory H1 hypothesis test or physical failure evidence is involved; the candidate JSON remains DRAFT_NOT_PREREGISTERED.


## R9: constructed physical incidence controls and explicit nonparity of compute

[R9](R9-physical-identity-and-budget.md) defines six tiny **independently designed artificial fixtures**: two separate physical channels, route-name aliases of one mechanism, common-cause disabling and stock/deadline bottlenecks. The strict R1 pair and standard minimum event cut are computed from declared event footprints, with the same physical event effects applied to fixed R7 policy trajectories. For one and two available kits, both structural scores are identical but actual strict restoration differs. A bounded exact standard reference consumes a declared count of simulated timeline ticks; when incomplete, it produces exact lower and upper probability bounds, never an unjustified point forecast. **Cross-algorithm equal CPU/wall-time/memory is NOT achieved**, and no training, sealed-family, field-data or H1 prediction has been performed. The previously archived R8 zero-gain result remains unchanged, and P1 registration stays blocked.


## R10 developer-only operational-prefix and shared worker-cap gate

[R10](R10-joint-executable-backup-and-process-caps.md) introduces a distinct exploratory **single-prefix jointly ready** feature: two physically event-disjoint delivery mechanisms must both be preparable by one admissible pre-shock action history with shared stock, before a known toy shock boundary. A conventional augmented-state DP and separate action-history DFS independently agree on its definition; a fixed-priority policy's own readiness is reported independently. The result is ordinary finite-state reachability, not proof of a new science or a fixed R1/P1 feature. Static R1, joint state DP and standard full-model expected restoration are run under the same enforced Linux **process limits**, but have different outputs and are not equal-information prediction baselines with matched training/evaluation. No outcome, seed or model from the sealed future H1 family generators is used. Protocol DRAFT_NOT_PREREGISTERED remains in force.


## R11 development-only same-objective prediction with unknown event time

[R11](R11-unknown-time-matched-task-predictive-pilot.md) now compares raw conventional features and two implementations of the same prior-weighted joint-readiness feature (standard state DP and independent chronological DFS) with a **single exact model-expected Brier endpoint** on nine constructed physical configurations. Only the pre-event probability of early/late shock is known; no realized time or identity is exposed to the policy or learner features. Linux workers execute each model's end-to-end feature generation, synthetic target generation, training and prediction under identical 5-second wall/CPU and 256-MiB virtual-AS ceilings. **27 TRAIN and 18 TUNE parameter settings reuse the same nine configurations**, so no independent holdout or causal/external predictive evidence arises. No H1 feature, final policy or inferential test is frozen. The original R8 negative remains untouched and P1 remains DRAFT_NOT_PREREGISTERED.


## R12 development-only independent-grammar transfer — not H1 registration

[R12](R12-cross-grammar-external-validity-readiness.md) tests a separate exploratory R10 readiness representation across disjoint *artificial* graph grammars, not new empirical domains. The direct route TRAIN grammar has nine mode×stock structures (27 time-prior rows); two new TUNE families have eighteen structural mode×stock structures (36 time-prior rows). A graph/physical-event-incidence fingerprint must show zero TRAIN/TUNE overlap. The same R7 nonanticipative policy with unknown shock tick 2/3 and stipulated event law gives exact strict restoration; raw, conventional interaction, standard state-DP and independent-history features use the same fixed Ridge procedure. A separate exact model-known oracle supplies the conventional Bayes lower bound under the stipulated simulator, not a matched-capacity learner. All predictions run with the same enforceable Linux process ceiling, but work and model dimensions differ. No independently observed faults, actual physical entities, preregistration or H1 confirmatory inference occur; P1 remains DRAFT_NOT_PREREGISTERED and the R8 negative result is untouched.


## R13 independent physical-data admissibility: no empirical H1 records yet

[R13's six-source institutional metadata inventory](R13-public-source-admission-manifest.json) and [admission report](R13-public-data-admission-and-evidence-gaps.md) check whether public descriptions prove actual individual-service pre-fault activity, causal goal loss, restoration on the same observed policy history, physical event identities, resource/topology snapshots, deadline observation and independent physical sampling. **No full source files were retrieved or independently row-audited; none was admitted for original H1.** The R13 [episode schema guard](../experiments/p1_r13_real_data_admission.py) may calculate provisional 0/1 labels for SYNTHETIC demonstration episodes but explicitly NEVER certifies external real-world provenance; loss-ineligible and censored cases are not converted to nonrestoration outcomes. P1 remains DRAFT_NOT_PREREGISTERED; any different county-outage proxy requires a separate research question, not an H1 rewrite.


## R14 raw operational source intake — auxiliary node failures remain NOT H1

[R14](R14-lanl-actual-raw-node-fault-intake.md) streams a bounded copy of the historical 1996–2005 LANL all-systems node failure/interrupt CSV from a **specific public third-party Git mirror commit and blob** in CI. A small, non-outcome-selected first-256-record quality screen counts parseable node fault/fix times, inconsistent intervals, missing fields and root-cause presence; a complete file row count and SHA256 record the actual bytes read. Raw rows and node IDs are not stored in the research repository. **Origin equality with LANL is not independently established**, and physical node fault/repair events alone do NOT satisfy the strict individual-service-loss/policy/restoration H1 risk-set. No field H1 unit is admitted or fitted, the original R8 negative remains intact, and P1 is DRAFT_NOT_PREREGISTERED.


## R15 primary-original attestation and strict same-job linkage remain blocked

The [R15 report](R15-original-source-and-job-lineage-gate.md) distinguishes two independent prerequisites: official LANL byte-source authentication and observed job/service-goal recovery. The initial GitHub Actions official-web-page link probe returned URLError; **no original publisher tar.gz data were retrieved**. The R14 third-party mirror file has 26 actual CSV columns for node failure and administrative fix but NO identified stable original-job/restart identity. LANL's System-20 usage and event raw archives are separately published but **uninspected** for compatible join semantics. A constructed temporal node/job overlap cannot serve as real actual-loss/restoration proof. The R15 program fails closed and admits 0 service episodes, preserves P1 DRAFT_NOT_PREREGISTERED, sealed H1 families and R8/R12 scores.
