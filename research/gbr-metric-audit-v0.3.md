# Critical GBR metric audit v0.3 — Issue #9, related #12

**Disposition: RAW GBR IS REPRESENTATION- AND EXPOSURE-DEPENDENT. These are deterministic negative controls, not held-out resilience experiments.**

## 1. The existing definition remains unchanged

G1's binary backup predicate for goal g counts any **two distinct labeled plans** whose full causal supports have no common token **after projection to an analyst-selected exposure set F**. Its increment when optional construction is enabled is the current GBR gain.

The G1 model checks that F is nonempty; that guard does **not** establish that F is complete, that physical fault identities are correctly modeled, or that plan descriptions are observationally nonredundant. Agreement between G1's two plan enumerators cannot detect a flaw that both share in the metric definition.

## 2. Mandatory interpretation of F

F must mean **failure-event units** in a declared fault ontology, not arbitrary labels chosen after outcomes. Before running predictions, document:

- which physical assets, rule implementations, shared infrastructures and correlated failure mechanisms are modeled;
- which units are not exposed and the **scope of that protection assumption**;
- whether two different names refer to one physical unit or two physically independent failure units;
- failure timing, repair semantics, fault dependencies, and permitted shock distributions;
- sensitivity to plausible enlarged and contracted F, reported alongside the primary preregistered F.

A nonempty F by itself is insufficient. If a support has no exposed units, that pathway may be *invulnerable within the modeled scope*, but this says nothing about real faults outside it.

## 3. Executable negative controls

Run \`python -m experiments.gbr_review_counterexamples\` and \`python -m unittest discover -s tests -v\`. The test suite includes 12 targeted checks. Recorded values below are exact expected properties of constructed examples—not observations of real systems.

| Deliberate test | Original G1 outcome | Audit interpretation |
|---|---|---|
| Two differently named rules are aliases of the **same declared physical route**; one is marked generative | GBR gain **1**, GOG **0** | **False physical backup** if alias IDs are incorrectly treated as independently vulnerable |
| Map both rule tokens to the **same declared physical ID** | Canonical physical-support pair **0**; min failure hitting set **1** | The duplicate operational description no longer creates a second physically distinct backup |
| Add the shared source to F in the alias case | Raw GBR gain **0** | Scope matters, even without correcting rule identity |
| Mathematically evaluate the pair predicate with F empty | Pair indicator **1** for any two labeled plans | Vacuous disjointness; G1 construction correctly rejects empty F but incomplete F is still possible |
| Give two source labels to one **declared shared physical supply** | Raw gain **1**, physical-ID-aware pair **0** | A refinement can invent apparent independence unless failures of the shared source are coupled |
| Original wired/optical alarm; then add common power to F | Gain **1 → 0** | Excluding a true common cause may entirely reverse the indicator |
| Alternative path takes the **entire horizon** | Gain **1**, backup slack **0 ticks** | Binary backup ignores near-deadline fragility; shorten horizon by one and gain becomes **0** |

**Important semantic caveat:** two physically separate machines implementing identical rules should **not** be merged. The external physical-ID map is an *assumption requiring evidence*, not an automatic synonym detector. The split-source example is comparable only **conditional on the externally declared single-supply semantics** and coupled fault events; under independent source failures it is a genuinely different system.

## 4. Diagnostic baseline, not a repair of GBR

The audit's \`physical_signatures\` projects causal support tokens into **externally assigned physical identities** and deduplicates exact matches of (goal, duration, cost, complete projected causal support, projected exposure). The associated \`canonical_backup\` applies the pair predicate after this limited projection. It is **not** a universally correct definition of policy or semantic equivalence.

The tiny \`min_failure_hitting_set\` is a simple combinatorial structural baseline: fewest modeled failure IDs that hit *every* feasible path. It returns \`None\` if no failure set inside F can eliminate a plan, and is capped at 12 IDs because enumeration is exponential. It is **not** a weighted probabilistic reliability model, a general dynamic min-cut solver or a runtime scalability result.

The example with two rule aliases yields raw hitting-set size 2 but size 1 after declaring the shared physical identity. This illustrates why the **unit of failure** must be fixed independently of the representation.

## 5. Other essential baselines

- **Disjoint path counts / maximal support packing** rather than a saturated binary indicator;
- minimum hitting set, static/dynamic minimum cut and appropriate fault-tree methods;
- reliability under stated independent *and correlated* component failures;
- cost, activation delay, backup horizon slack, resource consumption and joint feasibility;
- equal-information policies using full augmented state, with explicit compute/memory accounting.

No one baseline is universally superior; select baselines consistent with AND requirements, fault semantics, information sets and mission deadlines. A count of supports is not a substitute for a calibrated restoration probability.

## 6. Outcome and status

**Established negative result in this version:** the current raw GBR pair indicator can change with alias encoding or the chosen exposure vocabulary and can report a physical backup that does not exist under a declared common physical identity. The vulnerability is **demonstrated in constructed finite cases**, not quantified in a held-out population.

**Remaining for #9/#12:** rigorously define physically meaningful plan/policy equivalence for consuming inventory and stochastic execution; prove or specify invariance on an admitted class of representations; declare a preregistered shock ontology; evaluate stability across scale and multiple independent generator families; time/memory/timeout benchmarking; compare independent-failure and common-cause calibrated baselines. **Issues #9 and #12 must stay open.**
