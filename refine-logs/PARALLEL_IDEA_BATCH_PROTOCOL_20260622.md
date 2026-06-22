# Parallel Idea Batch Protocol

**Date**: 2026-06-22
**Purpose**: use idle GPU time to screen multiple graph contrastive learning
ideas in parallel without weakening result comparability.

## Policy

1. Use sub-agents for early-stage idea pilots, not final paper numbers.
2. Run at most 2 concurrent GPU workers on the current single-GPU machine by
   default. Small transductive graphs underuse GPU, but sklearn probes and data
   loading still consume CPU, so more workers can slow the queue down.
3. Each worker must use a distinct output directory and report exact commands.
4. Training and representation extraction should use `--device=auto` and
   confirm `device=cuda` in metrics.
5. Final node-classification probes remain the canonical CPU sklearn protocol.
6. Workers may use `--eval_backend=torch_gpu_fast` only for rough screening,
   and must clearly mark those results as screening-only. If a fast-probe run
   looks positive, it must be re-run with `--eval_backend=sklearn`.
7. A positive worker result must be re-run by the main thread in the canonical
   workspace before promotion to active method.
8. A failed worker result may be recorded as negative evidence if it includes
   commands, metrics, and no-NaN/no-collapse diagnostics.

## Current Parallel Batch

| Worker | Idea | Scope | Gate |
|---|---|---|---|
| A | Protected Ego-Path Complement BGRL | preserve standard self-loop/identity branch while adding no-self/path complement | Chameleon must clearly beat BGRL and not damage Cora/CiteSeer |
| B | Pair-Utility Calibrated / PU-Abstention GCL | calibrate or abstain positive pairs with label-free utility instead of node-loss weighting | Chameleon must clearly beat BGRL and Cora/CiteSeer must stay safe |

## Promotion Rule

Promote only if the worker result satisfies all of:

- no NaN/collapse;
- uses CUDA for training;
- Cora/CiteSeer are not meaningfully below BGRL;
- Chameleon improves meaningfully over BGRL;
- the method is not merely a restatement of LIFT-Portfolio, Positive-Path,
  RFM/feature masking, SPGCL/prealignment, or direct no-self BGRL.

Otherwise record it as `FAILED_SPLIT0_GATE`, `INTERNAL_SIGNAL_ONLY`, or
`NOVELTY_RISK_TOO_HIGH`.
