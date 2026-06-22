# SRLP Target Alignment Diagnostics

**Date**: 2026-06-22  
**Input runs**: `baselines/BGRL/runs/srlp_aux_10split_target_family_20260621_221832/`  
**Purpose**: diagnose why SRLP-Aux only helps Chameleon and does not reliably beat FullLatent/ZPZ on Texas, Wisconsin, and Actor.

This is not a new paper table. It is a method-level diagnostic over existing checkpoints.

## Diagnostic Setup

For each dataset and Geom-GCN split 0-9, load trained teacher encoders from:

- `full_latent_iso`
- `srlp_aux`

Then compute label alignment of target components by frozen linear evaluation:

```text
full            = normalize(z_v)
proj            = normalize(q_v q_v^T z_v)
rank1_residual  = normalize(z_v - q_v q_v^T z_v)
zpz             = normalize(z_v - P z_v)
srlp_aux_target = normalize(z_v + 0.1 * w_v * rank1_residual)
```

The diagnostic also evaluates local multi-direction residuals:

```text
rankk_residual = normalize((I - U_k U_k^T) z_v), k in {1,2,4,8}
```

where `U_k` is the top-k local context subspace from visible neighbor teacher latents.

## SRLP-Aux 10 Split Context

| Dataset | FullLatent-Iso | ZPZ-Iso | SRLP-Aux | Aux vs best non-Aux |
|---|---:|---:|---:|---:|
| Chameleon | 0.49167 +/- 0.02850 | 0.44342 +/- 0.02989 | 0.49759 +/- 0.02102 | +0.00395 |
| Texas | 0.58919 +/- 0.05375 | 0.61081 +/- 0.05583 | 0.58919 +/- 0.04558 | -0.02432 |
| Wisconsin | 0.54118 +/- 0.05080 | 0.53725 +/- 0.04256 | 0.53725 +/- 0.04452 | -0.01765 |
| Actor | 0.27592 +/- 0.00663 | 0.27355 +/- 0.00775 | 0.27592 +/- 0.00856 | -0.00145 |

## Component Alignment: SRLP-Aux Teacher

| Dataset | Full | SRLP-Aux Target | Rank-1 Residual | Projection | ZPZ |
|---|---:|---:|---:|---:|---:|
| Chameleon | 0.45219 +/- 0.01799 | 0.45482 +/- 0.01565 | 0.43026 +/- 0.02909 | 0.54781 +/- 0.02105 | 0.41491 +/- 0.03096 |
| Texas | 0.57838 +/- 0.05284 | 0.58919 +/- 0.05375 | 0.61892 +/- 0.06427 | 0.58378 +/- 0.06885 | 0.64595 +/- 0.05619 |
| Wisconsin | 0.54510 +/- 0.05831 | 0.54118 +/- 0.06075 | 0.53922 +/- 0.03949 | 0.54118 +/- 0.05861 | 0.53333 +/- 0.07148 |
| Actor | 0.27257 +/- 0.01031 | 0.27158 +/- 0.01185 | 0.27868 +/- 0.01466 | 0.25658 +/- 0.01248 | 0.27322 +/- 0.01003 |

## Rank-k Residual Alignment: SRLP-Aux Teacher

| Dataset | Full | Rank-1 | Rank-2 | Rank-4 | Rank-8 | Best Rank-k vs Full |
|---|---:|---:|---:|---:|---:|---:|
| Chameleon | 0.45219 | 0.41404 | 0.42741 | 0.43706 | 0.44013 | -0.01206 |
| Texas | 0.57838 | 0.61351 | 0.62162 | 0.62162 | 0.62162 | +0.04324 |
| Wisconsin | 0.54510 | 0.55294 | 0.57255 | 0.57843 | 0.59020 | +0.04510 |
| Actor | 0.27257 | 0.27270 | 0.27224 | 0.27020 | 0.27428 | +0.00171 |

## Findings

1. **The original rank-1 residual assumption is not universal.**  
   Chameleon rank-k residual is consistently weaker than full latent, while Texas and Wisconsin rank-k residuals are stronger than full latent.

2. **Chameleon should not remove the projection component.**  
   The projection component has much stronger label alignment than full latent and residual on Chameleon. This means the visible context direction is not merely a shortcut there; it carries task-relevant signal.

3. **Texas/Wisconsin failures are not because residuals lack signal.**  
   Texas and Wisconsin rank-k residuals have strong label alignment, especially rank-2/rank-8. The failure is likely an interface/training issue: SRLP-Aux's single weak residual mixture does not transfer that target signal into the online representation.

4. **Actor is near the noise floor.**  
   Full, residual, ZPZ, and SRLP-Aux target alignment are all close. This dataset should not drive the next method revision.

## Method Implication

The next method should not be a universal residual objective. The more defensible direction is:

> decompose teacher information into context-aligned and context-residual components, then use a label-free gate to decide when residual prediction is helpful.

The gate cannot use labels. Candidate label-free signals:

- residual energy relative to projection energy;
- stability of rank-k residual under edge/feature perturbation;
- agreement between propagation residual `Z-PZ` and context-subspace residual;
- online predictability of residual from isolated context.

## Current Recommendation

Do not run external baselines or large datasets. The next smallest useful step is a pure diagnostic or small pilot for an adaptive target:

```text
y_v = normalize(z_v + lambda_r * g_r(v) * r_k(v) + lambda_p * g_p(v) * p_v)
```

where:

```text
p_v = U_k U_k^T z_v
r_k(v) = (I - U_k U_k^T) z_v
g_r(v), g_p(v) are label-free gates
```

For Chameleon, the gate should preserve or emphasize `p_v`. For Texas/Wisconsin, the gate should emphasize multi-direction residual. If a simple gate cannot separate these cases, SRLP should be downgraded to an auxiliary diagnostic rather than a paper method.

## Output Files

- Raw component alignment: `baselines/BGRL/runs/srlp_aux_10split_target_family_20260621_221832/target_alignment.csv`
- Component summary: `baselines/BGRL/runs/srlp_aux_10split_target_family_20260621_221832/target_alignment_summary.json`
- Rank-k raw alignment: `baselines/BGRL/runs/srlp_aux_10split_target_family_20260621_221832/target_alignment_rankk.csv`
- Rank-k summary: `baselines/BGRL/runs/srlp_aux_10split_target_family_20260621_221832/target_alignment_rankk_summary.json`
