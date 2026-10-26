# Appendix C — Declared physical fault-event ontology (R1)

**Status: restricted provisional measurement contract, 26 October 2026. Not an endorsed replacement for G1 GBR.**

Reviewer Issues [#9](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/9) and [#12](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/12) show why different software names must not imply different physical failure mechanisms. Standard fault-tree analysis already models basic events, path/cut sets and common causes (Ruijters & Stoelinga, 2015). R1 deliberately adopts this modest established event perspective.

## C.1 Externally declared units

For an enumerated plan p reaching goal g, let S(p) be its causal support: initial components and rules needed by the goal, excluding unrelated executed actions.

An externally justified mechanism map m(x) assigns every support token to a physical mechanism ID. Two software aliases map to one ID **only if physical identity is independently supported**. Identical recipes implemented by separate equipment must NOT be merged.

Each token x must have either a nonempty set E(x) of **declared basic failure-event IDs**, or an explicitly stated protected status and a written scope-specific justification. The union of fault-event IDs constitutes the modeled failure universe F. Missing tokens, contradictory event incidence for one mechanism, and unlabeled protection cause validation failure; unknown exposure is not silently interpreted as independence.

Define a restricted canonical key and event footprint:

\[
K(p)=(g(p),\{m(x):x\in S(p)\}, t(p),c(p)),
\qquad D_F(p)=\bigcup_{x\in S(p)} E(x).
\]

Here t and c are *G1-model* sequential duration and cost. Equal canonical keys are duplicate **descriptions in this restricted grammar**, not a proof of full behavioral equivalence. Different cost/time schedules can still use the same vulnerable assets.

The guarded binary pair condition is

\[
b^{R1}_{g,F}=\mathbf{1}\{\exists K(p)\ne K(q):
D_F(p)\cap D_F(q)=\varnothing\}.
\]

It is assessed only after every plan token is mapped and **every candidate path has at least one modeled exposed event**. Otherwise the evaluator returns INSUFFICIENT_FAULT_COVERAGE rather than a misleading positive or negative number. This conservative guard does not deny truly invulnerable paths; it says that their independence cannot be evaluated with this incomplete scope.

## C.2 Comparison with existing fault-set measures

For a nonempty list of event-exposed feasible plans, the size of a minimum event hitting set is

\[
\kappa_g=\min\{|A|:A\subseteq F,\quad
 A\cap D_F(p)\ne\emptyset\ \forall p\in\mathcal P_g\}.
\]

This is a static cut over the **declared incidence model**, not an exact dynamic AND/OR repair-network cut. The tiny reference implementation exhaustively searches at most 12 basic events. If some feasible path has zero events in F, the scope contains no cut hitting all paths.

Given independent Bernoulli **basic event IDs** with externally specified rational failure probabilities q_e, a separate small-model oracle enumerates event subsets and reports probability at least one *static listed* plan survives. Shared event IDs encode a common cause acting on multiple paths. Neither this calculation nor the pair indicator measures resource-consuming dynamic restoration.

## C.3 Deterministic negative and positive controls

| Predeclared physical interpretation | Raw G1 GBR gain | Guarded R1 pair | Small event cut |
|---|---:|---:|---:|
| Two names for ONE physical channel, ONE failure event | 1 | 0 | 1 |
| Two genuinely separate implementations, independent events | 1 | 1 | 2 |
| Two differently labeled power sources representing ONE grid event | 1 | 0 | 1 |
| Optical/wired routes with common power excluded (protected) | 1 | 1 | See model |
| Same alarm routes with shared power exposed | 0 in expanded raw scope | 0 | See model |

With a basic-event failure chance of one half, two aliases for one failed channel have modeled static survival **1/2**, whereas two independent channels have **3/4**. These are exact constructed numbers, NOT observed reliability.

## C.4 Scientific status and acceptance boundaries

The attached code [R1 ontology audit](../experiments/fault_ontology_r1.py) and [tests](../tests/test_fault_ontology_r1.py) provide explicit identifiers, conservative missing-coverage handling, exact static cut/reliability baselines and alias/split/common-power controls. Failure scope and evidence would need to be **registered before** measuring any actual system.

R1 is **not invariant under arbitrary refinement**, does not check policy-equivalence under inventory consumption or interrupted actions, does not infer event identities from data, and does not model correlated basic-event indicators except through a *declared common event*. All practical ontology/provenance claims remain unvalidated. Reviewer Issues #9 and #12 remain OPEN.
