---
type: paper
node_id: paper:wang2025_khangcl_kolmogorovarnold_network
title: "Khan-GCL: Kolmogorov-Arnold Network Based Graph Contrastive Learning with Hard Negatives"
authors: ["Zihu Wang", "Boxun Xu", "Hejia Geng", "Peng Li"]
year: 2025
venue: "arXiv"
external_ids:
  arxiv: "2505.15103"
  doi: null
  s2: null
tags: []
added: 2026-06-21T08:38:37Z
---

# Khan-GCL: Kolmogorov-Arnold Network Based Graph Contrastive Learning with Hard Negatives

## One-line thesis
Khan-GCL 将 KAN encoder 与语义 hard negatives 结合，用于提升 graph-level contrastive representation。

## Problem / Gap
传统 GCL 常用 MLP-based encoders，表达能力受限。现有 hard negatives 要么来自随机 augmentation、难以提供有效难例，要么没有充分处理图语义差异。

## Method
Khan-GCL 把 Kolmogorov-Arnold Network (KAN) 引入 GCL encoder，以增强非线性建模能力。它利用 KAN coefficient parameters 设计 CKFI，识别 discriminative 和 independent features，并通过对关键特征做最小扰动生成 semantically meaningful hard negatives。训练时这些 hard negatives 迫使 encoder 学到更能区分图语义的表示。

## Key Results
- transfer learning 实验覆盖 Zinc-2M 预训练和 8 个 MoleculeNet biochemical datasets。
- unsupervised graph classification 在 8 个 TU-datasets 上评估，Khan-GCL 在 6/8 个数据集取得最好结果并得到最佳平均表现。
- 消融显示 KAN encoder 本身优于 MLP 对应版本，加入 hard negatives 后进一步提升。

## Assumptions
- 论文主要面向 graph classification / graph-level representation，而非节点分类。
- KAN coefficient parameters 被假设能暴露对图语义有用的 critical features。
- hard negative 通过 feature perturbation 构造，依赖扰动能改变语义但不完全破坏样本结构。

## Limitations / Failure Modes
- 作者指出未来需要探索 KAN intermediate layers 中的 feature perturbation 和 hard negative generation。
- KAN spline computations 带来额外训练成本，论文明确提出需要更高效架构来降低开销。
- 方法没有直接处理 heterophilous node classification 中的 false negative / false positive 图邻接陷阱。

## Reusable Ingredients
- 用模型内部系数或参数敏感性识别 critical features，而不是随机选择扰动维度。
- hard negative 应围绕语义差异构造，可作为本项目 hard-negative 方向的风险参照。
- KAN-vs-MLP 消融提醒新方法要区分 encoder capacity gain 和 contrastive objective gain。

## Open Questions
- KAN 系数导出的 critical features 能否迁移到 node-level 表示，还是只适合 graph-level 任务？
- 在异配图节点分类中，hard negative 是否会把真实同类但图上远离的节点错误推开？

## Claims
_No claims tracked yet — populate via /result-to-claim._

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

## Relevance to This Project
本项目的 gap map 已把 hard negatives 标为异配图风险点；Khan-GCL 提供了近期 hard-negative 设计的强 prior。它也提示后续方案必须证明收益来自无标签选择/传播机制，而不是更强 encoder 或更重计算。

## Abstract (original)

> Graph contrastive learning (GCL) has demonstrated great promise for learning generalizable graph representations from unlabeled data. However, conventional GCL approaches face two critical limitations: (1) the restricted expressive capacity of multilayer perceptron (MLP) based encoders, and (2) suboptimal negative samples that either from random augmentations-failing to provide effective 'hard negatives'-or generated hard negatives without addressing the semantic distinctions crucial for discriminating graph data. To this end, we propose Khan-GCL, a novel framework that integrates the Kolmogorov-Arnold Network (KAN) into the GCL encoder architecture, substantially enhancing its representational capacity. Furthermore, we exploit the rich information embedded within KAN coefficient parameters to develop two novel critical feature identification techniques that enable the generation of semantically meaningful hard negative samples for each graph representation. These strategically constructed hard negatives guide the encoder to learn more discriminative features by emphasizing critical semantic differences between graphs. Extensive experiments demonstrate that our approach achieves state-of-the-art performance compared to existing GCL methods across a variety of datasets and tasks.
