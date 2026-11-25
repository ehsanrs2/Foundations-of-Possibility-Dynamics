# R16-N / GOG-1a — exact goal-wise slicing development protocol

2026-11-25. **Developer protocol, not a novel algorithm claim or an H1 test.**
N1 paused R1 confirmatory preparation. GOG is a separate reachability query:
the number of individually reachable registered goals in E+ but not E0.
No shock, unit-time actions, durable capabilities, nonnegative integer stock,
consumption and yield vectors, optional wait, fixed goal vocabulary. Both arms
use the same input; E0 disables generative actions. Earliest goal ticks as
well as complete goal sets must agree. Joint attainment is a different query.

## Fixed comparison before execution

Compare four ordinary algorithmic designs, each solving both arms:
1. exact state-layer search (no dominance);
2. same-layer Pareto dominance on capability inclusion and componentwise stock;
3. shared backward AND/OR dependency slicing for all declared goals plus dominance;
4. goal-wise backward slicing plus dominance, union of exact individual results.

The fourth is a candidate engineering representation, **not a claim of a new
planning method**. A slice must retain every allowed action with any positive
resource yield, even if its output is irrelevant to the goal. Seed relevance
with the goal(s) and prerequisites of all such actions; iteratively close under
prerequisites of any action producing a relevant capability. Retain these
actions and project held capabilities onto relevance. This overapproximation
is deliberate: an apparently irrelevant action can replenish scarce resources.
An omitted action produces no relevant capability and yields nothing, so it
can be replaced by WAIT, never decreasing retained resources. With no shocks
or negative preconditions, same-tick dominance is sound by monotonicity.
Any projected path lifts to the original model with the same actions and
stock. Thus earliest individual goal ticks are preserved in this profile.
This is not a proof of general trace, controller, joint or physical equivalence.

Fixed development fixtures: independent branches with irrelevant producers
(0, 4, 8 distractors), shared prerequisite with 2 or 4 goals, resource-yield
bridge with tight time or stock, and mutually exclusive goals. Include alias,
renaming, changed goal vocabulary, time and resource negatives in tests.
Use deterministic bounded generated tiny cases separately for oracle checks.
None are sealed H1 families, sampled systems, or confirmatory holdouts.

## Work and measurement

Each method gets the identical fixed suite in a fresh Linux worker with
12 s wall, 12 s CPU, 256 MiB RLIMIT_AS; peak RSS recorded rather than capped.
Measure end-to-end wall, worker CPU and search effort: expanded states,
action checks, same-layer dominance checks, and retained actions per query.
Count repeated work across goal-wise calls and both arms. Include slicing,
input construction and result formatting in worker budget. No cache shared
between arms. Independent G2 oracle agreement required for suite results;
oracle cost separate from method timing. One process per method is only a
development rehearsal, not reliable latency inference. No partial winner
when a method fails, times out or differs in earliest goal dictionaries.
Do not assert that goal-wise search is always cheaper: shared dependencies
can make repeated slicing/search more expensive. Report negatives too.

## Exit

Exact equality on suite and bounded oracle tests; retain all output and
costs. Compare against both ordinary dominance and shared slicing, not only
unoptimized BFS. GOG-1b only if a promising scoped advantage merits a
prospective larger diverse benchmark with repeated randomized run order,
uncertainty, scaling, and comparison to standard planning algorithms.
Otherwise retain GOG as descriptive. No H1 feature swap, sealed access,
field inference, causal inference, or independent physical novelty claim.
