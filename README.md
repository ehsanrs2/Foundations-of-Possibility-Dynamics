# Foundations of Possibility Dynamics

**Working scientific monograph v0.2 (26 October 2026)** — an open research record, **not an established scientific discipline or empirically validated general theory**.

[Read the 10 chapters](book/index.md) · [Persian guide](README.fa.md) · [Research protocol](research/protocol.md) · [Claims ledger](research/claims.md) · [Technical review](research/scientific-review-v0.2.md)

## Aim

Study how bounded systems generate, lose and rebuild *operationally reachable* capabilities under resource and time constraints. Test whether constructible backup routes predict disturbance recovery above established network redundancy, reachability, viability and empowerment measures.

## Present scientific status

The book contains finite-system definitions, candidate GOG and GBR gain measures, a hand-designed illustrative communication scenario and a detailed prospective experimental protocol. **No ensemble validation, cross-domain tests or general physical law has been established.** Known augmented state-space methods may describe the same phenomena.

## Reproduce and build

Requires Python 3.9+; Pandoc for publication artifacts.

    python -m unittest discover -s tests -v
    python -m experiments.toy_case
    python scripts/check_book.py
    bash scripts/build_book.sh

The build generates HTML and EPUB in the ignored dist directory. GitHub Actions runs unit/integrity checks and uploads HTML/EPUB build artifacts. An illustrative example is not confirmatory scientific evidence.

## Scientific integrity

See the [claims ledger](research/claims.md) before citing a statement as a result. Negative evidence and mathematical counterexamples are essential. The editorial roadmap and caveats are in [the self-review](research/scientific-review-v0.2.md).

## Attribution and licensing

Formal author credit and an open-content license have **not been agreed or granted**. A public repository does not automatically provide an open license. Third-party sources are cited, not reproduced.

**Formal audit:** [Mathematical propositions and counterexamples](appendices/A-mathematical-propositions.md) · [Artifact provenance](appendices/B-reproducibility.md).

## P1 G0 verification and external tools

[Gate G0 report](research/G0-verification.md): two independent bounded reachability solvers agreed on 256 fixed-seed comparisons over 64 synthetic instances and their shock variants. This is **software verification, not evidence for H1**. Run: python -m experiments.p1_gate0.

[QuantConnect LEAN decision](integrations/lean/README.md): potentially useful for a *later financial-domain transfer*, but is not adopted as the core mathematical simulation engine. No LEAN backtest was run.

## Latest verification: Gate G1

[Gate G1 report](research/G1-verification.md) and [code](experiments/p1_gate1.py): bounded causal plan-support tracking, scope-dependent backup calculations and pre-plan shocks. Two enumeration approaches agreed on 192 complete plan-set comparisons from 48 tiny sampled models and paired starting-source failures (no disagreements); 13 dedicated tests were added. **This is only a software/formal gate, not a predictive validation or mathematical novelty result.** Future studies remain subject to preregistration and robust baselines.

## Latest bounded verification: Gate G2

[Gate G2](research/G2-verification.md) introduces discrete **consumable inventory**, replenishment, and a **single in-run fault at a tick boundary**, evaluated by independent exhaustive DFS versus time-layer state-set search. It checks *post-fault goal availability*, which can mean retention as well as restoration. [Executable experiment](experiments/p1_gate2.py), [expected diagnostic](experiments/g2_expected.json), and [tests](tests/test_p1_gate2.py) are versioned. These software checks are **not GBR prediction experiments** or evidence for H1.

## Gate G3: time-consistent restoration and joint feasibility

[Gate G3 report](research/G3-verification.md) distinguishes post-fault availability, function retained across the fault, **strict restoration after an observed loss**, and **joint attainability of all targets on one history**. An explicit history enumerator is compared with a standard augmented-state solver and the G2 reachability baseline. All results are **perfect-foresight software checks**, not a predictive result, new law or validation of GBR. [Code](experiments/p1_gate3.py) · [Tests](tests/test_p1_gate3.py).

## Gate G4: information-consistent policies

[Gate G4 report](research/G4-verification.md) compares *non-clairvoyant common pre-shock prefixes with scenario-adapted post-shock recourse* to a full-information upper bound from ordinary augmented-state reachability. Two independent search strategies provide a bounded software cross-check. [Code](experiments/p1_gate4.py) · [Tests](tests/test_p1_gate4.py) · [Deterministic manifest](experiments/g4_expected.json). **This is not empirical evidence for H1 or for a new general theory.**


## Reviewer-driven critical audit (Issues #8 and #9)

[Novelty and information-redundancy audit](research/novelty-audit-v0.3.md) · [GBR exposure/representation counterexamples](research/gbr-metric-audit-v0.3.md) · [Executable negative-control diagnostic](experiments/gbr_review_counterexamples.py).

