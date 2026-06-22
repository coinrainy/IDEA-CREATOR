# RSP-GCL M2-M4 Results and Novelty Gate

**Date**: 2026-06-22  
**Status**: `DIAGNOSTIC_ONLY_AFTER_GATE`  
**Candidate**: RSP-GCL, Role-Signature Positive Graph Contrastive Learning  

## 结论

RSP-GCL 不适合作为当前 2026 论文级主线继续扩展。

实验证据是条件性正信号：Chameleon 上 role/WL/landmark signature 仍然很强，验证集也会稳定选择 `graph_raw_role`。但 Texas/Wisconsin 上 raw 特征明显主导，role-fused 分支稳定负迁移；验证集门控只能大致保护 raw，不能产生跨数据集增益。

新颖性也不够干净。GALE 已经把节点等价类用于自监督图学习作为 ICML 2025 oral 主线；WLGCL 直接使用 WL 结构相似性构造 GCL 正样本；SPGCL 在 2026-06-09 又进一步刷新了 positive-sample GCL 方向。因此，RSP 不能声称“结构角色正样本”或 “WL structural positives” 是新的核心贡献。

当前保留价值：RSP 是一个强诊断，说明 Chameleon 类图存在可由无标签 role/WL/landmark signature 捕获的非局部角色信号。它可以作为后续方法的分析工具或 baseline，不应作为主方法继续跑外部强基线或大图。

## M2: Chameleon 10-Split RSP Training

Command:

```text
python .\reproduce_dcgcl.py --datasets chameleon --variants rsp --splits 0,1,2,3,4,5,6,7,8,9 --epochs 200 --eval_epochs 50 --output_dir runs/rsp_m2_chameleon10_20260622 --clean --results_csv runs/rsp_m2_chameleon10_20260622/results.csv
```

CSV:

```text
baselines/BGRL/runs/rsp_m2_chameleon10_20260622/results.csv
```

| Representation | Mean Test | Std | Interpretation |
|---|---:|---:|---|
| raw | 0.456798 | 0.017763 | weak |
| graph only `test@best` | 0.429825 | 0.025873 | weak |
| graph+raw `fused_test@best` | 0.470175 | 0.016417 | below old RFA/DCA controls |
| graph+raw+role `role_fused_test@best` | 0.573684 | 0.026265 | strong on Chameleon |

Integrity: 10/10 rows completed, `nan_flag=0`, `collapse_flag=0`.

Interpretation: RSP preserves the Chameleon role-signature signal during training, but the graph encoder itself is not the source of the gain. The gain mostly comes from concatenating the static role signature with graph/raw features.

## M3: Chameleon Validation-Selected Gate

Command:

```text
python .\evaluate_rsp_gate.py --dataset chameleon --splits 0,1,2,3,4,5,6,7,8,9 --checkpoint_template 'runs/rsp_m2_chameleon10_20260622/{dataset}/rsp/seed_0_split_{split}_e200/checkpoint.pt' --representations raw,graph_raw,graph_raw_role --output_csv runs/rsp_gate_m2_chameleon10_20260622/chameleon.csv
```

CSV:

```text
baselines/BGRL/runs/rsp_gate_m2_chameleon10_20260622/chameleon.csv
```

| Representation | Mean Test | Std | Selected Count |
|---|---:|---:|---:|
| raw | 0.456798 | 0.017763 | 0/10 |
| graph_raw | 0.474123 | 0.020497 | 0/10 |
| graph_raw_role | 0.574781 | 0.023321 | 10/10 |
| validation-selected | 0.574781 | 0.023321 | 10/10 |

Interpretation: on Chameleon, validation selection is not post-hoc cherry-picking; it consistently selects the role-augmented representation.

## M4: Texas/Wisconsin RSP Training and Gate

Command:

```text
python .\reproduce_dcgcl.py --datasets texas,wisconsin --variants rsp --splits 0,1,2,3,4,5,6,7,8,9 --epochs 200 --eval_epochs 50 --output_dir runs/rsp_m2_webkb10_20260622 --clean --results_csv runs/rsp_m2_webkb10_20260622/results.csv
```

CSV:

```text
baselines/BGRL/runs/rsp_m2_webkb10_20260622/results.csv
baselines/BGRL/runs/rsp_gate_m2_webkb10_20260622/texas.csv
baselines/BGRL/runs/rsp_gate_m2_webkb10_20260622/wisconsin.csv
```

Training summary:

| Dataset | Raw | Graph+Raw | Graph+Raw+Role | NaN/Collapse | Interpretation |
|---|---:|---:|---:|---|---|
| Texas | 0.829730 ± 0.048423 | 0.759459 ± 0.037156 | 0.727027 ± 0.054659 | 0/0 | role branch hurts |
| Wisconsin | 0.839216 ± 0.040942 | 0.807843 ± 0.045395 | 0.774510 ± 0.033102 | 0/0 | role branch hurts |

Validation-selected gate:

| Dataset | Raw Mean | GraphRaw Mean | GraphRawRole Mean | Val-Selected Mean | Selection Pattern | Interpretation |
|---|---:|---:|---:|---:|---|---|
| Texas | 0.829730 | 0.751351 | 0.729730 | 0.827027 | raw 9, graph_raw 1, role 0 | mostly protects raw |
| Wisconsin | 0.839216 | 0.796078 | 0.754902 | 0.827451 | raw 9, role 1 | one role mis-selection hurts |

Interpretation: validation selection can reduce damage, but it does not create a positive method effect on raw-dominant WebKB graphs. A method that merely learns to fall back to raw is not enough for a graph contrastive learning paper claim.

## Novelty Gate

Close priors:

- GALE, **Equivalence is All: A Unified View for Self-supervised Graph Learning**, ICML 2025 oral: unifies automorphic and attribute equivalence, constructs approximate equivalence classes, and enforces them in self-supervised graph learning. This directly overlaps with the RSP idea of role-equivalent nodes.
- WLGCL, **Graph Contrastive Learning via Weisfeiler-Leman Dual-View Sampling**, TMLR submission: uses WL structural similarity and feature similarity to construct reliable positives and hard negatives. This is a direct blocker for generic WL/structure-positive claims.
- SPGCL, **Revisiting Positive Samples in Graph Contrastive Learning: From the Perspective of Message Passing**, arXiv:2606.10284, 2026-06-09: shows positive-sample learning is a crowded and actively moving 2026 topic, with energy-guided positive sampling and propagation.

Sources:

```text
https://openreview.net/forum?id=ZAlII9wL5i
https://proceedings.mlr.press/v267/wang25ez.html
https://openreview.net/attachment?id=uuk14WVKyj&name=pdf
https://arxiv.org/abs/2606.10284
https://arxiv.org/html/2606.10284v1
```

Defensible remaining RSP claim is narrow:

> A label-free role/WL/landmark signature is an effective diagnostic and post-hoc feature source for Chameleon-like heterophily graphs, but it is not a broadly positive GCL training objective and not novel enough as a standalone structural-positive method.

## Decision

RSP-GCL is downgraded from `ACTIVE_WITH_SCOPE_LIMIT` to `DIAGNOSTIC_ONLY_AFTER_GATE`.

Do not run external baselines, large graphs, or paper-table expansion for RSP. The next pipeline step should restart idea discovery with a different mechanism family, using the RSP lesson as a constraint:

1. avoid generic node-equivalence/WL-positive claims;
2. avoid methods whose only success comes from concatenating static handcrafted features;
3. require a label-free activation rule that gives actual gains rather than merely falling back to raw;
4. keep Chameleon role signatures as a diagnostic baseline for future candidates.
