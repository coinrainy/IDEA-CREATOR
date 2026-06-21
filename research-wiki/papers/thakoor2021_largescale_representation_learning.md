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

> Self-supervised learning provides a promising path towards eliminating the need for costly label information in representation learning on graphs. However, to achieve state-of-the-art performance, methods often need large numbers of negative examples and rely on complex augmentations. This can be prohibitively expensive, especially for large graphs. To address these challenges, we introduce Bootstrapped Graph Latents (BGRL) - a graph representation learning method that learns by predicting alternative augmentations of the input. BGRL uses only simple augmentations and alleviates the need for contrasting with negative examples, and is thus scalable by design. BGRL outperforms or matches prior methods on several established benchmarks, while achieving a 2-10x reduction in memory costs. Furthermore, we show that BGRL can be scaled up to extremely large graphs with hundreds of millions of nodes in the semi-supervised regime - achieving state-of-the-art performance and improving over supervised baselines where representations are shaped only through label information. In particular, our solution centered on BGRL constituted one of the winning entries to the Open Graph Benchmark - Large Scale Challenge at KDD Cup 2021, on a graph orders of magnitudes larger than all previously available benchmarks, thus demonstrating the scalability and effectiveness of our approach.

