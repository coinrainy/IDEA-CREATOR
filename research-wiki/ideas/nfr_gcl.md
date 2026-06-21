---
type: idea
node_id: idea:nfr_gcl
title: "NFR-GCL: Node-Frequency Routed Graph Contrastive Learning"
stage: proposed
status: abandoned
outcome: stopped_for_low_novelty
fair_test_status: not_run
based_on: ["paper:yang2023_graph_contrastive_learning", "paper:wang2022_augmentationfree_graph_contrastive", "paper:zhu2020_deep_graph_contrastive"]
target_gaps: ["gap:G1", "gap:G4", "gap:G5"]
added: 2026-06-21T08:48:28Z
---

# NFR-GCL: Node-Frequency Routed Graph Contrastive Learning

## Status

ABANDONED / ARCHIVED. After a novelty scan on 2026-06-21, the idea was judged too close to recent node-level adaptive spectral fusion work for graph contrastive learning. The user decided not to continue this direction because its chance of becoming a strong new-paper contribution is low.

## Hypothesis

Node-wise routing over low/mid/high frequency views can outperform global high/low frequency mixing on heterophilous node classification.

## Proposed Method

Reuse PolyGCL/ChebNetII filters to compute low-, mid-, and high-pass node views. Learn a label-free node router from local feature similarity, structural compatibility, high-frequency energy, and residual statistics. Use the router to weight mixed-frequency contrastive consistency for each node.

## Fair Test

Actor, Chameleon, and Squirrel official 10 fixed splits. Must compare against PolyGCL, GRASS, EDA-GCL, GCA, and GRACE. Go/no-go: average +1.5 accuracy points over current best local baseline and at least 2/3 dataset wins.

## Failure Notes

Stopped before implementation. The main reason is novelty risk rather than an experimental failure. The closest-risk area is node-level adaptive low/high spectral fusion for graph contrastive learning; NFR-GCL would need a much sharper delta such as indispensable mid-band routing plus local compatibility-driven routing, but that is no longer the preferred path.

## Connections

Edges are recorded in `graph/edges.jsonl`.
