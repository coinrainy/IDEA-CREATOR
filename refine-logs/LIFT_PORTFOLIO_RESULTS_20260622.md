# LIFT-Portfolio R088 Results

**Date**: 2026-06-22  
**Status**: `STRONG_BASELINE_LOW_NOVELTY`  
**Script**: `baselines/BGRL/evaluate_lift_portfolio.py`  
**Raw CSVs**:
- `baselines/BGRL/runs/lift_portfolio_homo10_20260622/results.csv`
- `baselines/BGRL/runs/lift_portfolio_hetero10_fast_20260622/results.csv`
- `baselines/BGRL/runs/lift_portfolio_chameleon10_fullgrid_20260622/results.csv`
- `baselines/BGRL/runs/lift_stack_chameleon_split0_fullgrid_check_20260622/results.csv`

## Motivation

R088 audits a C-grid mismatch: Chameleon split-0 under full linear-eval C-grid
has `P2X/global LIFT = 0.699561`, while `LIFT-Stack 0123 = 0.668860`. The
earlier LIFT-Stack result used a fast C-grid for heterophily, which understated
the single-depth P2 baseline on Chameleon.

This means the strongest fixed-propagation control is not plain LIFT-Stack, but
a small portfolio:

```text
if global LIFT selects K0:
    use raw X
elif global LIFT selects K2 and lift(X) < 0.05:
    use single P2X
else:
    use concat(normalize(X), normalize(PX), normalize(P2X), normalize(P3X))
```

Intuition: if raw features have almost no edge-lift, concatenating raw/PX/P3
with P2 can inject noise; use the selected single propagation depth. If raw
features retain meaningful edge-lift, the stack helps.

## Results

| Dataset / protocol | Global LIFT | LIFT-Stack 0123 | LIFT-Portfolio | Portfolio choice |
|---|---:|---:|---:|---|
| Cora, 10 random splits full grid | 0.830042 | 0.848869 | 0.848869 | stack_0123 |
| CiteSeer, 10 random splits full grid | 0.701202 | 0.726972 | 0.726972 | stack_0123 |
| Chameleon, 10 official splits full grid | 0.685746 | 0.671053 | 0.685746 | single_k2_low_raw_lift |
| Squirrel, 10 official splits fast grid | 0.520365 | 0.543708 | 0.543708 | stack_0123 |
| Texas, 10 official splits fast grid | 0.805405 | 0.805405 | 0.805405 | raw_k0 |
| Wisconsin, 10 official splits fast grid | 0.841176 | 0.841176 | 0.841176 | raw_k0 |
| Cornell, 10 official splits fast grid | 0.786486 | 0.786486 | 0.786486 | raw_k0 |
| Actor, 10 official splits fast grid | 0.347566 | 0.347566 | 0.347566 | raw_k0 |

## Decision

LIFT-Portfolio replaces plain LIFT-Stack as the strongest current
training-free control. It fixes the Chameleon full-grid issue while retaining
the Cora/CiteSeer/Squirrel stack gains and raw protection on WebKB/Actor/Cornell.

This is still not the final requested GCL method. It remains in the
fixed-propagation / selector family with high novelty risk against SIGN, SGC,
FAF, PROPGCL, GLANCE-style label-free routing, and graph usefulness estimators.
Use it as the required baseline for the next mechanism-family restart.
