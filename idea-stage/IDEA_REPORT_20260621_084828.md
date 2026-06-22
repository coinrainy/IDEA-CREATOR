# Idea Discovery Report

**Direction**: 图对比学习，节点分类  
**Date**: 2026-06-21  
**Pipeline**: research-lit → idea-creator → Codex reviewer → research-refine-pipeline lite  
**Reviewer**: Codex 子智能体 `019ee957-c111-7e42-ada2-d9f9f216e59c`  

## Executive Summary

推荐主线是 **NFR-GCL: Node-Frequency Routed Graph Contrastive Learning**。它合并候选 I1+I4：在 PolyGCL/HLCL/AF-GCL 的频带洞察基础上，把“应该低通对齐还是高通/混合频率对齐”从全图级决策推进到节点级路由。当前没有 pilot 结果，因此状态是 **ACTIVE / READY_TO_PILOT**，不是已证实方法。

最强 backup 是 **Masked Heterophilous Edge Reconstruction**，即候选 I6。它贴合 GRASS 在 Cornell/Wisconsin 的本地强结果，但 novelty 更容易被 GRASS/GREET/GraphMAE 类工作压住，所以不作为第一主线。

## Literature Landscape

本地 `baselines/reproduction_results.xlsx` 已经覆盖 DGI、MVGRL、GRACE、GCA、BGRL、PolyGCL、GRASS、EPAGCL、EDA-GCL 等 GCL 节点分类 baseline。结果显示：同配图上 Cora/CiteSeer/Amazon-Photo 已较饱和，多方法差距接近方差；异配图上差距更大，PolyGCL 和 GRASS 明显强于传统 GRACE/GCA/DGI。

关键 prior work 包括 GRACE/GCA/BGRL 作为经典 augmentation 或 bootstrap GCL；AF-GCL 指出 graph augmentation 保留低频、扰动中高频，因此会伤害高频偏好的 heterophily 数据；HLCL 通过高/低通图滤波处理 heterophily；PolyGCL 在本地异配图上是最强锚点；2025 contrastive similarity theory 与 Khan-GCL 说明 negative similarity / hard negatives 仍是开放方向。

结构性缺口是：现有强方法要么使用全图级频带组合，要么使用全局 edge/feature augmentation。真实图内部常混合同配区域、异配区域、噪声边和结构角色节点，因此需要节点级、无标签的局部频带路由。

## Ranked Ideas

### Idea 1: NFR-GCL: Node-Frequency Routed Graph Contrastive Learning — ACTIVE / READY_TO_PILOT

- **Status rationale**: Codex reviewer 排名第 1，paper potential 8.0/10；novelty risk 为 MEDIUM，条件是必须证明 node-wise routing 强于 PolyGCL 的全局 high/low 组合。
- **Fair-test status**: 尚未公平测试。必须在 official heterophily splits 上直接对比 PolyGCL、GRASS、EDA-GCL、GCA/GRACE。
- **Method (what we actually do)**: 复用 PolyGCL 的 ChebNetII high/low-pass encoder，额外构造 mid-band view；为每个节点用无标签局部统计学习 routing weights；同配倾向节点强调 low/mid consistency，异配倾向节点强调 mid/high complementary consistency；edge compatibility 只作为路由输入，不作为独立贡献。
- **Hypothesis**: 节点级频带路由能在图内混合同配/异配区域时，比全局 high/low 组合更稳定地保留 task-relevant signal。
- **Minimum experiment**: Actor、Chameleon、Squirrel official 10 splits，平均超过当前 best local baseline 至少 +1.5 points，至少 2/3 数据集胜出；Cora/CiteSeer smoke 不下降超过 1 point。
- **Novelty**: 7.5/10。Closest: PolyGCL、HLCL、AF-GCL。差异点是 node-wise routing + mixed-frequency consistency，而非全图固定滤波。
- **Pilot result**: SKIPPED / not run in this turn.
- **Reviewer likely objection**: “这只是 PolyGCL/HLCL 加门控。”
- **Pre-defense**: 加 global-router、random-router、feature-only-router、graph-level-router、no-mid-band、no-compatibility ablation，并报告路由与后验 label homophily 的相关性，后者只做分析不参与训练。

