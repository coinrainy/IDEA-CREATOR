# Post-ORFA Idea Discovery: FBA-GCL

**Date**: 2026-06-22  
**Trigger**: ORFA-GCL failed to become the final method after RFA-BGRL exposed raw-feature retention as a strong diagnostic.

## Decision

Stop ORFA-GCL and BiFilter-BGRL as main routes.

Select **FBA-GCL: Filter-Bank Anchored Graph Contrastive Learning** for one focused gate.

## Why FBA

The current evidence shows that different datasets need different spectral regimes:

- Cora/CiteSeer: low-pass propagated features are strong (`P^2X`).
- Texas: high-order high-pass residual `X-P^4X` can exceed raw on split 0.
- Wisconsin/Cornell: raw features remain dominant.
- Chameleon: deterministic filters alone are weak, but learned graph embeddings plus raw plus a small filter anchor reach the strongest current signal.

Chameleon 10-split re-evaluation from existing RFA 1000 checkpoints:

| Representation | Mean Test | Std |
|---|---:|---:|
| `graph+raw` | 0.496711 | 0.022175 |
| `graph+raw+0.5H1` | 0.500219 | 0.020769 |
| `graph+raw+P4` | 0.500219 | 0.018697 |

## Scope

FBA is not a finished paper method. It is `ACTIVE_NEEDS_STRICT_GATE`.

The next step is a reusable fixed-family evaluator, then a frozen candidate gate on Cora/CiteSeer/Chameleon/Texas/Wisconsin. No large baseline expansion should run until that gate passes.

## Updated Entrypoints

- `idea-stage/IDEA_REPORT.md`
- `idea-stage/IDEA_CANDIDATES.md`
- `refine-logs/FINAL_PROPOSAL.md`
- `refine-logs/EXPERIMENT_PLAN.md`
- `refine-logs/EXPERIMENT_RESULTS.md`
- `refine-logs/EXPERIMENT_TRACKER.md`
- `refine-logs/ORFA_BIFILTER_FBA_RESULTS_20260622_0935.md`
