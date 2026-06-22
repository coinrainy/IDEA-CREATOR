# Sharpness-Stable Alignment BGRL R100/R101 Results

**Date**: 2026-06-22 19:03  
**Status**: `BGRL_INTERNAL_WEAK_SIGNAL_NOT_MAIN_METHOD`  
**Code**: `baselines/BGRL/train_npg_transductive.py`,
`baselines/BGRL/reproduce_npg.py`  
**Runs**:
`baselines/BGRL/runs/ssa_smoke_20260622/results.csv`,
`baselines/BGRL/runs/ssa_m1_split0_20260622/results.csv`

## Question

SSA-BGRL tests whether BGRL should trust only those node-level alignment
signals that remain stable under small online-network parameter perturbations.
At each step, the online encoder and predictor receive a temporary random
parameter perturbation, the perturbed node-level alignment loss is measured,
and nodes with low sharpness drift receive larger weights.

Two variants were tested:

- `ssa_weight`: reweight BGRL node losses by perturbation stability.
- `ssa_consistency`: add a small consistency term to the perturbed online
  predictions in addition to the stability weights.

The final node-classification probe remains the canonical CPU sklearn protocol.
Training runs on CUDA when available.

## Engineering Check

R100 smoke passed on Cora and Chameleon for both SSA variants. No NaN or
collapse was observed.

| Dataset | Variant | Epochs | Device | Test@Best | Collapse |
|---|---|---:|---|---:|---:|
| Cora | `ssa_weight` | 5 | cuda | 0.776188 | 0 |
| Cora | `ssa_consistency` | 5 | cuda | 0.776188 | 0 |
| Chameleon | `ssa_weight` | 5 | cuda | 0.401316 | 0 |
| Chameleon | `ssa_consistency` | 5 | cuda | 0.401316 | 0 |

## Split-0 Gate

R101 ran 200-epoch split-0 comparisons on Cora, CiteSeer, and Chameleon, then
stopped early before Texas/Wisconsin after the Chameleon gate failed.

| Dataset | BGRL control | `ssa_weight` | `ssa_consistency` | Best SSA delta | LIFT-Portfolio split-0 | Decision |
|---|---:|---:|---:|---:|---:|---|
| Cora | 0.832949 | 0.834333 | 0.834333 | +0.001384 | 0.842640 | weak internal gain |
| CiteSeer | 0.693088 | 0.696093 | 0.694966 | +0.003005 | 0.725770 | weak internal gain |
| Chameleon | 0.438596 | 0.438596 | 0.438596 | +0.000000 | 0.699561 | no gain |

Texas `bgrl_control` completed before interruption (`0.621622`), but SSA
variants were not run because the method had already failed the main gate.

## Interpretation

The perturbation-stability signal is measurable and stable: final stability
means are about `0.984` on the completed 200-epoch SSA runs, with no collapse.
However, the weighting effect is too weak. It gives only tiny homophily gains
and does not improve Chameleon at all.

This is not enough for a paper-level graph contrastive method. It also remains
far below the required LIFT-Portfolio control on all three evaluated datasets.
Recent work on graph sharpness/generalization and ASPECT-S style
stability-aware GCL further narrows the novelty window for a plain
perturbation-stability claim.

## Decision

Do not expand SSA-BGRL to 10-split or external baselines. Keep it as negative
evidence: parameter-sharpness stability alone is too mild to convert BGRL into
a competitive node-classification method under the current protocol.
