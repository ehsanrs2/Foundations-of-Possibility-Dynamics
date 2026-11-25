import unittest
from dataclasses import replace
from copy import deepcopy
from experiments.p1_gate2 import Fault, bfs_postfault, dfs_postfault, generated
from experiments.p1_r16n_gog1_goal_slicing import _action, _model
from experiments.p1_r16o_gog1b_scaling import index_actions, indexed_slice
from experiments.p1_r16p_gog2a_components import (
    METHODS, REPETITIONS, GroupWork, components, union_slice, fixture,
    cases, solve, query, worker, reference, compare, orders,
)

class ComponentTests(unittest.TestCase):
    def test_matched_size_and_arity(self):
        self.assertEqual(len(cases()),28)
        for n in (4,6):
            for stock in (1,3):
                for noise in (0,2):
                    models=[fixture(n,k,stock,noise)
                            for k in ("singleton","pairs","all")]
                    shapes=[[(len(a.requires),a.consumes,a.yields,a.generative)
                             for a in m.actions] for m in models]
                    self.assertTrue(all(x==shapes[0] for x in shapes))
                    self.assertEqual(len(shapes[0]),2*n+noise)

    def test_grouping_interleaved_and_transitive(self):
        expected={"singleton":[["g0"],["g1"],["g2"],["g3"]],
                  "pairs":[["g0","g2"],["g1","g3"]],
                  "all":[["g0","g1","g2","g3"]],
                  "chain":[["g0","g1","g2","g3"]]}
        for k,g in expected.items():
            m=fixture(4,k,3,0)
            self.assertEqual(solve(m,"adaptive_components",True)[2],g)
        self.assertEqual(solve(fixture(4,"pairs",3,0),"fixed_pairs",True)[2],
                         [["g0","g1"],["g2","g3"]])

    def test_empty_action_slices_stay_separate(self):
        w=GroupWork()
        self.assertEqual(components({"a":(frozenset({"a"}),()),
                                     "b":(frozenset({"b"}),())},w),
                         [frozenset({"a"}),frozenset({"b"})])
        self.assertEqual(w.pair_tests,1)
        self.assertEqual(w.merge_operations,0)

    def test_resource_producers_connect_and_preserve_goals(self):
        m=_model([_action("collect",["seed"],"unused",reward=1),
                  _action("a",["seed"],"a",2,generative=True),
                  _action("b",["seed"],"b",2,generative=True)],
                 ["a","b"],stock=1,horizon=2)
        result=query(m,"adaptive_components")
        self.assertEqual(result["groups"]["constructive"],[["a","b"]])
        self.assertEqual(result["constructive"],{"a":2,"b":2})

    def test_union_matches_direct_closure(self):
        for m,_ in cases().values():
            for enabled in (False,True):
                actions=tuple(a for a in m.actions if enabled or not a.generative)
                w=GroupWork()
                idx=index_actions(actions,w)
                slices={g:indexed_slice(actions,frozenset({g}),idx,w) for g in m.goals}
                for group in components(slices,w):
                    self.assertEqual(union_slice(actions,group,slices,w),
                                     indexed_slice(actions,group,idx,w))

    def test_all_cases_all_methods_both_arms(self):
        for name,(m,_) in cases().items():
            for enabled in (False,True):
                expected=bfs_postfault(m,construction=enabled)
                for method in METHODS:
                    with self.subTest(name=name,enabled=enabled,method=method):
                        self.assertEqual(solve(m,method,enabled)[0],expected)

    def test_generated_tiny_oracle(self):
        for m in generated(seed=161126,n=32):
            m=replace(m,fault=Fault(0,frozenset(),(0,)*len(m.resources)))
            for enabled in (False,True):
                expected=dfs_postfault(m,construction=enabled)
                self.assertEqual(solve(m,"adaptive_components",enabled)[0],expected)

    def test_grouping_cost_counted(self):
        m=fixture(6,"pairs",3,2)
        a=query(m,"adaptive_components")["work"]
        b=query(m,"shared_index")["work"]
        self.assertEqual(a["index_action_checks"],b["index_action_checks"])
        self.assertEqual(a["pair_tests"],30)
        self.assertEqual(a["merge_operations"],3)
        self.assertGreater(a["union_action_memberships"],0)
        self.assertGreater(a["union_capability_memberships"],0)
        self.assertEqual(b["pair_tests"],0)

    def test_repetitions_balanced_and_incomplete_blocked(self):
        self.assertEqual(list(orders()),list(orders()))
        self.assertEqual(len(list(orders())),REPETITIONS)
        self.assertTrue(all(sorted(x)==sorted(METHODS) for x in orders()))
        self.assertIsNone(compare({},{}))
        self.assertIsNone(compare({m:[{"status":"WALL_TIMEOUT"}]*REPETITIONS
                                   for m in METHODS},{}))

    def test_same_count_wrong_time_blocks_comparison(self):
        oracle=reference()
        runs={}
        for method in METHODS:
            r=worker(method)
            runs[method]=[{"status":"PASS","wall_ms":1.0,**deepcopy(r)}
                          for _ in range(REPETITIONS)]
        runs["adaptive_components"][0]["cases"]["pairs_g4_stock3_noise0"]["constructive"]["g1"]=99
        with self.assertRaisesRegex(AssertionError,"earliest mismatch"):
            compare(runs,oracle)

if __name__=="__main__":
    unittest.main()
