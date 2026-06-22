# LIFT-PROP-GCL Extra Validation

**Date**: 2026-06-22 12:25  
**Status**: `POSITIVE_BUT_INCOMPLETE`  

## Purpose

After the five-dataset M0 gate and novelty check, we tested whether the
edge-lift rule transfers beyond Cora/CiteSeer/Chameleon/Texas/Wisconsin.

Gate:

```text
if lift(P^2X) >= 0.35: use K=2
else: use K=0
```

## Results

CSV:

```text
baselines/BGRL/runs/lift_prop_extra_hetero10_20260622/results.csv
baselines/BGRL/runs/lift_prop_actor_squirrel_split0_20260622/results.csv
baselines/BGRL/runs/lift_prop_actor_squirrel10_fast_20260622/results.csv
baselines/BGRL/runs/lift_prop_actor_squirrel10_fast_20260622/selected_summary.csv
```

| Dataset | Split protocol | K0 | K1 | K2 | K3 | lift(P2X) | Gate choice | Oracle K | Decision |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| Cornell | 10 Geom-GCN splits | 0.816216 +/- 0.059487 | 0.591892 | 0.589189 | 0.581081 | 0.169372 | 0 | 0 | hit |
| Actor | split 0 only | 0.348684 | 0.287500 | 0.299342 | 0.279605 | 0.249076 | 0 | 0 | hit |
| Squirrel | split 0 only | 0.328530 | 0.529299 | 0.571566 | 0.536984 | 0.446390 | 2 | 2 | hit |
| Actor | 10 splits, fast C-grid `-4,0,4` | 0.347566 | 0.281382 | 0.293487 | 0.279671 | 0.249076 | 0 | 0 | hit |
| Squirrel | 10 splits, fast C-grid `-4,0,4` | 0.328530 | 0.520365 | 0.509030 | 0.456964 | 0.446390 | 2 | 1 | useful near miss |

## Notes

The previous full 10-split Cornell/Actor/Squirrel run was interrupted because
Actor's linear evaluation was too slow under the full C-grid. Cornell completed
before interruption. Actor and Squirrel were then checked on split 0 only.

The gate still chooses the oracle K on all completed extra checks:

- Cornell behaves like WebKB: propagation hurts, raw should be preserved.
- Actor split 0 also prefers raw.
- Squirrel split 0 behaves like Chameleon: propagation is strongly helpful.
- The faster Actor/Squirrel 10-split check confirms the same raw-vs-propagation
  decision, but shows that Squirrel may prefer K=1 over K=2 under a reduced
  linear-eval grid. This suggests the next method revision should keep the
  edge-lift abstention gate, but consider a second label-free selector between
  K=1 and K=2 when propagation is enabled.

## Decision

This strengthens LIFT-PROP-GCL but does not make it paper-ready. The next
method task is to compare the K2 gate against validation-selected K and a
label-free K1/K2 selector, then compare directly to PROPGCL-style
validation-selected propagation.
