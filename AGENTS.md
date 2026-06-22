<!-- ARIS-CODEX:BEGIN -->
## ARIS Codex Skill Scope
ARIS Codex packages installed in this project: skills-codex
Managed entries: 80
Manifest: `.aris/installed-skills-codex.txt`
ARIS repo root: `/root/aris_repo`
Project skill path: `.agents/skills/<skill-name>`
For ARIS Codex workflows, prefer the project-local skills under `.agents/skills/`.
When a skill needs ARIS helper scripts, resolve the repo root from the manifest or set it explicitly:
`ARIS_REPO=$(awk -F'\t' '$1=="repo_root"{print $2; exit}' "/root/autodl-tmp/IDEA-CREATOR/.aris/installed-skills-codex.txt")`
Do not edit or delete symlinked skills in place; update upstream or rerun:
`bash /root/aris_repo/tools/install_aris_codex.sh "/root/autodl-tmp/IDEA-CREATOR" --reconcile`
For copied Codex installs, use:
`bash /root/aris_repo/tools/smart_update_codex.sh --project "/root/autodl-tmp/IDEA-CREATOR"`
<!-- ARIS-CODEX:END -->

## Project Handoff Notes

Last reviewed: 2026-06-22.

Latest task sync:
- 2026-06-22: Completed RSP-GCL M2-M4 gates after the role-signature idea
  discovery pass. Chameleon 10-split RSP training is positive but conditional:
  role-fused `0.573684 +/- 0.026265`, no NaN/collapse; validation selection
  chooses `graph_raw_role` in 10/10 splits and reaches
  `0.574781 +/- 0.023321`. Texas/Wisconsin do not support the role branch:
  raw `0.829730` / `0.839216` beats role-fused `0.727027` / `0.774510`;
  validation-selected gates mostly fall back to raw (`0.827027` / `0.827451`)
  but do not create broad gains. Direct novelty check found strong overlap:
  GALE already centers node equivalence in graph SSL, WLGCL directly uses WL
  structural similarity for GCL positives, and SPGCL shows positive-sample GCL
  is crowded in 2026. Decision: downgrade RSP-GCL to
  `DIAGNOSTIC_ONLY_AFTER_GATE`; do not run external baselines or large graphs
  for RSP. Next action: restart idea discovery with a different mechanism
  family. Report saved at `refine-logs/RSP_M2_M4_RESULTS_20260622.md`.
- 2026-06-22: 重新使用 idea-discovery 宽搜索后，当前 ACTIVE 候选切换为
  RSP-GCL（Role-Signature Positive Graph Contrastive Learning）。新增
  `evaluate_role_position_anchor.py`、`train_rsp_transductive.py`，并在
  `reproduce_dcgcl.py` 中加入 `--variants rsp`。核心机制是用无标签
  role statistics、WL-hash neighborhood signature、landmark diffusion
  signature 构造非局部结构角色等价正样本。Chameleon 10-split
  zero-training proxy 很强：`graph_raw_role_wl_landmark=0.585965`，
  高于 `graph_raw=0.496711` 和此前 DCA 最好 `0.505044`；训练版
  RSP-GCL split-0 role-fused `0.596491`，无 NaN/collapse。但
  Texas/Wisconsin 仍是 raw-dominant，full role proxy `0.678378` /
  `0.719608` 明显低于 raw `0.829730` / `0.839216`。当前状态是
  `ACTIVE_WITH_SCOPE_LIMIT`，不是 paper-ready；下一步必须跑
  Chameleon 10-split training、加入 role gate 保护 Texas/Wisconsin，
  并直接查新 WL/role/landmark-positive GCL。报告见
  `refine-logs/RSP_ROLE_SIGNATURE_RESULTS_20260622.md` 和
  `idea-stage/POST_CIG_ROLE_SIGNATURE_IDEA_DISCOVERY_20260622.md`。
