"""R13 field-evidence fail-closed intake and public-source metadata audit."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from datetime import datetime
import json
import unittest

from experiments.p1_r13_real_data_admission import (
    MANIFEST,REQUIRED,STATUS,_time,
    screen_sources,check_episode_contract,demo_episode,
    diagnostic_controls,audit,
)


class R13EvidenceAdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.result=audit()

    def test_all_six_citable_source_candidates_exist(self):
        data=self.manifest
        self.assertEqual(data["gate"],"R13")
        self.assertEqual(data["raw_files_retrieved"],0)
        self.assertEqual(data["raw_observational_rows_inspected"],0)
        self.assertEqual(len(data["candidates"]),6)
        for x in data["candidates"]:
            self.assertTrue(x["source_url"].startswith("https://"))
            self.assertTrue(x["dataset_url"].startswith("https://"))
            self.assertGreater(len(x["publisher_described_evidence"]),25)

    def test_public_description_does_not_grant_h1_qualification(self):
        result=screen_sources(self.manifest)
        self.assertEqual(result["source_candidates_screened"],6)
        self.assertEqual(result["sources_admitted_for_strict_restoration"],0)
        self.assertEqual(result["verified_raw_source_rows"],0)
        self.assertEqual(result["independent_physical_systems_admitted"],0)
        self.assertTrue(all(x["strict_h1_episode_admission"]==
                            "BLOCKED_PUBLISHER_METADATA_ONLY"
                            for x in result["source_screens"]))

    def test_unverified_not_misreported_as_absent(self):
        self.assertIn("NOT_DEMONSTRATED",STATUS)
        for record in self.manifest["candidates"]:
            self.assertIn("NOT_DEMONSTRATED",record["criteria"].values())
            self.assertEqual(record["raw_records_read"],0)
            self.assertFalse(record["qualified_for_h1"])

    def test_county_aggregate_is_not_a_single_service_identity(self):
        for id in ("pnnl_event_correlated_outages","ornl_eagle_i_2025"):
            item=next(x for x in self.manifest["candidates"] if x["source_id"]==id)
            self.assertEqual(item["criteria"]["stable_physical_service_identity"],
                             "INCOMPATIBLE_UNIT")

    def test_device_failure_does_not_imply_same_service_restoration(self):
        for id in ("backblaze_drive_stats","lanl_usrc_hpc_failures"):
            item=next(x for x in self.manifest["candidates"] if x["source_id"]==id)
            self.assertEqual(item["criteria"]["same_service_recovery_on_trajectory"],
                             "NOT_DEMONSTRATED")

    def test_metadata_claims_must_not_exceed_review_scope(self):
        bad=deepcopy(self.manifest)
        bad["candidates"][0]["qualified_for_h1"]=True
        with self.assertRaises(ValueError):
            screen_sources(bad)
        bad=deepcopy(self.manifest)
        bad["candidates"][0]["raw_file_verified"]=True
        with self.assertRaises(ValueError):
            screen_sources(bad)
        bad=deepcopy(self.manifest)
        bad["metadata_only"]=False
        with self.assertRaises(ValueError):
            screen_sources(bad)

    def test_cannot_drop_or_fabricate_admission_fields(self):
        bad=deepcopy(self.manifest)
        del bad["candidates"][0]["criteria"]["same_service_recovery_on_trajectory"]
        with self.assertRaises(ValueError):
            screen_sources(bad)
        bad=deepcopy(self.manifest)
        bad["candidates"][1]["criteria"]["policy_actions_and_observation_history"]="CONFIRMED_BY_ME"
        with self.assertRaises(ValueError):
            screen_sources(bad)

    def test_good_synthetic_control_is_only_provisional(self):
        q=check_episode_contract(demo_episode())
        self.assertEqual(q["contract_status"],
                         "PROVISIONAL_SCHEMA_COMPLETE_NOT_VERIFIED_PHYSICAL")
        self.assertEqual(q["provisional_strict_restoration_label"],1)
        self.assertFalse(q["independently_verified_real_provenance"])
        self.assertFalse(q["admitted_as_confirmatory_h1"])

    def test_claimed_observed_origin_still_not_admitted(self):
        q=demo_episode()
        q["origin"]="OBSERVED_BUT_UNVERIFIED"
        record=check_episode_contract(q)
        self.assertEqual(record["provisional_strict_restoration_label"],1)
        self.assertFalse(record["admitted_as_confirmatory_h1"])

    def test_observed_at_deadline_no_recovery_is_zero(self):
        row=demo_episode()
        row["regained_at"]=None
        row["service_regained_on_same_trajectory"]=False
        answer=check_episode_contract(row)
        self.assertEqual(answer["provisional_strict_restoration_label"],0)

    def test_no_followup_to_deadline_is_censored_not_failure(self):
        row=demo_episode()
        row["regained_at"]=None
        row["service_regained_on_same_trajectory"]=False
        row["followup_until"]="2026-11-01T08:35:00+00:00"
        result=check_episode_contract(row)
        self.assertEqual(result["contract_status"],"CENSORED_BEFORE_DEADLINE")
        self.assertIsNone(result["provisional_strict_restoration_label"])

    def test_late_restoration_after_deadline_is_failure(self):
        row=demo_episode()
        row["regained_at"]="2026-11-01T09:30:00+00:00"
        res=check_episode_contract(row)
        self.assertEqual(res["provisional_strict_restoration_label"],0)

    def test_hardware_failure_with_no_goal_loss_is_ineligible(self):
        row=demo_episode()
        row["service_held_after_fault"]=True
        row["regained_at"]=None
        row["service_regained_on_same_trajectory"]=False
        q=check_episode_contract(row)
        self.assertEqual(q["contract_status"],"INELIGIBLE_NO_ACTUAL_SERVICE_LOSS")
        self.assertIsNone(q["provisional_strict_restoration_label"])

    def test_not_active_before_fault_is_ineligible(self):
        row=demo_episode()
        row["service_held_before"]=False
        q=check_episode_contract(row)
        self.assertEqual(q["contract_status"],"INELIGIBLE_NO_ACTUAL_SERVICE_LOSS")
        self.assertIsNone(q["provisional_strict_restoration_label"])

    def test_aggregate_count_never_becomes_single_service(self):
        row=demo_episode()
        row["observation_unit"]="COUNTY_OUTAGE_COUNT"
        q=check_episode_contract(row)
        self.assertEqual(q["contract_status"],"BLOCKED_INVALID_EPISODE")
        self.assertIn("UNIT_NOT_TRACKED_SINGLE_SERVICE",q["errors"])

    def test_prediction_snapshot_cannot_come_from_after_fault(self):
        row=demo_episode()
        row["snapshot_at"]="2026-11-01T08:25:00+00:00"
        q=check_episode_contract(row)
        self.assertIn("INCONSISTENT_EVENT_ORDER",q["errors"])
        self.assertIsNone(q["provisional_strict_restoration_label"])

    def test_right_censoring_and_ordering_guard_against_impossible_times(self):
        row=demo_episode()
        row["followup_until"]="2026-11-01T08:21:00+00:00"
        self.assertIn("RESTORATION_OUTSIDE_OBSERVED_WINDOW",
                      check_episode_contract(row)["errors"])
        row=demo_episode()
        row["deadline_at"]="2026-11-01T08:02:00+00:00"
        self.assertIn("INVALID_DEADLINE",check_episode_contract(row)["errors"])

    def test_invalid_and_naive_timestamps_are_refused(self):
        row=demo_episode()
        row["fault_at"]="2026-11-01T08:10:00"
        self.assertIn("INVALID_TZ_TIME:fault_at",
                      check_episode_contract(row)["errors"])
        with self.assertRaises(ValueError):
            _time("2026-11-01T08:10:00")
        with self.assertRaises(ValueError):
            _time("not a time")

    def test_action_links_must_reference_same_system_service_and_policy(self):
        row=demo_episode()
        row["action_log"][0]["service_id"]="different-physical-service"
        self.assertIn("CROSS_SYSTEM_OR_POLICY_TRAJECTORY_JOIN",
                      check_episode_contract(row)["errors"])
        row=demo_episode()
        row["action_log"][0]["policy_id"]="different-policy"
        self.assertIn("POLICY_VERSION_MISMATCH",
                      check_episode_contract(row)["errors"])

    def test_action_timeline_does_not_use_future_information(self):
        row=demo_episode()
        row["action_log"][0]["at"]="2026-11-01T07:59:00+00:00"
        self.assertIn("ACTION_OUTSIDE_OBSERVED_EPISODE",
                      check_episode_contract(row)["errors"])

    def test_explicit_ontology_and_resource_inventory_required(self):
        row=demo_episode()
        row["physical_pathways"][0]["fault_event_ids"]=[]
        self.assertIn("UNSCOPED_PHYSICAL_FAULT_PATHS",
                      check_episode_contract(row)["errors"])
        row=demo_episode()
        row["pre_fault_inventory"]["kit"]=-1
        self.assertIn("INVALID_PREFAULT_RESOURCES",
                      check_episode_contract(row)["errors"])

    def test_missing_fields_cannot_silently_default_to_success(self):
        for key in ("regained_at","causal_link_evidence_id",
                    "physical_pathways","followup_until","action_log"):
            row=demo_episode()
            del row[key]
            result=check_episode_contract(row)
            self.assertEqual(result["contract_status"],"BLOCKED_MISSING_REQUIRED")
            self.assertIsNone(result["provisional_strict_restoration_label"])

    def test_no_implicit_boolean_truthy_acceptance(self):
        row=demo_episode()
        row["service_held_before"]=1
        self.assertIn("NON_BOOLEAN:service_held_before",
                      check_episode_contract(row)["errors"])

    def test_synthetic_controls_include_explicit_censoring_and_no_loss(self):
        controls=diagnostic_controls()
        self.assertEqual(controls["demo_cases"],7)
        self.assertEqual(controls["true_physical_observations"],0)
        self.assertEqual(controls["provisional_binary_demo_labels"],2)
        self.assertFalse(any(x["admitted_as_confirmatory_h1"]
                             for x in controls["demo_outcomes"].values()))

    def test_R13_does_not_modify_R8_negative_archive_or_H1_status(self):
        p=Path(__file__).parents[1]
        old=json.loads((p/"research/R8-development-summary-seed20261101.json").
                       read_text(encoding="utf-8"))
        h1=json.loads((p/"research/p1_h1_design_candidate_v0_1.json").
                      read_text(encoding="utf-8"))
        self.assertTrue(old["r1_non_discriminating"])
        self.assertEqual(old["mean_paired_improvement_baseline_minus_augmented"],0)
        self.assertEqual(h1["status"],"DRAFT_NOT_PREREGISTERED")

    def test_external_data_admission_is_explicitly_zero(self):
        self.assertEqual(self.result["real_raw_observational_rows_ingested"],0)
        self.assertEqual(self.result["actual_strict_restoration_labels_verified"],0)
        self.assertEqual(self.result["independent_physical_systems_admitted"],0)
        self.assertFalse(self.result["H1_preregistered"])
        self.assertEqual(self.result["sealed_test_families_instantiated"],0)
        self.assertEqual(self.result["result"],"PASS")


if __name__=="__main__":
    unittest.main()
