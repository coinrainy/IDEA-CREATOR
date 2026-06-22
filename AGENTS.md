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
- 2026-06-22: Clarified evaluation backend policy after the user asked whether
  evaluation/data preprocessing must stay on CPU. Conclusion: canonical
  reported node-classification evaluation remains CPU sklearn logistic
  regression because it matches the existing BGRL/GCL protocol and historical
  results; GPU should be used for training, encoder forward / representation
  extraction, tensor propagation, feature construction, and proxy diagnostics.
  Added optional `--eval_backend=torch_gpu_fast` to
  `baselines/BGRL/train_npg_transductive.py` and pass-through support in
  `reproduce_npg.py`, with `eval_backend` recorded in CSV. Smoke checks on
  Cora split 0, 1 epoch passed for both `sklearn` (`0.792340`) and
  `torch_gpu_fast` (`0.759114`) on CUDA, showing the fast probe is usable but
  not protocol-equivalent. Policy report:
  `refine-logs/EVAL_BACKEND_POLICY_20260622.md`.
- 2026-06-22: Implemented and gated Ego-NoSelf BGRL R110/R111 after MFS
  failed. Added `NoSelfGCN` and `ego_noself` to
  `baselines/BGRL/train_npg_transductive.py`, with reproducer support in
  `reproduce_npg.py`. Motivation was to test whether the strong fixed
  Positive-Path / no-self LIFT signal can become a trained BGRL encoder by
  setting `GCNConv(add_self_loops=False)`. CUDA smoke passed with no
  NaN/collapse, but split-0 gate decisively failed: Cora `0.815874` vs BGRL
  `0.832949`, CiteSeer `0.663411` vs `0.693088`, and Chameleon `0.287281` vs
  BGRL `0.438596` / Positive-Path `0.725877`. Decision:
  `FAILED_SPLIT0_GATE`; direct no-self message passing destroys too much node
  identity during BGRL training. Keep no-self only as a fixed feature/channel
  control unless a protected raw identity branch is added. Report:
  `refine-logs/EGO_NOSELF_R110_R111_RESULTS_20260622.md`.
- 2026-06-22: Implemented and gated Missing-Feature Stress GCL (MFS-GCL)
  R108/R109 after DDC failed. Added `mfs_clean` and `mfs_aux` variants to
  `baselines/BGRL/train_npg_transductive.py` and `reproduce_npg.py`.
  Mechanism: apply node-wise independent feature-entry dropout to the online
  view and align it either directly (`mfs_clean`) or as an auxiliary loss
  (`mfs_aux`) to a clean teacher target. R108 CUDA smoke passed on
  Cora/Chameleon with no NaN/collapse. R109 split-0 gate failed as a main
  method: Cora improves over same-run BGRL (`0.832949 -> 0.840794`) but remains
  below LIFT (`0.842640`); CiteSeer is nearly flat (`0.693088 -> 0.693839`);
  Chameleon has only a tiny BGRL-internal gain (`0.438596 -> 0.449561`) and is
  far below Positive-Path (`0.725877`). Novelty risk is high near RFM, FDAGCL,
  and masked/adversarial feature GCL. Decision: `FAILED_SPLIT0_GATE`; do not
  run WebKB, 10-split, or external baselines for MFS. Report:
  `refine-logs/MFS_R108_R109_RESULTS_20260622.md`. GPU policy clarified:
  training and representation extraction should use CUDA when available, but
  final node-classification probes remain canonical CPU sklearn unless a GPU
  solver is separately equivalence-validated.
- 2026-06-22: Implemented and gated Depth-Disagreement Contrast (DDC-BGRL)
  R106/R107 after Cycle-Balance was downgraded. Added `ddc_control`,
  `ddc_weight`, and `ddc_aux` variants to
  `baselines/BGRL/train_npg_transductive.py` plus reproducer support in
  `reproduce_npg.py`. DDC uses a `DepthTraceGCN` to expose shallow/deep states,
  then weights BGRL node losses by shallow/deep disagreement or adds an
  auxiliary shallow-depth alignment target. CUDA smoke passed on Cora/Chameleon
  with no NaN/collapse. M1 split-0 gate failed: Cora has only a weak
  same-architecture gain (`0.802953 -> 0.811260`) and remains below BGRL/LIFT;
  CiteSeer is nearly flat (`0.677310 -> 0.678062`); Chameleon regresses
  (`0.394737 -> 0.383772`) and is far below BGRL/Positive-Path. Novelty risk is
  also high near BlockGCL and stage-aware GCL. Decision:
  `FAILED_SPLIT0_GATE`; do not expand DDC to WebKB, 10-split, or paper
  refinement. Report: `refine-logs/DDC_R106_R107_RESULTS_20260622.md`.
