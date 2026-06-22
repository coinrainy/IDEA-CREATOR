# CCR-SAFE R095 Residual-Safety Diagnostic

**Date**: 2026-06-22 17:58  
**Status**: `PROMISING_DIAGNOSTIC_NOT_METHOD_READY`  
**Code**: `baselines/BGRL/evaluate_ccr_safety.py`  
**Input checkpoints**: `baselines/BGRL/runs/ccr_m1_split0_20260622/*/ccr_orth_var/split_0/bgrl-ccr.pt`

## Question

R093/R094 showed that a learned CCR residual branch has a real Cora complement
signal, but the first label-free certificate admitted harmful residuals on
CiteSeer, Chameleon, Texas, and Wisconsin. R095 tests whether simple label-free
safety policies can accept only residuals that look like a moderate complement
to the LIFT-Portfolio teacher.

Evaluation policy follows the project GPU rule: checkpoint forward passes,
projection/cosine diagnostics, and tensor reductions use CUDA when available;
the final formal node-classification probe remains CPU sklearn to preserve
comparability with previous tables.

## Policies

| Policy | Rule |
|---|---|
| `never_concat` | always use LIFT-Portfolio |
| `always_concat` | always concatenate LIFT-Portfolio with the CCR residual |
| `old_cert_v1` | use residual if residual edge-lift is high and teacher-anchor cosine is low |
| `raw_protect` | reject residual only when LIFT-Portfolio selected raw K0 |
| `portfolio_stack_only` | use residual only when LIFT-Portfolio selected stack |
| `stack_moderate_residual` | use residual only when portfolio selected stack, residual edge-lift `>=0.2`, and residual edge cosine `<=0.8` |

## Split-0 Results

| Dataset | Portfolio | Always concat | Old cert v1 | Stack moderate residual | Use residual? | Delta vs portfolio |
|---|---:|---:|---:|---:|---:|---:|
| Cora | 0.842640 | 0.851869 | 0.851869 | 0.851869 | 1 | +0.009229 |
| CiteSeer | 0.725770 | 0.713373 | 0.713373 | 0.725770 | 0 | +0.000000 |
| Chameleon | 0.699561 | 0.629386 | 0.629386 | 0.699561 | 0 | +0.000000 |
| Texas | 0.810811 | 0.783784 | 0.783784 | 0.810811 | 0 | +0.000000 |
| Wisconsin | 0.823529 | 0.803922 | 0.803922 | 0.823529 | 0 | +0.000000 |

## Diagnostic Interpretation

The old certificate fails because it accepts residuals that are graph-aligned
but not task-helpful. `raw_protect` fixes WebKB only; it still accepts the
harmful Chameleon and CiteSeer residuals. `portfolio_stack_only` rejects
Chameleon through the LIFT-Portfolio choice, but still accepts CiteSeer.

`stack_moderate_residual` is the first safety rule that improves Cora while
protecting all four other split-0 settings in this diagnostic batch. The
decisive extra filter is residual edge cosine: CiteSeer residual edge cosine is
too high (`0.868966`), suggesting over-smoothing or redundant graph alignment,
whereas Cora is moderate (`0.768316`).

## Decision

This is not paper-ready. The rule was derived after inspecting the same five
split-0 settings, so it may be overfit. However, it rescues the learned
residual direction from an outright stop: CCR should be reframed as a
label-free residual-safety problem rather than another residual-training run.

Next required check: train or reuse CCR checkpoints on fresh splits, then test
`stack_moderate_residual` without changing thresholds. A minimum useful gate is
Cora/CiteSeer/Chameleon splits 0-2, with Texas/Wisconsin kept as raw-protection
sentinels.
