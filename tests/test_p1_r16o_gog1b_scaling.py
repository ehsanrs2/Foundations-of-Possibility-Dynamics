import unittest
from dataclasses import replace
from experiments.p1_gate2 import generated, Fault, bfs_postfault, dfs_postfault
from experiments.p1_r16n_gog1_goal_slicing import backward_slice, Work
from experiments.p1_r16o_gog1b_scaling import (
    METHODS, REPETITIONS, IndexedWork, index_actions, indexed_slice,
    factorial, query, solve, orders, compare_runs, worker,
)

class ScalingTests(unittest.TestCase):
    def test_factorial_design_is_fixed(self):
        models=factorial()
        self.assertEqual(len(models),27)
        for overlap in ("shared","disjoint"):
            self.assertEqual(sum(meta["overlap"]==overlap
                                 for _,meta in models.values()),12)
        self.assertEqual(max(len(m.actions) for m,_ in models.values()),14)

    def test_every_factorial_earliest_goal_dictionary(self):
        for name,(m,_) in factorial().items():
            for enabled in (False,True):
                expected=bfs_postfault(m,construction=enabled)
                for method in METHODS:
                    with self.subTest(case=name,arm=enabled,method=method):
                        self.assertEqual(solve(m,method,enabled)[0],expected)

    def test_index_equals_scan_closure_on_generated_cases(self):
        for m in generated(seed=161125,n=32):
            m=replace(m,fault=Fault(0,frozenset(),(0,)*len(m.resources)))
            for enabled in (False,True):
                actions=tuple(a for a in m.actions if enabled or not a.generative)
                w=IndexedWork()
                index=index_actions(actions,w)
                self.assertEqual(w.index_action_checks,len(actions))
                for goals in [m.goals]+[frozenset({g}) for g in m.goals]:
                    self.assertEqual(indexed_slice(actions,goals,index,w),
                                     backward_slice(actions,goals,Work()))
                self.assertEqual(solve(m,"goalwise_index",enabled)[0],
                                 dfs_postfault(m,construction=enabled))

    def test_resource_yield_and_deadline_controls(self):
        for name,expected in (("resource_yield",1),
                ("resource_tight_time",0),("resource_tight_stock",0)):
            m,_=factorial()[name]
            self.assertEqual(query(m,"goalwise_index")["gog"],expected)

    def test_index_once_per_arm_not_per_goal(self):
        m,_=factorial()["disjoint_g6_stock3_noise2"]
        a=query(m,"goalwise_index")["work"]
        b=query(m,"shared_index")["work"]
        self.assertEqual(a["index_action_checks"],b["index_action_checks"])
        self.assertEqual(a["search_calls"],12)
        self.assertEqual(b["search_calls"],2)

    def test_repeated_order_is_balanced_and_reproducible(self):
        self.assertEqual(list(orders()),list(orders()))
        self.assertEqual(len(list(orders())),REPETITIONS)
        self.assertTrue(all(sorted(x)==sorted(METHODS) for x in orders()))

    def test_incomplete_coverage_has_no_comparison(self):
        self.assertIsNone(compare_runs({},{}))
        runs={m:[{"status":"PASS"}]*REPETITIONS for m in METHODS}
        runs["shared_index"]=[{"status":"WALL_TIMEOUT"}]*REPETITIONS
        self.assertIsNone(compare_runs(runs,{}))

    def test_wrong_earliest_tick_blocks_comparison(self):
        from copy import deepcopy
        r=worker("shared_index")
        oracle={n:{k:c[k] for k in ("ordinary","constructive")}
                for n,c in r["cases"].items()}
        runs={m:[{"status":"PASS",**deepcopy(r),"method":m}
                 for _ in range(REPETITIONS)] for m in METHODS}
        runs["shared_index"][0]["cases"]["shared_g2_stock1_noise0"]["constructive"]["g1"]=99
        with self.assertRaisesRegex(AssertionError,"earliest mismatch"):
            compare_runs(runs,oracle)

if __name__=="__main__":
    unittest.main()
