# R16 — LANL publisher-original integrity and System-20 Usage/Event lineage admission protocol

**Status (2026-11-08): PROTOCOL ONLY / EMPIRICAL INTAKE BLOCKED.** R16 is NOT a preregistration or a test of H1. No original LANL archive, System-20 Usage archive, or Event archive is claimed to have been downloaded or inspected by R16. All H1 evaluation families remain sealed.

## 1. Frozen inputs and starting evidence

- R14 read 23,739 nonblank data rows, 26 fields from a Git-commit-pinned **third-party XZ mirror**. Compressed mirror SHA256: `ed32fd254a013df79f5f475f4eac85980f7229735e100ac427343ef449a75140`. This is a **mirror checksum, not a publisher checksum**.
- Publisher page lists 23,741 all-systems failure records. The -2 discrepancy is UNRESOLVED.
- R15 failed to retrieve the publisher original from its CI runner (URLError), and has not ingested either System-20 Usage or Event archive. Its deterministic fail-closed demonstration admitted zero real strict-restoration H1 observations.
- Official catalog: https://usrc.lanl.gov/data/failure-data.php ; historical usage/failure context: https://www.usenix.org/cfdr-data .
- Publisher lists original tar.gz + README, System-20 node-level Usage (489,376 records), and System-20 Event (433,490 records). These counts are **publisher declarations, not R16 parsed observations**.

## 2. Ordered physical-source evidence procedure

### A. Retrieve and authenticate publisher-original bytes

1. Obtain download links **from the official LANL HTML page**, not guessed host/path strings. Record retrieval UTC timestamp, URL, redirect chain, status, compressed bytes, final host, and SHA256 for each of the three retrieved archives. Allow only clearly authorized LANL origins or a documented curator-sanctioned mirror; an unverified third-party mirror cannot be promoted to publisher original.
2. Verify tar.gz stream, reject traversal paths, links, unexpected archive members, excessive decompression, and non-text unexpected payloads. Store hashes and metadata only; do **not** commit data/rows/pseudonymous identifiers.
3. Extract and archive README schema/clock/unit descriptions and observed member names and SHA256 values; preserve exact file bytes, encoding, delimiter, and column order.
4. Obtain **publisher-published** SHA256 or signed manifest when available; distinguish `PUBLISHER_DIGEST_VERIFIED`, `DIRECT_PUBLISHER_FETCH_NO_INDEPENDENT_DIGEST`, `CUSTODIAN_ATTESTED`, `THIRD_PARTY_MIRROR_ONLY`, and `UNAVAILABLE`. A checksum calculated locally over a direct download proves repeatability of the fetched bytes, **not independently** their publisher-stated digest.
5. Compare canonical publisher failure CSV and R14 mirror by byte content first, then documented normalization (compression, line endings, record terminator, header). Report *all* discrepancies and the 23,741 vs 23,739 record mismatch. Never infer that the two-record difference is just a counting convention.

### B. Inspect System-20 Usage and Event

For each actual archive separately record: member paths, README, schema headers, parsed row count, malformed/duplicate/missing fields, time units/timezone and clock synchronization, anonymization and zero-based node indexing. Check whether the failure table's System-20 node representation is independently documented to share exactly the same machine topology, numbering and timescale. Historical layout snapshots do not guarantee a stationary node map.

Document, with literal README/field citations (and without exporting individual IDs), the existence and semantics of:
- immutable **original job identity** and independent **attempt/run identity**;
- scheduler lifecycle statuses (submit, dispatch, interrupted/failed, resubmitted/restarted, completion);
- checkpoint/restart linkage to the *same original job*, including node migration;
- timestamped allocated nodes, overlaps, shared incident references and cancellation semantics;
- pre-failure goal-active observations and post-failure **same goal** attainment;
- exact observed controller actions, information and resources under one fixed nonanticipative policy.

The existence of a `job_id`-like column alone is **NOT** proof that restart attempts preserve identity; time/node overlap is candidate-only, not a causal or same-job match.

