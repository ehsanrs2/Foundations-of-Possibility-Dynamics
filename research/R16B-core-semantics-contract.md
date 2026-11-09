# B1 — Versioned operational-semantics profile and historical compatibility

**Date:** 2026-11-09. **Status:** `B1_PROVISIONAL_DEVELOPER_CONFORMANCE`, **NOT a final universal semantic freeze**. R16-A Gate A is still `UNDER_REVIEW` in its machine-readable manifest; merge of a roadmap is not independent scientific approval. **No preregistration, no sealed family access, no empirical H1 evidence.**

This proposal implements the first tiny compatibility slice of the [R16-A roadmap](R16A-scientific-architecture-and-roadmap.md): a deliberately **no-shock, finite, action/resource-bounded GOG query** on the already published G2 model. It neither redefines G1/R1 GBR nor changes the old G2/G3/G4/R3/R7/R10 code. It is designed to expose semantic collisions before attempting a new shared `core/` library.

## 1. Scope and operational objects

The **long-term** model considered in [Chapter 3](../book/03-formal-foundations.md) has state `s_t=(C_t,r_t,e_t)`, legal actions, transition kernel/relation and time/resource horizon. Different legacy executors only implement *subsets* of that abstract model. The following is a precise **B1_GOG_G2_NO_SHOCK_V1** subset:

| Domain concept | B1 developer contract | Explicitly not established |
|---|---|---|
| State | finite held capability set and nonnegative integer resource vector | physical world state, uncertainty, continuous dynamics |
| Rule/action | unique action name; finite AND prerequisites, output; one-tick action; nonnegative consume/yield vectors; `generative` bool | actual equipment/causal evidence, multi-tick interruption |
| Environment/fault | single **zero-effect** boundary vector at tick **0**, no removed capability, disabled action or stock loss | actual fault process or real node repair |
| Horizon | discrete ticks `0..H`; H ≤ 6 in diagnostic | scalable or optimal real-time planner |
| Controls | each arm may wait; `E0` bans generative actions, `E+` optionally allows them; same initial state, resource budget, model and target vocabulary | fixed nonanticipative policy evaluation, interventions causing real resilience |
| Goal | externally declared fixed set `G` of target **capability membership predicates**; *each* can be witnessed at some tick by a different legal history | simultaneous attainability, value/desirability, unforeseen goals |
| Output | `R0`, `R+`, and `GOG = |R+ \\ R0|` for the SAME model, goal universe, time and resources | GBR, restoration probability, causal effect, ontic emergence |

The optional construction arm **nests** the baseline arm, so `R0 ⊆ R+` is required. B1 rejects any nonzero fault, changed clock or empty goal query rather than accidentally importing G2 **post-fault availability** and calling it pre-shock generativity. B1 allows only a small oracle workload (H ≤ 6, ≤ 8 actions, ≤ 2 resource types, each initial stock ≤ 4); these are engineering limits of this test, not general-theory assumptions.

**Semantics note:** a goal is attained if it is *ever* held at or before `H`. Two different goals can be attained along mutually exclusive executions. Their inclusion in `R+` does **not** imply a single history reaches both. In particular, GOG is **not** a probability and its numeric change under an externally altered goal vocabulary is not necessarily a failure of behavioral invariance.

## 2. Historical implementation compatibility — no silent translation

| Layer | Model/observable | Endpoint and information | B1 compatibility |
|---|---|---|---|
| **G2** | one-tick operations, durable capabilities, integer inventory, one shock at start of a tick | existential post-shock target availability, even without preceding loss; no policy history guarantee | **Direct subset**: use G2 with an inert tick-0 fault; G2 state-layer and chronological enumeration must match |
| **G3** | G2 plus per-history lost-target flags and augmented state | distinguishes availability, retention, existential strict restoration and joint goal presence; uses foresight for a known fault | **Direct subset only for availability**: compare G3 augmented `available` with G2 results; do not infer strict restoration from this no-shock query |
| **G4** | G2 with known shock time, scenario distribution, common nonanticipative pre-shock prefix and scenario-dependent recourse | joint post-event attainment and clairvoyant diagnostic upper bound, not G3 strict restoration | **Different estimand**: no automatic conversion into GOG or H1 |
| **R3** | G2 + one deterministic fixed action-priority policy | one *executed* trajectory, genuine lost-then-reacquired target; event-observed signal, not future foresight | **Different outcome**: loss-conditioned strict restoration on same history; this is not existential goal gain |
| **R7** | R3-compatible fixed policy but detection depends on actual observable state changes | invisible no-effect fault cannot announce itself; complete instant state sensing, not partial/noisy measurement | **Separate observation profile**: cannot merge R3's event-announcement behavior with R7 without explicit version change |
| **R10** | physically declared event footprints, shared-stock nonanticipative preparation prefix for two routes; known synthetic boundary | joint pre-event readiness, calculated by conventional state DP and history enumeration | **Distinct representation** from GOG and R1, not a replacement for H1's primary feature |
| **B1** | inert shock at tick 0, G2 atomic action grammar and fixed goal vocabulary | existential per-goal `R+` vs `R0`, measured with ordinary G2/G3 algorithms | **GOG-only conformance**; no event/policy/recovery label generated |

