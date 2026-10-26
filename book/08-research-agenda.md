# Chapter 8 — A staged program of scientific tests

**Status: research roadmap; stages below are not claims of completion.**

## Stage A — Formal verification

Freeze the rule grammar, resource semantics, timing and fault model. Prove monotonicity properties when optional construction is added, state precisely when they fail, and search for counterexamples to representation invariance. Compare the definitions to dynamic hypergraph reachability, AND/OR networks, repair and viability theory.

## Stage B — Software correctness

Create a small-state exhaustive search oracle independent of the production solver. Check enumeration against hand-specified cases and metamorphic tests: renaming capabilities, removing budgets, enforcing shared prerequisites and adding irrelevant options.

## Stage C — Benchmarking

Preregister the E0/E1/E2 simulation grid, sample size or precision calculation, baseline metrics, generator families and evaluation score. Run family-held-out comparisons and publish raw outcomes, code commits and null findings. Compare feature computation costs.

## Stage D — External validity

After synthetic results, select a real bounded system where goals, failure events, resources and repair rules are directly measurable—for instance modular computing equipment or a reproducible laboratory setup. Audit measurement error and feasibility of causal interventions.

## Stage E — Theoretical synthesis

Only then evaluate whether predictive patterns explain mechanisms that existing frameworks leave insufficiently captured. A successful specialized model may be a valuable publication even without founding a new discipline.

This stage-gated structure prevents the scientific book from becoming a narrative in which attractive conjectures are progressively mistaken for proven laws.

## Gate G0: software verification (completed)

An independent exhaustive search oracle and a dynamic-programming solver agreed on 256 small-reachability comparisons from a seeded generator. The [G0 audit](../research/G0-verification.md) reports this software result and its restrictions. The GBR predictor and formal P1 trial **remain untested**. [LEAN](../integrations/lean/README.md) is proposed only for a later financial-domain transfer study, and no LEAN engine run is claimed.
