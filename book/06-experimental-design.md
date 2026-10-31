# Chapter 6 — Experimental systems and controlled comparisons

**Status: prospective methodology; no P1 ensemble results exist.**

## 6.1 System units and dependency grammar

Represent every system by a directed dependency hypergraph: a construction rule may need several components jointly and yield a new capability. Specify the initial inventory, prerequisite set, rule latency, consumed resources, target predicates, horizon, and an externally imposed failure process. Ordinary graph edges do not suffice for AND-type prerequisites without extra intermediate nodes.

## 6.2 Three paired conditions

In **E0** construction is forbidden. In **E1** construction is enabled with exactly the same initial resources, target family and disturbances. In **E2** separately ablate cost, time, common-cause exposure or resource reserves. A comparison is interpretable only when its changes are enumerated: merely adding options changes the action set and may trivially improve reachability.

## 6.3 Endpoints and fair information

The primary endpoint is the proportion of predefined goals recovered under a held-out shock, subject to a fixed post-shock budget and deadline. Pre-shock features must not depend on the realized test shock. Provide all prediction models access to equivalent observable rule and resource information. Compare with strong alternatives: graph and hypergraph cuts, route redundancy, feasible goal count, viability-style measures, and where practical information-theoretic empowerment.

## 6.4 Generalization and analysis

Split by **entire system instance and generator family** before training or choosing metrics. Avoid splitting repeated shocks of the same network between training and test sets. Report recovery prediction error, effect sizes, instance-clustered uncertainty, computational cost and explicit out-of-distribution degradation. No confirmatory sample size or power calculation has yet been frozen.

## 6.5 Interpretation

An improvement limited to a simulator family supports an engineering predictor in that family, not a universal law. Null results would be scientifically valuable. See [Protocol P1](../research/protocol.md) for the preregistration checklist.

## 6.6 G2 implementation: a strictly bounded execution kernel

The [G2 software kernel](../experiments/p1_gate2.py) extends the earlier monotone rules with per-action consumable stock, replenishment, waiting, and a single irreversible fault at a discrete time boundary. It reports *the earliest time each target is available after the disturbance*. This intentionally covers both retention and restoration, and cannot be called a strict restoration-time estimate. Separate goals are existentially tested and need not be jointly satisfiable. The model's one-tick atomic operations are a simplification, not a realistic treatment of failures during long-running actions. The [G2 audit](../research/G2-verification.md) defines these restrictions; no prospective P1 ensemble experiment is reported.

## 6.7 Strict restoration and perfect foresight

The [G3 solver](../research/G3-verification.md) separates retention from restoration using loss-at-fault history flags. Its strict restoration query requires the goal to be held just before the fault, removed by the fault, and reacquired later on the **same trajectory**. It also computes whether all goals can coexist on one inventory-feasible trajectory. These are best-case reachable outcomes under an **already known future fault**. They cannot represent policy performance under unknown future disturbances without a new information model and policy evaluation protocol.

## 6.8 G4: separate foresight from resilience

The [G4 model](../research/G4-verification.md) considers a finite scenario distribution whose realization cannot affect pre-shock actions; the controller observes the scenario only at the known shock time and may then take different feasible continuation actions. This avoids the specific G3 pitfall of optimizing the pre-shock history *with* knowledge of the realized future fault. For the same model, a scenario-by-scenario clairvoyant solver provides an **upper bound**, not a deployable prediction benchmark. The G4 endpoint is binary joint goal attainment after the fault, not the strict-restoration endpoint of G3. The underlying observation and fault-time assumptions remain restrictive; no P1 confirmatory experiment has yet been executed.

## 6.9 Distinct estimands and fixed risk population

[Appendix D](../appendices/D-predictive-estimands.md) separates (A) nested-option reachability (definitional), (B) a prospective incremental predictive-risk contrast, and (C) an exploratory causal intervention contrast. Only B can test the current proposed H1. Its tentative label is **strict restoration after actual loss under a single frozen non-anticipative rollout policy**, with a clearly defined loss-conditioned denominator and explicit handling of zero-loss cases. This is a *pre-freeze methodological draft*: final shock distributions, model-family splits, sample size, compute budgets, loss functions and baselines have not yet been registered.


