# Appendix D — Separate estimands and candidate loss-conditioned endpoint

**Status: prospective PRE-FREEZE specification, not registered confirmatory P1 or H1 evidence.** Responds to reviewer [#11](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/11), with dependency on [#10](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/issues/10).

## D.1 Three non-interchangeable claims

**A. Optional-action eligibility theorem:** if construction merely adds optional legal actions without changing baseline costs/resources, existential reachable goals cannot decrease. This is a conditional definitional fact (Appendix A), **not** experimental evidence of resilience.

**B. Predictive increment (future primary H1):** under identical permitted pre-shock raw observables X, learning capacity and feature-computation budget, does a *prespecified, physically justified* structural feature Z=f(X) improve out-of-family prediction of an executable policy outcome Y beyond strong network/cut/reachability features?

Define the future prospective estimand

\[
\Delta_{\mathrm{pred}}=\mathbb E_{\mathrm{heldout}}
 [L(Y,\widehat Y_{\mathrm{base}})-L(Y,\widehat Y_{\mathrm{aug}})].
\]

Positive means improved held-out predictive loss. **H0: Delta ≤ 0; H1: Delta > 0**, subject to a practical effect-size and uncertainty rule yet to be frozen. The unrestricted optimal predictor with all X cannot gain new information from deterministic Z=f(X); any benefit would be finite-data, computation-bounded or representational.

**C. Causal intervention effect:** a separately randomized physically realizable intervention that *changes actual generative capability* might alter observed restoration, with

\[
\Delta_{\mathrm{causal}}=\mathbb E[Y(1)-Y(0)].
\]

Manipulating a numerical score is not automatically a causal intervention. Interference, measurement validity and confounding control must be specified independently. This is **exploratory and unidentified**, not inferred from A or B.

## D.2 A candidate strict-restoration denominator (not yet frozen)

For independent instance i, predefined goal g, and realized shock rollout omega under **one common, frozen, non-anticipative evaluation policy**, register:

- A: goal was held immediately BEFORE the shock;
- L: goal was held then and actually REMOVED by that shock;
- R: L occurred and the SAME trajectory reacquired the goal by deadline H.

R cannot equal 1 when L=0. The tentative per-instance outcome is

\[
Y_i=
\frac{\sum_{\omega,g}w_\omega L_{ig\omega}R_{ig\omega}}
{\sum_{\omega,g}w_\omega L_{ig\omega}}.
\]

The weights are prespecified shock probabilities or prespecified sampling weights. **A denominator of zero yields an undefined outcome, not a fabricated zero or one.** Never-lost goals belong in separate retention/availability reports. Truly lost goals not regained by H count as failure; time-to-event censoring requires its own explicit rule.

Selection caveat: a policy may change whether L occurs. Compare predictive models on outcomes generated under **the same evaluation policy and same at-risk protocol**; for interventions changing policies/actions, define a fixed eligible population or properly analyze selection into actual loss. Do not compare different loss-conditioned denominators as though they were a causal contrast.

## D.3 Hard preregistration dependencies

Before confirmatory sampling, freeze the physically evidenced event identity/incidence map (Appendix C); the final feature and representation contract; shock distributions and observation histories; a non-clairvoyant rollout policy and equal-information baselines; the exact primary outcome, denominator-zero rule, loss, goal sampling, model family splits, sample size/precision, realistic compute caps and independent-unit uncertainty procedure. Reserve untouched held-out generator families. Archive negative outcomes and deviations.

**No P1 H1 statistical test, independent-domain validation or causal effect has yet been completed.** This appendix only prevents those distinct claims from being conflated.
