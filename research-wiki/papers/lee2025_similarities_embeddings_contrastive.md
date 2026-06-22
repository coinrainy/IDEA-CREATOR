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
_TODO: fill in after reading._

## Problem / Gap
_TODO._

## Method
_TODO._

## Key Results
_TODO._

## Assumptions
_TODO._

## Limitations / Failure Modes
_TODO._

## Reusable Ingredients
_TODO._

## Open Questions
_TODO._

## Claims
_TODO._

## Connections
_Edges are recorded in `graph/edges.jsonl`; summarize here for human readers._

## Relevance to This Project
_TODO._

## Abstract (original)

> Contrastive learning operates on a simple yet effective principle: Embeddings of positive pairs are pulled together, while those of negative pairs are pushed apart. In this paper, we propose a unified framework for understanding contrastive learning through the lens of cosine similarity, and present two key theoretical insights derived from this framework. First, in full-batch settings, we show that perfect alignment of positive pairs is unattainable when negative-pair similarities fall below a threshold, and this misalignment can be mitigated by incorporating within-view negative pairs into the objective. Second, in mini-batch settings, smaller batch sizes induce stronger separation among negative pairs in the embedding space, i.e., higher variance in their similarities, which in turn degrades the quality of learned representations compared to full-batch settings. To address this, we propose an auxiliary loss that reduces the variance of negative-pair similarities in mini-batch settings. Empirical results show that incorporating the proposed loss improves performance in small-batch settings.

