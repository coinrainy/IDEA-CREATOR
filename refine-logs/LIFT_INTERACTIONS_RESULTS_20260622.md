# LIFT Interaction Features R087 Results

**Date**: 2026-06-22  
**Status**: `FAILED_SPLIT0_GATE`  
**Script**: `baselines/BGRL/evaluate_lift_interactions.py`  
**Raw CSV**: `baselines/BGRL/runs/lift_interactions_split0_fast_20260622/results.csv`

## Question

R087 tested whether fixed nonlinear interactions between raw features and
propagated features add information that plain LIFT-Stack cannot express with a
linear probe. Variants append blocks such as `X * P^kX`, `|P^kX - X|`, and
hop-to-hop deltas to the LIFT-Stack representation.

## Fast Split-0 Result

| Dataset | LIFT-Stack | Best Interaction | Best Variant | Delta | Decision |
|---|---:|---:|---|---:|---|
| Cora | 0.842640 | 0.845408 | stack_plus_diff | +0.002768 | small local positive |
| CiteSeer | 0.725770 | 0.729527 | stack_plus_agree | +0.003757 | small local positive |
| Chameleon | 0.668860 | 0.666667 | stack_plus_delta | -0.002193 | fail |

Other Chameleon interaction variants are much worse: `stack_plus_agree`
`0.607456`, `stack_plus_diff` `0.638158`, and `stack_plus_agree_delta`
`0.616228`.

## Decision

Do not expand R087. The small Cora/CiteSeer gains are variant-specific and do
not transfer to Chameleon, the key propagation-positive heterophily setting.
Fixed nonlinear feature interactions remain a diagnostic / feature-engineering
observation, not a paper-level GCL mechanism.
