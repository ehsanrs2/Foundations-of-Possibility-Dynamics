# R16-G / B6 — Noisy sensing, delayed decisions and instrumented evidence firewall

**Date:** 2026-11-11. **Status:** B6_PROVISIONAL_DEVELOPER_CONFORMANCE. Not a preregistration, independently obtained physical result, causal estimate, or novel theorem. This intentionally preserves B1–B5, the negative R8 result, and all sealed H1 test families.

## 1. Research purpose

B5 established an explicit truth-based distinction among same-history restoration, absence of actual loss, fully followed failure and censoring. B4/B5 assumed deterministic or simply time-lagged observations. B6 asks the narrower engineering question: **can noisy readings and delayed delivery be represented without leaking actual fault identity, unseen current state or future observations into the controller, while producing independently checkable labels and auditable evidence boundaries?**

This gate is an exact small synthetic **one-goal/one-repair** model. It does **not** estimate real-world sensitivity, specificity, censoring mechanisms or service restoration rates. It is not another primary H1 feature and does not replace the predictive/causal distinction of [R16-A](R16A-scientific-architecture-and-roadmap.md).

## 2. Frozen B6 operational profile

Use [B4](R16E-B4-hidden-fault-policy-conformance.md) finite G2 transition semantics and [B5](R16F-B5-strict-restoration-lag-and-censoring.md) loss truth labeling:

