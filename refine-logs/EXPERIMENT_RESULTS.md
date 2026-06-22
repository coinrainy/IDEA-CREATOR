# Latest Experiment Results

**Last updated**: 2026-06-22  
**Current candidate**: none ready  
**Decision**: RSP-GCL is downgraded to diagnostic-only after M2-M4 gates; DCA/VST/CIG/CLEAR remain stopped as main methods.

## Latest Update: RSP M2-M4 Gate

RSP-GCL completed the required Chameleon 10-split training, WebKB raw-protection
gate, and direct novelty check. It has a real Chameleon role-signature signal,
but it is not broad or novel enough for a 2026 paper-level main method.

| Gate | Result | Decision |
|---|---:|---|
| Chameleon 10-split RSP training, `role_fused_test@best` | 0.573684 +/- 0.026265 | positive |
| Chameleon validation-selected gate | 0.574781 +/- 0.023321 | selects role in 10/10 |
| Texas RSP training, raw / graph_raw / graph_raw_role | 0.829730 / 0.759459 / 0.727027 | role hurts |
| Texas validation-selected gate | 0.827027 vs raw 0.829730 | protects raw, no gain |
| Wisconsin RSP training, raw / graph_raw / graph_raw_role | 0.839216 / 0.807843 / 0.774510 | role hurts |
| Wisconsin validation-selected gate | 0.827451 vs raw 0.839216 | partial protection, no gain |

Novelty boundary: GALE already centers node equivalence in self-supervised graph
learning, WLGCL directly uses WL structural similarity for GCL positive
sampling, and SPGCL shows positive-sample GCL is an active 2026 area. RSP is
kept as a diagnostic baseline, not an active paper route.

## Current Best Evidence

| Candidate | Key setting | Result | Decision |
|---|---|---:|---|
| TD-GCL | Cora split-0, lambda_dyn 0.5 vs no-dyn | 0.842640 vs 0.807107 | speculative positive |
| TD-GCL | CiteSeer split-0, lambda_dyn 0.5 vs no-dyn | 0.729527 vs 0.712622 | speculative positive |
| TD-GCL | Chameleon split-0, lambda_dyn 0.2/0.5 vs no-dyn | 0.478070 vs 0.467105 | weak positive |
| TD-GCL | Texas/Wisconsin split-0 | no gain vs no-dyn and below raw | not broad |
| RSP role signature | Chameleon 10-split zero-training proxy | 0.585965 +/- 0.026073 | diagnostic lead |
| RSP-GCL train | Chameleon 10-split, 200 epoch, role-fused | 0.573684 +/- 0.026265 | diagnostic-only |
| RSP validation gate | Texas/Wisconsin selected vs raw | 0.827027 / 0.827451 vs 0.829730 / 0.839216 | no broad gain |
| RSP role signature | Texas/Wisconsin 10-split full role proxy | 0.678378 / 0.719608 vs raw 0.829730 / 0.839216 | gate required |
| DCA `dca_h1_p4` | Chameleon 10-split, RFA 1000 checkpoints | 0.505044 +/- 0.022791 | current best lead |
| DCA `dca_h1_h4_p4` | Chameleon 10-split, RFA 1000 checkpoints | 0.505044 +/- 0.019908 | current best lead |
| DCA `dca_h1_half_p4_half` | Chameleon 10-split, RFA 1000 checkpoints | 0.503070 +/- 0.021266 | positive |
| FBA `graph+raw+0.5H1` | Chameleon 10-split, same checkpoints | 0.500219 +/- 0.020769 | diagnostic |
| RFA `graph+raw` | Chameleon 10-split, same checkpoints | 0.496711 +/- 0.022175 | baseline |
| FBA-high1 train | Chameleon 10-split, 1000 epoch | 0.487061 +/- 0.025714 | fail |
| SBN-GCL | Chameleon split 0 fused | 0.462719 | fail |
| Semantic kNN anchor proxy | split-0 rescue probe | no decisive heterophily win | fail |
| ZCA/whitening proxy | split-0 rescue probe | timed out at 120s | fail |
| VST-GCL default | Cora/Chameleon/Texas/Wisconsin split 0, 200 epoch | Chameleon fused 0.469298; Texas/Wisconsin below raw | fail |
| VST-GCL low auxiliary | Cora/Chameleon split 0, 200 epoch | Chameleon fused 0.467105 | fail |
| CIG/CLEAR edge masks | Texas/Wisconsin 10-split counterfactual edge evaluator | validation-selected masks still below raw | fail |

