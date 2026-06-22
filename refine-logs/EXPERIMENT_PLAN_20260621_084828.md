# Experiment Plan

**Problem**: 图对比学习在 heterophily 节点分类中缺少节点级频带自适应。  
**Method Thesis**: NFR-GCL uses node-wise routing over low/mid/high frequency views to preserve homophilic smoothness and heterophilic high-frequency signal within the same graph.  
**Date**: 2026-06-21  

## Claim Map

| Claim | Why It Matters | Minimum Convincing Evidence | Linked Blocks |
|---|---|---|---|
| C1: Node-local frequency routing improves heterophily GCL | 主贡献，必须打过 PolyGCL/GRASS 等强基线 | Actor/Chameleon/Squirrel 平均超过当前 best +1.5 points，2/3 数据集胜出 | B1, B2 |
| C2: Gain comes from routing, not parameter/tuning budget | 防止被审稿人认为只是更复杂 | global/random/feature-only/no-mid-band ablation 显著弱于 full | B3 |
| C3: Method does not harm homophily | 证明不是只为小异配图过拟合 | Cora/CiteSeer smoke 不下降超过 1 point | B4 |

## Experiment Blocks

### Block 1: Main Heterophily Pilot

- **Claim tested**: C1。
- **Dataset / split / task**: Actor、Chameleon、Squirrel；Geom-GCN official 10 fixed splits；node classification。
- **Compared systems**: PolyGCL、GRASS、EDA-GCL、GCA、GRACE、NFR-GCL。
- **Metrics**: Accuracy/F1Mi mean±std；paired split wins。
- **Success criterion**: 三数据集平均超过当前 best local baseline 至少 +1.5 points，至少 2/3 数据集胜出。
- **Failure interpretation**: 如果不超过阈值，不写强 claim；切换 I6 backup。
- **Priority**: MUST-RUN。

### Block 2: WebKB Backup / Robustness

- **Claim tested**: C1 robustness。
- **Dataset**: Cornell、Texas、Wisconsin official 10 fixed splits。
- **Compared systems**: GRASS、PolyGCL、EDA-GCL、NFR-GCL。
- **Success criterion**: 不要求全赢 GRASS，但至少不能明显退化；若 NFR-GCL 失败而 I6 强，切 backup。
- **Priority**: MUST-RUN after Block 1 positive or for backup decision。

### Block 3: Routing Ablations

- **Claim tested**: C2。
- **Variants**: full router、global learned alpha/beta、random router、feature-only router、graph-level router、no-mid-band、no-compatibility features、matched-parameter MLP。
- **Success criterion**: full router 在主数据集平均优于所有 routing ablations。
- **Priority**: MUST-RUN if Block 1 positive。

### Block 4: Homophily No-Regression

- **Claim tested**: C3。
- **Dataset**: Cora、CiteSeer；optional Amazon-Photo/Amazon-Computers。
- **Compared systems**: PolyGCL、BGRL、EDA-GCL、NFR-GCL。
- **Success criterion**: 不下降超过 1 point；若提升则只作为 supporting evidence。
- **Priority**: MUST-RUN smoke, NICE-TO-HAVE full 10-run。

### Block 5: Diagnostics

- **Claim tested**: mechanism plausibility。
- **Outputs**: router distribution by dataset、router entropy、correlation with post-hoc label homophily、frequency energy histograms、per-split route usage。
- **Success criterion**: NFR-GCL 在异配图中使用更多 high/mid routing，而同配图中更多 low/mid routing；这只是解释性证据，不作为训练信号。
- **Priority**: NICE-TO-HAVE after positive results。

## Run Order and Milestones

| Milestone | Goal | Runs | Decision Gate | Cost | Risk |
|---|---|---|---|---|---|
| M0 | sanity | Chameleon split0, 50-100 epochs | loss finite, router not collapsed | <1 GPU-hour | router/loss bug |
| M1 | decisive pilot | Actor/Chameleon/Squirrel 10 splits | avg +1.5 and 2/3 wins | 1-2 GPU-days estimated | no signal |
| M2 | ablation | routing variants on positive datasets | full beats ablations | 1 GPU-day | attribution weak |
| M3 | no-regression | Cora/CiteSeer smoke | drop <=1 point | <1 GPU-day | overfit heterophily |
| M4 | backup gate | I6 on WebKB if NFR fails | avg +2 over GRASS/PolyGCL | 1 GPU-day | novelty weak |

## Final Checklist

- [ ] Main heterophily table uses official splits.
- [ ] Strong baselines include PolyGCL and GRASS.
- [ ] Ablations isolate node router and mid-band view.
- [ ] No label leakage in routing features.
- [ ] Results below threshold are reported as negative/partial, not oversold.

