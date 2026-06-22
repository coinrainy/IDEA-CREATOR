---
type: paper
node_id: paper:chen2024_leveraging_contrastive_learning
title: "Leveraging Contrastive Learning for Enhanced Node Representations in Tokenized Graph Transformers"
authors: ["Jinsong Chen", "Hanpeng Liu", "John E. Hopcroft", "Kun He"]
year: 2024
venue: "arXiv"
external_ids:
  arxiv: "2406.19258"
  doi: null
  s2: null
tags: []
added: 2026-06-21T08:38:37Z
---

# Leveraging Contrastive Learning for Enhanced Node Representations in Tokenized Graph Transformers

## One-line thesis
GCFormer 用正负 token 序列和 contrastive learning 提升 tokenized graph Transformer 的节点表示。

## Problem / Gap
现有 node tokenized graph Transformers 主要依赖高相似节点构造 token 序列，会丢掉低相似但携带互补信息的节点。GNN 的 message passing 还受 over-smoothing 和 over-squashing 限制，难以稳定捕获长程依赖。

## Method
GCFormer 设计 hybrid token generator，同时生成 positive token sequences 和 negative token sequences。它用定制的 Transformer backbone 编码这些序列，再通过 contrastive learning 从正负 token 中学习可区分的节点表示。相对只采样高相似 token 的方法，GCFormer 显式保留 node representation 的 commonality 和 disparity。

## Key Results
- 在 8 个同配/异配节点分类数据集上，GCFormer 在表 1 中均取得最好平均准确率。
- 补充实验显示，GCFormer 在所有数据集上优于代表性 GCL 方法和 GraphGPS 配置。
- 消融结果表明，引入 negative token sequences、Transformer 编码负 token 表示、以及 contrastive learning 都对性能有贡献。

## Assumptions
- 任务是带节点属性的 transductive node classification，且可以根据节点相似度采样 token 序列。
- 模型假设高相似节点和低相似节点都包含可利用信息，而不是只保留邻近或高相似 token。
- 采样规模和正负 token 融合权重需要按数据集调节。

## Limitations / Failure Modes
- 论文明确指出 GCFormer 使用统一采样策略，不同类型图上的最优 sampling size 不一致。
- 性能对 sampling size 敏感，作者认为需要 adaptive sampling strategy 来提升稳定性。
- 方法依赖 graph Transformer/tokenized pipeline，未展示能否直接迁移到轻量 BGRL 式训练框架。

## Reusable Ingredients
- 正负 token 序列同时采样：高相似 token 提供 commonality，低相似 token 提供 disparity。
- 用负 token 表示作为辅助视角，而不是只把它们当作需要排斥的噪声样本。
- 对 sampling size 的敏感性分析可作为无标签图属性诊断的参考。

## Open Questions
- 能否用无标签统计量为不同图自动选择 positive/negative token 的采样规模？
- 正负 token 机制能否在非 Transformer 的轻量 GCL encoder 中复用？

## Claims
_No claims tracked yet — populate via /result-to-claim._

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

## Relevance to This Project
本项目正在寻找适合图对比学习节点分类、尤其是异配图的轻量机制；GCFormer 提供了“正负结构信息都要保留”的有用信号。由于项目约束偏向现有 `baselines/` harness，GCFormer 更适合作为设计启发或边界基线，而不是立即新开 graph Transformer 代码栈。

## Abstract (original)

> While tokenized graph Transformers have demonstrated strong performance in node classification tasks, their reliance on a limited subset of nodes with high similarity scores for constructing token sequences overlooks valuable information from other nodes, hindering their ability to fully harness graph information for learning optimal node representations. To address this limitation, we propose a novel graph Transformer called GCFormer. Unlike previous approaches, GCFormer develops a hybrid token generator to create two types of token sequences, positive and negative, to capture diverse graph information. And a tailored Transformer-based backbone is adopted to learn meaningful node representations from these generated token sequences. Additionally, GCFormer introduces contrastive learning to extract valuable information from both positive and negative token sequences, enhancing the quality of learned node representations. Extensive experimental results across various datasets, including homophily and heterophily graphs, demonstrate the superiority of GCFormer in node classification, when compared to representative graph neural networks (GNNs) and graph Transformers.
