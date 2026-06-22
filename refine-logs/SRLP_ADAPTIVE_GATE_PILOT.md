# SRLP Adaptive Gate Diagnostic and Pilot

**日期**: 2026-06-22  
**范围**: SRLP-Aux 10-split 失败后的方法级补充诊断。  
**结论级别**: Go/Kill 小门控，不是论文主表。

## 背景

SRLP-Aux 10 split 只在 Chameleon 有小幅正信号，Texas/Wisconsin 不能稳定优于 FullLatent/ZPZ。随后目标对齐诊断显示：

- Chameleon 的 context projection 是强标签信号，不应被残差目标强行削掉；
- Texas/Wisconsin 的 rank-k residual 有标签信号，但旧 SRLP-Aux 的 rank-1 弱混合没有把它转成表征收益；
- Actor 接近噪声底，不适合作为下一步设计驱动。

因此本轮只检查一个保守方向：FullLatent 作为主目标，label-free adaptive residual 作为小权重辅助。

## Label-Free Gate Diagnostic

诊断使用已有 `srlp_aux` 10-split checkpoint，不重新训练。门控信号为：

```text
g_r = clip(rho_r, tau_r) * clip(s_r, tau_s) * clip(a_r, tau_a)
g_p = clip(rho_p, tau_p) * clip(s_p, tau_s)
```

其中 `rho` 表示 residual/projection 能量占比，`s` 表示边扰动下的稳定性，`a_r` 表示 residual 与 `Z-PZ` 的方向一致性。

| Dataset | rho_r | rho_p | s_r | s_p | a_r | g_r | g_p | k1/k2/k4 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Chameleon | 0.6724 | 0.3276 | 0.9669 | 0.8561 | 0.4107 | 0.1768 | 0.0680 | 0.204/0.280/0.516 |
| Texas | 0.8031 | 0.1969 | 0.9533 | 0.5353 | 0.5400 | 0.3346 | 0.0130 | 0.584/0.257/0.159 |
| Wisconsin | 0.8517 | 0.1483 | 0.9662 | 0.5888 | 0.5575 | 0.3702 | 0.0059 | 0.524/0.284/0.192 |
| Actor | 0.6741 | 0.3259 | 0.9422 | 0.7070 | 0.4351 | 0.1883 | 0.0399 | 0.267/0.252/0.481 |

诊断判断：**部分通过**。Residual gate 能把 Texas/Wisconsin 明显抬高，并压低 Chameleon/Actor；projection gate 在 Chameleon 相对最高，但绝对值不高。因此只允许进入极小 pilot，不允许扩展外部强基线或大图。

输出：

- `baselines/BGRL/runs/srlp_aux_10split_target_family_20260621_221832/adaptive_gate_diagnostic.csv`
- `baselines/BGRL/runs/srlp_aux_10split_target_family_20260621_221832/adaptive_gate_diagnostic_summary.json`

## Implemented Pilot Variant

新增 `target_mode=srlp_adaptive_aux`：

```text
p_v = U_{v,k} U_{v,k}^T z_v
r_v = z_v - p_v
y_v = normalize(z_v + lambda_r * g_r(v) * normalize(r_v)
                  + lambda_p * g_p(v) * normalize(p_v))
```

默认 pilot 配置：

- `lambda_r=0.1`
- `lambda_p=0.0`
- `k in {1,2,4}`, `gamma=0.8`
- `tau_r=0.45`, `tau_p=0.45`, `tau_s=0.5`, `tau_a=0.2`
- `adaptive_drop_edge_p=0.2`

代码位置：

- `baselines/BGRL/bgrl/srlp_utils.py`
- `baselines/BGRL/train_srlp_transductive.py`
- `baselines/BGRL/reproduce_srlp.py`

## 200-Epoch Fair Pilot

所有 run 使用 Geom-GCN 官方 split 0，`eval_epochs=20`，单进程顺序运行。

