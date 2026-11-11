# R16-F / B5 — Strict same-history restoration with lagged sensing and censored follow-up

**Date:** 2026-11-11. **Scientific status:** PROVISIONAL_SYNTHETIC_RESTORATION_CONFORMANCE, **not** H1 preregistration, not physical validation, not independent inference and not a new scientific law. Successor to [B4](R16E-B4-hidden-fault-policy-conformance.md). All fixtures are designed by the researcher; the original R8 negative result and sealed P1/H1 families are untouched.

## 1. Why terminal presence is insufficient

B4's primary bounded solver asked whether a target was *held at the terminal horizon*. That mixes (i) a service never damaged, (ii) a service recovered after genuine loss, and (iii) a service constructed for the first time. The original H1 target is much stricter: **the same previously active goal must actually be removed by the fault and subsequently reacquired on the same executed nonanticipative policy history by deadline**.

This B5 gate changes the **developer-only outcome definition** without modifying B4 or the P1 primary feature. It does **not** silently reinterpret B4 terminal-goal probability as strict restoration or upgrade synthetic labels to field evidence.

## 2. Exact finite profile

Reuse B4's finite, predeclared exogenous \`World\` and exact rational scenario weights: G2 atomic one-tick actions; a hidden fault at an unknown tick 1 or 2 of a horizon H=2 or 3, applied **before** the command at its tick; no artificial fault-occurred notification. A separately declared observation projection reports capability presence and resource stock. Each scenario has a known synthetic prior but its identity and realized future fault time are unavailable to the acting policy.