- 2026-06-22: Tested the CIG/CLEAR counterfactual edge-influence family before
  implementing a training objective. Added
  `evaluate_counterfactual_edges.py` and evaluated frozen RFA checkpoints under
  raw/graph/disagreement/align edge masks. Split-0 showed only a local
  Wisconsin positive (`0.843137` vs raw `0.823529`); Cora/Chameleon had no
  useful signal and Texas stayed below raw. The 10-split check invalidated the
  route: Wisconsin best fixed mask `0.823529` and validation-selected `0.827451`
  both below raw `0.839216`; Texas best fixed `0.794595` and validation-selected
  `0.805405` both below raw `0.829730`. Decision: stop CIG/CLEAR; do not
  implement a training objective or expand to external baselines. Report saved
  at `refine-logs/CIG_EDGE_COUNTERFACTUAL_RESULTS_20260622.md`.
- 2026-06-22: Implemented and tested VST-GCL, the speculative transport route
  selected after DCA novelty failed. Added `train_vst_transductive.py` and
  `reproduce_dcgcl.py --variants vst`. M0 smoke on Cora/Chameleon passed
  engineering checks with no NaN/collapse. M1 200-epoch split-0 gate failed:
  Cora fused `0.814490` (below prior anchor controls), Chameleon fused
  `0.469298` (below graph_raw/DCA controls), Texas fused `0.729730` vs raw
  `0.810811`, and Wisconsin fused `0.803922` vs raw `0.823529`. Low-auxiliary
  ablation also failed (`Cora 0.810337`, `Chameleon 0.467105`). Decision: stop
  VST-GCL and restart wide idea discovery; do not tune DCA/VST or expand them
  to external baselines. Report saved at
  `refine-logs/VST_M0_M1_RESULTS_20260622.md`.
- 2026-06-22: Ran the DCA novelty/method gate after its edge-positive local
  results. Verdict: DCA is `DIAGNOSTIC_ONLY_AFTER_NOVELTY_FAIL`, score about
  `3/10`. Closest priors already cover the core pieces: ASPECT and LOHA cover
  low/high spectral GCL, HLCL covers heterophily graph filters, FC-GSSL covers
  frequency-aware GSSL, Less is More and FB-GCL cover graph/feature
  complementary fusion, and GCL-GroW/GWGCL cover whitening rescue directions.
  Quick rescue probes also failed to create a new main route: semantic kNN
  anchors only gave small Cora/CiteSeer signal and did not beat key
  Chameleon/Texas/Wisconsin controls; ZCA/whitening timed out in the quick
  loop and is not novel enough. Current status: no `READY_TO_REFINE` method.
  Next eligible candidate is VST-GCL, a speculative sparse local transport
  target between topology-neighborhood mass and raw-feature semantic mass.
  Run only a split-0 proxy before any 10-split or external baseline expansion.
  Reports: `refine-logs/DCA_NOVELTY_CHECK_20260622.md` and
  `idea-stage/POST_DCA_IDEA_DISCOVERY_20260622.md`.
- 2026-06-22: Continued idea discovery after the FBA training failure. Tested
  SBN-GCL (semantic raw-feature kNN positives plus low-similarity edge boundary
  negatives) and stopped it after split-0 failure: Cora fused `0.820951`, but
  Chameleon `0.462719`, Texas `0.729730`, and Wisconsin `0.784314` remained
  below the relevant controls; Chameleon ablations also failed. The strongest
  current empirical lead is DCA-GCL (Deferred Complementary Anchor GCL): keep
  raw/high/low deterministic anchors outside training and fuse them after the
  graph encoder is learned. Chameleon 10-split improved from graph_raw
  `0.496711` and one-anchor FBA `0.500219` to DCA `0.505044`; Cora/CiteSeer
  improved over graph_raw, while Texas/Wisconsin remain raw-dominant. Decision:
  DCA is `EMPIRICAL_EDGE_POSITIVE_NEEDS_NOVELTY_REVIEW`, not final paper-ready.
  Next action is strict novelty/method review against ASPECT, FC-GSSL, SPGCL,
  Less is More, HLCL/GREET/SIGNA, and simple graph-feature fusion; do not run
  external baselines or large graphs yet. Report saved at
  `refine-logs/SBN_DCA_RESULTS_20260622_1335.md`.
