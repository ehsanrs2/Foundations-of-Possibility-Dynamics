# Chapter 4 — Candidate measures and consistency

**Status: provisional definitions; not established discoveries.**

## 4.1 Why new-goal counts miss resilience

Let R0(s;H,B) denote the end goals reachable in a finite model when capability construction is disabled; R+(s;H,B) the same goals when optional construction is allowed, with all other constraints fixed. Define **generative option gain** as

\[
\mathrm{GOG}(s)=|\mathcal R^+(s;H,B)\setminus\mathcal R^0(s;H,B)|.
\]

This detects *newly reachable goals*, not new ways to reach an existing goal. Where construction is optional, R0 is a subset of R+, but neither set specifies probability or desirability.

## 4.2 Generative backup redundancy *gain* (GBR)

For baseline-reachable goal g, let P0(g,s) be individually feasible plans without construction and P+(g,s) a superset also allowing construction. Plan feasibility requires a specified budget, duration and resource semantics. Let F be the finite set of failure-exposed components in a **specified intervention model**, and let D_F(p) be every element of F required by plan p, including construction prerequisites.

For j in {0,+}, let

\[
b_g^j(s)=\mathbf{1}\{\exists p\ne q\in\mathcal P_g^j(s):
D_F(p)\cap D_F(q)=\varnothing\}.
\]

Our **candidate** measure is

\[
\mathrm{GBR}_{gain}(s)=
\sum_{g\in\mathcal R^0(s;H,B)}
\left(b_g^+(s)-b_g^0(s)\right).
\]

This corrects the v0.1 mismatch: original prose described existence of a constructed backup but toy code computed the **increment** of a binary backup indicator. Provided P0 is contained in P+, GBR gain cannot be negative. The metric saturates after one independent backup *pair* per goal; it does not count every possible independent route or provide a probability of recovery.

## 4.3 Three critical limitations

First, independence is **relative to F**, not absolute. Two routes can share power and sensor components absent from F and both fail if those shared components break. Second, a plan feasible before a shock can become infeasible after it; post-shock recovery must be recomputed with surviving resources, time and capabilities. Third, two individually feasible plans may compete for resources and be impossible to execute simultaneously.

## 4.4 A potential trivialization

Any finite construction rule can be represented as another transition in an augmented ordinary state space. In a complete model, standard reachability can already represent constructed alternatives. **No claim that the metric transcends control or network theory follows.** The testable possibility is more modest: a compact pre-shock structural feature may improve *held-out prediction* given a stated information and computation budget.

## 4.5 Hypotheses

**H0:** GBR gain yields no reproducible incremental predictive value over strong baselines.

**H1:** GBR gain improves held-out prediction on prespecified system families.

**H2 (exploratory):** benefits vanish under common-cause failures, high construction costs or short horizons.

A predictive improvement would not establish causation or a fundamentally new law. These hypotheses have **not** been empirically tested.

## 4.6 G1 operational implementation and exposure sensitivity (not H1 evidence)

[Gate G1](../research/G1-verification.md) introduces a causal-support representation: every feasible goal plan carries provenance from initial inputs and rule instances. Backup-path independence is checked **only after intersecting those full supports with the declared failure-exposure set F**. This makes the scope of the claim explicit. In the illustrative alarm system, an optical and a wired pathway have disjoint exposed dependencies when power and sensor are protected; extending F to include the shared power supply changes the backup indicator from one to zero. A conditional binary feature does not supply a recovery probability or claim of immunity to common-cause faults.

Two differently organized finite enumerators agreed on 192 plan-set comparisons; they share representation conventions and are not wholly independent implementations. G1 contains no fitted predictive model, held-out benchmark or inferential result. Formal hypotheses H0/H1 remain open.

## 4.7 G3: structural option scores versus executable joint outcomes

[Gate G3](../research/G3-verification.md) gives an inventory-constrained counterexample where different goals can be achieved separately but cannot be held together along any one feasible history. Thus binary disjoint-path indicators and separately computed option sets are not enough to infer execution feasibility under competing resource use. This finding concerns **model semantics**, not measured predictive performance of GBR. Any future GBR implementation with consumable resources must state whether it represents mutually exclusive alternatives or simultaneously executable backup plans.


## 4.8 Reviewer-critical counterexamples to raw GBR gain

[The executable metric audit](../research/gbr-metric-audit-v0.3.md) shows that raw GBR can be **1** for two labeled rules that denote **one declared physical implementation**, where an identity-aware projection gives **0**. Similarly, adding shared power to the exposed set can flip the alarm example from **1** to **0**, and an alternative route requiring the entire time horizon can still receive the same binary backup indicator as a route with ample slack. These are constructed negative controls, not empirical distributional estimates.

All uses of GBR must therefore state the external fault ontology, physical component identity, scope of exposure F, plan-equivalence convention, cost/deadline rules and uncertainty about unmodeled common causes. Never treat physical identity as automatically recoverable from software labels. This v0.3 audit **does not silently redefine** the historical G1 index or establish a universally correct replacement.

## 4.9 A conditional information limitation

If the entire observable pre-failure model is X and exact GBR is Z=f(X), then an unrestricted Bayes-optimal predictor given X cannot improve merely by also receiving Z: the best attainable predictions from (X,Z) are exactly those from X. The proof and scope are in [Issue #8 audit](../research/novelty-audit-v0.3.md). A finite-data or resource-limited learner may still benefit from engineered Z, but this is an **unverified empirical/computational claim**, not novel information or an independent physical law.
