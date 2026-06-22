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

> Graph contrastive learning (CL) methods learn node representations in a self-supervised manner by maximizing the similarity between the augmented node representations obtained via a GNN-based encoder. However, CL methods perform poorly on graphs with heterophily, where connected nodes tend to belong to different classes. In this work, we address this problem by proposing an effective graph CL method, namely HLCL, for learning graph representations under heterophily. HLCL first identifies a homophilic and a heterophilic subgraph based on the cosine similarity of node features. It then uses a low-pass and a high-pass graph filter to aggregate representations of nodes connected in the homophilic subgraph and differentiate representations of nodes in the heterophilic subgraph. The final node representations are learned by contrasting both the augmented high-pass filtered views and the augmented low-pass filtered node views. Our extensive experiments show that HLCL outperforms state-of-the-art graph CL methods on benchmark datasets with heterophily, as well as large-scale real-world graphs, by up to 7%, and outperforms graph supervised learning methods on datasets with heterophily by up to 10%.

