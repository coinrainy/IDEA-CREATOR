# LIFT-PROP R077-R078 Results

**Date**: 2026-06-22  
**Status**: `SELECTOR_BASELINE_NOT_MAIN_METHOD`  
**Scope**: learned coefficient GCL pilot plus node-wise LIFT routing pilot

## Question

R076 showed that LIFT-PROP is a strong zero-label global selector against
fixed PROP-step heuristics, but it did not answer whether LIFT-PROP can become
a full graph contrastive learning method. R077 and R078 tested two compact
extensions:

1. **R077 edge-NCE learned propagation mix**: learn soft coefficients over
   `[X, PX, P2X, P3X]` using an edge-positive/random-negative contrastive loss.
2. **R078 node-wise LIFT routing**: choose raw/K1/K2/K3 per node using local
   edge-vs-random cosine lift.

Both are label-free. Labels are used only for downstream linear evaluation.

## R077: Edge-NCE Learned Mix

Command:

```bash
python evaluate_lift_prop_gcl.py \
  --datasets=cora,citeseer,chameleon,texas,wisconsin \
  --splits=0 \
  --edge_nce_epochs=120 \
  --edge_batch_size=4096 \
  --edge_nce_negatives=32 \
  --edge_nce_lr=0.1 \
  --edge_nce_tau=0.2 \
  --output_dir=runs/lift_prop_gcl_r077_split0_20260622 \
  --device=auto
```

| Dataset | Fixed selector | Edge-NCE mix | LIFT-gated Edge-NCE | Oracle | Decision |
|---|---:|---:|---:|---:|---|
| Cora | 0.825565 | 0.831103 | 0.831103 | 0.828334 | local positive |
| CiteSeer | 0.709617 | 0.684072 | 0.684072 | 0.709617 | fail |
| Chameleon | 0.699561 | 0.622807 | 0.622807 | 0.699561 | fail |
| Texas | 0.810811 | 0.621622 | 0.810811 | 0.810811 | gate protects raw |
| Wisconsin | 0.823529 | 0.568627 | 0.823529 | 0.823529 | gate protects raw |

The learned coefficients are not reliable. Edge-NCE pushes toward
edge-similar representations, but edge similarity is not the same as
classification usefulness. On CiteSeer and Chameleon it damages the strong
fixed selector. On Texas/Wisconsin, the global LIFT gate correctly falls back
to raw and prevents large damage.

## R078: Node-Wise LIFT Routing

Command:

```bash
python evaluate_lift_prop_nodewise.py \
  --datasets=cora,citeseer,chameleon,texas,wisconsin \
  --splits=0 \
  --random_samples=32 \
  --local_batch_size=128 \
  --c_powers=-4,0,4 \
  --output_dir=runs/lift_prop_nodewise_fast_split0_20260622
```

| Dataset | Global v1 | Node hard v1 | Node max-lift | Node soft K0/K2 | Decision |
|---|---:|---:|---:|---:|---|
| Cora | 0.825565 | 0.830180 | 0.827411 | 0.836641 | local positive |
| CiteSeer | 0.716003 | 0.707363 | 0.684448 | 0.710744 | fail |
| Chameleon | 0.668860 | 0.594298 | 0.616228 | 0.653509 | fail |
| Texas | 0.810811 | 0.783784 | 0.729730 | 0.783784 | fail |
| Wisconsin | 0.823529 | 0.745098 | 0.705882 | 0.784314 | fail |

Node-wise LIFT has a Cora-only signal, but it consistently hurts the decisive
heterophily cases. The likely failure mode is representational inconsistency:
row-wise selecting different propagation depths produces a feature space that
is less coherent for one shared linear classifier.

## Decision

LIFT-PROP should no longer be treated as a promising full GCL-training route in
the current form.

Supported claims:

- A global edge-lift selector is a strong label-free propagation reliability
  diagnostic.
- The selector protects raw-dominant graphs from harmful propagation.
- Unconstrained edge-positive contrastive coefficient learning can be actively
  worse than the fixed selector.

Unsupported claims:

- LIFT-PROP beats learned PROPGCL / PROP-GRACE / PROP-DGI.
- Node-wise LIFT routing improves broad node classification.
- Edge-NCE coefficient learning is a viable main method.

## Next Action

Downgrade LIFT-PROP to a required selector/diagnostic baseline unless the
project intentionally pivots to a selector-only paper. Restart idea discovery
with a new mechanism family. Any new GCL idea must compare against global
LIFT-PROP as a strong training-free control and must not equate higher edge
alignment with downstream utility.
