# Research Findings

## 2026-06-22: RSP-GCL downgraded after M2-M4 gate and novelty check

**Verdict**: diagnostic-only, not a final 2026 paper-level method.

RSP-GCL completed the required Chameleon 10-split training, validation-selected
raw/role gate, and direct novelty check. The empirical signal is real but too
conditional: Chameleon role-fused training reaches `0.573684 +/- 0.026265`, and
the validation gate selects `graph_raw_role` in 10/10 splits with
`0.574781 +/- 0.023321`. However, Texas and Wisconsin are raw-dominant:
RSP role-fused is `0.727027` / `0.774510` while raw is `0.829730` / `0.839216`.
Validation selection mostly falls back to raw (`0.827027` Texas,
`0.827451` Wisconsin), which protects against damage but does not create a
broad method gain.

Novelty is also too crowded. GALE already uses node equivalence as a central
self-supervised graph learning principle, WLGCL directly uses WL structural
similarity to construct GCL positives, and SPGCL shows positive-sample GCL is
still an active 2026 direction. RSP should remain a diagnostic baseline for
Chameleon-like role signatures, not a main method for external baseline
expansion.

Recommended next action: restart idea discovery with a different mechanism
family. Avoid generic node-equivalence/WL-positive claims and avoid methods
whose only gain comes from concatenating static handcrafted signatures.

## 2026-06-22: RSP-GCL is the new active role-signature candidate

**Verdict**: active with scope limit, not paper-ready yet.

After CIG/CLEAR failed, a fresh idea-discovery pass moved to structural role equivalence rather than spectral fusion, semantic kNN, local transport, prototypes, residual targets, or edge masks. The new candidate is RSP-GCL: Role-Signature Positive Graph Contrastive Learning. It builds label-free role/WL/landmark signatures and uses them to define nonlocal role-equivalent positives for a BGRL-style objective.

Key evidence:

- Chameleon 10-split zero-training proxy: `graph_raw_role_wl_landmark = 0.585965 +/- 0.026073`, far above `graph_raw = 0.496711` and previous DCA best `0.505044`.
- RSP-GCL training split-0: Chameleon role-fused `0.596491`, no NaN/collapse.
- Texas/Wisconsin remain raw-dominant: full role proxy `0.678378` / `0.719608` vs raw `0.829730` / `0.839216`.

Recommended next action: run Chameleon 10-split RSP training, add a role gate over `{0, role}` to protect raw-dominant graphs, and run a direct novelty check against Str-GCL, CoRep, H3GNNs/HarmonyGNNs, structural encoders, and WL/role-positive GCL.

## 2026-06-22: SRLP main-method claim invalidated

**Verdict**: negative, high confidence.

The SRLP / SRLP-Aux / Adaptive-Aux line should not continue as a main graph SSL method. Residual-only SRLP failed the small heterophily split-0 gate, SRLP-Aux did not beat target-family ablations across 10 Geom-GCN splits, and Adaptive-Aux only produced a local Wisconsin split-0 positive signal while hurting Chameleon and Texas.

What remains useful:

- target-incident-edge hard isolation reduces leakage;
- shortcut leakage reduction does not automatically imply better downstream node classification;
- projection/residual target components have dataset-dependent semantic value.

Constraint for future ideas: do not assume that removing context-predictable latent components is beneficial. Any future latent-prediction GCL idea must show that its target remains task-relevant, not merely shortcut-resistant.

Recommended next action: re-run idea discovery with this failure mode as a constraint.

## 2026-06-22: Fresh idea discovery selected DCGCL for pilot

**Verdict**: paper-only active route, no GPU evidence yet.

The new candidate is DCGCL, Disagreement-Calibrated Prototype Graph Contrastive Learning. It replaces SRLP-style residual latent prediction with a label-free prototype objective built from two weak teachers: a feature-only teacher and a propagation-view teacher. Agreement between their soft prototype assignments defines reliable global positives; disagreement is kept through dual semantic/topology heads and a gate instead of being forced into one pseudo-class.

Why it was selected: it directly addresses the SRLP lesson that shortcut resistance is not enough; the target must be task-relevant for node classification. It also avoids the abandoned frequency-routing line and does not require LLM/text data.

Next action: implement only the M0/M1/M2 pilot from `refine-logs/EXPERIMENT_PLAN.md`. Do not launch 10-split expansion unless split-0 DCGCL beats or matches the best local controls and the no-dual/no-gate ablations confirm the mechanism.

## 2026-06-22: DCGCL V0 initial pilot did not pass M2

**Verdict**: engineering pass, method gate fail.

DCGCL V0 is implemented and stable in the BGRL harness, but the first split-0 gate is insufficient. It has a small positive signal on Chameleon (`0.4276` vs best local control `0.4232`), ties Wisconsin (`0.5882`), and regresses on Texas (`0.6216` vs `0.6486`) and Cora (`0.7790` vs BGRL `0.8090`). No NaN or collapse occurred.

