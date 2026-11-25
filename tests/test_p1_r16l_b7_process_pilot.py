import unittest
from experiments.p1_r16l_b7_process_pilot import run_pilot

class B7ProcessTests(unittest.TestCase):
    def test_real_local_restart_and_same_job(self):
        r = run_pilot()
        self.assertEqual(r["endpoint"],"RESTORED")
        events = [x["event"] for x in r["logs"]]
        self.assertEqual(events, ["pre_fault_response","stop_requested",
            "actual_child_exit","observed_unavailable","restart_requested",
            "same_job_probe","same_job_continued"])
        self.assertEqual(r["logs"][0]["job_id"],r["logs"][-1]["job_id"])
        self.assertEqual(r["logs"][-1]["completed"],2)
        ticks = [x["elapsed_ns"] for x in r["logs"]]
        self.assertEqual(ticks,sorted(ticks))
        self.assertFalse(r["H1_admitted"])
        self.assertFalse(r["independent_assessor"])
        self.assertEqual(r["H1_confirmatory_samples"],0)

    def test_no_restart_waits_to_declared_deadline(self):
        r = run_pilot(False)
        self.assertEqual(r["endpoint"],"NOT_RESTORED")
        self.assertGreaterEqual(r["logs"][-1]["elapsed_ns"],r["deadline_ns"])
        self.assertFalse(r["H1_admitted"])

    def test_invalid_control(self):
        with self.assertRaises(ValueError):
            run_pilot("true")

if __name__=="__main__":
    unittest.main()