Detailed reports:

```text
refine-logs/FBA_M0_M2_RESULTS_20260622_1115.md
refine-logs/SBN_DCA_RESULTS_20260622_1335.md
refine-logs/RSP_ROLE_SIGNATURE_RESULTS_20260622.md
refine-logs/RSP_M2_M4_RESULTS_20260622.md
refine-logs/TDGCL_M0_M1_RESULTS_20260622.md
```

## TD-GCL

TD-GCL uses training-dynamics positives: nodes are positives when their current
embedding update directions are similar under BGRL training.

| Dataset | No Dynamics | Best Dynamics | Delta | Decision |
|---|---:|---:|---:|---|
| Cora | 0.807107 | 0.842640 | +0.035533 | positive split-0 |
| CiteSeer | 0.712622 | 0.729527 | +0.016905 | positive split-0 |
| Chameleon | 0.467105 | 0.478070 | +0.010965 | weak positive |
| Texas | 0.756757 | 0.756757 | +0.000000 | no gain; below raw |
| Wisconsin | 0.803922 | 0.803922 | +0.000000 | no gain; below raw |

No NaN/collapse was observed. TD-GCL is `SPECULATIVE_INCUBATE`, not
`READY_TO_REFINE`; it needs multi-seed/split homophily validation, WebKB
reliability gating, and a direct novelty check before any expansion.

## RSP-GCL

RSP-GCL uses role/WL/landmark signatures to define nonlocal role-equivalent positives for graph contrastive learning.

### Chameleon 10-Split Role-Signature Proxy

| Representation | Mean Test | Std | Decision |
|---|---:|---:|---|
| `raw` | 0.456798 | 0.017763 | weak |
| `graph_raw` | 0.496711 | 0.022175 | baseline |
| `raw_role` | 0.501316 | 0.020993 | small positive |
| `graph_raw_role` | 0.546930 | 0.021334 | positive |
| `graph_raw_wl` | 0.578290 | 0.025837 | positive |
| `graph_raw_role_wl` | 0.583333 | 0.020431 | positive |
| `graph_raw_role_wl_landmark` | 0.585965 | 0.026073 | best fixed |

### RSP-GCL 200-Epoch Split-0 Training

| Dataset | Graph Test@Best | Fused Test@Best | Role-Fused Test@Best | Raw | Decision |
|---|---:|---:|---:|---:|---|
| Chameleon | 0.429825 | 0.478070 | 0.596491 | 0.440789 | positive |
| Texas | 0.648649 | 0.783784 | 0.702703 | 0.810811 | gate required |
| Wisconsin | 0.568627 | 0.803922 | 0.725490 | 0.823529 | gate required |

No NaN/collapse was observed. RSP-GCL should continue only through Chameleon 10-split training plus a role gate that protects Texas/Wisconsin raw baselines.

## DCA-GCL

DCA keeps deterministic anchors outside training and fuses them after the graph contrastive encoder is learned.

### Chameleon 10-Split

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

### Cora / CiteSeer Fixed Split

| Dataset | GraphRaw | Best fixed anchor | Test | Decision |
|---|---:|---|---:|---|
| Cora | 0.812183 | `fba_p4` | 0.841717 | positive |
| CiteSeer | 0.706236 | `dca_h1_p4` | 0.732532 | positive |

### Texas / Wisconsin 10-Split

| Dataset | Raw | GraphRaw | Best DCA/FBA family | Decision |
|---|---:|---:|---:|---|
| Texas | 0.829730 | 0.751351 | `fba_h1` 0.770270 | raw dominates |
| Wisconsin | 0.839216 | 0.792157 | `fba_h1` 0.827451 | raw dominates |

## SBN-GCL

SBN-GCL used semantic kNN positives and low-similarity edge boundary negatives.

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

