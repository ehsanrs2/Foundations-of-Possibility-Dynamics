"""Avoid treating hypothetical sensitivity planning as measured statistical power."""
import unittest
from experiments.p1_sample_size_sensitivity import illustrative_n, table


class SampleSizeSensitivityTests(unittest.TestCase):
    def test_known_formula_cells(self):
        self.assertEqual(illustrative_n(0.1,0.02),197)
        self.assertEqual(illustrative_n(0.2,0.02),785)

    def test_smaller_minimum_effect_requires_more_independent_systems(self):
        self.assertGreater(illustrative_n(0.1,0.01),
                           illustrative_n(0.1,0.03))

    def test_larger_sd_requires_more_systems(self):
        self.assertGreater(illustrative_n(0.2,0.02),
                           illustrative_n(0.05,0.02))

    def test_invalid_quantities_rejected(self):
        for sd,effect in ((0,0.02),(0.1,0),(1.1,0.1)):
            with self.assertRaises(ValueError):
                illustrative_n(sd,effect)

    def test_illustrative_not_final(self):
        t=table()
        self.assertIn("HYPOTHETICAL",t["classification"])
        self.assertEqual(len(t["rows"]),12)


if __name__ == "__main__":
    unittest.main()
