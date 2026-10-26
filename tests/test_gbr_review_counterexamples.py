"""Regression suite for review #8/#9 negative metric findings (NOT H1)."""
import unittest
from dataclasses import replace

from experiments.p1_gate1 import Rule, _backup, enumerate_dfs, example, measures
from experiments.gbr_review_counterexamples import (
    alias_fixture, split_source_fixture, deadline_fixture,
    physical_signatures, canonical_backup, min_failure_hitting_set, audit,
)


class CriticalReviewAuditTests(unittest.TestCase):
    def test_duplicate_alias_produces_spurious_raw_gbr(self):
        m = alias_fixture()
        self.assertEqual(measures(m)["gog"], 0)
        self.assertEqual(measures(m)["gbr_gain"], 1)
        plans = enumerate_dfs(m, construction=True)
        self.assertEqual(len(plans), 2)

    def test_physical_alias_identity_prevents_false_pair(self):
        m = alias_fixture()
        plans = enumerate_dfs(m, construction=True)
        identities = {"rule:ordinary": "physical:same",
                      "rule:alias": "physical:same"}
        self.assertEqual(canonical_backup(plans, "goal", m.exposed, identities), 0)
        self.assertEqual(len(physical_signatures(
            plans, "goal", m.exposed, identities)), 1)

    def test_explicitly_distinct_physical_routes_are_not_collapsed(self):
        m = alias_fixture()
        plans = enumerate_dfs(m, construction=True)
        self.assertEqual(canonical_backup(plans, "goal", m.exposed, {}), 1)

    def test_repeated_rule_naming_does_not_modify_physical_result(self):
        original = alias_fixture()
        renamed = replace(original, rules=tuple(
            replace(r, name="new_" + r.name) for r in original.rules),
            exposed=frozenset("rule:new_" + r.name for r in original.rules))
        ids = {"rule:new_ordinary": "physical:same",
               "rule:new_alias": "physical:same"}
        self.assertEqual(measures(renamed)["gbr_gain"], 1)
        self.assertEqual(canonical_backup(
            enumerate_dfs(renamed, construction=True), "goal",
            renamed.exposed, ids), 0)

    def test_exposure_scope_includes_shared_initial_capability(self):
        m = alias_fixture()
        full = replace(m, exposed=m.exposed | {"cap:source"})
        self.assertEqual(measures(full)["gbr_gain"], 0)

    def test_empty_exposure_causes_vacuous_pair_even_if_model_forbids_it(self):
        m = alias_fixture()
        plans = enumerate_dfs(m, construction=True)
        self.assertEqual(_backup(plans, "goal", frozenset()), 1)
        with self.assertRaises(ValueError):
            replace(m, exposed=frozenset())

    def test_split_alias_sources_change_raw_measure(self):
        m = split_source_fixture()
        plans = enumerate_dfs(m, construction=True)
        self.assertEqual(measures(m)["gbr_gain"], 1)
        physical = {"cap:power_a": "physical:common_power",
                    "cap:power_b": "physical:common_power"}
        self.assertEqual(canonical_backup(
            plans, "goal", m.exposed, physical), 0)
        self.assertEqual(canonical_backup(plans, "goal", m.exposed, {}), 1)

    def test_shared_power_fault_scope_changes_alarm_example(self):
        m = example()
        self.assertEqual(measures(m)["gbr_gain"], 1)
        self.assertEqual(measures(replace(
            m, exposed=m.exposed | {"cap:power"}))["gbr_gain"], 0)

    def test_binary_gbr_ignores_zero_backup_slack(self):
        m = deadline_fixture()
        self.assertEqual(measures(m)["gbr_gain"], 1)
        paths = enumerate_dfs(m, construction=True)
        backup = next(p for p in paths if "rule:late_backup" in p.support)
        self.assertEqual(backup.duration, m.horizon)  # slack=0
        self.assertEqual(measures(replace(m, horizon=3))["gbr_gain"], 0)

    def test_small_hitting_set_baseline_disagrees_with_alias_score(self):
        m = alias_fixture()
        plans = enumerate_dfs(m, construction=True)
        self.assertEqual(min_failure_hitting_set(
            plans, "goal", m.exposed, {}), 2)
        self.assertEqual(min_failure_hitting_set(
            plans, "goal", m.exposed,
            {"rule:ordinary": "physical:same",
             "rule:alias": "physical:same"}), 1)

    def test_unmodeled_failure_cannot_cut_vulnerable_set(self):
        m = alias_fixture()
        plans = enumerate_dfs(m, construction=True)
        self.assertIsNone(min_failure_hitting_set(
            plans, "goal", frozenset(), {}))

    def test_counterexample_audit_has_all_expected_flags(self):
        a = audit()
        self.assertEqual(a["result"], "EXPECTED_METRIC_FAILURES_REPRODUCED")
        self.assertEqual(a["alias_raw_gbr_gain"], 1)
        self.assertEqual(a["alias_physical_pair"], 0)
        self.assertEqual(a["deadline_backup_slack_ticks"], 0)


if __name__ == "__main__":
    unittest.main()
