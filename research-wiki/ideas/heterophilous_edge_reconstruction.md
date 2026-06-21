---
type: idea
node_id: idea:heterophilous_edge_reconstruction
title: "Masked Heterophilous Edge Reconstruction"
stage: proposed
status: backup
outcome: pending
fair_test_status: not_run
based_on: ["paper:yang2023_graph_contrastive_learning"]
target_gaps: ["gap:G2", "gap:G4", "gap:G5"]
added: 2026-06-21T08:48:28Z
---

# Masked Heterophilous Edge Reconstruction

## Status

BACKUP / ACTIVE. Codex reviewer ranked this second with paper potential 7.2/10.

## Hypothesis

GRASS-style masked-edge reconstruction can be improved by reconstructing unsupervised edge compatibility types instead of binary edge existence.

## Proposed Method

Replace GRASS random negative edge reconstruction with a three-way objective: homophilic-compatible edge, heterophilic-compatible edge, and noise/non-edge.

## Fair Test

Cornell, Texas, and Wisconsin official 10 fixed splits against GRASS and PolyGCL. Success requires average +2 points over best-of-GRASS/PolyGCL or clear paired split wins on at least 2/3 datasets.

## Failure Notes

Not failed yet. Risk: novelty may collapse if the method is only GraphMAE/GRASS with different pseudo-labels.

## Connections

Edges are recorded in `graph/edges.jsonl`.

