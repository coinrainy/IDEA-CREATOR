# Round 2 Review: SRLP

**Reviewer agent**: `019ee9db-8d1c-7da1-b821-96873d7b1a0b`
**Date**: 2026-06-21
**Verdict**: READY for pilot
**Overall score**: 7.35 / 10

## Parsed Scores

| Round | Problem Fidelity | Method Specificity | Contribution Quality | Frontier Leverage | Feasibility | Validation Focus | Venue Readiness | Overall | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2 | 8 | 8 | 7 | 7 | 7 | 8 | 5 | 7.35 | READY for pilot |

## Key Reviewer Conclusion

The revised method no longer needs major method-level changes before pilot. The context-projected residual target is a cleaner contribution than `Z-PZ`, and hard target isolation is a reasonable first-pass leakage control.

Remaining risks are empirical:

1. The residual may be too conditionally unpredictable after hard isolation.
2. Rank-1 context projection must be compared against full-latent and `Z-PZ` targets.
3. If warmup is used, no-warmup must also be reported.

## Raw Reviewer Summary

已读取并复审 `refine-logs/round-1-refinement.md`。

**七项评分**

| 项目 | 分数 |
|---|---:|
| Problem Fidelity | 8/10 |
| Method Specificity | 8/10 |
| Contribution Quality | 7/10 |
| Frontier Leverage | 7/10 |
| Feasibility | 7/10 |
| Validation Focus | 8/10 |
| Venue Readiness | 5/10 |

**OVERALL SCORE**: 7.35/10。

**Verdict**: READY，准确说是 READY for pilot。现在不需要继续做方法层重大修改，应该进入小规模 pilot。

**Drift Warning**: NONE。

**剩余问题**

CRITICAL: NONE。上一轮的核心硬伤已经基本修掉。

IMPORTANT:

1. context-projected residual 明显优于 `Z-PZ`，但 rank-1 mean neighbor projection 仍可能被 reviewer 追问是不是“邻居残差/弱高通”的变体。方法叙事必须固定为 visible-context subspace residual，并在 pilot 中强制加入 `Z-PZ` 对照；不要把核心解释写成频率或平滑。
2. hard target isolation 解决了直接泄漏，但可能让目标变得过难。pilot 必须记录 `R_raw` norm、prediction cosine、embedding rank；若 one-hop 太弱，只允许作为诊断切到 two-hop context，不要恢复 target incident edges。
3. optional warmup 可能混淆贡献。若使用 warmup，必须同时报告 no-warmup；主表述里把 warmup 写成 stabilization，不写成方法组成。

MINOR:

1. 跳过低残差节点可能改变训练节点分布。记录 skipped target ratio；如果比例高，调低 rank 或 epsilon，而不是静默跳过。
2. SRLP / SRLP-GCL 命名有点摇摆。建议正文用 SRLP，背景中说它面向 GCL 正目标问题。
3. rank-k QR 被列为 ablation，但容易诱发复杂化。pilot 只做 rank-1；rank-k 仅在 rank-1 失败但诊断显示可救时再碰。

**Simplification Opportunities**

1. 继续保持 v1 无 conditional InfoNCE、无 learned alpha、无结构标量输入。
2. 先不做 covariance regularizer，只保留 optional variance floor。
3. one-hop context 是默认实现；two-hop 只作为失败诊断，不作为初始主方法。

**Modernization Opportunities**: NONE。不需要 LLM/VLM/Diffusion/RL。

**最终建议**

1. 进入 BGRL-based pilot，实现 rank-1 context-projected residual + hard target isolation + cosine loss。
2. pilot 的最小对照必须包含 full-latent target、`Z-PZ` target、no incident-edge removal。
3. 第一轮结果先看三件事：残差是否有稳定能量、预测是否非 collapse、Chameleon/Actor split 0 是否比 full-latent 有信号。若三者过不了，直接 kill 或降级，不再加模块硬救。
