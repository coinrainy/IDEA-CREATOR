---
type: paper
node_id: paper:zhu2020_deep_graph_contrastive
title: "Deep Graph Contrastive Representation Learning"
authors: ["Yanqiao Zhu", "Yichen Xu", "Feng Yu", "Qiang Liu", "Shu Wu", "Liang Wang"]
year: 2020
venue: "arXiv"
external_ids:
  arxiv: "2006.04131"
  doi: null
  s2: null
tags: []
added: 2026-06-21T08:38:37Z
---

# Deep Graph Contrastive Representation Learning

## One-line thesis
GRACE 通过节点级跨视图对比和结构/属性双重扰动，建立了经典的 graph contrastive learning 框架。

## Problem / Gap
监督式 GNN 依赖大量标签，传统无监督图表示方法又常过度依赖图邻近重构或低效负采样。DGI 的 local-global contrast 还依赖全图 readout，并且单纯 feature shuffling 在稀疏特征上可能不足。

## Method
GRACE 为同一图生成两个 corrupted views，并用共享 GNN encoder 得到两组节点表示。训练目标直接最大化同一节点跨视图 embedding 的 agreement，同时把其他节点的 inter-view 与 intra-view embeddings 当作 negatives。view generation 同时包括 edge removal 和 feature masking，理论上从 mutual information 与 triplet loss 两个角度解释 objective。

## Key Results
- GRACE 在 Cora、Citeseer、Pubmed、DBLP、Reddit、PPI 等 6 个 benchmark 上显著超过无监督 baselines。
- alphaXiv overview 报告 PPI 上 GRACE micro-F1 为 66.2%，高于 DGI 的 63.8%。
- 消融显示 edge removal 与 feature masking 都重要，加入 intra-view negatives 的 objective 优于 strict InfoNCE 变体。

## Assumptions
- 同一节点的不同 corrupted views 应被拉近，其他节点默认作为 negatives。
- 随机 edge removal 与 feature masking 能产生语义保持但足够不同的 graph views。
- 评估覆盖 transductive 与 inductive node classification，但主要不是异配图专项设置。

## Limitations / Failure Modes
- 负样本默认来自其他节点，在异配或类别不均衡图上可能产生 false negatives。
- 随机 augmentation 未显式判断哪些边或特征对当前图是重要/有害的。
- 论文没有提供 heterophily-specific routing 或 raw fallback 机制。

## Reusable Ingredients
- 节点级跨视图 contrastive objective 是后续 GRACE/GCA 系列的基础模板。
- edge removal + feature masking 的双扰动可作为最小 GCL baseline。
- intra-view negatives 可用于检查 smoothing 导致的同视图表示过近问题。

## Open Questions
- 在异配图上，随机 edge removal 是否会破坏本来就稀缺的有用结构？
- 能否用无标签 edge compatibility 指标替换 GRACE 的均匀 augmentation？

## Claims
_No claims tracked yet — populate via /result-to-claim._

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

## Relevance to This Project
GRACE 是本项目所有图对比学习候选必须对照的基础范式。当前 LIFT-PROP 更偏向训练-free 传播选择，但仍需要用 GRACE 的 augmentation/negative-sample 逻辑解释为什么简单对比目标可能在异配图上失效。

## Abstract (original)

> Graph representation learning nowadays becomes fundamental in analyzing graph-structured data. Inspired by recent success of contrastive methods, in this paper, we propose a novel framework for unsupervised graph representation learning by leveraging a contrastive objective at the node level. Specifically, we generate two graph views by corruption and learn node representations by maximizing the agreement of node representations in these two views. To provide diverse node contexts for the contrastive objective, we propose a hybrid scheme for generating graph views on both structure and attribute levels. Besides, we provide theoretical justification behind our motivation from two perspectives, mutual information and the classical triplet loss. We perform empirical experiments on both transductive and inductive learning tasks using a variety of real-world datasets. Experimental experiments demonstrate that despite its simplicity, our proposed method consistently outperforms existing state-of-the-art methods by large margins. Moreover, our unsupervised method even surpasses its supervised counterparts on transductive tasks, demonstrating its great potential in real-world applications.
