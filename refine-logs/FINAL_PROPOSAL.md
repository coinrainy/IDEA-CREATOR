# Current Proposal Status: No Ready Proposal After RSP Gate

**Date**: 2026-06-22  
**Status**: `NO_READY_METHOD`; RSP-GCL is `DIAGNOSTIC_ONLY_AFTER_GATE`  
**Candidate**: RSP-GCL, Role-Signature Positive Graph Contrastive Learning  

## Gate Outcome

RSP-GCL should not be refined into a paper proposal in its current form.

| Gate | Result | Decision |
|---|---:|---|
| Chameleon 10-split RSP training | role-fused `0.573684 +/- 0.026265` | conditional positive |
| Chameleon validation-selected gate | `0.574781 +/- 0.023321`, role selected 10/10 | positive |
| Texas validation-selected gate | `0.827027` vs raw `0.829730` | no gain |
| Wisconsin validation-selected gate | `0.827451` vs raw `0.839216` | no gain |
| Novelty check | GALE/WLGCL/SPGCL overlap | fail for main claim |

RSP remains useful as a diagnostic role-signature baseline, especially for
Chameleon-like graphs. It is not the final graph contrastive learning method.

## Problem Anchor

Current graph contrastive learning methods often fail on heterophilic node classification because they assume one of a few crowded mechanisms:

- adjacent nodes or raw-feature kNN nodes are useful positives;
- low/high spectral channels can be mixed into a robust representation;
- prototypes or latent residual targets capture task-relevant identity;
- edge perturbation or transport can repair local neighborhoods.

These routes either failed in this workspace or are too close to recent literature. The new anchor is narrower:

> Some heterophilic graphs, especially Chameleon in the current evidence, are better explained by nonlocal structural role equivalence than by raw-feature similarity, adjacency, or spectral low/high mixing.

## Method Thesis

RSP-GCL builds a role signature for each node from:

1. local structural statistics;
2. WL-hash neighborhood patterns;
3. landmark diffusion responses.

The role signature defines nonlocal positive samples for a BGRL-style graph encoder:

```text
S_i = normalize([role_stats_i || wl_hash_i || landmark_diffusion_i])
P_i = top-k nodes under cosine(S_i, S_j)
L_role_nce = - sum_j P_ij log softmax(q_i^T z_j / tau)
L_role_anchor = 1 - cos(g(z_i), S_i)
L = lambda_bgrl L_BGRL + lambda_role_nce L_role_nce + lambda_role_anchor L_role_anchor
```

The downstream representation is:

```text
h_i = [z_i^graph || x_i^raw || gate_i * S_i^role]
```

The gate is mandatory. Current evidence says `gate=1` is good for Chameleon and bad for Texas/Wisconsin.

## Evidence

| Evidence | Result | Interpretation |
|---|---:|---|
| Chameleon 10-split proxy, `graph_raw_role_wl_landmark` | 0.585965 | strong positive over graph_raw and DCA |
| Chameleon 10-split proxy, `graph_raw` | 0.496711 | baseline |
| Chameleon 10-split DCA best | 0.505044 | previous best lead |
| Chameleon RSP train split-0, role-fused | 0.596491 | training prototype preserves signal |
| Texas 10-split full role proxy | 0.678378 vs raw 0.829730 | role branch hurts |
| Wisconsin 10-split full role proxy | 0.719608 vs raw 0.839216 | role branch hurts |

## Novelty Boundary

Close works include ASPECT, PROPGCL, H3GNNs/HarmonyGNNs, Str-GCL, CoRep, HLCL, and Less is More. RSP-GCL should not claim broad firstness. Its defensible claim is:

> A compact role/WL/landmark signature can define nonlocal role-equivalent positives for graph contrastive learning, producing a large gain on role-structured heterophily when gated away on raw-dominant graphs.

## Decision

The promotion gate failed. Restart idea discovery with a different mechanism
family. Future candidates should avoid generic node-equivalence/WL-positive
claims and avoid relying only on concatenated handcrafted structural signatures.
