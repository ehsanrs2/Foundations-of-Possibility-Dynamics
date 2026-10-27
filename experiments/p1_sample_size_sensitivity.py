"""Illustrative P1 precision/power sensitivity, NOT a final sample-size choice.

Independent clustered system-level paired loss differences are ASSUMED normal
with hypothetical standard deviation. Assumes two-sided alpha and known SD.
Family distribution shifts, policy variance and SD estimation are omitted.
"""
from math import ceil
from statistics import NormalDist
import json


def illustrative_n(sd, difference, alpha=0.05, power=0.8):
    if not (0 < sd <= 1 and 0 < difference < 1 and 0 < alpha < 1
            and 0.5 < power < 1):
        raise ValueError("positive SD, improvement, alpha and power needed")
    z = NormalDist().inv_cdf(1-alpha/2) + NormalDist().inv_cdf(power)
    return ceil((z*sd/difference)**2)


def table():
    return {"classification":"HYPOTHETICAL_NORMAL_APPROX_NOT_A_SAMPLE_SIZE_COMMITMENT",
            "alpha":0.05, "power":0.8,
            "independent_unit":"system_not_shock_rollout",
            "rows":[{"hypothetical_paired_sd":sd,"minimum_Brier_improvement":effect,
                     "approx_independent_systems":illustrative_n(sd,effect)}
                    for sd in (0.05,0.1,0.15,0.2)
                    for effect in (0.01,0.02,0.03)]}


if __name__ == "__main__":
    print(json.dumps(table(),indent=2,sort_keys=True))