| Dataset | Variant | Valid@Best | Test@Best | Final Test | Pred Cos | Skipped | Rank | g_r | g_p | NaN | Collapse |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| Chameleon | FullLatent-Iso | 0.4184 | 0.4189 | 0.4189 | 0.6241 | 0.0286 | 72.64 | 0.0000 | 0.0000 | false | false |
| Chameleon | ZPZ-Iso | 0.4156 | 0.4057 | 0.4035 | 0.6287 | 0.0286 | 65.34 | 0.0000 | 0.0000 | false | false |
| Chameleon | SRLP-Aux | 0.4170 | 0.4232 | 0.4232 | 0.6211 | 0.0286 | 72.51 | 0.0000 | 0.0000 | false | false |
| Chameleon | Adaptive-Aux | 0.4170 | 0.4145 | 0.4079 | 0.6259 | 0.0066 | 68.10 | 0.2636 | 0.0469 | false | false |
| Texas | FullLatent-Iso | 0.6102 | 0.6216 | 0.7027 | 0.7800 | 0.0000 | 14.22 | 0.0000 | 0.0000 | false | false |
| Texas | ZPZ-Iso | 0.6441 | 0.6486 | 0.6486 | 0.6085 | 0.0000 | 15.20 | 0.0000 | 0.0000 | false | false |
| Texas | SRLP-Aux | 0.6102 | 0.6216 | 0.6757 | 0.7652 | 0.0000 | 14.30 | 0.0000 | 0.0000 | false | false |
| Texas | Adaptive-Aux | 0.6102 | 0.6216 | 0.6757 | 0.7137 | 0.0541 | 17.66 | 0.1357 | 0.0000 | false | false |
| Wisconsin | FullLatent-Iso | 0.6125 | 0.5686 | 0.5686 | 0.7111 | 0.1200 | 19.38 | 0.0000 | 0.0000 | false | false |
| Wisconsin | ZPZ-Iso | 0.5875 | 0.5882 | 0.5686 | 0.4535 | 0.1200 | 20.97 | 0.0000 | 0.0000 | false | false |
| Wisconsin | SRLP-Aux | 0.6125 | 0.5882 | 0.5686 | 0.6946 | 0.1200 | 19.47 | 0.0000 | 0.0000 | false | false |
| Wisconsin | Adaptive-Aux | 0.6000 | 0.6078 | 0.6078 | 0.7047 | 0.0800 | 22.38 | 0.2259 | 0.0007 | false | false |

Delta vs best non-adaptive:

| Dataset | Adaptive-Aux Test@Best | Best non-adaptive Test@Best | Delta |
|---|---:|---:|---:|
| Chameleon | 0.4145 | 0.4232 | -0.0088 |
| Texas | 0.6216 | 0.6486 | -0.0270 |
| Wisconsin | 0.6078 | 0.5882 | +0.0196 |

输出：

- Adaptive pilot: `baselines/BGRL/runs/srlp_adaptive_aux_pilot_20260622_0120/results.csv`
- 200-epoch fair controls: `baselines/BGRL/runs/srlp_200epoch_controls_20260622_0135/results.csv`

## Decision

**结论：不进入扩展。**

Adaptive-Aux 的工程实现和训练稳定性通过：无 NaN、无 collapse，日志字段完整。但方法信号不足：

- Chameleon 小幅落后，说明 residual gate 对 projection-rich 图仍不够保守；
- Texas 仍被 ZPZ-Iso 压住，说明 rank-k residual label alignment 没有可靠转化为 online representation；
- Wisconsin 有局部正信号，但单个 split、单个数据集不足以支撑继续 10 split 或外部强基线。

推荐停止把 SRLP 继续包装为主方法。后续若继续研究，应转向更清晰的新问题，例如“label-free target decomposition diagnostic”或“何时 residual target 有用”的分析型工作，而不是继续堆 SRLP 变体。
