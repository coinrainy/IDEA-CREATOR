# Latest Experiment Results

**Last updated**: 2026-06-22  
**Current candidate**: LIFT-PROP-GCL remains active after novelty check, but only with caution  
**Decision**: proceed to compact refinement and direct PROPGCL-facing validation; not paper-ready yet.

## Latest Update: LIFT-PROP Selector v1

Fixed K2 was revised into a plateau-aware selector:

```text
if lift(P^2X) < 0.35: K=0
elif lift(P^2X) <= lift(PX) + 0.02: K=1
else: K=2
```

On Actor/Squirrel fast-grid 10-split, v1 matches oracle on both:

| Dataset | Selected K | Selected test | Oracle K | Oracle test |
|---|---:|---:|---:|---:|
| Actor | 0 | 0.347566 | 0 | 0.347566 |
| Squirrel | 1 | 0.520365 | 1 | 0.520365 |

Across current observed datasets/settings, v1 matches oracle on 7/8, with Cora
as the only near miss. Full report:
`refine-logs/LIFT_PROP_SELECTOR_V1_RESULTS_20260622.md`.

## Latest Update: LIFT-PROP Extra Validation

LIFT-PROP was extended beyond the original five datasets. Cornell 10-split is
complete; Actor/Squirrel were checked on split 0 because the full 10-split run
was too slow under the current linear-eval grid.

| Dataset | Protocol | Gate choice | Gate result | Oracle K | Decision |
|---|---|---:|---:|---:|---|
| Cornell | 10 splits | K=0 | 0.816216 +/- 0.059487 | 0 | hit |
| Actor | split 0 | K=0 | 0.348684 | 0 | hit |
| Squirrel | split 0 | K=2 | 0.571566 | 2 | hit |
| Actor | 10 splits fast grid | K=0 | 0.347566 | 0 | hit |
| Squirrel | 10 splits fast grid | K=2 | 0.509030 | 1, 0.520365 | near miss; still above raw |

Full report: `refine-logs/LIFT_PROP_EXTRA_VALIDATION_20260622.md`.

## Latest Update: LIFT-PROP-GCL Novelty Check

Direct novelty review gives LIFT-PROP-GCL `5.5/10`, verdict
`PROCEED_WITH_CAUTION`. The closest prior is PROPGCL, which already establishes
training-free propagation as a strong GCL mechanism. Related risks include
GNNEvaluator / When Do GNNs Help for label-free graph-help estimation, GLANCE
for label-free homophily routing, Less is More for graph/raw dual views, ASPECT
for adaptive spectral GCL, and GRAPHITE for feature-node graph transformation.

Defensible delta: a very simple label-free edge-lift statistic for raw-vs-`P^2X`
abstention, matching the oracle choice on 4/5 pilot datasets and solving the
Chameleon/WebKB tradeoff. Full report:
`refine-logs/LIFT_PROP_NOVELTY_CHECK_20260622.md`.

## Latest Update: LIFT-PROP-GCL M0

LIFT-PROP-GCL reframes the post-GDC search around graph-view reliability. The
proxy tests raw features, deterministic propagation `P^K X`, and feature-token
propagation. The key gate is label-free:

```text
if lift(P^2 X) = mean_edge_cos(P^2 X) - mean_random_pair_cos(P^2 X) >= 0.35:
    use P^2 X
else:
    use raw X
```

| Dataset | K2-gate choice | K2-gate result | Oracle result | Decision |
|---|---:|---:|---:|---|
| Cora split-0 | K=2 | 0.826488 | K=3, 0.835256 | near miss |
| CiteSeer split-0 | K=2 | 0.709617 | K=2, 0.709617 | hit |
| Chameleon 10-split | K=2 | 0.685746 +/- 0.021187 | K=2, 0.685746 | hit |
| Texas 10-split | K=0 | 0.829730 +/- 0.051042 | K=0, 0.829730 | hit |
| Wisconsin 10-split | K=0 | 0.839216 +/- 0.043157 | K=0, 0.839216 | hit |

Verdict: `ACTIVE_WITH_NOVELTY_RISK`. Full report:
`refine-logs/LIFT_PROP_M0_RESULTS_20260622.md`.

## Latest Update: GDC-GCL+ M0-M1

GDC-GCL+ tested whether dynamic positives based on gradient-residual learning
directions can recover the earlier TD-GCL signal while giving a cleaner novelty
claim. The implementation is stable, but the split-0 effect is not strong
enough.

| Dataset | BGRL control | TD direction | GDC residual | Best delta vs control | Decision |
|---|---:|---:|---:|---:|---|
| Cora | 0.833410 | 0.830180 | 0.830641 | -0.002769 | fail |
| CiteSeer | 0.693464 | 0.694591 | 0.691210 | +0.001127 | too small / TD only |
| Chameleon | 0.438596 | 0.438596 | 0.442982 | +0.004386 | weak |
| Texas | 0.621622 | - | 0.621622 | +0.000000 | tie |
| Wisconsin | 0.549020 | - | 0.549020 | +0.000000 | tie |

No NaN/collapse occurred. Verdict: `FAILED_SPLIT0_GATE`. Full report:
`refine-logs/GDC_M0_M1_RESULTS_20260622.md`.

## Latest Update: SC-BGRL M0-M1

SC-BGRL tested fixed same-compatible / different-compatible graph views. After
fixing the sign split to use rank rather than a value threshold, the fair
split-0 result was not positive:

| Dataset | Control | SC | Delta | Decision |
|---|---:|---:|---:|---|
| Cora | 0.832487 | 0.828334 | -0.004153 | fail |
| Chameleon | 0.438596 | 0.436404 | -0.002193 | fail |
| Texas | 0.621622 | 0.621622 | +0.000000 | tie |
| Wisconsin | 0.549020 | 0.549020 | +0.000000 | tie |

Verdict: `FAILED_FIXED_SIGN_PILOT`. Move to GDC-GCL+. Full report:
`refine-logs/SCBGRL_M0_M1_RESULTS_20260622.md`.

## Latest Update: NPG-GCL M0-M2

NPG-GCL tested whether positive alignment should be weighted by nontrivial gain
over message-passing prealignment. It is stable but only weakly positive.

| Dataset | Control | NPG | Delta | Decision |
|---|---:|---:|---:|---|
| Cora | 0.830641 | 0.834333 | +0.003692 | weak positive |
| CiteSeer | 0.692712 | 0.691210 | -0.001503 | weak negative |
| Chameleon | 0.438596 | 0.442982 | +0.004386 | weak positive |
| Texas | 0.621622 | 0.621622 | +0.000000 | tie |
| Wisconsin | 0.549020 | 0.549020 | +0.000000 | tie |

Ablations do not support promotion: on Cora, random weighting reaches
`0.838948`, above NPG `0.834333`; on Chameleon, NPG `0.442982` beats uniform
`0.438596` and random `0.429825`, but the gain is too small.

Verdict: `WEAK_SIGNAL_DEPRIORITIZED`. Move to SC-BGRL. Full report:
`refine-logs/NPG_M0_M2_RESULTS_20260622.md`.

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
