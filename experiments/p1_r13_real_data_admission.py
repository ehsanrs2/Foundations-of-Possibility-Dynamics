"""R13: fail-closed intake for real-world strict-restoration evidence.

The public sources are reviewed from PUBLISHER DESCRIPTIONS ONLY; no raw
observational record has been ingested. An equipment failure, county outage
count, incident end or node-up event is NOT automatically loss and recovery
of the same service under one observed nonanticipative policy.

All example episodes below are explicitly SYNTHETIC and only test the
REQUIRED input contract. Passing a structural schema is NOT physical
provenance verification, prospective registration or H1 validation.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import argparse
import copy
import json
import re

HERE = Path(__file__).resolve().parents[1]
MANIFEST = HERE / "research" / "R13-public-source-admission-manifest.json"
STATUS = frozenset(("DOCUMENTED_FOR_RELEVANT_UNIT",
                    "NOT_DEMONSTRATED", "INCOMPATIBLE_UNIT"))
REQUIRED = (
    "source_id","source_record_uri","source_record_sha256",
    "origin","observation_unit","physical_system_id","service_id",
    "episode_id","trajectory_id","risk_sample_group_id",
    "snapshot_at","prediction_at","fault_at","post_fault_at",
    "deadline_at","followup_until","regained_at",
    "service_held_before","service_held_after_fault",
    "service_regained_on_same_trajectory","causal_link_evidence_id",
    "observed_policy_id","observation_log_complete","action_log_complete",
    "action_log","pre_fault_capability_snapshot","pre_fault_inventory",
    "declared_action_rules","physical_pathways","ontology_evidence_uri",
)
TIMES = ("snapshot_at","prediction_at","fault_at","post_fault_at",
         "deadline_at","followup_until")


def _time(x: str) -> datetime:
    if not isinstance(x,str) or not x:
        raise ValueError("required explicit timezone-aware ISO timestamp")
    parsed=datetime.fromisoformat(x.replace("Z","+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("naive timestamp is forbidden")
    return parsed.astimezone(timezone.utc)


def screen_sources(manifest: dict) -> dict:
    """Only a metadata admission screen, never row certification."""
    criteria=manifest["admission_criteria"]
    candidates=manifest["candidates"]
    if len(set(criteria))!=len(criteria) or len(criteria)<10:
        raise ValueError("incomplete strict-restoration admission criterion set")
    if len({s["source_id"] for s in candidates})!=len(candidates):
        raise ValueError("duplicate public source key")
    if not manifest["metadata_only"] or manifest["raw_observational_rows_inspected"]!=0:
        raise ValueError("this R13 revision is intentionally METADATA ONLY")
    rows=[]
    for source in candidates:
        if set(source["criteria"])!=set(criteria):
            raise ValueError(("incomplete source criterion checklist",source["source_id"]))
        if any(s not in STATUS for s in source["criteria"].values()):
            raise ValueError("invalid source evidence status")
        if source["raw_file_verified"] or source["raw_records_read"]!=0:
            raise ValueError("raw provenance asserted without a raw-file intake pipeline")
        if source["qualified_for_h1"]:
            raise ValueError("cannot certify H1 from description-level material")
        if (not source["source_url"].startswith("https://") or
            not source["dataset_url"].startswith("https://")):
            raise ValueError("citable publisher source URL required")
        counts={key:sum(v==key for v in source["criteria"].values())
                for key in sorted(STATUS)}
        rows.append({
            "source_id":source["source_id"],
            "documented_criteria":counts["DOCUMENTED_FOR_RELEVANT_UNIT"],
            "not_demonstrated":counts["NOT_DEMONSTRATED"],
            "incompatible_unit":counts["INCOMPATIBLE_UNIT"],
            "raw_rows_verified":0,
            "strict_h1_episode_admission":"BLOCKED_PUBLISHER_METADATA_ONLY",
            "potential_auxiliary_use":source["auxiliary_purpose_only"],
            "critical_gap":source["critical_strict_restoration_gap"],
        })
    return {
        "gate":"R13",
        "status":"SOURCE_DISCOVERY_NOT_H1_VALIDATION",
        "source_candidates_screened":len(rows),
        "source_ids":[r["source_id"] for r in rows],
        "verified_raw_source_rows":0,
        "independent_physical_systems_admitted":0,
        "sources_admitted_for_strict_restoration":0,
        "source_screens":rows,
    }


def _result(status: str, errors: list[str], label=None) -> dict:
    """Never infer real-data admission from user-supplied or toy field values."""
    return {
        "contract_status":status,
        "provisional_strict_restoration_label":label,
        "errors":sorted(set(errors)),
        "independently_verified_real_provenance":False,
        "admitted_as_confirmatory_h1":False,
    }


def check_episode_contract(row: dict) -> dict:
    """Timestamp/identity/causality-risk checks for a *provisional* episode.

    Syntactically complete and internally plausible is NEVER equivalent to a
    trusted observation. This module intentionally has NO path that accepts
    a row as independently verified real-world H1 evidence.
    """
    if not isinstance(row,dict):
        return _result("INVALID_RECORD",["NOT_A_DICT"])
    missing=sorted(set(REQUIRED)-set(row))
    if missing:
        return _result("BLOCKED_MISSING_REQUIRED",["MISSING:"+x for x in missing])
    errors=[]
    for field in ("source_id","source_record_uri","origin","physical_system_id",
                  "service_id","episode_id","trajectory_id",
                  "risk_sample_group_id","causal_link_evidence_id",
                  "observed_policy_id","ontology_evidence_uri"):
        if not isinstance(row[field],str) or not row[field].strip():
            errors.append("EMPTY_ID:"+field)
    if row["observation_unit"]!="SINGLE_PHYSICAL_SERVICE":
        errors.append("UNIT_NOT_TRACKED_SINGLE_SERVICE")
    if not re.fullmatch(r"[0-9a-fA-F]{64}",str(row["source_record_sha256"])):
        errors.append("SOURCE_SHA256_NOT_DOCUMENTED")
    when={}
    for field in TIMES:
        try:
            when[field]=_time(row[field])
        except (TypeError,ValueError,OverflowError):
            errors.append("INVALID_TZ_TIME:"+field)
    regained=None
    if row["regained_at"] is not None:
        try:
            regained=_time(row["regained_at"])
        except (TypeError,ValueError,OverflowError):
            errors.append("INVALID_TZ_TIME:regained_at")
    if len(when)==len(TIMES):
        if not (when["snapshot_at"]<=when["prediction_at"]<
                when["fault_at"]<when["post_fault_at"]<=
                when["followup_until"]):
            errors.append("INCONSISTENT_EVENT_ORDER")
        if not when["fault_at"]<when["deadline_at"]:
            errors.append("INVALID_DEADLINE")
        if regained is not None and not (
            when["post_fault_at"]<=regained<=when["followup_until"]):
            errors.append("RESTORATION_OUTSIDE_OBSERVED_WINDOW")
    for field in ("service_held_before","service_held_after_fault",
                  "service_regained_on_same_trajectory",
                  "observation_log_complete","action_log_complete"):
        if type(row[field]) is not bool:
            errors.append("NON_BOOLEAN:"+field)
    if row["observation_log_complete"] is not True or (
        row["action_log_complete"] is not True):
        errors.append("INCOMPLETE_POLICY_OR_OBSERVATION_HISTORY")
    if not isinstance(row["pre_fault_capability_snapshot"],list) or (
        not row["pre_fault_capability_snapshot"]):
        errors.append("MISSING_PREFAULT_CAPABILITIES")
    if not isinstance(row["pre_fault_inventory"],dict) or (
        not row["pre_fault_inventory"]) or any(
            not isinstance(qty,int) or isinstance(qty,bool) or qty<0
            for qty in row["pre_fault_inventory"].values()):
        errors.append("INVALID_PREFAULT_RESOURCES")
    if not isinstance(row["declared_action_rules"],list) or (
        not row["declared_action_rules"]):
        errors.append("MISSING_ACTION_GRAPH")
    paths=row["physical_pathways"]
    if (not isinstance(paths,list) or len(paths)<2 or
        any(not isinstance(p,dict) or
            not isinstance(p.get("mechanism_id"),str) or
            not p.get("mechanism_id") or
            not isinstance(p.get("fault_event_ids"),list) or
            not p.get("fault_event_ids") or
            any(not isinstance(e,str) or not e for e in p["fault_event_ids"])
            for p in paths)):
        errors.append("UNSCOPED_PHYSICAL_FAULT_PATHS")
    actions=row["action_log"]
    if not isinstance(actions,list):
        errors.append("MISSING_ACTION_LOG")
    else:
        action_times=[]
        for action in actions:
            if not isinstance(action,dict):
                errors.append("INVALID_ACTION_RECORD")
                continue
            if any(action.get(name)!=row[name] for name in (
                "physical_system_id","service_id","trajectory_id")):
                errors.append("CROSS_SYSTEM_OR_POLICY_TRAJECTORY_JOIN")
            if action.get("policy_id")!=row["observed_policy_id"]:
                errors.append("POLICY_VERSION_MISMATCH")
            if not isinstance(action.get("action_name"),str) or not action["action_name"]:
                errors.append("MISSING_ACTION_ID")
            try:
                t=_time(action["at"])
                action_times.append(t)
                if len(when)==len(TIMES) and not (
                    when["prediction_at"]<=t<=when["followup_until"]):
                    errors.append("ACTION_OUTSIDE_OBSERVED_EPISODE")
            except (KeyError,TypeError,ValueError,OverflowError):
                errors.append("INVALID_ACTION_TIMESTAMP")
        if action_times!=sorted(action_times):
            errors.append("OUT_OF_ORDER_ACTIONS")
    if regained is None and row["service_regained_on_same_trajectory"] is True:
        errors.append("RECOVERY_FLAG_WITHOUT_RESTORATION")
    if regained is not None and row["service_regained_on_same_trajectory"] is False:
        errors.append("RESTORATION_WITHOUT_SAME_TRAJECTORY")
    if errors:
        return _result("BLOCKED_INVALID_EPISODE",errors)

    # Ineligible episodes are NEVER failures. A hardware incident with no
    # actual service loss is excluded even if repaired later.
    if row["service_held_before"] is not True or (
        row["service_held_after_fault"] is not False):
        return _result("INELIGIBLE_NO_ACTUAL_SERVICE_LOSS",[],None)
    if regained is None:
        if when["followup_until"]<when["deadline_at"]:
            return _result("CENSORED_BEFORE_DEADLINE",[],None)
        label=0
    else:
        label=int(regained<=when["deadline_at"])
    return _result("PROVISIONAL_SCHEMA_COMPLETE_NOT_VERIFIED_PHYSICAL",[],label)


def demo_episode() -> dict:
    """Pure synthetic positive control; never an actual observational row."""
    return {
        "source_id":"R13_SYNTHETIC_CONTRACT_ONLY",
        "source_record_uri":"synthetic://r13/ep1",
        "source_record_sha256":"d"*64,
        "origin":"SYNTHETIC_DEMONSTRATION",
        "observation_unit":"SINGLE_PHYSICAL_SERVICE",
        "physical_system_id":"toy-unit-1",
        "service_id":"toy-service-1",
        "episode_id":"toy-episode-1",
        "trajectory_id":"toy-trajectory-1",
        "risk_sample_group_id":"toy-system-1",
        "snapshot_at":"2026-11-01T08:00:00+00:00",
        "prediction_at":"2026-11-01T08:05:00+00:00",
        "fault_at":"2026-11-01T08:10:00+00:00",
        "post_fault_at":"2026-11-01T08:11:00+00:00",
        "deadline_at":"2026-11-01T09:10:00+00:00",
        "followup_until":"2026-11-01T10:00:00+00:00",
        "regained_at":"2026-11-01T08:30:00+00:00",
        "service_held_before":True,
        "service_held_after_fault":False,
        "service_regained_on_same_trajectory":True,
        "causal_link_evidence_id":"toy-incident-link",
        "observed_policy_id":"toy-policy-v1",
        "observation_log_complete":True,
        "action_log_complete":True,
        "action_log":[{
            "at":"2026-11-01T08:20:00+00:00",
            "physical_system_id":"toy-unit-1","service_id":"toy-service-1",
            "trajectory_id":"toy-trajectory-1","policy_id":"toy-policy-v1",
            "action_name":"toy-restore"
        }],
        "pre_fault_capability_snapshot":["toy-service-1","channel-a"],
        "pre_fault_inventory":{"kit":1},
        "declared_action_rules":[{"name":"toy-restore",
                                  "requires":["channel-a"],"consumes":{"kit":1}}],
        "physical_pathways":[
            {"mechanism_id":"toy-physical-A","fault_event_ids":["toy-fault-A"]},
            {"mechanism_id":"toy-physical-B","fault_event_ids":["toy-fault-B"]}
        ],
        "ontology_evidence_uri":"synthetic://r13/toy-ontology",
    }


def diagnostic_controls() -> dict:
    demo=demo_episode()
    cases={
        "eligible_recovered":demo,
        "eligible_no_recovery_observed_to_deadline":{
            **demo,"regained_at":None,
            "service_regained_on_same_trajectory":False,
        },
        "censored_no_followup":{
            **demo,"regained_at":None,
            "service_regained_on_same_trajectory":False,
            "followup_until":"2026-11-01T08:35:00+00:00",
        },
        "device_failure_without_service_loss":{
            **demo,"service_held_after_fault":True,
            "regained_at":None,
            "service_regained_on_same_trajectory":False,
        },
        "aggregate_count_not_unit":{
            **demo,"observation_unit":"COUNTY_AGGREGATE_CUSTOMER_COUNT",
        },
        "postfault_feature_leak":{
            **demo,"snapshot_at":"2026-11-01T08:25:00+00:00",
        },
        "different_service_trajectory":{
            **demo,"action_log":[{**demo["action_log"][0],
                                   "service_id":"different-service"}],
        },
    }
    outputs={key:check_episode_contract(value) for key,value in cases.items()}
    expected={
        "eligible_recovered":("PROVISIONAL_SCHEMA_COMPLETE_NOT_VERIFIED_PHYSICAL",1),
        "eligible_no_recovery_observed_to_deadline":(
            "PROVISIONAL_SCHEMA_COMPLETE_NOT_VERIFIED_PHYSICAL",0),
        "censored_no_followup":("CENSORED_BEFORE_DEADLINE",None),
        "device_failure_without_service_loss":(
            "INELIGIBLE_NO_ACTUAL_SERVICE_LOSS",None),
        "aggregate_count_not_unit":("BLOCKED_INVALID_EPISODE",None),
        "postfault_feature_leak":("BLOCKED_INVALID_EPISODE",None),
        "different_service_trajectory":("BLOCKED_INVALID_EPISODE",None),
    }
    for name, pair in expected.items():
        got=outputs[name]
        if (got["contract_status"],got["provisional_strict_restoration_label"])!=pair:
            raise AssertionError(("intake negative control failed",name,got))
        if got["admitted_as_confirmatory_h1"]:
            raise AssertionError("no synthetic example can be admitted as H1")
    return {
        "examples_are_synthetic_not_real_samples":True,
        "demo_cases":len(outputs),
        "provisional_binary_demo_labels":2,
        "true_physical_observations":0,
        "demo_outcomes":outputs,
    }


def audit() -> dict:
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    screened=screen_sources(manifest)
    controls=diagnostic_controls()
    if screened["sources_admitted_for_strict_restoration"]!=0:
        raise AssertionError("metadata-only review cannot discover empirical H1 labels")
    return {
        "gate":"R13",
        "classification":"PUBLIC_DATA_PROVENANCE_SCREEN_NOT_H1",
        "public_source_review":screened,
        "schema_only_synthetic_controls":controls,
        "real_raw_observational_rows_ingested":0,
        "actual_strict_restoration_labels_verified":0,
        "independent_physical_systems_admitted":0,
        "full_raw_data_access_verified":False,
        "H1_preregistered":False,
        "sealed_test_families_instantiated":0,
        "R8_negative_archive_unchanged":True,
        "recommendation":"REQUIRE_INDEPENDENT_PHYSICAL_EPISODE_SOURCE_AND_ROW_LEVEL_PROVENANCE_BEFORE_H1",
        "result":"PASS",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    result=audit()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",
                               encoding="utf-8")
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=="__main__":
    main()