## 3. Conformance examples and what they show

All examples are **deterministic and researcher-constructed**, not held-out populations.

1. **New operational goal:** `seed` + a kit permits a generative `bridge`, followed by an ordinary `service` action. With two ticks `R0=∅`, `R+={service}`, so **GOG=1**. With one tick or zero kits **GOG=0**.
2. **Backup only:** add a direct non-generative route to `service`. Both arms already reach `service`, so **GOG=0** despite construction adding an alternative action sequence. This is why GOG cannot substitute for GBR.
3. **Separate versus joint:** build `g1` or `g2` for one kit each with only one kit. `R+={g1,g2}` and **GOG=2**; ordinary G3 joint reachability remains **false** on a single shared-stock history. With two kits it becomes true within the same two-tick horizon. Do not interpret GOG as jointly executable goal capacity.
4. **Representation control:** add a second differently named action identical in input/output/stock effects and an inert self-loop. The reachable goal sets and GOG stay the same. This **does not** fix R1/GBR's false physical independence under aliased rules.
5. **Vocabulary dependence:** if the intermediate `bridge` is **explicitly added to the queried goal set**, GOG changes from 1 to 2. This is a **different estimand**, not a contradiction.
6. **Bijection:** bijectively rename the full capability vocabulary, including prerequisites, produced and target capability names; the GOG count is invariant. Nonbijective or incomplete maps must be rejected.

B1 uses **G2 state layers**, **G2 separate chronological history search**, and **G3 conventional augmented-state availability** on each same-input construction arm. Their agreement is a bounded software consistency check, **not three independent physical validations**. Representation equivalence under arbitrary coarse/fine reencoding, novel ontological categories and scaling remain **open**.

## 4. H1 and novelty firewall

- The P1/H1 primary *draft* is `R1_scoped_pair_pre_fault` predicting actual strict restoration after *actual* loss under one fixed nonanticipative policy. **B1 does not change this**.
- The R8 zero-gain negative developer result is retained. R11/R12's positive **small artificial development** results concern a different, conventionally computable joint-readiness feature, not a registered H1 test.
- R16's LANL publisher checksum and same-job lineage evidence obligations remain **independent**; B1 performs no file retrieval or observed job/repair matching.
- Any deterministic GOG feature computed from complete pre-event state information `X` has the same unrestricted-prediction information-redundancy limitation `Z=f(X)` as other deterministic structural features. A putative bounded-budget compression/prediction result requires a separate registered comparison with standard dynamic reachability/hypergraph methods.
- Historical data archives and official claim register **must not be rewritten** to make the new GOG fixtures look like confirmations.

## 5. Reproduction and exit gate

Run:

```bash
python -m unittest tests.test_p1_r16b_semantic_conformance -v
python -m experiments.p1_r16b_semantic_conformance
python -m unittest discover -s tests -v
```

The dedicated B1 workflow runs the focused and standard-library full-suite tests and uploads the diagnostic JSON; normal book CI also discovers tests. No field identifiers, secret data or sealed-family outcomes are produced.

**B1 exit remains provisional**, pending critical inspection of the full state/observation/behavioral-equivalence contract. B2 should explicitly define a *behavioral equivalence relation* for time/resource-preserving rule refinements (rather than simply rename invariance), compare multiple-action latency and partial observability profiles, and decide whether the new `core/schema` package is justified. C1 may then implement genuinely competitive fixed-compute baselines. D1 (original LANL Usage/Event authentication) proceeds in parallel, and must stop without H1 admission if unique same-job lineage remains unavailable.

**Reviewers should check:** [Issue #8](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/8) non-novel augmented-state equivalence; [#9](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/9) GBR alias; [#10](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/10) nonanticipation; [#11](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/11) separate estimands; [#12](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/12) encoding/refinement robustness. See [R16-A manifest](R16A-decision-manifest.json).
