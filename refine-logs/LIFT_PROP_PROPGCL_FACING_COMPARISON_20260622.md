# LIFT-PROP PROPGCL-Facing Comparison

**Date**: 2026-06-22 13:15  
**Milestone**: R076 first pass  
**Status**: `POSITIVE_FIRST_PASS`, not a full PROPGCL main-method comparison

## Prior Boundary

PROPGCL establishes PROP as a strong training-free GCL baseline:

```text
H_PROP = A_hat^K X
```

It also introduces PROPGCL, which learns graph-adaptive polynomial propagation
coefficients:

```text
H_PROPGCL = sum_k theta_k g_k(L) X
```

The PROPGCL appendix reports that the best PROP step varies by dataset: K=1
for Cora, CiteSeer, Chameleon, Squirrel, Computers, and Photo; K=0 for Texas,
Wisconsin, Cornell, Actor, and CS.

Therefore LIFT-PROP's defensible comparison is not "we invented propagation".
The fair first-pass question is:

> Can LIFT-PROP select raw/propagation depth without validation labels better
> than simple fixed-K, max-lift, first-threshold, or PROPGCL reported-step
> heuristics?

## Inputs

CSV:

```text
baselines/BGRL/runs/lift_prop_propgcl_facing_20260622/selector_comparison.csv
baselines/BGRL/runs/lift_prop_propgcl_facing_20260622/selector_aggregate.csv
```

Selector definitions:

- `lift_prop_v1`: if `lift(P2X)<0.35`, K=0; else if
  `lift(P2X)<=lift(PX)+0.02`, K=1; else K=2.
- `propgcl_reported_step`: K=1 for Cora/CiteSeer/Chameleon/Squirrel, K=0 for
  Texas/Wisconsin/Cornell/Actor, following PROPGCL Appendix E's qualitative
  best-step statement.
- `first_lift_threshold`: first K>0 whose lift exceeds `0.35`, else K=0.
- `max_lift`: K with maximum lift among K=0..3.
- `validation_selected`: K with best validation accuracy in the current sweep.
- `oracle`: K with best test accuracy in the current sweep.

## Aggregate Results

| Selector | Mean selected test | Mean oracle gap | Exact oracle hits | Within 0.02 of oracle |
|---|---:|---:|---:|---:|
| validation-selected | 0.697964 | 0.000000 | 8/8 | 8/8 |
| oracle | 0.697964 | 0.000000 | 8/8 | 8/8 |
| LIFT-PROP v1 | 0.696868 | 0.001096 | 7/8 | 8/8 |
| PROPGCL reported-step heuristic | 0.686911 | 0.011052 | 5/8 | 6/8 |
| first-threshold | 0.686911 | 0.011052 | 5/8 | 6/8 |
| fixed K0 raw | 0.623593 | 0.074370 | 4/8 | 4/8 |
| fixed K2 PROP | 0.602119 | 0.095845 | 2/8 | 4/8 |
| fixed K1 PROP | 0.579870 | 0.118093 | 1/8 | 2/8 |
| max-lift | 0.586202 | 0.111762 | 2/8 | 3/8 |

## Where LIFT-PROP Improves Over PROPGCL Reported-Step Heuristic

| Dataset | LIFT-PROP K / test | PROPGCL heuristic K / test | Difference |
|---|---:|---:|---:|
| Cora | K2 / 0.826488 | K1 / 0.803876 | +0.022612 |
| CiteSeer | K2 / 0.709617 | K1 / 0.697971 | +0.011645 |
| Chameleon | K2 / 0.685746 | K1 / 0.640351 | +0.045395 |
| Squirrel | K1 / 0.520365 | K1 / 0.520365 | +0.000000 |
| Texas | K0 / 0.829730 | K0 / 0.829730 | +0.000000 |
| Wisconsin | K0 / 0.839216 | K0 / 0.839216 | +0.000000 |
| Cornell | K0 / 0.816216 | K0 / 0.816216 | +0.000000 |
| Actor | K0 / 0.347566 | K0 / 0.347566 | +0.000000 |

## Interpretation

This result gives LIFT-PROP a concrete delta against the closest PROP-style
prior:

- PROPGCL already observes that propagation depth matters.
- LIFT-PROP adds a zero-label selector that adapts the step in the current
  protocol and improves over the paper-reported K0/K1 heuristic.
- The largest advantage comes from Chameleon and Cora, where K2 is better than
  the PROPGCL reported K1 heuristic under the current split/evaluation setup.

This is still not a full comparison against learned PROPGCL (`PROP-GRACE` or
`PROP-DGI`). Learned propagation coefficients remain a stronger prior. The
current evidence supports LIFT-PROP as a label-free selector and reliability
gate, not as a superior learned GCL model.

## Decision

R076 first pass is positive. LIFT-PROP remains active, but the next step must
address one of:

1. reproduce or approximate learned PROPGCL coefficients;
2. show that LIFT-PROP can be plugged into PROP-GRACE/PROP-DGI as an abstention
   gate;
3. position LIFT-PROP as a training-free reliability selector, with PROPGCL as
   the learnable upper-neighbor rather than the direct baseline to beat.
