# LIFT Channel Gate R086 Results

**Date**: 2026-06-22  
**Status**: `FAILED_ROBUSTNESS_GATE`  
**Script**: `baselines/BGRL/evaluate_lift_channel_gate.py`  
**Raw CSVs**:
- `baselines/BGRL/runs/lift_channel_gate_split0_20260622/results.csv`
- `baselines/BGRL/runs/lift_channel_gate_hetero10_fast_20260622/results.csv`

## Question

After LIFT-Stack became the strongest control, R086 tested whether its high
dimensional fixed propagation stack could be improved by label-free channel
weights. Each feature channel receives an edge-lift score:

```text
score_j = mean_(i,k in E) z_ij z_kj - mean_(u,v random) z_uj z_vj
```

where `z` is a standardized channel. Variants use ReLU, sqrt, softplus, or
top-k weights. Channel gating is applied only when the global LIFT selector
chooses propagation; K0 raw-dominant graphs remain raw.

## Split-0 Gate

| Dataset | LIFT-Stack | Best Channel Gate | Best Variant | Delta | Decision |
|---|---:|---:|---|---:|---|
| Cora | 0.842640 | 0.841255 | relu | -0.001385 | fail |
| CiteSeer | 0.725770 | 0.719760 | sqrt | -0.006010 | fail |
| Chameleon | 0.668860 | 0.688596 | softplus | +0.019737 | local positive |
| Texas | 0.810811 | 0.810811 | K0 raw fallback | +0.000000 | protected |
| Wisconsin | 0.823529 | 0.823529 | K0 raw fallback | +0.000000 | protected |

The Chameleon split-0 signal is real, but it is not enough because the same
mechanism hurts both Cora and CiteSeer.

## Heterophily 10-Split Fast Grid

| Dataset | LIFT-Stack | Channel ReLU | Channel Softplus | Decision |
|---|---:|---:|---:|---|
| Chameleon | 0.662500 | 0.663377 | 0.661404 | neutral / not robust |
| Squirrel | 0.543708 | 0.525360 | 0.543420 | fail |
| Actor | 0.347566 | raw fallback | raw fallback | protected |
| Cornell | 0.786486 | raw fallback | raw fallback | protected |

The Chameleon split-0 improvement does not survive 10-split evaluation, and
Squirrel is damaged by ReLU channel gating.

## Decision

Do not promote LIFT Channel Gate. Channel-level edge-lift is too coarse: it can
identify a Chameleon-local denoising opportunity, but it does not reliably
improve propagation-positive graphs. Keep it as a diagnostic observation only.
Future candidates should avoid simple feature-channel pruning/weighting on
fixed propagation stacks unless paired with a stronger graph-level or node-level
reliability model.
