# Chapter 5 — A minimal constructed example

**Status: didactic demonstration, not confirmatory evidence.**

## 5.1 Scenario and assumptions

A system initially has six capabilities: power, sensor, wire transmitter, LED, timer and assembly device. The alarm goal is reachable through an existing wire transmitter. A second plan constructs an optical transmitter from LED, timer and assembly device, using a kit and an extra step. Both routes use power and sensor.

The illustrative shock model declares only four exposed components: wire transmitter, LED, timer and assembly device. Power and sensor are assumed protected for **that specific shock experiment**, rather than inherently invulnerable.

## 5.2 Deterministic outcomes

| Computed quantity | Initially | After loss of wire transmitter |
|---|---:|---:|
| Goal reachable without construction | Yes | No |
| Goal reachable with construction | Yes | Yes |
| GOG | 0 | 1 |
| GBR gain | 1 | 0 |

The first row pair proves only that a previously reachable goal can gain a second route without increasing the number of reachable goals. The numeric GBR result depends on the vulnerability definition and the archived two-plan code; it is **not** independent evidence of general resilience.

## 5.3 Counterexamples

Removal of *power* or *sensor* disables **both** paths. If the kit budget is zero or the available horizon is one step, the optical plan is infeasible. Correlated failures can also defeat formally disjoint paths. These boundary conditions matter as much as the successful wire-failure example.

## 5.4 Reproduction

The exact v0.1 scenario is retained as [Python source](../experiments/toy_case.py) and [archived JSON](../experiments/toy_case_results_v0_1.json), with [seven regression checks](../tests/test_toy_case.py). Run:

    python -m unittest discover -s tests -v
    python -m experiments.toy_case

Tests establish deterministic software behavior, **not** that GBR is novel, causally relevant, or superior to existing network-science measures.

## 5.5 G1 reconstruction as an explicit rule graph

The scenario now has three named rules: an ordinary wire-alarm use rule; a **generative** optical-transmitter construction rule requiring LED, timer and assembly; and an ordinary optical-alarm use rule. Time and kit costs are included for each legal sequence. The rule graph and its plan ancestry are executable in [G1](../experiments/p1_gate1.py). With the initial exposure set, GOG remains zero while GBR gain equals one. After a wire-source fault, the optical sequence can still reach the goal if prerequisites survive; after deleting a shared sensor or power input, neither route reaches the goal. This example remains constructed, not representative data.
