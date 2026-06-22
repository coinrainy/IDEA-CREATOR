# SRLP-Aux 10 Split Internal Ablation Results

**Completed**: 2026-06-22 00:27  
**Output CSV**: `baselines/BGRL/runs/srlp_aux_10split_target_family_20260621_221832/results.csv`  
**Scope**: Geom-GCN official splits 0-9, target-family internal ablation only.  
**Variants**: `FullLatent-Iso`, `ZPZ-Iso`, `SRLP-Aux`.

## Run Integrity

| Check | Value |
|---|---:|
| Expected rows | 120 |
| Actual rows | 120 |
| NaN flags | 0 |
| Collapse flags | 0 |
| Max skipped ratio | 0.05405 |

## Mean +/- Std Test@Best

| Dataset | FullLatent-Iso | ZPZ-Iso | SRLP-Aux | Aux vs best non-Aux | Split wins/ties/losses |
|---|---:|---:|---:|---:|---:|
| Chameleon | 0.49167 +/- 0.02850 | 0.44342 +/- 0.02989 | 0.49759 +/- 0.02102 | +0.00395 | 5/1/4 |
| Texas | 0.58919 +/- 0.05375 | 0.61081 +/- 0.05583 | 0.58919 +/- 0.04558 | -0.02432 | 0/5/5 |
| Wisconsin | 0.54118 +/- 0.05080 | 0.53725 +/- 0.04256 | 0.53725 +/- 0.04452 | -0.01765 | 0/5/5 |
| Actor | 0.27592 +/- 0.00663 | 0.27355 +/- 0.00775 | 0.27592 +/- 0.00856 | -0.00145 | 3/2/5 |

## Interpretation

- **Chameleon**: positive but small. SRLP-Aux improves mean test over the best non-Aux target-family variant by about 0.40 percentage points.
- **Texas**: negative. ZPZ-Iso is clearly stronger on mean test.
- **Wisconsin**: negative to tied. FullLatent-Iso is strongest; SRLP-Aux matches ZPZ-Iso mean but trails the best non-Aux variant.
- **Actor**: effectively tied with FullLatent-Iso on mean, but split-wise wins are not stable.

## Decision

SRLP-Aux is a real improvement over residual-only SRLP, but the 10 split internal ablation does **not** support moving to an external strong-baseline paper table.

Current status:

- residual-only SRLP: failed as a main method;
- SRLP-Aux: useful as a safer residual auxiliary, but not yet a strong paper method;
- next method step: revise the target again or downgrade the contribution to a diagnostic/auxiliary regularization claim.

## Recommended Next Step

Do not expand to PubMed, Squirrel, Amazon, Coauthor, Wiki-CS, or external baselines yet. If continuing, focus on method-level redesign:

1. replace rank-1 context direction with a small multi-direction context subspace;
2. measure label alignment of full latent vs residual components;
3. test whether SRLP-Aux should be dataset-gated rather than universal.
