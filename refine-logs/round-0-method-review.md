# SRLP-GCL Round-0 Method Review

Date: 2026-06-21

Verdict: REVISE.

Weighted overall score: 5.95 / 10.

Scores:
- Problem Fidelity: 7
- Method Specificity: 6
- Contribution Quality: 5
- Frontier Leverage: 6
- Feasibility: 7
- Validation Focus: 7
- Venue Readiness: 4

Core review conclusion:
SRLP-GCL has a plausible and compact problem framing, but the current method is
not yet reviewer-proof. The residual target `Z - alpha PZ` is still too easy to
read as graph high-pass filtering, which creates direct novelty pressure against
ASPECT and SPGCL. The first revision should make the residual target explicitly
"context-unpredictable" rather than merely "neighbor-subtracted", strengthen
target leakage control, and remove or demote conditional InfoNCE from the main
method.

Top revision priorities:
1. Redefine the residual target as the component of the teacher latent that is
   not predictable from the allowed masked context, preferably with a fixed or
   deterministic projection/gate rather than a learned alpha that can collapse
   back to the raw teacher target.
2. Make target masking stricter: mask target features, remove all incident
   target edges in the online branch for the first pilot, and compute any
   compatibility/statistical conditioning without access to the target raw
   feature.
3. Keep the first implementation minimal in the existing BGRL-style harness:
   residual cosine prediction plus optional light variance regularization only;
   move conditional InfoNCE, structural scalars, and learned alpha to later
   ablations if the core residual target works.

Implementation note:
The existing `baselines/BGRL` code already has an online encoder, EMA target
encoder, predictor, transductive training entry, and heterophily fixed-split
evaluation path. A low-cost pilot is realistic if SRLP-GCL is implemented as a
small BGRL variant. Conditional negative mining or memory-bank sampling would
materially increase implementation and debugging cost.
