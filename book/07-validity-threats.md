# Chapter 7 — Threats to validity and limiting examples

**Status: critical methodological analysis.**

## 7.1 A known transition in disguise

A new capability may be introduced by a rule, but any such bounded rule can be encoded in a larger static state-transition space. A putatively new mathematical mechanism could therefore be a re-description of ordinary reachability. The originality question requires comparison of formal models, not terminology alone.

## 7.2 Dependency omissions

A backup route score is valid only for the exposed component set declared in advance. Shared electrical power, maintenance tools, suppliers or sensors may invalidate apparent independence. Correlated shocks and common-cause failures must be tested explicitly.

## 7.3 Representation changes

Relabeling a capability must not change scores. Splitting one component into multiple bookkeeping components might change path counts while leaving real capabilities unchanged. A robustness claim must state which refinements preserve the modeled transitions.

## 7.4 Opportunity costs

A construction rule that expands the options in one goal can consume the only resources needed for another goal. Individual plan feasibility is not simultaneous executability. Dynamic budgets, competing goals and path-dependent stock consumption require explicit policies.

## 7.5 Information leakage

A score calculated with knowledge of the future failure cannot serve as a pre-failure predictor. Nor is it fair to allow a new metric to inspect the full generating grammar while depriving baseline methods of it. Observability and compute cost belong in experimental design.

## 7.6 Philosophical limitations

Finite predeclared rules may produce novelty along a trajectory without creating new physically possible worlds. The model cannot resolve whether unforeseeable ontic possibilities arise in nature. Operational and epistemic novelty are different from that ontic thesis.

## 7.7 Selection effects

A hand-crafted example is useful pedagogy but not an unbiased evaluation. Register independent samples, negative outcomes, uncertainty procedures and reasons for discarded cases prior to confirmatory testing.

## 7.8 Fault-time and consumption ambiguity

With resource-consuming rules, individual routes cannot be combined merely by union: they can require the **same kit** or compete for stock after a loss. A fault at a transition boundary differs from a fault during an operation. The current G2 engine makes this distinction explicit and has no interrupted-action semantics. An end goal present after the fault may have survived it instead of being newly restored; these are different resilience outcomes. [G2 specification and limitations](../research/G2-verification.md).

## 7.9 Perfect-foresight planning and endpoint selection

A pre-shock plan conditioned on the exact future failure realization is **clairvoyant**; using its outcome as a label for an actual agent without future information would overstate resilience. The [G3 audit](../research/G3-verification.md) explicitly separates different history-dependent endpoints. Moreover, earliest post-fault availability and earliest strict restoration can be realized by **different** histories and must not be treated as one recovery policy. Pre-register the target outcome and observability assumptions before any model comparison.

## 7.10 Selection of information sets and scenario distributions

A future-fault scenario cannot be used to select actions *before* that scenario is observed. The [G4 verification](../research/G4-verification.md) enforces a common pre-shock prefix across all scenarios and allows branching only after the shock. Its exact toy case yields success 1/2 with non-clairvoyant preparation versus 1 with perfect scenario foresight. These numbers are properties of a designed model, not observed recovery frequencies. The nominal **shock time is still known**, the complete scenario set is predefined, and the fault identity is revealed immediately; a deployment policy may lack any of these. Do not treat a clairvoyant optimizer as an equal-information prediction baseline.


## 7.11 Fault ontology and representation-induced false backups

