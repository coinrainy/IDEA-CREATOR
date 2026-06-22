# LIFT-PROP-GCL Selector v1 Results

**Date**: 2026-06-22 12:45  
**Status**: `METHOD_V1_ACTIVE`, still `PROCEED_WITH_CAUTION`

## Selector v1

The fixed K2 gate was revised after Squirrel fast-grid 10-split preferred K1.
The v1 selector is:

```text
if lift(P^2X) < 0.35:
    select K = 0
else if lift(P^2X) <= lift(PX) + 0.02:
    select K = 1
else:
    select K = 2
```

Interpretation:

- `lift(P^2X) < 0.35` means propagation is not reliable enough; preserve raw.
- If K2 lift does not improve over K1 by at least `0.02`, propagation has
  plateaued; use the shallower K1.
- Otherwise use K2.

## Validation

CSV:

```text
baselines/BGRL/runs/lift_prop_actor_squirrel10_fast_k12_20260622/results.csv
baselines/BGRL/runs/lift_prop_actor_squirrel10_fast_k12_20260622/selected_summary.csv
baselines/BGRL/runs/lift_prop_selector_v1_summary_20260622/selected_summary.csv
```

| Dataset | Protocol | Selected K | Selected test | Oracle K | Oracle test | Decision |
|---|---|---:|---:|---:|---:|---|
| Actor | 10 splits, fast C-grid `-4,0,4` | 0 | 0.347566 | 0 | 0.347566 | hit |
| Squirrel | 10 splits, fast C-grid `-4,0,4` | 1 | 0.520365 | 1 | 0.520365 | hit |

Using existing K-sweep results, v1 would choose:

| Dataset | Selector v1 K | Oracle K | Notes |
|---|---:|---:|---|
| Cora | 2 | 3 | near miss; K2 `0.826488`, K3 `0.835256` |
| CiteSeer | 2 | 2 | hit |
| Chameleon | 2 | 2 | hit |
| Texas | 0 | 0 | hit |
| Wisconsin | 0 | 0 | hit |
| Cornell | 0 | 0 | hit |
| Actor | 0 | 0 | hit |
| Squirrel | 1 | 1 | hit under fast-grid 10-split |

Selector v1 matches the observed oracle on 7/8 datasets/settings, with Cora as
the only near miss.

The aggregate selector summary also compares v1 against validation-selected K
from the same K-sweep results. Selector v1 matches validation-selected K on
7/8 settings, again with only Cora differing by `0.008768` absolute accuracy.

## Decision

LIFT-PROP-GCL now has a concrete method form rather than only a K2 proxy. It
still needs:

1. Full-grid Actor/Squirrel 10-split confirmation if runtime can be optimized.
2. Direct comparison to validation-selected K and PROPGCL-style propagation.
3. A theory/diagnostic section showing why edge-lift predicts propagation gain.
4. A decision on whether to frame the contribution as a training-free
   propagation-contrastive method or as a reliability gate for GCL objectives.
