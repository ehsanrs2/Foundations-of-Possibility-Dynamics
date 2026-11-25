# R16-O / GOG-1b — bounded scaling and indexed relevance development

2026-11-25. Development protocol only; fixed before execution of this suite.
GOG-1a preserved exact goal sets and earliest times but goal-wise slicing
required more preprocessing, with no convincing latency advantage over
shared slicing. Test whether the work trade-off depends on goal overlap
rather than claim a generally faster or novel method.

## Prespecified comparison

24 deterministic factorial cases: 2/4/6 registered goals, disjoint or fully
shared construction prerequisites, stock 1/3, 0/2 irrelevant actions;
horizon 4, unit-time actions, durable positive capabilities, zero-effect
fault, one integer resource. Goal0 initially held in every factorial case
to ensure a nonempty ordinary reachable set. Other goals require construction.
Include the three existing resource-yield/time/stock controls from GOG-1a.
These are 27 developer fixtures, not independent samples or H1 populations.
The 14-action, 8-goal, 5-tick GOG-1a limits still apply. This is a bounded
scaling diagnostic, not asymptotic validation.

Five methods: unchanged state-layer search; shared and goal-wise scanning
slices; shared and goal-wise indexed slices. All sliced methods use exactly
the same existing Pareto pruning and search semantics. Indexed closure is
standard reverse dependency adjacency plus a worklist. Build the index once
per construction arm, retaining all resource producers and closing their
prerequisites, and count that cost. No cache shared across arms or cases.
The independent G2 BFS verifies both exact earliest dictionaries; identical
GOG counts alone are insufficient. No speed claim if a method fails or differs.

Three repetitions with deterministic shuffled method order (seed 161125).
Each method/repetition runs the identical suite in its own Linux process
with 12s CPU, 12s wall and 256 MiB virtual address space cap. Measure parent
wall, worker CPU, peak RSS, per-case query wall, and separate work counters
(search checks, dominance, slice inspections, index inspections, states).
No hard RSS cap; worker CPU starts after import. Compare medians, preserve
all raw runs, report both overlap classes. No significance claim or stable
speed ranking from three local repetitions. Count index construction and
repeated queries, no summing heterogeneous counters as if equally costly.
Exact reference work is outside timed methods. Incomplete coverage blocks
comparative summaries; retain failure records.

## Decision boundary

The GOG definition is a set difference over nested action permissions.
Indexing, dominance and dependency slicing are conventional algorithms.
A performance difference is a scoped engineering observation only.
If the advantage over shared indexed search is absent or depends on overlap,
record that trade-off; do not propose general algorithmic superiority.
A later study would require larger diverse externally reviewed domains,
strong standard planner/encoding baselines, and a prospective effect
criterion before timing. No H1 change or access to sealed families, no
physical/causal claim, and no reversal of the N1 pause.
