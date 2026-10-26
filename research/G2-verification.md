# Gate G2 — finite resource consumption and in-run boundary faults

**Research integrity status:** bounded software-validation diagnostic; *not* a preregistered P1 experiment, not a predictive assessment of GBR, not a new physical law.

## Aim

G1 considered monotone capability creation and shocks before planning. G2 introduces a **nonrenewable or replenishable integer stock**, action-level consumption/replenishment and a disturbance occurring at a chosen **discrete time boundary while the system is operating**.

This allows a simple question: which specified goals can be *available after a disturbance*, taking construction times and finite inventories into account?

## Exact transition semantics (G2.0)

- State before each integer time boundary: durable capability labels plus a vector of nonnegative integer stock quantities. Time runs from t=0 to t=H.
- An action lasts **exactly one tick**, has a name, durable prerequisites, stock units consumed, stock units yielded, one durable capability output and an optional 'generative' marker.
- Inputs in the durable capability set are **not consumed**; the stock vector *is* consumed. Goals are durable capability predicates, not utilities or probabilistic outcomes.
- Waiting one tick is always a legal action. Repeating an action is allowed, including replenishment, provided prerequisites and stock remain feasible.
- A single deterministic fault event at t=tau **first** deletes named durable capabilities, removes up to a specified stock quantity from each inventory (clamped at zero), and disables named actions from tau onward. The event occurs **before** scoring goals or selecting a new action at tau.
- No action can be interrupted mid-tick: the fault occurs at a boundary. There are no further shocks; source capabilities can be reconstructed later using rules unless a corresponding action has been disabled.
- A goal counts as available **at/after the fault** if some legal plan has that goal held at a time t≥tau after the fault update. If the goal was already present before the shock and survives it, that is *retention*, not necessarily restoration. The earliest recorded tick is existential per goal; separate goals need not be achievable together.
- The non-generative (E0-like) system forbids only actions marked 'generative'; it still permits all ordinary operation and stock replenishment. The construction-enabled model contains all the baseline trajectories; it does not force generation.

The fixed example has one kit. A wired alarm route can emit an alarm before t=1 but at t=1 the fault removes the alarm capability and wire; fixed-only planning cannot restore it. An optical route, built with one kit, reaches the alarm goal at t=2. This is one specially designed *software fixture*.

## Two implementations

**DFS oracle:** explicit recursion over action histories, with mutable per-path resource dictionaries and direct fault application. It deliberately does not deduplicate states or use the DP transition engine.

**Time-layer solver:** keeps a set of distinct (durable-set, integer-stock-vector) states per tick, applies the same fault boundary rule, and expands with wait/action transitions.

They have distinct search and stock representations but still share the input schema and abstract domain semantics. Agreement is **not a formal correctness proof** or a truly independent experimental replication.

## Diagnostic and expected outputs

The fixed-seed diagnostic creates 64 small systems and for each a more severe-fault variant. Each of these 128 instances is checked with construction on and off:

| Software-verification item | Count |
|---|---:|
| Seed | 20261026 |
| Original models | 64 |
| More severe-fault variants | 64 |
| Paired solver comparisons | 256 |
| Expected mismatches | 0 |

Additional boundary tests cover stock depletion, resource replenishment, a shock destroying stock at t=0, common-cause component deletion, disabled actions, tight horizons and distinct individual-goal versus joint-plan feasibility. See [executable G2 model](../experiments/p1_gate2.py), [unit tests](../tests/test_p1_gate2.py), and [frozen diagnostic expected output](../experiments/g2_expected.json).

Reproduce:

    python -m experiments.p1_gate2
    python -m unittest discover -s tests -v

A passing run establishes **only** agreement for the tested bounded cases. No sample-size justification, adversarial solver proof, benchmark performance estimate, explanatory advantage or hypothesis-test p-value is claimed.

## Differences from G1 and what remains open

G2 is an **outcome/reachability engine**, not a plan-provenance and GBR engine. It does **not** transport G1's binary pathway score to consuming resources. In particular, two plans with individually adequate stock may not be jointly executable. No fault happens inside an action; no multiple correlated failures, continuous time, hidden environmental variables, concurrent operations, uncertain transition probabilities, utility or feedback-policy learning are modeled.

**Next gate (G3):** clarify plans versus policies, inventory-sharing and dynamic plan provenance; independently compute the post-fault outcome against an explicit augmented-state reachability baseline; then freeze statistical design and compare candidate predictors under held-out model families before claiming empirical benefit.

The interpretation "available after fault" is deliberately weaker than "must have failed and then been restored." Never substitute these endpoints without separate bookkeeping.
