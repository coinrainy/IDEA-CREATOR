# CIG/CLEAR Counterfactual Edge Results

**Date**: 2026-06-22  
**Candidate family**: CIG-GCL / CLEAR-GCL  
**Verdict**: `STOP`

## Motivation

After DCA and VST failed as main methods, the next speculative family was counterfactual edge influence:

- CIG-GCL: dynamically gate edges by teacher consistency or influence.
- CLEAR-GCL: treat high-variance/high-influence edges as augmentation environments instead of positive evidence.

Before implementing a new training objective, we ran a cheaper diagnostic: load existing RFA/BGRL checkpoints, apply deterministic counterfactual edge masks at inference, and evaluate `graph + raw`.

Implementation:

- `baselines/BGRL/evaluate_counterfactual_edges.py`

Closest novelty risks:

- ACGA: model-based adversarial contrastive graph augmentation with counterfactual regularization.
- SPGCL: structure-aware SVD-guided perturbation and sparse recovery.
- AFECL: edge-level graph contrastive learning.
- RaDAR: relation-aware edge refinement in contrastive learning.

## Split-0 Diagnostic

Commands wrote:

```text
baselines/BGRL/runs/cig_edge_counterfactual_split0_20260622/{dataset}.csv
```

| Dataset | Best counterfactual fused | Original fused | Raw/control | Decision |
|---|---:|---:|---:|---|
| Cora | 0.812183 (`orig`) | 0.812183 | prior anchors ~0.84 | no signal |
| Chameleon | 0.513158 (`orig`) | 0.513158 | DCA split-0 ~0.508 / graph_raw 0.513 | no signal |
| Texas | 0.783784 | 0.729730 | raw 0.810811 | fail vs raw |
| Wisconsin | 0.843137 | 0.784314 | raw 0.823529 | local positive |

Only Wisconsin split 0 showed a positive edge-mask signal.

## Texas / Wisconsin 10-Split Check

Commands wrote:

```text
baselines/BGRL/runs/cig_edge_counterfactual_texas10_20260622/results.csv
baselines/BGRL/runs/cig_edge_counterfactual_wisconsin10_20260622/results.csv
```

### Wisconsin

| Selection | Mean Test |
|---|---:|
| raw baseline | 0.839216 |
| best fixed mask (`keep_align_lo`) | 0.823529 |
| validation-selected mask | 0.827451 |
| original fused RFA in this evaluator | 0.792157 |

### Texas

| Selection | Mean Test |
|---|---:|
| raw baseline | 0.829730 |
| best fixed mask (`keep_disagree_lo`) | 0.794595 |
| validation-selected mask | 0.805405 |
| original fused RFA in this evaluator | 0.751351 |

## Verdict

Stop CIG/CLEAR as a main route.

The family has diagnostic value: counterfactual edge masks can improve some raw-fused graph representations relative to RFA on Texas/Wisconsin. However, even validation-selected masks do not beat raw-only 10-split baselines. Chameleon, the decisive non-raw-dominant dataset, does not improve over the original graph view.

Do not implement a training objective for this family unless a new mechanism can beat the raw baseline without validation engineering.