## 6.10 Structural feature versus resource-aware policy outcome

The [R2 negative control](../research/R2-resource-policy-bridge.md) fixes fault identities and their probability distribution, and varies **only** inventory size or the number of available pre-fault preparation ticks. The independent structural path-pair indicator remains unchanged under positive kit supply while the non-clairvoyant optimized joint-service outcome changes. For future P1, planners and structural features must share resource/observation information, and *clairvoyant* solvers are upper bounds rather than deployable policy baselines. R2 evaluates *post-fault service availability*, not Appendix D's stricter restoration-after-loss estimand.


## 6.11 P1/H1 candidate study design and the registration boundary

The [prospective study design v0.1](../research/P1-H1-study-design-v0.1.md) now proposes a **pre-failure prediction** of strict actual-loss restoration under one fixed non-anticipating evaluation policy. It compares the same capacity-limited learner and raw information with/without a physically scoped candidate R1 feature, against augmented-state and conventional fault-cut/reachability measures. Rollouts are nested within **independently generated systems**, and a system without actual loss has an undefined *conditional* target, not automatic failure/success. Six train/tune/sealed-test family *names* are proposed, but their generators and held-out samples do not exist yet. No sample size, policy implementation, positive practical effect, primary interval rule or feature semantics is frozen. This is **not preregistration and no H1 experiment has been performed**.


## 6.12 R3: executed strict restoration with a non-anticipative policy

[R3](../research/R3-nonanticipative-strict-restoration.md) adds an actual finite state-and-inventory trajectory kernel controlled by a deterministic fixed-priority policy. It observes current capabilities, stock, currently disabled operations and the event-occurrence flag, *never the future scenario identity or future shock time*. It records the goal immediately before and immediately after a single fault and labels strict restoration only if a previously held goal was **actually removed** and the same trajectory reacquired it by the deadline. Goals not lost are not assigned failure or success. Conditional loss eligibility is reported, not silently taken as 100%. This is a methodological pilot and does not lock the future evaluation policy or estimate predictive performance.


## 6.13 R4 development-family registry (no held-out generation)

[R4](../research/R4-development-family-boundary.md) provides executable builders for three synthetic TRAIN families (random AND/OR, modular modules, shared hub) and one synthetic TUNE family (temporal preparation bottlenecks). The SHA-256 per-instance seed derivation and deterministic fingerprints make developer simulations reproducible. Two named SEALED families are **deliberately not implemented or instantiated**. Every system has four nested developer shock cases with exactly stated probabilities, executed under the same R3 policy interface. These case outcomes and generated fingerprints are *developer diagnostics*, not untouched family-level holdout evidence or a sample-size justification. Generator names and seed separation do not demonstrate scientific independence or cross-domain generalization.


## 6.14 R5 developmental pilot: policy and eligibility diagnostics only

The [R5 pilot](../research/R5-development-pilot.md) evaluates 24 independently generated developer systems per TRAIN grammar and 12 TUNE systems under three fixed policy variants: original R3, prepare-first after fault, and construction disabled. It evaluates the **same four nested fault cases per system**, records actual-loss eligibility and strict same-history restoration, and separates action kit consumption from fault-caused stock destruction. The constructed cases mechanically yield **3/4 eligibility**, so their frequency must not be interpreted as a measured fault prevalence. Developer performance and policy sensitivity cannot substitute for H1 held-out predictive tests, matched-information machine learning or independent physical validation.


## 6.15 R6 variable synthetic event risks and an exact pre-failure oracle

[R6](../research/R6-variable-risk-and-exact-baseline.md) implements a **development-only** joint basic-event model for service loss, shared infrastructure failure and one-unit inventory loss, with per-system separately seeded *stipulated* probabilities and variable early/late event times. R3 executes the same fixed non-clairvoyant policy under every case. The pre-shock exact reference integrates over the declared scenario law to predict strict recovery *conditioned on actual loss*, rather than conditioning on any realized future shock. Systems with zero actual-loss risk have undefined conditional outcomes. This removes the artificial R5 3/4 fixed risk-set share, but it **does not estimate actual fault incidence or validate a GBR feature**. The exact full-model reference supplies a strong known-simulator comparison, not a deployed bounded-compute learner.
