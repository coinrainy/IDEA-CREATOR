# Refinement Report

**Problem**: 图对比学习节点分类中的 heterophily failure。  
**Initial direction**: 基于本地 `baselines/` 结果寻找可发表 idea。  
**Date**: 2026-06-21  
**Final verdict**: READY_TO_PILOT  

## Output Files

- Review summary: `refine-logs/REVIEW_SUMMARY.md`
- Final proposal: `refine-logs/FINAL_PROPOSAL.md`
- Experiment plan: `refine-logs/EXPERIMENT_PLAN.md`
- Experiment tracker: `refine-logs/EXPERIMENT_TRACKER.md`

## Score Snapshot

| Idea | Reviewer score | Status |
|---|---:|---|
| I1+I4: Node-wise Frequency Routed GCL | 8.0/10 | ACTIVE / READY_TO_PILOT |
| I6: Masked Heterophilous Edge Reconstruction | 7.2/10 | BACKUP |
| I11: Heterophily-aware hard negatives | 6.4/10 | AUXILIARY |
| I16: Node-local BGRL | 6.3/10 | DEPRIORITIZED |
| I2: Compatibility edges | 5.8/10 | KILLED as standalone |

## Method Evolution

1. 原始候选池中有多个相近路线：频带路由、edge compatibility、hard negatives、BGRL augmentation-free。
2. Reviewer 建议把主线压缩为一个 dominant contribution：node-local frequency routing。
3. Edge compatibility 只保留为 router input；hard negatives 只作为后续 ablation；I6 保留为 backup。

## Remaining Weaknesses

- 尚未有 pilot，所有效果提升都是假设。
- Novelty 依赖于节点级路由是否明显强于 PolyGCL/HLCL 的全局频带机制。
- 如果路由退化为全局权重，主线应停止。

## Raw Reviewer Response

完整 trace: `.aris/traces/idea-discovery/2026-06-21_run01/001-top-ideas-review.response.md`