- 2026-06-22: Completed Cycle-Balance R104/R105 ablations and downgraded the
  route. Extended `baselines/BGRL/evaluate_cycle_balance_proxy.py` with
  component variants (`cycle_gate_pos1`, `cycle_gate_balanced2`,
  `cycle_gate_diff2`, etc.) and sign controls (`random`, `rank`,
  `rank_global_shuffle`, `rank_node_shuffle`). The crucial finding is that
  Chameleon's original median-cosine sign rule degenerates to all-positive
  edges (`edge_threshold=0.0`, `pos_ratio=1.0`), so R102/R103's strong
  `cycle_gate_signed_all` result is not evidence for a true signed/balance
  mechanism. Component ablation shows the gain is mostly positive/no-self
  one-hop propagation (`cycle_gate_pos1` fast-grid `0.706579` vs portfolio
  `0.655482`) plus a smaller two-hop complement; negative and unbalanced
  channels contribute nothing. Sign controls confirm the downgrade: random
  signs `0.642763`, rank 50/50 signs `0.685526`, rank global shuffle
  `0.645395`, rank node shuffle `0.667105`, while all-positive cosine remains
  `0.708114`. Decision: Cycle-Balance is
  `POSITIVE_PATH_BASELINE_NOT_MAIN_METHOD`; do not implement a trained
  Cycle-Balance objective. Restart main-method search with Positive-Path /
  No-self LIFT as a required baseline. Report:
  `refine-logs/CYCLE_BALANCE_R104_R105_ABLATIONS_20260622.md`.
- 2026-06-22: Added and tested Cycle-Balance Gated LIFT R102/R103 as the
  first post-SSA active candidate. Added
  `baselines/BGRL/evaluate_cycle_balance_proxy.py`, which induces signed edges
  from raw feature cosine on observed unsigned graph edges, builds positive /
  negative one-hop and balanced / unbalanced two-hop path channels, and appends
  them only when LIFT-Portfolio selects `single_k2_low_raw_lift`; otherwise it
  falls back exactly to the protected portfolio. Tensor propagation and signed
  feature construction use `--device=auto` / CUDA when available, while final
  node-classification probes remain canonical CPU sklearn. Split-0 five-dataset
  gate protects Cora/CiteSeer/Texas/Wisconsin and improves Chameleon
  (`0.699561 -> 0.717105`). Chameleon 10-split full C-grid improves from
  portfolio `0.685526 +/- 0.021292` to `0.725877 +/- 0.019174`. Extra split-0
  scope check protects Squirrel/Actor/Cornell unchanged. Manual novelty check is
  `PROCEED_WITH_CAUTION` around `5/10`: closest risks are SGCL/SGCA signed GCL,
  HLCL/HeterGCL, ASPECT, and GCL-OT. External reviewer call failed with a 403
  quota error; trace saved under `.aris/traces/novelty-check/2026-06-22_cycle_balance_run01/`.
  Initial decision was `ACTIVE_CANDIDATE_WITH_NOVELTY_RISK`, not paper-ready,
  but this was later downgraded by R104/R105 sign-control ablations. Report:
  `refine-logs/CYCLE_BALANCE_R102_R103_RESULTS_20260622.md`.
- 2026-06-22: Implemented and gated Sharpness-Stable Alignment BGRL
  (SSA-BGRL) R100/R101 after low-rank failed. Added `ssa_weight` and
  `ssa_consistency` variants to `baselines/BGRL/train_npg_transductive.py` and
  `reproduce_npg.py`. Mechanism: temporarily perturb the online
  encoder/predictor parameters, measure node-level alignment-loss drift, and
  weight stable nodes higher; `ssa_consistency` also aligns to perturbed
  predictions. CUDA smoke passed on Cora/Chameleon with no NaN/collapse. M1
  200-epoch split-0 produced only weak internal gains: Cora `0.832949 ->
  0.834333`, CiteSeer `0.693088 -> 0.696093`, Chameleon tied BGRL at
  `0.438596`, all far below LIFT-Portfolio (`0.842640`, `0.725770`,
  `0.699561`). The run was stopped before Texas/Wisconsin to save GPU.
  Decision: `BGRL_INTERNAL_WEAK_SIGNAL_NOT_MAIN_METHOD`; do not expand SSA.
  Report: `refine-logs/SSA_M0_M1_RESULTS_20260622.md`.
- 2026-06-22: Added optional GPU tensor evaluation support for LIFT-family
  evaluators without changing the canonical final probe. Updated
  `evaluate_lift_prop.py`, `evaluate_lift_stack.py`,
  `evaluate_lift_portfolio.py`, `evaluate_lift_viewset_dispersion.py`, and
  `evaluate_lift_lowrank.py` with `--device cpu|cuda|auto`. The switch moves
  propagation matrix multiplications to torch sparse CUDA when requested, then
  returns NumPy arrays for the existing CPU sklearn logistic-regression probe.
  Cora CPU-vs-CUDA propagation equivalence check passed with max absolute
  differences `[0.0, 5.96e-08, 7.45e-08, 1.04e-07]`. Policy: use GPU tensor
  evaluation for screening/proxy speed, but keep final reported
  node-classification probes on canonical CPU sklearn unless a GPU solver is
  separately validated as protocol-equivalent.
