# Appendix A — Provable properties and limits

**Scope:** exact statements about the finite *definitions* in Chapters 3–4. These propositions do not prove predictive usefulness or the originality of Possibility Dynamics.

## A.1 Assumptions

Let the capability vocabulary U, available resource states, environmental states, goals and legal operations form finite sets. Let the horizon H be finite. The construction-enabled system contains **all** baseline transitions with unchanged costs and feasibility, plus optional construction transitions. All comparisons start from the same state s, share budget B and evaluate the same target predicates.

If construction changes initial holdings, renders existing actions unavailable or forces resource consumption, the inclusion assumption fails and the results below do not automatically apply.

## A.2 Proposition: monotonic goal reachability

**Statement.** Under the assumptions above,

\[
\mathcal R^0_{H,B}(s)\subseteq \mathcal R^+_{H,B}(s).
\]

**Proof.** Let goal g be in the baseline reachable set. Then a legal baseline trajectory of at most H steps and cost at most B reaches g. Every transition in that trajectory remains available, at the same cost, after optional construction operations have been added. Taking the same trajectory reaches g in the enlarged system. Therefore g is in the construction-enabled reachable set. QED.

**Consequence.** The GOG candidate is nonnegative. This is a trivial monotonicity statement about nested action sets, not a new scientific law.

## A.3 Proposition: bounds on GBR gain

For each baseline-reachable goal g let b0(g) and b+(g) be the binary existence indicators for two distinct feasible plans with disjoint **F-exposed** dependencies as in Chapter 4. Since the baseline feasible-plan set is included in the enlarged set, any pair witnessing b0(g)=1 also witnesses b+(g)=1.

Therefore,

\[
0\leq \mathrm{GBR}_{gain}(s)\leq|\mathcal R^0_{H,B}(s)|.
\]

**Proof.** For every included goal, b+(g)-b0(g) is either zero or one. Summing yields the bound. QED.

**Important caveat.** If F is empty, *any* pair of distinct plans has disjoint exposed dependencies: the indicator can become meaningless. A meaningful fault model must specify which dependencies are exposed.

## A.4 Proposition: invariance under relabeling

Suppose a bijective renaming of capability labels is applied simultaneously to initial holdings, production prerequisites and outputs, target predicates and fault-exposure sets, preserving every operation's cost and duration. Then legal trajectories and feasible plans correspond bijectively, with identical costs and dependency intersections. Consequently GOG and GBR gain do not change.

**Proof.** Map each step of any legal trajectory through the bijection, and map it back with the inverse. Both mappings preserve legality, targets, cost and exposed-set disjointness. Reachable goal sets and witness pairs therefore correspond. QED.

**Boundary.** Splitting a capability into several interacting labels is not a bijection and need not preserve the metrics.

## A.5 Proposition: finite state augmentation equivalence

Let S be the finite set of all triples (capability subset, resource state, environment state). Include every allowed construction and ordinary action as a labeled edge between states in a conventional transition graph on S, with costs and times attached.

**Statement.** A goal is reachable under the original finite generative rules if and only if it is reachable in the augmented ordinary transition system under the same constraints.

**Proof.** By construction, the two descriptions have identical initial state and legal one-step transitions. Induction on trajectory length gives a one-to-one correspondence of every legal finite trajectory. Their reachable target sets coincide. QED.

**Consequence.** Dynamic capability creation is not intrinsically beyond standard finite-state control theory. Possible research contributions must instead concern useful structure, explanation, efficient compression, restricted observability or empirically validated predictions.

## A.6 Counterexample: GBR does not determine recovery probability

Consider two fully established routes whose exposed components are disjoint and whose failure events have marginal probability p (0 < p < 1). Both systems receive the same binary backup indicator. In one population, route failures are independent, so the probability that **at least one route survives** is 1-p². In another, both routes suffer perfectly correlated failures, giving survival probability 1-p. Despite equal structural scores, recovery probabilities differ. Thus GBR alone cannot determine recovery without the dependence structure of shocks.

This is an analytic counterexample, not new empirical data.

## A.7 What remains unproved

No general predictive superiority of GBR, no causal effect of increasing it, no theoretical irreducibility beyond familiar control representations, and no cross-domain law is proven. Strong empirical evaluation remains necessary.


## A.8 Conditional information redundancy of a deterministic feature

Let X be the *complete* preregistered pre-failure input representation and Z=f(X) an exact deterministic feature (including candidate GBR). Every predictor h(X,Z) is the X-only function x↦h(x,f(x)). Conversely, an X-only predictor can ignore Z. Therefore the infimum achievable expected loss over unrestricted predictors is identical with and without Z. When defined, conditional mutual information I(Y;Z|X)=0. **This is elementary information redundancy, not a novel scientific law.** It does not rule out empirical advantages in finite sample size, capacity-limited learning, compression or fixed compute budgets, where calculating Z itself must be budgeted.

See [the explicit reviewer novelty audit](../research/novelty-audit-v0.3.md) for limitations and falsifiers.