Verdict: stop SBN.

## Previous Routes

| Route | Final decision |
|---|---|
| SRLP / SRLP-Aux / Adaptive-Aux | invalidated as main method by 10-split and fair pilot evidence |
| DCGCL | failed Chameleon/Texas 10-split despite Wisconsin signal |
| FTDR | stable but no positive effect |
| CFR | stable but feature channel forgot raw signal |
| RFA | keep as strong baseline and diagnostic |
| ORFA | stable but not enough; below raw/RFA where it matters |
| BiFilter-BGRL | naive trainable low/high branch failed |
| FBA-GCL training auxiliary | failed Chameleon 10-split |

## DCA Novelty Check

DCA novelty score is `3/10`. Closest prior work includes ASPECT, FC-GSSL, LOHA, HLCL, Less is More, FB-GCL, and GCL-GroW/GWGCL. DCA should stay as a diagnostic/simple baseline, not a main method.

## Semantic Anchor Rescue Proxy

The quick semantic kNN anchor tested `S X`, `X-SX`, and graph/raw/semantic concatenations on split 0.

| Dataset | Best relevant semantic-anchor result | Key control | Decision |
|---|---:|---:|---|
| Cora | `graph_raw_sem16_p4` 0.840332 | DCA/FBA best 0.841717 | no improvement |
| CiteSeer | `graph_raw_sem16_p4` 0.735913 | low2 0.738167 | no improvement |
| Chameleon | `graph_raw_sem16_sh` 0.508772 | graph_raw split-0 0.513158 | no improvement |
| Texas | `raw_sem16` 0.783784 | raw 0.810811 | fail |
| Wisconsin | best semantic family 0.823529 | raw 0.823529 | tie only |

Verdict: do not promote semantic anchors.

## VST-GCL

VST-GCL implemented a sparse local feature-topology transport target. It was stable, but did not produce a usable method signal.

| Dataset | Graph Test@Best | Fused Test@Best | Raw | Decision |
|---|---:|---:|---:|---|
| Cora | 0.804338 | 0.814490 | 0.659437 | weak; below prior anchor controls |
| Chameleon | 0.405702 | 0.469298 | 0.440789 | fail |
| Texas | 0.621622 | 0.729730 | 0.810811 | fail |
| Wisconsin | 0.549020 | 0.803922 | 0.823529 | fail |

Low-auxiliary ablation (`lambda_bgrl=1.0`, `lambda_transport=0.1`) also failed:

| Dataset | Graph Test@Best | Fused Test@Best | Raw | Decision |
|---|---:|---:|---:|---|
| Cora | 0.808030 | 0.810337 | 0.659437 | no improvement |
| Chameleon | 0.410088 | 0.467105 | 0.440789 | fail |

Report:

```text
refine-logs/VST_M0_M1_RESULTS_20260622.md
```

## CIG/CLEAR Counterfactual Edge Diagnostic

CIG/CLEAR tested whether counterfactual edge masks could rescue the graph branch before implementing a training objective.

Split-0:

| Dataset | Best counterfactual fused | Original fused | Key control | Decision |
|---|---:|---:|---:|---|
| Cora | 0.812183 | 0.812183 | prior anchors ~0.84 | no signal |
| Chameleon | 0.513158 | 0.513158 | DCA/graph_raw similar | no signal |
| Texas | 0.783784 | 0.729730 | raw 0.810811 | fail |
| Wisconsin | 0.843137 | 0.784314 | raw 0.823529 | local positive |

The Wisconsin split-0 positive did not hold as a method-level result:

| Dataset | Raw 10-split | Best fixed mask | Validation-selected mask | Decision |
|---|---:|---:|---:|---|
| Texas | 0.829730 | 0.794595 | 0.805405 | fail |
| Wisconsin | 0.839216 | 0.823529 | 0.827451 | fail |

Report:

```text
refine-logs/CIG_EDGE_COUNTERFACTUAL_RESULTS_20260622.md
```

## Next Required Run

Restart idea discovery with a genuinely different mechanism family. Do not locally tune DCA, VST, CIG, or CLEAR.