- 2026-06-22: Completed the post-ORFA FBA focused gate. ORFA-GCL was stable
  but failed as a main route: Chameleon 1000 split-0 only `0.484649`, Texas
  below raw, Wisconsin tied raw. BiFilter-BGRL was also implemented and failed
  split-0 (`Cora 0.702815`, `Chameleon 0.458333`, `Texas 0.729730`,
  `Wisconsin 0.666667`). FBA-GCL was then implemented in two forms:
  post-hoc evaluator `evaluate_filterbank_anchor.py` and trainable
  `train_fba_transductive.py`. Post-hoc FBA has a narrow Chameleon 10-split
  signal (`graph+raw 0.496711`, `graph+raw+0.5H1 0.500219`,
  `graph+raw+P4 0.500219`), but the training auxiliary failed the strict
  Chameleon 10-split gate: FBA-high1 train `0.487061` vs same-run graph_raw
  `0.493202`, with no NaN/collapse. Decision: current FBA is a diagnostic /
  post-hoc filterbank baseline, not a final paper method. Next action should
  be method-level review or fresh idea discovery, not external baselines or
  large-graph expansion. Reports saved at `refine-logs/FBA_M0_M2_RESULTS_20260622_1115.md`
  and `refine-logs/ORFA_BIFILTER_FBA_RESULTS_20260622_0935.md`.
- 2026-06-22: Completed a new idea-discovery pass after FTDR/CFR. CFR-BGRL
  (learned graph channel + learned feature channel) was stable but failed
  split-0: Cora `0.8002` vs BGRL `0.8090`, Chameleon `0.4079` vs `0.4232`,
  Texas tied `0.6486`, Wisconsin regressed to `0.5294`. Raw-feature probes
  showed strong signal on Texas/Wisconsin, so RFA-BGRL was implemented:
  BGRL graph branch plus protected raw-feature anchor. RFA is stable and very
  strong against prior GCL-style controls on Texas/Wisconsin 10-split
  (`0.7622` / `0.8098`), but raw-only is still stronger (`0.8297` /
  `0.8392`), so gains are raw-retention driven. Chameleon 1000-epoch 10-split
  reaches `0.4928`, still below the strict prior control around `0.5004`.
  A zero-training ORFA-style post-hoc graph residualization check only moved
  Chameleon 1000-epoch validation-selected scale to about `0.4943`, so ORFA
  must be trained as a complementary-residual objective rather than applied as
  a representation trick.
  Decision: keep RFA as a required diagnostic baseline, do not claim it as the
  final paper method; next method should be ORFA-GCL, a protected raw anchor
  plus complementary graph residual. Reports saved at
  `idea-stage/POST_FTDR_CFR_RFA_IDEA_DISCOVERY_20260622_0610.md` and
  `refine-logs/CFR_RFA_M0_M2_RESULTS_20260622_0610.md`.
- 2026-06-22: Implemented FTDR-BGRL as the post-DCGCL lightweight pilot:
  `train_ftdr_transductive.py` routes each node's bootstrap target between a
  topology teacher and a feature-only teacher by feature-topology disagreement.
  Smoke passed with no NaN/collapse. M1 split-0 was stable but not positive:
  Cora best `0.8076` vs BGRL `0.8090`, Chameleon `0.4035` vs `0.4232`,
  Texas `0.6486` vs `0.6486`, Wisconsin `0.5882` vs `0.5882`. Decision: do
  not run FTDR 10-split; stop simple latent-target/teacher-routing variants
  and move the next idea search to a different mechanism family. Report saved
  at `refine-logs/FTDR_M0_M1_RESULTS_20260622_0405.md`.
- 2026-06-22: Re-entered idea discovery after DCGCL failed the 10-split gate.
  New lightweight shortlist selected FTDR-BGRL (Feature-Topology
  Disagreement-Routed Bootstrap) as the next minimal pilot. It avoids SRLP's
  residual target assumption and DCGCL's global prototype positives by routing
  each node's bootstrap target between a topology teacher and a feature-only
  teacher using label-free teacher disagreement, with explicit BGRL fallback
  when feature/topology agree. Report saved at
  `idea-stage/POST_DCGCL_IDEA_DISCOVERY_20260622_0345.md`. Next action:
  implement `target_mode=ftdr_bgrl` inside `baselines/BGRL`, run 5-epoch smoke,
  then a split-0 M1 on Cora/Chameleon/Texas/Wisconsin before any 10-split
  expansion.
