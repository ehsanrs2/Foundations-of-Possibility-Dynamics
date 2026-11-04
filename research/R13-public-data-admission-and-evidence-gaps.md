# R13 — Public physical-data admission and honest evidence gaps

**Review date: 2026-11-04. Status: PUBLIC DESCRIPTIONS ONLY; ZERO raw records retrieved or validated; NOT H1, NOT preregistered.**

## Question and current answer

Can public data substantiate **actual goal loss caused by a physical fault followed by restoration of the same goal on the same observed non-anticipative policy trajectory**? From six publisher/official descriptions screened here, **NO source is yet demonstrated to satisfy the entire contract**. This is a statement about current documentation and verification, not proof that corresponding data can never exist. No source files or episodes were actually downloaded, independently linked or assessed at row level.

The [six-source evidence register](R13-public-source-admission-manifest.json) preserves the verified publication URLs, observed unit, candidate uses, 11 strict-evidence fields and unresolved gaps. None is admitted for H1.

## Reviewed public candidate sources

| Published source | What is documented | Why it does NOT currently qualify for strict H1 |
|---|---|---|
| [PNNL / DOE Event-correlated Outage Dataset in America](https://catalog.data.gov/dataset/event-correlated-outage-dataset-in-america) | County-level customer outages in 15-minute intervals correlated with DOE-417 major events, available in the U.S. data catalog, with CC BY 4.0 listing. | A decrease in total outages is not proof the SAME individual customer's service returned, or which policy actions and physical assets caused it. No raw record audited. |
| [ORNL EAGLE-I Power Outage Data 2025](https://impact.ornl.gov/en/datasets/eagle-i-power-outage-data-2025/) | Public utility outage-map observations, county and FIPS counts of customers out, at 15-minute intervals. | The observational unit is an aggregate area/time, not a uniquely linked service episode; the individual restoration and policy chain is not demonstrated. |
| [DOE-417 electric emergency reports](https://doe417.energy.gov/) and [EIA disturbance archive](https://www.eia.gov/electricity/data/disturbance/disturb_events_archive.html) | Utility-reported major emergency/disturbance events and times. | Incident start/end or restoration information is not enough for a verified same-service policy trajectory with preevent resources. Raw annual event rows not inspected. |
| [LANL USRC historical HPC failure datasets](https://usrc.lanl.gov/data/failure-data.php), [USENIX description](https://www.usenix.org/cfdr-data) | Historic node outages, component failures, system/usage event collections, and categorized cause; some node intervals. | A node back online is not proof that one identified pre-fault job/service recovered its lost goal under a documented policy. |
| [Backblaze Drive Stats](https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data) | Daily drive S.M.A.R.T. snapshots and component failure data; free-to-use terms with attribution and non-resale constraints. | A failed disk does not necessarily produce service loss; no same-service reconstruction or recovery policy is established by the documented disk rows. |
| [Google production cluster 2011 trace](https://research.google/blog/more-google-cluster-data/) | Anonymized machine availability/failure, workload requests and exits in a 29-day cluster trace. | Machine availability or re-addition does not prove strict loss and reacquisition of an identified end-user service goal. |

These differences matter. **A source may be suitable for an entirely different, scientifically legitimate study**: PNNL/ORNL for county outage-duration proxies, LANL for machine/node downtime, Backblaze for device failure risk and Google for machine availability/workload scheduling. An auxiliary outage proxy MUST NOT be silently relabeled as the original H1 strict restoration endpoint.

In the register, NOT_DEMONSTRATED means the public text did not prove the required field; this does NOT claim the complete real dataset lacks it. INCOMPATIBLE_UNIT means the publisher-described unit (county total, physical component, node) is not a tracked **individual service**. DOCUMENTED_FOR_RELEVANT_UNIT confirms only a documented subproperty, not scientific admission.

## What would be needed before any genuine empirical H1

1. Stable and safely pseudonymous physical **system and individual service identity**; external provenance and linked policy episode ID.
2. Pre-fault proof the goal was active, with timestamped raw capability/asset graph, stock, policy-visible observations and prediction made before the fault.
3. Fault identification and defensible event-to-that-service **causal loss** link; not mere time coincidence.
4. Documented **same service** regaining its goal along the same policy trajectory, or follow-up through a fixed deadline. Missing observation before the deadline is **censoring**, not a failure.
5. Timestamped real policy actions, no future-fault information leakage, physical event/asset identities and common causes, including aliasing.
6. Independent real system grouping, licensing/privacy permissions, time-zone and clock validation, follow-up/missingness, prospectively frozen samples and primary estimand.

No candidate had its raw observations examined at this stage. External domain experts must verify fault provenance, service linkage, event identities and policy history **independently**; matching a schema is necessary but not sufficient. A source file that labels itself OBSERVED is not automatically independently validated.

## Executable fail-closed R13 contract

[The R13 audit](../experiments/p1_r13_real_data_admission.py) checks the public metadata register and seven explicitly SYNTHETIC local episode controls. It distinguishes actual service loss from equipment faults without service loss; right-censoring from nonrestoration; late restoration from restoration by deadline; physically tracked service IDs from county totals; legitimate action joins from cross-system joins; pre-fault snapshots from leakage; and exposed fault pathways from undeclared aliases/common causes.

Even a complete synthetic episode with provisional binary strict-restoration label is **never admitted as independent physical H1 data**. There is intentionally NO acceptance path for real-data provenance in this release. All six real candidate sources remain BLOCKED_PUBLISHER_METADATA_ONLY. No raw data, hardware measurements, real episodes or private identifiers enter the repository.

To reproduce:

    python -m unittest tests.test_p1_r13_real_data_admission -v
    python -m experiments.p1_r13_real_data_admission --output r13_metadata_screen.json

[The R13 dedicated workflow](../.github/workflows/r13-real-data-admission.yml) uploads the reproducible screen and schema controls. After all tests pass, a stable exact numerical summary can be archived with a new rerun check. The original R8 null finding, R12 synthetic result and original P1 DRAFT_NOT_PREREGISTERED protocol remain unchanged.

## Recommended data acquisition, not yet carried out

An authorized real-world provider would need to supply a deidentified and securely joinable **service-level event evidence bundle**, including verified pre-fault active state, actual fault-caused loss, recovery or censoring, preevent topology/stock, policy action and observation histories, external physical event mapping and sampling keys. See the prepared [minimum provider evidence checklist](R13-physical-evidence-request-checklist.md). Avoid patient/customer personal identifiers, security-sensitive infrastructure details or proprietary incident disclosures without permission.

Without such evidence, the scientifically correct conclusion is **insufficient observational evidence for H1**, not an H1 null result or a proof of a new science. An independent paper on aggregate outages may be appropriate under a separately preregistered, weaker estimand, but cannot validate the originally stated same-service restoration hypothesis.

Keep Issues #3 and #8–#12 open.
