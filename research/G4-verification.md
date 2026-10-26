# Gate G4 — Non-clairvoyant prefix policies and equal-information controls

**Status: bounded exact model/software study, 2026-10-26. Not a confirmatory P1 experiment.**

## Motivation

G3 allowed its optimizer to know the exact future failure **before choosing actions**. That produces a useful theoretical upper bound but is generally not an executable resilience policy. G4 removes one specific form of look-ahead: a controller knows the **distribution and time** of a possible boundary shock, but not which of the declared shock scenarios will be realized. The scenario is observed fully at shock time, after which the controller may adapt.

This isolates the value of *information about the future* from the effect of adding capability-generating actions. Nothing about G4 establishes the statistical utility of GBR.

## Declared assumptions

The underlying G2/G3 system has finite durable capability sets, consumable integer resource inventories, one-tick atomic sequential actions, one known shock boundary at time tau (0 ≤ tau ≤ H), and a finite set of scenarios with **positive rational probabilities** summing to one exactly. Each scenario specifies a one-time deletion of capabilities, stock destruction and post-shock action disabling. Optional generative actions are available before or after the shock if the model and resource constraints allow them.

No randomness occurs before the shock. Hence an admissible deterministic controller has one common action prefix up to tau, although its *post-shock continuation* may branch on the observed scenario. A full adaptive policy for a random pre-shock observation process is **not** modeled.

The controller knows the scenario set and its probabilities and knows when observation will occur, but **not the realized future scenario**. The shock itself cannot interrupt a one-tick action. The goal objective here is the event that **all predefined goal capabilities coexist in one reachable post-shock state by the deadline**. It is not a real-time reward, multi-agent utility or a strict-restoration endpoint.

## Information sets and exact objective

Write x for the complete resource/durable state achieved at tau by one feasible deterministic pre-shock prefix p. After scenario omega is observed, let

\[
V_\omega(x)=\mathbf 1\{\exists\text{ a feasible scenario-adapted continuation reaching all goals by }H\}.
\]

The **non-clairvoyant** maximum expected binary success is

\[
V_{\mathrm{NC}}=\max_{p\in\mathcal P_{\mathrm{prefix}}}
\sum_{\omega\in\Omega} P(\omega)\,V_\omega(x(p)).
\]

Every scenario must share the same chosen pre-shock prefix. Continuing actions can vary *after* the scenario is observed.

For comparison, an optimizer with advance access to the scenario may choose a *different pre-shock prefix for each omega*:

\[
V_{\mathrm{PI}}=\sum_{\omega\in\Omega}P(\omega)
\max_{p\in\mathcal P_{\mathrm{prefix}}}V_\omega(x(p)).
\]

By the elementary inequality max(sum) ≤ sum(max),

\[
0\le V_{\mathrm{NC}}\le V_{\mathrm{PI}}\le1.
\]

The gap is the **perfect-information advantage in this small decision model**, not evidence of a new universal law. If construction is optional and the baseline action set is nested, the non-clairvoyant construction-enabled optimum cannot be worse than the construction-disabled optimum under the same distribution and information.

This objective maximizes *expected feasibility* with scenario-adapted recourse, not expected payoff or expected performance of an actual pre-trained learned policy.

## Independent solver comparison

**Solver A — state-set dynamic programming:** enumerate distinct states reachable under one common prefix from t=0 to tau, keeping a representative prefix for each identical complete state; calculate scenario-specific post-shock full state reachability from each state, then maximize the probability-weighted success.

**Solver B — exhaustive action-history oracle:** recursively enumerate every legal pre-shock sequence including waiting, then separately explore post-shock sequences for every declared scenario using a dictionary inventory representation, without using Solver A's state transition routine or caching. Select the best common prefix from complete histories.

**Established upper bound:** the existing G3 full augmented-state solver is run separately for each scenario, allowing its pre-shock decisions to depend on the scenario. This is the comparison V_PI. It is not a competing learned predictor.

Both NC solvers share the underlying action and shock specification, so agreement is a software/model consistency check, not a formal proof of program correctness.

## Illustrative negative control

The diagnostic includes a single kit that can be used **before** t=1 to prepare either channel A or channel B, but not both. At t=1 the kit stock is destroyed. In one equally probable scenario only the A-service action is allowed after the shock; in the other only the B-service action is allowed. The service can be delivered by t=2 if the matching channel was built.

A policy that **knows the future** chooses the correct channel in each scenario and attains score **1**. A non-clairvoyant controller must select one channel in advance and attains score **1/2**. Without optional construction the score is **0**.

The numbers are exact arithmetic of one deliberately constructed toy environment; they are **not** empirical frequencies or statistical estimates.

## Diagnostics and evidence status

G4 checks a deterministic seed (20261026) and 40 generated tiny models plus 40 variants with more severe stock-destruction shocks. Each is compared in construction-enabled and construction-disabled conditions: **160 solver-pair comparisons** expected, zero disagreements. Additional unit tests check different scenario priors, immediate observation, reduced deadline, channel failures, strict inventory sharing, non-generative baseline, scenario permutation and invalid probability/fault contracts.

Reproduce from repository root:

    python -m experiments.p1_gate4
    python -m unittest discover -s tests -v

[Code](../experiments/p1_gate4.py) · [Unit tests](../tests/test_p1_gate4.py) · [Expected deterministic manifest](../experiments/g4_expected.json).

No held-out system-family sampling, power calculation, confidence interval, GBR feature comparison, or external-domain replication has been conducted. G4 is **not** the registered confirmatory P1 experiment.

## Limits and next decision gate

G4 still assumes a known *shock time*, full revelation of the scenario upon shock, deterministic transitions conditioned on it, a finite enumerated scenario set, no pre-shock uncertainty, and centralized observation/action. A real system can lack this information and can fail continuously or have delayed/noisy observations. Moreover, the binary objective is **joint post-shock availability**, not strict restoration; G3 already showed those are distinct.

A subsequent research gate should implement a truly non-clairvoyant **policy-state model with imperfect observations** and resource-sensitive causal-support measures, then freeze an out-of-generator-family P1 comparison against augmented-state and conventional resilience baselines.

**Decision:** G4 closes an information-consistency software gate only. The scientific H1 hypothesis remains untested.
