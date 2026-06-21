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

> Graph contrastive learning (GCL) is the most representative and prevalent self-supervised learning approach for graph-structured data. Despite its remarkable success, existing GCL methods highly rely on an augmentation scheme to learn the representations invariant across different augmentation views. In this work, we revisit such a convention in GCL through examining the effect of augmentation techniques on graph data via the lens of spectral theory. We found that graph augmentations preserve the low-frequency components and perturb the middle-and high-frequency components of the graph, which contributes to the success of GCL algorithms on homophilic graphs but hinder its application on heterophilic graphs, due to the high-frequency preference of heterophilic data. Motivated by this, we propose a novel, theoretically-principled, and augmentation-free GCL method, named AF-GCL, that (1) leverages the features aggregated by Graph Neural Network to construct the self-supervision signal instead of augmentations and therefore (2) is less sensitive to the graph homophily degree. Theoretically, We present the performance guarantee for AF-GCL as well as an analysis for understanding the efficacy of AF-GCL. Extensive experiments on 14 benchmark datasets with varying degrees of heterophily show that AF-GCL presents competitive or better performance on homophilic graphs and outperforms all existing state-of-the-art GCL methods on heterophilic graphs with significantly less computational overhead.

