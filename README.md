# Foundations of Possibility Dynamics

**Working scientific monograph v0.2 (26 October 2026)** — an open research record, **not an established scientific discipline or empirically validated general theory**.

[Read the 10 chapters](book/index.md) · [Persian guide](README.fa.md) · [Research protocol](research/protocol.md) · [Claims ledger](research/claims.md) · [Technical review](research/scientific-review-v0.2.md)

## Aim

Study how bounded systems generate, lose and rebuild *operationally reachable* capabilities under resource and time constraints. Test whether constructible backup routes predict disturbance recovery above established network redundancy, reachability, viability and empowerment measures.

## Present scientific status

The book contains finite-system definitions, candidate GOG and GBR gain measures, a hand-designed illustrative communication scenario and a detailed prospective experimental protocol. **No ensemble validation, cross-domain tests or general physical law has been established.** Known augmented state-space methods may describe the same phenomena.

## Reproduce and build

Requires Python 3.9+; Pandoc for publication artifacts.

    python -m unittest discover -s tests -v
    python -m experiments.toy_case
    python scripts/check_book.py
    bash scripts/build_book.sh

The build generates HTML and EPUB in the ignored dist directory. GitHub Actions runs unit/integrity checks and uploads HTML/EPUB build artifacts. An illustrative example is not confirmatory scientific evidence.

## Scientific integrity

See the [claims ledger](research/claims.md) before citing a statement as a result. Negative evidence and mathematical counterexamples are essential. The editorial roadmap and caveats are in [the self-review](research/scientific-review-v0.2.md).

## Attribution and licensing

Formal author credit and an open-content license have **not been agreed or granted**. A public repository does not automatically provide an open license. Third-party sources are cited, not reproduced.

**Formal audit:** [Mathematical propositions and counterexamples](appendices/A-mathematical-propositions.md) · [Artifact provenance](appendices/B-reproducibility.md).

## P1 G0 verification and external tools

[Gate G0 report](research/G0-verification.md): two independent bounded reachability solvers agreed on 256 fixed-seed comparisons over 64 synthetic instances and their shock variants. This is **software verification, not evidence for H1**. Run: python -m experiments.p1_gate0.

[QuantConnect LEAN decision](integrations/lean/README.md): potentially useful for a *later financial-domain transfer*, but is not adopted as the core mathematical simulation engine. No LEAN backtest was run.

## Latest verification: Gate G1

[Gate G1 report](research/G1-verification.md) and [code](experiments/p1_gate1.py): bounded causal plan-support tracking, scope-dependent backup calculations and pre-plan shocks. Two enumeration approaches agreed on 192 complete plan-set comparisons from 48 tiny sampled models and paired starting-source failures (no disagreements); 13 dedicated tests were added. **This is only a software/formal gate, not a predictive validation or mathematical novelty result.** Future studies remain subject to preregistration and robust baselines.

## Latest bounded verification: Gate G2

[Gate G2](research/G2-verification.md) introduces discrete **consumable inventory**, replenishment, and a **single in-run fault at a tick boundary**, evaluated by independent exhaustive DFS versus time-layer state-set search. It checks *post-fault goal availability*, which can mean retention as well as restoration. [Executable experiment](experiments/p1_gate2.py), [expected diagnostic](experiments/g2_expected.json), and [tests](tests/test_p1_gate2.py) are versioned. These software checks are **not GBR prediction experiments** or evidence for H1.
