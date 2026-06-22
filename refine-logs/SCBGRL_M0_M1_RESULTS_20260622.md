# SC-BGRL M0-M1 Results

**Date**: 2026-06-22 10:42  
**Candidate**: SC-BGRL, Signed-Compatibility BGRL  
**Status**: `FAILED_FIXED_SIGN_PILOT`  

## Implementation

New files:

```text
baselines/BGRL/train_sc_transductive.py
baselines/BGRL/reproduce_sc.py
```

SC-BGRL uses a fixed sign heuristic: raw-feature endpoint cosine ranks edges
into top-half same-compatible and bottom-half different-compatible views, then
BGRL aligns the same node across these two signed structural views.

Important fix: the first implementation used a value threshold. On Chameleon,
many edge similarities were exactly zero, so the split collapsed and SC became
identical to the control. The final result below uses rank-based splitting,
which forces a real 50/50 same/different split.

## M0 Smoke

CSV:

```text
baselines/BGRL/runs/sc_m0_smoke_20260622/results.csv
baselines/BGRL/runs/sc_m0_smoke_rankfix_20260622/results.csv
```

Smoke passed with no NaN/collapse. Rank-fix Chameleon SC used
`same_edge_ratio=0.500014`, `diff_edge_ratio=0.499986`.

## M1 Split-0 Fair Pilot

CSV:

```text
baselines/BGRL/runs/sc_m1_split0_rankfix_20260622/results.csv
```

| Dataset | Control | SC | Delta | Decision |
|---|---:|---:|---:|---|
| Cora | 0.832487 | 0.828334 | -0.004153 | fail |
| Chameleon | 0.438596 | 0.436404 | -0.002193 | fail |
| Texas | 0.621622 | 0.621622 | +0.000000 | tie |
| Wisconsin | 0.549020 | 0.549020 | +0.000000 | tie |

No NaN/collapse occurred. The signed views are real after rank-fix, but they do
not improve the graph encoder.

## Decision

Stop fixed-sign SC-BGRL as a main route. A learned sign/sheaf version remains
possible in principle, but this cheap pilot gives no reason to spend a larger
implementation cycle now.

Next action: move to GDC-GCL+, the gradient-residual dynamics backup route.
