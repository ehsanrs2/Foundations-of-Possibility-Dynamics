# R16-A — Scientific architecture and decision roadmap (review candidate)

**Snapshot:** main `0a5e0613be7a30c5489c2bb0cfc864587aa47f29` (R15), reviewed on 2026-11-09.  
**Status:** `ARCHITECTURE_REVIEW_PROPOSED` — **not** an H1 preregistration, no change to scientific outcomes or sealed families.

## 1. One mission, three distinct claims

**Mission:** Explain and test how bounded operational capabilities can be *constructed, lost, preserved, and restored* when time, resources, physical dependencies and information constrain feasible actions. Do not conflate physically possible, operationally reachable, epistemically envisaged or desirable outcomes.

1. **P1/H1 — primary prospective *predictive* claim:** A specified pre-fault physically grounded constructible-backup feature might reduce independent held-out prediction loss for *strict restoration after actual loss* under one nonanticipative policy, over matched-information, capacity, training, and all-in compute conventional baselines. This is *currently a draft*, **not preregistered**. It is not a claim of new information over the full source model or a causal intervention effect. The R1 scoped-pair candidate and later R10 readiness feature are **different features**; changing the primary feature requires a new, openly revised protocol before confirmatory data access.
2. **GOG program — separate exploratory generativity claim:** When construction is optional under the same initial state and budget, count *newly reachable target predicates*, separately from multiple backup routes to pre-existing targets. Explore the sensitivity of `GOG` to action grammar, goal-universe choice, observation and resource limits. Nested-action-set monotonicity is **definitional/conditional**; useful prediction of future goal-space expansion or a compression advantage must be independently compared against standard augmented-state and dynamic-hypergraph methods. **Do not silently redefine H1 into GOG.**
3. **Intervention program — separate exploratory causal claim:** Changing available construction resources or permitted actions may change realized recovery, but different risk sets or policies can bias loss-conditioned comparisons. A causal estimand requires distinct intervention/randomization and interference assumptions. No causal finding is claimed.

## 2. Read the history without promoting development to confirmation

- **G0–G4:** verified bounded planning/causal-support/resource/fault/observation semantics; tiny software checks, not novel physical laws.
- **R1–R4:** physical fault identity constraints, individually versus jointly feasible construction, draft H1 endpoint and sealed-family guards.
- **R5–R9:** synthetic pilots and controls; **R8 found exactly zero added Brier value for the R1 feature** across the studied developer systems because the assessed feature did not vary.
- **R10–R12:** exploratory *different* joint-readiness feature is exactly expressible by conventional augmented-state reachability. R11/R12 show small development-side Brier improvements with repeated researcher-designed synthetic structures, **not** independent H1 confirmation or formal novelty. Exact full-known-model oracle is not a matched-capacity trained comparator.
- **R13–R15:** source descriptions, then R14's **third-party mirrored** LANL node failure file. Publisher original checksum and system-20 Usage/Event job lineage remain unverified. A node's administrative fix is not the original job's strict restoration. **Zero independently observed H1 field episodes**.
- **R16 PR #31** is a separate, currently draft, evidence-track *protocol document*. It adds no authenticated original bytes or evaluated job lineage. Keep it separate from this scientific-architecture PR.

## 3. Proposed semantic core (not an implemented API)

Maintain a versioned normative specification, then implement a shared model library only **after** reviewing behavioral equivalence against prior modules. Initial objects:

| Object | Contract to freeze | Risk to test |
|---|---|---|
| State | capabilities held, stock/inventory, environment, physical mechanism IDs, time | hidden information vs full state |
| Action/rule | AND-prerequisites, required stock, outputs, costs, duration, deletions | multiple rule aliases, competing resources |
| Shock | independently evidenced event identity, common causes, onset/end and action interruption | missing exposure; clock mappings |
| Observation and policy | observable history only; one nonanticipative action rule, observation delays declared | future-event leakage, automatic silent event announcement |
| Goal | externally specified target predicate and protected/potentially new goal vocabulary | GOG sensitivity to arbitrarily enlarged goal universe |
| Endpoints | retain vs lose vs restore **same goal** by deadline; censoring and undefined no-loss risk | treating node repair as service recovery |
| Feature and baseline | versioned R1/GBR/GOG/readiness implementations and standard DP/hypergraph/cut counterparts | computation, scale, representation invariance |

**Architectural direction:** split `core/schema` (immutable versioned semantics), `core/oracles` (exhaustive + augmented-state), `benchmarks` (fixed shared tasks/resources), `data_admission` (provenance and outcome joins), and `research` (claims/registrations). These are proposed packages, **not existing directories or already completed refactors**. Do not change R3–R15 results or import semantics as a side effect. Add metamorphic coarse/fine encoding, alias/common-cause and zero-eligible cases to the conformance suite.

## 4. Ordered gates and independent evidence track

