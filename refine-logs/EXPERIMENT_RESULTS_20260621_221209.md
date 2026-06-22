# SRLP 4060 小图实验结果

**日期**：2026-06-21  
**计划**：`refine-logs/EXPERIMENT_PLAN.md`  
**实现位置**：`baselines/BGRL`  
**GPU**：NVIDIA GeForce RTX 4060 Laptop GPU，约 8GB 显存。

## 实现状态

- 已在 `baselines/BGRL/` 中加入 SRLP 工具、训练入口、顺序运行器和泄漏探针。
- 已安装 `tensorboard`，但实验主输出仍是 `metrics.json` 和汇总 `results.csv`。
- 未构造稠密 `N x N` 传播矩阵；`ZPZ` 使用 sparse edge propagation。
- Chameleon 原始 PyG `edge_index` 方向性很强，因此 context 和 `PZ` 均使用无向一跳邻接。
- Codex 子智能体代码审稿结论为 `PASS_WITH_FIXES`；已修复 hard isolation 自环泄漏、CSV 可追溯字段、CiteSeer split 预生成和数据集路径大小写。

## M0 Smoke Test

| 数据集 | 划分 | Test@Best | Skipped Ratio | Effective Rank | NaN | Collapse |
|---|---|---:|---:|---:|---|---|
| Cora | fixed 1:1:8 seed 0 | 0.76927 | 0.04613 | 154.69 | false | false |
| Chameleon | Geom-GCN split 0 | 0.41886 | 0.00879 | 100.37 | false | false |

结论：M0 通过。实现不 OOM、不 NaN，split 路径和计数正常打印，`skipped_ratio < 0.4`。

## M1 Cora/CiteSeer 200 Epoch

| 数据集 | 变体 | Valid@Best | Test@Best | Final Test | Pred Cos | Residual Norm | Skipped | Rank |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Cora | BGRL | 0.83026 | 0.80895 | 0.80895 | 0.59820 | 0.00000 | 0.00000 | 148.01 |
| Cora | FullLatent-Iso | 0.83026 | 0.80065 | 0.80065 | 0.61988 | 10.61305 | 0.04613 | 122.16 |
| Cora | ZPZ-Iso | 0.79336 | 0.76742 | 0.73466 | 0.27681 | 2.92307 | 0.04797 | 137.37 |
| Cora | SRLP hard | 0.78967 | 0.76465 | 0.77527 | 0.25927 | 4.17948 | 0.06827 | 132.59 |
| Cora | SRLP-NoIso | 0.78598 | 0.77527 | 0.76327 | 0.36091 | 4.21768 | 0.06642 | 123.47 |
| CiteSeer | BGRL | 0.69970 | 0.69684 | 0.69684 | 0.59286 | 0.00000 | 0.00000 | 170.38 |
| CiteSeer | FullLatent-Iso | 0.69069 | 0.68633 | 0.69159 | 0.62414 | 10.81818 | 0.12782 | 146.40 |
| CiteSeer | ZPZ-Iso | 0.64865 | 0.64876 | 0.61119 | 0.27378 | 1.94960 | 0.12782 | 153.70 |
| CiteSeer | SRLP hard | 0.65465 | 0.67280 | 0.65101 | 0.22925 | 3.30580 | 0.17594 | 153.61 |
| CiteSeer | SRLP-NoIso | 0.64565 | 0.65515 | 0.65477 | 0.34322 | 3.33929 | 0.17293 | 139.44 |

结论：M1 在同配图上不支持强 claim。Cora 上 SRLP 明显弱于 BGRL 和 FullLatent-Iso；CiteSeer 上 SRLP 优于 ZPZ/NoIso，但仍弱于 BGRL 和 FullLatent-Iso。

## Chameleon 200 Epoch

| 变体 | Valid@Best | Test@Best | Prediction Cosine | Residual Norm | Skipped Ratio | Effective Rank |
|---|---:|---:|---:|---:|---:|---:|
| FullLatent-Iso | 0.41838 | 0.41886 | 0.62414 | 9.50410 | 0.02857 | 72.64 |
| ZPZ-Iso | 0.41564 | 0.40132 | 0.62868 | 8.91162 | 0.02857 | 65.33 |
| SRLP hard | 0.43073 | 0.42325 | 0.57322 | 8.08275 | 0.02857 | 67.72 |
| SRLP-NoIso | 0.43073 | 0.41886 | 0.58576 | 8.07344 | 0.02857 | 63.74 |
| BGRL | 0.42112 | 0.43860 | 0.67890 | 0.00000 | 0.00000 | 115.11 |

结论：短训下 SRLP 对 target-family 消融有弱正信号，但仍低于 BGRL。

## Chameleon 1000 Epoch

