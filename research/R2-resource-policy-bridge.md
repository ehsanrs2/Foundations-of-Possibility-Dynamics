# R2 — Why physically independent backup routes need not imply an executable robust policy

**Status:** deterministic counterexample and exact tiny-model calculation, NOT H1 validation or a proposed new metric. Builds on [R1](../appendices/C-fault-event-ontology.md), [G1](G1-verification.md), and [G4](G4-verification.md).

## Scientific question and scope

After R1, a pair of individually feasible plans can be *physically independent relative to a declared fault-event ontology*. Does that guarantee an actual **non-anticipating** policy can preserve a service goal across possible failures with limited *shared consumable resources* and a short preparation window?

**No, not in general.** Even in a small known scenario model, the same physical fault-event-disjoint pair of individual plans can exist in two systems with different implementable ex-ante success probabilities.

This is not a newly discovered law: standard constrained stochastic planning already represents the distinction. It is a **construct-validity negative control** for interpreting raw GBR or even R1's guarded pair indicator as actual resilience.

## Shared assumptions and compatible mapping

Two physically independent communication channels A and B can support the same service goal. Constructing either channel consumes one kit and one discrete action tick. Invoking a prepared channel to provide service takes one more tick. The preparation base is assumed protected in the toy; channel A service can be disabled by basic event e_A, and channel B service by e_B. These two basic events are *declared independent* with probability 1/2 each. A shared event would make the pair structurally dependent.

R1's structural calculation uses complete individual causal-support paths in G1, each requiring **one kit and two sequential steps**. They are each feasible *in isolation*, but plan enumeration **does not** impose simultaneous investment requirements on both alternative paths.

G4's reference policy calculation uses **the same named channel operations and event effects** as executable one-tick actions with a **shared kit inventory**. Four outcomes (neither failed; only A; only B; both) have probability 1/4 each. The controller knows the fault boundary but cannot know the future event realization during preparation. At the fault boundary, unspent kits and any earlier service output are removed, requiring service to be provided **after** the event from surviving prepared channels. The controller fully observes the realized scenario and can use any enabled prepared channel for the final tick. This is deliberately narrower than realistic unknown shock timing and noisy observations.

The physically declared event incidence is the same in all compared conditions. The difference between conditions is **the kit count and the number of pre-fault action ticks**, not an after-the-fact change of F.

## Exact counterexample

| Condition | Guarded R1 pair | Static path-event survival if both paths available | Optimal non-clairvoyant success | Clairvoyant upper bound |
|---|---:|---:|---:|---:|
| 1 kit; 2 preparation ticks | 1 | 3/4 | **1/2** | 3/4 |
| 2 kits; 2 preparation ticks | 1 | 3/4 | **3/4** | 3/4 |
| 2 kits; only 1 preparation tick | 1 | 3/4 | **1/2** | 3/4 |
| 0 kits; 2 preparation ticks | 0 | not applicable (no feasible path) | **0** | 0 |

**Interpretation:** with one kit, the controller must choose a channel in advance; its success is 1/2. Knowing which channel will survive would allow choice of an appropriate one in three of four event realizations, giving the *unimplementable* clairvoyant bound 3/4. Two kits **and** two preparation ticks permit preparing both channels before the unknown fault, matching the static 3/4 survival probability. Two kits with only one preparation tick do not. So even a physically correct structural pair score is not sufficient for feasibility of *pre-fault joint preparation*.

The static survival 3/4 is not a prognosis for a policy which cannot instantiate both paths. The exact G4 policy calculation is a **strong existing planning baseline**, not a scientific contribution exclusive to Possibility Dynamics.

## Cross-checks and reproducibility

[Executable R2 diagnostic](../experiments/resource_policy_r2.py), [twelve deterministic checks](../tests/test_resource_policy_r2.py), and [expected JSON record](../experiments/r2_expected.json) compare policy-state DP with an independent history enumerator from G4. They also test negative cases, including disabled construction, empty preparation time, source-event common causes, scenario reordering and resource scarcity.

Reproduce from root:

    python -m experiments.resource_policy_r2
    python -m unittest discover -s tests -v

**No independent population of networks or real assets was sampled.** The probabilities are stipulated exact fractions of a *hand-designed* finite model. The results are not confidence intervals, observed data or evidence of H1.

## Review implications: Issues #9, #10, #11, #12 and #3

1. R1's externally scoped fault ontology is **necessary but not sufficient** for making a prediction about resilient behavior. Structural supports, executable investments and risk exposure are different objects.
2. A valid eventual feature must declare whether it measures *alternative individually feasible plans*, *simultaneously prepared alternatives*, or *an optimized non-clairvoyant contingency policy*. These are not interchangeable definitions.
3. An indicator may be an interpretable descriptive feature, but its predictive value is not established by agreement with an **oracle that has all simulator rules and the realized failure distribution**.
4. The proposed P1 conditional strict-restoration endpoint is a different variable from R2's post-fault joint service availability. No direct result about the future strict-restoration endpoint follows from this R2 calculation.
5. Before any confirmatory H1 experiment, freeze fault identity/scope, shared resource semantics, scenario observation assumptions, policy/evaluation endpoint, compute budget and matched-information static/planning baselines.

**Decision:** do **not** quietly rename R1 or GBR to an inventory-aware metric on the strength of this negative control. Issues #9/#10/#11/#12/#3 remain OPEN.
