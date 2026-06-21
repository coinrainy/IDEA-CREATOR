# Pipeline Summary

**Problem**: GCL node classification under heterophily.  
**Final Method Thesis**: NFR-GCL learns node-wise routing over low/mid/high frequency views so each node receives the contrastive signal appropriate to its local homophily/heterophily structure.  
**Final Verdict**: READY_TO_PILOT  
**Date**: 2026-06-21  

## Final Deliverables

- Idea report: `idea-stage/IDEA_REPORT.md`
- Proposal: `refine-logs/FINAL_PROPOSAL.md`
- Review summary: `refine-logs/REVIEW_SUMMARY.md`
- Experiment plan: `refine-logs/EXPERIMENT_PLAN.md`
- Experiment tracker: `refine-logs/EXPERIMENT_TRACKER.md`

## Contribution Snapshot

- **Dominant contribution**: Node-local frequency routing for graph contrastive learning.
- **Supporting contribution**: Label-free edge/local compatibility features as router inputs.
- **Explicitly rejected complexity**: Standalone hard-negative method, BGRL+filter paper, graph transformer/tokenized route.

## First Runs to Launch

1. Chameleon split0 sanity run for NFR-GCL.
2. Actor/Chameleon/Squirrel official 10-split decisive pilot.
3. Routing ablations only if the decisive pilot passes.

## Main Risks

- **Novelty risk**: Looks like PolyGCL/HLCL plus gate. Mitigation: strong router ablations.
- **Empirical risk**: No pilot yet. Mitigation: strict go/no-go threshold.
- **Variance risk**: Heterophily small datasets are noisy. Mitigation: official 10 splits and paired split analysis.

## Next Action

Proceed to implementation of NFR-GCL in the PolyGCL baseline.

