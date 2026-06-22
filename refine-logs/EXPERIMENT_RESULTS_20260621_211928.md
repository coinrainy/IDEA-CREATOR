# Initial Experiment Results: SRLP 4060 Small-Graph Pilot

**Date**: 2026-06-21
**Plan**: `refine-logs/EXPERIMENT_PLAN.md`
**Implementation base**: `baselines/BGRL`
**GPU**: NVIDIA GeForce RTX 4060 Laptop GPU, about 8GB VRAM.

## Implementation Status

- Added SRLP utilities, training entrypoint, sequential runner, and leakage probe under `baselines/BGRL/`.
- Installed `tensorboard` into the active Python environment; scripts still write JSON/CSV as primary outputs.
- Used no dense `N x N` matrix. `ZPZ` uses sparse message passing.
- Context and `PZ` now use undirected one-hop adjacency; Chameleon required this because the raw PyG edge index is highly directed.
- Applied Codex subagent review fixes: strict target self-loop isolation, expanded CSV traceability fields, pre-generated CiteSeer split, and fixed the CiteSeer dataset directory casing.

## M0 Smoke Results

| Dataset | Split | Test@Best | Skipped Ratio | Effective Rank | NaN | Collapse |
|---|---|---:|---:|---:|---|---|
| Cora | fixed 1:1:8 seed 0 | 0.76927 | 0.04613 | 154.69 | false | false |
| Chameleon | Geom-GCN split 0 | 0.41886 | 0.00879 | 100.37 | false | false |

## Chameleon 200-Epoch M1 Results

| Variant | Valid@Best | Test@Best | Prediction Cosine | Residual Norm | Skipped Ratio | Effective Rank |
|---|---:|---:|---:|---:|---:|---:|
| FullLatent-Iso | 0.41838 | 0.41886 | 0.62414 | 9.50410 | 0.02857 | 72.64 |
| ZPZ-Iso | 0.41564 | 0.40132 | 0.62868 | 8.91162 | 0.02857 | 65.33 |
| SRLP hard | 0.43073 | 0.42325 | 0.57322 | 8.08275 | 0.02857 | 67.72 |
| SRLP-NoIso | 0.43073 | 0.41886 | 0.58576 | 8.07344 | 0.02857 | 63.74 |
| BGRL | 0.42112 | 0.43860 | 0.67890 | 0.00000 | 0.00000 | 115.11 |

## Leakage Probe

| Variant | Probe Cosine | Probe MSE | Interpretation |
|---|---:|---:|---|
| SRLP hard | 0.27185 | 0.00362 | Lower probe signal, expected direction. |
| SRLP-NoIso | 0.63130 | 0.00236 | Higher probe signal, suggests incident-edge leakage is real. |

## Current Interpretation

- Implementation and output protocol are functional.
- Hard isolation appears to reduce leakage substantially on Chameleon.
- Short 200-epoch Chameleon downstream accuracy is target-family positive: SRLP beats `FullLatent-Iso`, `ZPZ-Iso`, and `SRLP-NoIso`, but does not beat BGRL.
- Next decision should use Cora/CiteSeer 200-epoch pilots and possibly Chameleon 1000-epoch extension before expanding to WebKB/Actor.

## Next Step

Run Cora and CiteSeer 200-epoch M1 variants, then decide whether Chameleon SRLP deserves a 1000-epoch extension.
