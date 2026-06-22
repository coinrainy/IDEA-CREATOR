# Spillover-Blocked BGRL R097 Results

**Date**: 2026-06-22 18:24  
**Status**: `FAILED_MIXED_SPLIT0_GATE`  
**Code**: `baselines/BGRL/train_npg_transductive.py`, `baselines/BGRL/reproduce_npg.py`

## Method

SBB is a minimal spillover-blocking prototype inside the existing NPG runner.
For edges with low raw feature cosine, the GCN forward pass keeps the neighbor
message value but stop-gradients that message path. The intent is to preserve
neighbor information while preventing harmful self-supervised gradients from
training the encoder around unreliable neighbor messages.

Variants:

- `sbb_hard`: hard stop-gradient on the bottom raw edge-cosine quantile.
- `sbb_soft`: soft interpolation between normal and detached messages.

Training used CUDA (`--device=auto`); final probe stayed CPU sklearn.

## Results

| Dataset | BGRL control | SBB hard | SBB soft | Best SBB delta | LIFT-Portfolio split-0 | Decision |
|---|---:|---:|---:|---:|---:|---|
| Cora | 0.832949 | 0.815413 | 0.812644 | -0.017536 | 0.842640 | fail |
| CiteSeer | 0.692712 | 0.687077 | 0.688204 | -0.004508 | 0.725770 | fail |
| Chameleon | 0.438596 | 0.427632 | 0.401316 | -0.010965 | 0.699561 | fail |
| Texas | 0.621622 | 0.648649 | 0.594595 | +0.027027 | 0.810811 | internal-only |
| Wisconsin | 0.549020 | 0.568627 | 0.568627 | +0.019608 | 0.823529 | internal-only |

## Interpretation

SBB is stable from an engineering standpoint: no NaN, no collapse, and CUDA
training worked. But the method damages Cora, CiteSeer, and Chameleon, which
are the decisive settings for a general graph contrastive method. The WebKB
gains are only relative to a weak BGRL control and remain far below the
raw/LIFT-Portfolio baseline.

The stop-gradient message path is therefore too blunt. It likely blocks useful
optimization signal on homophilous graphs and does not fix Chameleon.

## Decision

Do not run SBB 10-split or tune edge quantiles. Keep it as negative evidence
against simple low-cosine message stop-gradient. The next method should not
rely on post-hoc edge cosine alone to decide which message paths are allowed to
train.