| 变体 | Valid@Best | Test@Best | Final Test | Pred Cos | Residual Norm | Skipped | Rank |
|---|---:|---:|---:|---:|---:|---:|---:|
| BGRL | 0.45267 | 0.44298 | 0.47149 | 0.93303 | 0.00000 | 0.00000 | 138.45 |
| FullLatent-Iso | 0.51303 | 0.49781 | 0.49781 | 0.81536 | 9.38578 | 0.00659 | 103.00 |
| ZPZ-Iso | 0.46228 | 0.41447 | 0.41228 | 0.89289 | 10.63802 | 0.00659 | 71.57 |
| SRLP hard | 0.49657 | 0.46053 | 0.46053 | 0.80083 | 8.21885 | 0.00659 | 94.01 |
| SRLP-NoIso | 0.47599 | 0.44956 | 0.46930 | 0.79205 | 8.06435 | 0.00659 | 95.34 |

结论：训练稳定，但正信号没有延续到 1000 epoch。SRLP hard 高于 ZPZ-Iso 和 NoIso，但低于 FullLatent-Iso。

## M2 小异配图 Split 0

| 数据集 | FullLatent-Iso | ZPZ-Iso | SRLP hard | SRLP-NoIso | SRLP 是否赢最强消融 |
|---|---:|---:|---:|---:|---|
| Cornell | 0.54054 | 0.54054 | 0.54054 | 0.54054 | 并列 |
| Texas | 0.64865 | 0.64865 | 0.62162 | 0.62162 | 否 |
| Wisconsin | 0.52941 | 0.58824 | 0.47059 | 0.54902 | 否 |
| Actor | 0.27237 | 0.26579 | 0.26776 | 0.27171 | 否 |
| Chameleon | 0.49781 | 0.41447 | 0.46053 | 0.44956 | 否 |

诊断字段均正常：所有 M2 run 的 `nan_flag=false`、`collapse_flag=false`，`skipped_ratio` 范围为 0.00659 到 0.05405。

结论：M2 未通过。按照原计划门槛，SRLP 需要至少在 3/5 个小异配图上优于最强 target-family 消融；当前是 0/5 明确获胜，Cornell 仅并列。

## 泄漏探针

| 变体 | Probe Cosine | Probe MSE | 解释 |
|---|---:|---:|---|
| SRLP hard | 0.27185 | 0.00362 | hard isolation 泄漏信号更低，方向正确。 |
| SRLP-NoIso | 0.63130 | 0.00236 | NoIso 更容易由 online hidden state 线性预测 target，说明 incident-edge leakage 存在。 |

结论：泄漏控制本身有效，但下游分类收益不足。

## 总结判断

- 工程实现：通过。
- 协议完整性：通过，固定 split、Geom-GCN split、JSON/CSV 字段和稀疏传播均已落地。
- 泄漏诊断：通过，hard isolation 明显降低 probe cosine。
- 方法效果：未通过当前小图门槛。SRLP 没有在小异配图 split 0 上形成稳定优势。

## Post-Experiment Revision: SRLP-Aux

根据 Codex 子智能体方法审稿，residual-only SRLP 被降级：它不再作为主目标，而改为 **FullLatent + energy-gated residual auxiliary**。

实现的最小版本为单头混合 target：

```text
y_v = normalize(z_hat_v + lambda_t * w_v * r_hat_v)
L = mean_{v in T_valid} [1 - cosine(p_v, y_v)]
```

其中 `lambda_max=0.1`，`tau=0.15`，前 10% epoch 线性 warmup。

### SRLP-Aux Gate Results

| Dataset | Old SRLP hard | SRLP-Aux | Delta vs hard | Best target-family | Aux vs best | NaN | Collapse | Skipped |
|---|---:|---:|---:|---:|---:|---|---|---:|
| Chameleon | 0.46053 | 0.50658 | +0.04605 | 0.49781 | +0.00877 | false | false | 0.00659 |
| Texas | 0.62162 | 0.64865 | +0.02703 | 0.64865 | +0.00000 | false | false | 0.05405 |
| Wisconsin | 0.47059 | 0.54902 | +0.07843 | 0.58824 | -0.03922 | false | false | 0.02000 |
| Actor | 0.26776 | 0.26974 | +0.00197 | 0.27237 | -0.00263 | false | false | 0.05329 |
| CiteSeer | 0.67280 | 0.67656 | +0.00376 | 0.68633 | -0.00977 | false | false | 0.24511 |

Gate 判断：

- SRLP-Aux 相对旧 SRLP hard：**5/5 提升**。
- 异配图达到或超过最强 target-family：**2/4**，Chameleon 和 Texas 通过。
- 相对 FullLatent-Iso 低于 1.5 个百分点以上：**0/5**。
- NaN/collapse：**0/5**。

结论：SRLP-Aux 通过小 gate。Residual-only SRLP 仍应视为失败版本；当前可继续有限 10 split target-family 内部扩展，但仍不应进入外部强基线论文主表。

## 下一步建议

恢复有限 10 split 内部消融，但只针对 SRLP-Aux 与 target-family 消融，不扩外部强基线主表。优先数据集为 Chameleon、Texas、Wisconsin、Actor；若 10 split mean 仍不稳，则停止 SRLP-Aux 作为论文主方法。
