---
type: idea
node_id: idea:srlp_gcl
title: "SRLP: Shortcut-Resistant Latent Prediction for Graph Self-Supervised Learning"
stage: proposed
status: ready_for_pilot
outcome: refined_ready_for_pilot
fair_test_status: planned_not_run
based_on: ["paper:thakoor2021_largescale_representation_learning", "paper:skenderi2023_graph_jepa", "paper:hou2023_graphmae2", "paper:srinivasan2025_predict_cluster_refine", "paper:shan2026_revisiting_positive_samples", "paper:li2026_aspect"]
target_gaps: ["gap:G3", "gap:G4", "gap:G5", "gap:G6"]
added: 2026-06-21T18:53:14+08:00
---

# SRLP: Shortcut-Resistant Latent Prediction for Graph Self-Supervised Learning

## Status

READY FOR PILOT after two reviewer rounds. No implementation or GPU pilot has been run yet.

## Hypothesis

Graph self-supervised learning becomes more useful for node classification when the positive target is the component of the target node's teacher latent that is not directly explained by the visible context subspace.

## Proposed Method

Use an EMA teacher encoder on the clean graph to produce node latents. For each target node, build a rank-1 visible-context direction from stop-gradient normalized teacher latents of its visible neighbors, then remove the projection of the stop-gradient target teacher latent onto that context direction. Low-energy residuals are skipped with an `epsilon` threshold and the skipped ratio is logged. The online encoder sees a target-isolated graph where target features are masked and all target incident edges are removed. It predicts the normalized context-projected residual with a cosine loss; the variance floor is only a collapse fallback, not part of the main method.

## Fair Test

Start with Cora and Chameleon single seed/split as a non-collapse pilot. The minimum controls are full-latent target, `Z-PZ` target, SRLP target, and no incident-edge-removal. If positive, run Actor, Chameleon, and Squirrel split 0. A full fair test must use the Geom-GCN official fixed splits for Actor, Chameleon, Squirrel, Cornell, Texas, and Wisconsin from `baselines/dataset_splits/heterophily/geom-gcn/`.

## Closest Prior Work

- BGRL predicts alternative augmented views with a bootstrap target encoder, but does not construct context-projected residual hidden targets.
- Graph-JEPA and JPEB-GSSL validate graph JEPA-style predictive learning, but they do not focus on target-isolated node-level context-projected residuals for heterophilous node classification.
- GraphMAE2 uses latent representation prediction inside masked feature reconstruction, but SRLP avoids raw reconstruction and predicts only the visible-context residual target.
- ASPECT covers node-level spectral fusion and must be cited as closest recent GCL prior, but SRLP is not a spectral routing method.
- SPGCL motivates the target design by showing that message passing can trivialize ordinary positive sample alignment.

## Failure Notes

Main risk: the context-projected residual may be too conditionally unpredictable after hard target isolation. Pilot must monitor residual raw norm, skipped target ratio, prediction cosine, embedding rank, and compare against full-latent and `Z-PZ` targets. If skipped ratio is high, tune `epsilon` or target ratio before adding any new module. If ablation shows SRLP does not beat full-latent targets, kill or demote the route quickly.

## Connections

Edges are recorded in `graph/edges.jsonl`.
