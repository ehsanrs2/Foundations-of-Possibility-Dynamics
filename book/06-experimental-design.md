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

## 6.6 G2 implementation: a strictly bounded execution kernel

The [G2 software kernel](../experiments/p1_gate2.py) extends the earlier monotone rules with per-action consumable stock, replenishment, waiting, and a single irreversible fault at a discrete time boundary. It reports *the earliest time each target is available after the disturbance*. This intentionally covers both retention and restoration, and cannot be called a strict restoration-time estimate. Separate goals are existentially tested and need not be jointly satisfiable. The model's one-tick atomic operations are a simplification, not a realistic treatment of failures during long-running actions. The [G2 audit](../research/G2-verification.md) defines these restrictions; no prospective P1 ensemble experiment is reported.

## 6.7 Strict restoration and perfect foresight

The [G3 solver](../research/G3-verification.md) separates retention from restoration using loss-at-fault history flags. Its strict restoration query requires the goal to be held just before the fault, removed by the fault, and reacquired later on the **same trajectory**. It also computes whether all goals can coexist on one inventory-feasible trajectory. These are best-case reachable outcomes under an **already known future fault**. They cannot represent policy performance under unknown future disturbances without a new information model and policy evaluation protocol.

## 6.8 G4: separate foresight from resilience

The [G4 model](../research/G4-verification.md) considers a finite scenario distribution whose realization cannot affect pre-shock actions; the controller observes the scenario only at the known shock time and may then take different feasible continuation actions. This avoids the specific G3 pitfall of optimizing the pre-shock history *with* knowledge of the realized future fault. For the same model, a scenario-by-scenario clairvoyant solver provides an **upper bound**, not a deployable prediction benchmark. The G4 endpoint is binary joint goal attainment after the fault, not the strict-restoration endpoint of G3. The underlying observation and fault-time assumptions remain restrictive; no P1 confirmatory experiment has yet been executed.
