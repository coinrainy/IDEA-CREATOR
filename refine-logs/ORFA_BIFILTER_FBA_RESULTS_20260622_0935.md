# ORFA / BiFilter / FBA-GCL Gate Results

**Date**: 2026-06-22  
**Goal**: find a new graph contrastive learning method for node classification after SRLP, DCGCL, FTDR, CFR, and raw-anchor RFA failed to become final paper methods.  
**Protocol**: small transductive node classification first; heterophily datasets use Geom-GCN official fixed splits.

## Executive Decision

ORFA-GCL and the naive two-branch high-pass/low-pass BiFilter-BGRL are stopped.

The surviving candidate is **FBA-GCL: Filter-Bank Anchored Graph Contrastive Learning**. It combines a learned BGRL graph view with deterministic graph-filter anchors:

```text
P = normalized graph propagation
L_k = P^k X
H_k = X - P^k X
z_final = normalize([z_g || X || selected_filter_anchor])
```

Current status is `ACTIVE_NEEDS_STRICT_GATE`, not paper-ready. The strongest signal is Chameleon 10-split re-evaluation from existing RFA checkpoints:

| Representation | Chameleon 10-split mean Test | Std | Decision |
|---|---:|---:|---|
| `graph + raw` | 0.496711 | 0.022175 | RFA-level |
| `graph + raw + 0.5*H1` | 0.500219 | 0.020769 | edge positive |
| `graph + raw + P4` | 0.500219 | 0.018697 | edge positive |

CSV: `baselines/BGRL/runs/rfa_chameleon_filterbank_eval_20260622_0910.csv`

This is only a narrow positive signal. It justifies a focused FBA-GCL refinement, not a main-table expansion yet.

## ORFA-GCL Result

ORFA attempted to preserve the raw-feature anchor while training the graph branch as an orthogonal residual.

### Smoke

| Dataset | ORFA Test@Best | Scale | Graph | Residual | Raw | NaN/Collapse |
|---|---:|---:|---:|---:|---:|---|
| Cora | 0.778957 | 1 | 0.766960 | 0.762806 | 0.659437 | no/no |
| Chameleon | 0.475877 | 2 | 0.379386 | 0.377193 | 0.440789 | no/no |

### Split-0 200 Epoch

| Dataset | ORFA Test@Best | Graph | Residual | Raw | Decision |
|---|---:|---:|---:|---:|---|
| Cora | 0.816336 | 0.809875 | 0.810798 | 0.659437 | pass local |
| Chameleon | 0.458333 | 0.412281 | 0.418860 | 0.440789 | fail |
| Texas | 0.783784 | 0.621622 | 0.621622 | 0.810811 | below raw |
| Wisconsin | 0.823529 | 0.549020 | 0.588235 | 0.823529 | ties raw |

### Chameleon 1000 Epoch

| Dataset | ORFA Test@Best | Final Test | Graph | Residual | Raw | Decision |
|---|---:|---:|---:|---:|---:|---|
| Chameleon | 0.484649 | 0.493421 | 0.473684 | 0.456140 | 0.440789 | below RFA 1000 |

**Verdict**: stop. ORFA does not solve Chameleon, and Texas/Wisconsin still do not beat raw features.

## BiFilter-BGRL Result

BiFilter-BGRL used a low-pass GCN branch and a high-pass residual-feature MLP branch under the normal BGRL bootstrap loss.

Implementation:

- `baselines/BGRL/train_bifilter_transductive.py`
- `baselines/BGRL/reproduce_dcgcl.py` variant `bifilter`

### Split-0 200 Epoch

| Dataset | Fused Test@Best | Low Branch | High Branch | Decision |
|---|---:|---:|---:|---|
| Cora | 0.702815 | 0.788186 | 0.260729 | fail |
| Chameleon | 0.458333 | 0.440789 | 0.353070 | fail |
| Texas | 0.729730 | 0.675676 | 0.756757 | fail |
| Wisconsin | 0.666667 | 0.568627 | 0.686275 | fail |

**Verdict**: stop. A naive trainable high-pass branch is not enough; it harms homophily and does not fix heterophily.

## Training-Free Filter-Bank Diagnostic

Direct linear probes on deterministic graph-filtered features showed why FBA is worth keeping.

| Dataset | Best Useful Filter Signal | Test | Interpretation |
|---|---|---:|---|
| Cora | `P^2 X` | 0.834333 | low-pass filters are stronger than BGRL/RFA |
| CiteSeer | `P^2 X` | 0.738167 | same low-pass pattern |
| Chameleon | `raw + low/high filters` | 0.462719 | filter bank alone is weak, but complements learned graph view |
| Texas | `X - P^4 X` | 0.837838 | high-order high-pass can beat raw on split 0 |
| Wisconsin | raw `X` | 0.823529 | raw remains strongest on split 0 |
| Actor | `raw + H4` | 0.359211 | small positive over raw |
| Cornell | raw `X` | 0.675676 | raw remains strongest |

## Literature Boundary

FBA-GCL is close to recent simple graph SSL/GCL directions and must be positioned carefully:

- Less is More / simple GCN-MLP GCL: <https://arxiv.org/abs/2509.25742>
- SimMLP / self-supervised GNN-MLP alignment: <https://arxiv.org/abs/2412.03864>
- SPGCL / high Dirichlet energy positive learning: <https://arxiv.org/abs/2606.10284>
- GCL-OT / heterophilic structure-text alignment: <https://arxiv.org/abs/2511.16778>

The viable novelty is not "use raw and graph views." The defensible angle is:

> Graph contrastive encoders and raw features fail in different spectral regimes; deterministic low/high graph filters can serve as anchor views, and contrastive graph encoders should be calibrated against this filter bank instead of collapsing everything into same-node agreement.

## Next Gate

FBA-GCL should only continue if the next implementation satisfies all of:

1. Adds a reusable FBA evaluator/training script instead of ad hoc notebook-style probes.
2. Uses a fixed candidate family, not hand-selected per split after seeing test.
3. Beats or ties RFA on Chameleon 10-split and does not regress Cora/CiteSeer.
4. Beats raw-only or explains why Texas/Wisconsin should be reported as raw-dominant diagnostics rather than main wins.
5. Survives a novelty review against Less is More, SimMLP, and SPGCL.

Recommended minimal implementation:

```text
L = L_BGRL
  + lambda_anchor * (1 - cos(MLP(z_g), stopgrad(z_filter)))

z_filter in {P^2 X, P^4 X, X - P X, X - P^4 X}
z_final = normalize([z_g || X || beta z_filter])
```

The first fair test should use fixed `beta` values and validation-only selection inside a predeclared candidate set.
