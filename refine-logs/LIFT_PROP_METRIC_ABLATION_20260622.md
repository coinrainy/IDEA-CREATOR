# LIFT-PROP Metric Ablation

**Date**: 2026-06-22 13:00  
**Milestone**: R074 first pass  
**Status**: `POSITIVE_DIAGNOSTIC`

## Question

Does edge-lift explain propagation gain better than simpler label-free graph
statistics?

We compare metrics against:

```text
gain_k2_vs_k0 = Acc(P^2X) - Acc(X)
```

across the current eight observed datasets/settings.

CSV:

```text
baselines/BGRL/runs/lift_prop_metric_ablation_20260622/metric_rows.csv
baselines/BGRL/runs/lift_prop_metric_ablation_20260622/correlation_summary.csv
```

## Correlation Summary

| Metric | Pearson with gain | Spearman with gain | Interpretation |
|---|---:|---:|---|
| `delta_lift_k2_k0` | 0.915337 | 0.880952 | strongest positive predictor |
| `delta_lift_k2_k1` | 0.755958 | 0.809524 | useful for K1/K2 selector |
| `k2_lift` | 0.809922 | 0.761905 | strong but less robust than delta lift |
| `k1_lift` | 0.829257 | 0.761905 | strong |
| `k0_lift` | 0.118289 | 0.142857 | raw lift alone is weak |
| `k2_edge_cos` | -0.789316 | -0.904762 | high edge cosine alone often indicates oversmoothing/raw damage |
| `k0_rand_cos` | -0.974058 | -0.970077 | high random-pair similarity is a strong negative signal |

## Interpretation

The useful signal is not edge cosine itself. WebKB/Cornell/Actor can have very
high propagated edge cosine, but propagation still hurts because random-pair
cosine also becomes high. Edge-lift and especially `lift(P^2X)-lift(X)` capture
the distinction between useful graph-aligned structure and global smoothing.

This supports LIFT-PROP's core claim more directly than the accuracy tables:
the selector is not an arbitrary threshold on graph smoothness; it measures
whether propagation increases edge-specific alignment beyond random-pair
alignment.

## Decision

R074 first pass is positive. The next version should:

- add confidence intervals via bootstrap over nodes or random pairs;
- compare against degree/density/effective-rank metrics;
- run the same correlation after full-grid Actor/Squirrel if feasible.