| Gate | Purpose and measurable exit | Disposition when blocked |
|---|---|---|
| **A — scientific review** (this PR) | Signed-off distinction H1 vs GOG vs causal, traceable archived negatives, proposed core schema and falsifiers; reviewer Issues #3/#8–#12 cross-referenced | keep as review candidate; no freeze |
| **B — semantic conformance** | Versioned state/action/shock/observation/goal/endpoint contract; dual-oracle equivalence on tiny cases; documented differences between historical R1, R10 and GOG; metamorphic refinement controls | return to definitions, do not run confirmation |
| **C — competitive benchmark design** | Primary feature and endpoint selected *before holdout*; equal raw pre-fault information, all-in feature computation, matched compute and capacity; ordinary DP, dynamic reachability, fault-tree/path-cut/repair baselines; scaling and abstention/timeout rules | retain engineering-only findings, no novelty claim |
| **D — independent evidence feasibility** (parallel with B/C) | Either independently verified real job-goal/policy episodes, or a deliberately instrumented repeatable physical/controlled testbed with preevent state, actual fault, action and same-goal outcome; source hashes/permissions/identity documented | explicitly publish infeasibility; LANL node repair remains an **auxiliary** study only |
| **E — preregistration** | After B/C and critical independent protocol review: immutable commit/registered version; primary hypothesis, sample unit/size, effect floor, interval and negative controls; never inspect sealed outcomes before lock. For a *field* claim D is also required | P1 remains DRAFT; do not generate or inspect sealed cases |
| **F — confirmatory evaluation** | Only after E: untouched held-out families or independent measured units; report clustered uncertainty, practical effect, all timeouts, and negative findings; for field inference require D | no confirmatory result; no post-hoc replacement of primary feature |
| **G — synthesis** | Claims ledger, chapters and release scope updated based on accepted positive, negative or explicit feasibility result and independent criticism | publish as bounded method / inconclusive research, not a new discipline |

**Parallelism:** D's LANL audit need not block *designing* B/C or a future explicitly synthetic registered benchmark. But D is essential for any claim of independent *field* validation. R16 original/Usage/Event branch is a D input, **not** the central theoretical objective.

## 5. Decisions and stopping rules

- **Stop a new-theory claim** when a conventional equivalent representation reaches the same endpoint at comparable total compute, or when any alleged improvement relies on extra input/leaked future events, metric aliases, or a representation artifact. A useful bounded feature-engineering result may still be publishable.
- **Stop the current R1 primary-feature candidacy for the selected population** if it remains constant, unidentifiable or too costly. Preserve R8's zero-gain result; changing to R10 readiness is a **new prospective feature hypothesis**, not a correction to the R8 result.
- **Stop a LANL-to-H1 join** when original-job/attempt identity, same-goal loss/reacquisition, policy/actions and clocks cannot be validated. Carry forward only a separately named node administrative-fix duration question, with new endpoint and protocol; do not call it H1.
- **Stop an apparent GOG result** if its gain disappears under sensible goal-vocabulary/behavior-preserving encoding, or if a standard model gives the same value more cheaply; never infer 'new physical laws'.
- **Allow a negative scientific conclusion.** Absence of incremental predictive benefit under valid prespecified tests is a publishable boundary, not justification for swapping outcomes post hoc.

## 6. Immediate implementation and verification

**This R16-A PR adds** the roadmap, a machine-readable decision manifest, a fail-closed audit against R8/R11/R12/R15 and P1 archived scientific status, and regression tests. It **does not** create independent reviewer approval or finish gates B–F.

Next actionable work after review: **B1** draft normative semantic contracts and a compatibility table for G2/G3/G4/R3/R7/R10, with explicit GOG test fixtures; **C1** specify matched-budget conventional baselines; in parallel **D1** complete or explicitly close the publisher-original and Usage/Event feasibility investigation from draft PR #31. No retrospective test family is relabeled a confirmatory holdout.

## 7. Audit and provenance links

- Canonical mission: [Scientific motivation](scientific-motivation-and-boundaries.md); [novelty limitations](novelty-audit-v0.3.md); [GBR review](gbr-metric-audit-v0.3.md).
- Prospective **unregistered** H1: [P1 candidate](P1-H1-study-design-v0.1.md), [JSON](p1_h1_design_candidate_v0_1.json), [three distinct estimands](../appendices/D-predictive-estimands.md).
- Actual development archives: [R8](R8-development-summary-seed20261101.json), [R11](R11-unknown-time-prediction-results-20261102.json), [R12](R12-cross-grammar-results-20261102.json).
- Physical-data barriers: [R14 audit](R14-lanl-mirror-raw-audit-20261108.json), [R15](R15-original-source-and-job-lineage-gate.md), [R15 result](R15-node-job-lineage-results-20261108.json); R16 [draft PR #31](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/pull/31).
- Unresolved scientific reviewer [Issues #3](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/3), [#8](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/8), [#9](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/9), [#10](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/10), [#11](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/11), [#12](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/12).
