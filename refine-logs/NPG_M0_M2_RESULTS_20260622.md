# NPG-GCL M0-M2 Results

**Date**: 2026-06-22 10:28  
**Candidate**: NPG-GCL, Nontrivial Positive Gain Graph Contrastive Learning  
**Status**: `WEAK_SIGNAL_DEPRIORITIZED`, not `READY_TO_REFINE`  
**Subagent reviewer policy**: disabled only for ad-hoc reviewer/code-review subagents; `research-review` and `auto-review-loop` remain available later.

## Implementation

New files:

```text
baselines/BGRL/train_npg_transductive.py
baselines/BGRL/reproduce_npg.py
```

The trainer keeps BGRL's node-wise bootstrap alignment and applies a detached
nontrivial positive-gain weight computed from a normalized propagation
prealignment baseline. It writes parseable JSON/CSV diagnostics.

Verification:

```text
python -m py_compile train_npg_transductive.py reproduce_npg.py
python reproduce_npg.py --datasets cora,chameleon --variants npg --splits 0 --epochs 5 --eval_epochs 5 --output_dir runs/npg_m0_smoke_20260622 --clean
```

Both passed.

## M0 Smoke

CSV:

```text
baselines/BGRL/runs/npg_m0_smoke_20260622/results.csv
```

| Dataset | Variant | Epochs | Test@Best | NaN | Collapse |
|---|---|---:|---:|---:|---:|
| Cora | NPG | 5 | 0.772497 | 0 | 0 |
| Chameleon | NPG | 5 | 0.396930 | 0 | 0 |

## M1 Split-0 Main Pilot

CSV:

```text
baselines/BGRL/runs/npg_m1_split0_20260622/results.csv
```

| Dataset | Control | NPG | Delta | NPG weight std | NPG gain mean | Decision |
|---|---:|---:|---:|---:|---:|---|
| Cora | 0.830641 | 0.834333 | +0.003692 | 0.412098 | 0.039775 | weak positive |
| CiteSeer | 0.692712 | 0.691210 | -0.001503 | 0.416771 | 0.033108 | weak negative |
| Chameleon | 0.438596 | 0.442982 | +0.004386 | 1.057297 | 0.250888 | weak positive |
| Texas | 0.621622 | 0.621622 | +0.000000 | 0.440493 | 0.053985 | tie |
| Wisconsin | 0.549020 | 0.549020 | +0.000000 | 0.339933 | 0.031689 | tie |

No NaN/collapse occurred. NPG did not damage WebKB, but it also did not produce
the required `+0.01` Cora/CiteSeer signal.

## M2 Ablation

CSV:

```text
baselines/BGRL/runs/npg_m2_ablate_20260622/results.csv
```

| Dataset | Control | NPG | Uniform gain | Random gain | Interpretation |
|---|---:|---:|---:|---:|---|
| Cora | 0.830641 | 0.834333 | 0.833410 | 0.838948 | NPG not better than random weighting |
| Chameleon | 0.438596 | 0.442982 | 0.438596 | 0.429825 | NPG has a small non-random signal |

## Decision

NPG-GCL is not dead as an auxiliary idea, but it is not strong enough to become
the active paper route:

- passes engineering and stability checks;
- produces only weak split-0 gains;
- fails the Cora ablation because random weighting is stronger;
- has a small interpretable Chameleon signal, but too small for 3-split
  expansion under the positive-method objective.

Next action: stop NPG as the lead and move to SC-BGRL, the signed-compatibility
backup route. Do not run NPG 3-split unless later methods suggest reusing
nontrivial positive-gain weights as a component.
