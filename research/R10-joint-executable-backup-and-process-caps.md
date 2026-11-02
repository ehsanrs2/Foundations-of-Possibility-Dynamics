# R10 — Jointly executable pre-event backup and shared process caps

**Status: bounded synthetic construct-validity and implementation gate; NOT preregistered H1, NOT a domain-validated metric, and NOT a prediction contest. 2026-11-02.**

## Objective and interpretation

R8 established a **negative** development result (a narrowly scoped static R1 backup feature was identically zero on 84 small TRAIN/TUNE systems and yielded zero incremental predictive Brier reduction). R9 exposed why individually feasible event-disjoint static backup routes can still be useless under a shared stock/time budget. Neither earlier result is revised or reinterpreted in R10.

R10 defines a **new exploratory operational notion**, intentionally distinguished from the archived R1 scientific candidate:

> Two event-disjoint physical repair routes are *jointly preparable* if there exists ONE lawful, non-anticipative pre-event action prefix whose jointly held state contains both route-enabling channel capabilities, while satisfying all shared kit constraints, per-action duration and the available preparation window.

This is a conventional **finite augmented-state reachability property**, NOT a new mathematical theorem. It does not, on its own, prove resilience under future failures or validate the predictive H1 hypothesis.

## Two logically separate readiness questions

1. **Existential jointly preparable:** Does *some* permitted pre-event prefix prepare two truly fault-event-disjoint mechanisms? This is computed by [standard state-layer DP](../experiments/p1_r10_executable_backup.py) on full (capabilities, shared stock) states and checked by an **independently coded exhaustive action-history DFS** with mutable inventory. The witness lists the required pre-event action sequence. If physical incidence is aliased/common or the state search cannot finish within the explicit state cap, the code must NOT invent an independent backup.
2. **Ready under the single fixed policy:** Does the specific R9 deterministic, observation-limited policy *actually* prepare both mechanisms? This is computed by applying only the current pre-event policy observation interface, not consulting future shock labels. It is not automatically equivalent to the existential property on arbitrary systems. The six tiny R9 fixtures happen to coincide under the chosen priority order.

Both require a declared [R9 physical mechanism ontology](../experiments/p1_r9_physical_controls.py): the two delivery actions must correspond to distinct mechanisms and disjoint **nonempty** basic fault-event footprints. Merely different action labels are insufficient. In the alias and common-cause fixtures, both physical route capabilities might be prepared, yet **the scoped independent-backup indicator must still be zero**.

The property is tied to R9's **known shock boundary**, a single fault, perfect and immediate knowledge of the current capabilities and kit stock, one-tick atomic actions and at most four legal actions. No claim is made for unknown shock timing or partially observed realistic systems.

## Explicit development controls

| R9 predeclared fixture | Individually feasible static R1 | Jointly executable physical pair (R10) | Known-model R7 strict restoration |
|---|---:|---:|---:|
| Two independent channels, one kit and two preparation ticks | 1 | **0** | 1/2 |
| Two independent channels, two kits and two preparation ticks | 1 | **1** | 3/4 |
| Two independent channels, two kits but one preparation tick | 1 | **0** | 1/2 |
| Two names for the same physical channel | 0 | **0** | 1/2 |
| Two physical channels with an upstream common-cause fault | 0 | **0** | 9/16 |
| No available kits | 0 | **0** | 0 |

These are constructed exact expectations under stipulated probabilities, not empirical physical observations. **R10 does distinguish** the first two systems that R1 could not distinguish. This is a limited *construct discrimination* result; it does **not** show any incremental prediction advantage over a standard state-space representation. Indeed, the exhaustive independent reference and the normal augmented-state DP intentionally compute the **same property**. This direct standard-method correspondence is an important **negative novelty control**.

## New enforceable subprocess limit — and exactly what it does NOT establish

R9 only counted an abstract number of simulated timeline ticks in its standard rollout. R10 adds a stronger, genuinely **enforced Linux subprocess boundary** to three methods, run separately under identical limits:

- Static physically scoped R1 support enumeration;
- Augmented-state joint preparation search, including state construction and relevant ontology validation;
- Conventional known-model scenario enumeration / R7 policy rollout.