- 2026-06-22: Tested LIFT Low-Rank Bottleneck R099 as a proxy before any
  learned low-rank GCL objective. Added
  `baselines/BGRL/evaluate_lift_lowrank.py`, which applies randomized SVD to
  normalized/centered LIFT-Portfolio representations and tests scaled and
  whitened low-rank coordinates while keeping the canonical CPU sklearn final
  probe. Result: `FAILED_PROXY_GATE`. CiteSeer has a local rank-32 gain
  (`0.725770 -> 0.731781`), but Cora has no gain (`0.842640 -> 0.842178`) and
  Chameleon fails decisively (`0.699561 -> 0.651316`). Decision: do not
  implement a learned low-rank GCL objective; keep low-rank only as a
  CiteSeer-overfitting diagnostic. Report:
  `refine-logs/LIFT_LOWRANK_R099_RESULTS_20260622.md`.
- 2026-06-22: Tested LIFT View-Set Dispersion R098 as a cheap proxy for a
  possible uncertainty/conformal view-set GCL direction. Added
  `baselines/BGRL/evaluate_lift_viewset_dispersion.py`. The proxy appends
  propagation-view mean/std/range/delta statistics over `[X,PX,P2X,P3X]` to
  LIFT-Portfolio and keeps the CPU sklearn final probe. Result:
  `FAILED_PROXY_GATE`. Cora has only a tiny local gain
  (`0.842640 -> 0.844947`), while CiteSeer and Chameleon regress
  (`0.725770 -> 0.720135`, `0.699561 -> 0.662281`). The run was stopped after
  Chameleon to save CPU time. Novelty risk is near IJCAI 2025 UGCL. Do not
  implement a trained view-set dispersion objective. Report:
  `refine-logs/LIFT_VIEWSET_DISPERSION_R098_RESULTS_20260622.md`.
- 2026-06-22: Implemented and gated SBB-BGRL R097 after CCR-SAFE failed fresh
  splits. Added `sbb_hard` / `sbb_soft` variants inside
  `baselines/BGRL/train_npg_transductive.py` and `reproduce_npg.py`. Mechanism:
  preserve low raw-cosine neighbor messages in the forward pass but
  stop-gradient those message paths. CUDA smoke passed and M1 split-0 completed
  on Cora/CiteSeer/Chameleon/Texas/Wisconsin with CPU sklearn final probes.
  Result: `FAILED_MIXED_SPLIT0_GATE`. Cora/CiteSeer/Chameleon regress
  (`0.832949 -> 0.815413`, `0.692712 -> 0.688204`,
  `0.438596 -> 0.427632`); Texas/Wisconsin improve only against weak BGRL
  (`0.648649`, `0.568627`) and remain far below LIFT/raw (`0.810811`,
  `0.823529`). Do not tune SBB quantiles or run 10-split. Report:
  `refine-logs/SBB_M0_M1_RESULTS_20260622.md`.
- 2026-06-22: Ran CCR-SAFE R096 fixed-threshold fresh-split validation after
  the promising R095 diagnostic. Fixed `evaluate_ccr_safety.py` so multi-split
  evaluation loads each split's own checkpoint, then trained fresh CCR
  checkpoints with CUDA for Cora splits 1-2 and CiteSeer split 1 using
  `reproduce_ccr.py --device=auto`. Result: `FAILED_FRESH_SPLIT_GATE`.
  `stack_moderate_residual` accepts harmful Cora residuals on both fresh
  splits (`0.844024 -> 0.832949`, `0.854638 -> 0.850023`) and protects only
  CiteSeer split 1 (`0.732156` preserved). The remaining queue was stopped to
  save compute. Decision: CCR-SAFE is no longer an active main-method route;
  restart main-method search with LIFT-Portfolio as the required control.
  Report: `refine-logs/CCR_SAFE_R096_FRESH_SPLIT_RESULTS_20260622.md`.
- 2026-06-22: Completed CCR-SAFE R095 residual-safety diagnostic after the
  R093/R094 certification failure. Added
  `baselines/BGRL/evaluate_ccr_safety.py`, which uses GPU for checkpoint
  forward passes and tensor diagnostics while retaining CPU sklearn for final
  accuracy numbers. Existing CCR checkpoints were evaluated with label-free
  residual policies. The old certificate still fails, but
  `stack_moderate_residual` accepts only Cora and improves LIFT-Portfolio
  (`0.842640 -> 0.851869`) while rejecting CiteSeer, Chameleon, Texas, and
  Wisconsin, preserving their portfolio scores (`0.725770`, `0.699561`,
  `0.810811`, `0.823529`). Decision:
  `PROMISING_DIAGNOSTIC_NOT_METHOD_READY`; thresholds were selected on the
  same split-0 batch, so CCR-SAFE needs fixed-threshold fresh-split validation
  before it can become an active main method. Report:
  `refine-logs/CCR_SAFE_R095_RESULTS_20260622.md`.
- 2026-06-22: Implemented and gated CCR-GCL, a LIFT-Portfolio-teacher +
  orthogonal learned-residual branch, after PAB only produced BGRL-internal
  gains. Added `baselines/BGRL/train_ccr_transductive.py` and
  `baselines/BGRL/reproduce_ccr.py`. M0 smoke and M1 split-0 ran on CUDA, with
  CPU sklearn final probes. Result: `FAILED_CERTIFICATION_GATE`. Cora has the
  strongest learned residual signal so far: LIFT-Portfolio `0.842640`,
  portfolio+residual `0.851407`, certified `0.855099`. But the same
  certification admits harmful residuals on CiteSeer (`0.725770 -> 0.714125`),
  Chameleon (`0.699561 -> 0.629386`), Texas (`0.810811 -> 0.783784`), and
  Wisconsin (`0.823529 -> 0.803922`). No NaN/collapse. Decision: do not run
  CCR 10-split; learned residuals should not continue until a stronger
  label-free residual safety criterion is found. Report:
  `refine-logs/CCR_M0_M1_RESULTS_20260622.md`.