- 2026-06-22: Continued DCGCL after the initial V0 failure. Implemented V1
  with separate feature/topology prototype banks, greedy prototype alignment,
  and a high-confidence agreement mask; implemented V2 with label-free
  `prototype_alignment` fallback to BGRL. Split-0 showed partial promise, but
  V1 10-split internal gate failed as a main method: Chameleon DCGCL mean
  `0.40658` vs best target-family control `0.50044` (0/0/10), Texas `0.58649`
  vs `0.61351` (3/0/7), Wisconsin `0.60392` vs `0.55490` (8/1/1). All 30 rows
  completed with no NaN/collapse. Decision: stop DCGCL as a main route; keep
  Wisconsin as a diagnostic observation only. Next action should be fresh idea
  discovery constrained by both SRLP and DCGCL failures. Saved report at
  `refine-logs/DCGCL_V1_10SPLIT_RESULTS_20260622_0336.md`.
- 2026-06-22: Implemented and initially tested DCGCL V0 inside the nested
  `baselines/BGRL` checkout after the fresh idea-discovery pass. Added
  `bgrl/dcgcl_utils.py`, `diagnose_dcgcl_prototypes.py`,
  `train_dcgcl_transductive.py`, and `reproduce_dcgcl.py`; fixed the runner's
  Windows child-output decoding to UTF-8. M0 prototype diagnostics and M1 smoke
  passed from an engineering standpoint, with no NaN/collapse. M2 split-0 gate
  did not pass: Cora DCGCL `test@best=0.7790` vs BGRL `0.8090`, Chameleon
  `0.4276` vs best control `0.4232` (small positive), Texas `0.6216` vs
  `0.6486`, Wisconsin `0.5882` vs `0.5882`. Decision: do not run 10-split or
  external strong-baseline expansion for DCGCL V0. Next action should be method
  revision, especially separate aligned feature/topology prototype banks plus a
  stricter high-confidence agreement mask. Saved report at
  `refine-logs/DCGCL_M0_M2_RESULTS_20260622_0227.md`.
- 2026-06-22: Re-ran `/idea-discovery` for a fresh graph contrastive
  learning method after SRLP main-method invalidation. Selected DCGCL
  (Disagreement-Calibrated Prototype Graph Contrastive Learning) as the new
  paper-only active route, not yet GPU-validated. DCGCL uses a feature-only
  teacher and a propagation-view teacher to produce soft prototype assignments:
  agreement nodes form reliable global positives, while disagreement nodes keep
  feature/topology semantics through dual heads and a gate. This directly
  targets the SRLP failure mode that shortcut-resistant residuals were not
  necessarily task-relevant. Saved artifacts at `idea-stage/IDEA_REPORT.md`,
  `idea-stage/IDEA_CANDIDATES.md`, `refine-logs/FINAL_PROPOSAL.md`,
  `refine-logs/EXPERIMENT_PLAN.md`, `refine-logs/EXPERIMENT_TRACKER.md`,
  `refine-logs/PIPELINE_SUMMARY.md`, and `research-wiki/ideas/dcgcl.md`.
  Next action: implement only M0/M1/M2 pilot diagnostics and split-0 checks;
  do not run 10-split expansion until DCGCL passes the local controls plus
  no-dual/no-gate ablations.
- 2026-06-22: Ran a Codex subagent result-to-claim gate for SRLP /
  SRLP-Aux / Adaptive-Aux. Verdict: `claim_supported=no`, confidence high.
  Supported evidence is limited to leakage reduction and target-decomposition
  diagnostics; the main method claim is invalidated by M2 split-0, SRLP-Aux
  10-split, and Adaptive-Aux 200-epoch fair pilot results. Next action should be
  negative findings + fresh idea discovery, not more SRLP baselines or large
  graphs. Saved verdict at `refine-logs/SRLP_RESULT_TO_CLAIM.md` and
  `findings.md`.
