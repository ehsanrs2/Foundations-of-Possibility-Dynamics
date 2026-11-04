# Claims and evidence ledger — revision 0.2

| ID | Claim | Status | Grounding |
|---|---|---|---|
| C-001 | Reachability and viability are established mathematical fields | Prior work | Aubin 1991 / 2009 |
| C-002 | Correlated and higher-order novelty have quantitative research traditions | Prior work | Tria 2014; Di Bona 2025; Loreto et al. 2026 |
| C-003 | Empowerment quantifies control via action-perception information | Prior work | Klyubin et al. 2005 |
| C-004 | A constructed backup can preserve a pre-existing goal without new end goals | Illustrated in toy | Chapter 5, executable code and tests |
| C-005 | GBR gain improves held-out recovery prediction beyond robust baselines | **Unverified hypothesis** | Requires preregistered P1 |
| C-006 | GBR gain is mathematically novel | **Unverified; may be a reparameterization** | Formal equivalence audit |
| C-007 | Effects generalize across chemical, ecological and AI systems | **Unsupported aspiration** | Independent empirical replication required |
| C-008 | A new scientific discipline has been established | **Not claimed** | No supporting evidence |
| C-009 | Illustrative program output agrees with archived result | Software regression result | Seven independent assertions (not hypothesis tests) |

| C-010 | Optional construction cannot reduce existential reachable goals under nested transitions | Proven conditional statement | Appendix A.2 |
| C-011 | GBR gain is bounded by the number of baseline-reachable goals | Proven conditional statement | Appendix A.3 |
| C-012 | Finite construction dynamics admit augmented-state transition representation | Proven conditional statement | Appendix A.5 |

**Policy:** Do not promote definitions, examples or hypotheses into findings without independent evidence and explicit uncertainty analysis. Retain null results.

C-013: On 64 seeded tiny systems plus shock variants, two independent solver implementations agreed across 256 comparisons. **Status: software verification only**, not empirical scientific validation. See [G0](G0-verification.md).

C-014: LEAN engine validation of GBR is **not yet performed**. See [integration decision](../integrations/lean/README.md).

C-015: Under G1's explicit finite, nonconsuming, sequential production assumptions, two enumeration strategies agreed on all **192 tested plan-set comparisons** and their candidate GOG/GBR values. **Status: bounded software verification only.** See [G1 audit](G1-verification.md).

C-016: GBR gain implies recovery under arbitrary correlated shocks. **Refuted by shared-component counterexample and exposure sensitivity.** See [G1 audit](G1-verification.md) and Chapter 7.

C-017: G2 implements post-fault existential reachability with finite consumable stock and one in-run boundary event, and compares DFS history enumeration to layered state search. **Status: software verification only.** See [G2](G2-verification.md). No statement about probabilistic resilience, GBR predictive value or real systems follows.

C-018: G3 distinguishes existential post-fault availability, retention, strict restoration conditional on *actual* fault-caused loss, and joint target attainability. **Status: operational definitions and bounded software checks only.** See [G3 report](G3-verification.md).

C-019: Individual attainability of two goals implies attainable simultaneous possession under shared consumable inventory. **False:** the one-kit/two-goal counterexample has both goals independently attainable but no joint feasible execution. See [G3 report](G3-verification.md).

C-020: G3 verifies GBR predictive superiority or non-clairvoyant adaptive policy quality. **Not claimed**; perfect foresight is part of the present diagnostic model.

C-021: G4 distinguishes a shared non-clairvoyant pre-shock prefix from scenario-dependent post-shock continuation under fully observed discrete shocks. **Status: operational modeling definition; software test only.** See [G4](G4-verification.md).

C-022: In a constructed single-kit, two-scenario example, a non-clairvoyant prefix attains exact modeled success 1/2 while advance scenario knowledge attains 1. **Status: analytical toy counterexample, not empirical probability or H1 evidence.**

C-023: Optimal non-clairvoyant joint-success probability does not exceed a scenario-clairvoyant upper bound under identical dynamics and scenario distribution. **Status: elementary conditional inequality, proved by max-sum ≤ sum-max; not a new general law.**


