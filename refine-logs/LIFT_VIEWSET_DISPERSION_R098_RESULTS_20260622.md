# LIFT View-Set Dispersion R098 Results

**Date**: 2026-06-22 18:36  
**Status**: `FAILED_PROXY_GATE`  
**Code**: `baselines/BGRL/evaluate_lift_viewset_dispersion.py`  
**Related prior risk**: UGCL, "Uncertainty-guided Graph Contrastive Learning from a Unified Perspective", IJCAI 2025.

## Question

After SBB failed, R098 tested a cheaper proxy for a possible
Conformal/View-Set GCL direction. The hypothesis was that node-level dispersion
across the propagation view set `[X, PX, P2X, P3X]` might provide useful
uncertainty information beyond LIFT-Portfolio.

This was deliberately evaluated as a training-free proxy first. If fixed
dispersion features hurt LIFT-Portfolio, a GPU-trained view-set uncertainty
objective is unlikely to be worth implementing. Final probes use the canonical
CPU sklearn protocol.

## Completed Split-0 Results

The run was stopped after Chameleon `portfolio_mean_std` because the proxy had
already failed decisively.

| Dataset | Portfolio | Best / tested dispersion variant | Result | Delta | Decision |
|---|---:|---|---:|---:|---|
| Cora | 0.842640 | `portfolio_mean_std` | 0.844947 | +0.002307 | tiny local gain |
| CiteSeer | 0.725770 | `portfolio_mean_std` | 0.720135 | -0.005635 | fail |
| CiteSeer | 0.725770 | `portfolio_stats` | 0.714876 | -0.010894 | fail |
| CiteSeer | 0.725770 | `portfolio_stats_deltas` | 0.710368 | -0.015402 | fail |
| Chameleon | 0.699561 | `portfolio_mean_std` | 0.662281 | -0.037281 | fail |

## Interpretation

The Cora gain is too small and not robust to adding richer statistics
(`portfolio_stats` regresses). CiteSeer and Chameleon are decisive failures:
dispersion features dilute or damage the strong LIFT-Portfolio representation,
especially when Chameleon correctly chooses single `P2X`.

The novelty case is also weak: uncertainty-guided GCL already exists and
jointly designs augmentation and contrastive loss around sample uncertainty.
Our fixed view-set dispersion proxy is narrower and empirically negative.

## Decision

Do not implement a GPU-trained view-set dispersion or conformal-view-set
objective from this proxy. Keep the script as a diagnostic. The next route
should not simply append propagation-view uncertainty statistics to
LIFT-Portfolio.