Lesson: disagreement-calibrated prototypes are not enough in their current shared-bank form. The method likely needs separate aligned feature/topology prototype banks and a stricter high-confidence agreement mask before another M2 run. Do not launch 10-split expansion for DCGCL V0.

## 2026-06-22: DCGCL V1 10-split gate invalidated the main method

**Verdict**: negative for main method, partial diagnostic signal.

DCGCL V1 added separate feature/topology prototype banks, greedy alignment, and a high-confidence agreement mask. Split-0 looked promising on Texas and Wisconsin, but 10-split validation did not hold: Chameleon `0.40658` vs best control `0.50044`, Texas `0.58649` vs `0.61351`, Wisconsin `0.60392` vs `0.55490`. Run integrity was clean: 30/30 rows, no NaN/collapse.

What remains useful: low feature/topology prototype alignment may identify a subset of graphs where dual prototype supervision helps, as Wisconsin improved on 8/10 splits. This is not enough for a 2026 paper-level graph contrastive learning method.

Recommended next action: stop DCGCL as a main route and restart idea discovery with two hard constraints: avoid residual targets whose label alignment is unproven, and avoid global prototype positives unless the method has a dataset-robust, label-free activation rule validated before training.

## 2026-06-22: FTDR-BGRL was stable but not positive

**Verdict**: weak / deprioritized.

FTDR-BGRL routed each node's bootstrap target between a topology teacher and a feature-only teacher using feature-topology disagreement. It avoided the exact SRLP/DCGCL failure modes, but split-0 evidence was not positive: Cora nearly tied BGRL (`0.8076` vs `0.8090` after raising `route_tau`), Chameleon remained below control (`0.4035` vs `0.4232`), and Texas/Wisconsin only tied control (`0.6486`, `0.5882`). No NaN/collapse occurred.

Lesson: the project should stop exploring simple latent-target routing variants for now. The next idea search should move to a different mechanism family rather than adding more route thresholds.

## 2026-06-22: RFA-BGRL exposed feature-signal forgetting but is not final

**Verdict**: strongest current diagnostic baseline, not yet a 2026 paper-level method.

After FTDR, CFR-BGRL tested a learned graph channel plus learned feature channel. It was stable but failed split-0: Cora `0.8002` vs BGRL `0.8090`, Chameleon `0.4079` vs `0.4232`, Texas tied `0.6486`, and Wisconsin regressed to `0.5294`. The key lesson was that a learned bootstrap feature channel can still forget raw-feature label signal.

RFA-BGRL then preserved raw features as an explicit anchor and concatenated them with a BGRL graph branch. It is stable and strong on Texas/Wisconsin: 10-split 200-epoch means are Texas `0.7622` and Wisconsin `0.8098`, far above prior local GCL controls. However, raw-only is still stronger on those datasets (`0.8297` and `0.8392`), so this is mostly feature retention rather than a new graph-contrastive mechanism.

Chameleon remains the decisive weakness. RFA improves over raw-only and graph-only, and 1000-epoch split-0 reaches `0.5022`, but 10-split 1000-epoch mean is `0.4928`, slightly below the strict prior control around `0.5004`.

Recommended next action: keep RFA as a required baseline and move the method to ORFA-GCL: a protected raw-feature anchor plus an explicitly complementary graph residual branch. Do not claim RFA itself as the final paper method.

## 2026-06-22: ORFA and BiFilter failed; FBA-GCL is the next focused gate

**Verdict**: ORFA-GCL and BiFilter-BGRL are stopped; FBA-GCL is diagnostic-only after the training gate failed.

ORFA-GCL preserved a raw-feature anchor and tried to train the graph branch as a complementary residual. It was stable, but the decisive results were not enough: Chameleon 1000 split-0 reached only `0.484649`, below RFA; Texas stayed below raw-only; Wisconsin only tied raw-only.

BiFilter-BGRL added a trainable low-pass GCN branch and high-pass residual-feature MLP branch. It also stayed stable but failed split-0: Cora `0.702815`, Chameleon `0.458333`, Texas `0.729730`, Wisconsin `0.666667`. A naive high-pass branch is not a good method.

The useful signal came from deterministic filter anchors. Training-free diagnostics show Cora/CiteSeer benefit from `P^2X`, Texas can benefit from `X-P^4X`, and Chameleon improves only when a learned graph view is combined with raw plus a small low/high filter anchor. Re-evaluating existing RFA Chameleon 1000 checkpoints across 10 official splits gives:

- `graph+raw`: `0.496711 +/- 0.022175`;
- `graph+raw+0.5H1`: `0.500219 +/- 0.020769`;
- `graph+raw+P4`: `0.500219 +/- 0.018697`.

The reusable FBA evaluator and trainable FBA implementation were added. The post-hoc filterbank signal reproduced, but the trainable anchor auxiliary failed the strict Chameleon 10-split gate:

