# Critical novelty audit v0.3 — Issue #8

**Disposition: MAJOR REVISION. The positive novelty claim is a falsifiable research hypothesis, not an established theorem or field.**  
**Recorded:** 2026-10-26. The review is targeted, not an exhaustive/systematic novelty survey.

## 1. What is already representable

Chapter 3's finite capability construction, Chapter 4's path predicate, and G0–G4's time/resource/shock dynamics are ordinary finite transition systems when the state is suitably augmented. Appendix A.5 already establishes this for bounded sequences. G4 additionally uses a standard full-information augmented-state optimizer as an upper bound, not as evidence that an irreducible new formalism was invented.

The presence of endogenous named operations or a more readable grammar alone cannot negate state-space equivalence. **Do not claim to be the first general mathematical theory of creating possibilities.**

## 2. A useful negative proposition: no new information given complete inputs

Let X be the **complete pre-disturbance model and observables**: capability/rule identities, resource constraints, exposure/physical-unit mapping, declared shock distribution, horizon, and every permitted pre-failure variable. Let Z=f(X) be an exactly computed deterministic candidate GBR feature. Let Y be any future recovery outcome with a well-defined joint distribution with X.

**Proposition (conditional information redundancy).** If the comparator may use all of X, then for any loss for which an optimal predictor exists,

\[
\inf_{h(X,Z)}\mathbb E[\ell(Y,h(X,Z))]
=
\inf_{h(X)}\mathbb E[\ell(Y,h(X))].
\]

When mutual information is well-defined, \(\ I(Y;Z\mid X)=0\).

**Proof.** Since Z=f(X), each candidate predictor h(X,Z) is the X-only predictor x→h(x,f(x)). Conversely, any X-only predictor can ignore Z. Their attainable prediction classes coincide; hence their optimal risks are equal. This holds regardless of the empirical distribution, provided both classes are unrestricted. QED.

**Meaning:** an exact GBR computation cannot add independent *information* beyond the entire model from which it was deterministically computed. This is not a new theorem. Nevertheless, a compact feature **may** improve finite-data, limited-capacity or time-limited prediction by providing a helpful representation or inductive bias. That limited-resource advantage must be separately established, and the computation cost of Z must count toward the budget.

**Boundary:** if X is only a restricted summary while Z uses additional permitted raw data, improved predictive performance could merely reflect **extra input information**, not superior structure. Both competitors must have access to the same full raw pre-failure information.

## 3. Candidate *positive*, narrow claim, stated as a test

**Working claim (unverified):** On preregistered, *held-out generator families* and under identical pre-failure data access, a prespecified structural feature derived from constructive alternatives can improve a **capacity/computation-bounded** recovery predictor over comparators using ordinary redundancy, physical fault-tree/path sets, min-hit/min-cut, resource reserves, standard reachability and equal-information augmented-state controls, after accounting for feature computation time and memory.

The outcome must be realized, non-clairvoyant **policy-trajectory** behavior, not the best theoretical path under realized-fault foresight. A strict-restoration endpoint must specify actual loss and its denominator. Chapter 6 and Issues #10–#11 must freeze details **before** generating the confirmatory outcomes.

**Specific falsifiers:** (i) no held-out predictive benefit under equal raw observables and training/compute budget, (ii) the benefit disappears under identity-aware physical-fault and encoding refinements, or (iii) the metric is too computationally expensive for the declared budget. Any of these defeats the corresponding positive claim under the tested scope. Negative results belong in the book without post-hoc hypothesis substitution.

No primary loss, minimum effect size, sample size, training set or held-out families are frozen yet: **this is a target for preregistration, not completed preregistration**.

## 4. Correspondence / prior-technique audit

| Prior technique | What it already captures | Contrast with candidate GOG/GBR | Required fair test |
|---|---|---|---|
| Finite augmented-state transition systems / constrained control | Capability construction, resource use, transitions, shocks, feedback | Explicit rule grammar may compress the description, **not** expand expressive power | Equal-information optimal/receding-horizon policy under identical rules and costs; runtime/memory |
| Temporal AND/OR dependency graphs and directed hypergraphs | Conjunctive prerequisites and derived reachability | Rules already encode AND dependencies | Compare full dependency grammar and dynamic hypergraph closure, including resource constraints |
| Repair, reconfiguration and resilience models | Alternative components, service recovery, dynamic repair actions | A constructible alternate channel can be a known repair/reconfiguration path | Matched recovery policy under the same fault/repair schedule |
| Fault-tree analysis and minimal path/cut sets | Failure path sets, fault-event dependencies and minimal cuts; common-cause extensions | Binary disjoint plan support is a very coarse structural reliability surrogate | Exposure-identity-aware cut sets and dependency-sensitive reliability baselines |
| Viability theory | Constrained safe behavior and feasible future trajectories | An operational goal-restoration target is not automatically a distinct viability concept | Match horizon, admissible controls, safe/target predicates |
| Empowerment | Channel capacity from actions to perceived futures | Capacity/agency is not a binary backup-pair indicator | Matched observation/action model or explicitly justified tractable approximation |

This is a **comparison agenda**, not a completed mathematical mapping or claim of first use. Primary references include Aubin (viability), Klyubin et al. (empowerment), Tria and Di Bona et al. (novelty), and Ruijters & Stoelinga (2015, fault trees including cut sets and common causes, DOI https://doi.org/10.1016/j.cosrev.2015.03.001). A formal line-by-line equivalence audit of dynamic AND/OR repair models remains open.

## 5. Acceptance status

**Completed now:** a precise information-theoretic limitation, a scoped positive hypothesis, explicit falsifiers, and a preliminary prior-technique correspondence matrix.

**Still open in #8:** demonstrate an actual nontrivial time/computation/compression advantage, or explicitly conclude that GBR is only a candidate feature-engineering choice; perform the full prior-art equivalence review; run a frozen independent comparison. Neither mathematical priority nor predictive benefit is established.
