# Experiment Plan: RSP-GCL Gate

**Date**: 2026-06-22  
**Candidate**: RSP-GCL  
**Status**: `COMPLETED_DOWNGRADED`

## Goal

Determine whether RSP-GCL can become a real graph contrastive learning method rather than a Chameleon-only structural feature observation.

## Completed Gates

| Run ID | Gate | Result | Decision |
|---|---|---:|---|
| R039 | role-signature proxy split-0 | Chameleon full role `0.596491`; Texas/Wisconsin below raw | partial pass |
| R040 | Chameleon 10-split proxy | full role `0.585965` vs graph_raw `0.496711` | pass |
| R041 | RSP training split-0 | Chameleon role-fused `0.596491`; Texas/Wisconsin below raw | partial pass |
| R042 | Chameleon 10-split RSP training | role-fused `0.573684 +/- 0.026265`; no NaN/collapse | pass with scope limit |
| R043 | validation-selected representation gate | Chameleon `0.574781`; Texas/Wisconsin `0.827027` / `0.827451` below raw | partial fail |
| R044 | direct novelty check | GALE/WLGCL/SPGCL overlap | fail |

## Final Decision

RSP-GCL is downgraded to diagnostic-only. Do not run external baselines, large
graphs, or paper-table expansion for this candidate.

Next plan: restart idea discovery with a different mechanism family and keep
RSP role signatures as a diagnostic baseline.

## Next Required Runs

No RSP runs are required. The historical plan below is retained for traceability.

### R042: Chameleon 10-Split RSP Training

Purpose: verify that the training objective, not only the post-hoc role signature, works across official splits.

Command template:

```powershell
python .\reproduce_dcgcl.py `
  --datasets chameleon `
  --variants rsp `
  --splits 0,1,2,3,4,5,6,7,8,9 `
  --epochs 200 `
  --eval_epochs 50 `
  --output_dir runs/rsp_m2_chameleon10_20260622 `
  --clean
```

Pass condition:

- role-fused mean clearly above `graph_raw=0.496711` and DCA `0.505044`;
- no NaN/collapse;
- graph-only branch does not collapse to rank < 2.

### R043: Role Gate for Raw-Dominant Graphs

Purpose: avoid Texas/Wisconsin regressions.

Minimal gate:

```text
h_i(alpha) = [z_i || x_i || alpha S_i], alpha in {0, 1}
select alpha on validation split
```

Pass condition:

- Texas 10-split selected mean is not below raw by more than noise;
- Wisconsin 10-split selected mean is not below raw by more than noise;
- Chameleon still selects role on most splits and keeps the positive signal.

### R044: Direct Novelty Check

Search specifically for:

- WL-positive graph contrastive learning;
- structural-role positive samples in GCL;
- landmark diffusion / positional signatures as contrastive positive selectors;
- Str-GCL, CoRep, H3GNNs/HarmonyGNNs, structural encoder overlap.

Pass condition:

- novelty is at least medium with a defensible delta;
- closest prior work does not already combine role/WL/landmark positives with role-gated node classification.

## Stop Conditions

Stop RSP-GCL if:

- Chameleon 10-split training mean falls back near DCA or graph_raw;
- role gate cannot protect Texas/Wisconsin raw;
- novelty collapses to a direct prior.

Do not run external baselines or large graphs before R042-R044 pass.
