# Evaluation Backend Policy

**Date**: 2026-06-22

## Decision

For graph contrastive learning node-classification experiments in this project,
the canonical reported evaluation remains CPU sklearn logistic regression.

Reason: the current BGRL codebase and most historical project results use the
standard unsupervised-encoder + sklearn linear-probe protocol. Replacing this
with a GPU PyTorch classifier changes the optimizer, multi-class formulation,
and hyper-parameter behavior, so it would weaken comparability.

## GPU Usage

Use GPU for:

- model training;
- encoder forward / representation extraction;
- tensor propagation, feature construction, and proxy diagnostics;
- optional early screening with a clearly marked fast PyTorch probe.

Do not use GPU fast-probe numbers as final paper/table numbers unless they are
separately equivalence-validated against sklearn for the exact dataset and
split protocol.

## Implemented Switch

`baselines/BGRL/train_npg_transductive.py` now supports:

```bash
--eval_backend=sklearn          # default, canonical
--eval_backend=torch_gpu_fast   # screening-only PyTorch linear probe
```

`baselines/BGRL/reproduce_npg.py` passes the backend through and records
`eval_backend` in `results.csv`.

## Smoke Checks

Both checks used Cora split 0, 1 epoch, `device=cuda`.

| Backend | Command output | Interpretation |
|---|---:|---|
| `sklearn` | 0.792340 | canonical path still works |
| `torch_gpu_fast` | 0.759114 | optional fast path runs, but differs from sklearn |

The mismatch is expected because the PyTorch fast probe is not protocol-
equivalent to sklearn/liblinear. Therefore it is suitable only for rough
screening and queue triage.
