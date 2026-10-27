"""R2 executable negative controls: structural backup != feasible robust policy."""
from dataclasses import replace
from fractions import Fraction
import json
from pathlib import Path
import unittest

from experiments.p1_gate1 import enumerate_dfs
from experiments.fault_ontology_r1 import assess
from experiments.p1_gate4 import (optimal_state_dp, optimal_history_oracle,
                                  clairvoyant_upper_bound)
from experiments.resource_policy_r2 import (
    individual_plan_model, physical_route_scope, bounded_policy_problem,
    compare, audit,
)


class R2PolicyBridgeTests(unittest.TestCase):
    def test_one_kit_has_static_backup_but_only_half_policy_success(self):
        data = compare(1, 2)
        self.assertEqual(data["scoped_backup_pair"], 1)
        self.assertEqual(data["static_plan_survival"], "3/4")
        self.assertEqual(data["nonclairvoyant_policy_success"], "1/2")
        self.assertEqual(data["clairvoyant_upper_success"], "3/4")

    def test_two_kits_allow_both_preparations(self):
        data = compare(2, 2)
        self.assertEqual(data["scoped_backup_pair"], 1)
        self.assertEqual(data["nonclairvoyant_policy_success"], "3/4")
        self.assertEqual(data["event_min_cut"], 2)

    def test_two_kits_but_one_preparation_tick(self):
        data = compare(2, 1)
        self.assertEqual(data["scoped_backup_pair"], 1)
        self.assertEqual(data["nonclairvoyant_policy_success"], "1/2")

    def test_no_kits_no_individual_route(self):
        data = compare(0, 2)
        self.assertEqual(data["scoped_backup_pair"], 0)
        self.assertEqual(data["individually_feasible_plans"], 0)
        self.assertEqual(data["nonclairvoyant_policy_success"], "0")

    def test_no_construction_is_zero(self):
        for kits in (0, 1, 2):
            p = bounded_policy_problem(kits=kits)
            self.assertEqual(optimal_state_dp(p, construction=False).value, 0)
            self.assertEqual(optimal_history_oracle(p, construction=False).value, 0)

    def test_same_physical_incidence_not_changed_by_inventory(self):
        scope = physical_route_scope()
        for kits in (1, 2):
            plans = enumerate_dfs(individual_plan_model(kits=kits),
                                  construction=True)
            self.assertEqual(assess(plans, "service", scope).indicator, 1)

    def test_common_cause_new_event_invalidates_disjointness(self):
        scope = physical_route_scope()
        common = replace(scope, scope_id="COMMON_CAUSE",
            incidence={
                "rule:serve_a": frozenset({"event:loss_a","event:shared"}),
                "rule:serve_b": frozenset({"event:loss_b","event:shared"}),
            },
            event_universe=scope.event_universe | {"event:shared"})
        plans = enumerate_dfs(individual_plan_model(kits=1),
                              construction=True)
        self.assertEqual(assess(plans,"service",common).indicator,0)
        self.assertEqual(assess(plans,"service",common).min_event_cut,1)

    def test_scenario_order_cannot_change_optimum(self):
        p = bounded_policy_problem(kits=1)
        rev = replace(p, scenarios=tuple(reversed(p.scenarios)))
        self.assertEqual(optimal_state_dp(p, construction=True).value,
                         optimal_state_dp(rev, construction=True).value)

    def test_preparation_deadline_zero(self):
        d = compare(2, 0)
        self.assertEqual(d["nonclairvoyant_policy_success"], "0")
        self.assertEqual(d["clairvoyant_upper_success"], "0")

    def test_only_one_kit_but_three_preparation_ticks(self):
        self.assertEqual(compare(1, 3)["nonclairvoyant_policy_success"], "1/2")

    def test_exact_rational_probabilities(self):
        p = bounded_policy_problem(kits=2)
        self.assertEqual(clairvoyant_upper_bound(p, construction=True),
                         Fraction(3, 4))

    def test_archived_audit(self):
        manifest = Path(__file__).parents[1] / "experiments" / "r2_expected.json"
        self.assertEqual(audit(), json.loads(manifest.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