- 2026-06-22: Completed the adaptive-gate follow-up after the SRLP-Aux
  10-split failure. Added `target_mode=srlp_adaptive_aux` inside the nested
  BGRL checkout and ran a 5-epoch smoke plus 200-epoch split-0 pilot on
  Chameleon/Texas/Wisconsin with matching 200-epoch FullLatent/ZPZ/SRLP-Aux
  controls. Gate diagnostics partially worked, but pilot evidence is not enough:
  Chameleon adaptive `test@best=0.4145` vs best non-adaptive `0.4232`, Texas
  `0.6216` vs `0.6486`, Wisconsin `0.6078` vs `0.5882`. No NaN/collapse.
  Decision: stop expanding SRLP/Adaptive-Aux as a main method; at most keep the
  line as a target-decomposition or leakage-diagnostic observation. Results are
  in `refine-logs/SRLP_ADAPTIVE_GATE_PILOT.md`.
- 2026-06-22: Completed strict method-only review of the SRLP label-alignment
  diagnostics after the 10-split target-family ablation. Verdict: RETHINK, not
  KILL. The unified rank-1 residual assumption is no longer defensible:
  Chameleon needs context-projection retention, Texas/Wisconsin need
  multi-direction residual only when label-free diagnostics support it, and
  Actor is too weak to drive design. Saved review at
  `refine-logs/SRLP_LABEL_ALIGNMENT_METHOD_REVIEW_20260622.md`. Next minimal
  step is a pure label-free gate diagnostic, followed only if it passes by a
  3-run Chameleon/Texas/Wisconsin split-0 pilot; do not expand external
  baselines or large graphs.
- 2026-06-22: Completed SRLP-Aux 10-split target-family internal ablation on
  Chameleon/Texas/Wisconsin/Actor using Geom-GCN official splits 0-9. All 120
  rows completed with no NaN/collapse and max skipped ratio 0.05405. Mean
  Test@Best: Chameleon FullLatent 0.49167, ZPZ 0.44342, SRLP-Aux 0.49759
  (small positive); Texas FullLatent 0.58919, ZPZ 0.61081, SRLP-Aux 0.58919
  (negative); Wisconsin FullLatent 0.54118, ZPZ 0.53725, SRLP-Aux 0.53725
  (negative/tied); Actor FullLatent 0.27592, ZPZ 0.27355, SRLP-Aux 0.27592
  (tied). Decision: do not expand to external strong baselines or large graphs;
  return to method-level target redesign or downgrade SRLP-Aux to an auxiliary
  diagnostic claim.
- 2026-06-21: Diagnosed why the active SRLP-Aux 10-split target-family GPU
  training felt slow. Live profile showed the current child process running
  `actor/full_latent_iso` split 3 with only about 2-14% RTX 4060 utilization,
  about 3GB GPU memory, near-zero disk I/O, and about one CPU core saturated.
  Root cause is not GPU overload: the small transductive graph workload is
  serialized by `reproduce_srlp.py`, CPU thread caps are forced to 1 for
  reproducibility, logs are buffered by `subprocess.run(stdout=PIPE)`, and
  per-epoch graph masking/TensorBoard plus periodic CPU linear evaluation add
  overhead. Diagnosis saved at
  `profile_output/current_gpu_training_slow_20260621.md`; training code was
  left unchanged while the run continued.
- 2026-06-21: Implemented the post-review SRLP-Aux revision and ran the 5-run
  Go/Kill gate. SRLP-Aux uses a single-head mixed target
  `normalize(z_hat + lambda_t * w * r_hat)` with `lambda_max=0.1`, `tau=0.15`,
  and 10% warmup. Smoke passed. Gate results passed: SRLP-Aux improved over
  old SRLP hard on Chameleon/Texas/Wisconsin/Actor/CiteSeer (5/5), reached or
  matched the strongest target-family result on Chameleon and Texas (2/4
  heterophily gate), and had no NaN/collapse. Current canonical proposal is
  `refine-logs/FINAL_PROPOSAL.md` for SRLP-Aux. Next step: limited 10-split
  target-family internal ablation; keep external strong-baseline paper table
  paused.
- 2026-06-21: Completed a method-only strict review of SRLP after the M2
  pilot results. Verdict: DOWNGRADE. Hard isolation does reduce leakage, but
  the residual-only target is internally misaligned with the reachable online
  signal and loses task-relevant latent information. Recommended revision is to
  demote SRLP from a standalone objective to an energy-gated residual auxiliary
  on top of a FullLatent primary objective, with a 3-5 run Go/Kill gate before
  abandoning the standalone SRLP claim.
