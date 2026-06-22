# CCR-SAFE R096 Fresh-Split Validation

**Date**: 2026-06-22 18:10  
**Status**: `FAILED_FRESH_SPLIT_GATE`  
**Training code**: `baselines/BGRL/reproduce_ccr.py`  
**Safety code**: `baselines/BGRL/evaluate_ccr_safety.py`

## Purpose

R095 found a split-0 safety rule, `stack_moderate_residual`, that accepted the
Cora residual and rejected harmful CiteSeer/Chameleon/WebKB residuals. R096
freezes the same thresholds and tests fresh splits. Training uses
`--device=auto` and completed with `device=cuda`; final formal probes remain
CPU sklearn.

The planned queue was interrupted early after decisive fresh-split failure to
avoid wasting GPU/CPU time on a route that no longer satisfies the promotion
gate.

## Completed Fresh-Split Runs

| Dataset | Split | Portfolio | Concat | Old cert v1 | Stack moderate residual | Use residual? | Delta vs portfolio |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cora | 1 | 0.844024 | 0.832949 | 0.832949 | 0.832949 | 1 | -0.011075 |
| Cora | 2 | 0.854638 | 0.850023 | 0.850023 | 0.850023 | 1 | -0.004615 |
| CiteSeer | 1 | 0.732156 | 0.723140 | 0.723140 | 0.732156 | 0 | +0.000000 |

## Interpretation

The fixed safety rule does protect CiteSeer split 1 by rejecting a high
edge-cosine residual (`0.862810`). However, it accepts both fresh Cora residuals
because their residual edge cosine remains below the `0.8` threshold
(`0.774591`, `0.781985`), and both accepted residuals hurt accuracy.

This invalidates the R095 hope that the Cora split-0 residual complement is a
stable learned signal. The problem is not collapse: the residual effective rank
is high and training used CUDA. The problem is that the label-free safety
diagnostic cannot distinguish helpful from harmful Cora residuals across
splits.

## Decision

CCR-SAFE is downgraded to `FAILED_FRESH_SPLIT_GATE`. Do not run the remaining
CCR fresh-split queue or 10-split expansion. Keep the evaluator as a diagnostic
tool and preserve the result as evidence that residual complementarity must be
validated out-of-split before being treated as a method claim.

Next action: restart the main-method search with a different mechanism family,
or design a residual objective whose safety signal is causal/validated before
training rather than fitted post hoc from residual edge statistics.
