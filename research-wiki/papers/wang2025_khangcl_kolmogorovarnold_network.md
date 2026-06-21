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

> Graph contrastive learning (GCL) has demonstrated great promise for learning generalizable graph representations from unlabeled data. However, conventional GCL approaches face two critical limitations: (1) the restricted expressive capacity of multilayer perceptron (MLP) based encoders, and (2) suboptimal negative samples that either from random augmentations-failing to provide effective 'hard negatives'-or generated hard negatives without addressing the semantic distinctions crucial for discriminating graph data. To this end, we propose Khan-GCL, a novel framework that integrates the Kolmogorov-Arnold Network (KAN) into the GCL encoder architecture, substantially enhancing its representational capacity. Furthermore, we exploit the rich information embedded within KAN coefficient parameters to develop two novel critical feature identification techniques that enable the generation of semantically meaningful hard negative samples for each graph representation. These strategically constructed hard negatives guide the encoder to learn more discriminative features by emphasizing critical semantic differences between graphs. Extensive experiments demonstrate that our approach achieves state-of-the-art performance compared to existing GCL methods across a variety of datasets and tasks.

