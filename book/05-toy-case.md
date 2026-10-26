# Chapter 5 — Illustrative construction and its limits

**Evidence category: didactic toy example, not a scientific validation study.**

## 5.1 Scenario

Consider an initially reachable communication goal. The baseline route requires a wired transmitter. A separate construction sequence combines three initially held components to create an optical transmitter, which can serve the same goal. If the wired transmitter fails, the constructible route can potentially restore communication, *provided its own prerequisites survive and its construction fits post-failure time and budget constraints*.

Before the failure, both configurations may reach exactly one target. Consequently, a measure counting **new end goals** can equal zero. A suitable backup-path indicator can nevertheless equal one.

## 5.2 What follows logically?

The example distinguishes two **definitions**, not two empirically validated theories: increase in reachable goals is not identical to addition of an alternative way to reach an existing goal.

Under explicitly assumed, disjoint vulnerable dependencies, the alternative may survive an isolated component failure. It need not survive common-cause failures, resource exhaustion, unavailable construction time, or poorly specified component dependencies.

## 5.3 What does NOT follow?

No universal law, superiority over minimum-cut/flow metrics, general recovery benefit, or cross-domain validity follows from this case. It was manually designed to illustrate the distinction, so performance on it is not an unbiased test.

## 5.4 Next steps for reproducibility

Retain the original exploratory Python artifact and its JSON output **only after** auditing code, environment, checks, and exact provenance. The present book records the conceptual scenario without claiming an independently rerun experiment in the repository.

The experimental protocol requires fresh, randomly generated networks, fully specified fault models, leakage-resistant splits and uncertainty reporting.
