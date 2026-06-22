# DCGCL Experiment Code Review

**Date**: 2026-06-22  
**Review route**: local-only checklist. A secondary Codex reviewer was not used because no explicit subagent delegation was requested in this turn.

## Files Reviewed

- `baselines/BGRL/bgrl/dcgcl_utils.py`
- `baselines/BGRL/diagnose_dcgcl_prototypes.py`
- `baselines/BGRL/train_dcgcl_transductive.py`
- `baselines/BGRL/reproduce_dcgcl.py`

## Checklist

| Check | Verdict | Evidence |
|---|---|---|
| Implements proposal mechanism | PASS | Dual feature/propa teacher assignment, shared prototype bank, soft NCE, dual heads, disagreement gate. |
| Hyperparameters are argparse-controlled | PASS | prototypes, temperatures, loss weights, split/seed/epochs all exposed. |
| Evaluation uses ground-truth labels only in eval/diagnostics | PASS | Loss uses teacher assignments only; labels only in `evaluate_linear_split` and post-hoc NMI/ARI diagnostics. |
| Follows fixed split protocol | PASS | Reuses `load_dataset_and_split` from `srlp_utils.py`, including Geom-GCN official heterophily splits. |
| JSON/CSV outputs exist | PASS | Each script writes `metrics.json`, per-run `results.csv`, and aggregate `results_csv`. |
| Sanity path before full runs | PASS | `reproduce_dcgcl.py` supports `dcgcl_diag` and short epoch smoke before 200-epoch gates. |
| Known risk | NON-BLOCKING | Prototype identities use a shared bank over mixed teacher embeddings, slightly simpler than the proposal's separate `C_x/C_a`; this is acceptable for first pilot and should be documented as V0. |

## Changes After Review

- Changed default `proto_tau` from `0.2` to `0.05` after M0 diagnostics showed `0.2` produced near-zero confidence.
- Made dual soft-label loss expression explicit with `+` for readability.
