"""R14 tests: real-file ingestion contract against SYNTHETIC XZ CSV fixtures."""
from __future__ import annotations

from contextlib import ExitStack
from hashlib import sha256
from pathlib import Path
import csv
import io
import lzma
import tempfile
import unittest

from experiments.p1_r14_lanl_raw_probe import (
    MIRROR_REPO,MIRROR_COMMIT,MIRROR_FILE,MIRROR_BLOB_SHA1,MIRROR_URL,
    SAMPLE_ROWS,audit_raw,
)

HEADER=[
    "System","machine type","number of nodes",
    "number of processors total","number of processors per node",
    "node number as it existed","node number starting with zero",
    "install date","production date","decommission date",
    "field replacable unit type","mememory","cpu type",
    "mememory type","number of interconnects","node purpose",
    "Problem Started","Problem Fixed","Down Time",
    "Facilities","Hardware","Human Error","Network",
    "Undetermined","Software","Same Event",
]


def row(*,system="2",node="0",started="6/21/2005 10:54",
        fixed="6/21/2005 11:00",downtime="6",cause="Graphics Accel Hdwr"):
    values=[""]*len(HEADER)
    values[0]=system
    values[1]="cluster"
    values[6]=node
    values[16]=started
    values[17]=fixed
    values[18]=downtime
    values[20]=cause
    values[25]="N"
    return values


