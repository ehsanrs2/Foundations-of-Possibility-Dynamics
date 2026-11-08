"""R15: archived raw node header, temporal ambiguity, and no fake job join."""
import json
from pathlib import Path
import unittest
from experiments.p1_r15_linkage_gate import (
    R14_ARCHIVE,REQUIRED_CONDITIONS,LANL_SOURCE_DOCUMENTS,
    raw_node_schema,evidence_status,temporal_candidate,demo,audit,
)

NODE={"system":"toy-s","node":"toy-n",
      "fault_start":"2026-11-08T08:00:00Z",
      "fault_end":"2026-11-08T08:15:00Z"}
JOB={"system":"toy-s","node":"toy-n","job_id":"toy-job-1",
     "run_start":"2026-11-08T07:58:00Z",
     "run_end":"2026-11-08T08:03:00Z"}


class R15JobLineageTests(unittest.TestCase):
    def test_observed_26_columns_have_no_actual_job_restart_ids(self):
        q=raw_node_schema()
        self.assertEqual(q["actual_csv_columns"],26)
        self.assertTrue(q["system_and_node_identifiers_present"])
        self.assertEqual(q["explicit_job_service_restart_policy_columns_present"],[])
        self.assertEqual(q["node_data_rows_inspected_in_R14"],23739)

    def test_original_lanl_authenticity_still_not_attested(self):
        self.assertFalse(raw_node_schema()["publisher_original_data_authenticated"])
        self.assertFalse(evidence_status()["direct_publisher_original_file_authenticated"])

    def test_two_officially_listed_usage_and_event_datasets_still_uninspected(self):
        r=evidence_status()["published_possible_complementary_sources"]
        self.assertEqual([x["publisher_listed_records"] for x in r],
                         [489376,433490])
        self.assertTrue(all(x["raw_rows_ingested_for_R15"]==0 for x in r))
        self.assertTrue(all(not x["stable_same_job_join_key_verified"] for x in r))

    def test_same_node_and_fault_time_yield_candidate_only(self):
        out=temporal_candidate(NODE,JOB)
        self.assertTrue(out["same_system_and_node"])
        self.assertTrue(out["overlapping_time_intervals"])
        self.assertTrue(out["temporal_candidate_only"])
        self.assertFalse(out["same_original_job_goal_reacquired"])
        self.assertFalse(out["admitted_as_real_h1_episode"])

    def test_different_job_same_node_can_be_an_equally_good_temporal_match(self):
        second={**JOB,"job_id":"unrelated-job-id"}
        a=temporal_candidate(NODE,JOB)
        b=temporal_candidate(NODE,second)
        self.assertEqual(a,b)
        self.assertFalse(a["physical_causal_service_loss_verified"])

    def test_nonoverlap_does_not_create_positive_join(self):
        later={**JOB,"run_start":"2026-11-08T09:00:00Z",
                     "run_end":"2026-11-08T09:10:00Z"}
        out=temporal_candidate(NODE,later)
        self.assertFalse(out["temporal_candidate_only"])

    def test_unequal_anonymized_system_or_node_does_not_join(self):
        for key in ("system","node"):
            modified={**JOB,key:"other"}
            self.assertFalse(temporal_candidate(NODE,modified)[
                "same_system_and_node"])

    def test_clock_timezone_required_for_real_data_join(self):
        without_offset={**JOB,"run_start":"2026-11-08T07:58:00"}
        with self.assertRaises(ValueError):
            temporal_candidate(NODE,without_offset)

    def test_reverse_or_invalid_intervals_refused(self):
        reversed_node={**NODE,"fault_start":"2026-11-08T08:30:00Z"}
        with self.assertRaises(ValueError):
            temporal_candidate(reversed_node,JOB)
        reversed_job={**JOB,"run_start":"2026-11-08T08:30:00Z"}
        with self.assertRaises(ValueError):
            temporal_candidate(NODE,reversed_job)

    def test_missing_required_join_keys_refused(self):
        for key in ("job_id","system","run_end"):
            less={k:v for k,v in JOB.items() if k!=key}
            with self.assertRaises(ValueError):
                temporal_candidate(NODE,less)

    def test_all_eleven_field_evidence_requirements_failing_closed(self):
        flags=evidence_status()["required_independently_verified_conditions"]
        self.assertEqual(len(flags),len(REQUIRED_CONDITIONS))
        self.assertTrue(all(v is False for v in flags.values()))
        self.assertFalse(evidence_status()["all_required_conditions_met"])

    def test_toy_multiple_jobs_one_node_is_ambiguous(self):
        item=demo()
        self.assertEqual(item["same_fault_node_candidate_job_runs"],2)
        self.assertEqual(item["verified_restarts"],0)
        self.assertEqual(item["valid_real_service_recovery_labels"],0)
        self.assertTrue(item["no_false_positive_h1_admission"])

    def test_h1_synthetic_sealed_policy_not_touched(self):
        output=audit()
        self.assertFalse(output["full_H1_evaluation_performed"])
        self.assertEqual(output["physical_service_restoration_labels"],0)
        self.assertTrue(output["R8_negative_result_preserved"])
        self.assertTrue(output["R14_mirror_sha256_and_row_count_preserved"])

    def test_exact_sources_are_documented_not_confused(self):
        self.assertEqual(len(LANL_SOURCE_DOCUMENTS),2)
        self.assertTrue(LANL_SOURCE_DOCUMENTS[0].startswith(
            "https://usrc.lanl.gov/"))
        self.assertEqual(LANL_SOURCE_DOCUMENTS[1],
                         "https://www.usenix.org/lanl-data")

    def test_versioned_R15_linkage_ledger_is_identical_to_audit(self):
        source=Path(__file__).resolve().parents[1]/"research"/(
            "R15-node-job-lineage-results-20261108.json")
        self.assertEqual(json.loads(source.read_text(encoding="utf-8")),audit())

    def test_r14_historical_archive_is_unaltered(self):
        data=json.loads(R14_ARCHIVE.read_text(encoding="utf-8"))
        self.assertEqual(data["raw_rows_inspected"],23739)
        self.assertEqual(data["compressed_sha256"],
                         "ed32fd254a013df79f5f475f4eac85980f7229735e100ac427343ef449a75140")
        self.assertEqual(data["strict_restoration_eligible_labels"],0)


if __name__=="__main__":
    unittest.main()
