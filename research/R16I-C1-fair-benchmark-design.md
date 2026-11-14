# R16-I / C1 — Matched-information and all-in-compute benchmark admission design

**Date:** 2026-11-14. **Status:** C1_BENCHMARK_PROTOCOL_ONLY / toy arithmetic and logical controls passed only if CI passes. **No actual comparator algorithms were run in this change, no real wall-time or RSS measurement was collected, no independent held-out field systems were tested, and H1 remains DRAFT_NOT_PREREGISTERED.**

## 1. Scientific question and boundaries

Before any new primary H1 test, ask whether the historical R1 pre-fault *physically scoped pair* feature adds predictive utility over the **best defensible standard method under the same information and overall computation budget**. A deterministic feature Z=f(X) has **no additional theoretical information** over a full input X to an unrestricted oracle; any claimed advantage must be finite-compute/finite-sample/finite-model-capacity and survive conventional augmented-state benchmarks.

- Primary *draft* outcome: conditional strict **same-history** reacquisition of a previously active goal **after actual fault-caused loss** by a fixed deadline under a fixed nonanticipative policy. Terminal presence or node administrative repair alone is **not** an acceptable substitute.
- Primary *draft* additional feature: historical **R1 scoped physical-pair** constructible backup, with mechanism identities requiring independent physical corroboration. R10 joint-readiness, B1 GOG, and B2–B6 observer effects are **separate exploratory variables**, never silent replacements after outcome inspection.
- Unit of generalization: independently sampled **physical system**, with repeated failures nested inside each system. Distinct toy grammar labels or repeated probabilities on one structure are not independently sampled units.

## 2. Planned paired comparator suite

Each arm receives exactly the same pre-fault raw model X and predeclared scenario prior, target, resource budget, controller observation contract and horizon. Use the same training-only standardization, model class/capacity, tuning budget and group-split. Every augmentation must pay its feature construction cost from a **single all-in budget**.

