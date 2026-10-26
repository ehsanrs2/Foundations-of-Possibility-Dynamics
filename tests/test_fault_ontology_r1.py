"""R1: fail-closed physical event ontology and deterministic negative controls."""
from dataclasses import replace
from fractions import Fraction
import unittest

from experiments.p1_gate1 import enumerate_dfs, example
from experiments.gbr_review_counterexamples import alias_fixture, split_source_fixture
from experiments.fault_ontology_r1 import (
    FaultOntology, alias_scope, split_source_scope, alarm_scope,
    normalized_supports, assess, minimum_event_cut,
    exact_static_survival_probability, audit,
)


class FaultOntologyR1Tests(unittest.TestCase):
    def setUp(self):
        self.plans = enumerate_dfs(alias_fixture(), construction=True)

    def test_same_physical_channel_is_not_backup(self):
        score = assess(self.plans, "goal", alias_scope(physically_distinct=False))
        self.assertEqual((score.indicator, score.canonical_plan_count,
                          score.min_event_cut), (0, 1, 1))

    def test_distinct_physical_channels_allow_scoped_backup(self):
        score = assess(self.plans, "goal", alias_scope(physically_distinct=True))
        self.assertEqual((score.indicator, score.canonical_plan_count,
                          score.min_event_cut), (1, 2, 2))

    def test_alias_relabeling_with_same_declared_physics(self):
        m = alias_fixture()
        renamed = replace(m, rules=tuple(replace(r, name="rename_" + r.name)
                                          for r in m.rules))
        original = alias_scope(physically_distinct=False)
        changed = FaultOntology("RENAMED", {
            "cap:source": "source:shared",
            "rule:rename_ordinary": "device:channel_a",
            "rule:rename_alias": "device:channel_a",
        }, {
            "rule:rename_ordinary": frozenset({"event:failure_a"}),
            "rule:rename_alias": frozenset({"event:failure_a"}),
        }, {"cap:source": "Source scope unchanged"},
            frozenset({"event:failure_a"}))
        self.assertEqual(assess(enumerate_dfs(renamed, construction=True),
                                "goal", changed).indicator,
                         assess(self.plans, "goal", original).indicator)

    def test_scope_without_source_incidence_must_explicitly_protect(self):
        m = alias_scope(physically_distinct=False)
        with self.assertRaises(ValueError):
            replace(m, protected={})  # reject incomplete scope at creation

    def test_missing_plan_support_rejected_not_ignored(self):
        m = alias_scope(physically_distinct=False)
        incomplete = replace(m, mechanisms={"rule:ordinary":"physical:x",
                                           "rule:alias":"physical:x"},
                             protected={},
                             incidence={"rule:ordinary": frozenset({"event:failure_a"}),
                                        "rule:alias": frozenset({"event:failure_a"})})
        with self.assertRaisesRegex(ValueError, "unmapped"):
            assess(self.plans, "goal", incomplete)

    def test_conflicting_incidence_for_same_mechanism_rejected(self):
        m = alias_scope(physically_distinct=False)
        with self.assertRaisesRegex(ValueError, "conflicting"):
            replace(m, incidence={"rule:ordinary": frozenset({"event:failure_a"}),
                                  "rule:alias": frozenset({"event:failure_b"})},
                    event_universe=frozenset({"event:failure_a","event:failure_b"}))

    def test_blank_protection_reason_not_accepted(self):
        m = alias_scope(physically_distinct=False)
        with self.assertRaises(ValueError):
            replace(m, protected={"cap:source": ""})

    def test_invalid_event_incidence_rejected(self):
        m = alias_scope(physically_distinct=False)
        with self.assertRaises(ValueError):
            replace(m, incidence={"rule:ordinary": frozenset(),
                                  "rule:alias": frozenset({"event:failure_a"})})
        with self.assertRaises(ValueError):
            replace(m, event_universe=frozenset({"event:other"}))

    def test_no_supported_exposure_means_indeterminate(self):
        physical = FaultOntology(
            "PROTECTED_PATH", {"cap:source":"component:source",
                               "rule:ordinary":"device:a","rule:alias":"device:b"},
            {"rule:ordinary":frozenset({"event:failure_a"})},
            {"cap:source":"Protected for this diagnostic",
             "rule:alias":"Action assumed protected for this diagnostic"},
            frozenset({"event:failure_a"}))
        assessed = assess(self.plans, "goal", physical)
        self.assertEqual(assessed.status, "INSUFFICIENT_FAULT_COVERAGE")
        self.assertIsNone(assessed.indicator)
        with self.assertRaises(ValueError):
            exact_static_survival_probability(
                self.plans,"goal",physical,{"event:failure_a": Fraction(1, 2)})

    def test_split_source_physical_identity_collapses_backup(self):
        plans = enumerate_dfs(split_source_fixture(), construction=True)
        outcome = assess(plans,"goal",split_source_scope())
        self.assertEqual(outcome.indicator, 0)
        self.assertEqual(outcome.min_event_cut, 1)

    def test_common_power_changes_alarm_scoped_pair(self):
        alarm = enumerate_dfs(example(), construction=True)
        self.assertEqual(assess(alarm,"alarm",alarm_scope(common_power_exposed=False)).indicator,1)
        self.assertEqual(assess(alarm,"alarm",alarm_scope(common_power_exposed=True)).indicator,0)

    def test_same_event_vs_independent_event_reliabilities(self):
        same = exact_static_survival_probability(
            self.plans,"goal",alias_scope(physically_distinct=False),
            {"event:failure_a": Fraction(1, 2)})
        independent = exact_static_survival_probability(
            self.plans,"goal",alias_scope(physically_distinct=True),
            {"event:failure_a": Fraction(1, 2),"event:failure_b": Fraction(1, 2)})
        self.assertEqual(same, Fraction(1, 2))
        self.assertEqual(independent, Fraction(3, 4))

    def test_invalid_probability_inputs_fail(self):
        s = alias_scope(physically_distinct=False)
        with self.assertRaises(ValueError):
            exact_static_survival_probability(
                self.plans,"goal",s,{"event:other":Fraction(1, 2)})
        with self.assertRaises(ValueError):
            exact_static_survival_probability(
                self.plans,"goal",s,{"event:failure_a":Fraction(3, 2)})
        with self.assertRaises(ValueError):
            exact_static_survival_probability(
                self.plans,"goal",s,{"event:failure_a":0.5})

    def test_no_feasible_goal_does_not_imply_backup(self):
        outcome = assess(frozenset(), "goal", alias_scope(physically_distinct=True))
        self.assertEqual((outcome.status,outcome.indicator,outcome.canonical_plan_count),
                         ("NO_FEASIBLE_PLAN",0,0))
        self.assertEqual(minimum_event_cut(frozenset()),0)

    def test_fixture_audit_expected(self):
        res = audit()
        self.assertEqual(res["result"],"PASS")
        self.assertEqual(res["same_physical_pair"],0)
        self.assertEqual(res["independent_physical_pair"],1)
        self.assertEqual(res["alarm_with_common_power_pair"],0)

    def test_archived_r1_manifest(self):
        import json
        from pathlib import Path
        path = Path(__file__).parents[1] / "experiments" / "r1_expected.json"
        self.assertEqual(audit(), json.loads(path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
