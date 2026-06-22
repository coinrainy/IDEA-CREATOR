---
type: paper
node_id: paper:thakoor2021_largescale_representation_learning
title: "Large-Scale Representation Learning on Graphs via Bootstrapping"
authors: ["Shantanu Thakoor", "Corentin Tallec", "Mohammad Gheshlaghi Azar", "Mehdi Azabou", "Eva L. Dyer", "Rémi Munos", "Petar Veličković", "Michal Valko"]
year: 2021
venue: "arXiv"
external_ids:
  arxiv: "2102.06514"
  doi: null
  s2: null
tags: []
added: 2026-06-21T08:38:37Z
---

# Large-Scale Representation Learning on Graphs via Bootstrapping

## One-line thesis
BGRL 用 bootstrap prediction 替代负样本对比，在图表示学习中实现可扩展的自监督训练。

## Problem / Gap
早期图自监督方法多依赖大量 negative examples 和复杂 augmentation，计算与显存成本在大图上很高。图表示学习需要一种不依赖二次级负样本比较、但仍能保持性能的训练目标。

## Method
Bootstrapped Graph Latents (BGRL) 使用 online encoder 预测同一图的另一个 augmented view 经过 target encoder 得到的表示。target encoder 通过 moving average 更新，训练不使用 negative examples，只依赖简单 graph augmentations。由于每个节点主要预测自身跨视图 target，BGRL 的内存与计算更适合大规模图。

## Key Results
- BGRL 在多个标准 benchmark 上超过或匹配 prior methods，同时显存成本降低 2-10x。
- 在 5 个 medium-scale 数据集上，BGRL 达到 4/5 个数据集的 state-of-the-art 表现。
- BGRL 扩展到 MAG240M 等超大图，并成为 KDD Cup 2021 OGB Large Scale Challenge 获奖方案的一部分。

## Assumptions
- 训练依赖两个简单 augmented graph views，且 bootstrap target 不需要显式负样本。
- EMA target encoder 能提供足够稳定的预测目标，避免 trivial collapse。
- 大规模设置下可以结合 sampled subgraphs 或 semi-supervised training。

## Limitations / Failure Modes
- 论文伦理说明指出，unsupervised pretraining embedding 若未经审查用于下游任务，可能继承或放大 bias。
- 作者也承认 BGRL 的 bootstrapping dynamics 尚未完全理解，黑盒使用时错误更难诊断。
- BGRL 主要解决可扩展性和负样本成本，不直接解决 heterophily 下传播何时有害的问题。

## Reusable Ingredients
- EMA target encoder + online predictor 的负样本自由训练框架。
- 简单 augmentation 即可工作的 bootstrap objective，适合作为本项目方法原型底座。
- 显存/性能 trade-off 表可作为评估新 GCL 方法是否值得扩展的工程基线。

## Open Questions
- BGRL 的 non-collapse 机制在异配图和 raw-dominant 数据集上是否仍然可靠？
- 能否加入无标签传播选择或 edge-lift gate，而不破坏 BGRL 的可扩展性？

## Claims
_No claims tracked yet — populate via /result-to-claim._

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

## Relevance to This Project
BGRL 是当前 `baselines/BGRL` harness 的核心底座，也是 LIFT-PROP 和多个失败候选的实现载体。该文说明了为什么项目应优先做轻量、可复现的小改动，而不是引入显存昂贵的全新对比框架。

## Abstract (original)

> Self-supervised learning provides a promising path towards eliminating the need for costly label information in representation learning on graphs. However, to achieve state-of-the-art performance, methods often need large numbers of negative examples and rely on complex augmentations. This can be prohibitively expensive, especially for large graphs. To address these challenges, we introduce Bootstrapped Graph Latents (BGRL) - a graph representation learning method that learns by predicting alternative augmentations of the input. BGRL uses only simple augmentations and alleviates the need for contrasting with negative examples, and is thus scalable by design. BGRL outperforms or matches prior methods on several established benchmarks, while achieving a 2-10x reduction in memory costs. Furthermore, we show that BGRL can be scaled up to extremely large graphs with hundreds of millions of nodes in the semi-supervised regime - achieving state-of-the-art performance and improving over supervised baselines where representations are shaped only through label information. In particular, our solution centered on BGRL constituted one of the winning entries to the Open Graph Benchmark - Large Scale Challenge at KDD Cup 2021, on a graph orders of magnitudes larger than all previously available benchmarks, thus demonstrating the scalability and effectiveness of our approach.