C-024: For full pre-failure information X and exact deterministic GBR feature Z=f(X), an unrestricted optimal predictor cannot improve its best attainable expected loss by adding Z to X. **Status: proved conditional information-redundancy statement; familiar property, not a novel theorem.** See [novelty audit](novelty-audit-v0.3.md).

C-025: Raw G1 GBR gain can equal 1 after adding a purely aliased second rule for the same declared physical implementation, while a physical-ID-aware check yields 0. **Status: constructed executable counterexample, not a population result.** See [metric audit](gbr-metric-audit-v0.3.md).

C-026: The numerical value of raw GBR is robust to omitted shared physical failure causes, token splitting and zero-slack alternative routes. **Status: false in explicit constructed counterexamples.** See [metric audit](gbr-metric-audit-v0.3.md).

C-027: GBR improves held-out non-clairvoyant recovery prediction beyond equal-information and equal-computation standard methods. **Status: H1 OPEN; no confirmatory test completed**.

C-028: A strict declaration of physical mechanism IDs, failure-event incidence and protected-component rationales can prevent the previously demonstrated alias-score false positive *under the declared R1 ontology*. **Status: constructed bounded modeling diagnostic, not real-world identification.** See [Appendix C](../appendices/C-fault-event-ontology.md).

C-029: Static survival under independent basic-event indicators differs for one shared event and two independent events in an illustrative two-route system (1/2 vs 3/4 when event failure probabilities equal 1/2). **Status: exact combinatorial toy calculation; not observed reliability or dynamic restoration**.

C-030: Definitional reachability gain, predictive benefit under matched information, and intervention-caused resilience benefit are three **distinct estimands**; none may substitute for evidence of another. **Status: conceptual separation; H1 remains untested.** See [Appendix D](../appendices/D-predictive-estimands.md).


C-031: Physical event-disjoint individual routes are not sufficient to ensure that a single non-clairvoyant policy can prepare both given shared consumable resources and preparation deadlines. **Status: exact constructed counterexample, not an empirical result.** See [R2](R2-resource-policy-bridge.md).

C-032: Under the fixed four-event toy distribution, the same R1 pair score of 1 coexists with policy success 1/2 (one kit, two preparation ticks), 3/4 (two kits, two ticks) and 1/2 (two kits, one tick). **Status: deterministic bounded-model comparison, not H1 predictive validation**.


C-033: A v0.1 prospective H1 design has been documented with a proposed pre-shock prediction moment, strict loss-conditioned restoration endpoint, matched-information conventional baselines and provisional generator-family split. **Status: unregistered design specification only, not results**. See [P1 draft](P1-H1-study-design-v0.1.md).

C-034: The normal approximation table gives hypothetical independent-system sample sizes that vary strongly with unobserved paired-loss dispersion and desired minimum Brier improvement. **Status: conditional mathematical planning illustration; actual power and n remain undetermined**. See [planning code](../experiments/p1_sample_size_sensitivity.py).

C-035: A final preregistered P1 study with independently validated recovery outcomes and held-out superiority of GBR exists. **Status: false; not claimed.** The study's core measurement, operational policy, generators, sample-size rationale, and comparison constraints remain open.


C-036: In a bounded G2 one-tick execution kernel, one fixed non-anticipative policy can produce a history-consistent binary label for strict post-fault restoration after actual loss, treating non-loss as undefined. **Status: R3 software/methods verification only, not measured predictive performance.** See [R3](R3-nonanticipative-strict-restoration.md).

C-037: In one hand-constructed three-scenario R3 example, eligible loss mass is 2/3 and conditional restoration success equals 1/2. **Status: exact fixture arithmetic, not a sampled population or statistical H1 finding.**


C-038: Four explicitly synthetic *development-side* generator grammars, three assigned TRAIN and one assigned TUNE, can be instantiated reproducibly with family/index-specific SHA-256-derived seeds and checked under the R3 trace oracle. **Status: software reproducibility gate, not independently validated families or H1 evidence.** See [R4](R4-development-family-boundary.md).

