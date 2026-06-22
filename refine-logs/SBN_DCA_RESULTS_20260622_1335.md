# SBN-GCL / DCA-GCL Results

**Date**: 2026-06-22  
**Goal**: continue the research pipeline after FBA training failed, searching for a node-classification graph contrastive learning idea with stronger effect and enough novelty.

## Literature Boundary

The latest scan constrains the novelty space:

- SPGCL, 2026: revisits GCL positive samples and uses Dirichlet-energy-guided sampling.
- ASPECT, 2026: node-level adaptive low/high spectral fusion for GCL.
- FC-GSSL, 2026: frequency-corrupt graph SSL with high-frequency-biased corruption and contrastive alignment.
- BES, 2026: adaptive contrastive boundary embedding shaping.
- Less is More, 2025/2026: simple GCN-MLP graph contrastive learning.
- HLCL/GREET/SIGNA: existing heterophily-aware edge/filter/neighborhood GCL.

Therefore, frequency fusion, edge heterophily discrimination, and generic positive-sample redesign are not enough as novelty claims.

## SBN-GCL

SBN-GCL tested a different mechanism family:

```text
semantic positives = top-k raw-feature nearest neighbors
boundary negatives = graph edges with low raw-feature similarity
L = semantic multi-positive NCE + BGRL stability + boundary repulsion
```

Implementation:

- `baselines/BGRL/train_sbn_transductive.py`
- `baselines/BGRL/reproduce_dcgcl.py --variants sbn`

### M1 Split-0 Results

| Dataset | Graph Test@Best | Fused Test@Best | Raw | Decision |
|---|---:|---:|---:|---|
| Cora | 0.814490 | 0.820951 | 0.659437 | weak local positive |
| Chameleon | 0.394737 | 0.462719 | 0.440789 | fail |
| Texas | 0.621622 | 0.729730 | 0.810811 | fail |
| Wisconsin | 0.686275 | 0.784314 | 0.823529 | fail |

Chameleon ablations:

| Variant | Graph Test@Best | Fused Test@Best | Decision |
|---|---:|---:|---|
| no boundary loss | 0.410088 | 0.482456 | fail |
| `positive_k=64`, lower boundary weight | 0.410088 | 0.471491 | fail |

**Verdict**: stop SBN. The semantic-kNN and low-similarity-edge boundary objective is not a viable main route in this harness.

## DCA-GCL

DCA-GCL is a refined post-hoc/deferred-fusion hypothesis from FBA:

> Do not force the graph encoder to predict or align filter anchors during training. Train the graph contrastive encoder normally, then fuse complementary raw, low-pass, and high-pass anchors only at representation time.

This differs from failed FBA training: the filter anchors are kept complementary rather than collapsed into the learned graph branch.

Fixed candidate:

```text
z_dca = normalize([z_graph || X || 0.5*(X-PX) || P^4X])
```

### Chameleon 10-Split, RFA 1000 Checkpoints

| Representation | Mean Test | Std | Decision |
|---|---:|---:|---|
| `graph_raw` | 0.496711 | 0.022175 | baseline |
| `fba_h1` | 0.500219 | 0.020769 | edge positive |
| `fba_p4` | 0.500219 | 0.018697 | edge positive |
| `dca_h1_p4` | 0.505044 | 0.022791 | best fixed candidate |
| `dca_h1_h4_p4` | 0.505044 | 0.019908 | best fixed candidate |
| `dca_h1_half_p4_half` | 0.503070 | 0.021266 | positive |

CSV:

```text
baselines/BGRL/runs/dca_eval_chameleon10_20260622_1315/results.csv
```

### Texas / Wisconsin 10-Split, RFA 200 Checkpoints

| Dataset | Raw | GraphRaw | Best DCA/FBA family | Decision |
|---|---:|---:|---:|---|
| Texas | 0.829730 | 0.751351 | `fba_h1` 0.770270 | raw dominates |
| Wisconsin | 0.839216 | 0.792157 | `fba_h1` 0.827451 | raw dominates |

### Cora / CiteSeer Fixed Split

| Dataset | GraphRaw | Best fixed anchor | Test |
|---|---:|---|---:|
| Cora | 0.812183 | `fba_p4` | 0.841717 |
| CiteSeer | 0.706236 | `dca_h1_p4` | 0.732532 |

## Current Verdict

DCA-GCL is the strongest current empirical candidate but not yet paper-ready:

- positive: fixed Chameleon 10-split improves over graph_raw and previous FBA;
- positive: Cora/CiteSeer improve over graph_raw;
- negative: Texas/Wisconsin still raw-dominant;
- risk: novelty is weak because ASPECT, HLCL, FC-GSSL, Less is More, and SPGCL are close.

Do not run external baselines yet. The next necessary step is a novelty/method review:

1. Is deferred fusion, rather than training-time fusion/alignment, a defensible new contribution?
2. Can the paper claim be framed as a negative/diagnostic finding plus a simple robust baseline?
3. If positive-method objective remains mandatory, DCA needs a stronger mechanism beyond fixed concatenation.
