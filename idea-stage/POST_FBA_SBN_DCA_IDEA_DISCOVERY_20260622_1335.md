# Post-FBA Idea Discovery: SBN Negative, DCA Candidate

**Date**: 2026-06-22  
**Skill**: idea-discovery / research-pipeline  
**Status**: DCA selected as current empirical lead, novelty review pending

## Search Constraint

After FBA training failed, the next candidate needed to avoid:

- residual latent targets with weak label alignment;
- global prototype positives without robust activation rules;
- learned feature branches that forget raw signal;
- training-time filter alignment that destroys complementary anchor information.

## Candidate Tested and Stopped: SBN-GCL

SBN-GCL used semantic raw-feature kNN positives and low-similarity graph-edge boundary negatives. It was implemented in `baselines/BGRL/train_sbn_transductive.py`.

Split-0 result:

| Dataset | Graph | Fused | Raw | Verdict |
|---|---:|---:|---:|---|
| Cora | 0.814490 | 0.820951 | 0.659437 | weak local positive |
| Chameleon | 0.394737 | 0.462719 | 0.440789 | fail |
| Texas | 0.621622 | 0.729730 | 0.810811 | fail |
| Wisconsin | 0.686275 | 0.784314 | 0.823529 | fail |

Verdict: stop SBN.

## Current Candidate: DCA-GCL

DCA-GCL keeps filter anchors out of the training objective and fuses them only at representation time:

```text
z_dca = normalize([z_graph || X || 0.5(X-PX) || P^4X])
```

Chameleon 10-split:

| Representation | Mean Test | Std |
|---|---:|---:|
| graph_raw | 0.496711 | 0.022175 |
| fba_h1 | 0.500219 | 0.020769 |
| fba_p4 | 0.500219 | 0.018697 |
| dca_h1_p4 | 0.505044 | 0.022791 |
| dca_h1_h4_p4 | 0.505044 | 0.019908 |

Cora/CiteSeer are positive over graph_raw; Texas/Wisconsin remain raw-dominant.

## Decision

DCA-GCL becomes the current candidate for method review, not for immediate main-table expansion. The next gate must check novelty against ASPECT, FC-GSSL, SPGCL, Less is More, HLCL/GREET/SIGNA, and simple graph-feature fusion baselines.

