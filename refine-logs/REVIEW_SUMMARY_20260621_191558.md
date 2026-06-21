# Review Summary

**Problem**: 让图自监督 / 图对比学习的正目标不再被普通消息传递平凡化。
**Initial Approach**: SRLP-GCL，最初用 `Z - alpha PZ` 作为残差隐目标。
**Date**: 2026-06-21
**Rounds**: 2
**Final Score**: 7.35 / 10
**Final Verdict**: READY for pilot, not yet paper-ready.

## Problem Anchor

- **Bottom-line problem**: 设计一个用于节点分类的图自监督方法，使正目标真正提供有用学习信号，而不是被普通消息传递或同节点增强视图对齐提前平凡化。
- **Must-solve bottleneck**: 当前 GCL 常把同一节点的两个增强视图当作正样本；在图编码器消息传递后，这种正样本相似性可能已经由邻域平滑自然产生，导致目标学习低信息量一致性，尤其难以解释异配图上的收益。
- **Non-goals**: 不继续 NFR-GCL 的节点级频率路由主线；不声称通用图 JEPA 或 latent prediction 本身新；不引入 LLM 文本教师、大图预训练或新的大模型栈；不把复杂实验矩阵当作贡献。
- **Constraints**: 第一版必须能嵌入现有 `baselines/` 节点分类评测；异配图必须使用 Geom-GCN 官方固定划分；本地 12GB GPU 友好；优先单进程顺序运行；新训练组件最多两个。
- **Success condition**: 上下文投影残差目标在 Cora/Chameleon 单 split pilot 中不 collapse，且在异配图官方 split 0 上比全隐表示预测、普通 BGRL/GRACE 对齐更有信号；正式评测中在 Actor/Chameleon/Squirrel/Cornell/Texas/Wisconsin 上相对强本地基线有稳定提升或清晰互补优势。

## Round-by-Round Resolution Log

| Round | Main Reviewer Concerns | What Changed | Solved? | Remaining Risk |
|---|---|---|---|---|
| 1 | `Z - alpha PZ` 像高频信号换名；泄漏控制太软；conditional InfoNCE 贡献发散。 | 改成 visible-context subspace residual；在线分支移除所有 target incident edges；删除 InfoNCE、learned alpha 和结构标量。 | Yes, major issues resolved. | 残差可能过难预测。 |
| 2 | rank-1 projection 仍需避免被写成弱高通；warmup 可能混淆贡献。 | 最终方案固定叙事为 context-projected residual；规定 pilot 必须包含 full-latent、`Z-PZ`、no-isolation 对照；warmup 必须有 no-warmup ablation。 | Ready for pilot. | Empirical validity only. |

## Overall Evolution

- 方法从“邻域平滑残差”改成“可见上下文子空间投影残差”，新颖性叙事更稳。
- 第一版删除 conditional InfoNCE、learned alpha、结构标量输入和 covariance regularizer，贡献明显收敛。
- 泄漏控制从软 edge dropout 改成 target feature mask + target incident edge removal。
- 实现落点收敛到 `baselines/BGRL` 小改版，适合先做 pilot。

## Final Status

- **Anchor status**: preserved.
- **Focus status**: tight enough for pilot.
- **Modernity status**: intentionally conservative; no LLM/VLM/Diffusion/RL needed.
- **Strongest parts**: context-projected residual target; hard target isolation; explicit go/kill diagnostics.
- **Remaining weaknesses**: method尚未实证；rank-1 residual 可能太难预测；若 warmup 有用，需要证明不是 warmup 在贡献主要收益。
