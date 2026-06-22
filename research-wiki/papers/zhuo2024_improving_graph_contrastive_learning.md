---
type: paper
node_id: paper:zhuo2024_improving_graph_contrastive_learning
title: "Improving Graph Contrastive Learning via Adaptive Positive Sampling"
authors: "Jiaming Zhuo, Feiyang Qin, Can Cui, Kun Fu, Bingxin Niu, Mengzhu Wang, Yuanfang Guo, Chuan Wang, Zhen Wang, Xiaochun Cao, Liang Yang"
year: 2024
venue: CVPR 2024
url: https://openaccess.thecvf.com/content/CVPR2024/html/Zhuo_Improving_Graph_Contrastive_Learning_via_Adaptive_Positive_Sampling_CVPR_2024_paper.html
added: 2026-06-22T01:49:39+08:00
---

# Improving Graph Contrastive Learning via Adaptive Positive Sampling

## Relevance

HEATS is the closest global-positive-sampling prior for DCGCL. It constructs adaptive positive sample matrices motivated by block-diagonal and idempotent properties, then alternates matrix construction with contrastive optimization.

## Constraint for DCGCL

DCGCL must not claim novelty for global positive sampling alone. The defensible delta is dual-teacher prototype disagreement calibration: feature-only and propagation-view teachers can agree or disagree, and disagreement is preserved through dual heads rather than forced into one positive block.