- A true goal indicator is present initially. A declared hidden event at tick 1 (or a model-supported hidden tick before H) can remove it; event application precedes the tick's observation and command.
- H is 2–3 one-tick decisions; the B6 test fixture uses H=3, a one-kit inventory, one ordinary \`repair\` action costing one kit, with 1/2 actual service loss and 1/2 inert event. Rational scenario weights are *stipulated*, not estimated.
- At each decision tick t, **after** any fault and **before** command, the evaluator privately records the true goal state \`G_t\` and draws a sensor report \`Y_t\`, with independently stipulated conditional probabilities:
  - \`sensitivity = P(Y_t=present | G_t=present)\`
  - \`specificity = P(Y_t=absent | G_t=absent)\`
- Conditional on each current true goal state, the sensor errors at separate ticks are independent. A past sensor error can change future **true** states because the policy reacts and may spend inventory; therefore the exact joint noise-path probability must be computed **sequentially** from the realized synthetic history. No assumption of independent future true states is made.
- Sensor reports sampled at t are **delivered at t+d**, where lag d is an integer 0, 1 or 2. Prior to the first delivered sample the policy receives \`None\`, **not** a fabricated current-value reading.
- The one fixed controller chooses \`repair\` only when the delivered report explicitly says \`absent\`; otherwise \`WAIT\`. It receives neither the scenario name nor hidden event timing/true state. A command may fail due to resources or disablement; its **acceptance is logged after execution**, not used by this particular controller for current action choice.
- Fault truth, noisy collection, delayed delivery, observed controller decisions and strict endpoint truth live in **distinct fields**; privileged evaluator data cannot be interpreted as a controller input.

This is a **measurement and execution grammar**, not a verified physical sensor, general POMDP, learned observation model, stochastic restoration effect estimate or real control policy.

## 3. Correct endpoint and missingness taxonomy

Record whether the **same** target was held immediately before the actual fault, whether it was removed *by* that fault, and whether it was regained at an action-completion time strictly after that fault on the **same** policy execution. Endpoints are reported relative to an inclusive follow-up tick F and horizon H.

| Status | Meaning |
|---|---|
| \`RESTORED\` | The goal was truly lost and reacquired by observed F. |
| \`NOT_RESTORED\` | The goal was truly lost and **complete** deadline follow-up F=H saw no reacquisition. |
| \`CENSORED\` | True loss was established, but restoration had not occurred by F<H; its later status cannot be inferred from the observed window. |
| \`NOT_AT_RISK\` | F covers the actual fault and the goal was **not actually lost** by that fault. Retained terminal service is not recovery. |
| \`UNKNOWN_RISK\` | F ends **before the actual event** and even risk eligibility cannot be established from the observed follow-up. Do not mark \`NOT_AT_RISK\` from a future privileged truth record. |

**Important clarification to B5:** The B5 synthetic \`NOT_AT_RISK\` category was computed from full privileged history even when a requested follow-up cutoff preceded the fault. B6 introduces an explicit \`UNKNOWN_RISK\` category for that subcase, **without retroactively rewriting B5 results or H1**. Physical datasets with uncertain event timing, missing loss evidence or incomplete episode identity require an equally conservative admission decision.

The observed-case descriptive fraction \`P(RESTORED)/[P(RESTORED)+P(NOT_RESTORED)]\` is only an arithmetic summary of the stipulated toy scenario masses. It is **null** if no determinate at-risk endpoint is observed and is not an estimator of a physical recovery probability under informative censoring.

## 4. Exact synthetic controls

Each policy/noise scenario enumerates all 2^H faithful/incorrect sensor sequences with exact \`fractions.Fraction\` weights. An immutable B4-transition executor and a **separately programmed mutable-set/dictionary replay** must agree for each scenario, observation delay and follow-up cutoff, including policy log, true goal samples, first reacquisition and risk status.

Under the stipulated H=3, two-scenario testbed:

| Observation contract | Restored mass | Fully followed non-restored mass | Not at risk |
|---|---:|---:|---:|
| Perfect, zero lag | 1/2 | 0 | 1/2 |
| Sensitivity 1/2, specificity 1, zero lag | 1/4 | 1/4 | 1/2 |
| Sensitivity 1, specificity 1/2, zero lag | 3/8 | 1/8 | 1/2 |
| Perfect, one-tick lag | 1/2 | 0 | 1/2 |
| Perfect, two-tick lag | 0 | 1/2 | 1/2 |

In the **first noisy row**, a false absence signal at tick 0 wastes the single repair kit **before** the real loss at tick 1. It is *not* evidence that a real sensor with 1/2 sensitivity causes a general 50% decline. In the **second noisy row**, a false presence signal after true loss delays repair; the following tick offers a further opportunity.

With perfect sensing and follow-up F=1, the actual-loss half is **CENSORED**, not a negative outcome. With F=0, **all** scenarios are \`UNKNOWN_RISK\`, not \`NOT_AT_RISK\`. These are explicit negative controls against information leakage and missingness misclassification.

## 5. Instrumented evidence separation and provenance discipline

B6 creates a deterministic **synthetic evidence record** with two segregated logs:

1. **Public controller log:** tick, delivered goal report (\`true\`, \`false\`, or \`null\`), selected canonical command and post-command acceptance. No fault time, scenario name, actual loss flag or future sensor sample.
2. **Privileged evaluator log:** declared scenario identity, fault tick, recorded true pre-command goal presence, sampled values, actual loss, first same-goal regain, horizon and follow-up status. This log is used for scoring only, not controller decisions.

The record has a canonical-JSON local SHA-256 for **byte-level repeatability and detecting modification relative to a previously trusted digest**. It does **not** authenticate an upstream publisher, provide an independently signed timestamp, validate physical equipment identity, establish independence between physical routes, or prove that a submitted log was recorded during real operation. Recomputing a checksum after falsifying a record is not prevented by an untrusted self-generated digest.

For a **future independently instrumented study**, separately demand: external testbed/custodian ID, independently witnessed fault injection or trusted incident record, synchronized clock calibration, immutable original job/service identity, configuration snapshots, sensor provenance and calibration, actual controller observation and command logs, receipt acknowledgements, fixed action permissions, independently logged same-goal loss/regain, declared deadline/follow-up and missingness mechanism, external-signature or publisher-chain evidence, plus blinded assessment where feasible. These requirements are an **admission checklist, not achievements of B6**. The LANL original/Usage/Event verification program remains an independent track and must not be relabeled as service restoration simply because its archive hash exists.

## 6. Pass and stop criteria

The gate passes **developer-only conformance** if and only if: source/observation timing is correct; all exact prior-weighted outcome masses sum to 1; the two independent replay implementations agree on every tested noise word; all risk statuses (including unknown eligibility) are disjoint; controller logs contain no privileged truth; changed logs fail verification against unchanged digest; no field/H1 status is promoted. Cross-check with full historical repository CI.

Do **not** use the output to support H1, causal claims, or quantitative real-world generalization. Its results cannot set a confirmatory effect floor or tune a primary feature after exposure to sealed H1 families. Historical R8 negative, R11/R12 developer-only observations, P1/H1 \`DRAFT_NOT_PREREGISTERED\` and zero accepted physical H1 samples remain unchanged.

To reproduce:

    python -m unittest tests.test_p1_r16g_b6_noisy_sensor_evidence -v
    python -m experiments.p1_r16g_b6_noisy_sensor_evidence
    python -m unittest discover -s tests -v

**Next decision (B7 / C1):** resist adding increasingly elaborate toy mechanisms without outside evidence. Design a genuinely *independent, instrumented testbed feasibility study* and a matched-information, all-in-compute standard comparator with prospective frozen hypotheses. If physical trace identity, sensor calibration, action auditing or full follow-up cannot be obtained, document the failure openly and keep empirical H1 closed. Relevant unresolved scientific Issues: #3, #8, #9, #10, #11 and #12.
