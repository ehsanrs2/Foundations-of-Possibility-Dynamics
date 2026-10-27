# Chapter 8 — A staged program of scientific tests

**Status: research roadmap; stages below are not claims of completion.**

## Stage A — Formal verification

Freeze the rule grammar, resource semantics, timing and fault model. Prove monotonicity properties when optional construction is added, state precisely when they fail, and search for counterexamples to representation invariance. Compare the definitions to dynamic hypergraph reachability, AND/OR networks, repair and viability theory.

## Stage B — Software correctness

Create a small-state exhaustive search oracle independent of the production solver. Check enumeration against hand-specified cases and metamorphic tests: renaming capabilities, removing budgets, enforcing shared prerequisites and adding irrelevant options.

## Stage C — Benchmarking

Preregister the E0/E1/E2 simulation grid, sample size or precision calculation, baseline metrics, generator families and evaluation score. Run family-held-out comparisons and publish raw outcomes, code commits and null findings. Compare feature computation costs.

## Stage D — External validity

After synthetic results, select a real bounded system where goals, failure events, resources and repair rules are directly measurable—for instance modular computing equipment or a reproducible laboratory setup. Audit measurement error and feasibility of causal interventions.

## Stage E — Theoretical synthesis

Only then evaluate whether predictive patterns explain mechanisms that existing frameworks leave insufficiently captured. A successful specialized model may be a valuable publication even without founding a new discipline.

This stage-gated structure prevents the scientific book from becoming a narrative in which attractive conjectures are progressively mistaken for proven laws.

## Gate G0: software verification (completed)

An independent exhaustive search oracle and a dynamic-programming solver agreed on 256 small-reachability comparisons from a seeded generator. The [G0 audit](../research/G0-verification.md) reports this software result and its restrictions. The GBR predictor and formal P1 trial **remain untested**. [LEAN](../integrations/lean/README.md) is proposed only for a later financial-domain transfer study, and no LEAN engine run is claimed.

## Gate G1: bounded causal-plan support (completed as software check)

[Gate G1](../research/G1-verification.md) establishes one narrow operational definition of a plan's causal source/rule dependencies and uses two distinct enumeration strategies to compare tiny examples under pre-planning shocks. The 192 successful paired plan-set checks indicate internal consistency in sampled finite instances, not the value or novelty of GBR. The next research priority is *resource-consuming, disturbance-aware plan execution*, independent provenance checking and preregistered out-of-family prediction baselines, **not** a domain-specific financial backtest.

## Gate G2: resource constraints and in-run faults (software gate)

The [G2 model](../research/G2-verification.md) adds inventory depletion/replenishment and shocks during a bounded trajectory. Two search strategies check post-fault goal availability. Its contributions are **operational correctness checks** only; no conclusion about GBR performance or the existence of a new fundamental science may be drawn. G3 must address plan/path provenance under consumption, multiple disturbances and equal-information full augmented-state baselines.

## Gate G3: dynamic restoration histories and shared inventory

The [G3 audit](../research/G3-verification.md) uses history flags and two search implementations to distinguish retention, genuine restoration and joint feasibility. It remains a bounded, perfect-foresight software gate. **G4 must remove inappropriate advance knowledge of disturbances**, evaluate executable policies and freeze equal-information baselines before any predictive benchmark for GBR can be interpreted.

## Gate G4: shock observation and non-clairvoyant action prefixes

The [G4 software specification](../research/G4-verification.md) replaces the single known realization with a finite distribution of possible shocks, requiring one pre-shock action history and admitting scenario-adaptive recourse only after observation. A full-information optimizer supplies a strictly more informed upper bound. This resolves one avoidable look-ahead ambiguity but **does not implement GBR predictive benchmarking**. Next priorities are scenario observation uncertainty, consuming-resource plan provenance, and prespecified held-out comparisons to conventional augmented-state control.


## R2: an additional falsifying construct-validity control

The [R2 audit](../research/R2-resource-policy-bridge.md) connects R1 physical fault-event supports with G4's finite non-clairvoyant policy oracle. It shows an informative limitation: identical disjoint-route structure can correspond to distinct best executable recovery/availability rates when upfront investment is limited by inventory or time. The next gate should specify any proposed **resource-aware plan/policy feature** in advance and compare it with a fully informed **equal-information** augmented-state baseline; do not retrofit the feature to these toy outcomes and call that a predictive test.


## P1/H1 design phase: no new confirmatory samples

An executable [draft-protocol consistency check](../experiments/p1_protocol_audit.py) and a [hypothetical precision sensitivity calculator](../experiments/p1_sample_size_sensitivity.py) now support the [proposed study design](../research/P1-H1-study-design-v0.1.md). These are internal design tests, not predictive performance results. The next **hard scientific gate** is to finish the resource-aware feature ontology, implement non-anticipative loss-and-restoration policy rollouts, fully specify generators and independent test-unit sampling, then justify power and a locked primary comparison before any confirmatory outcomes are generated.


## R3: bounded actual trajectory outcomes (software verification only)

[R3](../research/R3-nonanticipative-strict-restoration.md) provides a deterministic no-lookahead policy rollout and full same-history restoration bookkeeping with loss eligibility and resource-consuming actions. This closes one *implementation ambiguity*, not the broader H1 scientific gate. Future steps must independently fix the policy and fault observation model, generator distributions/seed registry, pre-failure physical feature contract, matched-information baselines and prospective statistical inference. The P1 JSON remains explicitly unregistered.


## R4: bounded developer-only system families

The [R4 registry](../research/R4-development-family-boundary.md) implements three named TRAIN and one TUNE small-system grammars without producing or even implementing the two reserved test families. Seed fingerprints, a sealed-family rejection contract and R3 trace consistency checks provide reproducibility for *development experiments only*. The strong required next work is to freeze policy/target selection, physical support identity and matched-information baselines; specify sealed-family sampling independently under an immutable protocol; then justify the independent-system test count. No H1 scientific evidence arises from R4.
