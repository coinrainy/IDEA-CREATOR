# CCR-GCL M0/M1 结果：正交残差有 Cora 信号，但 certification 失败

**日期**：2026-06-22  
**候选**：CCR-GCL（Complementarity-Certified Residual Graph Contrastive Learning）  
**状态**：`FAILED_CERTIFICATION_GATE`  
**代码**：`baselines/BGRL/train_ccr_transductive.py`，`baselines/BGRL/reproduce_ccr.py`

## 动机

LIFT-Portfolio 已经是强训练自由控制，但新颖性不足。EPI/PAB 说明仅改 BGRL 训练目标无法接近 LIFT-Portfolio。CCR-GCL 反过来把 LIFT-Portfolio 当作固定教师，要求 GPU 训练的 GNN 只学习“教师没覆盖的正交残差”：

- teacher = LIFT-Portfolio 表示；
- residual = BGRL/GCN 学到的表示；
- 训练损失 = BGRL loss + residual 与 teacher 随机投影 anchor 的正交惩罚 + 方差防坍塌；
- 评估 `portfolio`、`residual_only`、`portfolio_plus_residual`；
- certification 使用 label-free residual edge-lift 与 teacher-anchor mean abs cosine，决定是否拼接残差。

目标不是再微调 LIFT 特征，而是检验 learned residual 是否能在不破坏强 teacher 的前提下提供互补信息。

## GPU 与评估协议

- M0 smoke 与 M1 split-0 均记录 `device=cuda`。
- M1 所有 `stdout.log` 均包含 `Using cuda for training.`。
- 最终线性探针保持原 BGRL/sklearn CPU 口径。
- M1 无 NaN，无坍塌。

## M0 smoke

命令：

```bash
python baselines/BGRL/reproduce_ccr.py \
  --datasets=cora,chameleon \
  --variants=bgrl_control,ccr_orth_var \
  --splits=0 --epochs=5 --eval_epochs=5 \
  --device=auto \
  --output_dir=runs/ccr_smoke_20260622 --clean
```

结果：工程链路通过，LIFT-Portfolio teacher 构造、CUDA 训练、残差拼接评估、JSON/CSV 输出均正常。Chameleon smoke 已暴露风险：5 epoch residual concat 将 portfolio `0.699561` 拉低到 `0.618421`。

## M1 split-0 gate

命令：

```bash
python baselines/BGRL/reproduce_ccr.py \
  --datasets=cora,citeseer,chameleon,texas,wisconsin \
  --variants=ccr_orth_var \
  --splits=0 --epochs=200 --eval_epochs=200 \
  --device=auto \
  --output_dir=runs/ccr_m1_split0_20260622 --clean
```

| Dataset | Portfolio | Residual only | Portfolio + residual | Certified | Delta certified vs portfolio | Decision |
|---|---:|---:|---:|---:|---:|---|
| Cora | 0.842640 | 0.829257 | 0.851407 | 0.855099 | +0.012460 | strong local positive |
| CiteSeer | 0.725770 | 0.678437 | 0.714125 | 0.714125 | -0.011645 | fail |
| Chameleon | 0.699561 | 0.438596 | 0.629386 | 0.629386 | -0.070175 | fail |
| Texas | 0.810811 | 0.621622 | 0.783784 | 0.783784 | -0.027027 | fail |
| Wisconsin | 0.823529 | 0.549020 | 0.803922 | 0.803922 | -0.019608 | fail |

Diagnostics:

- residual effective rank remains healthy; no collapse.
- orthogonality penalty makes mean abs teacher cosine low (`~0.04-0.05`) on all datasets.
- residual edge-lift is not a sufficient safety certificate: Cora is positive with residual lift `0.567708`, but CiteSeer is negative despite residual lift `0.695747`; Texas/Wisconsin also pass the naive residual-lift certificate but hurt raw teacher.

## 判定

CCR-GCL 不通过主方法 gate。

关键原因：

1. Cora 上确有 strong local complementarity signal（`+0.01246` over LIFT-Portfolio split-0）。
2. 同一 certification 规则在 CiteSeer/Chameleon/WebKB 上错误放行有害 residual。
3. Chameleon 的损害很大：`0.699561 -> 0.629386`，不能作为 paper 方法接受。
4. 这复现并强化了 R085 的结论：trained residual 分支不天然互补于强固定传播控制；必须先解决 label-free residual safety/certification。

## 决策

- 保留 CCR 代码与 Cora 正信号作为诊断。
- 不做 CCR 10-split，不扩外部 baseline。
- learned residual 方向只有在出现更强 label-free residual safety criterion 时才可重启。
- 下一轮应优先搜索能直接判断 residual 是否会伤害 LIFT-Portfolio 的机制，而不是继续训练更复杂的 residual encoder。
