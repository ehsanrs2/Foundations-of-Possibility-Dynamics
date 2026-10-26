# Gate G0 — independent finite reachability audit

**Status: SOFTWARE VERIFICATION ONLY — not confirmatory P1. Date: 2026-10-26.**

## Modeling assumptions

Finite labeled capabilities, finite fixed initial holdings, AND-type production prerequisites, each rule uniquely producing one capability with strictly positive integer duration and nonnegative integer cost. Rules only ADD held capabilities, never consume prerequisites. All shocks delete a subset of *initial* holdings before the run. Resource budget and time horizon apply to each sequence. The system models no probabilistic disturbances, continuing shocks, shared resource contention among alternative plans, runtime repair policies, or complex goals.

This Gate G0 formalism is narrower than the theory in the main text. **GBR is not computed in G0.**

## Two independently implemented algorithms

1. An exhaustive recursive oracle enumerates all legal sequences and has no memoization.
2. An independent dynamic program uses capability bit masks and a time-indexed (state, minimum expenditure) table.

Both calculate existential reachability of target capability labels, not probability, policy quality or recovery.

## Diagnostic executed

With seed 20261026, 64 tiny independent systems are generated. Each has an original condition and one initial-capability-deletion condition. Two construction settings (enabled/disabled) yield **256** paired solver comparisons, with **zero differences**. Also checked: optional construction cannot reduce reachable goals; bijective relabeling preserves goal-count reachability; increasing budget or horizon cannot reduce goal reachability.

Reproduce from repository root:

    python -m experiments.p1_gate0
    python -m unittest discover -s tests -v

[Expected JSON output](../experiments/g0_results.json) is committed. Seven dedicated Python unit tests cover AND-prerequisites, time and cost limits, zero bounds, disabled generation, relabeling, invalid rule contracts and the seeded comparisons.

## Scientific interpretation

Agreement provides limited *software evidence*, not a proof of correctness for all finite systems. Random tiny systems do not constitute an externally valid sample. We have **not** tested GOG/GBR predictive performance, the H1 hypothesis, recovery probability or multi-domain applicability.

## Remaining blockers

Formalize GBR plan-dependency support and correlated failure exposure; independently verify the GBR implementation; establish proper resource-consumption semantics; freeze model-family splits, strong baselines and confirmatory sample size; then run the actual P1 study.
