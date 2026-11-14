"""B6: noisy/delayed goal sensing and auditable *synthetic* evidence artifacts.

This opt-in developer gate reuses B4's hidden-fault G2 semantics, but
preserves an explicit firewall between (a) what the FIXED policy receives
and (b) privileged scoring truth. Exact rational sensor probabilities are
stipulated; readings are independent conditional on their contemporaneous
true pre-command goal states. A measurement sampled at tick t is delivered
at t+lag, with no early value, never retroactively.

Nothing here authenticates outside data, verifies physical mechanisms,
identifies a causal effect, or preregisters/validates P1/H1.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json

from experiments.p1_gate2 import Action, Fault, Model
from experiments.p1_r16e_b4_hidden_fault_policy import (
    Scenario, World, _validate, _fault_state, _command_step,
)

PROFILE = "B6_SYNTHETIC_NOISY_SENSOR_LOG_V1"
RESTORED = "RESTORED"
NOT_RESTORED = "NOT_RESTORED"
NOT_AT_RISK = "NOT_AT_RISK"
CENSORED = "CENSORED"
UNKNOWN_RISK = "UNKNOWN_RISK"
STATUSES = (RESTORED, NOT_RESTORED, NOT_AT_RISK, CENSORED, UNKNOWN_RISK)


@dataclass(frozen=True)
class Sensor:
    """Exact P(report present|present), P(report absent|absent), and lag."""
    sensitivity: Fraction
    specificity: Fraction
    lag: int = 0

    def validate(self) -> None:
        if (type(self.sensitivity) is not Fraction or
            type(self.specificity) is not Fraction or
            not Fraction(0) <= self.sensitivity <= Fraction(1) or
            not Fraction(0) <= self.specificity <= Fraction(1)):
            raise ValueError("sensor rates must be exact rational probabilities")
        if type(self.lag) is not int or self.lag not in (0, 1, 2):
            raise ValueError("sensor lag must be an integer in 0..2")


@dataclass(frozen=True)
class Trace:
    scenario: str                    # evaluator-only
    fault_tick: int                  # evaluator-only
    sensor_bits: tuple[bool, ...]    # evaluator-only independent noise word
    true_samples: tuple[bool, ...]   # evaluator-only at pre-command ticks
    collected: tuple[bool, ...]      # evaluator-only sampled sensor values
    policy_log: tuple[tuple[int, bool | None, str, bool], ...]
    held_before_fault: bool
    lost_at_fault: bool
    first_regained_tick: int | None
    held_at_horizon: bool
    followup_until: int
    status: str


def _validate_inputs(world: World, scenario: Scenario, sensor: Sensor,
                     followup_until: int) -> None:
    _validate(world)
    sensor.validate()
    if scenario not in world.scenarios:
        raise ValueError("scenario is not part of the stipulated world")
    if (type(followup_until) is not int or
        not 0 <= followup_until <= world.base.horizon):
        raise ValueError("follow-up must be an inclusive tick in 0..H")
    if len(world.base.goals) != 1 or len(world.base.actions) != 1:
        raise ValueError("B6 is a one-goal, one-repair-action diagnostic")
    action = world.base.actions[0]
    if (action.name != "repair" or action.generative or
        action.produces not in world.base.goals):
        raise ValueError("B6 needs an ordinary 'repair' producing that goal")


def _status(fault_tick: int, followup: int, actual_loss: bool,
            regained: int | None, horizon: int) -> str:
    # B5's NOT_AT_RISK label assumed the fault truth was observed even if
    # followup stopped before the incident. B6 makes this gap explicit.
    if followup < fault_tick:
        return UNKNOWN_RISK
    if not actual_loss:
        return NOT_AT_RISK
    if regained is not None and regained <= followup:
        return RESTORED
    return CENSORED if followup < horizon else NOT_RESTORED


def execute(world: World, scenario: Scenario, sensor: Sensor,
            faithful_bits: tuple[bool, ...], *,
            followup_until: int | None = None) -> Trace:
    """One trajectory. Only delayed Boolean sensor readings reach policy."""
    H = world.base.horizon
    F = H if followup_until is None else followup_until
    _validate_inputs(world, scenario, sensor, F)
    if (len(faithful_bits) != H or
        any(type(x) is not bool for x in faithful_bits)):
        raise ValueError("sensor noise word must contain exactly H booleans")

    goal = next(iter(world.base.goals))
    held, stock, disabled = world.base.initial, world.base.stock, frozenset()
    truth: list[bool] = []
    measured: list[bool] = []
    log: list[tuple[int, bool | None, str, bool]] = []
    before = lost = False
    first = None
    actions = {"repair": world.base.actions[0]}
    for tick in range(H):
        if tick == scenario.fault.tick:
            before = goal in held
            held, stock, disabled = _fault_state(
                held, stock, disabled, scenario.fault)
            lost = before and goal not in held
        present = goal in held
        truth.append(present)
        measured.append(present if faithful_bits[tick] else not present)
        received = (measured[tick - sensor.lag]
                    if tick >= sensor.lag else None)
        # A fixed, nonclairvoyant rule: NEVER receives fault ID, loss flag,
        # physical current state, or not-yet-delivered sample.
        cmd = "repair" if received is False else "WAIT"
        accepted, held, stock = _command_step(
            held, stock, disabled, cmd, actions, False)
        log.append((tick, received, cmd, accepted))
        if lost and first is None and goal in held and tick >= scenario.fault.tick:
            first = tick + 1

    return Trace(scenario.name, scenario.fault.tick, faithful_bits,
                 tuple(truth), tuple(measured), tuple(log),
                 before, lost, first, goal in held, F,
                 _status(scenario.fault.tick, F, lost, first, H))


def independent_replay(world: World, scenario: Scenario, sensor: Sensor,
                       faithful_bits: tuple[bool, ...], *,
                       followup_until: int | None = None) -> Trace:
    """Second implementation: plain mutable sets/dicts, never B4 transitions."""
    H = world.base.horizon
    F = H if followup_until is None else followup_until
    _validate_inputs(world, scenario, sensor, F)
    if len(faithful_bits) != H or any(type(x) is not bool for x in faithful_bits):
        raise ValueError("invalid sensor noise word")
    goal = next(iter(world.base.goals))
    caps = set(world.base.initial)
    inv = dict(zip(world.base.resources, world.base.stock))
    disabled: set[str] = set()
    sensor_samples: list[bool] = []
    truth_samples: list[bool] = []
    controller: list[tuple[int, bool | None, str, bool]] = []
    held_before = loss = False
    restored = None
    action = world.base.actions[0]

    for t in range(H):
        if t == scenario.fault.tick:
            held_before = goal in caps
            caps -= set(scenario.fault.remove)
            for index, name in enumerate(world.base.resources):
                inv[name] = max(0, inv[name] - scenario.fault.destroy[index])
            disabled |= set(scenario.fault.disable)
            loss = held_before and goal not in caps
        present = goal in caps
        truth_samples.append(present)
        sensor_samples.append(present if faithful_bits[t] else not present)
        delivered = sensor_samples[t - sensor.lag] if t >= sensor.lag else None
        choice = "repair" if delivered is False else "WAIT"
        accepted = True
        if choice != "WAIT":
            accepted = (action.name not in disabled and
                        action.requires <= caps and all(
                            inv[name] >= amount for name, amount in
                            zip(world.base.resources, action.consumes)))
            if accepted:
                caps.add(action.produces)
                for name, taken, produced in zip(
                    world.base.resources, action.consumes, action.yields
                ):
                    inv[name] = inv[name] - taken + produced
        controller.append((t, delivered, choice, accepted))
        if loss and restored is None and goal in caps and t >= scenario.fault.tick:
            restored = t + 1
    return Trace(scenario.name, scenario.fault.tick, faithful_bits,
                 tuple(truth_samples), tuple(sensor_samples),
                 tuple(controller), held_before, loss, restored,
                 goal in caps, F, _status(scenario.fault.tick, F, loss, restored, H))


def _trace_mass(scenario: Scenario, sensor: Sensor, trace: Trace) -> Fraction:
    weight = scenario.probability
    for true_state, faithful in zip(trace.true_samples, trace.sensor_bits):
        correct = sensor.sensitivity if true_state else sensor.specificity
        weight *= correct if faithful else (1 - correct)
    return weight


def exact_distribution(world: World, sensor: Sensor, *,
                       followup_until: int | None = None) -> dict:
    """Enumerate all exact sensor paths, cross-check separately written oracle.

    Return exact category masses; observed-case ratio is NOT a valid
    population estimate under potentially informative censoring.
    """
    if not world.scenarios:
        raise ValueError("empty world")
    masses = {name: Fraction() for name in STATUSES}
    loss_mass = Fraction()
    compared = 0
    nonzero = 0
    for case in world.scenarios:
        for bits in product((False, True), repeat=world.base.horizon):
            primary = execute(world, case, sensor, bits,
                              followup_until=followup_until)
            oracle = independent_replay(
                world, case, sensor, bits, followup_until=followup_until)
            if primary != oracle:
                raise AssertionError("independent B6 execution/label disagrees")
            compared += 1
            weight = _trace_mass(case, sensor, primary)
            if weight == 0:
                continue
            nonzero += 1
            masses[primary.status] += weight
            if primary.lost_at_fault:
                loss_mass += weight
    if sum(masses.values(), Fraction()) != 1:
        raise AssertionError("exact sensor-scenario probability mass not conserved")
    observed = masses[RESTORED] + masses[NOT_RESTORED]
    return {
        "profile": PROFILE,
        "status_mass": {key: str(value) for key, value in masses.items()},
        "privileged_true_loss_mass": str(loss_mass),
        "observed_determinate_loss_mass": str(observed),
        "observed_case_fraction_descriptive_only": (
            str(masses[RESTORED] / observed) if observed else None),
        "all_noise_scenario_pairs_crosschecked": compared,
        "nonzero_weight_paths": nonzero,
        "population_inference_validated": False,
        "independent_field_records": 0,
        "H1_confirmatory_samples": 0,
    }


def fixture() -> World:
    """Two synthetic scenarios, one kit, a repair action consuming one kit."""
    base = Model(
        initial=frozenset({"seed", "service"}),
        goals=frozenset({"service"}),
        resources=("kit",), stock=(1,),
        actions=(Action("repair", frozenset({"seed"}), "service",
                        (1,), (0,)),),
        horizon=3, fault=Fault(0, frozenset(), (0,)))
    return World(base, (
        Scenario("fault", Fraction(1, 2),
                 Fault(1, frozenset({"service"}), (0,))),
        Scenario("unaffected", Fraction(1, 2),
                 Fault(1, frozenset({"absent"}), (0,))),
    ))


def _canonical(data: object) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("utf-8")


def evidence_record(world: World, scenario: Scenario, sensor: Sensor,
                    bits: tuple[bool, ...], *,
                    followup_until: int | None = None) -> dict:
    """Hash-separated controller log / privileged ground-truth synthetic log.

    SELF-COMPUTED DIGESTS are reproducibility aids, not external attestations.
    Both source and actor are the local synthetic simulation.
    """
    trace = execute(world, scenario, sensor, bits,
                    followup_until=followup_until)
    public_log = [{"tick": t, "reported_goal": reported,
                   "command": command, "accepted": accepted}
                  for t, reported, command, accepted in trace.policy_log]
    evaluator_log = {
        "scenario": trace.scenario, "fault_tick": trace.fault_tick,
        "true_goal_precommand": list(trace.true_samples),
        "sensor_sampled": list(trace.collected),
        "held_before_fault": trace.held_before_fault,
        "actually_lost_at_fault": trace.lost_at_fault,
        "first_same_goal_regained_tick": trace.first_regained_tick,
        "held_at_horizon": trace.held_at_horizon,
        "followup_until": trace.followup_until,
        "label": trace.status,
    }
    payload = {
        "profile": PROFILE,
        "evidence_class": "SELF_GENERATED_SYNTHETIC_NOT_FIELD_EVIDENCE",
        "sensor_parameters": {"sensitivity": str(sensor.sensitivity),
                              "specificity": str(sensor.specificity),
                              "lag": sensor.lag},
        "public_controller_log": public_log,
        "privileged_evaluator_log": evaluator_log,
        "external_publisher_attested": False,
        "physical_incident_identity_verified": False,
        "H1_admissible": False,
    }
    return {
        "payload": payload,
        "payload_sha256": sha256(_canonical(payload)).hexdigest(),
        "digest_role": "LOCAL_REPRODUCIBILITY_ONLY",
    }


def verify_record(record: dict) -> bool:
    """Detect mutation against a previously trusted digest, NOT provenance."""
    try:
        return (set(record) == {"payload", "payload_sha256", "digest_role"}
                and record["digest_role"] == "LOCAL_REPRODUCIBILITY_ONLY"
                and record["payload"]["evidence_class"] ==
                    "SELF_GENERATED_SYNTHETIC_NOT_FIELD_EVIDENCE"
                and record["payload"]["external_publisher_attested"] is False
                and record["payload"]["physical_incident_identity_verified"] is False
                and record["payload"]["H1_admissible"] is False
                and record["payload_sha256"] ==
                    sha256(_canonical(record["payload"])).hexdigest())
    except (TypeError, KeyError, ValueError):
        return False


def audit() -> dict:
    world = fixture()
    perfect = Sensor(Fraction(1), Fraction(1))
    false_alarm = Sensor(Fraction(1, 2), Fraction(1))
    missed_loss = Sensor(Fraction(1), Fraction(1, 2))
    perfect_lag1 = Sensor(Fraction(1), Fraction(1), 1)
    perfect_lag2 = Sensor(Fraction(1), Fraction(1), 2)

    a = exact_distribution(world, perfect)
    b = exact_distribution(world, false_alarm)
    c = exact_distribution(world, missed_loss)
    d = exact_distribution(world, perfect_lag1)
    e = exact_distribution(world, perfect_lag2)
    early_stop = exact_distribution(world, perfect, followup_until=1)
    before_event = exact_distribution(world, perfect, followup_until=0)
    record = evidence_record(world, world.scenarios[0], perfect, (True,) * 3)

    if not (
        a["status_mass"][RESTORED] == "1/2" and
        a["status_mass"][NOT_AT_RISK] == "1/2" and
        b["status_mass"][RESTORED] == "1/4" and
        b["status_mass"][NOT_RESTORED] == "1/4" and
        c["status_mass"][RESTORED] == "3/8" and
        c["status_mass"][NOT_RESTORED] == "1/8" and
        d["status_mass"][RESTORED] == "1/2" and
        e["status_mass"][NOT_RESTORED] == "1/2" and
        early_stop["status_mass"][CENSORED] == "1/2" and
        before_event["status_mass"][UNKNOWN_RISK] == "1" and
        before_event["observed_case_fraction_descriptive_only"] is None and
        verify_record(record) and
        "scenario" not in record["payload"]["public_controller_log"][0]
    ):
        raise AssertionError("B6 noisy/delayed restoration controls changed")
    return {
        "gate": "B6",
        "profile": PROFILE,
        "result": "PASS_PROVISIONAL_SYNTHETIC_SENSOR_AND_EVIDENCE_CONFORMANCE",
        "perfect_status_mass": a["status_mass"],
        "false_alarm_status_mass": b["status_mass"],
        "missed_loss_status_mass": c["status_mass"],
        "lag1_status_mass": d["status_mass"],
        "lag2_status_mass": e["status_mass"],
        "censoring_cannot_be_scored_as_failure": True,
        "cutoff_before_fault_yields_unknown_risk": True,
        "two_independently_written_replays_agree": True,
        "self_hash_does_not_authenticate_publisher": True,
        "physical_field_episodes_admitted": 0,
        "sealed_test_families_generated": 0,
        "H1_preregistered": False,
        "H1_confirmatory_samples": 0,
        "classification": "DEVELOPER_SYNTHETIC_NOT_H1_NOT_CAUSAL_NOT_FIELD",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
