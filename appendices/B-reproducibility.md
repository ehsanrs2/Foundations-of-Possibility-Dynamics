# Appendix B — Provenance and reproduction

**Status:** reproducible demonstration, not scientific validation.

The first hand-designed model was supplied as part of the exploratory Possibility Dynamics research charter. The prior source file and JSON have been migrated into experiments as a reformatted, behavior-preserving code copy and a matching output JSON.

## Recorded original local file hashes

- Original Python file SHA-256: 9a7e12ca03e20faaed01bdfa5c9675c7f2b50de80aa90121d7f5199f61360d38
- Original JSON SHA-256: db7ea6f70834ef8f0934e8ed7f34aa67299db698c03407b49e8c83140bda140b

These hashes refer to the **original local source artifacts**, not the GitHub-adapted formatting. No claim of byte-for-byte identity of the Python source is made.

## Reproduce

From the repository root using standard Python 3.9 or newer:

    python -m unittest discover -s tests -v
    python -m experiments.toy_case
    python scripts/check_book.py
    bash scripts/build_book.sh

Pandoc is required for the book export. The toy Python example uses no third-party packages.

## Scope of testing

- Deterministic goal reachability and the initially zero new-goal count
- Recovery after a specifically selected wire-transmitter shock
- Loss of recovery with failures in shared power or sensor
- Time and construction-kit restrictions
- Failure-sensitive dependency independence
- Agreement with archived numeric and Boolean JSON outputs

The outputs are **not** repeated random trials, population samples or H1 hypothesis tests. All parameters were chosen by hand to illustrate the concepts.

## Next reproducibility gate

An independently implemented exhaustive state-search oracle, a frozen preregistered experiment with sampled network families, explicit random seeds, environment manifests and uncertainty intervals must precede any confirmatory claim.
