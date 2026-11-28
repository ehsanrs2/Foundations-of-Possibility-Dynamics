# R16-R / S1 — Scientific synthesis: bounded operational possibility

**Snapshot:** main 2f76004da87892bf200b1b989ad8663833b0bacf, 2026-11-28 (merged #48).
**Disposition:** author/developer synthesis for critical review, not independent review, a systematic literature review, a preregistration, or a validated theory.

## 1. What the project studies

A bounded operational system can change which goals are attainable by using actions that construct capabilities, consume or replenish resources, or enable further actions. Disturbances can remove capabilities or disable actions. Observation restrictions constrain decisions. The project attempts to express creation, loss, retention and restoration in one explicit modeling vocabulary, and to evaluate whether particular summaries improve prediction or computation.

The word *possibility* here means **operational attainability under a specified model, goal ontology, resource accounting, horizon and action permissions**. It does not mean metaphysical possibility, physical discovery, epistemic belief, utility or the invention of a previously unrepresentable concept. All current implementations specify their representable types and transitions in advance. A generated capability is new to the current held set, not necessarily new to the universe of types.

The provisional contribution is a documented integration of operational definitions, negative controls and reproducible comparisons. A claim of priority, independent scientific discipline, superior algorithm or empirical law is **not established**. Even the value of the integration as a scholarly contribution requires comparison to prior art and external review.

## 2. A scoped mathematical correspondence, not a new core API

Use the narrow G2/B1/GOG profile for the following correspondence: finite capability universe U, durable held set C, d-dimensional nonnegative integer stock r, finite horizon H, atomic one-tick actions, explicit WAIT, no negative prerequisites. In the deterministic no-shock profile each action a has prerequisite set P_a, one output o_a, nonnegative integer consumption k_a and yield y_a, and a declared construction flag. It is legal when P_a is a subset of C and r is componentwise at least k_a. A legal action maps (C,r) to (C union {o_a}, r-k_a+y_a). Time increases by one. The constructive arm E+ allows all registered actions; E0 excludes the designated generative actions. Both use identical initial state, stock, goal vocabulary, horizon and accounting.

**Finite state correspondence.** For each arm, construct a directed layered graph with vertices (t,C,r) reachable from the initial state, t from 0 to H, and an edge labeled by each legal command including WAIT. Inventory is bounded on this finite horizon by initial stock plus H times the largest per-step yield in each dimension. Every legal history corresponds to a path from the initial vertex by induction on t. Conversely every such path corresponds to a legal action history by the edge definition. Hence the reachable goal sets and first attainment times coincide with ordinary augmented-state reachability. This is a scope-limited representation argument, not an efficiency bound or an assertion that all richer models in the book satisfy the same restrictions.

For fixed U and H, the graph may be exponentially large in the number of capability types; the construction does not promise tractability. A finite known fault schedule can be incorporated by augmenting the transition state with persistent disabled-action information and explicit chronology. Hidden event times and noisy observations require an observation process and a policy on delivered histories, not access to the latent state. B4's exact terminal-response comparison and B5/B6's strict restoration labels are distinct tasks. Their tiny bounded conformance results do not prove general stochastic equivalence.

## 3. Distinct estimands and what they do not imply

| Object | Question | Scope and nonimplication |
|---|---|---|
| Reachability R(E,g,H) | Is there a legal history reaching a named goal g by H? | Existential; does not say the acting controller can find it, nor that all goals can be attained together. |
| GOG | How many registered goals are reachable with construction but not without? | Set difference of individually reachable goals in nested arms; nonnegativity follows by path inclusion. Not a probability, utility, backup count, or ontology-invariant index. |
| Historical GBR gain | Does optional construction increase the binary backup-pair indicator for baseline-reachable goals? | Depends on plan equivalence, scope and physical event identities; not identical to R1 or R10. |
| R1 scoped pair | Are there two separately feasible supports disjoint under the declared exposed physical event ontology and identity convention? | Missing coverage is undefined, not zero. Separate feasibility does not ensure joint preparation, adequate time or successful repair. |
| R10 readiness | Can independent backup channels be prepared jointly under the available stock and time? | A conventional augmented-state feasibility question; not the historical R1 primary feature. |
| Retention | Does a previously active goal survive the event? | Not a restoration success. |
| Strict restoration | Given actual fault-caused loss of a previously active goal, is that same goal regained by H on the executed policy history? | Conditional, policy-specific; missing risk eligibility and incomplete follow-up do not establish failure. |
| Causal effect | Does changing construction permissions/resources change outcomes? | Requires a separately designed intervention, explicit estimand and risk-set assumptions; not inferred from prediction or GOG. |

For a fixed policy pi, define L as the event that the declared goal is held immediately before the fault and absent immediately after it; let T be first subsequent reacquisition on that history. The primary draft target is Pr(T <= H | L, pi, X), with X the admissible pre-fault input and the conditional probability defined only where Pr(L | pi,X)>0. Full follow-up is required for negative labels; censoring and unknown eligibility require separate handling. A terminal-possession target mixes retention, first attainment and restoration. B6's UNKNOWN_RISK corrects the interpretation when follow-up ends before the event; B5's privileged label convention is historical, not field evidence.

For any deterministic summary Z=f(X), unrestricted prediction based on (X,Z) has the same information as prediction based on X. A useful feature might reduce approximation, learning or computation cost for a restricted predictor; this is a comparative empirical/computational claim, not a new source of information. An intervention can change L itself, so comparing conditional restoration between interventions can select different at-risk populations. No causal inference follows.

## 4. Counterexamples are scientific constraints

- **Ontology sensitivity:** Adding an intermediate reachable bridge to the registered goals can change GOG without changing the action system. A harmless rename under a consistent bijection is a much weaker invariance than arbitrary refinement. See [B1](R16B-core-semantics-contract.md) and [GOG-1a](R16N-GOG1-exact-goal-slicing.md).
- **Individual versus joint feasibility:** A single kit can be enough for either of two constructions separately and insufficient for both together. The union of individually attainable goals is not a joint plan. See [G3](G3-verification.md) and [R10](R10-joint-executable-backup-and-process-caps.md).
- **Physical aliases and common causes:** Two rule names can encode a single mechanism; two routes can share an exposed power dependency. A model label or a local digest cannot establish physical independence. See [R1 audit](gbr-metric-audit-v0.3.md) and [R9](R9-physical-identity-and-budget.md).
- **Cut versus packing:** For nonempty event footprints, a disjoint pair requires a hitting set of size at least two; the reverse implication fails for the triangle {a,b}, {b,c}, {a,c}. This is a known type of combinatorial distinction, not a priority claim. See [N1](R16M-N1-novelty-and-R1-decision.md).
- **Timing and policy:** N1's retrospective 108 rows from C2a contain 18 of 27 cells with differing exact recovery probabilities despite matching mode, stock, prior, R1 and cut. A direct structure and dual-stage structure both have R1=1, cut=2, kits=2 and early prior=3/4 but conditional model probabilities 3/4 and 1/8. This does not isolate a causal effect of staging. See [N1 execution](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/actions/runs/45564779911).
- **Information and follow-up:** A silent event cannot announce itself via a privileged fault flag. Delayed or erroneous measurements can waste scarce resources or miss the deadline. Unknown eligibility cannot be coded as no loss. See [R7](R7-silent-event-observation.md), [B4](R16E-B4-hidden-fault-policy-conformance.md), [B5](R16F-B5-strict-restoration-lag-and-censoring.md), [B6](R16G-B6-noisy-observation-and-evidence-gate.md).

These are scoped logical or model-executed results, not estimates of real-world effect sizes.

## 5. Evidence synthesis: preserve negative and positive development findings

Lower Brier is better. These rows concern different designed development populations and feature definitions; absolute scores must not be pooled or compared across studies as one experiment.

| Study | Baseline | Augmented or comparator | Observed development result |
|---|---:|---:|---|
| R8 | 0.182841176250 raw | 0.182841176250 raw+R1 | Zero incremental gain; R1 constant at zero across 84 defined settings. No matched hard resource caps. |
| R11 | 0.163607515992 raw | 0.163115603693 raw+joint readiness (standard DP) | Small improvement, repeated structures, no independent heldout. |
| R12 | 0.165522792238 conventional interaction | 0.164259405297 raw+joint readiness (state DP) | Small improvement on structurally separated designed grammars; equal caps are not equal actual compute/capacity. Raw alone 0.165914979088. |
| C2a | 0.1595602648531204 raw | 0.16040127346668326 raw+R1 | R1 worse on DEV_EVAL; conventional joint-readiness DP 0.1552048132360558. No independent physical systems or confirmatory TEST. |

Sources: [R8 archive](R8-development-summary-seed20261101.json), [R11 archive](R11-unknown-time-prediction-results-20261102.json), [R12 archive](R12-cross-grammar-results-20261102.json), [C2a execution](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/actions/runs/45558400768), [N1](R16M-N1-novelty-and-R1-decision.md). R11/R12 are not tests of the primary R1 feature. N1 recommends pausing R1 confirmatory preparations, not statistically rejecting a preregistered H1.

For computational GOG, GOG-1a/b and GOG-2a compare ordinary exact search, dominance, dependency slices, indexing and grouping under bounded assumptions. GOG-2a's adaptive grouping preserved the exact outputs but had higher aggregate CPU and process-wall medians than ordinary goal-wise indexing in two CI executions of the same 28 cases. The deterministic work counts reproduced, but timings are not independent domain replications. See [R16-Q archive](R16Q-GOG2a-CI-summary-20261128.json). No general algorithmic superiority is established; do not tune the reused suite and relabel it an untouched test.

For physical evidence, R14 inspected a third-party LANL node-failure mirror (23,739 nonblank data rows; publisher listing 23,741 not reconciled). R15 did not authenticate the publisher's original file or verify original-job loss/restart lineage. B7a ran an actual local owned-process restart and no-restart control with a persistent work ID, but the operator and assessor are the same and the workload is trivial. **Zero independently admitted field H1 labels and zero confirmatory H1 samples.** See [R15 archive](R15-node-job-lineage-results-20261108.json), [R16 source gate](R16-lanl-publisher-usage-event-lineage-protocol.md), [B7a](R16L-B7a-local-process-operational-pilot.md).

## 6. What remains to compare with existing science (S2 agenda)

The existing [literature map](../book/02-prior-work.md) and [novelty audit](novelty-audit-v0.3.md) are starting points, not a completed search. The following correspondences are questions to investigate against verified primary/review sources, not claims that the literature lacks the project's concepts.

| Comparator family | Specific comparison question |
|---|---|
| Classical, temporal and resource-constrained planning / AND-OR and Petri-net encodings | Are generative actions just ordinary transitions with enabling predicates? Compare exact time/stock semantics, conditional planning, relevance analysis and goal decomposition. |
| Reachability, viability and controllability | Distinguish existential goal reachability from invariant constraint satisfaction, controllability and robust policies. |
| Partially observed stochastic control | Compare fixed-policy strict-loss targets, belief-state planning, event and observation timing and risk conditioning; do not substitute terminal reward. |
| Reliability, dynamic fault trees, network repair and resilience | Compare support packing/cuts, physical common causes, jointly feasible backup, time to recovery and service identity. |
| Adjacent possible, innovation, empowerment and evolvability | Distinguish expanding a represented action space, newly reachable named goals, channel capacity, novelty statistics and genuine changes in the representation universe. |

S2 must record databases/indexes, search strings and dates, inclusion/exclusion, verified publication metadata and accessible text, exact definition-to-definition mappings, limitations and contrary prior work. Avoid priority claims from absence of a match in a selective search. A comparison involving specific papers must cite actual retrieved sources. No external literature search or verification was performed in S1; S2 is not completed here.

## 7. Positioning and decisions for an independent reviewer

**Proposed identity:** a provisional operational framework and reproducible negative/positive development record, not a new discipline. The current model is expressible within conventional finite-state planning. Its definitions and counterexamples may be useful for explaining when simple redundancy summaries fail to characterize restoration. Whether this explanatory integration is distinctive enough to publish remains open.

Preserve three separate tracks: (i) predictive R1 H1 draft, paused pending independent justification; (ii) descriptive GOG with adaptive optimization paused; (iii) causal intervention design, not evaluated. Independent evidence acquisition may proceed as feasibility work, without treating it as confirmation.

Ask a reviewer who did not design these tests to record the version, expertise, conflicts, verdict and specific counterarguments. In particular ask whether any statement exceeds its evidence, whether standard planning/reliability already offers the same framing, whether a defensible nonredundant R1 population exists, whether GOG deserves a stronger benchmark, and what provenance would establish same-work restoration. Reviewers must be able to recommend abandoning either candidate.

S3 should choose among a genuinely distinct mathematical contribution (requires proof and verified prior-art comparison), a bounded engineering advantage (requires prospective competitive evidence), a useful explanatory/negative-results synthesis (requires review), or retirement of a claim. Do not silently substitute measures. Rewrite the book only after these distinctions are reviewed, with historical definitions and negative records traceable.

**Scientific firewall:** H1 remains DRAFT_NOT_PREREGISTERED, sealed families untouched. S1 changes neither primary feature, data, solver nor historical protocol. Issues #3 and #8–#12 remain open. No independent review, field experiment, external literature verification or new empirical test is claimed.