### Idea 2: Masked Heterophilous Edge Reconstruction — BACKUP / ACTIVE

- **Status rationale**: Reviewer 排名第 2，paper potential 7.2/10。本地 GRASS 在 Cornell/Wisconsin 最强，说明 masked-edge route 有信号。
- **Fair-test status**: 未公平测试；必须直接打 GRASS 与 PolyGCL，而不是只赢传统 baseline。
- **Method**: 把 GRASS 的随机负边重构改成三类无标签 edge compatibility reconstruction：homophilic-compatible edge、heterophilic-compatible edge、noise/non-edge。
- **Minimum experiment**: Cornell、Texas、Wisconsin official 10 splits；平均超过 best-of-GRASS/PolyGCL 至少 +2 points 或 2/3 数据集 split-wise 清楚胜出。
- **Novelty**: 6.8/10。Closest: GRASS、GREET、GraphMAE/MaskGAE。
- **Pilot result**: SKIPPED / not run.

### Idea 3: Heterophily-Aware Hard Negative Mining — DEPRIORITIZED / AUXILIARY

- **Status rationale**: Reviewer 认为 standalone 不够，适合作为 NFR-GCL 后续辅助 loss 或 ablation。
- **Fair-test status**: 仅在主方法 pilot 过线后考虑。
- **Method**: 用 compatibility guard 降低 false-negative 风险，只对结构相近但兼容性冲突的节点施加强 hard-negative pressure。
- **Novelty**: 6.4/10。Closest: ProGCL、AUGCL、Khan-GCL、2025 similarity theory。

### Idea 4: Augmentation-Free Node-Local BGRL — DEPRIORITIZED

- **Status rationale**: BGRL 同配强异配弱，但 reviewer 认为 novelty 偏弱，且需要先补齐 BGRL 在 Squirrel/WebKB 的本地 baseline。
- **Next condition**: 只有当它能打过 PolyGCL/GRASS，而不只是修复 BGRL 自己的弱点，才值得恢复。

### Idea 5: Compatibility-Calibrated Contrastive Edges — KILLED as standalone

- **Status rationale**: Reviewer 认为 standalone 很容易被认为是复杂版 GCA/EDA-GCL。保留为 NFR-GCL 的 routing signal。
- **Kill condition**: 除非它独立打过 GCA 和 EDA-GCL on Chameleon/Squirrel/Texas，否则不作为独立论文主线。

## Incubation Portfolio

| Idea | Status | Missing condition or next decisive test |
|---|---|---|
| NFR-GCL | ACTIVE / READY_TO_PILOT | Actor/Chameleon/Squirrel official 10-split pilot |
| Masked Heterophilous Edge Reconstruction | BACKUP | WebKB + Chameleon/Squirrel pilot against GRASS/PolyGCL |
| Heterophily-aware hard negatives | AUXILIARY | Only after NFR-GCL main signal is positive |
| Node-local BGRL | DEPRIORITIZED | Complete BGRL heterophily baseline first |

## Eliminated Ideas

| Idea | Fair reason |
|---|---|
| I2 standalone | Too close to GCA/EDA-GCL unless it independently beats them. |
| I11 standalone | Hard-negative GCL is crowded; keep as ablation. |
| I16 mainline | BGRL+filter framing likely too incremental. |
| Graph transformer/tokenized variants | Need a new code stack; not first pilot under current baselines. |
| Benchmark/diagnostic-only routes | User direction favors positive method paper, not diagnostic report. |

## Refined Proposal

- Proposal: `refine-logs/FINAL_PROPOSAL.md`
- Experiment plan: `refine-logs/EXPERIMENT_PLAN.md`
- Tracker: `refine-logs/EXPERIMENT_TRACKER.md`
- Pipeline summary: `refine-logs/PIPELINE_SUMMARY.md`

## Next Steps

- [ ] Implement NFR-GCL as a PolyGCL-based minimal patch.
- [ ] Run Actor/Chameleon/Squirrel official 10-split pilot.
- [ ] If pilot passes go/no-go, add ablations and homophily no-regression checks.
- [ ] If pilot fails, switch to I6 backup rather than stacking more modules onto NFR-GCL.

