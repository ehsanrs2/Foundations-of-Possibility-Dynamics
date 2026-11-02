# R12 — Cross-grammar synthetic transfer and validity-readiness audit

**Status: DEV-ONLY independent-*structure* transfer rehearsal. NOT independent physical sampling, NOT external validity, NOT H1. 2026-11-02.**

## The scientific necessity

R11 reported a small mean expected Brier reduction (+0.000491912299) from a joint-preparedness feature on 27 TRAIN and 18 TUNE settings. **Those rows reused the same nine handmade base structures at different shock-time prior parameters.** That result could not test transfer between different dependency architectures.

R12 deliberately breaks the architectural overlap and adds a stronger conventional **exact full-known-model probability oracle**, while retaining R11's scientific limitations rather than hiding them. We do not run the prospectively sealed P1/H1 families or claim that a hand-designed architecture is an independently sampled engineering system.

## The three separate declared synthetic grammar families

All have one initially working service; two delivery channels; a physical R9 independent, alias or common-cause identity; stock 0/1/2 consumable kits; and one declared event at unknown tau in {2,3}. The event removes the service, disables delivery rules according to the fixed synthetic basic fault events, and destroys all remaining kits. The fully observable R7 policy sees only current capabilities, kit stock and disabled operations AFTER any realized event, and never the future tau/case ID. End horizon is tick 4.

- **TRAIN: direct channels.** Prepare A and B each in one tick with one kit; both routes can be ready by tau=2 when kits>=2.
- **TUNE family 1: shared-stage enabling.** A single zero-kit unlock action must first produce a shared arming capability before either kit-consuming preparation is allowed. Both routes cannot be ready by tau=2, but can by tau=3 with two kits.
- **TUNE family 2: asymmetric-stage enabling.** Channel A requires an extra zero-kit opening action and channel B is prepared directly. Again, both routes become possible only by tau=3 with two kits.

The tiny families are hand-designed using the **same synthetic channel hazard identities**; the two TUNE graphs are not real-world external domains. For each family, the nine mode×stock structural combinations are evaluated at three predeclared TRAIN early-fault priors or two predeclared TUNE priors. That yields **nine distinct TRAIN graph signatures (27 parameter settings)** and **18 distinct TUNE graph signatures (36 parameter settings)**. Graph hashes are computed from action topology, costs, stocks, full starting state and explicitly declared physical event mechanism/incidence; they are checked for no overlap without relying on family labels or future-case labels.

**Critical interpretation:** even the 27 different source/target graph signatures share hand-coded assumptions and related grammar patterns. They cannot be treated as 27 independent real systems or 36 independent statistical samples. No valid field-domain confidence interval, measured external loss risk or new general scientific theorem follows.

## Same pre-event information, target and conventional challenges

Five operations face the **same synthetic outcome**: the exact conditional probability of strict reacquisition of the previously held service after actual fault-caused loss, by the final tick, on **one fixed nonanticipative R7 policy trajectory**.

1. **raw:** ordinary features from preevent mode, kit stock, action/prerequisite counts, basic physical min event cut, static R1 and disclosed early/late prior.
2. **interaction:** identical raw features plus a simple conventional hand-specified interaction between having two kits, truly distinct channel events and the late-shock prior. This is a serious low-cost feature-engineering challenge, not a purposely weak constant predictor.
3. **state_dp:** raw plus the hypothesized *pre-event* probability-weighted joint-ready feature calculated by ordinary augmented-state state-set reachability. It uses NO future realized event.
4. **history:** same feature obtained with a completely independent chronological shared-stock exhaustive action-history solver. It should be identical to state_dp; agreement is a direct **negative novelty check**.
5. **known_model:** the strong full-model exact pre-event scenario-marginal policy probability p*(X), giving the Bayes lower bound for Brier risk under the stipulated known model. This is a **different, unfitted oracle with complete simulator knowledge**, not an equal-capacity learner or a viable inference method for unknown real dynamics.

The first four operations use the same fixed Ridge linear-probability model (penalty 1), training-only standardization, TRAIN prior settings and TUNE structural domains. The known-model operation predicts its exact stipulated outcome, without fitting. None of the five receives the realized future fault, tau or successful restoration outcome as a predictive input. Scoring is exact model-expected conditional Brier, not an average of independent observed field labels.

R12 does **NOT** assert that its raw feature summaries represent all baseline information a conventional augmented-state model could use. It is crucial that the known-model oracle is much stronger and can match p*(X), and that the joint-readiness feature itself is nothing more than conventional finite reachability.

## Process, sampling and code controls