C-039: The R4 development builder refuses the two reserved SEALED family identifiers before generating seeds or instances. **Status: software API guard only; not a general information-security boundary or a scientific guarantee of independence.**


C-040: Bounded R5 development-only pilot infrastructure produces system-clustered, policy-specific strict-restoration and resource-use records under three fixed R3 policy variants on four synthetic TRAIN/TUNE grammars. **Status: exploratory diagnostics and software verification, not confirmatory H1 evidence.** See [R5](R5-development-pilot.md).

C-041: A 3/4 per-system actual-loss eligibility mass in R5 reflects fault-case construction (three service-loss cases, one retained case, all weighted equally), not an inferred real-world failure risk. **Status: exact sampling-design fact, not empirical observation or independently estimated prevalence.**


C-042: An explicit per-system *synthetic* independent-basic-event hazard law can replace R5's fixed 3/4 designed eligibility fraction and correctly report systems with zero actual-loss risk as having undefined conditional restoration. **Status: R6 model and software control; not externally calibrated failure incidence.** See [R6](R6-variable-risk-and-exact-baseline.md).

C-043: For a completely known finite scenario law X, exact marginalization of one fixed non-anticipative policy's strict-restoration outcome supplies the optimal pre-shock conditional probability under Brier loss. The expected excess loss of a competing probability q is (q−p*)². **Status: standard conditional-expectation identity and model-based demonstration, not a new Possibility Dynamics theorem nor H1 validation.**

C-044: A distinct scientific theory of dynamic possibility has been established as necessary by the experiments. **Status: NOT established.** The motivating questions, competing prior fields and explicit possible falsifiers are in [scientific motivation and boundaries](scientific-motivation-and-boundaries.md).


C-045: Under a *perfect-observation* finite model, an ineffective scheduled fault vector cannot legitimately change a policy's event-detected signal if no held capability, stock, or known disabled-action status changes. **Status: R7 definition and bounded software counterexample; not real-sensor evidence.** See [R7](R7-silent-event-observation.md).

C-046: Changing the observation contract from automatic fault-boundary notification (R3/R6) to change-triggered detection (R7) can alter an executable policy's action history without changing true goal loss. **Status: constructed diagnostic; no predictive/causal H1 inference.**


C-047: One developer-only ridge learner can compare common-fault-cut/topology/inventory baselines against the same model plus the R1 scoped pair indicator under identical pre-shock synthetic inputs, keeping the ideal full-model reference separate. **Status: bounded method comparison, not H1 confirmation.** See [R8](R8-development-predictive-baselines.md).

C-048: Under the declared R6 synthetic common-upstream fault identity, a pair of separately feasible plans is not necessarily an independent physical backup; an R1 predictor with no across-system variation cannot add discriminating signal. **Status: R8 construct-validity diagnostic (pending actual run), not a general mathematical theorem.**

C-049: R8 TRAIN/TUNE comparison (72 training and 12 tuning developer systems) obtained exactly zero incremental expected Brier improvement from the currently defined R1 scoped backup-pair indicator because the indicator was 0 for all 84 models under the declared common-upstream synthetic failure scope. **Status: executed negative developer-only construct-validity/prediction result, not final H1 or universal theorem.** See [R8 archive](R8-development-summary-seed20261101.json).


C-050: In six predeclared artificial R9 physical-control fixtures, a fully declared fault ontology distinguishes two separate event-exposed physical channels from two names for the same channel and a common-cause event, while preserving standard event min-cut controls. **Status: constructed finite examples only, not empirical physical validation.** See [R9](R9-physical-identity-and-budget.md).

C-051: A valid *individually feasible* fault-disjoint pair indicator and minimum event cut can remain unchanged (R1=1, min cut=2) while actual R7 fixed-policy restoration after loss differs between a one-kit and a two-kit system, because only one of the two preparation operations can be executed. **Status: resource/time counterexample, not a new predictive superiority theorem.**

C-052: Under a bounded full-model scenario enumeration where each evaluated timeline tick is one abstract unit and every case actually loses service, the partial evaluated mass yields rigorous conditional restoration lower/upper bounds without a fabricated exact point estimate. **Status: restricted software budget contract; no matched CPU/wall-time/memory across independent algorithms.**


