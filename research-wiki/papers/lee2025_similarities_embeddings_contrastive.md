---
type: paper
node_id: paper:lee2025_similarities_embeddings_contrastive
title: "On the Similarities of Embeddings in Contrastive Learning"
authors: ["Chungpa Lee", "Sehee Lim", "Kibok Lee", "Jy-yong Sohn"]
year: 2025
venue: "International Conference on Machine Learning (ICML) 2025"
external_ids:
  arxiv: "2506.09781"
  doi: null
  s2: null
tags: []
added: 2026-06-21T08:38:37Z
---

# On the Similarities of Embeddings in Contrastive Learning

## One-line thesis
该文用 cosine similarity 统一分析 contrastive embeddings，并提出降低 mini-batch negative similarity 方差的辅助损失。

## Problem / Gap
现有 contrastive learning 理论多依赖特定 loss，难以统一解释 full-batch 与 mini-batch 学到的 embedding 几何。实际训练常用 mini-batch，但小 batch 会改变 negative-pair similarity 分布并损害表示质量。

## Method
论文以 positive-pair 和 negative-pair 的 cosine similarity 为核心建立统一分析框架。在 full-batch 设置中，它证明当 negative-pair similarities 低于阈值时 perfect alignment 不可达，并指出加入 within-view negative pairs 可以缓解 misalignment。在 mini-batch 设置中，它分析小 batch 如何增加 negative-pair similarity 方差，并提出一个显式惩罚该方差的 auxiliary loss。

## Key Results
- 理论结果解释了 full-batch 下 positive alignment 与 negative separation 之间的阈值条件。
- 论文证明 batch size 变小时 negative-pair similarities 的方差会增大，从而降低 learned representation 质量。
- CIFAR 和 ImageNet 实验显示，该 auxiliary loss 在小 batch 设置下能提升 SimCLR、DCL、DHEL 等 CL 方法表现。

## Assumptions
- 分析围绕 normalized embeddings 与 cosine similarity 展开。
- 训练范式假设存在明确的 positive pairs 与 negative pairs。
- 实验主体是视觉数据集和 ResNet backbone，不是图节点分类任务。

## Limitations / Failure Modes
- 论文指出，negative-pair similarity 的方差有时可能承载语义差异，强行压低方差会抑制有用结构。
- batch size 较大时，该 loss 的边际收益会自然减弱。
- 方法新增超参数 `lambda`，需要调参。

## Reusable Ingredients
- 用 negative similarity distribution 的方差诊断 contrastive objective 是否过度分离。
- within-view negatives 可作为缓解 positive misalignment 的设计手段。
- 对小 batch 训练的几何分析可用于解释本项目中轻量 GPU 设置下的 GCL 稳定性。

## Open Questions
- 图节点上的 false negative 与 heterophily 会不会让“压低 negative similarity 方差”变成有害约束？
- 能否把该理论扩展到 graph propagation 后的节点 embedding，而不只是一组独立样本？

## Claims
_No claims tracked yet — populate via /result-to-claim._

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

## Relevance to This Project
本项目多次遇到 hard negative、false negative 和小批量/全图训练之间的张力；这篇论文提供了可复用的 embedding 几何诊断。它不是图论文，但能帮助审查新的 GCL loss 是否只是改变了 negative similarity 分布。

## Abstract (original)

> Contrastive learning operates on a simple yet effective principle: Embeddings of positive pairs are pulled together, while those of negative pairs are pushed apart. In this paper, we propose a unified framework for understanding contrastive learning through the lens of cosine similarity, and present two key theoretical insights derived from this framework. First, in full-batch settings, we show that perfect alignment of positive pairs is unattainable when negative-pair similarities fall below a threshold, and this misalignment can be mitigated by incorporating within-view negative pairs into the objective. Second, in mini-batch settings, smaller batch sizes induce stronger separation among negative pairs in the embedding space, i.e., higher variance in their similarities, which in turn degrades the quality of learned representations compared to full-batch settings. To address this, we propose an auxiliary loss that reduces the variance of negative-pair similarities in mini-batch settings. Empirical results show that incorporating the proposed loss improves performance in small-batch settings.