B5 deliberately restricts the goal vocabulary to **one named goal** and action grammar to **one non-generative \`repair\` action whose output is that goal**. This is an engineering diagnostic slice, not a general model of multi-step construction, policy optimization, resource-identical paths or asynchronous repair.

A **single fixed, observation-reactive policy** operates under lag \`d in {0,1,2}\`:

1. At decision tick t, the *evaluator* applies any event, records actual pre-command state, and stores a projected snapshot.
2. The **policy** sees only the projected snapshot from tick \`max(0, t-d)\`; it is not passed the privileged true loss flag, scenario label, disabled-action set, current unseen state, or future fault time.
3. If the **delivered** goal indicator is present, issue \`WAIT\`; otherwise issue \`repair\`. An illegal repair is rejected by the diagnostic executor and consumes a tick, matching B4's tester semantics. No override based on hidden faults is allowed.
4. The evaluator updates the actual physical-model capability/resource state. A repair issued at tick t completes at tick t+1. The simulator's true state is **used only to score outcomes**, not for policy decisions.

Lag is deliberately applied to the **entire publicly projected pre-command snapshot**, not to a privileged instantaneous fault detector. Acceptance/rejection is not independently provided to this narrow controller; extending its information set is a separate study. In this model only one synthetic exogenous event occurs. No noisy sensors or probabilistic missingness are yet simulated.

### Privileged per-scenario labels

Let \`g\` be the *same* declared target, \`tau\` its scenario's fault tick, \`H\` the deadline tick and \`F<=H\` the inclusive follow-up cutoff. The evaluator records:

- \`held_before_fault\`: goal is true **immediately before** application of the scenario event on that execution;
- \`lost_at_fault\`: goal was held before and is false **immediately after** the fault;
- \`first_regained_tick\`: earliest \`u>tau\` at which the goal becomes held again on that **same executed policy trajectory** (not an existential alternative), including completed one-tick repair;
- \`held_at_deadline\`: separate diagnostic, never itself a recovery label.

Then \`status\` is:

| Label | Exact meaning |
|---|---|
| \`NOT_AT_RISK\` | No true fault-caused loss of the previously held goal. A retained service is **not** counted as restoration. |
| \`RESTORED\` | Actual loss and verified same-history reacquisition by \`min(F,H)\`. |
| \`CENSORED\` | Actual loss but no reacquisition observed by follow-up cutoff \`F<H\`. Whether recovery eventually occurred cannot be inferred from that censored observation. |
| \`NOT_RESTORED\` | Actual loss, no reacquisition by **complete** deadline follow-up \`F=H\`. |

The simulator can know a synthetic run's eventual recovery even if it is hidden by the cut-off; the reported outcome still stays **CENSORED**. This is a test of label generation. In a field study, eligibility itself would require verified pre-fault goal status, fault-caused loss, matching job/service identity, credible action logs and follow-up provenance; this implementation proves none of them.

### Aggregation is not inference

B5 reports exact prior mass of each of the four statuses, the true synthetic fault-loss risk-set mass and the subset with observed determinate endpoints. It optionally prints the *descriptive observed-case* ratio \`mass(RESTORED)/(mass(RESTORED)+mass(NOT_RESTORED))\`. If the denominator is zero, this field is **null, never zero**. The ratio is NOT promoted to a population recovery probability: censoring may be informative and the toy scenario weights are stipulated, not sampled.

## 3. Deliberate adversarial checks

Three synthetic scenarios use \`P(early actual loss at t=1)=1/2\`, \`P(late actual loss at t=2)=1/4\`, and \`P(unaffected)=1/4\`, with H=3 and one legal service repair.

| Observer lag | Restored mass | Failed with full follow-up | Not at risk | Illustrative observed-case fraction |
|---|---:|---:|---:|---:|
| 0 ticks | 3/4 | 0 | 1/4 | 1 |
| 1 tick | 1/2 | 1/4 | 1/4 | 2/3 |
| 2 ticks | 0 | 3/4 | 1/4 | 0 |

When **follow-up ends at tick 2** instead of H=3 with lag 0: early loss recovery remains visible (1/2 mass), late recovery is **censored** (1/4 mass). The observed-case fraction becomes **1**, but this does **not** establish that shorter follow-up improved the policy or represents an unbiased estimate. With lag 1 and cutoff 2, **all** actual-loss mass (3/4) is censored and the observed-case fraction must be **null**.

Other negative controls: a never-damaged goal with terminal presence is NOT_AT_RISK; a goal never active before the fault is NOT_AT_RISK; a truly lost goal with repair disabled is NOT_RESTORED only when full follow-up is available, otherwise CENSORED. A status difference is not invented by reading scenario IDs into the policy.

Two mechanically distinct executors are required to agree **on every scenario, lag and follow-up cut-off**: (1) the B4 transition helpers with immutable states and (2) an independently programmed mutable-set/dictionary chronology with separate legality and action updates. They share the declared fixed profile, not transition code. Agreement is synthetic software verification, **not independent scientific replication**.

## 4. Limitations, stop rules and next gate

- **Known synthetic priors and deterministic rules only.** No independently observed failures, source checksum attestation, node-job join, real physical mechanism identities or controlled field interventions. LANL R16 source verification remains a separate evidence-track problem.
- **One fixed policy only; no optimal policy under delay.** Neither causal claims about observation systems nor general stochastic policy equivalence follow. Terminal possession and individual fault repairs must not be substituted for same-goal recovery.
- **Censoring is a follow-up observation convention**, not random dropout generation, survival modeling, propensity weighting or proof of independent censoring. A missing or unverified actual-loss label in physical data is an admission blocker, not a synthetic negative.
- **Lagged sensing does not automatically model noisy observations, controller action logs, sensor time synchronization or real checkpoint/restart identity**.
- **No premature promotion:** P1/H1 remains \`DRAFT_NOT_PREREGISTERED\`, no sealed sample access, no confirmatory sample; R8 negative and R11/R12 development status remain unchanged. Existing R3/R7/B4 results are not modified.

Reproduction:

    python -m unittest tests.test_p1_r16f_b5_strict_restoration -v
    python -m experiments.p1_r16f_b5_strict_restoration
    python -m unittest discover -s tests -v

**B5 exit:** green focused and full regression plus reviewer confirmation that strict loss, first reacquisition timing, observer lag and censoring remain distinct. **B6 proposal:** extend the information model to explicit noisy/late measurements, policy-command logs and deadline-conditioned censoring with a conventional belief-state comparator, then use a separately instrumented synthetic or physical controlled testbed for an independent data feasibility gate. Do not conflate this with preregistration or declare Issues [#3](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/3), [#8](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/8), [#9](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/9), [#10](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/10), [#11](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/11) or [#12](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/12) resolved.
