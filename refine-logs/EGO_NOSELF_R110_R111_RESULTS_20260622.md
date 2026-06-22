# Ego-NoSelf BGRL R110/R111 Results

**Date**: 2026-06-22
**Candidate**: Ego-NoSelf BGRL
**Status**: `FAILED_SPLIT0_GATE`

## Motivation

Positive-Path / No-self LIFT is currently the strongest low-novelty control on
Chameleon, so R110/R111 tested whether the same idea can become a trained BGRL
encoder: remove automatic self-loops from `GCNConv` and train standard BGRL.

Implementation:

- Added `NoSelfGCN` to `baselines/BGRL/train_npg_transductive.py`.
- Added variant `ego_noself` to `train_npg_transductive.py` and
  `reproduce_npg.py`.
- `NoSelfGCN` uses `GCNConv(add_self_loops=False)` in every layer.

## GPU / Evaluation Protocol

All runs used `--device=auto` and resolved to `cuda`. Training and
representation extraction used GPU. Final node-classification probes stayed on
the canonical CPU sklearn protocol.

## Commands

```bash
python reproduce_npg.py --datasets=cora,chameleon --variants=ego_noself --splits=0 --epochs=5 --eval_epochs=5 --device=auto --output_dir=runs/ego_noself_smoke_20260622 --clean
python reproduce_npg.py --datasets=cora,citeseer,chameleon --variants=ego_noself --splits=0 --epochs=200 --eval_epochs=20 --device=auto --output_dir=runs/ego_noself_m1_split0_20260622 --clean
```

## R110 Smoke

| Dataset | Variant | Device | Test@Best | Effective rank | NaN | Collapse |
|---|---|---|---:|---:|---:|---:|
| Cora | `ego_noself` | cuda | 0.759575 | 208.785 | 0 | 0 |
| Chameleon | `ego_noself` | cuda | 0.300439 | 120.748 | 0 | 0 |

Smoke passed engineering checks but was already weak.

## R111 Split-0 Gate

| Dataset | BGRL control reference | `ego_noself` | Delta | Required reference | Decision |
|---|---:|---:|---:|---:|---|
| Cora | 0.832949 | 0.815874 | -0.017074 | LIFT 0.842640 | fail |
| CiteSeer | 0.693088 | 0.663411 | -0.029677 | LIFT 0.725770 | fail |
| Chameleon | 0.438596 | 0.287281 | -0.151316 | Positive-Path 0.725877 | decisive fail |

No NaN/collapse occurred. The failure is representational, not numerical.

## Decision

`FAILED_SPLIT0_GATE`. Do not run WebKB, 10-split, or external baselines for
direct no-self BGRL training.

Interpretation: the no-self / positive-path signal is useful as a fixed
propagation feature channel under the LIFT-Portfolio gate, but simply removing
self-loops from the GCN encoder destroys too much node identity information
during BGRL training. Future ego-shortcut work must preserve a protected raw or
identity channel while isolating no-self path information; direct no-self
message passing is not viable.
