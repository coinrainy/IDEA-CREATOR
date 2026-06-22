# Post-DCA Idea Discovery

**Date**: 2026-06-22  
**Goal**: continue toward a graph contrastive learning method for node classification with enough empirical effect and 2026-level novelty.

## Starting Point

DCA-GCL produced the strongest current local signal, but novelty collapsed against recent and close prior work. It is now a diagnostic/simple baseline, not the active paper method.

Additional quick probes:

- Semantic kNN anchor (`S X`, `X-SX`) gave small Cora/CiteSeer gains but no decisive Chameleon/Texas/Wisconsin improvement.
- ZCA/whitening was too slow in this loop and is not cleanly novel because GCL-GroW/GWGCL already cover whitening GCL.

## Updated Banlist

Do not spend another main-method cycle on:

1. fixed raw/graph/filter concatenation;
2. node-level low/high spectral fusion;
3. prototype-positive routing;
4. residual latent prediction;
5. feature-channel preservation alone;
6. semantic kNN positives plus low-similarity edge negatives;
7. generic whitening/uniformity objectives.

## Candidate Portfolio

| Rank | Candidate | Mechanism | Novelty Risk | Cheap Test | Status |
|---:|---|---|---|---|---|
| 1 | VST-GCL: Variance-Stabilized Transport GCL | Build local transport plans between topology-neighborhood mass and raw-feature semantic mass; train the graph encoder toward transported teacher barycenters while downweighting unstable mass. | MEDIUM: close to GCL-OT/GALOPA, but different setting if no text/LLM and local feature-topology transport is used. | Implement a top-k Sinkhorn/soft-transport target on Cora/Chameleon/Texas/Wisconsin split 0. | SPECULATIVE_INCUBATE |
| 2 | CIG-GCL: Counterfactual Influence-Gated GCL | Estimate whether an edge helps or hurts teacher consistency under edge dropout, then use helpful and harmful edges as separate contrastive environments. | MEDIUM-HIGH: close to adaptive augmentation, but dynamic influence gating may be defensible. | Add edge-influence diagnostics first; train only if influence correlates with graph_raw errors. | SPECULATIVE |
| 3 | LER-GCL: Label-free Error-Risk Routed GCL | Use disagreement among raw, graph, and filter probes without labels to route nodes into raw-preserve, graph-smooth, or residual-preserve objectives. | HIGH: close to ASPECT/routing and previous failed gates. | Only worthwhile if a label-free diagnostic predicts raw-dominant vs graph-helpful regimes before training. | HOLD |
| 4 | DCA/AnchorBank baseline | Frozen raw/low/high/DCA candidate family with validation or label-free selection. | LOW: useful baseline, not a method paper. | Already has enough evidence. | DIAGNOSTIC_ONLY |

## Recommended Next Step

Run the cheap VST-GCL proxy only if the implementation can stay small:

1. use raw-feature top-k semantic neighbors and graph one-hop/two-hop candidates;
2. compute a local soft transport plan or normalized overlap weights, not a global dense OT matrix;
3. train BGRL with an extra transported-teacher barycenter loss;
4. first gate: Cora/Chameleon/Texas/Wisconsin split 0, 200 epochs;
5. kill immediately if it does not beat graph_raw/DCA on Chameleon and raw on Texas/Wisconsin is still untouched.

Do not run external baselines until a new candidate has a fair local positive signal and novelty survives a focused check.