- FBA-high1 train: `0.487061 +/- 0.025714`;
- same-run graph_raw: `0.493202 +/- 0.025013`;
- NaN/collapse: 0.

Recommended next action: keep FBA as a diagnostic/post-hoc filterbank baseline, or redesign the anchor selection/training objective before any new 10-split run. Do not launch a main-table expansion or claim a 2026 paper-level method from current FBA.

## 2026-06-22: SBN failed; DCA-GCL is the current empirical lead

**Verdict**: DCA is edge-positive but not paper-ready; novelty/method review is mandatory.

After FBA training failed, a fresh idea-discovery pass tested a different mechanism family, SBN-GCL: semantic raw-feature kNN positives plus low-similarity edge boundary negatives. SBN was stable but failed the split-0 gate: Chameleon fused `0.462719`, Texas `0.729730`, and Wisconsin `0.784314`, all below the relevant raw or local controls. Chameleon ablations without boundary loss or with larger positive neighborhoods also failed, so SBN should stop.

The useful signal came from deferred complementary anchors. DCA-GCL keeps filter anchors out of the training objective and fuses them only after the graph encoder is trained. On Chameleon 10 official splits, DCA improved over graph_raw and one-anchor FBA:

- `graph_raw`: `0.496711 +/- 0.022175`;
- `fba_h1`: `0.500219 +/- 0.020769`;
- `dca_h1_p4`: `0.505044 +/- 0.022791`;
- `dca_h1_h4_p4`: `0.505044 +/- 0.019908`.

Cora and CiteSeer also improve over graph_raw, but Texas/Wisconsin remain raw-dominant (`raw 0.829730/0.839216`, best DCA/FBA family below raw). Recommended next action: strict novelty/method review against ASPECT, FC-GSSL, SPGCL, Less is More, HLCL/GREET/SIGNA, and simple graph-feature fusion. Do not expand DCA to external baselines or claim a final paper method yet.

## 2026-06-22: DCA novelty failed; restart from a transport-style speculative route

**Verdict**: DCA is diagnostic-only, no active ready method yet.

The DCA novelty check scored only `3/10`. Closest work already covers the major pieces: ASPECT and LOHA cover low/high spectral GCL, HLCL covers heterophily-aware graph filters, FC-GSSL covers frequency-aware graph SSL, Less is More and FB-GCL cover graph/feature complementary fusion, and GCL-GroW/GWGCL cover whitening-style rescue ideas. The only defensible DCA contribution is a diagnostic finding: training-time filter-anchor alignment can hurt, while deferred anchors can be a useful baseline.

Two quick rescue probes did not produce a new main route. Semantic kNN anchors were weak: Cora/CiteSeer had small signal, but Chameleon did not beat graph_raw and Texas/Wisconsin remained raw-dominant. ZCA/whitening timed out in the quick loop and is not cleanly novel.

Recommended next action: do not tune DCA. The next eligible candidate is VST-GCL, a sparse local transport target between topology-neighborhood mass and raw-feature semantic mass. Treat it as speculative; run only a split-0 proxy before any 10-split or baseline expansion.

## 2026-06-22: VST-GCL transport target failed the split-0 gate

**Verdict**: stop VST; restart idea discovery.

VST-GCL implemented a sparse local transport target between raw-feature semantic neighbors and graph topology support. Engineering passed: smoke ran on Cora/Chameleon with no NaN/collapse. The 200-epoch split-0 gate failed:

- Cora fused `0.814490`, below prior anchor controls;
- Chameleon fused `0.469298`, below graph_raw/DCA controls;
- Texas fused `0.729730`, below raw `0.810811`;
- Wisconsin fused `0.803922`, below raw `0.823529`.

A low-auxiliary ablation (`lambda_bgrl=1.0`, `lambda_transport=0.1`) also failed: Cora fused `0.810337`, Chameleon fused `0.467105`. Transport diagnostics showed low stable support mass on Chameleon/Texas, so the method mostly degenerates toward semantic-kNN-like positives, which were already weak.

Recommended next action: do not tune VST. Restart idea discovery with a genuinely different mechanism family.

## 2026-06-22: CIG/CLEAR edge-influence route failed as a main method

**Verdict**: stop CIG/CLEAR.

A counterfactual edge-mask evaluator was added before implementing a full training objective. On split 0, edge masks did not improve Cora or Chameleon; Texas improved over fused RFA but stayed below raw; Wisconsin showed a local positive (`0.843137` vs raw `0.823529`).

The Wisconsin signal did not survive the 10-split check. On Wisconsin, the best fixed mask reached `0.823529` and validation-selected masks reached `0.827451`, both below raw `0.839216`. On Texas, the best fixed mask reached `0.794595` and validation-selected masks reached `0.805405`, both below raw `0.829730`.

Recommended next action: do not implement CIG/CLEAR training. Restart wide idea discovery with a different mechanism family.
