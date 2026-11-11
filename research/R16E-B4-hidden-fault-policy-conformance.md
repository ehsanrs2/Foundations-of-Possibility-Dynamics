# R16-E / B4 — Hidden stochastic fault and observation-based policy conformance

**Date:** 2026-11-10. **Status:** PROVISIONAL_SYNTHETIC_CONFORMANCE, NOT preregistered H1, NOT an independent physical-systems benchmark, NOT proof of new theory. Based on merged [B3](R16D-B3-command-response-policy-equivalence.md), [B2](R16C-B2-bounded-trace-equivalence.md) and [B1](R16B-core-semantics-contract.md).

## Research question

Can two systems with identical **no-fault** command-response behavior have different operational outcomes when the controller does not know which fault will happen or when? Can a fixed information restriction be enforced rather than scoring the optimal action chosen with knowledge of the realized scenario?

B3 compared all deterministic no-fault commands. B4 introduces a **known prior** over hidden exogenous faults, potentially occurring at different future ticks, and retains a policy that sees only a declared capability projection, stock and success/failure of its own commands. Scenario name, underlying disabled action, fault onset notification and future fault realization are **not** observed.

## Narrow, versioned B4 profile

- Use the G2/B3 finite one-tick AND-prerequisite actions, integer consumable stock and persistent capabilities. Each model's **base** G2 fault is inert at tick 0. The B4 world adds exactly one **separately declared synthetic** event scenario per rollout; there is no double application of the base fault.
- Horizon H is 2 or 3, at most 4 actions and 3 positive-probability scenarios; actual fault ticks are in {1,...,H-1}. The declared rational probabilities are positive and sum to **exactly one**. No reliability frequency was estimated from real data.
- At tick t, apply the hidden scenario fault first (removing capabilities, destroying stock, disabling action IDs). Then reveal the **pre-command** canonical visible capabilities and ordered stock; the controller picks a canonical command or WAIT; reveal command acceptance and **post-command** visible state. An ineffective event causes **no artificial announcement**. There is no noisy sensor, delayed perception or explicit fault-ID signal. Command rejection is a TESTER observation and costs a tick, not an implied production R3/R7 policy behavior.
- All compared worlds must have the **same** ordered resource axes and stock, goal vocabulary, canonical observable/command alphabets and declared exogenous scenario **names, probabilities, and onset times**. Their hypothetical physical effects may differ; without independently sourced physical identities, this is only a synthetic contrast.
- Endpoint for the policy solver is **one prespecified goal held at the final horizon**. This is deliberately **NOT** H1's strict lost-then-regained service endpoint, not a measure of resilience under independent observed policies, and not GOG/GBR.

## Two independent operational gates

### Gate B4-L — stochastic observable command-response law

For each fixed canonical action word w of length H, both ordinary (E0) and optional construction (E+) arms calculate the **exact law** over:

(initial public state, for each tick: (pre-command observation, action accepted, post-command observation)).

Each scenario contributes its prespecified rational mass; hidden names/times are never inserted as a public field. B4-L equality means these distributions are identical for **every** open-loop command word in each arm. A first counterexample command word is returned when they differ.

**Finite conditional-policy implication.** Under the declared exogenous scenario law, deterministic transitions, common canonical control alphabet and observation contract, equality of those joint public trace laws for every full command word implies equal public history distributions for each shared deterministic policy that picks its next action solely from prior and current public observations/replies. *Justification:* any feedback-policy history determines an action prefix; its probability is the probability of the corresponding public-cylinder event in the fixed-word experiment. Full-word law equality determines every prefix marginal, and induction over the policy tree gives the same probability for all visible leaves. This is a standard finite input/output-model consequence, not novel mathematical priority. It does **not** prove equivalence under different information sets, partially specified physical events, adversarial scenario adaptation to action, unbounded time, or arbitrary continuous observations.

### Gate B4-P — nonanticipative bounded policy outcome

Compare two developers' algorithms on the **same** terminal goal and observation restriction:

