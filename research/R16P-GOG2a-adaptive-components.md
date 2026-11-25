# R16-P / GOG-2a — exact dependency-component grouping

2026-11-25. Bounded developer protocol; no novel algorithm or H1 claim.
GOG-1b found a timing trade-off between shared and individual slicing,
but the compared graphs had different action counts. Here test a fixed
graph-based grouping rule, not a learned or outcome-tuned selector.

## Frozen design

24 factorial cases: 4 or 6 goals, singleton / interleaved pair / all-goal
dependency clusters, stock 1 or 3, 0 or 2 irrelevant producers. Horizon 4.
Every goal has a distinct unit-cost generative builder and ordinary serve
action; each serve requires its own bridge and either the seed (leader) or
its cluster leader's bridge. Every graph at fixed n/noise has exactly
2n+noise actions and identical per-action prerequisite arities and costs.
The first goal is initially held. Cluster leaders use the seed; groups
are interleaved in lexicographic goal order, not deliberately aligned with
the fixed pairs baseline. Changing prerequisites still changes difficulty
and resource requirements, so this is not a causal estimate of overlap alone.
Add the three resource controls and a chain-overlap case (28 cases total).
Existing GOG-1a bounds remain in force.

## Methods (same search kernel and exact task)

State layers, shared indexed slice, singleton indexed slice, fixed
lexicographic pairs with indexed closure, and adaptive components. The
adaptive rule builds one index per arm, computes each individual slice,
and joins goals iff their retained action sets intersect, taking transitive
connected components. Search each component on the union of its member
slices (no new closure or repeated index). Empty closures are singleton.
Resource producers may connect otherwise separate goals: conservative
grouping may be slower, not incorrect. Any goal partition is exact for
individual reachability: union of individually closed relevance sets is
closed, retains all yielding actions, and by GOG-1a lifting preserves all
earliest ticks for its goals. Does not preserve joint attainment or policies.
Standard dependency connected components are not themselves new.

Count index/slice action inspections, pair intersection tests, union
input action memberships, merge operations, search calls, action checks,
dominance checks and expanded states; counters are not equal-cost units.
All preparation included in timing. 3 repetitions, shuffled order
seed 161126, 12s CPU/wall and 256 MiB address-space cap per worker.
Measure whole-process wall, worker CPU, peak RSS, class query-wall medians.
Reference G2 BFS outside timed runs; compare full earliest dictionaries
in both arms and new goal sets. Every method/repetition must pass; missing
or failed runs block comparison. Record all outcomes including negatives.
No performance threshold or timing significance inference in this small
developer rehearsal. No new families from sealed P1. N1 pause unchanged.

Exit: exact results, work-accounting and negative tests, historical CI.
Only if grouping shows a meaningful scoped trade-off, consider externally
reviewed larger domains and strong conventional planning baselines. If
shared or singleton search wins, preserve that result. No post-hoc group
threshold tuning, no scientific or physical novelty claim.
