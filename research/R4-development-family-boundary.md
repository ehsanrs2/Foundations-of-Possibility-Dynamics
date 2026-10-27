# R4 — Development-family generator registry and held-out boundary

**27 October 2026 — DEVELOPMENT SOFTWARE GATE, NOT PREREGISTERED P1 AND NOT H1 EVIDENCE.**

This gate addresses an implementation dependency in the [prospective P1 design](P1-H1-study-design-v0.1.md): family names had been proposed without any executable family grammars. The [R4 generator](../experiments/p1_r4_development_families.py) now implements ONLY the first four development-side proposals, using the already reviewed [R3 execution engine](../experiments/p1_r3_policy_rollout.py). No H1 predictor is trained.

## Allowed development partitions

| Purpose | Family ID | Declared variation (synthetic, not an external domain) |
|---|---|---|
| Train | random_AND_OR | variable conjunctive input support for two substitute preparations |
| Train | modular_clusters | left/right module alternatives and a cross-module bridge |
| Train | hub_dependencies | shared hub prerequisite and conditional rebuild operation |
| Tune | temporal_bottleneck | slow multi-tick preparation vs a faster stock-intensive route |

The two proposed **sealed confirmatory families** (spatial_lattice and hierarchical_common_cause) are represented by identifiers only. No generators, cases, seeds, fingerprints or outcome distributions for them are created; attempting to call the development builder with either identifier raises PermissionError **before** deriving a seed or constructing a model. This is a good-faith workflow guard inside the repository, **not an access-security boundary** and not a way to prove the absence of all outcome peeking.

All four implemented grammars share G2's one-tick atomic actions, durable capabilities, one integer kit stock, horizon and a single fault. Goals are initially held so an actual loss can be measured; exactly four developer fault cases are declared with equal rational probability. Three cases delete the service capability, and one is a retained-service negative control. Cases vary their shock tick and can destroy stock, disable one repair operation or remove a common prerequisite.

**Important**: because three of four constructed cases remove service, the eligible-loss fraction is **designed**, not estimated from external system behavior. Case data and exact distributions have already been inspected by developers and cannot serve as untouched prospective confirmatory test samples. No claim that these four families represent independent real-world domains is justified.

## Reproducibility and independent experimental units

A caller supplies (family, master integer seed, nonnegative instance index). An SHA-256 digest over a fixed version prefix and those three values generates each instance's independent pseudorandom stream. This avoids Python's process-salted hash and avoids directly reusing the same seed for different family/index pairs. The generator provides a public seed fingerprint and a deterministic structural-model fingerprint. These fingerprints are **audit labels, not proof of statistical independence**: independence follows from the sampling assumptions, not from hashes, and PRNG-derived samples can still share design structure.

The correct experimental sampling unit is the **system instance**, with multiple shock cases nested within it, consistent with Appendix D. Four shock cases from one generated network must never be treated as four independent systems in a statistical test.

## Policy and outcome restrictions

R4 reuses R3's fixed deterministic, fully observing priority policy. Every action is listed exactly once both before and after the event, with restoration actions prioritized after the event. This policy is a **developer heuristic**, not a learned/optimal controller and **not the preregistered final evaluation policy**. No future scenario identity or event time is available through its observation interface.

Two independent R3 implementation paths compare whole executed histories for every development case. Outcomes are strict same-history actual-loss restoration or undefined for non-loss. To avoid accidentally treating developer fixtures as scientific training results, R4 records diagnostic counts only and carries the explicit label DEVELOPMENT_DIAGNOSTICS_NOT_H1.

Run:

    python -m experiments.p1_r4_development_families
    python -m unittest discover -s tests -v

The default bounded smoke runs **3 systems per family**, 12 developer system instances total and four cases each, yielding **48 full-trace oracle comparisons**. It does not construct held-out family datasets.

## Scientific blockers that remain

1. These developer grammars are tiny, share a common simulation engine and are not validated against engineering, hydrological, agricultural, biological or other external processes.
2. The named sealed-family generators are **not implemented or calibrated**. Do not set family_definitions_implemented=true in the P1 manifest.
3. A pre-outcome physical fault-identity ontology, a resource-aware GBR/R1 feature with admitted representation semantics, and matched conventional baselines have not been validated.
4. The R3 priority policy, fault observation assumptions, primary restoration risk set and family acceptance criteria are not frozen.
5. No independent sample-size calculation, practical effect floor, statistical decision rule, sealed random registry, or external protocol review is complete.

**Decision:** the R4 code improves reproducible *developer* experimental infrastructure, but cannot be used to announce H1 results or declare the prospective P1 study registered. Reviewer Issues #3, #8–#12 remain OPEN.
