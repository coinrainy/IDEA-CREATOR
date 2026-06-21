# SRLP Post-Experiment Method Review

**Date**: 2026-06-21  
**Reviewer**: Codex subagent `019eea7f-94f8-7171-9bf7-a154baedf09c`  
**Scope**: 方法内部缺陷审稿，不扩大实验菜单。

## Verdict

**DOWNGRADE**。

Residual-only SRLP 证明了 hard isolation 可以降低泄漏，但没有证明 residual target 比 FullLatent/ZPZ 更有方法价值。因此，SRLP 应从主目标降级为辅助约束。

## Core Defects

| 优先级 | 缺陷 | 机制原因 | 对 claim 的伤害 |
|---|---|---|---|
| 1 | residual target 定义过窄 | rank-1 邻居均值方向不等于 shortcut 子空间，可能删掉类别主信号并放大噪声 | 无法证明 target 真正 shortcut-resistant |
| 2 | teacher target 与 online 可达信息不一致 | teacher clean latent 含 target-local 信息，online hard isolation 后不可达 | 失败可能来自不可预测，而非稳健语义 |
| 3 | residual-only 丢掉语义锚 | 与上下文正交的成分不一定类别相关 | “去上下文可预测成分”不能等同于判别语义 |
| 4 | hard isolation 过粗 | incident edges 同时含泄漏和有效结构信号 | 可能是在牺牲图信号换泄漏降低 |
| 5 | 相对 ZPZ 优势不足 | ZPZ 有传播算子归纳偏置，SRLP rank-1 残差结构偏置弱 | 难支撑 SRLP residual 优于传播残差 |

## Accepted Revision

采用审稿人的主修订方向：**FullLatent + energy-gated residual auxiliary**。

本轮实现进一步简化为单头混合 target，不新增 predictor head：

```text
z_hat_v = normalize(stopgrad(z_v))
q_v = normalize(mean_{u in C_v} normalize(stopgrad(z_u)))
r_v = z_hat_v - q_v(q_v^T z_hat_v)
rho_v = ||r_v||_2
r_hat_v = normalize(r_v)
w_v = stopgrad(clip((rho_v - tau)/(1 - tau), 0, 1))
lambda_t = lambda_max * min(1, epoch / warmup_epochs)
y_v = normalize(z_hat_v + lambda_t * w_v * r_hat_v)
L = mean_{v in T_valid} [1 - cosine(p_v, y_v)]
```

默认值：

```text
lambda_max = 0.1
tau = 0.15
warmup_epochs = 0.1 * total_epochs
```

## Gate Results

| Dataset | Old SRLP hard | SRLP-Aux | Delta vs hard | Best target-family | Aux vs best | FullLatent gap <= 1.5pp |
|---|---:|---:|---:|---:|---:|---|
| Chameleon | 0.46053 | 0.50658 | +0.04605 | 0.49781 | +0.00877 | yes |
| Texas | 0.62162 | 0.64865 | +0.02703 | 0.64865 | +0.00000 | yes |
| Wisconsin | 0.47059 | 0.54902 | +0.07843 | 0.58824 | -0.03922 | yes |
| Actor | 0.26776 | 0.26974 | +0.00197 | 0.27237 | -0.00263 | yes |
| CiteSeer | 0.67280 | 0.67656 | +0.00376 | 0.68633 | -0.00977 | yes |

Gate summary:

- Improved over old SRLP hard: **5/5**.
- Heterophily runs reaching strongest target-family result: **2/4**.
- More than 1.5pp below FullLatent-Iso: **0/5**.
- NaN/collapse: **0/5**.

## Decision

SRLP-Aux passes the small revision gate. The residual-only version remains failed and should not be used as the main method. The next step is a limited 10-split target-family internal expansion for SRLP-Aux, not a paper main table.
