# VST-GCL M0/M1 Results

**Date**: 2026-06-22  
**Candidate**: VST-GCL, Variance-Stabilized Transport Graph Contrastive Learning  
**Verdict**: `FAIL`

## Implementation

Added a minimal VST prototype:

- `baselines/BGRL/train_vst_transductive.py`
- `baselines/BGRL/reproduce_dcgcl.py --variants vst`

The method builds sparse local transport weights from raw-feature semantic top-k neighbors, boosted when the semantic neighbor is also a graph-topology neighbor. The online graph embedding predicts the transported teacher barycenter:

```text
t_i = normalize(sum_j T_ij stopgrad(z_j^teacher))
L = lambda_bgrl L_BGRL + lambda_transport (1 - cos(q_i, t_i))
```

## M0 Smoke

Command:

```text
python reproduce_dcgcl.py --variants vst --datasets cora,chameleon --epochs 5 --eval_epochs 5 --output_dir runs/vst_m0_smoke_20260622 --clean --quiet
```

| Dataset | Graph Test@Best | Fused Test@Best | Raw | NaN | Collapse |
|---|---:|---:|---:|---|---|
| Cora | 0.767420 | 0.779880 | 0.659437 | no | no |
| Chameleon | 0.379386 | 0.464912 | 0.440789 | no | no |

Smoke passed engineering checks.

## M1 Split-0 Gate

Command:

```text
python reproduce_dcgcl.py --variants vst --datasets cora,chameleon,texas,wisconsin --epochs 200 --eval_epochs 20 --output_dir runs/vst_m1_split0_20260622 --clean --quiet
```

| Dataset | Graph Test@Best | Fused Test@Best | Raw | Decision |
|---|---:|---:|---:|---|
| Cora | 0.804338 | 0.814490 | 0.659437 | weak; below prior anchor controls |
| Chameleon | 0.405702 | 0.469298 | 0.440789 | fail vs graph_raw/DCA controls |
| Texas | 0.621622 | 0.729730 | 0.810811 | fail vs raw |
| Wisconsin | 0.549020 | 0.803922 | 0.823529 | fail vs raw |

Transport diagnostics:

| Dataset | Support | Stable support | No-stable ratio | Stable mass |
|---|---:|---:|---:|---:|
| Cora | 16.47 | 0.839 | 0.470 | 0.434 |
| Chameleon | 16.78 | 0.346 | 0.783 | 0.165 |
| Texas | 16.77 | 0.459 | 0.770 | 0.182 |
| Wisconsin | 16.67 | 0.633 | 0.665 | 0.271 |

The low stable-support mass on Chameleon/Texas indicates that local raw-feature semantics and graph topology rarely agree; the transport target mostly degenerates to semantic-kNN-like mass, which was already a weak direction.

## Low-Auxiliary Ablation

Command:

```text
python reproduce_dcgcl.py --variants vst --datasets cora,chameleon --epochs 200 --eval_epochs 20 --lambda_bgrl 1.0 --lambda_semantic 0.1 --output_dir runs/vst_ablate_low_aux_20260622 --clean --quiet
```

| Dataset | Graph Test@Best | Fused Test@Best | Raw | Decision |
|---|---:|---:|---:|---|
| Cora | 0.808030 | 0.810337 | 0.659437 | no improvement |
| Chameleon | 0.410088 | 0.467105 | 0.440789 | fail |

Reducing the transport loss does not recover a positive mechanism signal.

## Verdict

Stop VST-GCL as a main route.

The method is stable but not positive. Do not run 10-split, external baselines, or additional local tuning. The pipeline needs another divergence pass into a genuinely different mechanism family.