- 2026-06-22: Implemented and gated PAB-BGRL after EPI failed. Added
  `pab_hard` / `pab_soft` variants to `baselines/BGRL/train_npg_transductive.py`
  and `baselines/BGRL/reproduce_npg.py`, with explicit `--device=auto/cuda/cpu`.
  PAB downweights nodes whose BGRL positive alignment is likely already
  trivialized by message passing. M0 smoke and M1 split-0 ran on CUDA with no
  NaN/collapse. Result: `BGRL_INTERNAL_SIGNAL_NOT_MAIN_METHOD`. PAB improves
  BGRL on CiteSeer (`0.695342` vs `0.693464`), Chameleon (`0.449561` vs
  `0.438596`), and Texas (`0.648649` vs `0.621622`), but remains far below
  LIFT-Portfolio/raw controls (`0.725770`, `0.699561`, `0.810811`);
  Cora/Wisconsin tie BGRL. Novelty risk is high near SPGCL's 2026
  pre-alignment/message-passing analysis. Do not run PAB 10-split. Report:
  `refine-logs/PAB_M0_M1_RESULTS_20260622.md`.
- 2026-06-22: Implemented and gated EPI-BGRL as a genuinely different,
  GPU-trained mechanism family after LIFT-Portfolio became the required
  baseline. Added `baselines/BGRL/train_epi_transductive.py` and
  `baselines/BGRL/reproduce_epi.py`. EPI partitions nodes into label-free
  environments using degree and raw-feature neighborhood drift, then balances
  BGRL node losses across environments with a REx-style penalty. M0 smoke and
  M1 split-0 ran on CUDA (`device=cuda`; logs show `Using cuda for training`),
  while final linear probes kept the CPU sklearn protocol. Result:
  `FAILED_MIXED_SPLIT0_GATE`. Cora improves over BGRL (`0.840794` vs
  `0.833872`) but remains below LIFT-Portfolio split-0 (`0.842640`);
  CiteSeer/Chameleon regress (`0.690834` / `0.425439` vs BGRL `0.693839` /
  `0.438596`), and Texas/Wisconsin tie weak BGRL while far below raw/LIFT.
  Do not run EPI 10-split; keep as negative evidence. Report:
  `refine-logs/EPI_M0_M1_RESULTS_20260622.md`.
- 2026-06-22: User clarified that evaluation should also use GPU acceleration
  when possible, but not at the cost of changing the result protocol. Policy
  recorded below: GPU is preferred for protocol-equivalent tensor operations
  such as encoder forward, propagation, cosine/distance, and reductions; final
  paper linear-probe/logistic-regression numbers should keep the canonical CPU
  sklearn solver unless GPU equivalence is explicitly validated. GPU-only probe
  variants may be used for fast screening and must be labeled as screening.
- 2026-06-22: Completed R088 LIFT-Portfolio baseline audit after finding a
  fast/full C-grid mismatch on Chameleon. Added
  `baselines/BGRL/evaluate_lift_portfolio.py`. Full-grid Chameleon 10-split:
  global LIFT/P2 `0.685746`, LIFT-Stack `0.671053`, portfolio `0.685746`.
  Cora/CiteSeer 10-split full-grid keep stack gains (`0.848869` /
  `0.726972`), Squirrel fast 10-split keeps stack (`0.543708`), and
  Texas/Wisconsin/Cornell/Actor remain raw-protected. Portfolio rule: raw for
  selected K0; P2 for selected K2 when raw edge-lift `<0.05`; otherwise
  `[X,PX,P2X,P3X]`. Decision: `STRONG_BASELINE_LOW_NOVELTY`; LIFT-Portfolio
  replaces plain LIFT-Stack as the required control, but still is not the final
  paper-level GCL method due SIGN/SGC/FAF/PROPGCL and routing-prior novelty
  risk. Report: `refine-logs/LIFT_PORTFOLIO_RESULTS_20260622.md`.
- 2026-06-22: Diagnosed apparent "training not using GPU" issue during the
  LIFT-Portfolio homophily evaluation. The then-active process was
  `baselines/BGRL/evaluate_lift_portfolio.py --datasets=cora,citeseer`
  writing `runs/lift_portfolio_homo10_20260622/results.csv`. It is not a
  PyTorch CUDA training loop: LIFT feature propagation is computed as
  scipy/numpy arrays and homophily evaluation calls
  `bgrl.fit_logistic_regression`, which uses sklearn
  `GridSearchCV(..., n_jobs=5)` and spawns joblib `LokyProcess-*` CPU workers.
  `nvidia-smi` showed GPU 0% and no GPU process because this portfolio
  evaluation path is CPU-only by design. Prior BGRL-style training scripts still
  log `Using cuda for training` when launched.