| Method | Required substantive implementation in a **future C1 runner** | Interpretation |
|---|---|---|
| \`raw\` | unaugmented pre-fault source features | essential comparator |
| \`topology\` | ordinary AND/OR arity, bottlenecks, dependency structure, stock | conventional structural features |
| \`resource_reachability\` | ordinary non-generative bounded-resource reachability | strong finite-state comparator |
| \`physical_event_cut\` | externally justified basic-event footprints, cut/hitting-set proxies, common-cause risk | reject mere action-name alias as physical independence |
| \`augmented_state_dp\` | standard finite-state, fault-aware nonanticipative policy/backup preparedness feature with same source input | **primary conventional challenger** |
| \`r1_scoped_pair_candidate\` | historical fixed pre-fault R1 scoped pair feature, with source mechanism/provenance costs counted | **primary draft candidate** |

The exact full-known-world probability oracle is a **diagnostic ceiling**, not automatically a matched training-cost comparator. If conventional DP cannot finish under the prospective hard budget, record **abstention/timeout and coverage** on both arms; do **not** lower the comparator's input quality or declare a win from incomplete reporting. If R1 remains constant as in R8, report the negative finding; do not post-hoc substitute the different R10 feature.

## 3. Fairness and measurement contract

Prospective execution must freeze: (a) raw pre-fault input hashes for **every method**, (b) original physical system groups and structural signatures so train/tune/test do not reuse the same system, (c) feature versions and exact source fault-event ontology, (d) one common prediction deadline, fixed observation/policy rule, (e) identical learner family, regularization/search budget, training partition and tuning partition, (f) a **hard per-arm CPU/wall-time and peak-RSS memory limit** and explicit timeout/abstention scoring, and (g) separate feature, fitting and inference resource accounting **all included**.

A time budget consumed by an expensive feature is not available for training an enhanced model. Actual C1 execution should run benchmark methods in supervised isolated processes, capture process-exit status/timeout/peak memory, code revision/compiler/platform, and preserve both successful and failed comparisons in an independently reproducible artifact. Define behavior on partial predictions and missing eligibility **before** any confirmatory outcome access.

This PR's executable \`experiments/p1_r16i_c1_matched_benchmark.py\` intentionally uses **declared abstract integer work tokens** and completely **placeholder-not-executed** method specifications. Its 1-second / 256-MiB demo budgets are just declared validation fixtures; **no process timing, memory cap enforcement, training or prediction algorithm execution occurs**. Passing the C1 validator therefore proves *only protocol consistency*, not fairness of any actual implementation or real measured speed.

## 4. Scoring and inference contract

For each independently sampled system i with eligible actual-loss episodes j, use the prespecified per-system weighted conditional Brier

    B_i(method) = sum_{eligible j} w_ij (p_i,method - y_ij)^2
                  / sum_{eligible j} w_ij

where p is pre-fault and has **not** observed the realized fault or outcome, y is true strict restoration (0/1), and w is declared sampling/scenario weight.

Then compare the candidate and baseline on **matched same systems**:

    Delta = mean_{independent eligible systems i}
            [B_i(DP baseline) - B_i(R1 candidate)]

Positive Delta would favor R1 on this one properly executed predictive task. A system with zero actual eligible losses has an **undefined** B_i: report it and do not score it as recovery 0 or 1. Censored/unknown-risk endpoints are excluded from naive developer arithmetic, but a real study cannot simply discard informative censoring and claim a population parameter. Real inference must prespecify how to handle follow-up, competing risks, cluster uncertainty and missingness.

Future prospective confirmation requires system-cluster uncertainty (e.g. independent-system bootstrap or other justified hierarchical method), coverage/timeout rates, a **preregistered practically meaningful effect floor**, test-family independence checks, negative control data and sensitivity to topology encoding. No confidence interval or p-value is computed by the manufactured C1 fixture. Never treat each fault rollout as a new independent system.

## 5. What the executable C1 checks — and does NOT

The C1 checker asserts:
- all five required conventional arms plus the unchanged R1 candidate and declared endpoint;
- identical raw-information digest, learner/capacity, fixed policy, train/tune/test design and pre-fault feature timing;
- group identity/signature disjointness **within manufactured entries** (not physical independence proof);
- declarative all-in feature+fit+predict budget plus explicit timeout rule;
- exact Fraction-valued paired **per-system** scoring with genuine-loss eligibility, distinct censored/no-loss/unknown statuses and correct null when no eligible units;
- failure on a fabricated future-case feature, missing DP/cut baseline, swapped primary feature, duplicated system, extra clairvoyant comparator labelled fair, changed capacity, overbudget, or a false measurement/preregistration claim.

The artificial scoring fixture consists of 5 labelled toy systems (one TRAIN, one TUNE, three TEST) with **2 TEST units eligible** and **one TEST unit not eligible**. All forecast values are manufactured as 1/2, so paired DP–R1 toy gain is **exactly zero**. This is a test of the arithmetic and stopping behavior, **not a training result or validation of method quality**. The method names in this report are placeholders, not algorithms that actually ran.

## 6. Decisions and stop rules

**C1-DESIGN PASS (this PR):** syntax, negative cases, group-level arithmetic and full regression pass; reviewer accepts information/budget definition as a **proposal**.

**C1-EXECUTION BLOCKED:** until actual versions of each conventional baseline and the historical feature are implemented on a *single fixed task*, both observed with real time/RSS/timeout limits and independent held-out groups, do not claim any empirical performance edge. A positive developer-toy gain is never confirmation.

**H1-FIELD BLOCKED:** until B7 independently instrumented original evidence or another independently credible same-goal loss/recovery source passes physical provenance and lineage, and the experiment is separately preregistered before holdout access.

**Falsification:** zero R1 variation/zero benefit, stronger conventional performance at comparable all-in compute, overbudget feature costs, information leakage, common-cause/alias artifacts, or sensitivity to arbitrary representation must be reported as boundaries or negative evidence, not repaired by swapping metrics post hoc.

**Reproduction:**

    python -m unittest tests.test_p1_r16i_c1_matched_benchmark -v
    python -m experiments.p1_r16i_c1_matched_benchmark
    python -m unittest discover -s tests -v

Work alongside independent [B7](R16H-B7-independent-testbed-feasibility.md). H1 status and archived [R8 negative](R8-development-summary-seed20261101.json), [R11](R11-unknown-time-prediction-results-20261102.json), [R12](R12-cross-grammar-results-20261102.json), [R16 source protocol](R16-lanl-publisher-usage-event-lineage-protocol.md) remain unchanged. Scientific Issues [#3](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/3) and [#8–#12](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/8) remain open.
