---
type: idea
node_id: idea:heterophily_hard_negative_aux
title: "Heterophily-Aware Hard Negative Mining"
stage: proposed
status: auxiliary
outcome: pending
fair_test_status: not_run
based_on: ["paper:lee2025_similarities_embeddings_contrastive", "paper:wang2025_khangcl_kolmogorovarnold_network"]
target_gaps: ["gap:G3"]
added: 2026-06-21T08:48:28Z
---

# Heterophily-Aware Hard Negative Mining

## Status

DEPRIORITIZED as standalone. Keep only as an auxiliary ablation after NFR-GCL has positive pilot signal.

## Hypothesis

Compatibility-guarded hard negatives may improve NFR-GCL by avoiding false negatives in heterophilous neighborhoods.

## Proposed Method

Use local compatibility to stratify negatives. Increase pressure only for structurally close but compatibility-conflicting nodes.

## Fair Test

Compare no hard-negative, similarity-only hard-negative, and compatibility-guarded hard-negative variants after NFR-GCL passes the main pilot.

## Failure Notes

Standalone idea is too crowded and risky due to ProGCL/AUGCL/Khan-GCL and false-negative concerns.

## Connections

Edges are recorded in `graph/edges.jsonl`.

