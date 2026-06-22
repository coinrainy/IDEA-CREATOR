# Post-CIG Wide Idea Discovery: RSP-GCL

**Date**: 2026-06-22  
**Direction**: graph contrastive learning for node classification  
**Current active idea**: RSP-GCL, Role-Signature Positive Graph Contrastive Learning  

## 背景

SRLP、DCGCL、FTDR/CFR/RFA/ORFA、FBA/DCA、SBN、VST、CIG/CLEAR 都已被实验或新颖性审查降级。新的搜索必须避开以下机制：

- residual latent prediction
- prototypes / pseudo class positives
- feature-teacher routing
- fixed low/high spectral filters
- raw/graph/filter deferred fusion as main contribution
- semantic kNN positives
- local transport targets
- counterfactual edge masks
- whitening rescue

## 最新文献边界

近期工作使常规路线高度拥挤：

- ASPECT: node-wise spectral contrast and reliability-aware spectral gating, 2026.
- PROPGCL: propagation-only / learnable propagation as a strong GCL baseline, 2026.
- H3GNNs / HarmonyGNNs: joint structural node encoding and SSL for heterophily/homophily, 2025/2026.
- Str-GCL: structural commonsense rules inside GCL, WWW 2025.
- CoRep: coloring learning and multi-hop same-color positives for heterophilic graph representation, NeurIPS 2025.
- HLCL: heterophily graph filters for GCL.

因此，新方法不能只说“结构视图”“异配图”“高频/低频”“全局正样本”。必须有更窄的差异点和明确的负迁移保护。

## Candidate Pool

| # | Candidate | Bucket | Status | Reason |
|---:|---|---|---|---|
| 1 | RSP-GCL | role / position | ACTIVE | Chameleon 10-split role-signature proxy is strongly positive |
| 2 | validation-gated RSP | role / gate | ACTIVE_NEXT | needed to protect Texas/Wisconsin |
| 3 | label-free role reliability gate | role / gate | SPECULATIVE | avoids validation-tuned representation choice |
| 4 | role-only graph tokenizer | graph tokenizer | BACKUP | close to structural encoder papers |
| 5 | motif-role positive GCL | role / motif | HOLD | likely close to Str-GCL and structural role SSL |
| 6 | landmark diffusion contrast | position | HOLD | positive only as part of role signature |
| 7 | WL-hash neighborhood contrast | role | HOLD | strong Chameleon component, novelty needs check |
| 8 | training-dynamics easy/hard positive curriculum | dynamics | SPECULATIVE | different family, not tested |
| 9 | representation-forgetting contrast | dynamics | SPECULATIVE | may be expensive and unstable |
| 10 | confidence-calibrated BGRL target | dynamics | DEPRIORITIZED | resembles previous teacher/routing failures |
| 11 | role-conditioned invariance across augmentations | invariance | BACKUP | could combine with RSP if gate passes |
| 12 | graph-size normalized local rank contrast | rank | SPECULATIVE | no pilot yet |
| 13 | local ordinal-neighborhood consistency | rank | HOLD | risks overlap with ranking-based GSSL |
| 14 | signed role incompatibility negatives | contrastive negatives | BACKUP | useful ablation for RSP |
| 15 | raw-feature residual role branch | branch | DEPRIORITIZED | too close to failed residual/fusion routes |
| 16 | edge-label-free structural environment GCL | causal / env | HOLD | CIG/CLEAR edge route failed nearby |
| 17 | subgraph automorphism contrast | structural | SPECULATIVE | expensive and novelty uncertain |
| 18 | ego-net compression target | structural prediction | BACKUP | close to structural encoders |
| 19 | heterophily coloring plus role signature | coloring | KILLED_FOR_NOW | too close to CoRep |
| 20 | propagation-coefficient role gating | propagation | DEPRIORITIZED | too close to PROPGCL/ASPECT |
| 21 | spectral role-frequency cross objective | spectral | KILLED_FOR_NOW | too close to ASPECT/HLCL/LOHA |
| 22 | contrastive graph prompt tokens | prompt | SPECULATIVE | requires broader code stack |
| 23 | validation-supervised role contrast | semi-supervised | HOLD | easier gains but changes claim type |
| 24 | role-signature distillation without graph encoder | diagnostic | BACKUP | may become a baseline, not main GCL |

## Why RSP-GCL Survived

RSP-GCL tested a mechanism that is genuinely different from recent failed attempts: structural role equivalence rather than feature similarity, edge deletion, spectral fusion, or prototype membership.

Zero-training proxy:

| Dataset | Key result | Decision |
|---|---:|---|
| Chameleon 10-split | `graph_raw_role_wl_landmark = 0.585965` vs `graph_raw = 0.496711`, DCA best `0.505044` | strong positive |
| Texas 10-split | raw `0.829730` vs role full `0.678378` | role must be gated off |
| Wisconsin 10-split | raw `0.839216` vs role full `0.719608` | role must be gated off |

Training prototype:

| Dataset | RSP Role-Fused Split-0 | Raw | Decision |
|---|---:|---:|---|
| Chameleon | 0.596491 | 0.440789 | positive |
| Texas | 0.702703 | 0.810811 | gate required |
| Wisconsin | 0.725490 | 0.823529 | gate required |

## Current Thesis

Some heterophilic graphs are not best explained by adjacent-node similarity, raw-feature similarity, or low/high-frequency mixtures. Chameleon shows a stronger signal from nonlocal structural role equivalence: nodes with similar ego role, WL neighborhood pattern, and landmark diffusion response become useful positive pairs even when their local edges are heterophilic.

RSP-GCL turns this into a graph contrastive objective by using role signatures to define nonlocal positives and a role prediction head to stabilize the graph encoder. A role branch is used only when validation or a reliability gate indicates that role signatures carry downstream signal.

## Go / No-Go

Current status: `ACTIVE_WITH_SCOPE_LIMIT`.

Promote to `READY_TO_REFINE` only if:

- Chameleon 10-split training version stays close to the proxy gain.
- A validation-selected or label-free role gate preserves Texas/Wisconsin raw performance.
- Direct novelty search does not find an existing WL/role/landmark-positive GCL with the same mechanism.

