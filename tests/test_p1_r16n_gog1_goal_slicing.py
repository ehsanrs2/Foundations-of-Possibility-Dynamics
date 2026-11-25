import unittest
from dataclasses import replace
from experiments.p1_gate2 import Action, Fault, bfs_postfault, dfs_postfault, generated
from experiments.p1_gate3 import augmented_solver
from experiments.p1_r16b_semantic_conformance import (
    constructive_goal_fixture, backup_only_fixture, renamed_fixture,
    mutually_exclusive_goals_fixture,
)
from experiments.p1_r16n_gog1_goal_slicing import (
    METHODS, suite, solve, query, Work, backward_slice,
)

class GOG1Tests(unittest.TestCase):
    def check(self, model):
        for enabled in (False,True):
            expected=bfs_postfault(model,construction=enabled)
            for method in METHODS:
                self.assertEqual(solve(model,method,enabled)[0],expected)

    def test_all_fixed_suite_earliest_ticks(self):
        for name,model in suite().items():
            with self.subTest(case=name):
                self.check(model)

    def test_tiny_generated_oracle_agreement(self):
        for m in generated(seed=8117,n=40):
            m=replace(m,fault=Fault(0,frozenset(),(0,)*len(m.resources)))
            self.check(m)
            for arm in (False,True):
                self.assertEqual(solve(m,"goalwise_slice",arm)[0],
                                 dfs_postfault(m,construction=arm))

    def test_resource_producer_retained_despite_irrelevant_output(self):
        m=suite()["resource_yield"]
        relevant, actions=backward_slice(m.actions,m.goals,Work())
        self.assertNotIn("unrelated",relevant)
        self.assertIn("collect",{a.name for a in actions})
        self.assertEqual(query(m,"goalwise_slice")["constructive"],{"goal":3})

    def test_tight_time_and_stock(self):
        for name in ("resource_tight_time","resource_tight_stock"):
            self.assertEqual(query(suite()[name],"goalwise_slice")["gog"],0)

    def test_gog_does_not_measure_backup(self):
        self.assertEqual(query(backup_only_fixture(),"goalwise_slice")["gog"],0)

    def test_individual_goals_not_joint(self):
        m=mutually_exclusive_goals_fixture(stock=1)
        self.assertEqual(query(m,"goalwise_slice")["gog"],2)
        self.assertIsNone(augmented_solver(m,construction=True).joint)

    def test_alias_and_rename(self):
        m=constructive_goal_fixture()
        alias=replace(m,actions=m.actions+(replace(m.actions[0],name="alias"),))
        self.assertEqual(query(m,"goalwise_slice")["constructive"],
                         query(alias,"goalwise_slice")["constructive"])
        renamed=renamed_fixture(m,{"seed":"root","bridge":"relay","service":"objective"})
        self.assertEqual(query(renamed,"goalwise_slice")["constructive"],{"objective":2})
        self.check(alias)
        self.check(renamed)

    def test_goal_vocabulary_is_explicit(self):
        m=constructive_goal_fixture()
        expanded=replace(m,goals=m.goals|{"bridge"})
        self.assertEqual(query(m,"goalwise_slice")["gog"],1)
        self.assertEqual(query(expanded,"goalwise_slice")["gog"],2)

    def test_irrelevant_resource_producer_prerequisite_chain(self):
        m=suite()["resource_yield"]
        a=Action("open",frozenset({"seed"}),"access",(0,),(0,))
        m=replace(m,actions=(a,replace(m.actions[0],requires=frozenset({"access"})))+m.actions[1:],horizon=4)
        self.check(m)
        self.assertEqual(query(m,"goalwise_slice")["constructive"],{"goal":4})

    def test_fault_and_noninteger_stock_rejected(self):
        m=constructive_goal_fixture()
        for bad in (replace(m,fault=Fault(1,frozenset(),(0,))),
                    replace(m,stock=(1.5,))):
            with self.assertRaises(ValueError):
                solve(bad,"goalwise_slice",True)

    def test_repeated_goalwise_work_counted(self):
        m=suite()["shared_4"]
        self.assertEqual(query(m,"goalwise_slice")["work"]["search_calls"],8)
        self.assertEqual(query(m,"shared_slice")["work"]["search_calls"],2)

if __name__=="__main__":
    unittest.main()
