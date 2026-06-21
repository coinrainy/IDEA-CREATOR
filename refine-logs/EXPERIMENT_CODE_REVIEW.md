# Experiment Code Review: SRLP 4060 Pilot

**Date**: 2026-06-21
**Mode**: Codex subagent review
**Reviewer agent**: Fermat (`019eea57-fdd1-7922-b7ac-0b9771425912`)
**Original verdict**: PASS_WITH_FIXES
**Post-fix status**: PASS for pilot use

## Subagent Findings

### Blocking Issues

None. The reviewer found that the core SRLP formula, teacher stop-gradient, `T_valid`, `epsilon`, `skipped_ratio`, sparse `ZPZ`, hard/NoIso branches, label-based evaluation, and leakage-probe definition were broadly aligned with the plan.

### Non-Blocking Issues

1. `GCNConv` implicitly adds self-loops, which weakens the strict reading of `A_online[i,j]=0 if i in T or j in T`.
2. `results.csv` lacked split path/counts, epoch/mask/epsilon settings, and outer project commit.
3. Nested BGRL `commit_sha` alone was not enough because the nested repo is dirty.
4. CiteSeer fixed split had not yet been pre-generated.
5. `dataset.capitalize()` would map `citeseer` to `Citeseer`, which is not ideal cross-platform.

## Fixes Applied

- Added `GCN(add_self_loops=...)` while preserving the default behavior for existing BGRL code.
- SRLP pilot scripts now build `GCN(add_self_loops=False)` and add explicit self-loops:
  - clean teacher/eval graphs: all-node self-loops;
  - hard-isolated online graph: non-target self-loops only;
  - NoIso graph: all-node self-loops.
- Added a hard/noiso self-loop isolation check and verified it passes.
- Expanded `results.csv` with `split_path`, train/val/test counts, epoch settings, mask settings, epsilon, nested commit, and outer project commit.
- Pre-generated both Cora and CiteSeer fixed 1:1:8 split files.
- Replaced `dataset.capitalize()` with explicit `{"cora": "Cora", "citeseer": "CiteSeer"}` mapping.

## Verification After Fixes

- `python -m py_compile` passed for SRLP scripts and modified model/util files.
- Hard isolation edge check passed: target nodes have no incident edges or self-loops in online hard mode.
- M0 rerun passed on Cora and Chameleon.
- Chameleon 200-epoch 5-variant M1 rerun completed.
- Leakage probe rerun preserved the expected direction: hard probe cosine `0.27185`, NoIso probe cosine `0.63130`.

## Overall

The implementation is acceptable for pilot experiments. It is still not paper evidence until Cora/CiteSeer M1 and the next Chameleon/heterophily decision gates are completed.
