import unittest
from fractions import Fraction
from experiments.p1_r16m_n1_r1_information_audit import (
    audit, triangle_counterexample, _oracle_compression_penalty,
)

class N1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = audit()

    def test_cut_equivalence_is_not_general(self):
        self.assertEqual(triangle_counterexample(),
                         {"R1":0,"minimum_event_cut":2})

    def test_observed_development_redundancy(self):
        self.assertEqual(self.result["rows"],108)
        self.assertTrue(self.result["R1_equals_cut_at_least_two_on_C2a"])
        self.assertTrue(self.result["R1_equals_independent_times_positive_stock_on_C2a"])
        self.assertEqual(self.result["in_sample_raw_excess_brier"],
                         self.result["in_sample_raw_plus_R1_excess_brier"])

    def test_matched_witness_is_a_real_collision(self):
        low, high = self.result["witness_low"], self.result["witness_high"]
        for k in ("mode","kits","prior","R1","cut"):
            self.assertEqual(low[k],high[k])
        self.assertNotEqual(low["family"],high["family"])
        self.assertGreater(Fraction(high["p"]),Fraction(low["p"]))
        self.assertGreater(self.result["cells_with_different_exact_recovery"],0)

    def test_compression_penalty_exact(self):
        rows=[{"p":Fraction(0)},{"p":Fraction(1)}]
        self.assertEqual(_oracle_compression_penalty(rows,lambda _:0),Fraction(1,4))

    def test_scientific_firewall(self):
        self.assertFalse(self.result["H1_preregistered"])
        self.assertFalse(self.result["sealed_families_accessed"])
        self.assertEqual(self.result["field_labels"],0)
        self.assertEqual(self.result["H1_confirmatory_samples"],0)

if __name__=="__main__":
    unittest.main()
