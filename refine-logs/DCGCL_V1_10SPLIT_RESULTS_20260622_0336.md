# DCGCL V1 10-Split Internal Gate

**Date**: 2026-06-22  
**Method variant**: `dcgcl_v1`  
**Run dir**: `baselines/BGRL/runs/dcgcl_v1_10split_hetero_20260622_0325`  
**Scope**: Chameleon, Texas, Wisconsin; Geom-GCN official splits 0-9; 200 epochs; seed 0.

## Context

DCGCL V0 failed the first M2 gate. V1 revised the method from a shared prototype bank to separate feature/topology prototype banks with greedy prototype alignment and a high-confidence agreement mask. Split-0 was promising on Texas and Wisconsin, so V1 was expanded to a limited 10-split internal gate.

## Aggregate Results

Controls are the best target-family internal control per dataset/split from `srlp_aux_10split_target_family_20260621_221832`: FullLatent-Iso, ZPZ-Iso, and SRLP-Aux.

| Dataset | Rows | DCGCL mean | DCGCL std | Best-control mean | Delta | Wins/Ties/Losses | Valid mean | Positive active | Alignment | NaN | Collapse |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Chameleon | 10 | 0.40658 | 0.02055 | 0.50044 | -0.09386 | 0/0/10 | 0.42702 | 0.1272 | 0.8872 | 0 | 0 |
| Texas | 10 | 0.58649 | 0.07434 | 0.61351 | -0.02703 | 3/0/7 | 0.63898 | 0.0661 | 0.7644 | 0 | 0 |
| Wisconsin | 10 | 0.60392 | 0.05130 | 0.55490 | +0.04902 | 8/1/1 | 0.65625 | 0.0936 | 0.7521 | 0 | 0 |

## Per-Split Results

| Dataset | Split | DCGCL | Best control | Control mode | Delta |
|---|---:|---:|---:|---|---:|
| Chameleon | 0 | 0.41886 | 0.50658 | SRLP-Aux | -0.08772 |
| Chameleon | 1 | 0.42105 | 0.51974 | SRLP-Aux | -0.09868 |
| Chameleon | 2 | 0.42325 | 0.47368 | SRLP-Aux | -0.05044 |
| Chameleon | 3 | 0.42544 | 0.51316 | FullLatent-Iso | -0.08772 |
| Chameleon | 4 | 0.40351 | 0.54605 | FullLatent-Iso | -0.14254 |
| Chameleon | 5 | 0.40351 | 0.48465 | FullLatent-Iso | -0.08114 |
| Chameleon | 6 | 0.37500 | 0.47368 | ZPZ-Iso | -0.09868 |
| Chameleon | 7 | 0.36623 | 0.48465 | SRLP-Aux | -0.11842 |
| Chameleon | 8 | 0.41886 | 0.49342 | FullLatent-Iso | -0.07456 |
| Chameleon | 9 | 0.41009 | 0.50877 | SRLP-Aux | -0.09868 |
| Texas | 0 | 0.62162 | 0.64865 | FullLatent-Iso | -0.02703 |
| Texas | 1 | 0.59459 | 0.67568 | ZPZ-Iso | -0.08108 |
| Texas | 2 | 0.43243 | 0.48649 | FullLatent-Iso | -0.05405 |
| Texas | 3 | 0.64865 | 0.62162 | ZPZ-Iso | +0.02703 |
| Texas | 4 | 0.48649 | 0.59459 | FullLatent-Iso | -0.10811 |
| Texas | 5 | 0.62162 | 0.56757 | FullLatent-Iso | +0.05405 |
| Texas | 6 | 0.56757 | 0.59459 | ZPZ-Iso | -0.02703 |
| Texas | 7 | 0.62162 | 0.67568 | ZPZ-Iso | -0.05405 |
| Texas | 8 | 0.59459 | 0.62162 | FullLatent-Iso | -0.02703 |
| Texas | 9 | 0.67568 | 0.64865 | FullLatent-Iso | +0.02703 |
| Wisconsin | 0 | 0.66667 | 0.58824 | ZPZ-Iso | +0.07843 |
| Wisconsin | 1 | 0.62745 | 0.62745 | FullLatent-Iso | +0.00000 |
| Wisconsin | 2 | 0.60784 | 0.50980 | FullLatent-Iso | +0.09804 |
| Wisconsin | 3 | 0.54902 | 0.52941 | ZPZ-Iso | +0.01961 |
| Wisconsin | 4 | 0.54902 | 0.49020 | ZPZ-Iso | +0.05882 |
| Wisconsin | 5 | 0.68627 | 0.56863 | FullLatent-Iso | +0.11765 |
| Wisconsin | 6 | 0.64706 | 0.58824 | FullLatent-Iso | +0.05882 |
| Wisconsin | 7 | 0.58824 | 0.56863 | FullLatent-Iso | +0.01961 |
| Wisconsin | 8 | 0.56863 | 0.50980 | ZPZ-Iso | +0.05882 |
| Wisconsin | 9 | 0.54902 | 0.56863 | FullLatent-Iso | -0.01961 |

## Decision

DCGCL V1 fails as a main method. The Wisconsin result is real enough to keep as a diagnostic observation, but Chameleon fails on every split and Texas is negative overall. This is not a paper-level method signal and should not proceed to external strong baselines or paper writing.

DCGCL V2 with alignment-based BGRL fallback improved split-0 balance, but it has not passed 10-split validation and should not be treated as salvaging the method. The right next action is fresh idea discovery using the SRLP and DCGCL negative evidence as constraints.
