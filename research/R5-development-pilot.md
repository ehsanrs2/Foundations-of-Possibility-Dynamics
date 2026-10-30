# R5 — Exploratory developer-family pilot and policy sensitivity

**Status: DEVELOPMENT-ONLY EXPLORATORY DIAGNOSTICS; NOT H1 OR CONFIRMATORY PREREGISTRATION. Date: 30 October 2026.**

## Objective

The [prospective H1 design](P1-H1-study-design-v0.1.md) currently contains important unverified assumptions about the denominator for *actual loss*, the appropriateness of the fixed policy and computation budgets. R5 gathers explicitly **developer-only** diagnostic records from the four small R4 grammars. It DOES NOT train a predictor, evaluate GBR as a predictor, estimate out-of-family generalization, or establish performance of realistic systems.

## Sampling and separation

R5 deterministically creates **24 independent developer system instances per TRAIN family**, for three TRAIN families, and **12 developer instances from the TUNE temporal family**: 84 artificial systems. Each has exactly four *deliberately constructed* scenario cases of probability 1/4. Because exactly three cases remove the initially held service goal, eligibility mass is **3/4 by design in every generated instance and policy**. This is an audit of the model contract, **not an estimate of the incidence of failure in any actual population**.

The independent unit is the **system instance**. The four fault cases, three policy variants and any other observations from it are all nested. R5 uses one fixed master seed (20261030) and R4's family/index-specific SHA-256 seed derivation.

The two SEALED-family identifiers (spatial_lattice and hierarchical_common_cause) are never given to a builder. They remain unimplemented, and no confirmatory test seed, instance, outcome or independent-domain data are generated. Code-level refusal is not secure data isolation; the full eventual protocol and immutable test selection must be reviewed before a confirmatory study.

## Policy sensitivity, not a feature/predictor contest

Every generated system and every declared fault case is evaluated with exactly **three deterministic, non-anticipative policy variants**:

1. **R3_original**: R4's existing priority policy — generally prepare before a fault and prefer restoration actions after observation.
2. **prepare_first_after_fault**: identical pre-fault decisions, but action priorities after the event favor preparation over restoration.
3. **construction_disabled**: original priorities with optional capability-generating actions disabled. This is an E0-style illustrative ablation, NOT the strong conventional full-state predictor baseline required for H1.

Each policy is run on an actual R3 trajectory. Outcomes are either strict recovery of a goal actually lost at the fault, failure to recover such a goal by the deadline, or **undefined** for no actual loss. The policies receive current state only, not future shock time or identity. The same system/fault cases are reused for policy contrasts to avoid confounding changes in input scenarios.

A separately coded chronological R3 history oracle checks **each full trajectory**. For eligible actual-loss cases, the standard G3 augmented-state solver is checked as a *clairvoyant feasibility diagnostic* only: its result is never a deployable policy, fair predictor or scientific benchmark establishing GBR's utility.

## Recorded observables and interpretation

For each developer system × policy × scenario, preserve the source seed/model fingerprint, eligible status, exact rational scenario weight, strict restoration (0/1/null), G3 feasibility-only flag, time of fault, number of selected actions, kit inventory **consumed by actions** and kit inventory **destroyed by the fault**, separately, and policy decision horizon. These are needed to audit failure cases and identify resource bottlenecks.

For each family × policy report: number of independent developer systems; number with any eligible actual loss; mean per-system eligibility mass; **conditional** restoration among eligible cases; mean of per-system conditional restoration; pooled descriptive conditional restoration (distinct if eligibility masses differ); average resource/action use. Zero eligible systems must be reported and their conditional outcome remain null, not coded as 0.

The output includes a measured elapsed wall-clock for this exact interpreter/run, but this is **not** a controlled compute/memory benchmark and is excluded from deterministic summary comparisons. Strong baselines, equal compute caps, sampling distributions and realistic external fault mechanisms remain to be specified.

### Reproduce

    python -m unittest tests.test_p1_r5_dev_pilot -v
    python -m experiments.p1_r5_dev_pilot --seed 20261030 --train-n 24 --tune-n 12 --output r5_dev_pilot.json

On pull requests and main, the workflow [R5 development pilot](../.github/workflows/r5-development-pilot.yml) executes these steps, emits a machine-readable summary and uploads a **development-only** raw JSON artifact under the name r5-development-only-not-h1. This artifact is intentionally marked non-confirmatory and short-lived.

## Known methodological weaknesses

- The 3/4 eligibility fraction is hardcoded via the R4 case design, so this pilot **cannot inform the empirical prevalence or sampling precision of actual-loss events**. It can check restoration and policy sensitivity conditional on these constructed cases.
- All four families share the same simulator, service goal, initial holdings, kit stock model, priority policy interface and only differ in a small dependency grammar. Their separate labels do **not** establish independence across scientific domains.
- The R3 fixed policy is arbitrary and no policy here has been tuned to predict or maximize actual restoration. Comparing these policies explores specification sensitivity, not a causal intervention effect.
- The G3 oracle knows each fault in advance and can make decisions the executable policies cannot; it is not an equal-information predictive comparator.
- The static R1-scoped feature is not computed here. Even positive recovery in this developer pilot **cannot** support H1; no Brier comparison or inferential p-value is reported.
- Elapsed runtime is platform- and scheduling-dependent. No fixed per-instance wall-time/RAM cap, scalability guarantee, or estimate of real-system runtime follows.

## Preregistration implications

The R5 developer pilot may motivate revisions to **training-side** policy choice, family diversity and primary denominator design. Such revisions must be documented and frozen **before** inspecting any true confirmatory holdout outcome. The prospective JSON continues to declare DRAFT_NOT_PREREGISTERED with ten unresolved gates; the two SEALED family generators and future test sample sizes are not implemented.

In particular, the artificially fixed eligibility fraction highlights a **serious limit** of the current design: any future scientifically meaningful risk-set analysis must justify its fault sampling frame and the observed fraction with actual pre-shock goal loss. Without this, a precise descriptive fraction here can be misleading.

**Scientific status:** infrastructure and software checks only; no conclusion about GBR novelty, predictive advantage or causal resilience. Issues #3 and #8–#12 stay open.
