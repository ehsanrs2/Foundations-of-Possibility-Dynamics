# Chapter 6 — Experimental systems and controlled comparisons

**Status: prospective methodology; no P1 ensemble results exist.**

## 6.1 System units and dependency grammar

Represent every system by a directed dependency hypergraph: a construction rule may need several components jointly and yield a new capability. Specify the initial inventory, prerequisite set, rule latency, consumed resources, target predicates, horizon, and an externally imposed failure process. Ordinary graph edges do not suffice for AND-type prerequisites without extra intermediate nodes.

## 6.2 Three paired conditions

In **E0** construction is forbidden. In **E1** construction is enabled with exactly the same initial resources, target family and disturbances. In **E2** separately ablate cost, time, common-cause exposure or resource reserves. A comparison is interpretable only when its changes are enumerated: merely adding options changes the action set and may trivially improve reachability.

## 6.3 Endpoints and fair information

The primary endpoint is the proportion of predefined goals recovered under a held-out shock, subject to a fixed post-shock budget and deadline. Pre-shock features must not depend on the realized test shock. Provide all prediction models access to equivalent observable rule and resource information. Compare with strong alternatives: graph and hypergraph cuts, route redundancy, feasible goal count, viability-style measures, and where practical information-theoretic empowerment.

## 6.4 Generalization and analysis

Split by **entire system instance and generator family** before training or choosing metrics. Avoid splitting repeated shocks of the same network between training and test sets. Report recovery prediction error, effect sizes, instance-clustered uncertainty, computational cost and explicit out-of-distribution degradation. No confirmatory sample size or power calculation has yet been frozen.

## 6.5 Interpretation

An improvement limited to a simulator family supports an engineering predictor in that family, not a universal law. Null results would be scientifically valuable. See [Protocol P1](../research/protocol.md) for the preregistration checklist.