class R14RawNodeIntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/"node-failure-data.csv.xz"

    def put(self, data,header=HEADER):
        text=io.StringIO(newline="")
        writer=csv.writer(text)
        writer.writerow(header)
        writer.writerows(data)
        packed=lzma.compress(text.getvalue().encode("utf-8"))
        self.path.write_bytes(packed)
        return sha256(packed).hexdigest()

    def test_locked_mirror_and_raw_file_attribution(self):
        self.assertEqual(MIRROR_REPO,"Derek-Jones/ESEUR-code-data")
        self.assertEqual(len(MIRROR_COMMIT),40)
        self.assertEqual(len(MIRROR_BLOB_SHA1),40)
        self.assertIn(MIRROR_COMMIT,MIRROR_URL)
        self.assertIn("failure-data-1996-2005.csv.xz",MIRROR_FILE)

    def test_valid_node_failure_rows_not_service_restoration(self):
        h=self.put([row(),row(system="3",node="8"),row(system="2",cause="")])
        result=audit_raw(self.path,expected_sha256=h)
        self.assertEqual(result["raw_rows_inspected"],3)
        self.assertEqual(result["sample_rows_evaluated"],3)
        self.assertEqual(result["sample_anonymized_system_groups"],2)
        self.assertEqual(result["sample_parseable_start_and_fix_times"],3)
        self.assertEqual(result["sample_rows_with_cause_category"],2)
        self.assertEqual(result["schema_column_count"],len(HEADER))
        self.assertFalse(result["verified_same_service_reacquisition"])
        self.assertEqual(result["strict_restoration_eligible_labels"],0)
        self.assertFalse(result["H1_confirmatory_result"])

    def test_raw_file_sha256_pin_is_cryptographically_checked(self):
        digest=self.put([row()])
        self.assertEqual(audit_raw(self.path,expected_sha256=digest)["compressed_sha256"],
                         digest)
        with self.assertRaisesRegex(ValueError,"sha256 mismatch"):
            audit_raw(self.path,expected_sha256="0"*64)
        with self.assertRaisesRegex(ValueError,"lowercase hex"):
            audit_raw(self.path,expected_sha256="not-a-sha256")

    def test_sample_first_n_only_but_count_entire_raw_source(self):
        self.put([row(system=str(i)) for i in range(22)])
        result=audit_raw(self.path,sample_rows=5)
        self.assertEqual(result["raw_rows_inspected"],22)
        self.assertEqual(result["sample_rows_evaluated"],5)
        self.assertEqual(result["sample_anonymized_system_groups"],5)
        self.assertEqual(result["dataset_scale"],"RAW_MIRROR_NODE_FAILURE_RECORDS")

    def test_missing_timestamps_are_not_fabricated(self):
        self.put([row(started=""),row(fixed=""),row()])
        out=audit_raw(self.path)
        self.assertEqual(out["sample_time_missing"],2)
        self.assertEqual(out["sample_parseable_start_and_fix_times"],1)

    def test_nonparseable_time_is_not_truthful_external_label(self):
        self.put([row(started="2026-11-01"),row()])
        out=audit_raw(self.path)
        self.assertEqual(out["sample_time_unparseable"],1)
        self.assertEqual(out["strict_restoration_eligible_labels"],0)

    def test_reverse_event_order_detected_not_fixed(self):
        self.put([row(started="6/21/2005 11:54",fixed="6/21/2005 11:00")])
        self.assertEqual(audit_raw(self.path)["sample_fixed_before_start"],1)

    def test_root_cause_missing_is_reported_not_invented(self):
        self.put([row(cause="")])
        result=audit_raw(self.path)
        self.assertEqual(result["sample_rows_with_cause_category"],0)

    def test_missing_problem_fixed_column_blocks(self):
        header=[x for x in HEADER if x!="Problem Fixed"]
        self.put([row()[:-1]],header=header)
        with self.assertRaisesRegex(ValueError,"Problem Fixed"):
            audit_raw(self.path)

    def test_duplicate_critical_column_blocks(self):
        self.put([row()+["now"]],header=HEADER+["Problem Started"])
        with self.assertRaisesRegex(ValueError,"duplicated"):
            audit_raw(self.path)

    def test_malformed_width_row_is_counted_not_interpreted(self):
        self.put([row(),row()[:-3]])
        out=audit_raw(self.path)
        self.assertEqual(out["raw_rows_inspected"],2)
        self.assertEqual(out["malformed_width_rows"],1)
        self.assertEqual(out["sample_rows_evaluated"],1)

    def test_missing_file_rejected(self):
        with self.assertRaises(FileNotFoundError):
            audit_raw(self.path)

    def test_invalid_sample_sizes_rejected(self):
        self.put([row()])
        for n in (0,1025,-1,True,1.0):
            with self.subTest(n=n),self.assertRaises(ValueError):
                audit_raw(self.path,sample_rows=n)

    def test_invalid_compression_fails_closed(self):
        self.path.write_bytes(b"not a compressed LANL CSV")
        with self.assertRaises(lzma.LZMAError):
            audit_raw(self.path)

    def test_no_data_row_fails_closed(self):
        self.put([])
        with self.assertRaisesRegex(ValueError,"no raw data"):
            audit_raw(self.path)

    def test_metadata_never_certifies_independent_lanl_original(self):
        self.put([row()])
        result=audit_raw(self.path)
        self.assertFalse(result["independently_authenticated_against_original_LANL_bytes"])
        self.assertFalse(result["publisher_raw_file_directly_retrieved"])
        self.assertEqual(result["independent_real_physical_systems_admitted_for_H1"],0)
        self.assertEqual(result["admission"],
                         "BLOCKED_PHYSICAL_SERVICE_TRAJECTORY_AND_ORIGINAL_PROVENANCE")

    def test_earlier_H1_draft_and_R8_negative_archive_preserved(self):
        base=Path(__file__).resolve().parents[1]
        prior=__import__("json").loads(
            (base/"research"/"R8-development-summary-seed20261101.json").read_text())
        h1=__import__("json").loads(
            (base/"research"/"p1_h1_design_candidate_v0_1.json").read_text())
        self.assertEqual(prior["mean_paired_improvement_baseline_minus_augmented"],0)
        self.assertEqual(h1["status"],"DRAFT_NOT_PREREGISTERED")


if __name__=="__main__":
    unittest.main()
