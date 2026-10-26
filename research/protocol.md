# Protocol P1 — Testing generative options against resilience baselines

**Status: prospective protocol; no P1 experimental data have been collected.**

## Core estimand

Incremental out-of-sample predictive performance of candidate generative indicators for goal recovery after an intervention, beyond baseline graph topology, redundancy, resources and viable/reachable goal measures.

## Unit and sampling

Unit: independently sampled *system instance* with a capability dependency hypergraph, deterministic production rules, resources, horizon and target predicates. Generate families with controlled node count, prerequisite arity, degree distribution, density, costs and source availability. Split by **instance and generator family** before feature selection or hyperparameter tuning.

## Planned intervention groups

E0: static action/capability set, construction disabled.

E1: construction allowed with prespecified costs and prerequisite rules, otherwise matched to E0.

E2: construction allowed but subjected to ablations (correlated failures, resource bottlenecks, deadline constraints, and construction disabled after shock).

Ablations must avoid changing several confounders at once; explain when perfect matching is impossible.

## Outcomes

Primary: proportion of predefined goals recovered within a fixed horizon and resource cap after failure, across a fixed intervention distribution.

Secondary: time to first recovery, total resource usage, cost-adjusted recovery and reachable-goal retention. Register tie-handling, censoring and impossible-to-recover cases.

## Primary comparison

A baseline model with topology, standard path redundancy, min cuts, initial goals and resource reserves versus baseline plus GBR/GOG. Compare on held-out network families and never use outcomes to design feature computation. State the algorithmic cost of calculating every metric.

## Uncertainty and decision

Report differences in a prespecified predictive score (e.g. MAE for continuous recovery fraction), bootstrap intervals **resampled by independent system**, effect sizes, failure families, and sensitivity to horizon and budget. Publish null findings. Do not interpret a positive held-out score as proof of fundamentally new laws.

## Pre-execution checklist

1. Freeze precise graph/hypergraph semantics and failure units.
2. Freeze train/validation/test generator families and random seeds.
3. Freeze outcome definitions, baseline implementations, and primary metric.
4. Demonstrate that GBR does not look ahead at held-out faults.
5. Validate tiny networks by exhaustive plan enumeration.
6. Record environment, runtime, raw data and checksum manifests.
7. Execute; then publish all results and deviations from protocol.

No power calculation or sample-size justification has been performed yet; these must precede confirmatory claims.

## G0 verification status (completed, nonconfirmatory)

[G0](G0-verification.md) compares exhaustive enumeration with an independent mask/time solver for small bounded systems, including initial-component shocks: 256 comparisons, zero mismatches. The model does not implement GBR and cannot be used to claim H1. Subsequent P1 steps remain unexecuted.

[QuantConnect LEAN](../integrations/lean/README.md) was screened for eventual financial transfer but not used for the core P1 experiment.

## Gate G1 — bounded plan-support verification (software gate completed)

[G1](G1-verification.md) explicitly tracks initial-source and rule support in a sequential monotone production model, including scoped exposures and pre-run loss of initial components or rules. Complete sets of goal plans agreed between action-sequence DFS and rule-subset enumeration in **192 comparisons** from 48 small cases plus a faulted counterpart each; 13 dedicated checks exercise assumptions and counterexamples. **No P1 predictive data, calibration, held-out generalization or H1 testing were performed.**

To advance: independent oracle for causal-support extraction, consumable resources, dynamic shock distributions and fair strong baselines; preregister a meaningful sample size before any confirmatory analysis.
