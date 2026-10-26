# Claims and evidence ledger — revision 0.2

| ID | Claim | Status | Grounding |
|---|---|---|---|
| C-001 | Reachability and viability are established mathematical fields | Prior work | Aubin 1991 / 2009 |
| C-002 | Correlated and higher-order novelty have quantitative research traditions | Prior work | Tria 2014; Di Bona 2025; Loreto et al. 2026 |
| C-003 | Empowerment quantifies control via action-perception information | Prior work | Klyubin et al. 2005 |
| C-004 | A constructed backup can preserve a pre-existing goal without new end goals | Illustrated in toy | Chapter 5, executable code and tests |
| C-005 | GBR gain improves held-out recovery prediction beyond robust baselines | **Unverified hypothesis** | Requires preregistered P1 |
| C-006 | GBR gain is mathematically novel | **Unverified; may be a reparameterization** | Formal equivalence audit |
| C-007 | Effects generalize across chemical, ecological and AI systems | **Unsupported aspiration** | Independent empirical replication required |
| C-008 | A new scientific discipline has been established | **Not claimed** | No supporting evidence |
| C-009 | Illustrative program output agrees with archived result | Software regression result | Seven independent assertions (not hypothesis tests) |

| C-010 | Optional construction cannot reduce existential reachable goals under nested transitions | Proven conditional statement | Appendix A.2 |
| C-011 | GBR gain is bounded by the number of baseline-reachable goals | Proven conditional statement | Appendix A.3 |
| C-012 | Finite construction dynamics admit augmented-state transition representation | Proven conditional statement | Appendix A.5 |

**Policy:** Do not promote definitions, examples or hypotheses into findings without independent evidence and explicit uncertainty analysis. Retain null results.

C-013: On 64 seeded tiny systems plus shock variants, two independent solver implementations agreed across 256 comparisons. **Status: software verification only**, not empirical scientific validation. See [G0](G0-verification.md).

C-014: LEAN engine validation of GBR is **not yet performed**. See [integration decision](../integrations/lean/README.md).

C-015: Under G1's explicit finite, nonconsuming, sequential production assumptions, two enumeration strategies agreed on all **192 tested plan-set comparisons** and their candidate GOG/GBR values. **Status: bounded software verification only.** See [G1 audit](G1-verification.md).

C-016: GBR gain implies recovery under arbitrary correlated shocks. **Refuted by shared-component counterexample and exposure sensitivity.** See [G1 audit](G1-verification.md) and Chapter 7.

C-017: G2 implements post-fault existential reachability with finite consumable stock and one in-run boundary event, and compares DFS history enumeration to layered state search. **Status: software verification only.** See [G2](G2-verification.md). No statement about probabilistic resilience, GBR predictive value or real systems follows.

C-018: G3 distinguishes existential post-fault availability, retention, strict restoration conditional on *actual* fault-caused loss, and joint target attainability. **Status: operational definitions and bounded software checks only.** See [G3 report](G3-verification.md).

C-019: Individual attainability of two goals implies attainable simultaneous possession under shared consumable inventory. **False:** the one-kit/two-goal counterexample has both goals independently attainable but no joint feasible execution. See [G3 report](G3-verification.md).

C-020: G3 verifies GBR predictive superiority or non-clairvoyant adaptive policy quality. **Not claimed**; perfect foresight is part of the present diagnostic model.
