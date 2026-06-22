# GDC-GCL+ M0-M1 Results

**Date**: 2026-06-22 10:55  
**Candidate**: GDC-GCL+, Gradient-Residual Dynamics GCL  
**Status**: `FAILED_SPLIT0_GATE`, not `READY_TO_REFINE`

## Implementation

New files:

```text
baselines/BGRL/train_gdc_transductive.py
baselines/BGRL/reproduce_gdc.py
```

The trainer keeps the ordinary BGRL bootstrap objective and adds a dynamics
InfoNCE term after warmup. Three modes are supported:

- `bgrl_control`: ordinary BGRL under the same runner;
- `td_direction`: dynamic positives from EMA embedding update direction;
- `gdc_residual`: gradient direction after removing current-embedding and
  frozen raw-feature-anchor projections.

Verification:

```text
python -m py_compile train_gdc_transductive.py reproduce_gdc.py
python reproduce_gdc.py --datasets cora,chameleon --variants gdc_residual --splits 0 --epochs 5 --eval_epochs 5 --dyn_warmup_epochs 2 --output_dir runs/gdc_m0_smoke_20260622 --clean
```

Both passed. No NaN/collapse was observed.

## M0 Smoke

CSV:

```text
baselines/BGRL/runs/gdc_m0_smoke_20260622/results.csv
```

| Dataset | Variant | Epochs | Test@Best | Direction norm | Effective rank | NaN | Collapse |
|---|---|---:|---:|---:|---:|---:|---:|
| Cora | GDC residual | 5 | 0.772497 | 0.100884 | 207.307404 | 0 | 0 |
| Chameleon | GDC residual | 5 | 0.396930 | 0.125822 | 183.776596 | 0 | 0 |

## M1 Split-0 Main Pilot

CSV:

```text
baselines/BGRL/runs/gdc_m1_split0_20260622/results.csv
baselines/BGRL/runs/gdc_m1_td_direction_20260622/results.csv
```

| Dataset | BGRL control | TD direction | GDC residual | Best delta vs control | Decision |
|---|---:|---:|---:|---:|---|
| Cora | 0.833410 | 0.830180 | 0.830641 | -0.002769 | fail |
| CiteSeer | 0.693464 | 0.694591 | 0.691210 | +0.001127 | too small / TD only |
| Chameleon | 0.438596 | 0.438596 | 0.442982 | +0.004386 | weak |
| Texas | 0.621622 | - | 0.621622 | +0.000000 | tie |
| Wisconsin | 0.549020 | - | 0.549020 | +0.000000 | tie |

Diagnostics remained stable: GDC residual effective rank stayed high
(`70.93`-`211.75` across datasets), and all `nan_flag` / `collapse_flag`
values were zero. However, the gradient-residual dynamics term did not create
a useful method effect. It was below BGRL on Cora/CiteSeer, only weakly
positive on Chameleon, and inert on WebKB.

## Decision

Stop GDC-GCL+ as a main route:

- engineering is stable;
- residual gradient directions are measurable and non-collapsed;
- split-0 accuracy does not support promotion;
- the TD-style comparison also fails to reproduce the earlier TD-GCL strength
  under this runner and lower `lambda_dyn`;
- the broader dynamics-positive family remains novelty-risky and empirically
  fragile.

Next action: restart wide idea discovery with a different mechanism family.
Avoid local variations of dynamic positives, positive-gain weighting, fixed
signed views, role/WL positives, filter anchors, and raw-retention baselines
unless they are used only as diagnostics.
