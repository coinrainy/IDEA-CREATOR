# LIFT Low-Rank Bottleneck R099 Results

**Date**: 2026-06-22 18:44  
**Status**: `FAILED_PROXY_GATE`  
**Code**: `baselines/BGRL/evaluate_lift_lowrank.py`  
**Related prior risk**: Low-Rank Graph Contrastive Learning / GCL-LRR.

## Question

R099 tested whether the very high-dimensional LIFT-Portfolio representation can
be improved by label-free low-rank denoising before any learned low-rank GCL
objective is implemented.

The evaluator applies randomized SVD to the normalized/centered
LIFT-Portfolio representation and tests both scaled low-rank coordinates and
whitened coordinates. Final node-classification probes use the canonical CPU
sklearn protocol.

## Split-0 Results

The run was stopped after Chameleon rank 128 because the proxy had already
failed.

| Dataset | Portfolio | Best low-rank tested | Result | Delta | Decision |
|---|---:|---|---:|---:|---|
| Cora | 0.842640 | `lowrank_1024` | 0.842178 | -0.000461 | no gain |
| CiteSeer | 0.725770 | `lowrank_32` | 0.731781 | +0.006011 | local gain |
| Chameleon | 0.699561 | `lowrank_128` | 0.651316 | -0.048246 | decisive fail |

## Interpretation

Low-rank compression helps CiteSeer at small rank, likely by reducing
high-dimensional stack overfitting. It does not improve Cora and it severely
damages Chameleon, where LIFT-Portfolio correctly uses single `P2X`.

Whitened low-rank coordinates are broadly harmful, especially at larger ranks.
This suggests the useful signal is not a general low-rank contrastive
bottleneck but a dataset-specific classifier regularization effect.

The novelty case is also weak because low-rank GCL/LRR already exists as a
nearby graph contrastive learning direction.

## Decision

Do not implement a learned low-rank GCL objective or run 10-split expansion
from this proxy. Low-rank compression may remain a diagnostic for CiteSeer
overfitting, but it is not a paper-level main route.
