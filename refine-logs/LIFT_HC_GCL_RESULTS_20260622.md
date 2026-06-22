# LIFT-HC-GCL Results

**Date**: 2026-06-22  
**Status**: `FAILED_MIXED_SPLIT0_GATE`  
**Candidate**: LIFT-HC-GCL, hop-drop contrastive encoder on top of LIFT-Stack

## Method

LIFT-HC-GCL tests whether a genuine contrastive component can improve the
strong training-free LIFT-Stack baseline. It precomputes
`[X, PX, P2X, P3X]`, trains an MLP encoder with two hop/feature-drop views
using a SimSiam-style loss, and evaluates:

- `global_lift`: single-depth LIFT selector;
- `lift_stack`: raw fallback or `[X,PX,P2X,P3X]`;
- `ssl_only`: hop-contrastive embedding only;
- `lift_stack_plus_ssl`: concatenate LIFT-Stack and SSL embedding.

No labels are used in SSL training; labels are only used by downstream linear
evaluation.

## Main Split-0 Gate

Command:

```bash
python evaluate_lift_hc_gcl.py \
  --datasets=cora,citeseer,chameleon,texas,wisconsin \
  --splits=0 \
  --epochs=300 \
  --hidden_dim=512 \
  --output_dim=256 \
  --predictor_dim=256 \
  --c_powers=-4,0,4 \
  --output_dir=runs/lift_hc_gcl_split0_20260622
```

| Dataset | LIFT-Stack | SSL only | Stack + SSL | Decision |
|---|---:|---:|---:|---|
| Cora | 0.842640 | 0.837102 | 0.850023 | positive |
| CiteSeer | 0.725770 | 0.672427 | 0.716754 | fail |
| Chameleon | 0.668860 | 0.552632 | 0.657895 | fail |
| Texas | 0.810811 | 0.486486 | 0.810811 | protected |
| Wisconsin | 0.823529 | 0.588235 | 0.843137 | local positive |

## Short-Training Probe

20 epoch, 64-dimensional SSL:

| Dataset | LIFT-Stack | Stack + SSL | Decision |
|---|---:|---:|---|
| Cora | 0.842640 | 0.849562 | positive |
| CiteSeer | 0.725770 | 0.726897 | tiny positive |
| Chameleon | 0.668860 | 0.662281 | fail |

5 epoch, 64-dimensional SSL:

| Dataset | LIFT-Stack | Stack + SSL | Decision |
|---|---:|---:|---|
| Cora | 0.842640 | 0.850485 | positive |
| CiteSeer | 0.725770 | 0.724267 | tie/negative |
| Chameleon | 0.668860 | 0.664474 | fail |

## Interpretation

The hop-drop SSL branch is not robust enough to promote:

- Cora benefits consistently from the extra contrastive embedding.
- CiteSeer is sensitive to training length and embedding size.
- Chameleon, the decisive heterophily graph, regresses under all checked
  settings.
- WebKB raw-dominant graphs are protected only because LIFT keeps raw features;
  `ssl_only` itself is poor.

The likely failure mode matches PROPGCL's warning: contrastive transformation
can inject objectives that are misaligned with downstream node classification.
LIFT-Stack is still the stronger control.

## Decision

Do not expand LIFT-HC-GCL to 10-split or external baselines. Keep the script as
a diagnostic for "fixed stack + contrastive transformation" and restart the
main-method search with a mechanism that does not rely on adding a generic MLP
contrastive branch to LIFT-Stack.