- 2026-06-22: Completed R087 LIFT interaction-feature diagnostic. Added
  `baselines/BGRL/evaluate_lift_interactions.py`, which appends deterministic
  raw-propagation product, absolute-difference, and delta blocks to LIFT-Stack.
  Fast split-0 results: Cora has a tiny `stack_plus_diff` gain (`0.845408` vs
  `0.842640`), CiteSeer has a tiny `stack_plus_agree` gain (`0.729527` vs
  `0.725770`), but Chameleon fails (`0.666667` best interaction vs
  `0.668860`, with several variants much worse). Decision:
  `FAILED_SPLIT0_GATE`; stop fixed-feature micro-tuning on top of LIFT-Stack.
  Report: `refine-logs/LIFT_INTERACTIONS_RESULTS_20260622.md`.
- 2026-06-22: Completed R086 LIFT Channel Gate diagnostic. Added
  `baselines/BGRL/evaluate_lift_channel_gate.py`, which scores each LIFT-Stack
  feature channel by standardized edge-lift and applies ReLU/sqrt/softplus/top-k
  weights only when global LIFT enables propagation. Split-0 result: Cora and
  CiteSeer regress (`0.841255` / `0.719760` best channel gates vs LIFT-Stack
  `0.842640` / `0.725770`), Chameleon has a local softplus gain (`0.688596`
  vs `0.668860`), and WebKB remains raw-protected. Fast 10-split result:
  Chameleon is neutral (`0.663377` best vs `0.662500`), Squirrel ReLU regresses
  (`0.525360` vs `0.543708`) and softplus is neutral (`0.543420`). Decision:
  `FAILED_ROBUSTNESS_GATE`; keep channel edge-lift as a diagnostic only. Report:
  `refine-logs/LIFT_CHANNEL_GATE_RESULTS_20260622.md`.
- 2026-06-22: Completed R085 LIFT-Stack + checkpoint residual diagnostic.
  Added `baselines/BGRL/evaluate_lift_stack_plus_checkpoint.py`, which loads
  existing BGRL/GDC/TD encoder checkpoints and evaluates checkpoint-only plus
  LIFT-Stack concatenations. Split-0 result: Cora has a local complement signal
  (`0.852792` vs LIFT-Stack `0.842640`), but CiteSeer (`0.713749` vs
  `0.725770`), Chameleon (`0.638158` vs `0.668860`), Texas (`0.783784` vs
  `0.810811`), and Wisconsin (`0.803922` vs `0.823529`) all regress. Dynamic
  variants do not beat ordinary BGRL as a distinct complement. Decision:
  `FAILED_COMPLEMENTARITY_GATE`; do not promote learned-checkpoint
  concatenation. LIFT-Stack remains the required baseline and the main-method
  search must restart with a different mechanism family or a robust label-free
  residual-routing rule. Report:
  `refine-logs/LIFT_STACK_CHECKPOINT_RESIDUAL_RESULTS_20260622.md`.
- 2026-06-22: Implemented and gated LIFT-HC-GCL, a hop-drop contrastive MLP
  branch on top of LIFT-Stack. Added
  `baselines/BGRL/evaluate_lift_hc_gcl.py`. Main split-0 gate with 300 epochs:
  Cora `stack+SSL 0.850023` vs LIFT-Stack `0.842640` (positive), CiteSeer
  `0.716754` vs `0.725770` (fail), Chameleon `0.657895` vs `0.668860` (fail),
  Texas protected at `0.810811`, Wisconsin local positive `0.843137` vs
  `0.823529`. Short 5/20-epoch probes keep Cora positive and sometimes make
  CiteSeer near-neutral, but Chameleon remains negative. Decision:
  LIFT-HC-GCL is `FAILED_MIXED_SPLIT0_GATE`; do not expand. LIFT-Stack remains
  the required strong control. Report:
  `refine-logs/LIFT_HC_GCL_RESULTS_20260622.md`.
- 2026-06-22: Added and evaluated LIFT-Stack as a stronger training-free
  control after LIFT-PROP R077/R078 failed. New script:
  `baselines/BGRL/evaluate_lift_stack.py` with `--variants` filtering.
  LIFT-Stack rule: if global LIFT selects K0 use raw `X`, otherwise use
  concatenated normalized `[X,PX,P2X,P3X]`. Results: Cora 10 random splits
  `0.848823` vs global LIFT `0.832995`; CiteSeer `0.727310` vs `0.700301`;
  Chameleon fast 10-split `0.662500` vs `0.655482`; Squirrel fast 10-split
  `0.543708` vs `0.520365`; Texas/Wisconsin/Cornell/Actor are protected by
  raw fallback. Decision: LIFT-Stack is `STRONG_BASELINE_LOW_NOVELTY`, not yet
  the final GCL idea, because SIGN/SGC, Fixed Aggregation Features
  (arXiv 2601.19449v2, 2026), and PROPGCL are very close. Next main-method
  restart must beat LIFT-Stack or provide a clearly more novel mechanism.
  Report: `refine-logs/LIFT_STACK_RESULTS_20260622.md`.
