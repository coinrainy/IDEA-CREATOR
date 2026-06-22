# RSP-GCL Role-Signature Discovery and Pilot Results

**Date**: 2026-06-22  
**Status**: `DIAGNOSTIC_ONLY_AFTER_GATE`  
**Candidate**: RSP-GCL, Role-Signature Positive Graph Contrastive Learning  

## 2026-06-22 M2-M4 Update

RSP-GCL has been downgraded after the required Chameleon 10-split training,
Texas/Wisconsin gate, and direct novelty check. See
`refine-logs/RSP_M2_M4_RESULTS_20260622.md`.

Key numbers:

| Gate | Result | Decision |
|---|---:|---|
| Chameleon RSP 10-split `role_fused_test@best` | 0.573684 +/- 0.026265 | positive but mostly static role-feature gain |
| Chameleon validation-selected gate | 0.574781 +/- 0.023321 | selects `graph_raw_role` in 10/10 splits |
| Texas validation-selected gate | 0.827027 vs raw 0.829730 | protects raw, no gain |
| Wisconsin validation-selected gate | 0.827451 vs raw 0.839216 | partial protection, no gain |

Novelty gate: GALE (ICML 2025), WLGCL, and SPGCL make the generic
node-equivalence / WL-positive-sampling claim too crowded. RSP should remain a
diagnostic baseline, not a final method route.

## 核心结论

RSP-GCL 是 CIG/CLEAR 失败后重新发现的当前最强候选。它不再沿用谱融合、固定滤波器、语义 kNN、原型、残差预测或边 mask 路线，而是引入无标签结构角色签名：

- local role statistics: degree, PageRank, clustering, triangle/core, neighbor degree histograms。
- WL-hash signature: 用 Weisfeiler-Lehman 式邻域标签哈希捕获结构等价模式。
- landmark diffusion signature: 用少量无标签 landmark 的传播响应刻画图中位置。

这些签名用于构造非局部 role-equivalent positives，并作为 role view 参与下游表示。当前证据显示它对 Chameleon 这类结构角色强相关的异配图非常有效，但对 Texas/Wisconsin 这类 raw-feature-dominant 小图会负迁移。因此下一步必须做门控或验证集选择，而不是无条件启用 role 分支。

## 代码与输出

新增代码：

```text
baselines/BGRL/evaluate_role_position_anchor.py
baselines/BGRL/train_rsp_transductive.py
baselines/BGRL/reproduce_dcgcl.py --variants rsp
```

主要结果：

```text
baselines/BGRL/runs/role_position_proxy_20260622/chameleon10.csv
baselines/BGRL/runs/role_position_proxy_20260622/texas10.csv
baselines/BGRL/runs/role_position_proxy_20260622/wisconsin10.csv
baselines/BGRL/runs/rsp_m0_smoke_20260622/results.csv
baselines/BGRL/runs/rsp_m1_split0_20260622/results.csv
```

验证：

```text
python -m py_compile .\reproduce_dcgcl.py .\train_rsp_transductive.py .\evaluate_role_position_anchor.py
python .\reproduce_dcgcl.py --datasets chameleon --variants rsp --epochs 5 --eval_epochs 5 --dry_run --output_dir runs/rsp_dryrun
```

两项均通过。

## Zero-Training Proxy: Role-Signature Anchor

### Chameleon 10 Splits

使用已有 RFA/BGRL 1000-epoch checkpoints，只改变线性评估输入。

| Representation | Mean Test | Std | Verdict |
|---|---:|---:|---|
| `raw` | 0.456798 | 0.017763 | weak |
| `graph_raw` | 0.496711 | 0.022175 | baseline |
| `raw_role` | 0.501316 | 0.020993 | small positive |
| `graph_raw_role` | 0.546930 | 0.021334 | strong positive |
| `graph_raw_wl` | 0.578290 | 0.025837 | strong positive |
| `graph_raw_role_wl` | 0.583333 | 0.020431 | strong positive |
| `graph_raw_role_wl_landmark` | 0.585965 | 0.026073 | best fixed |
| validation-selected over tested reps | 0.585746 | n/a | robust |

Interpretation: role/WL/landmark signatures give a much larger Chameleon gain than previous DCA (`0.505044`). This is not a small local tuning effect.

### Texas / Wisconsin 10 Splits

| Dataset | Raw | GraphRaw | Raw+Role | Full Role Signature | Val-Selected | Verdict |
|---|---:|---:|---:|---:|---:|---|
| Texas | 0.829730 | 0.751351 | 0.794595 | 0.678378 | 0.824324 | raw dominates |
| Wisconsin | 0.839216 | 0.792157 | 0.825490 | 0.719608 | 0.841176 | raw dominates |

Interpretation: role signatures are harmful when raw features already solve the task. A publishable method must include a gate or validation-selected role weight.

## Training Prototype: RSP-GCL

RSP-GCL adds two objectives to BGRL:

1. role-positive InfoNCE: positives are top-k nodes under role-signature similarity, not raw-feature kNN or adjacent nodes.
2. role-anchor prediction: online graph embedding predicts the role signature through a small projector.

Split-0 200-epoch pilot:

| Dataset | Graph Test@Best | Graph+Raw Test@Best | Graph+Raw+Role Test@Best | Raw | Role Only | NaN | Collapse |
|---|---:|---:|---:|---:|---:|---|---|
| Chameleon | 0.429825 | 0.478070 | 0.596491 | 0.440789 | 0.572368 | false | false |
| Texas | 0.648649 | 0.783784 | 0.702703 | 0.810811 | 0.621622 | false | false |
| Wisconsin | 0.568627 | 0.803922 | 0.725490 | 0.823529 | 0.549020 | false | false |

Interpretation: the training prototype is stable and preserves the Chameleon role signal, but role fusion must be disabled or downweighted on raw-dominant datasets.

## Novelty Boundary

Close papers:

- ASPECT covers node-wise spectral gating and adaptive low/high spectral contrast.
- PROPGCL shows propagation-only contrast can beat heavier GCL encoders.
- H3GNNs/HarmonyGNNs use joint structural node encoding and SSL for heterophily/homophily.
- Str-GCL injects structural commonsense rules into GCL.
- CoRep uses coloring learning and multi-hop same-color positives for heterophily.
- HLCL covers homophily/heterophily graph filters.

Defensible delta for RSP-GCL:

- Do not claim the first structural GCL or first heterophily SSL.
- Claim a narrower mechanism: nonlocal role-equivalent positive construction from compact role/WL/landmark signatures, with a role branch that can be validation-selected or gated away on raw-dominant graphs.
- The empirical hook is the unusually large Chameleon 10-split gain over RFA/DCA-style controls.

## Decision

RSP-GCL is `ACTIVE_WITH_SCOPE_LIMIT`.

Required next checks:

1. Run Chameleon 10-split training version, not only zero-training proxy.
2. Add a role-weight gate over `{0, role}` selected by validation or a label-free proxy, then verify Texas/Wisconsin do not regress below raw.
3. Search more directly for WL/role/landmark-positive GCL to tighten novelty before external baselines.
4. If Chameleon training 10-split stays near proxy and gate protects raw-dominant graphs, promote to `READY_TO_REFINE`.
