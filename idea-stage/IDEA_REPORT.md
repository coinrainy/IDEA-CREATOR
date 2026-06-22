# Idea Discovery Report: Role-Signature Positive GCL

**Date**: 2026-06-22  
**Current status**: `DIAGNOSTIC_ONLY_AFTER_GATE`  
**Latest decision**: RSP-GCL has been downgraded after M2-M4; DCA/VST/CIG/CLEAR remain stopped and no method is currently ready to refine.

## 2026-06-22 M2-M4 Update

RSP-GCL passed a narrow Chameleon gate but failed as a broad paper-level route.
Chameleon 10-split RSP training gives `role_fused_test@best = 0.573684 +/-
0.026265`, and validation selection chooses `graph_raw_role` in 10/10 splits
with `0.574781 +/- 0.023321`. Texas/Wisconsin remain raw-dominant: raw
`0.829730` / `0.839216` beats role-fused `0.727027` / `0.774510`, and
validation-selected fallback reaches only `0.827027` / `0.827451`.

Novelty check also weakens the route: GALE covers node equivalence in graph SSL,
WLGCL directly uses WL structural similarity for GCL positives, and SPGCL shows
positive-sample GCL is crowded in 2026. RSP should be kept as a diagnostic
baseline, not a main method. Full report:
`refine-logs/RSP_M2_M4_RESULTS_20260622.md`.

## Executive Summary

重新宽搜索后，当前最强新方向是 **RSP-GCL**（Role-Signature Positive Graph Contrastive Learning）。它用无标签结构角色签名构造非局部正样本：local role statistics、WL-hash neighborhood signature、landmark diffusion signature。这个机制避开了前面失败或低新颖性的谱融合、固定滤波器、语义 kNN、原型、残差预测、local transport 和 counterfactual edge mask 路线。

最强证据来自 Chameleon：在已有 RFA/BGRL 1000-epoch checkpoints 上做 zero-training proxy，`graph_raw_role_wl_landmark` 的 10-split mean test 为 `0.585965`，明显高于 `graph_raw=0.496711` 和此前 DCA 最好 `0.505044`。训练版 RSP-GCL split-0 也稳定，Chameleon `role_fused_test@best=0.596491`，无 NaN/collapse。

限制也很明确：Texas/Wisconsin 是 raw-feature-dominant，role branch 会负迁移。RSP-GCL 不能直接扩成“所有异配图无条件提升”的主张，必须加入验证集选择或 label-free role gate。

## Literature Boundary

近邻工作已经覆盖常规路线：

- ASPECT: node-wise spectral gating and adaptive spectral contrast.
- PROPGCL: propagation-only GCL and learnable propagation as a strong simple baseline.
- H3GNNs / HarmonyGNNs: joint structural node encoding with SSL.
- Str-GCL: structural commonsense rules in GCL.
- CoRep: coloring learning and multi-hop same-color positives for heterophily.
- HLCL: heterophily graph filters.
- Less is More: graph/feature complementary GCL.

RSP-GCL 的可辩护差异点不是“结构 GCL 首创”，而是更窄的：基于 role/WL/landmark signature 的非局部 role-equivalent positives，并且对 raw-dominant 图门控关闭。

## Ranked Current Ideas

| Rank | Candidate | Evidence | Status |
|---:|---|---|---|
| 1 | RSP-GCL | Chameleon 10-split proxy `0.585965`, training split-0 `0.596491` | ACTIVE_WITH_SCOPE_LIMIT |
| 2 | Validation-gated RSP | Texas/Wisconsin need role-off protection; val-selected proxy preserves raw roughly | ACTIVE_NEXT |
| 3 | Label-free role reliability gate | avoids validation-tuned representation choice | SPECULATIVE |
| 4 | WL-only / landmark-only RSP ablations | WL component is strong on Chameleon | BACKUP |
| 5 | Training-dynamics curriculum GCL | different mechanism family, not yet tested | SPECULATIVE |
| 6 | Role-conditioned invariance GCL | may strengthen RSP objective | BACKUP |
| 7 | DCA/AnchorBank | local positive but novelty score only about 3/10 | DIAGNOSTIC_ONLY |
| 8 | VST-GCL / CIG-CLEAR / SBN / SRLP / DCGCL / FTDR / CFR / ORFA / FBA | implemented or diagnosed and failed as main methods | STOP |

## Key Results

### Role-Signature Proxy

| Dataset | Best role result | Control | Decision |
|---|---:|---:|---|
| Chameleon 10-split | `graph_raw_role_wl_landmark` 0.585965 | `graph_raw` 0.496711, DCA 0.505044 | strong positive |
| Texas 10-split | full role 0.678378 | raw 0.829730 | gate required |
| Wisconsin 10-split | full role 0.719608 | raw 0.839216 | gate required |

### RSP-GCL Training Prototype

| Dataset | Graph | Graph+Raw | Graph+Raw+Role | Raw | Verdict |
|---|---:|---:|---:|---:|---|
| Chameleon split 0 | 0.429825 | 0.478070 | 0.596491 | 0.440789 | positive |
| Texas split 0 | 0.648649 | 0.783784 | 0.702703 | 0.810811 | gate required |
| Wisconsin split 0 | 0.568627 | 0.803922 | 0.725490 | 0.823529 | gate required |

## Next Step

Restart idea discovery with a different mechanism family. Keep RSP role
signatures as a Chameleon diagnostic baseline, but do not expand RSP to
external baselines or large graphs.