- 2026-06-22: Completed LIFT-PROP R077/R078 after the PROPGCL-facing selector
  check. Added `baselines/BGRL/evaluate_lift_prop_gcl.py` for edge-NCE learned
  propagation coefficients and `baselines/BGRL/evaluate_lift_prop_nodewise.py`
  for local/node-wise LIFT routing. R077 split-0 result: edge-NCE learned mix
  improves only Cora (`0.831103` vs selector `0.825565`) but fails CiteSeer
  (`0.684072` vs `0.709617`) and Chameleon (`0.622807` vs `0.699561`);
  Texas/Wisconsin are protected only because the global gate falls back to raw
  (`0.810811` / `0.823529`). R078 fast split-0 result: node-soft improves Cora
  (`0.836641` vs global `0.825565`) but hurts Chameleon/Texas/Wisconsin
  (`0.653509` / `0.783784` / `0.784314` vs global `0.668860` / `0.810811` /
  `0.823529`). Decision: LIFT-PROP is now
  `SELECTOR_BASELINE_NOT_MAIN_METHOD`; use global LIFT-PROP as a required
  training-free control, and restart the main-method search with a different
  mechanism family. Report:
  `refine-logs/LIFT_PROP_R077_R078_RESULTS_20260622.md`.
- 2026-06-22: Ran `/wiki-enrich` on the 8 missing
  `research-wiki/papers/*.md` scaffolds and filled all 10 writable sections for
  each page, while preserving frontmatter, `Connections`, and
  `Abstract (original)`. Source provenance: 7 pages from `alphaxiv-abs`
  (`chen2024_leveraging_contrastive_learning`,
  `lee2025_similarities_embeddings_contrastive`,
  `thakoor2021_largescale_representation_learning`,
  `wang2022_augmentationfree_graph_contrastive`,
  `wang2025_khangcl_kolmogorovarnold_network`,
  `yang2023_graph_contrastive_learning`,
  `zhu2020_graph_contrastive_learning`) and 1 page from `alphaxiv-overview`
  (`zhu2020_deep_graph_contrastive`). No `claim:` edges were present, so all
  paper `Claims` sections use the standard no-claims placeholder. Rebuilt
  `research-wiki/query_pack.md` for downstream `/idea-creator`; audit entries
  were appended to `research-wiki/log.md`.
- 2026-06-22: Completed LIFT-PROP R076 first-pass PROPGCL-facing comparison.
  Downloaded/extracted PROPGCL OpenReview PDF to
  `literature/PROPGCL_i4qdY4vQU9.pdf/.txt`. PROPGCL defines PROP as
  `A_hat^K X` and reports K=1 best for Cora/CiteSeer/Chameleon/Squirrel, K=0
  for Texas/Wisconsin/Cornell/Actor/CS. Added
  `baselines/BGRL/summarize_lift_prop_selectors.py`. On the eight observed
  settings, LIFT-PROP v1 has mean test `0.696868`, mean oracle gap `0.001096`,
  exact oracle hits `7/8`, within-0.02 `8/8`; the PROPGCL reported-step
  heuristic has mean test `0.686911`, mean oracle gap `0.011052`, exact hits
  `5/8`, within-0.02 `6/8`. Decision: positive for label-free selector claim,
  but not a full comparison against learned `PROP-GRACE` / `PROP-DGI`; LIFT-PROP
  remains active but not paper-ready. Report:
  `refine-logs/LIFT_PROP_PROPGCL_FACING_COMPARISON_20260622.md`.
- 2026-06-22: Completed LIFT-PROP R074 metric ablation first pass. Across the
  eight observed settings, `delta_lift_k2_k0 = lift(P2X)-lift(X)` correlates
  strongly with propagation gain `Acc(P2X)-Acc(X)` (Pearson `0.915337`,
  Spearman `0.880952`). Propagated edge cosine alone is negatively correlated
  because high edge cosine can mean global smoothing. Decision: edge-lift has
  real diagnostic support; next diagnostics should compare degree/density/rank
  and add bootstrap uncertainty. Report:
  `refine-logs/LIFT_PROP_METRIC_ABLATION_20260622.md`.
- 2026-06-22: Refreshed `refine-logs/FINAL_PROPOSAL.md` and
  `refine-logs/EXPERIMENT_PLAN.md` from stale NPG content to LIFT-PROP-GCL v1.
  Current plan milestones R072-R076 focus on selector summary, selector
  baselines, metric ablations, full-grid Actor/Squirrel if feasible, and direct
  PROPGCL-facing comparison. R077 GCL training integration is blocked until the
  selector/novelty checks justify it.
- 2026-06-22: Refined LIFT-PROP into selector v1. Rule:
  if `lift(P2X)<0.35`, select K=0; else if
  `lift(P2X) <= lift(PX)+0.02`, select K=1; otherwise select K=2. Re-ran
  Actor/Squirrel fast-grid 10-split with v1: Actor selects K0 and matches
  oracle (`0.347566`), Squirrel selects K1 and matches oracle (`0.520365`).
  Across observed datasets/settings, selector v1 hits oracle on 7/8, with Cora
  as the only near miss (selected K2 `0.826488`, oracle K3 `0.835256`).
  Aggregate summary also shows selector v1 matches validation-selected K on
  7/8 without labels. R072-R073 are completed.
  Decision: LIFT-PROP now has a concrete method v1, but remains
  `PROCEED_WITH_CAUTION`; next required checks are direct PROPGCL comparison,
  full-grid Actor/Squirrel if feasible, and theory/diagnostics linking
  edge-lift to propagation gain. Report:
  `refine-logs/LIFT_PROP_SELECTOR_V1_RESULTS_20260622.md`.