- 2026-06-21: Continued the SRLP experiment bridge through M2. Cora/CiteSeer
  200-epoch pilots completed, Chameleon was extended to 1000 epochs, and
  Cornell/Texas/Wisconsin/Actor split-0 1000-epoch target-family ablations
  completed sequentially on the 4060. Engineering and leakage checks pass, but
  the method-effect criterion does not: SRLP has 0/5 clear wins over the
  strongest target-family ablation across Cornell/Texas/Wisconsin/Actor/
  Chameleon split 0, with Cornell only tied. Pause 10 split and external
  strong-baseline expansion until the residual target design is revised.
- 2026-06-21: User preference update: experiment progress and results should
  be reported in Chinese by default, with numeric metrics shown in tables when
  possible and a clear pass/fail/next-step interpretation after each batch.
- 2026-06-21: Implemented the SRLP 4060 small-graph experiment bridge inside
  the nested `baselines/BGRL` checkout. Added SRLP utilities, training runner,
  sequential reproducer, leakage probe, Cora/CiteSeer fixed split files, and
  JSON/CSV output protocol. Codex subagent review verdict was PASS_WITH_FIXES;
  fixes applied include strict hard-isolation self-loop control, expanded CSV
  traceability fields, CiteSeer split pre-generation, and dataset path casing.
  M0 Cora/Chameleon smoke passed; Chameleon 200-epoch target-family pilot is
  positive for SRLP against FullLatent/ZPZ/NoIso but still below BGRL.
- 2026-06-21: Organized the SRLP idea-discovery and refinement artifacts for
  Git tracking and pushed them to `origin/master`. Commit scope includes the
  latest SRLP idea report, reviewer/refinement logs, formula-tightened final
  proposal, research-wiki notes, manifest entries, and this handoff update.
- 2026-06-21: Tightened SRLP final formulas in
  `refine-logs/FINAL_PROPOSAL.md`: added teacher-side stop-gradient, normalized
  context direction, `epsilon`/`T_valid`/`skipped_ratio`, explicit
  `A_online` target-incident-edge masking, online context normalization, and
  made `L_var` a collapse-only fallback rather than part of the main method.
- 2026-06-21: Completed a first-round senior-reviewer method audit of
  `refine-logs/round-0-initial-proposal.md` for SRLP-GCL. Verdict: REVISE,
  weighted score 5.95/10. Main required revisions are to make the residual
  target explicitly context-unpredictable rather than merely `Z - alpha PZ`,
  strengthen target leakage control, and demote conditional InfoNCE from the
  first implementation. Review saved at
  `refine-logs/round-0-method-review.md`.
- 2026-06-21: Completed a second-round review of
  `refine-logs/round-1-refinement.md`. Verdict: READY for pilot, weighted
  score 7.35/10. The context-projected residual and target-isolated online
  encoding are sufficient for a small BGRL-based pilot; remaining risk is
  empirical predictability of the residual after hard isolation. Review saved
  at `refine-logs/round-1-method-review.md`.

Communication preference:
- Use Chinese when explaining research ideas, novelty, experiment status, and
  implementation decisions. Avoid unnecessary English terminology; when a
  technical term, paper title, file name, or command must stay in English,
  explain it in Chinese immediately.
- For literature search and novelty checks, prioritize recent papers from the
  last two years and always check the most recent 6 months. Only use older
  papers when they are foundational or uniquely representative.
- For experiment reporting, describe each run batch in Chinese. Prefer compact
  tables for metrics such as validation accuracy, test accuracy, prediction
  cosine, residual norm, skipped ratio, effective rank, probe cosine, and MSE;
  after the table, add a short interpretation: passed / failed / inconclusive
  and the recommended next action.

This workspace is a research project for graph contrastive learning node
classification. The previous selected research direction was NFR-GCL
(Node-Frequency Routed Graph Contrastive Learning), but it was abandoned on
2026-06-21 before implementation because the chance of making it a strong new
paper contribution is low after novelty checking.

