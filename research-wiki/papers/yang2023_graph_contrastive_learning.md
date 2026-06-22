---
type: paper
node_id: paper:yang2023_graph_contrastive_learning
title: "Graph Contrastive Learning under Heterophily via Graph Filters"
authors: ["Wenhan Yang", "Baharan Mirzasoleiman"]
year: 2023
venue: "arXiv"
external_ids:
  arxiv: "2303.06344"
  doi: null
  s2: null
tags: []
added: 2026-06-21T08:38:37Z
---

# Graph Contrastive Learning under Heterophily via Graph Filters

## One-line thesis
HLCL 用特征相似度拆分同配/异配子图，并分别用 low-pass/high-pass filters 做异配图 GCL。

## Problem / Gap
普通 graph CL 在异配图上表现差，因为相连节点常属于不同类别，简单拉近 augmented views 会混淆语义。无标签场景下，关键难点是识别哪些邻域应聚合相似节点、哪些邻域应区分相连节点。

## Method
HLCL 先根据 node feature cosine similarity 从原图中识别 homophilic subgraph 和 heterophilic subgraph。随后对同配子图应用 low-pass graph filter 聚合相似节点，对异配子图应用 high-pass graph filter 区分相连但不同类的节点。最终表示通过同时 contrast augmented low-pass filtered views 和 high-pass filtered views 学得。

## Key Results
- HLCL 在异配 benchmark 上取得 state-of-the-art，并在同配图上保持 comparable performance。
- 论文报告 HLCL 在异配图上相对 graph CL baselines 最高提升 up to 7%。
- HLCL 还在异配数据集上超过 popular graph supervised learning methods up to 10%。

## Assumptions
- node feature similarity 能近似指示哪些边更同配、哪些边更异配。
- 同配子图适合 low-pass aggregation，异配子图适合 high-pass differentiation。
- 训练仍依赖 graph structure 对节点分类有帮助。

## Limitations / Failure Modes
- 论文明确指出，当 feature similarity 与 label similarity 几乎无关时，HLCL 和其他 SSL 方法会遇到困难；Penn94 是代表例子。
- Actor 这类图中结构对分类可能无益，仅依赖特征的 MLP 可超过 GNN/HLCL。
- 子图识别质量是关键瓶颈，作者认为更准确地找到同配/异配子图是未来方向。

## Reusable Ingredients
- 用 feature cosine similarity 做无标签 edge/subgraph routing。
- low-pass 与 high-pass filters 分别服务于相似聚合和差异放大。
- Actor/Penn94 失败模式可作为 LIFT-PROP gate 必须保留 raw fallback 的证据。

## Open Questions
- 能否用 edge-lift 或其他无标签指标替代 feature cosine 来判断 subgraph routing 是否可靠？
- 当 graph structure 不帮忙时，GCL 方法应如何自动退回 raw-feature 或 identity view？

## Claims
_No claims tracked yet — populate via /result-to-claim._

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

## Relevance to This Project
HLCL 是本项目异配图方向的核心近邻工作，也是 LIFT-PROP novelty risk 中的明确边界条件。它支持“不同图/边需要不同传播滤波”的动机，但也显示单靠 feature similarity routing 会在 raw-dominant 数据集上失效。

## Abstract (original)

> Graph contrastive learning (CL) methods learn node representations in a self-supervised manner by maximizing the similarity between the augmented node representations obtained via a GNN-based encoder. However, CL methods perform poorly on graphs with heterophily, where connected nodes tend to belong to different classes. In this work, we address this problem by proposing an effective graph CL method, namely HLCL, for learning graph representations under heterophily. HLCL first identifies a homophilic and a heterophilic subgraph based on the cosine similarity of node features. It then uses a low-pass and a high-pass graph filter to aggregate representations of nodes connected in the homophilic subgraph and differentiate representations of nodes in the heterophilic subgraph. The final node representations are learned by contrasting both the augmented high-pass filtered views and the augmented low-pass filtered node views. Our extensive experiments show that HLCL outperforms state-of-the-art graph CL methods on benchmark datasets with heterophily, as well as large-scale real-world graphs, by up to 7%, and outperforms graph supervised learning methods on datasets with heterophily by up to 10%.
