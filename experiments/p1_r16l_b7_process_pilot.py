"""B7a: actual local subprocess restart feasibility pilot, NOT independent evidence.

Only child processes created here are stopped. No network, external service,
real user data or production fault injection. The parent is both operator and
assessor, so these traces must never be admitted to H1 or called independent.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from time import monotonic_ns, sleep
from uuid import uuid4
import json
import selectors
import subprocess
import sys

WORKER = r'''
import json, sys, os
from pathlib import Path
p = Path(sys.argv[1])
for line in sys.stdin:
    state = json.loads(p.read_text())
    if line.strip() == "ADVANCE":
        state["completed"] += 1
        temp = p.with_suffix(".tmp")
        temp.write_text(json.dumps(state))
        os.replace(temp, p)
    elif line.strip() != "PROBE":
        raise ValueError("unregistered command")
    print(json.dumps(state), flush=True)
'''


def _call(child, command, deadline):
    if child.poll() is not None:
        raise RuntimeError("child unavailable")
    child.stdin.write(command + "\n")
    child.stdin.flush()
    remaining = (deadline-monotonic_ns())/1e9
    with selectors.DefaultSelector() as sel:
        sel.register(child.stdout, selectors.EVENT_READ)
        if remaining <= 0 or not sel.select(remaining):
            raise TimeoutError("child response deadline")
    response = child.stdout.readline()
    if not response:
        raise RuntimeError("child closed response stream")
    return json.loads(response)


def run_pilot(restart=True):
    """Observe a genuine stopped worker and same-ID checkpoint continuation.

    An observed process exit plus failed availability is not inferred from
    a simulated fault label. Deadline is a local 5-second engineering window,
    not a calibrated failure distribution. No external signature is verified.
    """
    if type(restart) is not bool:
        raise ValueError("restart must be boolean")
    start = monotonic_ns()
    deadline = start + 5_000_000_000
    job_id = uuid4().hex
    log = []
    children = []
    def mark(event, **fields):
        log.append({"event":event, "elapsed_ns":monotonic_ns()-start, **fields})
    with TemporaryDirectory(prefix="b7a-owned-") as d:
        p = Path(d)/"checkpoint.json"
        p.write_text(json.dumps({"job_id":job_id,"completed":0}))
        def spawn():
            c = subprocess.Popen([sys.executable,"-u","-c",WORKER,str(p)],
                  stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                  stderr=subprocess.DEVNULL, text=True)
            children.append(c)
            return c
        def remaining():
            return max(0.001,(deadline-monotonic_ns())/1e9)
        try:
            c = spawn()
            before = _call(c,"ADVANCE",deadline)
            if before != {"job_id":job_id,"completed":1}:
                raise AssertionError("incorrect pre-fault checkpoint")
            mark("pre_fault_response", **before)
            mark("stop_requested", owned_child=True)
            c.terminate()
            c.wait(timeout=remaining())
            if c.poll() is None:
                raise AssertionError("worker has not exited")
            mark("actual_child_exit", exit_code=c.returncode)
            try:
                _call(c,"PROBE",deadline)
            except RuntimeError:
                mark("observed_unavailable")
            else:
                raise AssertionError("stopped worker unexpectedly responded")
            regained = False
            if restart:
                mark("restart_requested")
                new = spawn()
                after = _call(new,"PROBE",deadline)
                if after != before:
                    raise AssertionError("checkpoint identity or progress changed")
                mark("same_job_probe", **after)
                continued = _call(new,"ADVANCE",deadline)
                if continued != {"job_id":job_id,"completed":2}:
                    raise AssertionError("same job did not continue")
                mark("same_job_continued", **continued)
                regained = monotonic_ns() <= deadline
            else:
                # Complete follow-up to the declared deadline, rather than
                # calling an abbreviated interval a failure.
                sleep(max(0,(deadline-monotonic_ns())/1e9))
                if c.poll() is None:
                    raise AssertionError("unexpected worker availability")
                mark("deadline_without_restart")
            return {"classification":"LOCAL_OPERATOR_OWNED_PROCESS_PILOT",
                    "job_id":job_id, "deadline_ns":5_000_000_000,
                    "endpoint":"RESTORED" if regained else "NOT_RESTORED",
                    "logs":log, "independent_assessor":False,
                    "independent_physical_systems":0,
                    "H1_confirmatory_samples":0, "H1_admitted":False,
                    "field_evidence_status":"BLOCKED_INDEPENDENT_ATTESTATION"}
        finally:
            for c in children:
                if c.poll() is None:
                    c.kill()
                    c.wait(timeout=2)
                c.stdin.close()
                c.stdout.close()


if __name__ == "__main__":
    print(json.dumps({"restart":run_pilot(True),
                      "no_restart":run_pilot(False)},indent=2))