1. **Conventional belief-state dynamic programming:** propagate probability-weighted augmented states (scenario, held capabilities, stock, disabled actions); partition by **visible pre-action observation** and, after a candidate command, by **acceptance and visible post-state**. The decision in each partition is common to every hidden scenario in that partition. Maximize final goal-presence mass without inspecting realized case before action.
2. **Independent chronological policy-tree history replay:** for every branch, replay that scenario's earlier command sequence using a separate mutable inventory/set implementation, partition current scenarios by their public history, and enumerate legal tester commands. No DP state cache is shared. Compare exact Fraction-valued optimal probabilities. This is a software cross-check, not statistical replication.

An unconstrained clairvoyant scenario-specific action selector can have a higher value; that is a **diagnostic upper bound**, not a deployable fair baseline.

## Controlled developer findings / expected fixtures

| Synthetic fixture | Contractual outcome | What the fixture shows |
|---|---|---|
| Identical base commands, one of two repair actions disabled by a hidden equiprobable event at tick 1 | B3 no-fault response equal; B4-L unequal if the competing model protects both actions | No-fault equivalence need not extend to hidden physical exposure |
| Service initially present, then actually removed at tick 1; either channel a or b is secretly disabled, with no identifying observation | Belief DP = independent history oracle = **1/2** final service probability | Without advance knowledge, a one-repair-tick controller cannot choose the intact channel with certainty |
| Same case, but the disabled channel has a distinct **observable sensor-loss signature** | Belief DP = history oracle = **1** with the prespecified sensor observation | Additional legitimate information may change achievable policy value; it must not be quietly given to only one comparator |
| Unknown fault time, tau 1 or 2 with rational prior 1/2 each | Exact bounded policy DP and history oracle agree; fault time not announced | Feedback can react to actual current state, not hidden future timing |
| Hidden event removes only an absent capability vs a genuinely inert event, same prior and tick | Identical B4-L distributions | Invisible null-effect event must not create an informational alert |
| Renamed source action IDs, and declared matching canonical commands plus matching renamed disabled-action footprints | Identical B4-L distributions | Command renaming does not authorize guessing real physical mechanism identity |

These are hand-constructed demonstrations, **not independently sampled test families**. The 1/2 and 1 results are *model-exact arithmetic*, not estimates of deployment performance.

## Invalid comparisons and stop rules

Reject: invalid or floating-point priors; duplicated scenario names; unaccounted event times; wrong resource dimensions, altered physical-event priors, changed goal/query vocabularies, unmapped action names, invalid disable IDs, non-inert base model fault, nonexistent goal, unbounded oracle work. Each rejection is **unassessable**, not evidence of non-equivalence. The code does not derive fault identity from graph/action labels or fit hidden hazard priors from field data.

B4 preserves [R8's negative R1 feature result](R8-development-summary-seed20261101.json), [R11](R11-unknown-time-prediction-results-20261102.json) and [R12](R12-cross-grammar-results-20261102.json) as purely developmental, and [R15's zero admitted service episodes](R15-node-job-lineage-results-20261108.json). [R16](R16-lanl-publisher-usage-event-lineage-protocol.md) remains an *independent* data provenance/lineage track. **P1/H1 remains DRAFT_NOT_PREREGISTERED; zero confirmatory samples; no sealed test family use.** A goal held at the horizon can be retained and is not automatically a strict restoration label.

## Reproduction and next scientific gate

    python -m unittest tests.test_p1_r16e_b4_hidden_fault_policy -v
    python -m experiments.p1_r16e_b4_hidden_fault_policy
    python -m unittest discover -s tests -v

The B4 workflow checks the focused controls, performs the independent exact-Fraction audit and runs all historical tests; stores only synthetic JSON without production identifiers.

**B4 exit** is *bounded software/modeling conformance only*, dependent on green CI and critical review of the hidden-information timing and feedback comparison. Do **not** open the sealed H1 population or declare the new finite model a new scientific theory.

**Next B5 decision:** introduce actual loss/reacquisition **on one policy history** with non-loss and censoring distinguished; test a delayed/noisy observation contract and evidence-derived/defensible physical event ontology, and compare conventional standard belief-state/repair baselines with explicit all-in compute ceilings. Resolve Issues [#3](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/3), [#8](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/8), [#9](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/9), [#10](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/10), [#11](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/11), and [#12](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/12) on their independent scientific terms; none is closed by B4.
