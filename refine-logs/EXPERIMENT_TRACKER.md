# Experiment Tracker: RSP-GCL

| Run ID | Milestone | Purpose | Variant | Split | Metrics | Priority | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| R001-R013 | historical | SRLP/DCGCL/FTDR gates | multiple | multiple | node classification | historical | STOP | archived in timestamped result files |
| R014 | M1 | CFR pilot | CFR-BGRL | Cora/Chameleon/Texas/Wisconsin split 0 | test@best | historical | FAIL | stable but non-positive |
| R015-R020 | M2/M3 | RFA feature-retention gates | RFA-BGRL | split 0 and 10-split | raw/graph/RFA test | historical | BASELINE | strong diagnostic, not final method |
| R021 | M1 | ORFA split-0 gate | ORFA-GCL | Cora/Chameleon/Texas/Wisconsin split 0 | ORFA/raw/graph/residual test | historical | FAIL | Cora pass, Chameleon fail, Texas below raw, Wisconsin raw tie |
| R022 | M2 | ORFA Chameleon long gate | ORFA-GCL | Chameleon split 0, 1000 epoch | test@best | historical | FAIL | 0.484649, below RFA |
| R023 | M1 | trainable high-pass/low-pass gate | BiFilter-BGRL | Cora/Chameleon/Texas/Wisconsin split 0 | low/high/fused test | historical | FAIL | naive high-pass branch regressed |
| R024 | M2 | post-hoc filter-bank Chameleon gate | FBA post-hoc | Chameleon splits 0-9 | mean +/- std | historical | EDGE-PASS | `graph+raw+0.5H1` and `graph+raw+P4` both mean 0.500219 |
| R025 | M0 | reusable evaluator | FBA/DCA evaluator | reproduce R024 | csv parity | historical | DONE | `evaluate_filterbank_anchor.py` reproduces post-hoc results |
| R026 | M1 | fixed family split-0 gate | FBA fixed candidates | Cora/CiteSeer/Chameleon/Texas/Wisconsin split 0 | valid/test | historical | DONE | strong Cora, small CiteSeer, heterophily raw/graph dependent |
| R027 | M2 | Chameleon fixed 10-split gate | FBA fixed candidates | Chameleon splits 0-9 | mean +/- std | historical | EDGE-PASS | only narrow positive |
| R028 | M3 | anchor-alignment auxiliary split-0 | FBA train | Cora/CiteSeer/Chameleon/Texas/Wisconsin split 0 | test@best | historical | PARTIAL | Cora strong, CiteSeer small positive, heterophily not enough |
| R029 | M4 | anchor-alignment auxiliary 10-split | FBA-high1 train | Chameleon splits 0-9, 1000 epoch | mean +/- std | historical | FAIL | FBA `0.487061` vs graph_raw `0.493202`; no NaN/collapse |
| R030 | M0 | semantic-boundary alternative | SBN-GCL | Cora/Chameleon/Texas/Wisconsin split 0 | graph/fused/raw test | MUST | FAIL | Cora weak positive only; Chameleon/Texas/Wisconsin fail |
| R031 | M1 | deferred complementary anchor fixed family | DCA-GCL | Chameleon 10 splits; Cora/CiteSeer split 0; Texas/Wisconsin 10 splits | mean/test | MUST | EDGE-PASS | Chameleon `0.505044`, Cora/CiteSeer positive; Texas/Wisconsin raw-dominant |
| R032 | M2 | novelty/method review | DCA-GCL | paper-only review | verdict | MUST | FAIL | novelty score 3/10; keep DCA diagnostic-only |
| R033 | M0 | semantic anchor rescue proxy | Semantic kNN anchor | Cora/CiteSeer/Chameleon/Texas/Wisconsin split 0 | valid/test | SHOULD | FAIL | small Cora/CiteSeer signal only; no decisive heterophily win |
| R034 | M0 | whitening rescue proxy | ZCA/whitening | split-0 quick proxy | runtime/test | SHOULD | FAIL | timed out in 120s and novelty is covered by GCL-GroW/GWGCL |
| R035 | M0/M1 | sparse local transport proxy | VST-GCL default | Cora/Chameleon/Texas/Wisconsin split 0 | test@best | MUST | FAIL | stable but Chameleon/Texas/Wisconsin fail decisive controls |
| R036 | M1 ablation | low-weight transport auxiliary | VST-GCL low aux | Cora/Chameleon split 0 | test@best | SHOULD | FAIL | Chameleon fused 0.467105, no positive mechanism signal |
| R037 | diagnostic | counterfactual edge masks split-0 | CIG/CLEAR proxy | Cora/Chameleon/Texas/Wisconsin split 0 | fused test | SHOULD | PARTIAL_FAIL | only Wisconsin split 0 positive; Chameleon no signal |
| R038 | diagnostic | counterfactual edge masks 10-split | CIG/CLEAR proxy | Texas/Wisconsin splits 0-9 | mean fused test | SHOULD | FAIL | best fixed and validation-selected masks below raw baselines |
| R039 | M0 | role-signature proxy split-0 | RSP role anchor | Cora/Chameleon/Texas/Wisconsin split 0 | valid/test | MUST | PARTIAL_PASS | Chameleon full role 0.596491; Texas/Wisconsin below raw |
| R040 | M1 | Chameleon role-signature proxy 10-split | RSP role anchor | Chameleon splits 0-9 | mean +/- std | MUST | PASS | full role 0.585965 vs graph_raw 0.496711 and DCA 0.505044 |
| R041 | M1 | RSP training split-0 | RSP-GCL | Chameleon/Texas/Wisconsin split 0 | graph/fused/role-fused test | MUST | PARTIAL_PASS | Chameleon role-fused 0.596491; Texas/Wisconsin require gate |
| R042 | M2 | Chameleon RSP training 10-split | RSP-GCL | Chameleon splits 0-9 | role-fused mean +/- std | MUST | PASS_WITH_LIMIT | role-fused 0.573684 +/- 0.026265; no NaN/collapse; gain mostly from static role signature |
| R043 | M3 | validation-selected RSP representation gate | RSP-GCL | Chameleon/Texas/Wisconsin splits 0-9 | selected test mean | MUST | PARTIAL_FAIL | Chameleon selects role 10/10 and reaches 0.574781; Texas/Wisconsin mostly fall back to raw with no gain |
| R044 | M4 | direct novelty gate | RSP-GCL | paper-only check | closest prior overlap | MUST | FAIL | GALE, WLGCL, and SPGCL make generic role/WL positive-sampling claim insufficiently novel |
| R045 | M0 | TD-GCL smoke | TD-GCL | Cora/Chameleon split 0, 5 epoch | NaN/collapse | SHOULD | PASS | dynamic loss warmup inactive; no runtime or collapse issue |
| R046 | M1 | TD-GCL split-0 pilot | TD-GCL lambda_dyn=0.2 | Cora/Chameleon/Texas/Wisconsin split 0 | test@best | SHOULD | PARTIAL_PASS | Cora +3.09, Chameleon +1.10 vs no-dyn; Texas/Wisconsin no gain |
| R047 | M1 ablation | TD-GCL strength check | lambda_dyn=0.0/0.5 | Cora/Chameleon/Texas/Wisconsin split 0 | test@best delta | SHOULD | PARTIAL_PASS | lambda 0.5 improves Cora to 0.842640 but hurts Texas |
| R048 | M1 ablation | TD-GCL CiteSeer check | lambda_dyn=0.0/0.5 | CiteSeer fixed split | test@best delta | SHOULD | PARTIAL_PASS | CiteSeer improves 0.712622 -> 0.729527 |

## Active Rule

No candidate is currently `READY_TO_REFINE`. RSP-GCL is downgraded to a diagnostic baseline after R042-R044. TD-GCL is `SPECULATIVE_INCUBATE`: it has homophily split-0 signal but needs novelty and robustness gates. Do not expand RSP, DCA, VST, CIG, CLEAR, or TD-GCL to external baselines yet.
