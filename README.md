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
