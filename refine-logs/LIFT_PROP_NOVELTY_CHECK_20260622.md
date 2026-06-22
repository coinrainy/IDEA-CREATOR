# LIFT-PROP-GCL Novelty Check

**Date**: 2026-06-22 12:05  
**Method**: LIFT-PROP-GCL, label-free edge-lift gated propagation  
**Verdict**: `PROCEED_WITH_CAUTION`  
**Novelty score**: `5.5 / 10`  
**External reviewer**: attempted via `mcp__claude_review.review`, failed with 403 insufficient quota; trace saved under `.aris/traces/novelty-check/2026-06-22_run01/`.

## Proposed Method

LIFT-PROP-GCL computes a label-free reliability score for graph propagation:

```text
lift(P^2X) = mean_cos_edges(P^2X) - mean_cos_random_pairs(P^2X)
```

If `lift(P^2X) >= 0.35`, it uses `P^2X`; otherwise it abstains from graph
propagation and keeps raw `X`. This protects raw-dominant graphs while
preserving strong propagation gains on graphs where propagation is reliable.

## Core Claims

1. **Propagation reliability can be decided without labels.**  
   Novelty: `MEDIUM`. Closest: GNNEvaluator, When Do GNNs Help, GLANCE.

2. **A simple edge-vs-random cosine lift can route raw vs `P^2X`.**  
   Novelty: `MEDIUM-HIGH` as a specific metric; not found as an exact method in
   searched papers, but conceptually close to feature homophily and graph-help
   predictors.

3. **The route is useful for GCL because it turns PROPGCL-style propagation into
   a reliability-aware mechanism.**  
   Novelty: `LOW-MEDIUM`. PROPGCL already establishes propagation as a strong
   GCL baseline and discusses depth; LIFT-PROP's delta is abstention and a
   label-free gate, not propagation itself.

4. **Feature-token graph views are not the contribution.**  
   Novelty: `LOW`. GRAPHITE directly covers feature-node graph transformation
   for heterophily, so feature-token propagation should be diagnostic only.

## Closest Prior Work

| Paper | Year | Venue / status | Overlap | Key difference |
|---|---:|---|---|---|
| PROPGCL: Unleashing the Power of Propagation in GCL | 2025/2026 | ICLR 2026 submission | Establishes training-free PROP as competitive with GCL and discusses propagation depth. | LIFT-PROP adds a label-free abstention gate for raw vs `P^2X`, especially to avoid WebKB damage. |
| When Do Graph Neural Networks Help with Node Classification? | 2023 | NeurIPS | Studies when graph-aware models help beyond homophily; proposes feature-based performance metrics. | LIFT-PROP is a much simpler unsupervised edge-lift gate tied to deterministic propagation views. |
| GNNEvaluator | 2023 | NeurIPS | Estimates GNN performance without labels. | GNNEvaluator trains an evaluator over graph discrepancies; LIFT-PROP uses no learned evaluator. |
| GLANCE | 2025 | arXiv | Uses label-free homophily estimates for routing. | GLANCE routes LLM vs GNN assistance with trained routing features, not propagation depth/raw abstention in GCL. |
| Less is More | 2025/2026 | ICLR 2026 withdrawn | Simple graph/raw dual-view GCL for heterophily. | LIFT-PROP does not train dual encoders; it gates whether graph propagation should be used at all. |
| ASPECT | 2026 | arXiv | Adaptive low/high spectral fusion for GCL. | LIFT-PROP is not node-level spectral fusion; it is a graph-level raw-vs-propagation abstention gate. |
| GRAPHITE | 2026 | ICLR | Feature-node graph transformation to improve homophily. | Feature-token views are explicitly not the main claim for LIFT-PROP. |
| HLCL | 2024 | UAI | Feature-cosine subgraphs plus low/high-pass contrastive filters for heterophily. | LIFT-PROP avoids subgraph construction and filtering; it only decides whether propagation is reliable. |

## Assessment

LIFT-PROP is **not high novelty** if framed as "we use propagation for graph
contrastive learning"; PROPGCL already owns that space. It is also not enough
to claim "we use feature nodes"; GRAPHITE owns that boundary.

The defensible claim is narrower:

> A zero-label edge-lift statistic can predict when deterministic propagation
> should be enabled or abstained from, selecting the oracle raw-vs-`P^2X` choice
> on 4/5 pilot datasets and solving the historical Chameleon/WebKB tradeoff.

This is a plausible workshop or main-track idea only if strengthened. As-is, it
is a strong baseline finding and a promising reliability-gate component, not a
complete paper-level method.

## Minimum Strengthening Required

1. **Compare directly to PROPGCL.**  
   LIFT-PROP must beat or complement PROPGCL's validation-selected propagation
   depth and any graph-adaptive filter variant. If PROPGCL already has an
   unsupervised depth rule or raw abstention, abandon LIFT-PROP as a main claim.

2. **Expand datasets.**  
   Run Cornell, Actor, Squirrel, PubMed/Amazon/Coauthor if available. The fixed
   threshold `0.35` must not be tuned on Chameleon/WebKB only.

3. **Prove or empirically support the metric.**  
   Show that edge-lift correlates with downstream gain `Acc(P^2X)-Acc(X)` and
   with a contrastive objective alignment term better than raw feature
   homophily, degree, density, rank, or validation-free smoothness.

4. **Turn it into a GCL method, not only a deterministic evaluator.**  
   Options:
   - use the gate to decide whether a BGRL/PROP contrastive objective should
     align to propagation targets or abstain;
   - use edge-lift as a node/cluster-level reliability weight;
   - frame propagation as implicit GCL and provide a precise objective-level
     connection to PROPGCL.

5. **Report raw protection as a first-class criterion.**  
   Texas/Wisconsin must remain at raw-level performance; any method variant
   that lowers them repeats the earlier failure pattern.

## Recommendation

`PROCEED_WITH_CAUTION`.

Do not enter full paper-writing or large external baseline expansion yet. The
next justified step is a compact method refinement plus a direct PROPGCL-facing
experiment plan. If novelty against PROPGCL collapses, downgrade LIFT-PROP to a
required baseline and restart idea discovery.
