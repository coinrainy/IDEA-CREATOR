# LIFT-PROP-GCL M0 Results

**Date**: 2026-06-22 11:45  
**Candidate**: LIFT-PROP-GCL, Label-free edge-LIFT gated propagation for graph contrastive learning  
**Status**: `ACTIVE_WITH_NOVELTY_RISK`, not yet paper-ready  

## Motivation

After NPG-GCL, fixed-sign SC-BGRL, and GDC-GCL+ failed, a deterministic
propagation proxy revealed a stronger and cleaner problem: graph propagation is
very useful on Cora/CiteSeer/Chameleon, but actively harmful on Texas/Wisconsin.
This is not another positive-mining problem. It is a reliability-routing
problem: decide, without labels, whether to use a graph-propagated view or keep
the raw feature view.

Closest literature boundary:

- PROPGCL already shows that simple propagation can be a strong graph
  contrastive learning baseline.
- GRAPHITE already covers feature-token graph construction, so feature-token
  views are diagnostic only here.
- Less is More and ASPECT cover graph/raw dual views and spectral/adaptive
  propagation-style routes.

The tentative delta is the label-free reliability gate: use edge-vs-random
cosine lift of `P^2 X` to decide whether propagation should be enabled at all.

## Implementation

New files:

```text
baselines/BGRL/evaluate_factor_token_proxy.py
baselines/BGRL/evaluate_lift_prop.py
```

`evaluate_factor_token_proxy.py` tests raw, original-graph propagation, and
feature-token propagation proxies.

`evaluate_lift_prop.py` sweeps `K=0..3` deterministic propagation views and
computes a label-free reliability score:

```text
lift(P^K X) = mean_cos_edges(P^K X) - mean_cos_random_pairs(P^K X)
```

The current gate is:

```text
if lift(P^2 X) >= 0.35: use P^2 X
else: use raw X
```

This gate uses no labels and no validation accuracy.

## M0 Factor-Token Proxy

CSV:

```text
baselines/BGRL/runs/factor_token_hetero10_core_20260622/results.csv
baselines/BGRL/runs/factor_token_homo_split0_core_20260622/results.csv
```

| Dataset | Raw | `P^2 X` graph | Feature-token graph | Decision |
|---|---:|---:|---:|---|
| Cora split-0 | 0.694509 | 0.825565 | 0.828334 | graph/feature graph useful |
| CiteSeer split-0 | 0.676183 | 0.709617 | 0.711495 | graph/feature graph useful |
| Chameleon 10-split | 0.456798 +/- 0.018724 | 0.685526 +/- 0.021292 | 0.601096 +/- 0.013257 | `P^2 X` dominates |
| Texas 10-split | 0.829730 +/- 0.051042 | 0.583784 +/- 0.046289 | 0.759459 +/- 0.039166 | raw dominates |
| Wisconsin 10-split | 0.839216 +/- 0.043157 | 0.619608 +/- 0.064834 | 0.800000 +/- 0.056072 | raw dominates |

Feature-token propagation is useful but not the lead. It is weaker than
`P^2 X` on Chameleon and weaker than raw on WebKB. Given GRAPHITE overlap, it
should remain a diagnostic component.

## M0 Lift-Gate Sweep

CSV:

```text
baselines/BGRL/runs/lift_prop_k03_20260622/results.csv
```

| Dataset | K=0 test | K=1 test | K=2 test | K=3 test | `lift(P^2X)` | K2-gate choice | K2-gate test | Oracle K |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Cora split-0 | 0.694509 | 0.803876 | 0.826488 | 0.835256 | 0.585357 | 2 | 0.826488 | 3 |
| CiteSeer split-0 | 0.676183 | 0.697971 | 0.709617 | 0.688956 | 0.701554 | 2 | 0.709617 | 2 |
| Chameleon 10-split | 0.456798 | 0.640351 | 0.685746 | 0.668640 | 0.581182 | 2 | 0.685746 | 2 |
| Texas 10-split | 0.829730 | 0.575676 | 0.583784 | 0.583784 | 0.201230 | 0 | 0.829730 | 0 |
| Wisconsin 10-split | 0.839216 | 0.527451 | 0.619608 | 0.501961 | 0.244926 | 0 | 0.839216 | 0 |

The K2 gate selects the oracle K on 4/5 datasets. On Cora it selects K=2 while
K=3 is best, but K=2 is still strong and close to recent BGRL controls.

## Decision

Promote LIFT-PROP-GCL to `ACTIVE_WITH_NOVELTY_RISK`:

- It passes a fair zero-training proxy on the exact fixed splits used in this
  project.
- It explains both sides of the historical failure pattern: Chameleon needs
  propagation, while WebKB must keep raw features.
- It is label-free and does not use validation labels for the gate.
- It has clear novelty risk against PROPGCL and propagation/filtering work, so
  it cannot be called paper-ready yet.

## Next Checks

1. Direct novelty check against PROPGCL, Less is More, ASPECT, GRAPHITE,
   graph-adaptive propagation, and label-free graph structure reliability
   metrics.
2. Extend to Cornell, Actor, and Squirrel if data is available.
3. Convert the proxy into a formal method runner with parseable CSV:
   `reproduce_lift_prop.py`.
4. If novelty survives, refine the method as a reliability-gated graph
   contrastive / propagation-contrastive framework rather than a generic
   deterministic baseline.
