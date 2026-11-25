import unittest
from fractions import Fraction
from experiments.p1_r16k_c2_grouped_development import (
    FAMILIES, METHODS, trial_for, static_metrics, features,
    validate_split, grouped_brier, evaluate,
)
from experiments.p1_r9_physical_controls import static_pair
from experiments.p1_r12_cross_grammar_transfer import structure_signature

class C2Tests(unittest.TestCase):
    def test_direct_projection_matches_historical_feature(self):
        for mode in ("independent", "alias", "common"):
            for kits in (0, 1, 2):
                t = trial_for("direct", mode, kits, Fraction(1,2))
                p, c = static_metrics(t, mode)
                old = static_pair(mode, kits)
                self.assertEqual((p,c), (old["scoped_pair"], old["event_min_cut"]))

    def test_dual_stage_is_not_renaming(self):
        t = trial_for("dual_stage_dev", "independent", 2, Fraction(1,2))
        self.assertEqual(len(t.base.actions), 6)
        self.assertEqual(t.base.actions[3].requires, frozenset({"port_b"}))
        self.assertNotEqual(structure_signature(t,"independent"),
            structure_signature(trial_for("shared_stage","independent",2,
                                          Fraction(1,2)), "independent"))

    def test_sealed_family_rejected(self):
        for family in ("spatial_lattice", "hierarchical_common_cause"):
            with self.assertRaises(ValueError):
                trial_for(family, "independent", 2, Fraction(1,2))

    def test_split_rejects_signature_overlap(self):
        rows = [{"family":f,"partition":p,"group":f,"signature":f}
                for f,p in FAMILIES.items()]
        validate_split(rows)
        rows[-1]["signature"] = rows[0]["signature"]
        with self.assertRaisesRegex(ValueError,"cross-partition"):
            validate_split(rows)

    def test_group_weights_not_row_weights(self):
        rows = [{"group":"a","truth":"1","prediction":1.}]*3 + [
                {"group":"b","truth":"1","prediction":0.}]
        self.assertEqual(grouped_brier(rows), .5)

    def test_six_equal_slot_methods(self):
        t = trial_for("dual_stage_dev", "independent", 2, Fraction(1,2))
        xs = [features(t,"independent",Fraction(1,2),m) for m in METHODS]
        self.assertTrue(all(len(x)==9 for x in xs))
        self.assertEqual(len({x[:-1] for x in xs}),1)

    def test_real_fit_and_grouped_scores(self):
        r = evaluate("r1_scoped_pair")
        self.assertEqual(r["groups"], {"TRAIN":18,"TUNE":9,"DEV_EVAL":9})
        self.assertEqual(r["confirmatory_samples"],0)
        self.assertTrue(all(0 <= v <= 1 for v in r["scores"].values()))

if __name__ == "__main__":
    unittest.main()
