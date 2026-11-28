# R16-Q — GOG computational checkpoint and independent review request

2026-11-28. **Proposed research decision; not independent review or scientific acceptance.** Source main 9b647ec766694cbb9cf6fb1b90aac3a267ee829f, merged PR #47. Both GOG-1b and GOG-2a are merged. Preserve all historical results and the N1 pause.

## Evidence recovered from CI

The [archived summaries](R16Q-GOG2a-CI-summary-20261128.json) are parsed from the actual successful job logs for the [PR run](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/actions/runs/45611438837) and [merged-main run](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/actions/runs/46111841179). Each reports 28 developer fixtures, two action-permission arms, five exact methods, three process repetitions and 10 focused / 655 historical tests (historical count includes focused tests). Both runs reproduce the same integer work counters. The archive is the printed summary, not raw per-repetition data, signed provenance or independent replication. See the original workflow artifacts for raw output while retained.

| Method | PR CPU median ms | main CPU median ms | action checks | dominance checks | search calls |
|---|---:|---:|---:|---:|---:|
| state layers | 27.990821 | 20.994592 | 25718 | 0 | 56 |
| shared index | 22.996642 | 17.996220 | 10243 | 31808 | 56 |
| goal-wise index | 12.005228 | 8.996418 | 3329 | 1752 | 254 |
| fixed pairs | 13.997600 | 9.995484 | 4767 | 4117 | 130 |
| adaptive components | 16.994168 | 11.996382 | 5283 | 8596 | 199 |

The adaptive method uses fewer search calls than singleton slicing but performs more action and dominance checks, plus 516 pair tests, 55 merges and 1997 action-membership union inspections. It is slower in the reported aggregate CPU and process-wall medians on both runs. This is a **negative developer result for the proposed adaptive grouping against the conventional singleton comparator**, not a statistical rejection of all grouping methods. Fixed pairs have lower reported all-overlap-class query wall time than singleton in both runs. Counters describe different operations, not commensurate work units. Both runs use the same small designed cases; runner load and startup differ; no timing confidence interval or external-domain effect inference is available.

GOG-1a and 1b already established exactness under the bounded monotone, no-shock, unit-tick model and a trade-off in slice work. GOG-2a matches action counts and prerequisite arities, but changes prerequisites and resulting resource difficulty. It is not an isolated causal estimate of overlap. All algorithms are conventional search, projection, dominance, indexing or graph components. GOG is descriptive under a fixed goal ontology; individual attainability is not joint attainability.

## Decision Q1 (proposed)

Pause further adaptive grouping tuning on these developer cases. Preserve goal-wise indexed search as a scoped conventional engineering baseline, not a new theory. Do not infer general superiority, and do not change the grouping rule after these results and relabel the same suite a new test. No further tiny synthetic timing exercise is a prerequisite to a scientific decision.

The next high-value activity is independent critical review of the monograph, methods, and proposed claims. An independent reviewer should have a different role from the original code and hypothesis designer, record conflicts and version reviewed, and be free to recommend rejection. No such review has occurred in this PR. Keep issues #3 and #8–#12 open until separately justified.

## Review packet and exit criteria

| Track | Ask the reviewer | Minimum evidence to reopen or progress |
|---|---|---|
| Semantics (B) | Check projection lifting, action identity, goal vocabulary sensitivity, time/resource monotonicity and individual versus joint outcomes. | Explicit scoped statement and proof/counterexample review. |
| Predictive R1 (C/N1) | Review R8, C2a and N1's information loss, cut counterexample and negative comparisons. | A justified, prospective population with nonconstant, potentially useful R1; strong same-input baseline and meaningful effect criterion. Otherwise retire candidate transparently. |
| GOG efficiency | Review GOG-1a/b and 2a; does the claim survive ordinary planner search and encoding? | A prospective externally reviewed task/benchmark with diverse domains, fair resource accounting, stronger conventional solver(s), prespecified practical improvement, exact outcome preservation, repeated timings and timeout coverage. Otherwise retain descriptive GOG only. |
| Evidence (D/B7) | Can separate controller, assessor and custodian establish same-service loss/regain? | Independent isolated authorized apparatus, immutable raw logs, clock uncertainty, identity and attestation. Local owned-process pilot alone is insufficient. |
| H1 (E/F) | Is the claim and test population defensible after these negatives? | Independently reviewed, immutable preregistration before any sealed access; no replacement with GOG or R10. |

Recommend first a reviewer-facing synthesis of the core definitions and their relationships to conventional planning, control and reliability methods, with explicit negative findings and claim limitations. A literature comparison requires verified sources; this checkpoint is not that literature review. No independent testbed is available to this workflow, no physical evidence admitted, H1 remains DRAFT_NOT_PREREGISTERED and sealed families remain untouched.

## Reproducibility

Run python -m unittest tests.test_p1_r16q_gog_review_archive -v to check archived summary consistency only. To rerun the actual benchmark, run python -m experiments.p1_r16p_gog2a_components on Linux. Do not expect the archived times to recur exactly. No new benchmark or tuning is introduced here.
