# Chapter 4 — Candidate measures

**Status: working proposals; names and formulas are provisional.**

## 4.1 Why counting newly reachable goals is insufficient

For a target family \(\mathcal G\), define the *candidate* generative option gain

\[
\mathrm{GOG}(s)=|\mathcal R^{\mathrm{construct}}_{H,B}(s)\setminus
\mathcal R^{\mathrm{no\;construct}}_{H,B}(s)|.
\]

This nonnegative count only captures newly attainable goals under a specified comparison. It **misses** a constructible redundant route to a goal already reachable without construction. A zero score need not imply weak recoverability.

Names used in previous exploratory notes (e.g., “GOP”) are not standardized; this book uses GOG unless a later decision log revises terminology.

## 4.2 Generative backup redundancy (GBR)

Let \(\mathcal P_g^0(s)\) denote baseline feasible plans for target \(g\) without constructing new capability types, and \(\mathcal P_g^+(s)\) feasible plans allowed to construct them. Choose an **explicit failure-sensitive component set** \(F\), and define \(D(p)\subseteq F\) as the vulnerable components required by plan \(p\).

For goals reachable at baseline, define the candidate indicator:

\[
b_g(s)=\mathbf 1\{\exists p\in\mathcal P_g^0(s),\,
q\in\mathcal P_g^+(s)\setminus\mathcal P_g^0(s):
D(p)\cap D(q)=\varnothing\}.
\]

Then

\[
\mathrm{GBR}(s)=\sum_{g\in\mathcal R^0_{H,B}(s)} b_g(s).
\]

**Important:** This indicator by itself only says there is *some* independent constructible alternative, and depends on the specified vulnerability set and entire plan semantics. It is not a universally established robustness metric. If \(F\) is empty, if all dependencies are counted incorrectly, or if construction requires the failed component, the interpretation fails. In particular, a plan-dependent rule should not be mistaken for one that remains feasible *after* a failure without recomputing the feasible plans in the post-intervention state.

## 4.3 Three distinct evaluation targets

- **Pre-disturbance feature:** GBR estimated only with data available before intervention.
- **Post-disturbance outcome:** goal recovery, restoration latency and incurred cost after a held-out failure.
- **Incremental predictive value:** improvement beyond matched baselines on held-out network families and interventions.

A correlation between a feature and an outcome is not evidence that increasing that feature causes resilience. Use randomized manipulations or well-supported causal assumptions for such a claim.

## 4.4 Strong baseline families

Compare against graph size and degree distributions; paths/edge- or vertex-connectivity; minimal cuts; resource slack; standard reachability and viability measures; and where tractable, empowerment or state-action-channel approximations. Use matched computational budgets where applicable.

## 4.5 Provisional predictions

H1: Under matched initial conditions, capability-generating dependency structure explains **held-out** recovery outcomes beyond simpler topology-only baselines.

H0: It contributes no reproducible incremental predictive value.

H2 (exploratory): The effect changes sign or disappears under high generation costs, tight deadlines, or correlated prerequisite failures.

No prediction has been empirically validated in this edition.