Each worker constructs the same unaltered R9 fixture inputs itself. Its interpreter startup, imported modules, feature construction, evaluation and serialization fall under a **5-second parent wall-time deadline**, a **5-second Linux CPU-time limit**, and a **256-MiB virtual address-space (RLIMIT_AS) cap**. Statuses distinguish success, wall-time expiry and child failure; they do not silently replace a cap exceedance with a negative result. Worker CPU consumption and peak resident set on Linux are measured alongside all-in observed worker wall time, and **not treated as deterministic performance numbers**.

These caps are **identical limits**, not identical *actual work or task*. CPU-time RLIMIT_CPU is coarse-grained; RLIMIT_AS constrains virtual address space, not directly peak resident memory. The three computations produce **different outputs**: an individually feasible structural score, an executable-prefix feasibility indicator, and a known-model exact recovery probability. R10 therefore **does not compare predictive Brier losses, fitted models or equal-information H1 prediction under a shared learning budget**. Also, a six-fixture exact calculation is not a scalability evaluation.

The independent DFS verification and the historical R9 complete-trace verification run outside the subprocess budget as reproducibility checks. They are not silently included as competing inference costs.

## Reproduction

    python -m unittest tests.test_p1_r10_executable_backup -v
    python -m experiments.p1_r10_executable_backup --output r10_dev_full_records.json

The [dedicated R10 workflow](../.github/workflows/r10-executable-backup.yml) executes the full toy control with bounded Linux processes, uploads a short-lived raw record including **non-deterministic resource measurements**, and prints a stable summary that intentionally strips wall-time/CPU/RSS measurements. A separate archived stable JSON can be checked for exact rerun equality, while still collecting raw timing variations to avoid claiming machine-independent speed.

## Scientific decisions and unresolved gate

R10 operationalizes two independent backup paths under shared material and temporal constraints on tiny synthetic fixtures. This succeeds as a correctness/interpretation check and **is explicitly equivalent to ordinary bounded augmented-state reachability**, not independent scientific innovation. It must not be retrofitted into R8's negative result or silently substituted as the original H1 feature. A new prospective H1 feature hypothesis, if desired, needs a separate immutable preregistration and independent data.

The next scientifically adequate experiment needs independently justified physical event IDs, observed or validated hazard distributions, unrestricted sensor/observation specification, unknown fault times, a resource-aware **pre-failure** feature with a fixed computation budget, and properly matched predictive learners on held-out independently sampled systems. The sealed families remain untouched, and reviewer Issues #3 and #8–#12 remain open.


## Actually executed R10 developer controls — 2026-11-02

The initial [R10 development workflow](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/actions/runs/41393048336) succeeded: the 20 focused R10 tests passed; the six known artificial fixture cases produced exactly the predeclared joint readiness results and **all 18 separate Linux worker invocations** (3 distinct computations × 6 fixtures) returned PASS under **identical 5-second wall / 5-second CPU / 256-MiB virtual-address-space caps**. All six independently coded DFS/DP prefix comparisons agreed. The previous R9 check also independently compared **28 complete R7 scenario trajectories**.

| Exact designed fixture | Static R1 | Jointly executable fault-independent pair | Same fixed-policy readiness | Model-known conditional restoration |
|---|---:|---:|---:|---:|
| separate_one_kit | 1 | 0 | 0 | 1/2 |
| separate_two_kits | 1 | 1 | 1 | 3/4 |
| separate_short_window | 1 | 0 | 0 | 1/2 |
| aliased_same_mechanism | 0 | 0 | 0 | 1/2 |
| common_upstream_cause | 0 | 0 | 0 | 9/16 |
| no_kits | 0 | 0 | 0 | 0 |

**Positive but narrow construct discrimination:** the one-kit and two-kit independent cases both have static R1=1, but the new joint prefix feature is respectively 0 and 1. **Independent standard state DP and independent chronological DFS compute identical outcomes**. Thus this is a correct reformulation of conventional reachability, not a novel physical law or evidence of Brier improvement.

The exact JSON scientific results and fixed caps are retained as [the deterministic R10 archive](R10-joint-executable-results-20261102.json), with a regression test that regenerates and compares them. CPU consumption, all-in wall time and Linux peak resident memory **differ between environments and are intentionally omitted from the deterministic archive**; they remain in the per-run [raw Actions artifact](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/actions/runs/41393048336) subject to retention.

**Scientific boundary:** equal resource *limits* were enforced, but not equal CPU work, statistical training, output objective or predicted accuracy. None of these six constructed systems were sampled independently from a physical population; both the ontology and the event timings are toy assumptions. R8's archived zero-gain predictive comparison remains unchanged, and the H1 study remains unregistered.
