# Internal scientific and reproducibility review — 2026-10-26

This is **a self-review**, not independent peer review.

| Issue identified | Disposition |
|---|---|
| v0.1 GBR prose counts presence whereas code counts incremental redundancy | **Corrected** formula in Chapter 4 to GBR gain |
| Independence was interpreted without clear vulnerability scope | Added explicit set F and common-cause counterexamples |
| Finite predeclared capability universe may be confused with truly unforeseen futures | Bounded scope retained in Chapters 3, 7 and 9 |
| State augmentation may already encode all generation and recovery | Added equivalence threat and full-information baseline |
| Synthetic demonstration might be confused with evidence for H1 | Restored archived example and JSON with seven software regression tests |
| Contemporary novelty literature incomplete | Added 2025 higher-order novelties and 2026 Oxford monograph |
| Book had no reproducible rendering process | Added Pandoc HTML/EPUB build, integrity checks and CI |
| Author and licensing governance unspecified | Leave ownership and publishing license explicitly unresolved; do not invent author consent |

## Local technical checks

Seven Python standard-library unit tests passed against the recreated example, and its output matched the archived v0.1 JSON. Pandoc HTML/EPUB pipeline was tested locally on a ten-chapter fixture. Neither action measures scientific novelty or predictive performance.

## Remaining barriers to an actual scientific finding

Formal equivalence literature review; finalized P1 preregistration and sample-size justification; independent simulator oracle; adequately controlled benchmark datasets; uncertainty analysis; expert peer review. We must not describe these as complete.