- 2026-06-22: Optimized LIFT-PROP evaluation with `--c_powers` and ran a
  fast-grid Actor/Squirrel 10-split check. Actor remains raw-protection
  positive: gate K=0, oracle K=0, `0.347566`. Squirrel remains
  propagation-positive, but fixed K2 is a near miss under fast grid: K2
  `0.509030` beats raw `0.328530`, while K1 is oracle at `0.520365`. Decision:
  keep the edge-lift abstention gate, but next method revision should add a
  label-free K1/K2 selector when propagation is enabled. Updated report:
  `refine-logs/LIFT_PROP_EXTRA_VALIDATION_20260622.md`.
- 2026-06-22: Added formal LIFT-PROP runner
  `baselines/BGRL/reproduce_lift_prop.py` plus streaming output. Extra
  validation is positive but incomplete. Cornell 10-split selects raw K=0 by
  edge-lift and matches oracle (`0.816216 +/- 0.059487`). Actor split-0 selects
  raw K=0 and matches oracle (`0.348684`). Squirrel split-0 selects K=2 and
  matches oracle (`0.571566`). The attempted Cornell/Actor/Squirrel 10-split
  run was interrupted after Cornell because Actor linear evaluation was too
  slow with the full C-grid. Decision: LIFT-PROP remains
  `ACTIVE_PROCEED_WITH_CAUTION`; next action is faster Actor/Squirrel 10-split
  plus direct comparison to validation-selected K and PROPGCL-style
  propagation. Report:
  `refine-logs/LIFT_PROP_EXTRA_VALIDATION_20260622.md`.
- 2026-06-22: Completed first novelty check for LIFT-PROP-GCL. Verdict:
  `PROCEED_WITH_CAUTION`, novelty score `5.5/10`, not paper-ready. External
  Claude reviewer call failed with a 403 quota error and the failure trace was
  saved under `.aris/traces/novelty-check/2026-06-22_run01/`. Closest prior is
  PROPGCL, which already establishes training-free propagation as a strong GCL
  mechanism. Other risks: GNNEvaluator / When Do GNNs Help for label-free graph
  usefulness estimation, GLANCE for label-free homophily routing, Less is More
  for graph/raw dual views, ASPECT for adaptive spectral GCL, GRAPHITE for
  feature-node graph transformation, and HLCL for feature-cosine heterophily
  filters. Defensible delta is narrow: edge-lift raw-vs-`P^2X` abstention that
  matches oracle K on 4/5 pilot datasets. Next action: compact method refinement
  plus direct PROPGCL-facing validation; do not enter full paper writing or
  large external baseline expansion yet. Report:
  `refine-logs/LIFT_PROP_NOVELTY_CHECK_20260622.md`.
- 2026-06-22: Restarted after NPG/SC/GDC failures and found a stronger active
  route: LIFT-PROP-GCL, a label-free edge-lift gate for propagation reliability.
  Added `baselines/BGRL/evaluate_factor_token_proxy.py` and
  `baselines/BGRL/evaluate_lift_prop.py`. Feature-token propagation was useful
  but not the lead and overlaps with GRAPHITE. The decisive proxy is raw vs
  `P^KX`: using `lift(P^2X)=mean_edge_cos(P^2X)-mean_random_pair_cos(P^2X)`
  with threshold `0.35` selects K=2 for Cora/CiteSeer/Chameleon and K=0 for
  Texas/Wisconsin. M0 results: Cora split-0 K2 `0.826488` (oracle K3
  `0.835256`), CiteSeer K2 `0.709617`, Chameleon K2 `0.685746 +/- 0.021187`,
  Texas raw `0.829730 +/- 0.051042`, Wisconsin raw
  `0.839216 +/- 0.043157`. Decision: LIFT-PROP-GCL is
  `ACTIVE_WITH_NOVELTY_RISK`; direct novelty check against PROPGCL, Less is
  More, ASPECT, GRAPHITE, and graph-adaptive propagation/filtering is mandatory
  before claiming paper readiness. Report:
  `refine-logs/LIFT_PROP_M0_RESULTS_20260622.md`.