**Major Revision remains necessary.** The raw candidate GBR can report false physical backup under a merely duplicated rule alias; a deterministic GBR feature adds no information to an unrestricted predictor already given its complete source model. These are negative/conditional results, **not** empirical H1 validation. Reviewer Issues #8, #9, #10, #11, #12 and overarching #3 stay open.

## R1 reviewer response: physical fault-event ontology and separate estimands

[Appendix C — fault ontology](appendices/C-fault-event-ontology.md) · [Appendix D — predictive/causal estimands](appendices/D-predictive-estimands.md) · [strictly scoped executable diagnostics](experiments/fault_ontology_r1.py). Physical failure IDs and shared causes are external assumptions requiring evidence; unknown support tokens cause a hard error. This **does not** establish a valid universal GBR metric or finish preregistration. Issues #9, #11, #12 and #3 remain open.


## R2 — Physically disjoint routes vs executable joint preparation

[Resource-and-policy counterexample](research/R2-resource-policy-bridge.md) uses the same declared failure events but changes consumable kit supply and available pre-shock preparation time. A physically event-disjoint route pair exists in all positive-kit cases, yet **optimal non-clairvoyant post-fault goal attainment** ranges from 1/2 to 3/4 depending on resources and time. [Run the toy](experiments/resource_policy_r2.py). This is negative construct-validity evidence, NOT H1, real-world reliability or a general new metric.


## P1/H1 main predictive study — draft design, not preregistered

[Prospective H1 study design](research/P1-H1-study-design-v0.1.md) · [machine-readable draft](research/p1_h1_design_candidate_v0_1.json) · [audit](experiments/p1_protocol_audit.py) · [hypothetical sample-size sensitivity](experiments/p1_sample_size_sensitivity.py).

A primary strict-restoration outcome, matched-information baseline matrix, train/tune/sealed-family partition, clustered system-level loss and explicit freeze blockers are now documented. **The six family names are design placeholders, not generated datasets. Sample sizes, model/feature implementation, actual evaluation policy and effect threshold are NOT frozen. H1 has not been tested.** 


## R3 — Executed, non-anticipative strict restoration

[R3 methods report](research/R3-nonanticipative-strict-restoration.md) · [fixed-policy rollout code](experiments/p1_r3_policy_rollout.py) · [tests](tests/test_p1_r3_policy_rollout.py). Realized goal loss and subsequent reacquisition are now distinguished *on the same executed trajectory*, with unknown future shock time and conditional no-loss outcomes explicitly undefined. Two separately coded execution routines cross-check full histories. This is a **software/endpoint gate only**, not validation of H1, a trained predictor, or a frozen P1 rollout policy.


## R4: development-only generators and sealed holdouts

[Research status](research/R4-development-family-boundary.md) · [developer generator](experiments/p1_r4_development_families.py) · [regression tests](tests/test_p1_r4_development_families.py). Three TRAIN families (random AND/OR, modular cluster, hub dependency) and one TUNE family (temporal bottleneck) now have bounded synthetic builders and reproducible per-system SHA-256 seed streams. **The two named sealed-test families cannot be generated by this builder**, and have no implementation or outcome data. Developer diagnostics are not empirical H1 findings. The evaluation policy, full family specification, physical ontology and preregistration remain open.


## R5: exploratory developer-only pilot (NOT H1)

[R5 methodological report](research/R5-development-pilot.md) · [bounded pilot code](experiments/p1_r5_dev_pilot.py) · [workflow and JSON artifact](.github/workflows/r5-development-pilot.yml). The developer pilot executes 24 systems per TRAIN family and 12 TUNE systems under three fixed R3 policy variants, preserves nested scenario labels, resource accounting and full-history oracle comparisons. **The designed loss-eligibility mass is 3/4 by construction, not an empirical fault rate.** No held-out systems, predictive models, actual experiment preregistration or H1 results are produced.


## Fundamental motivation and R6 developer-risk audit

[Scientific question and limits](research/scientific-motivation-and-boundaries.md) explains why an operational-possibility research program could matter and what *would* establish novelty, without presupposing a new science. [R6](research/R6-variable-risk-and-exact-baseline.md) replaces R5's hard-coded 3/4 eligible-loss case design with independently stipulated variable **synthetic** basic event probabilities, explicitly preserving zero-risk systems. [R6 code](experiments/p1_r6_fault_risk_dev.py) computes a complete pre-fault, equal-information exact marginal reference under the known model. Neither real hazard rates nor GBR predictive advantage are established. H1 is untested.


## R7: a silent no-effect event is not a visible disruption

[Observation-filtered R7 executor and methods](research/R7-silent-event-observation.md) · [code](experiments/p1_r7_silent_observation.py) · [verification tests](tests/test_p1_r7_silent_observation.py). R7 is a separate opt-in full-state observation contract: only **actual changes** in held capabilities, available resources or visible disabled actions can switch a fixed policy from preparation to response mode. A scheduled but wholly ineffective R6 fault vector is **not announced**. Historical R3–R6 archives stay intact. This is synthetic software verification, not real sensor validation or H1 evidence.
