---
type: idea
node_id: idea:compatibility_calibrated_edges
title: "Compatibility-Calibrated Contrastive Edges"
stage: killed
status: killed_standalone
outcome: negative
fair_test_status: reviewer_gate
based_on: ["paper:zhu2020_graph_contrastive_learning", "paper:yang2023_graph_contrastive_learning"]
target_gaps: ["gap:G2"]
added: 2026-06-21T08:48:28Z
---

# Compatibility-Calibrated Contrastive Edges

## Status

KILLED as standalone. Kept only as a routing signal inside NFR-GCL.

## Hypothesis

Edge compatibility can improve contrastive view construction by separating homophilic-compatible, heterophilic-compatible, and noisy edges.

## Proposed Method

Replace random or centrality-based edge dropping with compatibility-calibrated edge view construction.

## Failure Notes

Codex reviewer judged the standalone route too close to GCA, EDA-GCL, GREET, and HLCL. It should not be revived unless it independently beats both GCA and EDA-GCL on Chameleon/Squirrel/Texas.

## Connections

Edges are recorded in `graph/edges.jsonl`.

