"""Property and negative tests; no confirmatory scientific inference."""
import unittest
from dataclasses import replace
from experiments.p1_gate0 import Rule, Instance, exhaustive_oracle, dp_reachability, shock, rename, audit


class Gate0Tests(unittest.TestCase):
    def test_and_prerequisites(self):
        inst = Instance(frozenset({'a','b'}), frozenset({'goal'}),
                        (Rule(frozenset({'a','b'}),'goal',1,1),),1,1)
        self.assertEqual(dp_reachability(inst), frozenset({'goal'}))
        self.assertEqual(dp_reachability(shock(inst,{'b'})),frozenset())

    def test_cost_and_latency(self):
        inst = Instance(frozenset({'a'}),frozenset({'goal'}),
                        (Rule(frozenset({'a'}),'b',1,2),
                         Rule(frozenset({'b'}),'goal',2,1)),3,3)
        for change in ({'budget':2},{'horizon':2}):
            self.assertEqual(dp_reachability(replace(inst, **change)),frozenset())
        self.assertEqual(dp_reachability(inst),frozenset({'goal'}))
        self.assertEqual(exhaustive_oracle(inst),dp_reachability(inst))

    def test_zero_time_and_budget(self):
        inst=Instance(frozenset({'a'}), frozenset({'a','goal'}),
                      (Rule(frozenset({'a'}),'goal',0,1),),0,0)
        self.assertEqual(dp_reachability(inst),frozenset({'a'}))
        self.assertEqual(dp_reachability(inst,allow_build=False),frozenset({'a'}))

    def test_disabled_construction(self):
        inst=Instance(frozenset({'a'}), frozenset({'goal'}),
                      (Rule(frozenset({'a'}),'goal',0,1),),1,0)
        self.assertFalse(dp_reachability(inst,allow_build=False))
        self.assertTrue(dp_reachability(inst))

    def test_renaming(self):
        inst=Instance(frozenset({'a'}), frozenset({'g'}),
                      (Rule(frozenset({'a'}),'g',0,1),),1,0)
        self.assertEqual(len(dp_reachability(inst)),len(dp_reachability(rename(inst))))

    def test_invalid_models(self):
        with self.assertRaises(ValueError): Rule(frozenset({'a'}),'a')
        with self.assertRaises(ValueError): Rule(frozenset(),'a',-1)
        with self.assertRaises(ValueError): Rule(frozenset(),'a',0,0)
        with self.assertRaises(ValueError): Instance(frozenset(),frozenset(),tuple(),-1,0)
        with self.assertRaises(ValueError): Instance(frozenset(),frozenset(),
                            (Rule(frozenset(),'a'), Rule(frozenset(),'a')),1,1)

    def test_randomized_crosscheck_fixed_seed(self):
        d=audit()
        self.assertEqual(d['outcome'],'PASS')
        self.assertEqual(d['solver_pair_comparisons'],256)
        self.assertEqual(d['oracle_mismatches'],0)

if __name__=='__main__': unittest.main()
