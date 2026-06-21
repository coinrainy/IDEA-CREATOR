# Refinement Report

**Problem**: graph self-supervised learning positive targets can become trivial under message passing.
**Initial Approach**: SRLP-GCL with `Z - alpha PZ` residual latent prediction.
**Date**: 2026-06-21
**Rounds**: 2
**Final Score**: 7.35 / 10
**Final Verdict**: READY for pilot.

## Output Files

- Initial proposal: `refine-logs/round-0-initial-proposal.md`
- Round-0 method review: `refine-logs/round-0-method-review.md`
- Raw round-1 review archive: `refine-logs/round-1-review.md`
- Round-1 refinement: `refine-logs/round-1-refinement.md`
- Round-1 method review: `refine-logs/round-1-method-review.md`
- Round-2 review archive: `refine-logs/round-2-review.md`
- Review summary: `refine-logs/REVIEW_SUMMARY.md`
- Final proposal: `refine-logs/FINAL_PROPOSAL.md`
- Score history: `refine-logs/score-history.md`

## Score Evolution

| Round | Problem Fidelity | Method Specificity | Contribution Quality | Frontier Leverage | Feasibility | Validation Focus | Venue Readiness | Overall | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 7 | 6 | 5 | 6 | 7 | 7 | 4 | 5.95 | REVISE |
| 2 | 8 | 8 | 7 | 7 | 7 | 8 | 5 | 7.35 | READY for pilot |

## Final Proposal Snapshot

- Final method name: SRLP.
- Core target: rank-1 context-projected residual teacher latent.
- Core isolation: target features are masked and every target incident edge is removed in the online branch.
- Core loss: residual cosine prediction plus optional variance floor.
- Implementation target: `baselines/BGRL` small variant.

## Method Evolution Highlights

1. Replaced `Z - alpha PZ` with `Z - q q^T Z`, where `q` is the visible context teacher-latent direction.
2. Removed conditional InfoNCE, learned alpha, structural predictor scalars, rank-k projection, and covariance regularization from v1.
3. Added explicit go/kill diagnostics: residual energy, prediction cosine, embedding rank, skipped target ratio, full-latent and `Z-PZ` controls.

## Pushback / Drift Log

| Reviewer Said | Author Response | Outcome |
|---|---|---|
| Add no LLM/VLM/Diffusion/RL. | Accepted; no external modern component is added. | Preserved focus. |
| `Z-PZ` looks like high-frequency filtering. | Accepted; target is now visible-context projection residual. | Major risk reduced. |
| Conditional InfoNCE distracts from contribution. | Accepted; removed from v1. | Contribution narrowed. |
| Hard target isolation may make task too hard. | Accepted as empirical risk; pilot must monitor diagnostics and may try two-hop only as diagnostic. | Ready for pilot, not paper-ready. |

## Remaining Weaknesses

- No empirical result yet.
- Rank-1 context projection may be too weak or too hard to predict.
- If warmup is needed, no-warmup ablation is mandatory.
- If full-latent target beats SRLP in pilot, the route should be killed or demoted instead of adding modules.

## Next Steps

1. Implement BGRL-based SRLP pilot.
2. Run Cora + Chameleon split 0 with full-latent, `Z-PZ`, SRLP, and no-isolation controls.
3. If positive, run Actor/Chameleon/Squirrel split 0 before any full 10-split experiment.
