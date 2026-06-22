# Cycle-Balance R104/R105 Ablations

**Date**: 2026-06-22
**Status**: `DOWNGRADE_REFRAME_REQUIRED`
**Code**: `baselines/BGRL/evaluate_cycle_balance_proxy.py`
**Protocol**: CUDA tensor propagation / signed-path construction, canonical CPU sklearn final probe

## Question

R102/R103 showed a strong Chameleon gain for `cycle_gate_signed_all`, but the
mechanism claim was still uncertain. R104/R105 tested whether the gain came
from a true signed/balance-theory signal or from simpler propagation-channel
augmentation.

## R104: Component Ablations

### Chameleon 10-Split Fast Grid

| Variant | Dim | Pos ratio | Test mean | Test std | Delta vs portfolio |
|---|---:|---:|---:|---:|---:|
| portfolio | 2325 | 1.0 | 0.655482 | 0.019790 | - |
| cycle_gate_signed_all | 13950 | 1.0 | 0.708114 | 0.017032 | +0.052632 |
| cycle_gate_signed1 | 6975 | 1.0 | 0.706579 | 0.020902 | +0.051096 |
| cycle_gate_pos1 | 4650 | 1.0 | 0.706579 | 0.020902 | +0.051096 |
| cycle_gate_balance2 | 9300 | 1.0 | 0.674781 | 0.015300 | +0.019298 |
| cycle_gate_balanced2 | 4650 | 1.0 | 0.675877 | 0.017538 | +0.020395 |
| cycle_gate_diff2 | 4650 | 1.0 | 0.675877 | 0.017538 | +0.020395 |
| cycle_gate_neg1 | 4650 | 1.0 | 0.655482 | 0.019790 | +0.000000 |
| cycle_gate_unbalanced2 | 4650 | 1.0 | 0.655482 | 0.019790 | +0.000000 |

### Chameleon Split-0 Full Grid

| Variant | Dim | Pos ratio | Test |
|---|---:|---:|---:|
| portfolio | 2325 | 1.0 | 0.699561 |
| cycle_gate_signed_all | 13950 | 1.0 | 0.717105 |
| cycle_gate_balance2 | 9300 | 1.0 | 0.708333 |
| cycle_gate_signed1 | 6975 | 1.0 | 0.706140 |
| cycle_gate_pos1 | 4650 | 1.0 | 0.706140 |
| cycle_gate_balanced2 | 4650 | 1.0 | 0.703947 |

The attempted 10-split full-grid focused component sweep was interrupted after
more than 14 minutes without producing a first row. The bottleneck was the
canonical CPU sklearn linear probe, not CUDA tensor construction. This is
recorded as an evaluation-cost limitation, not a method failure.

## R105: Sign Controls

The original `cosine` sign rule used a median threshold and `>= threshold`.
For Chameleon this degenerates:

```text
edge_threshold = 0.0
pos_ratio = 1.0
```

Therefore the original strongest `cycle_gate_signed_all` result has no
negative-edge channel in practice. It is closer to appending self-loop-free
positive one-hop and two-hop path channels than to a signed structural-balance
mechanism.

### Chameleon 10-Split Fast Grid

| Sign mode | Pos ratio | Test mean | Test std | Interpretation |
|---|---:|---:|---:|---|
| cosine | 1.000000 | 0.708114 | 0.017032 | all-positive degenerate best |
| global_shuffle | 1.000000 | 0.708114 | 0.017032 | identical because all signs are positive |
| node_shuffle | 1.000000 | 0.708114 | 0.017032 | identical because all signs are positive |
| random | 0.499320 | 0.642763 | 0.021696 | random same-dim channels fail |
| rank | 0.500000 | 0.685526 | 0.018728 | true 50/50 sign split is only moderate |
| rank_node_shuffle | 0.500000 | 0.667105 | 0.023250 | preserving node sign-degree loses most gain |
| rank_global_shuffle | 0.500000 | 0.645395 | 0.020286 | shuffled edge signs fail |

## Decision

Cycle-Balance as a signed/balance-theory paper idea is **not supported**.

Supported evidence:

- The strong R102/R103 Chameleon result is real under the current evaluation
  protocol.
- The gain is not due to arbitrary random same-dimensional channels.
- The strongest component is effectively positive/no-self one-hop propagation
  plus a smaller positive/no-self two-hop complement.

Unsupported evidence:

- The original result does not demonstrate a true signed-edge or
  balanced/unbalanced-cycle mechanism, because the cosine threshold degenerates
  to all-positive edges on Chameleon.
- A forced rank-based 50/50 signed split is weaker and does not exceed the
  previously observed full-grid portfolio baseline.
- The novelty delta against signed GCL becomes much weaker, while the remaining
  mechanism is close to fixed propagation/path-feature baselines.

## Recommendation

Downgrade Cycle-Balance from active main-method candidate to
`POSITIVE_PATH_BASELINE_NOT_MAIN_METHOD`.

The next main-method search should keep the following lesson:

1. LIFT-style gates are useful for protecting raw/stack-dominant graphs.
2. Chameleon benefits from self-loop-free positive path channels.
3. A paper-level method must add a genuinely new training or selection
   principle beyond fixed propagation channel concatenation.

