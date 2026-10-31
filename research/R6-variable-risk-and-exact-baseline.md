# R6 — Variable, explicitly stipulated fault risk and full-information reference

**Status:** DEV-ONLY methodological and software gate, 31 October 2026. **NOT an empirical failure model, preregistered H1, or a tested GBR improvement.**

## Why R5 was insufficient

The [R5 pilot](R5-development-pilot.md) gave every system exactly three service-loss cases of four equally weighted cases: its reported 75% loss eligibility was **hardcoded**, not an empirical event frequency. It also lacked a pre-failure full-input reference predicting strict recovery under one fixed executable policy.

R6 removes this *specific artificial 3/4 eligibility design* by making the service-loss risk vary over systems. It does **not** estimate those risks from physical data. All event probabilities below are **invented diagnostic input values** and must not be treated as actual engineering failure rates.

## New developer-only generative fault model

For each R4 TRAIN/TUNE system, derive a separate deterministic PRNG seed from SHA-256 with domain prefix R6-DEV-RISK-V1 and the system's family/index. This seed chooses:

- Basic event S: immediate loss of the service goal; probability from {0, 1/8, 1/4, 1/2, 3/4};
- Basic event C: loss of a common prerequisite (base, or hub in the hub family); probability from {0, 1/4, 1/2};
- Basic event K: destruction of one consumable kit; probability from {0, 1/4, 1/2}.

The three binary basic-event indicators are **assumed independent within each synthetic system**. Their joint effect on different routes can be coupled because event C disables a common dependency. With an independent, equally weighted early/late fault time, enumerate up to sixteen nonzero-probability cases and apply the union of event effects **at one boundary only**. This is a single joint event at the boundary, not a sequential event process with separate arrival times.

All realized cases are registered with exact rational probabilities. R3 observes only current capabilities, stock, disabled actions and the event boundary. The scenario identity and future time are hidden from the fixed policy. R6's exact reference integrates **over** all possible cases before their realization; it never conditions the feature/predictor on the actual future event.

**Important R3 modeling defect to keep visible:** even an event vector (S,C,K)=(0,0,0) generates an *observable scheduled boundary signal* in the current R3 interface. This is a null-effect event, not a physically nonexistent incident. A genuinely silent no-event history, uncertain event detection or partial sensor observations would require a revised execution kernel. This remains a scientific blocker.

## Strict restoration and risk-set audit

The service goal is initially held and can only be removed by event S. Consequently:

\[
P(L=1 \mid X)=p_S,
\]

where L means **actual loss at the event boundary**, and p_S is the **chosen synthetic** event probability. It is no longer 3/4 for every system and can be exactly zero.

When p_S = 0, the conditional outcome \(P(\text{restore}\mid L=1,X)\) is **undefined**. Such systems must not be encoded as failures or included with an invented conditional target. R6 records the number of zero-risk systems separately for each developer family.

When p_S > 0, R6 computes the fixed-policy, pre-failure strict-restoration probability

\[
p^*(X)=\frac{\sum_\omega w_\omega L_\omega R_\omega}
{\sum_\omega w_\omega L_\omega}.
\]

R3's execution and independent-history implementation cross-check each realized path. This is a **model-defined exact conditional expectation**, not an estimated empirical probability. The predictor needs the whole declared pre-fault model X, including the prior distribution, as any fair GBR-based predictor would.

## A deliberately strong, familiar baseline

If the system's complete pre-failure dynamics, policy, deadlines and shock law X are all known and the tiny scenario enumeration is computationally affordable, the exact marginalized p*(X) is already the Bayes-optimal probability prediction for this specific synthetic conditional outcome under squared/Brier loss.

For any other pre-fault probability q(X),

\[
\mathbb E[(q-Y)^2 \mid X,L=1]
=p^*(1-p^*) + (q-p^*)^2.
\]

Therefore a deterministic added feature GBR(X) **cannot** lower this population conditional expected loss below p*(1-p*) when the comparator already uses complete X and is unrestricted. This is a standard consequence of conditional expectation, not a new theorem.