Key artifacts:
- `MANIFEST.md` tracks ARIS-generated outputs.
- `idea-stage/IDEA_REPORT.md` contains the latest RSP-GCL idea report, but RSP
  has now been downgraded after M2-M4.
- `idea-stage/IDEA_CANDIDATES.md` contains the latest RSP candidate table and
  should be refreshed on the next idea-discovery restart.
- `refine-logs/FINAL_PROPOSAL.md` contains the latest RSP proposal context, now
  diagnostic-only rather than paper-ready.
- `refine-logs/EXPERIMENT_PLAN.md` contains the RSP gate plan; R042-R044 are
  completed and failed to promote RSP.
- `refine-logs/EXPERIMENT_TRACKER.md` tracks R039-R044 and marks RSP
  diagnostic-only after novelty and gate checks.
- `refine-logs/EXPERIMENT_RESULTS.md` is the latest compact result summary.
- `research-wiki/` stores paper notes, gap map, idea pages, and graph edges.
- `baselines/` contains local baseline code, datasets, split files, run logs,
  and reproduction summaries.

Implementation orientation:
- Do not implement NFR-GCL unless the user explicitly reverses the decision.
- If the user wants to continue from the old backup, inspect
  `research-wiki/ideas/heterophilous_edge_reconstruction.md` first and reassess
  novelty before writing code.
- If a new method is selected later, prefer a small pilot inside the existing
  `baselines/` harness rather than starting a new large code stack.
- The latest tested candidate is RSP-GCL (Role-Signature Positive Graph
  Contrastive Learning), now diagnostic-only after Chameleon/WebKB gates and
  novelty review.
- Keep RFA-BGRL and RSP role signatures as required diagnostic baselines. Do
  not claim RFA, ORFA, BiFilter-BGRL, FBA, DCA, VST, CIG/CLEAR, or RSP as final
  methods.
- Preserve the protocol in `baselines/reproduction_protocol.md`: heterophily
  datasets must use Geom-GCN official fixed splits from
  `baselines/dataset_splits/heterophily/geom-gcn/`, not random splits.
- Run baseline experiments sequentially with CPU thread caps unless there is an
  explicit protocol exception.

Novelty status update:
- 2026-06-21 novelty scan found ASPECT (arXiv 2604.01878, 2026), which directly
  overlaps with node-level adaptive spectral fusion for graph contrastive
  learning. Original NFR-GCL should be treated as LOW-to-MEDIUM novelty unless
  reframed around a clear delta: mid-band routing, label-free compatibility
  router features, stronger diagnostics, and direct comparison to ASPECT.
- Do not claim NFR-GCL is the first node-wise spectral/frequency routing GCL
  method. Add ASPECT as required closest prior work/baseline for any paper plan.
- User decision on 2026-06-21: abandon NFR-GCL rather than spend experiment time
  on a low-novelty direction.
- 2026-06-21 cross-domain transfer survey saved at
  `idea-stage/CROSS_DOMAIN_TRANSFER_GCL_20260621.md`. Strongest directions to
  investigate next are latent-prediction graph contrastive learning,
  invariant-environment graph contrastive learning, and optimal-transport soft
  alignment for edge/semantic compatibility.
- 2026-06-21 latent-prediction scan selected SRLP as the next active idea. A
  two-round reviewer refinement changed the target from `Z - alpha PZ` to a
  context-projected residual: remove only the component of the target teacher
  latent explained by the visible context subspace, then predict that residual
  from a target-isolated online graph. Closest risks are Graph-JEPA,
  GraphMAE2, BGRL, JPEB-GSSL/Predict-Cluster-Refine, ASPECT, and SPGCL. Do not
  claim generic graph latent prediction is novel; the novelty claim must be
  target construction for shortcut-resistant node-level graph SSL.

Repository status note:
- This checkout was initialized locally. The outer repository should track
  research documents, protocol files, fixed split masks, and result summaries.
- Baseline method directories under `baselines/` are nested Git repositories
  and are ignored by the outer repository to avoid accidental gitlink commits.
- GitHub remote is configured as
  `origin=https://github.com/coinrainy/IDEA-CREATOR.git`; `master` tracks
  `origin/master`.
