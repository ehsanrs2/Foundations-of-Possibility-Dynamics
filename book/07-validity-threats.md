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