### C. Candidate join audit, not an H1 outcome

After source authentication and README semantic review, build only privacy-safe aggregates of candidate associations. Require independently documented `original_job_id -> attempt_id -> incident_id` relationships; prohibit using mere equality of node/time as a unique identifier. Count unique, ambiguous, missing and conflicting candidate joins and maintain explicit unresolved classifications. Verify examples under independent custodian scrutiny before any recovery interpretation.

Reject false equivalences: `Prob Fixed` != job resumed; job end-time != same goal regained; resubmission != checkpoint restart; node uptime != guaranteed service restoration.

## 3. R16 decision gates

| Gate | PASS requires | If not met |
|---|---|---|
| G16-P source provenance | Original-bytes chain plus explicitly classified publisher/custodian digest status; count discrepancies documented | BLOCKED_SOURCE_AUTHENTICITY |
| G16-S schema and clocks | Actual Usage/Event data/READMEs parsed, node/time identifiers and maps validated | BLOCKED_SCHEMA_OR_CLOCK |
| G16-J lineage | Stable original-job and attempt/restart relationship independently documented and empirically unambiguous | BLOCKED_SAME_JOB_LINEAGE |
| G16-C causal endpoint | Observed pre-fault original goal, fault-caused loss, timestamped same-goal recovery/censoring | BLOCKED_RECOVERY_ENDPOINT |
| G16-H strict H1 admission | All preceding plus fixed policy/actions/resources, competing mechanisms, independent units, common-cause fault map and separate locked H1 preregistration | H1_SEALED_NO_CONFIRMATORY_TEST |

G16-P digest status must be transparently reported even when no official published digest exists; a direct official-host fetch may strengthen provenance without warranting the false label 'publisher checksum verified'. **A G16-J PASS alone cannot unlock H1.**

## 4. Precommitted alternative if job lineage is unavailable

Create a **separate** node time-to-administrative-fix study, not a relabeled H1. Unit: observed node-interruption record, clustering by physical system/node when stable, with shared events and repeat failures handled explicitly. Define time origin = `Prob Started`; candidate endpoint = `Prob Fixed`; validate semantics against publisher README before calling it repair. Report missing intervals, zero/negative durations, overlapping events, recording truncation, administrative versus physical repair distinction, censoring and timestamp ambiguity. Specify survival analysis and sensitivity to grouping, cause, system, and era. Register this distinct question separately before confirmatory estimation. **No result of this auxiliary study may be interpreted as evidence for H1 strict restoration or possibility dynamics.**

## 5. Output contract and immutable scientific state

Produce privacy-safe `R16-source-intake-results.json` with fields: UTC run date, each source URL and provenance class, digest algorithm/value/source, archive/README/CSV SHA256, publisher vs actual row counts, exact column schemas, missingness aggregates, node/clock map documentation status, join candidate ambiguity counts, each gate verdict with explanation, and `new_confirmatory_h1_samples: 0` unless a separately authorized and preregistered H1 study actually runs. Never export raw rows or identifying node/job IDs.

Current evidence-based verdict (2026-11-08): **G16-P=BLOCKED; G16-S=BLOCKED; G16-J=BLOCKED; G16-C=BLOCKED; G16-H=SEALED.** No new raw publisher/Usage/Event bytes were available for direct R16 verification at protocol creation. H1 remains DRAFT_NOT_PREREGISTERED. R8 negative outcome, R12 synthetic results, R14 mirror audit and R15 controls are unchanged.

## References

- LANL official catalog: https://usrc.lanl.gov/data/failure-data.php
- R14 intake and audit: [R14](R14-lanl-actual-raw-node-fault-intake.md), [audit](R14-lanl-mirror-raw-audit-20261108.json)
- R15 linkage and archived results: [R15](R15-original-source-and-job-lineage-gate.md), [results](R15-node-job-lineage-results-20261108.json)
- Historical context: https://www.usenix.org/cfdr-data
