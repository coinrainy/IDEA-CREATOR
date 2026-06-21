---
type: idea
node_id: idea:nfr_gcl
title: "NFR-GCL: Node-Frequency Routed Graph Contrastive Learning"
stage: proposed
status: active
outcome: pending
fair_test_status: not_run
based_on: ["paper:yang2023_graph_contrastive_learning", "paper:wang2022_augmentationfree_graph_contrastive", "paper:zhu2020_deep_graph_contrastive"]
target_gaps: ["gap:G1", "gap:G4", "gap:G5"]
added: 2026-06-21T08:48:28Z
---

# NFR-GCL: Node-Frequency Routed Graph Contrastive Learning

## Status

ACTIVE / READY_TO_PILOT. Codex reviewer ranked this as the first-choice idea with paper potential 8.0/10.

## Hypothesis

Node-wise routing over low/mid/high frequency views can outperform global high/low frequency mixing on heterophilous node classification.

## Proposed Method

Reuse PolyGCL/ChebNetII filters to compute low-, mid-, and high-pass node views. Learn a label-free node router from local feature similarity, structural compatibility, high-frequency energy, and residual statistics. Use the router to weight mixed-frequency contrastive consistency for each node.

## Fair Test

Actor, Chameleon, and Squirrel official 10 fixed splits. Must compare against PolyGCL, GRASS, EDA-GCL, GCA, and GRACE. Go/no-go: average +1.5 accuracy points over current best local baseline and at least 2/3 dataset wins.

## Failure Notes

Not failed yet. Stop this route if the learned node router does not beat global/random router ablations or if gains fall below the go/no-go threshold.

## Connections

Edges are recorded in `graph/edges.jsonl`.

