# R14 — Inspect actual LANL node-failure records from a version-pinned public mirror

**Status: raw operational data-file audit, NOT field strict-restoration H1 validation.**

## Data source and restricted scientific claim

The [Los Alamos National Laboratory / USRC failure-data page](https://usrc.lanl.gov/data/failure-data.php) states that its 1996–2005 all-systems failure/interrupt CSV contains around 23,741 records and is released for research with LANL attribution (LA-UR-05-7318). The [USENIX CFDR description](https://www.usenix.org/cfdr-data) states that failure records track node/system outages, start/end times and cause types, and that interrupted jobs may be restarted from checkpoints. This does **not** establish unique job/service restored-state tracking or action-by-action policy observations in the released failure-event table.

A small compressed archived copy is available in the THIRD-PARTY [Derek-Jones/ESEUR-code-data public analysis repository](https://github.com/Derek-Jones/ESEUR-code-data), with a [README describing the schema](https://github.com/Derek-Jones/ESEUR-code-data/blob/bc1d9e99da2a956cdecba9d9d7f6f9b61a371c5f/reliability/LA-UR-05-7318-failure-data-1996-2005.README) and a version-pinned XZ-compressed CSV. The official LANL release notes universal research access and requests citation. R14 only downloads the fixed **mirror** version to a temporary CI workspace for a bounded, reproducible schema and data-quality check. R14 does not redistribute raw node-level rows or publish pseudonymous node/system IDs.

**Provenance caveat:** the mirror's Git commit ID and Git blob SHA1 authenticate which bytes GitHub served at THAT mirror revision. They **do not independently establish that the original LA-UR-05-7318 LANL file has identical bytes**. A SHA-256 checksum of the downloaded mirror archive is recorded after execution and later locked. This is a meaningful real file inspection, but *not* independent verification of upstream official provenance. No new physical H1 episodes are admitted.

## Raw audit methodology

1. In CI only, fetch the pinned raw mirror object using HTTPS and a strict file-size cap; compare the bytes' Git blob object ID to the fixed public GitHub tree SHA1.
2. Record the compressed-file SHA256 and byte count, and decompress the bounded XZ stream into a memory-limited CSV reader. Fail closed if the compressed or decompressed size is abnormal, parsing fails, required column names are missing/duplicated, or the input contains no records.
3. Count the entire file's nonblank records, but evaluate only the **first 256 well-formed raw records in archive order** for missing/fault times, parse errors, start-after-end cases, root cause classification, downtime field presence and pseudonymous system-count summaries. Avoid selecting records based on recovery outcomes. Do not publish row content or node identifiers.
4. Treat dates explicitly as local/unspecified-timezone values: no unverified UTC normalization, timezone precision, service-level downtime interpretation, or policy chronology. This QA is descriptive only.
5. Give H1 admission **zero** because the table's fault start/fixed timestamps are node-level administrative events; there is no externally validated service-goal ID, pre-fault state, observed nonanticipative action log, common-cause route ontology or timestamped same-goal restoration.

The previous [R13 intake contract](../experiments/p1_r13_real_data_admission.py) requires all of those absent links for a strict restoration label, and rejects node/equipment failure as a substitute. R14 deliberately makes no attempt to construct a fabricated service ID from node, workload type or outage end. This remains **an auxiliary physical-node failure corpus only**.

## Source details frozen BEFORE inspecting file contents

- Publisher: Los Alamos National Laboratory USRC; official catalog: https://usrc.lanl.gov/data/failure-data.php
- Third-party mirror: https://github.com/Derek-Jones/ESEUR-code-data
- Mirror commit: bc1d9e99da2a956cdecba9d9d7f6f9b61a371c5f
- Mirror file: reliability/LA-UR-05-7318-failure-data-1996-2005.csv.xz
- Fixed Git blob SHA1: 1f3c115dd319a2cbabc02d312bb733c60e1ef29d
- Raw file bytes are never committed; artifact contains only audit metadata and counts.
- The archive is subject to LANL attribution and whatever provenance/licensing verification a downstream full-study data custodian must complete.

## Reproduce the real-file audit (network required)

    python -m unittest tests.test_p1_r14_lanl_raw_probe -v

The [dedicated CI workflow](../.github/workflows/r14-lanl-raw-intake.yml) fetches the pinned raw mirror, checks its Git blob SHA, and executes:

    python -m experiments.p1_r14_lanl_raw_probe --input-xz YOUR_DOWNLOADED_FILE --sample-rows 256 --output r14_audit.json

Use the observed mirror archive SHA-256 as the exact expected SHA-256 on subsequent runs. Do not equate the audited sample with 256 independently sampled physical systems. No source data are sent to any external training service and no H1 model is fitted.

## Scientific decision

**An actually obtained raw node-failure file is more informative than publisher metadata**, because field presence and missingness can be verified. However node return from interruption is not strict restored service, and an independently verified original publisher-file checksum is still absent.

A genuinely qualifying H1 task must secure a service/job join to the actual interrupted workload, full pre-event capabilities and available backup resources, a fixed observed policy, actual goal loss, and restoration under the same episode with a validated physical fault-event map. Until then no independent field restoration label, population Brier gain or H1 inference is admissible. The original R8 and R12 scores remain frozen; P1 stays DRAFT_NOT_PREREGISTERED.

If a valid service-level corpus proves impossible, it is acceptable to preregister a DIFFERENT auxiliary node-time-to-repair study, but its target and novelty claims MUST NOT be relabeled as the original H1 hypothesis.
