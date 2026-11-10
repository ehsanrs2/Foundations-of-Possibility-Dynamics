# R16-D / B3 — Deterministic command-response equivalence and policy implications

**Date:** 2026-11-10. **Status:** `B3_PROVISIONAL_DEVELOPER_CONFORMANCE`. This is a bounded modeling/software audit, **not** a novel theorem, physical validation, H1 preregistration, or an assertion that the architecture review has been signed off independently.

## 1. The scientific question

[B1](R16B-core-semantics-contract.md) distinguishes the count of newly reachable goals (GOG) from alternative backup routes or simultaneous attainability. [B2](R16C-B2-bounded-trace-equivalence.md) compared the **set** of possible observable capability/inventory traces, hiding which actions produced them. Two systems can have identical B2 languages yet respond differently when a controller sends the **same action command**. This matters for the claim that an equivalence is valid for an implementable policy rather than merely for existential reachability.

The B3 result is deliberately stronger than B2 **only in one narrow deterministic no-fault profile**. It cannot yet settle the critical policy/bisimulation/physical identity concerns of [Issue #10](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/10) or the broader representation question of [#12](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/12).

## 2. Exact contract: what is observable and controlled

Reuse the **existing** G2 unit-tick, immutable capability, AND-precondition, integer stock, generative-action-flag transitions with **no effective shock** (`Fault(tick=0, remove=∅, destroy=0, disable=∅)`). Preserve the same fixed horizon and resource coordinates/stocks in both models. Only a finite goal vocabulary and a declared injective projection of source capability names into common *canonical observable* indicators are observed; stock is always fully observed.

A **separately declared bijection** maps source action identifiers to one common canonical command alphabet. This mapping identifies *tester commands only*: it is **not** a physical-equipment/causal-identity attestation. Each tick, the controller issues one command from that alphabet or `WAIT`. If legal according to its construction arm, prerequisites and stock, the action executes for one tick. Otherwise the B3 **diagnostic tester** records `REJECT`, leaves state unchanged and advances one tick. This rejection is not a property of the existing deployed R3/R7 policies, which instead try to choose only legal actions.

For command word `w=(a_0,...,a_{H-1})` define the deterministic response:

```
Resp_M,k(w) = (visible(s_0),
               (accepted_0, visible(s_1)), ...,
               (accepted_{H-1}, visible(s_H)))
visible(s)  = (visible canonical capabilities, ordered stock vector)
```

`k` is either E0 (generative actions prohibited) or E+ (generative actions optionally legal). We compare the complete map `w -> Resp_M,k(w)` over **all** canonical words of length H and both arms. A model pair is `B3-equivalent` iff these two maps are equal, under a common canonical visible goal vocabulary, observation projection, command alphabet, horizon and initial resources.

### Conditional finite-policy implication

**Elementary consequence, with exact limits:** If both command-response maps are equal, every deterministic controller that selects canonical commands as a function **only of the common past visible replies** receives the same visible history on both systems through H, assuming the controller starts in the same internal state, uses the same rule, and its commands belong to the common alphabet. **Proof:** at time zero observations match; if histories match up to t, such a controller selects the same next command. Equality of the response map for that common command prefix yields the same acceptance and next observation. Induct to H.

This does **not** prove state bisimulation, preservation of unobservable private states, equivalence under exogenous random/hidden faults, information-set changes, arbitrary environment choices, different policy families, cross-domain transfer, or that observed equal success came from the same physical device. Deterministic fixed scripts are included in the bounded controller class. No claim about a full history-dependent stochastic controller follows without an explicit event/observation process.

## 3. Adversarial B2-equivalent / B3-non-equivalent fixtures

All are **developer-constructed**, not independent physical systems.

| Case | B2 existential projected trace languages | B3 command-response verdict | Why |
|---|---|---|---|
| Same model vs itself | equal for E0 and E+ | equal | exact reflexivity check |
| Two labeled commands `primary` and `probe`; in one system both produce `service`, in another `probe` is a self-loop | equal E0/E+ | **different** E0/E+ | The unordered set of visible histories hides which command created the service |
| `primary` and `probe` both produce `service`, but their kit costs are swapped between models | equal E0/E+ | **different** E0/E+ | B2 cannot recover which action consumed the kit, even though it observes stock |
| Bijective capability/action rename with explicit public canonical maps | equal E0/E+ | equal E0/E+ | a legal representation change preserves command meaning under the declared mapping |
| One fixed reactive policy: send `probe` first; if service is still missing, `primary` next, else `WAIT` | B2 equal in the underlying pair | **different realized policy commands and visible time paths** | An actual nonanticipative controller can distinguish operational effects despite equal existential trace sets |

**Crucial counterexample:** In the first differing pair, the same fixed observer-reactive policy sends `(probe, WAIT)` in one system but `(probe, primary)` in the other. It sees only current/past visible goal and stock. The divergence is due to the action semantics, **not** use of future event information. This establishes that B2 trace-set equality alone cannot justify a claim about fixed-policy operational equivalence.

The result does *not* claim physical independent channels because canonical tester commands may still be aliases for a single component. That question remains governed by R1's externally verified physical fault-event ontology.

## 4. Precise limitations and computational work

- Limits: `H <= 3`, `actions <= 4`, `goals <= 3`, inherited B1 resource/stock caps, at most **625 command words** (maximum in this profile is 125); every attempted action is included, even if currently illegal, to expose enablement differences.
- Complexity: worst-case number of words `(|A|+1)^H`; this is an **exact exhaustive tester**, not a scalable representation-compression result. Both arms rerun the tester. Timeout/cap refusal means *unassessable*, never inequivalent.
- Observation scope: all declared goal indicators and integer stock are visible, but hidden capabilities, disabled equipment, physical event incidence, noisy sensors and delayed observations are not represented.
- The complete B2 trace comparison is run for each B3 pair. B3 equality is asserted not to coexist with B2 inequality under this shared profile. This is an executable consistency implication of the respective definitions, not external validation.
- R3 and R7 historical policies are **not modified**; the B3 diagnostic `REJECT` is a new interface for testing legality, not an instruction to force failed actions onto production controllers.
- The fixed `ReactivePolicy` object accesses only a tuple of public observation snapshots. It is a small example, **not** all nonanticipative stochastic policies.

## 5. Scientific barriers unchanged and next step

- **R8** negative original R1 incremental development result remains intact; **R11/R12** small engineering gains from ordinary augmented-state readiness are development-only. No new feature is installed as P1 primary.
- **H1** remains `DRAFT_NOT_PREREGISTERED`; 0 confirmatory samples, no sealed-family generation. B3 reports *no predictive accuracy, causal effect, physical novelty or field validation*.
- **LANL R16** publisher-source/Usage/Event lineage work is independent; node administrative fix remains distinct from recovery of the original work.
- The architecture [R16-A](R16A-scientific-architecture-and-roadmap.md) was merged as a roadmap, not an independent signoff of Gate A; B3 is **provisional**.

**Reproduce:**

```bash
python -m unittest tests.test_p1_r16d_b3_policy_response -v
python -m experiments.p1_r16d_b3_policy_response
python -m unittest discover -s tests -v
```

**B3 review gate:** confirm deterministic command-response equality and all negative controls, command-name mapping and tester-rejection semantics; label the scope correctly. Next is **B4**: introduce a predeclared hidden stochastic fault and observable action/goal signal, compare full **observation-based nonanticipative policy trees** under common exogenous scenario laws, and independently check a conventional augmented-state solution. Add explicit common-cause physical identities only when externally justified. Only then reconsider any shared `core/schema` refactor. Scientific [Issues #3](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/3), [#8](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/8), [#9](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/9), [#10](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/10), [#11](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/11), and [#12](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/12) remain open.
