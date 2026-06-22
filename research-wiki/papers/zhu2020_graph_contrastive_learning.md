---
type: paper
node_id: paper:zhu2020_graph_contrastive_learning
title: "Graph Contrastive Learning with Adaptive Augmentation"
authors: ["Yanqiao Zhu", "Yichen Xu", "Feng Yu", "Qiang Liu", "Shu Wu", "Liang Wang"]
year: 2020
venue: "arXiv"
external_ids:
  arxiv: "2010.14945"
  doi: null
  s2: null
tags: []
added: 2026-06-21T08:38:37Z
---

# Graph Contrastive Learning with Adaptive Augmentation

## One-line thesis
GCA 用 centrality-aware adaptive augmentation 替代均匀扰动，让 graph CL 更保留重要结构和属性。

## Problem / Gap
多数 graph CL 方法把 edge dropping 和 feature corruption 设为均匀随机过程，缺少对哪些边/特征应被保留的建模。这样的 augmentation 可能扰动关键结构和语义，导致表示学习次优。

## Method
GCA 根据 topological 与 semantic priors 设计 adaptive augmentation。拓扑层面，它用 node centrality measures 估计边的重要性，对不重要边赋予更高 removal probability；属性层面，它对不重要 feature dimensions 添加更多噪声。模型再最大化两个 adaptive augmented views 的节点 embedding agreement。

## Key Results
- GCA 在 Wiki-CS、Amazon-Computers、Amazon-Photo、Coauthor-CS、Coauthor-Physics 等节点分类数据集上优于现有 state-of-the-art baselines。
- 论文报告该无监督方法在部分数据集上超过若干 supervised counterparts。
- 消融显示 adaptive edge removal 与 adaptive feature masking 都能稳定提升性能。

## Assumptions
- centrality measures 能识别对图连通结构更重要的节点/边。
- 不重要 feature dimensions 加噪更安全，且能迫使模型关注底层语义。
- 数据 augmentation 应保持图的 intrinsic structure 和 attributes。

## Limitations / Failure Modes
- 论文指出，具体 augmentation functions 与 mutual-information lower bound 之间的关系仍难以推导，留作未来工作。
- 评估主要围绕常见同配节点分类数据集，没有给出 heterophily-specific 安全机制。
- centrality-aware edge dropping 仍以 edge importance 为核心，未区分同配兼容边、异配有用边和噪声边。

## Reusable Ingredients
- 根据 edge/node importance 非均匀选择 augmentation 强度。
- 将 topology prior 与 feature prior 分开建模，便于做消融。
- “保留 intrinsic structure/attributes”的原则可作为评估 LIFT-PROP selector 是否过度平滑的标准。

## Open Questions
- centrality prior 在 Texas/Wisconsin/Actor 这类 raw-dominant 或异配图上是否仍可靠？
- 能否把 GCA 的 adaptive augmentation 改成 label-free propagation depth selection？

## Claims
_No claims tracked yet — populate via /result-to-claim._

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

## Relevance to This Project
GCA 是 edge/feature 自适应增强的经典边界条件，本项目后续任何“自适应图视图”贡献都必须与它区分。LIFT-PROP 当前的差异在于选择传播深度/是否退回 raw，而不是重新设计随机 edge dropping。

## Abstract (original)

> Recently, contrastive learning (CL) has emerged as a successful method for unsupervised graph representation learning. Most graph CL methods first perform stochastic augmentation on the input graph to obtain two graph views and maximize the agreement of representations in the two views. Despite the prosperous development of graph CL methods, the design of graph augmentation schemes -- a crucial component in CL -- remains rarely explored. We argue that the data augmentation schemes should preserve intrinsic structures and attributes of graphs, which will force the model to learn representations that are insensitive to perturbation on unimportant nodes and edges. However, most existing methods adopt uniform data augmentation schemes, like uniformly dropping edges and uniformly shuffling features, leading to suboptimal performance. In this paper, we propose a novel graph contrastive representation learning method with adaptive augmentation that incorporates various priors for topological and semantic aspects of the graph. Specifically, on the topology level, we design augmentation schemes based on node centrality measures to highlight important connective structures. On the node attribute level, we corrupt node features by adding more noise to unimportant node features, to enforce the model to recognize underlying semantic information. We perform extensive experiments of node classification on a variety of real-world datasets. Experimental results demonstrate that our proposed method consistently outperforms existing state-of-the-art baselines and even surpasses some supervised counterparts, which validates the effectiveness of the proposed contrastive framework with adaptive augmentation.
