# R16-H / B7 — Independent instrumented testbed feasibility and fail-closed evidence admission

**Date:** 2026-11-14. **Status:** FEASIBILITY PROTOCOL + SYNTHETIC STRUCTURAL CHECKS ONLY. No actual laboratory or physical system was controlled or observed, no independent data was collected, no publisher or custodian signature was verified, and no P1/H1 confirmatory assessment was conducted.

## 1. Why B7 replaces more synthetic feature exploration

B1–B6 identified concrete semantic distinctions (generativity, backup, commanded behavior, hidden fault observation, same-history reacquisition, delayed/noisy sensors and censoring). These are useful **software checks**, not independent proof that a possibility-dynamics feature beats conventional augmented-state reachability or that real systems have independently grounded route identities. R13–R16 LANL investigation cannot yet demonstrate the original service/job lineage required for H1. A new toy family alone would not resolve either limitation.

**B7 research question:** Can an independently witnessed, legally authorized, isolated fault trial produce the minimal pre-event snapshot, policy input/output, independent truth stream and same-goal reacquisition records needed even to contemplate a future preregistered **field** comparison?

This is **not** the experiment itself. R16-H only defines an evidence-acceptance envelope and fails closed when source provenance is unverified.

## 2. Candidate practical testbed (NOT built or operated here)

Use a **deliberately isolated laboratory** (not a production cluster or third-party LANL installation). Candidate: one host with two independent service execution workers and an independently instrumented monitor; an explicit goal is successful completion of the **same immutable work ID** or continued service predicate. All available construction/restart actions must be specified before injection; observer/logger, operator and policy owner should be distinct roles, with permission to inject an interruption. A controlled stop must not affect real users, safety-relevant services or external systems.

Before executing a single real trial, require an operationally approved runbook with: administrative authorization, isolation, rollback plan, resource limits, no real personal/user data, clock synchronization and uncertainty bound, fault/event identity and component incidence, unique work/service/run/attempt linkage, and an independent observer with an immutable receipt chain. Confirm the monitor can distinguish retained service from actual loss and restore the same declared goal. Failure to establish any of these is a **STOP** not an opportunity to backfill plausible identities.

Recommended *engineering pilot* is several short trials covering: real induced loss with same-goal reacquisition, loss with no reacquisition by full horizon, no-loss negative control, a short follow-up censored episode, and intentional missing-log rejection. These are **feasibility tests**, not statistical samples, evidence of a benefit, or registered H1 outcomes. No count is claimed completed here.

## 3. Evidence streams and contract

At least three distinct chains should be collected **without using evaluator truth to decide actions**:

| Producer | Required record | Trust boundary |
|---|---|---|
| Policy/controller logger | actual inputs delivered at each time, selected commands, dispatch/receipt acknowledgements, fixed policy version and prior authorized action set | MUST NOT contain fault ID, future observations or privileged evaluator status prior to the action |
| Independent truth assessor | authenticated pre-fault goal existence, event-induced loss, subsequent same-goal target state, deadline and independent work/service identity across attempts | MUST NOT be substituted by node-up or administrative fault-fixed time |
| Testbed/custodian and clock witness | independently verified exact archive hashes, hardware/work identity, fault injection permission, incident mechanism, UTC clock calibration/uncertainty, immutable chain of receipt and signer verification | a self-produced local SHA-256 alone does NOT authenticate this stream |

For a future real source, require verified signature or controlled custodian-attested original bytes by a trusted external reviewer; avoid leaking raw job identifiers into GitHub JSON. Preserve the full raw evidence outside the public repository under appropriate permissions. Evaluate units as **independently instrumented physical systems**, not correlated repeated runs on one system.

The dry-run \`B7_INSTRUMENTED_TESTBED_FEASIBILITY_V1\` envelope requires policy prediction freeze before the pre-event snapshot, an explicit event time, assessor truth before and after, one immutable service/trajectory link across roles, synchronized timestamps, delivered observation time no later than command time, actual controller decision and an explicit follow-up cutoff.

The Python checker can establish **only syntactic/chronological consistency** of a *self-generated synthetic envelope*. It cannot prove that the event really happened, the hardware paths were independent, a policy was followed without coercion or that a purported signer's key is trusted. It rejects claims of external attestation because this version contains **no trusted independent signature verifier**.

## 4. Endpoint and missingness

For a declared same goal:

- **RESTORED:** genuine goal held before the fault, lost at the fault, regained strictly afterwards on the recorded policy trajectory by follow-up.
- **NOT_RESTORED:** genuine loss with complete follow-up through the deadline but no regain.
- **NOT_AT_RISK:** fault was observed by the cutoff but did not cause loss of an active goal.
- **CENSORED:** loss was observed but follow-up ended before the deadline with no observed recovery.
- **UNKNOWN_RISK:** follow-up ended before the event, or risk eligibility cannot be independently verified. Missing truth/logs **block admission** rather than being assigned a negative outcome.

These are only synthetic structural labels in B7. Independent field scoring further requires independent provenance of the assessor stream and original work/service identity.

## 5. Explicit gate decisions

| Gate | Exit criterion | Status at creation |
|---|---|---|
| B7-S structure | Synthetic envelope passes timestamp, source/trajectory/goal, action, risk and censoring controls and negative tests | developer check implemented; CI required |
| B7-O operational authorization | isolated apparatus + accepted real-world authorization, rollback and safety plan | NOT DONE |
| B7-I instrumented source | independent assessor, controller stream, clock witness, signed/attested original logs, independently checked hashes and link identities | NOT DONE |
| B7-Q field study eligibility | external custodian confirmation, distinct units, protocol version, consent/permissions as needed, meaningful policy/action/fault observations | BLOCKED |
| B7-H H1 field eligibility | ALL above plus separately reviewed and **preregistered** primary H1 feature, test population, comparator, uncertainty, stopping rules and locked holdout before outcome access | SEALED |

Do not mark B7-I or B7-Q PASS merely because the same script calculates and verifies its own hash. Even an accurately signed synthetic trace cannot prove that any real trial happened.

## 6. Reproduction, review and next decision

    python -m unittest tests.test_p1_r16h_b7_testbed_feasibility -v
    python -m experiments.p1_r16h_b7_testbed_feasibility
    python -m unittest discover -s tests -v

The change **does not create a physical testbed, collect raw data, certify a custodian or release any held-out outcomes**. It preserves R8's zero-gain R1 developer negative; R11/R12 synthetic-only scope; R16 LANL raw/source limitation; and P1/H1 \`DRAFT_NOT_PREREGISTERED\`.

**Decision:** in parallel, implement C1's matched-information/capacity/**all-in computation** benchmark admission protocol. The first independent experiment should be prospective only if instrumentation and independent reviewer constraints can be satisfied. If no validated source/testbed is available, publish **field feasibility blocked** and keep an auxiliary node repair-duration study completely separate from H1. Review scientific Issues #3 and #8–#12; do not close them from a dry run.