R6 additionally records a **sanity-check** squared deviation from a fixed 1/2 forecast; this constant forecast is **not** a defensible main equal-information benchmark and its relative performance is not counted as a win for anything.

The exact marginal may be more computationally expensive on large systems. An actual feasible comparison would budget all inference, model learning, GBR computation, memory and time against **capacity-/compute-matched** augmented-state and fault-event baselines, using independent held-out instances. None has been performed here.

## Reproduction and separation

Source: [R6 risk law and oracle](../experiments/p1_r6_fault_risk_dev.py) · [18 contract tests](../tests/test_p1_r6_fault_risk_dev.py).

    python -m unittest tests.test_p1_r6_fault_risk_dev -v
    python -m experiments.p1_r6_fault_risk_dev --seed 20261031 --train-n 24 --tune-n 12 --output r6_dev_only.json

The [R6 CI workflow](../.github/workflows/r6-risk-developer.yml) produces exactly 84 development-side systems, per-system risk-law and conditional restoration records, grouped profiles and a temporary raw artifact. No TRAIN/TUNE case is an untouched confirmatory sample; **spatial_lattice** and **hierarchical_common_cause** remain entirely unimplemented and no held-out system or outcome is generated. Repeated event cases within a system do not increase the number of independent sampling units.

### Limits and decision

R6 removes the fixed 3/4 artificial incidence rate of R5, but the **new risk distribution is still synthetic by design** and therefore cannot estimate natural failure incidence, causal effects, risk-law goodness of fit or external predictive performance. Zero-risk eligibility is detectable, and a standard full-input model-based reference is now explicit.

Before scientific preregistration the program still needs a defensible physical event ontology, genuinely independent risk observations or calibrated domain evidence, robust handling of censored/non-detected events, policy/feature semantics locked before test data, full method/compute parity, independent generator families, sample size and a falsifiable effect threshold. Keep Issues #3, #8, #9, #10, #11, #12 open.

**Scientific verdict:** a measurement/design gate, not confirmation that Possibility Dynamics is a distinct science or that GBR predicts better than existing methods.


## Executed developer diagnostic results — 2026-10-31

The [R6 PR workflow run](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/actions/runs/41198411855) passed, producing the [R6 developer-only raw artifact](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/actions/runs/41198411855/artifacts/13040739409). The [summary JSON](R6-development-risk-summary-seed20261031.json) is also retained in the repository so the numerical findings do not depend only on a temporary artifact.

A total of **84 tiny developer systems**, **820 full-history equivalence checks** and **zero sealed or confirmatory examples** were used. The number of case executions is no longer fixed at four per system: only positive-weight event combinations are enumerated.

| Development family | Independent developer systems | Zero-loss-risk systems | Mean *designed* loss probability | Mean exact conditional restoration for eligible systems | Mean ideal Brier risk for eligible systems |
|---|---:|---:|---:|---:|---:|
| Random AND/OR | 24 | 3 | 11/32 | 1/3 | 67/336 |
| Modular clusters | 24 | 6 | 59/192 | 5/18 | 11/64 |
| Hub dependencies | 24 | 3 | 61/192 | 29/84 | 45/224 |
| Temporal bottleneck | 12 | 4 | 5/24 | 5/16 | 5/32 |

There are **16 zero-risk systems and 68 positive-loss-risk systems** overall, as determined by the deliberately chosen synthetic hazard family. This variation is useful for testing undefined conditional outcomes but **must not** be interpreted as 16 observed failure-free real-world systems or 68 actual failures. The reported Brier values are *exact known-model conditional expected risks* from the stipulated scenario distribution, **not fitted predictor scores or GBR gains**.

Unlike R5's uniform 3/4 loss-risk design, each system now has an explicit variable p_S, but all p_S values were still **chosen by a PRNG from human-authored probability categories**. The experiment improves the *internal measurement design* only. No calibrated real-data uncertainty, scientific generalization, or novelty claim follows.
