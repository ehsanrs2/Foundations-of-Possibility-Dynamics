"""R14: bounded *real raw node-failure* file inspection; NOT H1 restoration data.

The upstream LANL project publicly releases an all-systems failure CSV.
This workflow downloads a locked GitHub MIRROR of that raw file, rather than
LANL's own original archive. The mirror cannot independently authenticate
the original bytes. A recorded mirror Git blob hash checks version integrity
only, not original-source truth. No customer or node IDs or row data are
committed: just aggregate schema/time-quality counts and source hashes.

'Problem Fixed' refers to an HPC node/admin fault record, NOT documented
restoration of the SAME individual service under one observable fixed policy.
Passing R14 never confers H1 admission, even if all 23k rows parse.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime
from hashlib import sha256
from pathlib import Path
import argparse
import csv
import json
import lzma
import re

MIRROR_REPO = "Derek-Jones/ESEUR-code-data"
MIRROR_COMMIT = "bc1d9e99da2a956cdecba9d9d7f6f9b61a371c5f"
MIRROR_FILE = "reliability/LA-UR-05-7318-failure-data-1996-2005.csv.xz"
MIRROR_BLOB_SHA1 = "1f3c115dd319a2cbabc02d312bb733c60e1ef29d"
MIRROR_URL = (
    "https://raw.githubusercontent.com/" + MIRROR_REPO + "/" +
    MIRROR_COMMIT + "/" + MIRROR_FILE
)
LANL_RELEASE = "https://usrc.lanl.gov/data/failure-data.php"
LANL_CITATION = "Los Alamos National Laboratory, Ultrascale Systems Research Center (USRC) Data Sources"
SAMPLE_ROWS = 256
MAX_ARCHIVE_BYTES = 1_048_576
MAX_UNCOMPRESSED_BYTES = 8_388_608
MAX_ROWS = 40_000
REQUIRED_FIELDS = (
    "System", "node number starting with zero", "Problem Started",
    "Problem Fixed", "Down Time", "Same Event",
)
# A few of these header strings may have slight spelling/space changes
# relative to the published LANL README; only the four critical columns
# below determine admission for a node failure time interval.
MINIMUM_FIELDS = ("System", "Problem Started", "Problem Fixed", "Down Time")


def normalized(s: str) -> str:
    return re.sub(r"[^a-z0-9]","",s.lower())


def header_index(header: list[str], name: str) -> int:
    # The original published README spells these Problem Started/Fixed.
    # Real legacy CSVs sometimes abbreviate the column to Prob Started/Fixed.
    # Only these two transparent, explicitly documented aliases are allowed.
    aliases={
        "Problem Started":{"problemstarted","probstarted"},
        "Problem Fixed":{"problemfixed","probfixed"},
    }
    accepted=aliases.get(name,{normalized(name)})
    matches=[i for i,h in enumerate(header) if normalized(h) in accepted]
    if len(matches)!=1:
        raise ValueError("required LANL node-failure field missing or duplicated: "+name)
    return matches[0]


def _time(value: str) -> datetime | None:
    if not value.strip():
        return None
    # The README states local/unspecified time; no timezone can be assumed.
    return datetime.strptime(value.strip(), "%m/%d/%Y %H:%M")


def _stream(path: Path):
    """Bounded XZ decompression with an explicit uncompressed byte ceiling."""
    total=0
    with lzma.open(path,"rb") as fh:
        for line in fh:
            total+=len(line)
            if total>MAX_UNCOMPRESSED_BYTES:
                raise ValueError("decompressed size ceiling exceeded")
            yield line.decode("utf-8-sig",errors="replace")


def audit_raw(path: Path, *, expected_sha256: str | None = None,
              sample_rows: int = SAMPLE_ROWS) -> dict:
    """Process actual mirror data, never invent real service-goal labels.

    Header names, count, timestamps and missingness are read from the file;
    none of those fields can stand in for service-level restoration.
    """
    if type(sample_rows) is not int or not 1<=sample_rows<=1024:
        raise ValueError("bounded deterministic sample size required")
    if not path.is_file():
        raise FileNotFoundError(str(path))
    size=path.stat().st_size
    if not 0<size<=MAX_ARCHIVE_BYTES:
        raise ValueError("compressed file outside explicit size bound")
    raw=path.read_bytes()
    digest=sha256(raw).hexdigest()
    if expected_sha256 is not None:
        if not re.fullmatch(r"[0-9a-f]{64}",expected_sha256):
            raise ValueError("expected raw archive sha256 must be lowercase hex")
        if expected_sha256!=digest:
            raise ValueError("raw mirror archive sha256 mismatch: fail closed")
    rows=csv.reader(_stream(path))
    try:
        header=next(rows)
    except StopIteration:
        raise ValueError("empty compressed CSV")
    names={key:header_index(header,key) for key in MINIMUM_FIELDS}
    idx_system=names["System"]
    idx_started=names["Problem Started"]
    idx_fixed=names["Problem Fixed"]
    idx_down=names["Down Time"]
    all_rows=0
    malformed_width=0
    sampled=0
    sampled_systems=set()
    sample_time_complete=0
    sample_time_unparseable=0
    sample_time_missing=0
    sample_negative_duration=0
    sample_with_downtime=0
    sample_nonempty_root_cause=0
    sample_blank_system=0
    causes=[j for j,h in enumerate(header)
            if normalized(h) in {"facilities","hardware","humanerror",
                                  "network","undetermined","software"}]
    for fields in rows:
        if not fields or not any(f.strip() for f in fields):
            continue
        all_rows+=1
        if all_rows>MAX_ROWS:
            raise ValueError("row-count guard exceeded")
        if len(fields)!=len(header):
            malformed_width+=1
            continue
        if sampled>=sample_rows:
            continue
        sampled+=1
        if fields[idx_system].strip():
            sampled_systems.add(fields[idx_system].strip())
        else:
            sample_blank_system+=1
        if fields[idx_down].strip():
            sample_with_downtime+=1
        if any(fields[j].strip() for j in causes):
            sample_nonempty_root_cause+=1
        if not fields[idx_started].strip() or not fields[idx_fixed].strip():
            sample_time_missing+=1
            continue
        try:
            started=_time(fields[idx_started])
            fixed=_time(fields[idx_fixed])
        except ValueError:
            sample_time_unparseable+=1
            continue
        sample_time_complete+=1
        if fixed<started:
            sample_negative_duration+=1
    physical_line_count=sum(1 for _ in _stream(path))
    if physical_line_count<all_rows+1:
        raise AssertionError("CSV line counting is internally inconsistent")
    if all_rows==0 or sampled==0:
        raise ValueError("no raw data rows")
    if all_rows<10:
        # Toy files are allowed in contract tests, but a real-source result
        # must not claim meaningful coverage from such a tiny file.
        dataset_scale="SMALL_CONTRACT_FIXTURE_OR_TRUNCATED"
    else:
        dataset_scale="RAW_MIRROR_NODE_FAILURE_RECORDS"
    # Never publish individual source system/node IDs, raw text or service IDs.
    return {
        "gate":"R14",
        "classification":"MIRROR_RAW_NODE_FAILURE_AUXILIARY_NOT_H1",
        "source":"LANL USRC all-system historical node failure/interrupt collection",
        "original_publisher_page":LANL_RELEASE,
        "source_attribution":LANL_CITATION,
        "retrieval_kind":"GIT_COMMIT_PINNED_THIRD_PARTY_MIRROR",
        "mirror_repository":MIRROR_REPO,
        "mirror_commit":MIRROR_COMMIT,
        "mirror_git_blob_sha1":MIRROR_BLOB_SHA1,
        "mirror_archive_url":MIRROR_URL,
        "compressed_sha256":digest,
        "compressed_bytes":size,
        "uncompressed_physical_line_count":physical_line_count,
        "publisher_reported_record_count":23741,
        "mirror_parsed_nonblank_rows_minus_publisher_count":all_rows-23741,
        "publisher_vs_mirror_count_discrepancy_resolved":False,
        "actual_csv_column_names":header,
        "independently_authenticated_against_original_LANL_bytes":False,
        "publisher_raw_file_directly_retrieved":False,
        "dataset_scale":dataset_scale,
        "raw_rows_inspected":all_rows,
        "sample_protocol":"FIRST_N_WELL_FORMED_ROWS_IN_ARCHIVE_ORDER_NO_LABEL_SELECTION",
        "sample_limit":sample_rows,
        "sample_rows_evaluated":sampled,
        "schema_column_count":len(header),
        "critical_columns_documented":list(MINIMUM_FIELDS),
        "schema_has_node_fault_start_and_fix":True,
        "malformed_width_rows":malformed_width,
        "sample_anonymized_system_groups":len(sampled_systems),
        "sample_blank_system_id_rows":sample_blank_system,
        "sample_rows_with_downtime_field":sample_with_downtime,
        "sample_rows_with_cause_category":sample_nonempty_root_cause,
        "sample_parseable_start_and_fix_times":sample_time_complete,
        "sample_time_missing":sample_time_missing,
        "sample_time_unparseable":sample_time_unparseable,
        "sample_fixed_before_start":sample_negative_duration,
        "timestamp_timezone_documented_at_row_level":False,
        "verified_single_service_identity":False,
        "verified_pre_fault_service_active_state":False,
        "verified_fault_caused_loss_of_same_service":False,
        "verified_policy_actions_and_observation_history":False,
        "verified_same_service_reacquisition":False,
        "verified_physical_fault_disjoint_route_ontology":False,
        "independent_real_physical_systems_admitted_for_H1":0,
        "strict_restoration_eligible_labels":0,
        "H1_confirmatory_result":False,
        "H1_preregistered":False,
        "admission":"BLOCKED_PHYSICAL_SERVICE_TRAJECTORY_AND_ORIGINAL_PROVENANCE",
        "result":"PASS",
    }


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--input-xz",type=Path,required=True)
    parser.add_argument("--expected-sha256")
    parser.add_argument("--sample-rows",type=int,default=SAMPLE_ROWS)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    summary=audit_raw(args.input_xz,expected_sha256=args.expected_sha256,
                      sample_rows=args.sample_rows)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",
                               encoding="utf-8")
    print(json.dumps(summary,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
