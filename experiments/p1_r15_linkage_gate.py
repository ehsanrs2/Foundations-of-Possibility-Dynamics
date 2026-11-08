"""R15: raw LANL fault header vs service/job recovery join-admission checks.

The only actually inspected operational raw data here are R14's 26 LANL
node-failure CSV columns. The publisher lists separate system-20 usage and
event archives, but their raw rows and ID semantics are not yet audited.

Temporal overlaps or shared system/node numbers cannot prove job identity,
same-job restart, causality, policy action history or restored goal. This
module is fail-closed: even well-formed SYNTHETIC examples are NOT genuine
independently authenticated physical episodes for H1.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime,timezone
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[1]
R14_ARCHIVE=ROOT/"research"/"R14-lanl-mirror-raw-audit-20261108.json"

REQUIRED_CONDITIONS=(
    "primary_publisher_raw_failure_file_authenticated",
    "usage_and_event_raw_sources_authentic",
    "documented_same_machine_and_clock_mapping",
    "stable_original_job_identity",
    "validated_job_restart_lineage_after_failure",
    "pre_fault_job_working_goal_observed",
    "fault_caused_original_job_goal_loss",
    "same_job_goal_reacquired_on_original_policy_history",
    "recovery_actions_with_nonanticipative_policy_and_resources",
    "verified_physical_event_and_common_cause_mapping",
    "right_censoring_and_independent_system_units",
)
LANL_SOURCE_DOCUMENTS=(
    "https://usrc.lanl.gov/data/failure-data.php",
    "https://www.usenix.org/lanl-data",
)
PRIMARY_ORIGINAL_WITH_DIRECT_BYTE_ATTESTATION=False


def raw_node_schema() -> dict:
    """R14 observed actual CSV columns, NOT LANL-original authenticated bytes."""
    data=json.loads(R14_ARCHIVE.read_text(encoding="utf-8"))
    if (data["gate"]!="R14" or data["schema_column_count"]!=26
        or data["independently_authenticated_against_original_LANL_bytes"]
        or data["strict_restoration_eligible_labels"]!=0):
        raise ValueError("R14 source/provenance invariant changed")
    columns=data["actual_csv_column_names"]
    normalize=lambda x:re.sub(r"[^a-z0-9]","",x.lower())
    names={normalize(name) for name in columns}
    identity_columns=("system","nodenumz")
    fault_start=("probstarted",)
    fault_fixed=("probfixed",)
    if not all(name in names for name in identity_columns+fault_start+fault_fixed):
        raise ValueError("R14 actual fault identity/timing fields changed")
    job_fields=("jobid","jobidentifier","runid","attemptid","serviceid",
                "checkpointid","policyid","repairactionid")
    return {
        "source":"REAL_LANL_NODE_FAULT_CSV_THIRD_PARTY_MIRROR",
        "actual_csv_columns":len(columns),
        "system_and_node_identifiers_present":True,
        "node_fault_start_and_admin_fix_times_present":True,
        "explicit_job_service_restart_policy_columns_present":
            sorted(x for x in job_fields if x in names),
        "publisher_original_data_authenticated":False,
        "node_data_rows_inspected_in_R14":data["raw_rows_inspected"],
        "independently_validated_h1_labels":0,
    }


def evidence_status() -> dict:
    node=raw_node_schema()
    verified={name:False for name in REQUIRED_CONDITIONS}
    # Here the only real observed object is an archive of NODE failures;
    # its temporal data cannot meet service goal requirements. Do not
    # combine separately described source files before their rows or keys
    # have been inspected and externally justified.
    return {
        "gate":"R15",
        "classification":"REAL_NODE_TRACE_TO_JOB_RESTART_PROVENANCE_BLOCKED_NOT_H1",
        "observed_raw_input":node,
        "published_possible_complementary_sources":[
            {"name":"LANL System 20 usage with node info",
             "publisher_page":LANL_SOURCE_DOCUMENTS[0],
             "publisher_listed_records":489376,
             "raw_rows_ingested_for_R15":0,
             "stable_same_job_join_key_verified":False},
            {"name":"LANL System 20 usage event info",
             "publisher_page":LANL_SOURCE_DOCUMENTS[0],
             "publisher_listed_records":433490,
             "raw_rows_ingested_for_R15":0,
             "stable_same_job_join_key_verified":False},
        ],
        "published_context_checkpoint_restart":LANL_SOURCE_DOCUMENTS[1],
        "required_independently_verified_conditions":verified,
        "all_required_conditions_met":all(verified.values()),
        "direct_publisher_original_file_authenticated":False,
        "candidate_time_overlap_is_causal_join":False,
        "actual_service_episodes_admitted":0,
        "new_confirmatory_h1_samples":0,
        "sealed_H1_families_touched":0,
    }


def _as_utc(timestamp: str) -> datetime:
    if not isinstance(timestamp,str):
        raise ValueError("timestamp must be ISO string with timezone")
    parsed=datetime.fromisoformat(timestamp.replace("Z","+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timestamp timezone required")
    return parsed.astimezone(timezone.utc)


def temporal_candidate(node: dict,job: dict) -> dict:
    """A debugging *candidate overlap*, NEVER an evidence-validated H1 join."""
    for rec,fields in ((node,("system","node","fault_start","fault_end")),
                       (job,("system","node","job_id","run_start","run_end"))):
        if not isinstance(rec,dict) or any(f not in rec for f in fields):
            raise ValueError("incomplete synthetic join candidate record")
    start,end=(_as_utc(node["fault_start"]),_as_utc(node["fault_end"]))
    a,b=(_as_utc(job["run_start"]),_as_utc(job["run_end"]))
    if end<start or b<a:
        raise ValueError("invalid interval ordering")
    same_machine=(node["system"]==job["system"] and
                  node["node"]==job["node"])
    intervals_overlap=start<=b and a<=end
    return {
        "same_system_and_node":same_machine,
        "overlapping_time_intervals":intervals_overlap,
        "temporal_candidate_only":same_machine and intervals_overlap,
        "job_restarted_and_restored_proven":False,
        "same_original_job_goal_reacquired":False,
        "physical_causal_service_loss_verified":False,
        "admitted_as_real_h1_episode":False,
    }


def demo() -> dict:
    """Purely synthetic collision examples; no user data or raw node IDs."""
    node={
        "system":"toy-machine-system-1","node":"toy-node-2",
        "fault_start":"2026-11-08T08:00:00+00:00",
        "fault_end":"2026-11-08T08:15:00+00:00",
    }
    jobs=[
        {"system":node["system"],"node":node["node"],
         "job_id":"toy-job-A","run_start":"2026-11-08T07:58:00+00:00",
         "run_end":"2026-11-08T08:05:00+00:00"},
        {"system":node["system"],"node":node["node"],
         "job_id":"toy-job-B","run_start":"2026-11-08T07:59:00+00:00",
         "run_end":"2026-11-08T08:09:00+00:00"},
    ]
    overlaps=[temporal_candidate(node,j) for j in jobs]
    if not all(o["temporal_candidate_only"] and
               not o["admitted_as_real_h1_episode"] for o in overlaps):
        raise AssertionError("toy node collision guard failed")
    return {
        "origin":"SYNTHETIC_COLLISION_EXAMPLE",
        "same_fault_node_candidate_job_runs":len(overlaps),
        "unresolved_original_job_identity_collisions":2,
        "verified_restarts":0,
        "valid_real_service_recovery_labels":0,
        "no_false_positive_h1_admission":True,
        "cases":overlaps,
    }


def audit() -> dict:
    status=evidence_status()
    return {
        "gate":"R15",
        "status":"NO_EMPIRICAL_JOB_TO_NODE_RESTORATION_JOIN_VERIFIED",
        "original_failure_file_authentication":"BLOCKED_LANL_DIRECT_RETRIEVAL_NOT_VERIFIED",
        "source_join_evidence":status,
        "synthetic_join_collision_controls":demo(),
        "physical_service_restoration_labels":0,
        "full_H1_evaluation_performed":False,
        "R8_negative_result_preserved":True,
        "R14_mirror_sha256_and_row_count_preserved":True,
        "result":"PASS_EVIDENCE_GATE_REMAINS_BLOCKED",
    }


def main() -> None:
    print(json.dumps(audit(),sort_keys=True,indent=2))


if __name__=="__main__":
    main()
