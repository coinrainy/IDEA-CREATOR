# PUAB-GCL Worker B R112 Results

**Date**: 2026-06-22
**Worker**: B
**Candidate**: Pair-Utility Calibrated GCL / Positive-Unlabeled-Abstention
**Status**: `FAILED_SPLIT0_GATE`

## Idea

PUAB-GCL tests whether BGRL positive pairs should be calibrated at the
directional pair level rather than with a single node-level loss weight.
For each online-target positive pair, the utility gate uses only label-free
signals:

- positive-pair cosine loss, to abstain already-easy or outlier-hard pairs;
- target-view consistency, to avoid unstable positive targets;
- raw-vs-propagated prealignment as a weak prior, not as the sole node weight.

Two variants were tested:

- `puab_soft`: soft utility gate with normalized directional pair weights.
- `puab_hard`: hard abstention gate over reliable, nontrivial, non-outlier
  directional pairs.

This is intentionally different from earlier PAB-BGRL, which used one
node-level prealignment weight shared by both positive directions.

## Implementation

Worker-local code changes only:

- `/root/autodl-tmp/IDEA-CREATOR-workerB/baselines/BGRL/train_npg_transductive.py`
- `/root/autodl-tmp/IDEA-CREATOR-workerB/baselines/BGRL/reproduce_npg.py`

No main-thread files under `/root/autodl-tmp/IDEA-CREATOR` were edited by this
worker.

## GPU / Evaluation Protocol

All training runs used `--device=auto` and resolved to `cuda`. Encoder
training and representation extraction therefore used GPU. The reported
node-classification numbers are canonical CPU sklearn logistic-regression
probe numbers from the existing evaluation path. No GPU/PyTorch fast linear
probe was used in this worker result.

## Commands

```bash
python reproduce_npg.py --datasets=cora,chameleon --variants=puab_soft,puab_hard --splits=0 --epochs=5 --eval_epochs=5 --device=auto --output_dir=runs/puab_smoke_workerB_20260622 --clean
python reproduce_npg.py --datasets=cora,citeseer,chameleon --variants=bgrl_control,puab_soft,puab_hard --splits=0 --epochs=200 --eval_epochs=20 --device=auto --output_dir=runs/puab_m1_split0_workerB_20260622 --clean
```

Primary CSV:

`/root/autodl-tmp/IDEA-CREATOR-workerB/baselines/BGRL/runs/puab_m1_split0_workerB_20260622/results.csv`

## Smoke

| Dataset | Variant | Device | Test@Best | NaN | Collapse |
|---|---|---|---:|---:|---:|
| Cora | `puab_soft` | cuda | 0.772497 | 0 | 0 |
| Cora | `puab_hard` | cuda | 0.772497 | 0 | 0 |
| Chameleon | `puab_soft` | cuda | 0.396930 | 0 | 0 |
| Chameleon | `puab_hard` | cuda | 0.396930 | 0 | 0 |

Smoke passed engineering checks.

## Split-0 200-Epoch Gate

| Dataset | BGRL control | `puab_soft` | `puab_hard` | Best delta vs BGRL | Required reference | Decision |
|---|---:|---:|---:|---:|---:|---|
| Cora | 0.833410 | 0.832026 | 0.829257 | -0.001384 | LIFT 0.842640 | fail / slight damage |
| CiteSeer | 0.692712 | 0.691585 | 0.688580 | -0.001127 | LIFT 0.725770 | fail / slight damage |
| Chameleon | 0.438596 | 0.414474 | 0.418860 | -0.019737 | Positive-Path 0.725877 | fail |

## Diagnostics

| Dataset | Variant | Abstain ratio | Pair utility mean | Target consistency | Pair loss mean | Effective rank |
|---|---|---:|---:|---:|---:|---:|
| Cora | `puab_soft` | 0.676145 | 0.373067 | 0.750423 | 0.402035 | 196.147 |
| Cora | `puab_hard` | 0.451440 | 0.476043 | 0.750307 | 0.406367 | 196.693 |
| CiteSeer | `puab_soft` | 0.763451 | 0.348844 | 0.748240 | 0.408796 | 213.148 |
| CiteSeer | `puab_hard` | 0.452510 | 0.468478 | 0.747975 | 0.416230 | 213.700 |
| Chameleon | `puab_soft` | 0.516030 | 0.437959 | 0.837664 | 0.322461 | 168.085 |
| Chameleon | `puab_hard` | 0.453448 | 0.514877 | 0.837523 | 0.327514 | 169.150 |

No NaN or representational collapse occurred. The failure is methodological:
the pair-utility gate removes or downweights many positive pairs but does not
identify a task-useful subset. On homophilous Cora/CiteSeer it slightly harms
standard BGRL, and on Chameleon it falls below even the weak BGRL control.

## Decision

`FAILED_SPLIT0_GATE`. Do not run 10-split expansion or external baselines for
PUAB-GCL. Do not integrate into the main thread as an active method.

The pair-level abstention direction is only worth revisiting if the utility is
derived from a stronger independent signal, such as a fixed LIFT/Positive-Path
teacher or a calibrated raw-identity-preserving branch. The current
online-target pair loss / target-consistency gate is not enough.
