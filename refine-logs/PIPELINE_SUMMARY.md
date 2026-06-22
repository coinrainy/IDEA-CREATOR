# Pipeline Summary: No Ready Candidate After RSP Gate

**Last updated**: 2026-06-22  
**Current status**: RSP-GCL is diagnostic-only after M2-M4; TD-GCL is speculative-incubate; no final paper method yet.

## Current Candidate

RSP-GCL, Role-Signature Positive Graph Contrastive Learning, was the active route after DCA, VST, and CIG/CLEAR stopped. It has now been downgraded after the required Chameleon 10-split training, WebKB gate, and novelty check.

Core mechanism:

- build role/WL/landmark signatures without labels;
- use signature similarity to create nonlocal role-equivalent positives;
- train a BGRL-style graph encoder with role-positive InfoNCE and role-anchor prediction;
- use a role branch only when a gate or validation selection says it helps.

## Main Evidence

| Setting | Result | Decision |
|---|---:|---|
| Chameleon 10-split proxy, full role signature | 0.585965 | strong positive |
| Chameleon 10-split graph_raw | 0.496711 | baseline |
| Previous DCA best | 0.505044 | surpassed by role proxy |
| Chameleon RSP train split-0 role-fused | 0.596491 | positive and stable |
| Chameleon RSP train 10-split role-fused | 0.573684 +/- 0.026265 | positive but diagnostic |
| Chameleon validation-selected RSP gate | 0.574781 +/- 0.023321 | role selected 10/10 |
| Texas full role proxy | 0.678378 vs raw 0.829730 | gate required |
| Wisconsin full role proxy | 0.719608 vs raw 0.839216 | gate required |
| Texas validation-selected RSP gate | 0.827027 vs raw 0.829730 | protects raw, no gain |
| Wisconsin validation-selected RSP gate | 0.827451 vs raw 0.839216 | partial protection, no gain |
| TD-GCL Cora split-0 | 0.842640 vs no-dyn 0.807107 | speculative positive |
| TD-GCL CiteSeer split-0 | 0.729527 vs no-dyn 0.712622 | speculative positive |
| TD-GCL WebKB split-0 | no gain and below raw | gating needed |

## Route Decisions

| Route | Decision |
|---|---|
| RSP-GCL | diagnostic-only after M2-M4 and novelty gate |
| TD-GCL | speculative incubate; homophily signal only |
| DCA-GCL | diagnostic-only after novelty fail |
| VST-GCL | stopped after split-0 proxy and low-aux ablation |
| CIG/CLEAR | stopped after counterfactual edge masks failed Texas/Wisconsin |
| SRLP / SRLP-Aux / Adaptive-Aux | stopped as main method |
| DCGCL | stopped after 10-split gate |
| FTDR / CFR / ORFA / BiFilter / FBA / SBN | stopped |
| RFA | keep as diagnostic baseline |

## Novelty Gate

RSP cannot claim generic structural-role or WL-positive GCL novelty. GALE
(ICML 2025) already centers node equivalence in self-supervised graph learning;
WLGCL directly builds GCL positives from WL structural similarity; SPGCL shows
positive-sample GCL is a crowded 2026 topic.

## Next Step

Keep TD-GCL as a small incubated route and continue idea discovery for a
broader mechanism. Do not expand TD-GCL to external baselines before novelty,
multi-seed/split robustness, and raw-dominant graph gating pass.
