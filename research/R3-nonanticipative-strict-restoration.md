# R3 — Same-history strict restoration under a fixed, non-anticipative policy

**2026-10-27. SOFTWARE / METHODS GATE ONLY. No P1/H1 confirmatory outcomes.**

## Why this gate is needed

G3 asked whether any perfect-foresight path could restore a goal; G4 optimized a non-clairvoyant preparation prefix but scored existential post-fault availability. [P1/H1 prospective design](P1-H1-study-design-v0.1.md) instead requires a concrete goal actually lost and then restored **along a single executable trajectory**. R3 supplies that narrower outcome kernel.

## Execution and information semantics

The kernel uses G2 finite durable capabilities and **consumable** integer inventory. Every action lasts one tick; an action needs its prerequisites plus affordable stock, and produces one durable capability with a declared inventory change. One fault is applied at its tick boundary BEFORE selecting that tick's action; it can delete held capabilities, destroy stock and disable actions. Fault time varies between scenarios and **is not exposed before the event**. No mid-operation faults or repeated events are modeled.

A fixed deterministic policy uses a priority ordering of named actions before and after the observed event. It receives current tick, presently held capabilities, available stock, **currently observed** disabled actions, and a Boolean flag that the event has already occurred. It receives **no scenario label, future fault tick, future failure effect or future trajectory**. The agent fully observes the consequences at the fault boundary. It picks the first currently legal action; if none, it waits. No claim of optimality or deployment suitability is made.

## Strict restoration definition

For each goal g and realized scenario, record the same trajectory's immediately **pre-fault** goal holdings B, then apply the fault and record actual goal losses L. Subsequently, after the same policy continues, record first time strictly **later than the fault** that a goal in L reappears. The strict binary label is:

- 1: goal held before the fault, removed BY the event, and regained by the deadline;
- 0: goal held before the fault, removed BY the event, and NOT regained by the deadline;
- undefined: goal not actually removed, including retained or never-held goals.

Each tick's pre-event state, post-boundary observable state, selected action, inventory and resulting state is retained. No eligible actual loss at any rollout means the strict conditional restoration score is **undefined**, never fabricated 0 or 1.

For externally stipulated scenario weights, conditional restoration is the weighted successes among ACTUALLY lost goals divided by the total weight of ACTUALLY lost goals. The denominator (eligibility mass) is reported separately. This is neither G4 joint post-fault goal availability nor observed real-world reliability.

## Independent verification and designed example

Two independent search-free **execution procedures** apply the identical fixed priority policy: one uses immutable capability sets and tuple-stock, the other a mutable set and dictionary-stock implementation. They compare complete per-tick traces. For each realized successful restoration, G3's full augmented-state **clairvoyant** solver must also find a feasible witness no later than the fixed-policy time. This is a consistency upper bound, not a fair predictive baseline.

A seeded developer audit checks 32 bounded G2 artificial systems, with 2 fault variants each, plus a 3-scenario illustration: **67 full-trace comparisons**. The illustration has equiprobable early loss (restored at t=2), final-tick loss (not restored), and non-loss (not eligible). Thus eligible loss mass is 2/3 and restoration conditional on loss equals 1/2. These are **exact fixture outputs, not measured frequencies**.

Reproduction commands:

    python -m experiments.p1_r3_policy_rollout
    python -m unittest discover -s tests -v

Source: [R3 execution kernel](../experiments/p1_r3_policy_rollout.py) and [R3 unit tests](../tests/test_p1_r3_policy_rollout.py).

## Scientific limits

The policy is a transparent heuristic, not a non-anticipative optimizer; the fault effects are immediately and fully observed; there is still exactly one fault, atomic one-tick operations and a bounded horizon. No real fault ontology is verified, no independently held-out family is generated, no learned prediction is trained, and no H1 evidence exists. The primary risk-set design and zero-denominator handling still need external review.

R3 is one **necessary operational step**, not a preregistration freeze. The protocol remains DRAFT, and Issues #3 and #10 remain OPEN. Do not silently equate its output with a fully general stochastic resilience metric.