- 2026-06-22: Continued the post-TDGCL research-pipeline pilot queue. NPG-GCL
  was implemented and downgraded after weak split-0 evidence plus a failed
  random-weight ablation: Cora `0.834333` vs control `0.830641`, but random
  weighting `0.838948`; Chameleon `0.442982` vs control `0.438596`; CiteSeer
  regressed and WebKB tied. Fixed-sign SC-BGRL was implemented with a
  rank-based same/different edge split and failed split-0: Cora `0.828334` vs
  control `0.832487`, Chameleon `0.436404` vs `0.438596`, WebKB tied. GDC-GCL+
  was then implemented as gradient-residual dynamics positives in
  `train_gdc_transductive.py` / `reproduce_gdc.py`; smoke passed, but M1
  failed: Cora `0.830641` vs BGRL `0.833410`, CiteSeer `0.691210` vs
  `0.693464`, Chameleon only `+0.004386`, Texas/Wisconsin tied. No NaN/collapse.
  Decision: NPG, fixed-sign SC, and GDC are not `READY_TO_REFINE`; restart wide
  idea discovery with a different mechanism family. Reports:
  `refine-logs/NPG_M0_M2_RESULTS_20260622.md`,
  `refine-logs/SCBGRL_M0_M1_RESULTS_20260622.md`, and
  `refine-logs/GDC_M0_M1_RESULTS_20260622.md`.
- 2026-06-22: Implemented TD-GCL (Training-Dynamics Graph Contrastive
  Learning) after RSP was downgraded. Added
  `baselines/BGRL/train_tdgcl_transductive.py` and `reproduce_dcgcl.py
  --variants tdgcl`. TD-GCL uses similar EMA embedding update directions as
  dynamic positives during BGRL training. M0 smoke passed. Split-0 M1 evidence:
  Cora improves from no-dynamics `0.807107` to `0.842640`; CiteSeer improves
  `0.712622` to `0.729527`; Chameleon improves `0.467105` to `0.478070`;
  Texas/Wisconsin show no gain and remain below raw. No NaN/collapse. Decision:
  TD-GCL is `SPECULATIVE_INCUBATE`, not `READY_TO_REFINE`. Quick novelty risk:
  IFL-GCL/DGCL-PU already cover PU-style semantic positive mining, and dynamic
  positive mining exists in nearby graph contrastive/clustering work; TD-GCL's
  possible delta is embedding update-direction positives. Next action is deeper
  novelty check, then Cora/CiteSeer robustness and raw-dominant reliability
  gating if novelty survives. Report:
  `refine-logs/TDGCL_M0_M1_RESULTS_20260622.md`.
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
- Parallel idea screening preference: when GPU utilization is low, use at most
  two concurrent sub-agent workers for early idea pilots. Workers may run CUDA
  smoke/split-0 gates in their own forked workspaces and distinct output dirs,
  but any positive result must be re-run by the main thread in the canonical
  workspace before it can become an active method. Final node-classification
  probes remain canonical CPU sklearn unless a GPU probe is separately
  equivalence-validated. Protocol:
  `refine-logs/PARALLEL_IDEA_BATCH_PROTOCOL_20260622.md`.
- For evaluation speed, GPU is preferred for protocol-equivalent tensor work
  such as encoder forward passes, propagation, cosine/lift diagnostics, and
  matrix statistics. Final node-classification linear probes should stay on
  canonical CPU sklearn by default; use a GPU probe only after an explicit
  equivalence check shows it does not change the reported protocol.
- For actual model training, prefer GPU/CUDA by default. Launch training scripts
  with `--device=auto` or `--device=cuda` when supported, and verify CUDA usage
  with logs or `nvidia-smi` after launch. Clearly distinguish CPU-only
  training-free evaluation / sklearn linear probes from GPU training.
- For evaluation, use GPU acceleration when it preserves the same mathematical
  evaluation protocol, such as encoder forward passes, torch sparse/dense
  propagation, batched cosine/distance computation, and tensor reductions.
  Do not replace canonical CPU `sklearn` linear-probe / logistic-regression
  solvers with GPU alternatives for final paper numbers unless an explicit
  equivalence check passes; GPU-only probe variants are acceptable for fast
  screening and must be labeled as such.

This workspace is a research project for graph contrastive learning node
classification. The previous selected research direction was NFR-GCL
(Node-Frequency Routed Graph Contrastive Learning), but it was abandoned on
2026-06-21 before implementation because the chance of making it a strong new
paper contribution is low after novelty checking.

Key artifacts:
- `MANIFEST.md` tracks ARIS-generated outputs.
- `idea-stage/IDEA_REPORT.md` currently marks `NO_ACTIVE_MAIN_METHOD`; it
  records LIFT-Portfolio as the strongest low-novelty training-free control.
- `idea-stage/IDEA_CANDIDATES.md` ranks LIFT-Portfolio as
  `STRONG_BASELINE_LOW_NOVELTY`, keeps LIFT-PROP as
  `SELECTOR_BASELINE_NOT_MAIN_METHOD`, and lists remaining backup families for
  the next restart.
- `refine-logs/FINAL_PROPOSAL.md` contains the latest LIFT-PROP/LIFT-Portfolio
  selector proposal, now baseline-only rather than paper-ready.
- `refine-logs/EXPERIMENT_PLAN.md` contains the LIFT-PROP/LIFT-Portfolio gate
  plan; R088 makes LIFT-Portfolio the required baseline for restart.
- `refine-logs/EXPERIMENT_TRACKER.md` tracks R049-R088 and marks the current
  post-TDGCL queue exhausted except for LIFT-Portfolio as a strong baseline.
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
- The latest tested candidate is LIFT-Portfolio, now the strongest training-free
  baseline but low-novelty rather than a final method.
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
