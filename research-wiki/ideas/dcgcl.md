---
type: idea
node_id: idea:dcgcl
title: "DCGCL: Disagreement-Calibrated Prototype Graph Contrastive Learning"
stage: proposed
status: ready_for_pilot
outcome: paper_only_ready_for_pilot
fair_test_status: planned_not_run
based_on: ["paper:zhuo2024_improving_graph_contrastive_learning", "paper:shan2026_revisiting_positive_samples", "paper:yang2023_graph_contrastive_learning", "paper:li2026_aspect", "idea:srlp_gcl"]
target_gaps: ["gap:G2", "gap:G3", "gap:G4"]
added: 2026-06-22T01:49:39+08:00
---

# DCGCL: Disagreement-Calibrated Prototype Graph Contrastive Learning

## Status

READY FOR PILOT on paper. No GPU pilot has been run.

## Hypothesis

Node classification benefits more from task-related label-free prototype envelopes than from residual latent prediction. Agreement between a feature-only teacher and a propagation-view teacher provides reliable global positives, while disagreement indicates nodes where feature semantics and topology semantics should be preserved separately.

## Proposed Method

Maintain two weak teachers: one feature-only and one propagation-view. Each teacher assigns nodes to soft prototypes. High-confidence agreement nodes define global soft positive pairs. Disagreement nodes are trained through separate semantic and topology heads, then fused with a disagreement gate. The final encoder representation is evaluated with the existing linear node classification protocol.

## Fair Test

First run diagnostics on Cora, Chameleon, Texas, and Wisconsin split 0. Then run 5-epoch smoke and 200-epoch split-0 pilots against BGRL, FullLatent, ZPZ, and SRLP-Aux controls. Only expand to 10 Geom-GCN splits if split-0 results and ablations show a clear positive method effect.

## Closest Prior Work

- HEATS learns global adaptive positive matrices, but does not explicitly preserve feature/topology teacher disagreement.
- SPGCL analyzes positive pre-alignment under message passing, but solves it with Dirichlet-energy propagation and sampling rather than prototype disagreement.
- AFGRL/BGRL provide bootstrap and positive-pair infrastructure but lack prototype disagreement calibration.
- G-CENSOR, RGCL, and Community-Invariant GCL cover task-oriented views and invariance; DCGCL should be positioned as a label-free dual-teacher prototype target, not as a generic augmentation generator.

## Failure Notes

If feature/propagation teacher disagreement is not correlated with label difficulty or node classification error, kill this route before 10-split training. If single-teacher prototype contrast matches DCGCL, remove the dual-disagreement mechanism and downgrade the novelty claim.