C-053: In the predeclared R9 synthetic mechanism worlds, an exploratory *jointly executable pre-event backup* indicator differs from static separately feasible R1 under shared stock and preparation deadline; this is exactly a conventional augmented-state reachability property independently checkable by exhaustive chronological histories. **Status: bounded constructed-software correctness, not novel theorem or predictive H1.** See [R10](R10-joint-executable-backup-and-process-caps.md).

C-054: R10 launches static R1, augmented-state joint readiness and conventional finite-model policy marginalization in separate Linux subprocesses with the same **enforced 5-s wall/5-s CPU/256-MiB RLIMIT_AS caps** and measures observed time and peak RSS. Their outputs and statistical target remain different, so this is not an equal-objective predictive or work-parity result; the full H1 computation-matching requirement remains unsatisfied. **Status: bounded process-infrastructure validation only.**


C-055: One finite constructed task with a fault at an ex-ante unknown tick 1 or 2 permits a nonanticipative R7 policy to be evaluated under the same early/late prior available to all pre-event predictors; exact same-history conditional restoration is scored through familiar model marginalization. **Status: synthetic development-only software contract, not empirical or novel-theory evidence.** See [R11](R11-unknown-time-matched-task-predictive-pilot.md).

C-056: R11 compares the same trained Ridge conditional expected-Brier objective among raw topology/resource/fault-cut features and two independently computed versions of a prior-weighted joint-preparedness feature, using the same Linux process ceilings. The conventional state DP and independent history algorithm calculate the **same reachability-derived feature**; no independent predictive information is created. **Status: repeated-structure development model comparison, not H1 or external validation.**


C-057: R12 tests generalization only **between hand-designed synthetic action-graph grammars** with non-overlapping semantic graph signatures, not among independently observed physical systems. The cross-grammar holdout has nine direct TRAIN and eighteen distinct staged TUNE configurations repeated across prior settings; no legitimate field-domain uncertainty estimate follows. **Status: development-only representation transfer design, not external H1 validation.** See [R12](R12-cross-grammar-external-validity-readiness.md).

C-058: R12 adds a conventional interaction Ridge predictor and a full known-dynamics pre-fault exact-restoration Bayes reference to the same conditional expected-Brier development comparison as raw and augmented-state readiness learners. The exact oracle has different information/computation advantages and is NOT an equal-capacity learned model. **Status: synthetic standard-baseline stress test; no independent scientific novelty, no empirical H1.**

C-059: R12 produced a **developer-only cross-grammar synthetic** score difference (raw Brier 0.165914979088; raw + conventional interaction 0.165522792238; raw + standard-state readiness 0.164259405297; full-known-model ideal 0.162407769097), on 9 direct TRAIN and 18 staged TUNE graph signatures, repeated in 27/36 prior settings with no graph overlap. This is **not independent physical-system transfer or confirmatory H1**, and ordinary state DP and exhaustive history produce the same forecasts. **Status: executed contrived-transfer software result, not externally validated prediction.** See [R12 exact archive](R12-cross-grammar-results-20261102.json).


C-060: At R13, publisher descriptions of six institutional public datasets (PNNL event-correlated county outages, ORNL EAGLE-I, DOE-417, LANL node failures, Backblaze drive stats and Google cluster traces) do NOT establish the entire same-service actual-loss/restoration/policy observation chain needed for the original H1. **Status: reviewed public metadata ONLY, 0 raw observed rows or independent physical systems admitted; absence of documentation does not prove source records cannot contain further evidence.** See [R13 public source register](R13-public-source-admission-manifest.json).

C-061: An R13 fail-closed prototype distinguishes a genuine pre-fault-active and fault-lost service from unaffected service, missing/censored follow-up, cross-service action joins, post-fault leakage and aggregate counts; passing a schema, even with a self-declared OBSERVED origin, DOES NOT certify physical provenance. **Status: synthetic software contract and real-data feasibility blockers only, NOT H1 evaluation.** See [R13 audit](R13-public-data-admission-and-evidence-gaps.md).
