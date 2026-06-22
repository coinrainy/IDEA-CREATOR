# Pipeline Summary: DCGCL Idea Discovery

**Problem**: 重新构思一个能在节点分类上提升的图对比学习方法。  
**Final Method Thesis**: 用 feature-only 与 propagation-view teacher 的原型一致/分歧构造任务相关软对比目标。  
**Final Verdict**: READY_TO_PILOT, not yet evidence-supported.  
**Date**: 2026-06-22

## Final Deliverables

- Idea report: `idea-stage/IDEA_REPORT.md`
- Candidate summary: `idea-stage/IDEA_CANDIDATES.md`
- Proposal: `refine-logs/FINAL_PROPOSAL.md`
- Experiment plan: `refine-logs/EXPERIMENT_PLAN.md`
- Experiment tracker: `refine-logs/EXPERIMENT_TRACKER.md`

## Contribution Snapshot

- **Dominant contribution**: disagreement-calibrated prototype contrast for node-level graph SSL。
- **Supporting contribution**: label-free diagnostics that decide whether feature/topology disagreement is task-relevant before running large pilots。
- **Explicitly rejected complexity**: LLM/text teacher, frequency routing, residual latent target, OGB-scale pretraining。

## Must-Prove Claims

- DCGCL improves split-0 node classification against BGRL/FullLatent/ZPZ/SRLP-Aux controls。
- The improvement comes from dual-teacher disagreement calibration, not ordinary pseudo-label contrast。

## First Runs to Launch

1. Prototype diagnostics on Cora/Chameleon/Texas/Wisconsin。
2. 5-epoch smoke on Cora and Chameleon。
3. 200-epoch split-0 Chameleon gate against BGRL/FullLatent/ZPZ/SRLP-Aux。

## Main Risks

- **Prototype noise**: if teacher assignments are label-irrelevant, kill early。
- **Novelty pressure**: HEATS/SPGCL/AFGRL/JPEB-GSSL are close; ablations must isolate disagreement calibration。
- **Small split variance**: do not claim method success before official 10-split gate。

## Next Action

Proceed to implementation only for M0/M1/M2 pilot, not full benchmark expansion.
