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
