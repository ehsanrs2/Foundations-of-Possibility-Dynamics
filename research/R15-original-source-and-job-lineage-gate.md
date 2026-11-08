# R15 — Publisher-original LANL authentication and *same-job* recovery linkage gate

**Status: R15 implementation and source-feasibility investigation, 2026-11-08. NOT independent field H1 verification; no service-level restoration data admitted.**

## Decision and reason to stop at the evidence boundary

The previously archived R14 [raw source QA](R14-lanl-mirror-raw-audit-20261108.json) read **23,739 nonblank node-failure records** from a commit- and blob-pinned public third-party copy of the LANL 1996–2005 all-systems interruption dataset. Its **26 observed CSV header fields** include anonymized system and node IDs, failure/administrative-fix timestamps, downtime and classified cause. **None is a stable individual job/service identity, restart lineage ID, checkpoint ID, policy action, pre-fault service-state observation, backup-asset graph or resource/action history.** No H1 labels can follow from node's "Prob Fixed" field.

R15 tested the **publisher-direct original-file authentication dependency**. [LANL's official failure-data page](https://usrc.lanl.gov/data/failure-data.php) publicly lists a 336K compressed original **tar.gz**, 23,741 records, and additional separate system-specific USAGE/EVENT files, with universal research release and LANL attribution. The R14 mirrored XZ contains 23,739 data rows rather than the publisher's 23,741; this unresolved discrepancy cannot be settled by guessing a counting convention.

The [R15 network-safe publisher link probe](../experiments/p1_r15_upstream_probe.py) requests the **official landing page**, parses *real LANL HTTPS link targets* rather than guessing archive paths, rejects off-domain redirects, and reports download availability without accepting data. The initial [GitHub Actions probe](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/actions/runs/42453167471) yielded **UNAVAILABLE_OR_UNVERIFIED (URLError)** in its runner: NO publisher-original tarball was fetched; NO original CSV checksum was compared; the R14 mirror **is not authenticated against the publisher**. The R15 source-discovery result is an observable environment-dependent run artifact; a later successful website request must not be silently retroactively ascribed to this attempt.

## Separate usage/event archives are real descriptions, not proven service joins

The publisher explicitly lists the following *separate* system-20 operational collections:

| Published source | Publisher-listed record count | Actual R15 raw rows independently inspected |
|---|---:|---:|
| All-systems node failure/interrupt log, 1996–2005 (R14 mirrored file only) | 23,741 | 23,739 mirror records in R14 |
| System 20 usage with node info | 489,376 | **0** |
| System 20 event info | 433,490 | **0** |

These archives may help with node/time availability and scheduling studies, but **the mere existence of "usage" or "event" rows is not documentation of a valid stable original job ID, restart-attempt lineage, unambiguous job→node connection, or complete fixed-policy observation/action sequence**. The system/node identity and timestamps may be link *candidates*, not established causal or recovery joins.

The [USENIX historical LANL dataset description](https://www.usenix.org/lanl-data) explains that workloads are often checkpointed, that a failed node can stop a job, and that jobs may be restarted on different nodes or from scratch. This confirms why a *genuine* same-job restart study is worth pursuing; it does **not** prove the public node-failure CSV can track a particular original job through restart, its target regained, or the intervention policy. Avoid the tempting shortcut "node fixed" = "same job resumed" = "goal regained".

The R14 source format is a device-fault table; no per-job recovery outcomes or independent physical backup route ontology has been established. A complete statement about what the uninspected usage/event archives contain would exceed the evidence.

## Executable R15 linkage guard

[The R15 linkage code](../experiments/p1_r15_linkage_gate.py) loads **the actual archived R14 CSV schema** and inspects its observed 26 names. It fails closed unless independently verified evidence for ALL of the following exists:

- Authenticated publisher-original file and authenticated supplementary usage/event sources with documented clock and anonymization mapping.
- Unique stable identity of the **same original job** across an interrupted run and each subsequent restart attempt, beyond anonymized system and node IDs.
- An actually observed, active **pre-fault job goal**, an incident-caused actual loss of that goal, a timestamped subsequent goal reacquisition before a fixed deadline (or explicit right censoring).
- A fixed nonanticipating **observed** controller policy, what it knew, interventions and stock/resources along the **same** episode.
- Verified mechanisms and common-cause fault exposure, independent physical unit boundaries and allowed analysis use.

An explicit toy ambiguity demonstrates the trap: two distinct synthetic job IDs can both overlap the *same* node failure in system, node and time, yet neither overlap validates that the original job was lost or later restored. The code's time-overlap helper is a *candidate finder*, never an H1 admission rule. A matched job ID alone is likewise not externally verified checkpoint restart lineage.

Every demo is **SYNTHETIC**. The R15 tool has no code path declaring a field H1 observation, even if passed plausible matching timestamps. See [fifteen independent negative/control tests](../tests/test_p1_r15_linkage_gate.py).

## Reproducibility

    python -m unittest tests.test_p1_r15_upstream_probe tests.test_p1_r15_linkage_gate -v
    python -m experiments.p1_r15_upstream_probe --output r15_publisher_probe.json
    python -m experiments.p1_r15_linkage_gate

The R15 workflow rechecks the raw R14 artifact and source-link discovery; the latter is explicitly **not a stable publisher-data provenance verification** while original direct download is unavailable. The deterministic join gate can be archived and compared exactly. Neither raw per-node IDs nor job/user identifiers are exported.

## What would make a genuine physical H1 test admissible?

The next *real-data* step must obtain independently confirmed original LANL bytes (or a documented custodian checksum and archive provenance), **and separately** raw access to compatible job usage/event data. Even then, an independent domain custodian must justify *unique* job-run lineage and checkpoint restart semantics, event-to-job causal link, exact pre-fault goal state, policy action history, physical backup capacities and endpoint censoring.

If those cannot be verified, the defensible alternative is a **distinct preregistered node fault duration or usage scheduling question**. No statistical test of the originally framed H1 is permissible on the currently observed tables. The original R8 no-gain outcome and R12 synthetic comparisons are unchanged, H1 preregistration remains DRAFT, and all sealed test families remain closed.
