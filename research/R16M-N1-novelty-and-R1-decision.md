# R16-M / N1 — Scientific decision on R1, separate generativity research

2026-11-25. **Proposed decision, retrospective development only.** Source main 39590fd350a3b413e122b0eba0dc1a0650b1d3d7 (merged #42 and #43). No sealed samples, no external field labels, no preregistration.

## Observed evidence and failure analysis

R8's historical primary R1 feature had zero incremental Brier gain. In C2a's measured developer evaluation (run 45558400768), grouped DEV_EVAL Brier was 0.1595602648531204 raw, 0.16040127346668326 raw plus R1, and 0.1552048132360558 raw plus conventional joint-readiness DP. Thus R1 was worse than raw and the conventional DP in this particular designed transfer. Neither this nor earlier R8 is a population-level H1 rejection.

N1 revisits exactly the 108 existing C2a parameter rows (36 designed structural groups, three priors each), never a new holdout. It checks the equality of R1 with a threshold of the event hitting-set cut and with the interaction of independent route mode and positive kit stock. Since those two raw inputs were already provided, R1 adds no information to those raw summaries in this population. It may still act as a nonlinear interaction for a restricted learner; this diagnostic does not imply identical ridge predictions or universal predictive uselessness.

N1 searches for different model-exact conditional restoration probabilities while mode, stock, prior, R1 and cut remain equal, exposing information lost about temporal structure and fixed-policy ordering. It also reports exact retrospective within-cell target variance (excess expected Brier of an oracle restricted to cell-constant forecasts). This is descriptive, in-sample, and neither fitted forecast performance nor a generalization estimate.

**Proof boundary:** disjoint nonempty event supports require at least two events to hit all routes, but a cut of size two need not imply a disjoint pair. The triangle of footprints {a,b}, {b,c}, {a,c} has cut size two and no disjoint pair. Therefore the observed two-route C2a equality is NOT a general theorem identifying R1 with min-cut. Neither quantity establishes joint feasible preparation, policy performance or physical independence without an externally justified ontology.

## Proposed decision N1

Pause preparation of an R1 confirmatory test pending independent review. Preserve the primary draft, negative archive and sealed populations; do not replace R1 with DP readiness after looking at developer outcomes. No final statistical rejection of H1. An independent reviewer may recommend retirement of this candidate, or justify a genuinely different preregistered population with varying nonredundant R1 under fixed matching assumptions. A new hypothesis needs a new prospective protocol, not an edited historical result.

Possible contribution at present: transparent operational semantics, explicit counterexamples, limits of static redundancy for actual restoration and reproducible evaluation under a restricted information/budget contract. No evidence of a new independent science or a new physical law.

## GOG: separate research track, GOG-1 proposal

Return to the broader mission of constructive creation of operationally reachable goals, not only restoration. Fix goal ontology, unit of time, resource accounting, physical action identity and observer before scoring. GOG is the difference in reachable goal sets under optional construction vs no construction. Since allowed action sets are nested, the inclusion and nonnegative count are definitional; ordinary augmented-state reachability computes the same sets. Do not claim novelty for this identity.

First independent development question: can a representation of the *same* goal set make bounded reachability cheaper under explicitly measured total computation without losing time/resource semantics? Use ordinary state search with dominance/pruning and AND/OR dependency methods as strong comparators; compare exact goal sets, not count alone; include alias, cost/time, vocabulary, shared prerequisite and mutually exclusive goal negatives. Freeze scope and method before new development families; no H1 families. If no advantage, report negative and retain GOG as a descriptive measure. A causal intervention question needs separate risk-set and experimental design. No substitution into H1.

## B7a status

The local process pilot (#43) executed owned-child restart and no-restart controls in CI, but operator and assessor are the same and the workload is trivial. Keep external field admission blocked. A real independent assessor/custodian, isolated apparatus and clock/evidence verification remain required.

Reproduce N1 with python -m unittest tests.test_p1_r16m_n1_r1_information_audit -v and python -m experiments.p1_r16m_n1_r1_information_audit. This proposal does not close issues #3 or #8–#12.
