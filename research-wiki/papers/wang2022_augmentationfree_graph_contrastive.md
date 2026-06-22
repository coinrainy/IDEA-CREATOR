---
type: paper
node_id: paper:wang2022_augmentationfree_graph_contrastive
title: "Augmentation-Free Graph Contrastive Learning with Performance Guarantee"
authors: ["Haonan Wang", "Jieyu Zhang", "Qi Zhu", "Wei Huang"]
year: 2022
venue: "arXiv"
external_ids:
  arxiv: "2204.04874"
  doi: null
  s2: null
tags: []
added: 2026-06-21T08:38:37Z
---

# Augmentation-Free Graph Contrastive Learning with Performance Guarantee

## One-line thesis
AF-GCL 用 GNN 聚合特征构造自监督信号，避免传统 graph augmentations 对高频异配信息的破坏。

## Problem / Gap
传统 GCL 依赖 graph augmentations 学习 view-invariant representation，但这些扰动主要保留低频分量、破坏中高频分量。该偏置有利于同配图，却会伤害依赖高频信息的异配图。

## Method
论文从 spectral theory 分析 edge dropping、feature masking 等 augmentation 的频率效应。AF-GCL 不再手工构造两个 augmentation views，而是利用 GNN 聚合后的 features 构造 self-supervision signal。作者进一步给出 AF-GCL 的 performance guarantee，并用该理论解释其在不同 homophily degree 图上的有效性。

## Key Results
- AF-GCL 在 8 个 homophilic graph benchmarks 上达到 competitive or better performance。
- 在 6 个 heterophilic graph benchmarks 上，AF-GCL 超过已有 state-of-the-art GCL 方法。
- 论文报告 AF-GCL 具有 significantly less computational overhead。

## Assumptions
- 分析建立在图频率视角和 GNN 聚合特征可提供有效 self-supervision 的假设上。
- 主要任务是 transductive node classification。
- 理论保证依赖论文定义的 graph data assumption 与同/异配频率结构。

## Limitations / Failure Modes
- 论文明确承认主要关注 node classification，regression 和 graph classification 留作未来工作。
- AF-GCL 使用聚合特征作为信号，仍需判断聚合在 raw-dominant 或强异配数据上是否会引入错误平滑。
- 方法证明 augmentation-free 有效，但没有解决每个节点应选择 identity、low-pass 还是 high-pass 的局部路由问题。

## Reusable Ingredients
- 用 spectral analysis 检查 augmentation 是否过度保留低频、破坏高频。
- augmentation-free self-supervision 可作为 LIFT-PROP 中“传播本身是否足够”的近邻 prior。
- 将 homophily degree 与频率偏好关联起来，可作为 selector 设计的理论语言。

## Open Questions
- 能否从 AF-GCL 的图级频率结论推进到 node-level 或 edge-level 的无标签传播选择？
- 聚合特征 self-supervision 在 Actor/Texas/Wisconsin 这类 raw-dominant 场景中何时应被关闭？

## Claims
_No claims tracked yet — populate via /result-to-claim._

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

## Relevance to This Project
这篇是 LIFT-PROP 的重要边界先验：它说明训练-free 或 augmentation-free 的传播/聚合信号可以很强，但也提醒异配图中高频信息容易被平滑破坏。本项目的 edge-lift gate 可被看作对 AF-GCL 图级频率动机的无标签选择化补充。

## Abstract (original)

> Graph contrastive learning (GCL) is the most representative and prevalent self-supervised learning approach for graph-structured data. Despite its remarkable success, existing GCL methods highly rely on an augmentation scheme to learn the representations invariant across different augmentation views. In this work, we revisit such a convention in GCL through examining the effect of augmentation techniques on graph data via the lens of spectral theory. We found that graph augmentations preserve the low-frequency components and perturb the middle-and high-frequency components of the graph, which contributes to the success of GCL algorithms on homophilic graphs but hinder its application on heterophilic graphs, due to the high-frequency preference of heterophilic data. Motivated by this, we propose a novel, theoretically-principled, and augmentation-free GCL method, named AF-GCL, that (1) leverages the features aggregated by Graph Neural Network to construct the self-supervision signal instead of augmentations and therefore (2) is less sensitive to the graph homophily degree. Theoretically, We present the performance guarantee for AF-GCL as well as an analysis for understanding the efficacy of AF-GCL. Extensive experiments on 14 benchmark datasets with varying degrees of heterophily show that AF-GCL presents competitive or better performance on homophilic graphs and outperforms all existing state-of-the-art GCL methods on heterophilic graphs with significantly less computational overhead.
