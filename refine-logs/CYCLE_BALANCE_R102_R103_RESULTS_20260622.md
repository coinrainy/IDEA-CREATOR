# Cycle-Balance Gated LIFT Results (R102/R103)

**Date**: 2026-06-22  
**Status**: `ACTIVE_CANDIDATE_WITH_NOVELTY_RISK`, not paper-ready  
**Code**: `baselines/BGRL/evaluate_cycle_balance_proxy.py`  
**Core control**: LIFT-Portfolio  
**Evaluation policy**: CUDA is used for protocol-equivalent tensor propagation and signed-path feature construction; final node-classification probes remain canonical CPU sklearn logistic regression.

## Method

Cycle-Balance Gated LIFT starts from LIFT-Portfolio. When the portfolio selects
`single_k2_low_raw_lift`, it induces signed edges from raw feature cosine on
observed graph edges:

```text
positive edge: cos(x_i, x_j) >= median edge cosine
negative edge: otherwise
```

It then constructs signed-path channels:

- `signed_pos1 = P_pos X`
- `signed_neg1 = P_neg X`
- `balanced2 = P_pos P_pos X + P_neg P_neg X`
- `unbalanced2 = P_pos P_neg X + P_neg P_pos X`
- `signed_diff2 = balanced2 - unbalanced2`

The strongest tested variant, `cycle_gate_signed_all`, concatenates these
channels with the portfolio representation only under the gate. When
LIFT-Portfolio selects stack/raw on other graphs, it falls back exactly to the
portfolio representation.

## Main Results

### Split-0 Five-Dataset Gate

| Dataset | Portfolio choice | Portfolio | Cycle balance2 | Cycle signed-all | Decision |
|---|---|---:|---:|---:|---|
| Cora | `stack_0123` | 0.842640 | 0.842640 | 0.842640 | protected |
| CiteSeer | `stack_0123` | 0.725770 | 0.725770 | 0.725770 | protected |
| Chameleon | `single_k2_low_raw_lift` | 0.699561 | 0.708333 | 0.717105 | positive |
| Texas | `raw_k0` | 0.810811 | 0.810811 | 0.810811 | protected |
| Wisconsin | `raw_k0` | 0.823529 | 0.823529 | 0.823529 | protected |

### Chameleon 10-Split

| Grid | Variant | Dim | Val mean | Test mean | Test std | Delta vs portfolio |
|---|---|---:|---:|---:|---:|---:|
| fast C `{-4,0,4}` | portfolio | 2325 | 0.655693 | 0.655482 | 0.019790 | - |
| fast C `{-4,0,4}` | cycle_gate_balance2 | 9300 | 0.674211 | 0.674781 | 0.015300 | +0.019298 |
| fast C `{-4,0,4}` | cycle_gate_signed_all | 13950 | 0.700823 | 0.708114 | 0.017032 | +0.052632 |
| full C `{-10..10}` | portfolio | 2325 | 0.679973 | 0.685526 | 0.021292 | - |
| full C `{-10..10}` | cycle_gate_signed_all | 13950 | 0.721948 | 0.725877 | 0.019174 | +0.040351 |

### Extra Heterophily Split-0 Scope Check

| Dataset | Portfolio choice | Portfolio | Cycle signed-all | Decision |
|---|---|---:|---:|---|
| Squirrel | `stack_0123` | 0.550432 | 0.550432 | protected |
| Actor | `raw_k0` | 0.346053 | 0.346053 | protected |
| Cornell | `raw_k0` | 0.648649 | 0.648649 | protected |

## Novelty Check

Manual novelty status: `PROCEED_WITH_CAUTION`, approximate score `5/10`.

Closest prior work:

| Paper | Link | Overlap | Difference |
|---|---|---|---|
| SGCL: Contrastive Representation Learning for Signed Graphs, CIKM 2021 | https://dl.acm.org/doi/10.1145/3459637.3482478 | signed graph contrastive learning, balance theory | works on native signed graphs; not feature-induced signs on ordinary unsigned node-classification graphs |
| SGCA: Signed Graph Contrastive Learning with Adaptive Augmentation, IJCNN 2024 | https://ieeexplore.ieee.org/document/10651025/ | adaptive signed graph augmentation and balance constraints | native signed graph setting; not LIFT-gated unsigned graph propagation feature channels |
| HLCL: Graph Contrastive Learning under Heterophily via Graph Filters, UAI 2024 | https://openreview.net/forum?id=khvJM3uFk8 | cosine-based heterophily handling and graph filters | filter/spectral GCL, not explicit signed balanced/unbalanced path channels |
| HeterGCL, IJCAI 2024 | https://www.ijcai.org/proceedings/2024/265 | heterophilic GCL with structural and semantic learning | broader learned heterophily GCL, not training-free signed-path LIFT gate |
| ASPECT / ASPECT-S, arXiv 2026 | https://arxiv.org/html/2604.01878v2 | adaptive spectral GCL for heterophily | node-wise spectral policy; no feature-induced structural-balance path construction |
| GCL-OT, AAAI 2026 | https://ojs.aaai.org/index.php/AAAI/article/view/39704 | recent heterophilic graph contrastive learning | text-attributed graph OT alignment, not ordinary feature-induced signed path channels |

Attempted external review through `mcp__claude_review.review` failed with a 403
quota error. Trace saved at:

```text
.aris/traces/novelty-check/2026-06-22_cycle_balance_run01/trace.md
```

## Interpretation

This is the first post-LIFT-Portfolio candidate with a meaningful 10-split
full-grid Chameleon gain while preserving Cora/CiteSeer/WebKB and extra
heterophily controls through the label-free gate.

However, the contribution is not yet paper-ready:

- It is still a deterministic proxy, not a trained contrastive objective.
- It has a strong Chameleon signal but only protection, not improvement, on
  Squirrel/Actor/Cornell in the current quick scope check.
- The signed/balance-theory literature is close enough that novelty must be
  framed narrowly and tested against signed-GCL and heterophily-GCL baselines.

## Required Next Steps

1. Run Chameleon ablations with full C grid:
   `portfolio_signed1`, `portfolio_balance2`, `portfolio_signed_all`, and
   threshold variants.
2. Run Squirrel/Actor/Cornell 10-split with fast grid to verify that protection
   is stable beyond split 0.
3. Implement a trained contrastive variant only if ablations show that signed
   balanced/unbalanced channels add more than generic high-dimensional
   concatenation.
4. Compare directly against HLCL/HeterGCL/ASPECT-style heterophily GCL and
   signed graph contrastive baselines where protocol permits.
5. Add a feature-induced sign randomization ablation: random sign split,
   degree-preserving sign shuffle, and cosine-threshold alternatives.

