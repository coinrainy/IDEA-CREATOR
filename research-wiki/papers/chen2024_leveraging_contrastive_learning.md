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

> While tokenized graph Transformers have demonstrated strong performance in node classification tasks, their reliance on a limited subset of nodes with high similarity scores for constructing token sequences overlooks valuable information from other nodes, hindering their ability to fully harness graph information for learning optimal node representations. To address this limitation, we propose a novel graph Transformer called GCFormer. Unlike previous approaches, GCFormer develops a hybrid token generator to create two types of token sequences, positive and negative, to capture diverse graph information. And a tailored Transformer-based backbone is adopted to learn meaningful node representations from these generated token sequences. Additionally, GCFormer introduces contrastive learning to extract valuable information from both positive and negative token sequences, enhancing the quality of learned node representations. Extensive experimental results across various datasets, including homophily and heterophily graphs, demonstrate the superiority of GCFormer in node classification, when compared to representative graph neural networks (GNNs) and graph Transformers.

