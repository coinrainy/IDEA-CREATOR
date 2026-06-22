# Round 1 Review: SRLP-GCL

**Reviewer agent**: `019ee9db-8d1c-7da1-b821-96873d7b1a0b`
**Date**: 2026-06-21
**Verdict**: REVISE
**Overall score**: 5.95 / 10

## Parsed Scores

| Round | Problem Fidelity | Method Specificity | Contribution Quality | Frontier Leverage | Feasibility | Validation Focus | Venue Readiness | Overall | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 7 | 6 | 5 | 6 | 7 | 7 | 4 | 5.95 | REVISE |

## Key Reviewer Concerns

1. `R = normalize(Z - alpha PZ)` looks like high-frequency signal under another name, creating proximity risk with ASPECT/SPGCL.
2. Directly subtracting `PZ` may remove useful heterophilous neighbor information.
3. Target masking plus 20% edge dropout is too weak for transductive leakage control.
4. Conditional InfoNCE and learned/heuristic `alpha` make the contribution sprawl.
5. The first version should be much simpler: EMA teacher, target feature mask, full incident-edge removal, residual cosine loss.

<details>
<summary>Raw reviewer response</summary>

**1. 七项评分**

| 项目 | 分数 |
|---|---:|
| Problem Fidelity | 7/10 |
| Method Specificity | 6/10 |
| Contribution Quality | 5/10 |
| Frontier Leverage | 6/10 |
| Feasibility | 7/10 |
| Validation Focus | 7/10 |
| Venue Readiness | 4/10 |

**2. OVERALL SCORE**

5.95/10，约等于 6.0/10。

**3. Verdict**

REVISE

**4. Drift Warning**

NONE。下面建议仍围绕 SRLP-GCL 的正目标定义、泄漏控制、贡献收敛和低成本实现，不建议转向 LLM/VLM/Diffusion/RL 或新大模型栈。

**5. 主要质疑**

CRITICAL

1. 弱点：`R = normalize(Z - alpha PZ)` 在形式上就是对教师隐表示做图高通残差，很容易被认为是 high-frequency signal 换名。
Reviewer attack：ASPECT 已经覆盖节点级频谱/平滑融合，SPGCL 已经讨论正样本有效性；审稿人会问这和“高频目标”或“更难正样本”到底差在哪里。
修复：把目标重写为“masked context 不可预测的教师成分”，而不是“邻居均值相减”。例如只减去 `Z_v` 在可见邻居聚合向量上的投影，或用冻结/stop-gradient 的 context estimator 得到可预测成分，再取残差。核心叙事应是 conditional unpredictability，不是频率。

2. 弱点：直接 subtracting `PZ` 可能删掉异配图里真正有用的邻居信息。
Reviewer attack：异配图不等于邻居无用，邻居类别分布、角色结构、跨类连接模式本身可能是分类信号；你把它当 shortcut 扣掉，理论前提过强。
修复：不要整块扣除邻居平滑项。改成只扣除“与上下文聚合方向对齐、可被消息传递平凡恢复”的分量；`alpha` 若保留，应是确定性 reliability gate，而不是可学习逃生阀。最终 encoder 表示也不应被约束成纯残差，残差只作为训练目标。

3. 弱点：target masking + `eta=0.2` edge dropout 不足以防止信息泄漏。
Reviewer attack：在 transductive 图里，目标节点身份、度数、局部结构、邻居特征和保留边都可能泄漏目标信息；`c(v)` 还显式喂入结构标量，容易变成结构 ID shortcut。
修复：第一版应采用硬泄漏控制：在线分支对 target node mask feature，并移除所有 incident target edges；`local_feature_compatibility(v)` 不得使用目标原始特征；先不要把 `log_degree`、compatibility、mask ratio 喂给 predictor，等核心目标站住后再加。

IMPORTANT

1. 弱点：conditional InfoNCE 会让贡献发散。
Reviewer attack：如果它有效，贡献变成 conditional negative mining；如果无效，它是噪声模块。并且 `R` 被 normalize 后再按 `||R||` 分 bin，条件本身退化。
修复：从主方法删除。第一版只保留 `L_pred`，最多加轻量 variance regularizer；InfoNCE 放到后续 appendix/ablation，不进入核心 claim。

2. 弱点：`alpha(v)` 定义不够干净。
Reviewer attack：若可学习，模型可能把 `alpha` 学到接近 0，退回 full-latent prediction；若手工，审稿人会质疑调参驱动。
修复：v1 固定 `alpha=1` 或使用明确的非学习规则；如果固定版失败，再考虑 deterministic attenuation，而不是马上引入 learned alpha。

3. 弱点：EMA teacher residual 是自举移动目标，残差可能低能量且不稳定。
Reviewer attack：BGRL 的 target 已经会移动；再做 `Z-PZ` 可能放大噪声，形成 collapse 或 teacher-online collusion。
修复：保留 residual pre-norm 能量监控；对极小残差加 epsilon/energy floor；必要时用短暂 full-latent warmup 初始化 teacher，但不要把 warmup 写成新贡献。

MINOR

1. 弱点：`L_stab` 同时作用到 online predictions 和 teacher residual targets 表述不清。
Reviewer attack：teacher target stop-gradient 时，target-side covariance regularizer 没有训练意义。
修复：只对 `P_T` 加 variance/covariance，或先删掉 stabilizer。

2. 弱点：local feature compatibility 在稀疏文本特征图上可能很脆，而且可能泄漏目标 feature。
Reviewer attack：它会被认为是 dataset-specific trick。
修复：v1 不进入 predictor，只用于诊断或 deterministic gate。

3. 弱点：方法名字仍叫 GCL，但核心目标可完全 non-contrastive。
Reviewer attack：如果删掉 InfoNCE，论文定位会混乱。
修复：叙事改成 graph predictive self-supervised learning；GCL 只作为相关领域背景。

**6. Simplification Opportunities**

1. 删除 conditional InfoNCE 主分支，避免贡献从 residual target 漂到 negative sampler。

2. 第一版固定 `alpha`，删除 structural scalars，只测 residual target 是否有效。

3. 直接基于现有 BGRL harness 改一个小 variant：EMA teacher、target mask、incident-edge removal、residual cosine loss。这样低成本实现是成立的。

**7. Modernization Opportunities**

NONE。不需要 LLM/VLM/Diffusion/RL。强行加现代组件会稀释问题，并增加不可控变量。

**8. 最终建议**

下一版最应该改 3 点：

1. 把 residual target 从 `Z - alpha PZ` 改写为“可见 masked context 无法预测的教师残差”，明确避开纯高频叙事。

2. 把泄漏控制做硬：mask target feature，在线分支移除 target incident edges，所有 conditioning 统计不得读取目标原始特征。

3. 收敛第一版贡献：主方法只保留 residual prediction，先不要 learned alpha、conditional InfoNCE 和结构标量。这个版本最适合在现有 `baselines/BGRL` 代码里低成本落地。

</details>
