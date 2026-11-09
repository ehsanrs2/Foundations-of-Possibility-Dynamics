# R16-C / B2 — Bounded observable-trace equivalence gate

**Status (2026-11-09): PROVISIONAL_DEVELOPER_CONFORMANCE, not a universal theory result, not H1 preregistration.** This gate is an explicit successor to [B1](R16B-core-semantics-contract.md) and the [R16-A scientific roadmap](R16A-scientific-architecture-and-roadmap.md). It does not alter G2/G3/G4/R3/R7/R10, nor replace the draft primary H1 feature. Every example is **synthetic**; no source files or sealed test families are accessed.

## 1. Why GOG equality is too weak

In the existing G2 finite model, a system contains a set of held capabilities, nonnegative integer resource stock, AND-prerequisite actions, one-tick operations, a horizon and a declared goal vocabulary. B1 defines GOG as the number of new *individually reachable* goals under optional construction. Two models can have the **same GOG** while one completes a goal one tick earlier, uses more kits, or has a different visible ability to act. Thus a scalar endpoint is an inadequate test for operational representation equivalence. Historical R1/GBR additionally needs independently grounded **physical failure mechanism identity**; this B2 comparison cannot provide it.

## 2. Exact, bounded **observable trace-language** contract

Adopt a limited, explicitly chosen observation projection `O` from actual capabilities into **canonical visible capability indicators**, plus the exact ordered resource-stock vector. The declared target goals MUST all be visible. A goal/observation rename is accepted only with a specified injective mapping on source vocabulary; no identity mapping is inferred from similar labels. Source capability names absent in a model's produced/initial actions can be explicitly observable as always false.

For one fixed horizon `H`, initial stock, canonical goal vocabulary, same resource-axis names/order and action availability arm `k in {E0, E+}`, the trace language is

```
L_O,k(M,H) = {
  (O(s_0), O(s_1), ..., O(s_H)) :
  some legal H-tick history in M under arm k
}
O(s_t) = (canonical visible capabilities held at t, ordered stock vector at t)
```

A legal tick consists of precisely one applicable G2 action, or `WAIT`; each G2 action produces one durable capability after verifying AND-prerequisites and available consume-vector and updating stock via `stock - consumes + yields`. The B2 profile **requires a zero-effect fault vector at tick 0**. There are no real shocks, repair episodes, goal-loss histories, partially observed fault signals, stochastic fault priors or variable action durations here.

For the **two fixed E0/E+ arms**, B2 declares `M1 ≡_{O,H} M2` exactly when both complete projected trace languages are equal, after the evaluator has checked a common canonical observation/goal vocabulary, horizon and resource axes. It evaluates each arm separately; optional construction is never assumed to mean a fixed controller.

This is **finite existential trace-language equivalence under a declared observer**, not state or policy bisimulation. It does not preserve actions as controllable labels, nor causal fault-event identities, nor all hidden capabilities, nor unbounded future behavior. **It is wrong to replace a fixed-policy recovery probability or real backup identity with B2 equivalence.** Full nonanticipative policy equivalence requires a much stronger matching of choice/observation branching over controller histories and physical mechanisms.

B2 permits at most 4 ticks, 6 actions, 3 declared goals, and 20,000 distinct partial traces per layer; it inherits the bounded B1 validation of stock and resource axes. These bounds are **implementation ceilings**, not physical laws. Exceeding them is a failed admission, not a negative equivalence result.

## 3. Executed developer-controlled contrasts

| Contrast | GOG relation | Trace-language verdict (E0, E+) | Meaning |
|---|---|---|---|
| Add identical producer under another name and inert self-loop | unchanged | equal, equal | action alias alone did not change these observable traces; NOT physical route independence |
| Bijection `seed→root, bridge→relay, service→objective` with declared canonical goal identity | unchanged | equal, equal | valid semantic renaming at this observer projection |
| One-tick direct construction vs two-tick bridge construction | 1 vs 1 | equal, **different** | equal GOG can conceal real latency |
| Change one generative action's kit consumption from 1 to 0 | 1 vs 1 | equal, **different** | equal GOG can conceal physical resource demand |
| Bridge needed for goal vs a dead-end intermediate | 0 vs 0 at H=1 | equal, equal | horizon-1 equivalence is limited |
| Same pair evaluated at H=2 | 1 vs 0 | equal, **different** | bounded equivalence need not survive a longer horizon |
| Extra non-generative `secret` action, secret not visible | unchanged | equal, equal | projection hides an operational difference |
| Same extra action, with `secret` explicitly visible | unchanged | **different**, **different** | more informative observer distinguishes systems |

*The H=1 and H=2 row comparisons are independent queries at the same horizon **within each row**. B2 refuses a direct cross-horizon comparison.* These results are planned fixed fixtures, not samples of actual field systems.

## 4. GOG, behavioral invariance and the novelty boundary

Equal trace languages under E0 and E+ with the same canonical goal vocabulary imply equal reachable-goal sets and hence equal GOG for that bounded query. This implication is **immediate from definitions**, not a novel physical result. Its converse is false as the latency and inventory examples show. A claimed compact invariant must also survive meaningful **semantics-preserving** encodings, with computational budgets and a valid independent baseline.

Comparison with **ordinary state-space reachability** is deliberately built in: B2 calls the existing B1 evaluator, which in turn checks G2 state-layer search, G2 independent chronological enumeration and G3 augmented-state reachability. The B2 trace enumerator records every history projection rather than collapsing states. It demonstrates an operational modeling discipline, **not that Possibility Dynamics expresses more than standard state transitions**.

There are two specifically unresolved risks:
1. **Observability:** goals and resource stock are visible here, but disabled actions, policy commands, action IDs, environmental state, partial/noisy observations, hidden faults and intervention effects are not. Equality of projected traces is not a proof that two controllers can make identical choices.
2. **Computational scaling and representation:** this exact enumeration is exponential in general and only tests tiny toy systems. A coarse-to-fine refinement requiring two unit-tick actions **changes real time** unless an explicit duration-preserving translation is established. B2 must not label such a change 'equivalent' because final reachability remains unchanged.

## 5. Scientific protection and follow-on

- **R8** zero incremental predictive Brier gain for the historical R1 feature remains unchanged.
- **R11/R12** synthetic DP-computable developer effects remain development-only; B2 does not invent a novel metric or replace the original preregistration candidate.
- **P1/H1** is still `DRAFT_NOT_PREREGISTERED`. Zero confirmatory samples and zero sealed test-family calls.
- **R16 LANL** publisher-original/Usage/Event lineage gates are independent. A node administrative fix is not a recovered job goal.
- **R16-A Gate A** was merged as a proposal, not independently signed off as a scientific freeze.

Reproduce with:

```bash
python -m unittest tests.test_p1_r16c_bounded_trace_equivalence -v
python -m experiments.p1_r16c_bounded_trace_equivalence
python -m unittest discover -s tests -v
```

**B2 exit:** CI must pass the bounded contract/negative-control test suite, and reviewers must accept *only the scoped, observational trace equivalence definition*. The next proposed **B3** work is explicit action-observation branching and fixed-policy equivalence (plus an observationally sound cost/duration-preserving refinement); it must keep a conventional transition-system baseline and inspect worst-case work/timeout. This is necessary before any claims about general representation invariance, policy equivalence or a unified `core/` package. Issues [#8](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/8), [#9](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/9), [#10](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/10), [#11](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/11) and [#12](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/12) remain OPEN.
