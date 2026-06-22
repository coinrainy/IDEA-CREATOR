---
type: idea
node_id: idea:node_local_bgrl
title: "Augmentation-Free Node-Local BGRL"
stage: proposed
status: deprioritized
outcome: pending
fair_test_status: not_run
based_on: ["paper:thakoor2021_largescale_representation_learning", "paper:wang2022_augmentationfree_graph_contrastive"]
target_gaps: ["gap:G1", "gap:G5"]
added: 2026-06-21T08:48:28Z
---

# Augmentation-Free Node-Local BGRL

## Status

DEPRIORITIZED. BGRL is strong on homophily but weak/incomplete on heterophily; reviewer judged this route too incremental unless it beats PolyGCL/GRASS.

## Hypothesis

Node-local filtered targets could repair BGRL's heterophily weakness.

## Proposed Method

Use low/high filtered target embeddings in the BGRL target encoder and original or mixed-frequency embeddings in the online encoder.

## Fair Test

First complete BGRL heterophily baselines on Squirrel/WebKB. Then compare node-local BGRL against BGRL, AF-GCL, PolyGCL, and GRASS.

## Failure Notes

Standalone novelty is weak: likely perceived as BGRL plus filter unless empirical results are very strong.

## Connections

Edges are recorded in `graph/edges.jsonl`.