The [Issue #9 audit](../research/gbr-metric-audit-v0.3.md) demonstrates failure of raw GBR under duplicated rule aliases, source-token refinement, narrowed failure exposures and a zero-slack backup. An exposure token must map to a declared fault-relevant physical unit (or a genuinely separately failing rule implementation). The raw score cannot establish that two names correspond to two independent components. Semantics-preserving identity maps must be registered **before** computing the metric or evaluating held-out outcomes. Neither simple label-renaming tests nor two independent implementations of the *same* faulty score definition resolve this construct-validity threat.

## 7.12 Ontology uncertainty and conditional denominators

The [R1 scope contract](../appendices/C-fault-event-ontology.md) rejects unmodeled support tokens and explicitly records protected components, physical mechanism identities and event common causes. This is conservative but still depends on evidence not supplied by source code. The [proposed P1 restoration estimand](../appendices/D-predictive-estimands.md) warns that a policy can alter which goals are lost; comparing loss-conditioned restoration fractions between *different* policies can create selection bias. Prediction should use one common frozen evaluation policy and identical pre-shock observables, while causal effects require a separate design.


## 7.13 Individually feasible alternatives are not jointly preparable

Two fault-event-disjoint plans can each be individually feasible yet **cannot both be provisioned** before a fault under shared inventory depletion or inadequate preparation time. The [R2 controlled counterexample](../research/R2-resource-policy-bridge.md) exhibits this failure while holding the declared physical failure ontology and event probabilities fixed. Claiming practical resilience from a static GBR-like score alone conflates independent plans with an executable non-anticipative contingency policy. The R2 diagnostic does not establish a dynamic policy-sensitive GBR alternative.


## 7.14 Prospective P1 threat checklist: eligibility, information leakage, and repeated shocks

The [H1 design draft](../research/P1-H1-study-design-v0.1.md) protects the prediction timestamp before the realized fault, requires the same raw input and policy for baseline/candidate, counts feature runtime, and reserves family-level held-out partitions. Nevertheless, risk-set conditioning on **actual fault-caused loss** can select systematically different systems and policies; shock rollouts from one system are statistically dependent and must not masquerade as independent test instances. A fully informed augmented-state solver with the same simulator rules may correctly exhaust all useful predictive information; it is a scientifically essential negative comparator, not a straw baseline. Formal inferential rules and external-domain replication are not complete.


## 7.15 History-consistent endpoint versus implementability

The [R3 verification](../research/R3-nonanticipative-strict-restoration.md) prevents combining distinct success witnesses from different trajectories and avoids counting a retained goal as restored. Fault time now varies across scenarios and is not passed to the controller before occurrence. However the fixed action-priority heuristic assumes instantaneous full observation of post-fault capabilities and disabled actions, and the endpoint conditions on an **actual loss event**, which may itself depend on preparatory actions. Undefined risk-set cases must be disclosed by generator family; this remains a threat to confirmatory population inference.


## 7.16 Development-family and holdout leakage

The [R4 development registry](../research/R4-development-family-boundary.md) prevents an accidental call to its builder from producing either proposed sealed-test family. It is not a security sandbox: repository editors can inspect or change generator code, and separate scripts can bypass the guard. Four shock realizations sharing one synthetic network are **nested observations, not four independent experimental units**. A generator that deliberately includes three service-loss scenarios per system cannot supply an empirical estimate of real fault incidence. Before P1, lock the family acceptance rules, observation policy, generator signatures, held-out seed registry and physical event mapping; no meaningful population inference is possible yet.


## 7.17 R5 developer pilot: designed eligibility and policy dependence

The [R5 methods report](../research/R5-development-pilot.md) explicitly discloses that three of each four stipulated synthetic fault outcomes remove the initially held service. The resulting 3/4 conditional-risk eligibility is **designed** and yields no evidence of real-world frequency or independent sampling variance. A single system is the sampling unit even if each supplies twelve scenario/policy records; treating them as independent systems would be pseudoreplication. Policy variants alter resource consumption and recovery, but are developer heuristics not frozen policy interventions for causal inference. The test-family boundary remains unexamined.


## 7.18 R6: declared risk heterogeneity is not real fault calibration

R6 replaces a constant **designed** 3/4 eligibility mass with varied synthetic failure probabilities, some exactly zero. Those probabilities remain input assumptions; describing their distribution as estimated empirical risk would be invalid. The exact full pre-shock marginal baseline is Bayes-optimal *under the declared known model* and squared/Brier loss, so a deterministic extra representation cannot beat it in population expected loss at unlimited compute. Importantly, R3 still marks a **no-effect boundary as observed**, even when no component fails. Event non-detection, serial shocks and realistic delay/noise remain unmodeled and require a distinct inference design.


## 7.19 R7 observation validity and remaining realism gap

[Gate R7](../research/R7-silent-event-observation.md) removes the artificial observable boundary in R6's no-effect joint-event cases. However, its *perfect and immediate* visibility of all durable holdings, inventory and disabled-rule identities still assumes a strong sensor/diagnostic system; an ineffective **latent** failure may be dangerous even without immediate visible change. The one-event, atomic-operation model cannot represent delayed fault discovery, sensor false positives/negatives or partially observed policies. These must be explicitly treated before any claim of physical validity.


## 7.20 R8: artificial redundancy, target knowledge and compute parity

R8's source model includes full simulator rules and stipulated hazard priors: exact label probabilities are therefore **derived from the same known model**, not measured physical outcomes. The R1 feature is deliberately limited to one synthetic common-upstream event, with all other components assumed protected in this scope, so it may be constant or missing. A conditional actual-loss risk set excludes zero-risk systems, which must be enumerated. The ridge comparison controls training inputs, simple learner and capacity but **does not enforce a common wall-time/RAM cap** or implement all standard bounded augmented-state baselines. A TUNE-family result is not untouched confirmatory performance.


## 7.21 R9: feature-identity validity versus synthetic fixture performance

The [R9 designed physical mechanisms](../research/R9-physical-identity-and-budget.md) illustrate that textual action aliases must not be treated as separate assets and that a common upstream incident invalidates independently exposed route claims. Even valid disjoint-event plans may compete for one kit or miss a deadline. All incident probabilities and mechanism identities in R9 are **assumptions**, not externally confirmed material or sensor properties. The bounded standard reference counts only policy timeline steps; full plan enumeration, operation scanning, verification and real CPU/memory are not comparable, so shared computational parity still needs a separate gate.


## 7.22 R10: joint readiness remains known-boundary, synthetic reachability

The [R10 joint readiness gate](../research/R10-joint-executable-backup-and-process-caps.md) prevents treating *individually feasible* independent backup plans as jointly ready under a shared kit stock and preparation deadline. However its pre-event prefix is evaluated with the **known** synthetic R9 fault time; an unknown or partially observed shock-time distribution needs a new risk-aware policy contract. Physical event identities are stipulated toy assumptions. The common-process limits enforce Linux virtual-address-space and CPU caps, but are **not a matched all-in H1 prediction benchmark**: feature computation and full-model exact integration solve different problems. Neither physical validation nor inferential statistical power follows.


## 7.23 R11: equal prediction task is not independent scientific replication

The R11 development rehearsal compares genuinely identical Brier targets with preevent raw inputs and the same bounded worker environment. Yet the 27 training and 18 tuning observations are **different event-time prior settings for the same nine hand-built toy structures**. This is not an independent system sample, so standard inferential variance, generalization and H1 significance cannot be inferred. All response probabilities are exact consequences of the stipulated known simulator rather than external physical measurements. Feature computation is deterministic from information already available to the conventional standard state-DP learner; the two readiness implementations are expected to match. Equal ceilings also do not imply equal actual CPU work or parameter count.


## 7.24 R12: structural holdout is not statistical or external independence

Although R12 eliminates exact semantic action-graph overlap between artificial TRAIN and TUNE inputs, all grammars, physical event identities and shock-prior probabilities remain stipulated by researchers within one tiny family of channel-repair models. The 27 TRAIN and 36 TUNE rows are repeated parameter observations of only 9 and 18 synthetic graph configurations; these numbers are not independent engineering units and give no empirical confidence interval. A fitted Ridge representation may have capacity limitations, while standard augmented-state reachability derives the same readiness and a complete known-model probability oracle reaches Bayes risk. Identical Linux process ceilings are not identical measured work, and none of these results establishes real external validity or novelty.


## 7.25 R13: official source provenance does not imply endpoint validity

A publisher-hosted outage dataset can accurately measure county customer outage counts, and a failure dataset can accurately measure disk or machine failure, without establishing **fault-caused loss and restoration of an identified service goal under one observed policy**. [R13 screening](../research/R13-public-data-admission-and-evidence-gaps.md) records such unit and provenance mismatches explicitly. It reviews only public descriptions, NOT downloaded source records; NOT_DEMONSTRATED means lack of evidence, not evidence of universal absence. The new checker enforces timezone, nonanticipation, identity joins and censoring at the provisional schema level but **cannot verify physical truth from self-declared input fields**. No H1 external-validity claim or independent population inference is warranted.