Each operation is run from source through its whole end-to-end synthetic dataset generation, feature construction, learning (except the oracle), forecast and scoring **inside a fresh Linux worker**. All receive the same 10s parent wall limit, 10s RLIMIT_CPU and 256-MiB virtual-address-space limit. The hard limits are enforced, while measured wall-time, CPU and peak RSS may vary and are archived only in temporary CI artifacts; they are excluded from the stable scientific summary. The oracle and fitted models have different computation and parameter counts; identical upper bounds do not make their *actual work* equal.

[R12 source](../experiments/p1_r12_cross_grammar_transfer.py) also checks 54 independently reimplemented shared-stock prefix readiness judgments (27 model configurations × two possible shock times), as well as whole-history R7 chronological agreement for exact target generation. Structural non-overlap is checked at every predictor run, not just trusted as a report assertion.

Reproduce:

    python -m unittest tests.test_p1_r12_cross_grammar_transfer -v
    python -m experiments.p1_r12_cross_grammar_transfer --output r12_development_raw.json

The [R12 Actions workflow](../.github/workflows/r12-cross-grammar-dev.yml) keeps the complete development-only raw record, with a stable summary archived after successful validation. The prospective SEALED families (spatial_lattice, hierarchical_common_cause) remain unimplemented and **must not be generated during R12**.

## Interpretation and preregistration blockers

A positive raw-minus-joint-readiness Brier delta would establish only a finite-learner engineering benefit **in this contrived cross-grammar development transfer**. A negative delta would show this feature fails to provide additional accuracy here. Either outcome is a valid and reportable method-development finding. Since the same conventional state-DP computes it, no R12 outcome establishes scientific novelty.

A credible future external-validity program still needs independently sourced physical mechanism identities and common-cause exposures; device/incident-level failure and service-loss/recovery logs with preevent snapshots and intervention timestamps; prospectively locked real domain datasets and units; consent/licenses and leakage audit; estimated rather than invented hazard priors; realistic observation and policy data; stronger conventional predictors with genuinely comparable all-in resources and architecture capacity; uncertainty intervals clustered by genuinely independent physical systems; and sealed preregistration before confirmatory evaluation.

If no available dataset contains both actual goal loss and *same-policy service restoration*, one cannot label its generic uptime or damage outcome as strict restoration to manufacture validation.

R12 does not update the original R8 negative result, substitute a new feature into the P1 H1 protocol, or test whether Possibility Dynamics merits status as an independent scientific discipline. Keep Issues #3 and #8–#12 OPEN.


## Executed R12 developer cross-grammar comparison — 2026-11-02

The revised R12 [CI workflow run](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/actions/runs/41452753804) passed its 23 dedicated tests and all five separately resource-capped predictive workers. The six older R11 science files had been accidentally omitted from the first R12 branch tree; this was **corrected on the full R11 main tree** before the successful run, and regression preservation is checked. **576 independently coded complete R7 histories** agreed, along with **54 DP versus independent DFS prefix judgments**. The 27 training settings derive from nine direct-route graph signatures; 36 tuning settings derive from eighteen distinct staged-route graphs, with **zero graph-signature overlap**.

| Method on 36 synthetic TUNE *parameter settings* | Mean exact model-expected conditional Brier |
|---|---:|
| Conventional raw Ridge | **0.165914979088** |
| Raw + conventional stock/route/late-prior interaction | **0.165522792238** |
| Raw + standard augmented-state DP joint readiness | **0.164259405297** |
| Raw + equivalent independent history-based readiness | **0.164259405297** |
| Unfitted exact full-known-model conditional probability (ideal Bayes) | **0.162407769097** |

The synthetic *descriptive* mean difference raw minus augmented is **+0.001655573791**; relative to the conventional interaction comparator the difference is **+0.001263386941**. All feature and model comparisons are development-side only, not statistically inferential. The two ordinary algorithms produce identical forecast records. The known-model full-state baseline is still more accurate, as expected for an exact model-conditioned oracle.

**CRITICAL:** These are merely 27 *researcher-designed synthetic graph configurations* (9 training, 18 tuning), repeatedly reused at different known prior probabilities. Zero identical-graph hash overlap is a useful leakage control, **NOT proof of independent field engineering evidence** or independent population sampling. The TUNE grammars were expressly authored for this developer study. No natural failure rates, device IDs, deployable policy observations, external dataset or genuine confirmatory test has been supplied.

The [archived deterministic R12 JSON](R12-cross-grammar-results-20261102.json) preserves complete 36-row per-method forecast traces and the enforced resource caps. Per-worker nondeterministic CPU/wall/RSS measures remain in the [Actions raw artifact](https://github.com/ehsanrs2/Foundations-of-Possibility-Dynamics/actions/runs/41452753804) and are deliberately omitted from the reproducible archive.

**Decision:** advance to an independently sourced physical-data admission gate or explicit negative feasibility finding, not a declaration that the H1 hypothesis or a new science has been proven. The original R8 failure and the P1 draft protocol are unchanged.
