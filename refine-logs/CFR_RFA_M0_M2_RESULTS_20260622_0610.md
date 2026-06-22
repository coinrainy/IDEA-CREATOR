# CFR / RFA Results

**Date**: 2026-06-22  
**Methods**: CFR-BGRL and RFA-BGRL  
**Protocol**: BGRL small-graph harness; Geom-GCN official splits for heterophily datasets  

## CFR-BGRL

CFR-BGRL used a graph GCN channel and an MLP feature channel with a light redundancy penalty. It was intended to preserve feature/topology complementarity without FTDR-style target routing.

### CFR Split-0

| Dataset | CFR Test@Best | Best local control | Delta | Raw diagnostic | Decision |
|---|---:|---:|---:|---:|---|
| Cora | 0.8002 | 0.8090 | -0.0088 | raw 0.6594 | fail |
| Chameleon | 0.4079 | 0.4232 | -0.0154 | raw 0.4408 | fail |
| Texas | 0.6486 | 0.6486 | +0.0000 | raw 0.8108 | tie |
| Wisconsin | 0.5294 | 0.5882 | -0.0588 | raw 0.8235 | fail |

No NaN/collapse occurred. The learned feature channel had very high feature cosine, but it did not preserve the raw-feature class signal. CFR is therefore deprioritized.

## Raw-Feature Diagnostic

Before RFA, a linear probe on non-trained features showed:

| Dataset | Raw X | One-hop mean | Raw + one-hop |
|---|---:|---:|---:|
| Cora | 0.6594 | 0.7951 | 0.7748 |
| Chameleon | 0.4408 | 0.4298 | 0.4254 |
| Texas | 0.8108 | 0.6757 | 0.7838 |
| Wisconsin | 0.8235 | 0.6078 | 0.8039 |

Interpretation: on Texas/Wisconsin and partly Chameleon, the raw node feature space already contains strong label signal. Several SSL variants were damaging this signal instead of retaining it.

## RFA-BGRL Implementation

Added:

- `baselines/BGRL/train_rfa_transductive.py`
- `baselines/BGRL/evaluate_rfa_anchor_scales.py`
- `rfa` variant in `baselines/BGRL/reproduce_dcgcl.py`

RFA trains a standard BGRL graph branch and evaluates a feature-retentive final representation:

```text
z_final = normalize([normalize(z_graph) || alpha normalize(x_raw)])
```

It also logs graph-only and raw-only probes in the same row.

## RFA Split-0 Gate

| Dataset | RFA 200 Test@Best | Raw-only | Graph-only | Strict reference | Decision |
|---|---:|---:|---:|---:|---|
| Cora | 0.8094 | 0.6594 | 0.8094 | BGRL 0.8090 | pass/tie |
| Chameleon | 0.4671 | 0.4408 | 0.4123 | strict 1000-epoch control about 0.5004 | partial |
| Texas | 0.7297 | 0.8108 | 0.6216 | 0.6135 | pass, raw-driven |
| Wisconsin | 0.7843 | 0.8235 | 0.5686 | 0.6039 | pass, raw-driven |

Chameleon 1000-epoch split-0 improved to `0.5022`, suggesting the graph branch needs longer training there.

## RFA 10-Split Gate

### 200 Epoch, Chameleon/Texas/Wisconsin

| Dataset | RFA mean | RFA std | Raw mean | Graph mean | Strict reference | Wins/Ties/Losses vs reference |
|---|---:|---:|---:|---:|---:|---:|
| Chameleon | 0.4682 | 0.0199 | 0.4568 | 0.4022 | 0.5004 | 0/0/10 |
| Texas | 0.7622 | 0.0397 | 0.8297 | 0.6027 | 0.6135 | 10/0/0 |
| Wisconsin | 0.8098 | 0.0430 | 0.8392 | 0.5294 | 0.6039 | 10/0/0 |

### Chameleon 1000 Epoch

| Dataset | RFA mean | RFA std | Raw mean | Graph mean | Strict reference | Wins/Ties/Losses |
|---|---:|---:|---:|---:|---:|---:|
| Chameleon | 0.4928 | 0.0230 | 0.4568 | 0.4397 | 0.5004 | 3/0/7 |

## Anchor Scale Sweep

Re-evaluating the final 200-epoch checkpoints across anchor scales showed dataset-dependent preferences:

| Dataset | Best final-checkpoint scale | Best mean | Raw mean | Graph mean |
|---|---:|---:|---:|---:|
| Chameleon | 1 | 0.4776 | 0.4568 | 0.4048 |
| Texas | 8 | 0.8378 | 0.8297 | 0.6000 |
| Wisconsin | 4 or 8 | 0.8451 | 0.8392 | 0.5157 |

Validation-selected scale gives Texas `0.8162` and Wisconsin `0.8471`, but Chameleon remains `0.4675`. This confirms that fixed fusion is not enough and that the next method needs a principled anchor-weight mechanism.

## Zero-Training ORFA Sanity

A post-hoc ORFA-style residualization was tested on existing RFA checkpoints by subtracting the component of the graph embedding aligned with a 256-dimensional random projection of the raw anchor, then concatenating the residual graph vector with the full raw anchor. This does **not** solve the problem:

- Chameleon 200-epoch final-checkpoint best scale remains around `0.4737`.
- Chameleon 1000-epoch validation-selected scale reaches only `0.4943`, still below the strict prior control around `0.5004`.
- Texas/Wisconsin remain strong mainly because the raw anchor dominates at high scales.

Interpretation: ORFA cannot be a post-hoc representation trick. If pursued, the complementary residual must be part of the training objective.

## Decision

RFA-BGRL is the strongest current empirical clue, but not yet a sufficient 2026 paper method:

- Positive: stable; no NaN/collapse; huge gains over prior GCL-style controls on Texas/Wisconsin; improves over both raw and graph branches on Chameleon.
- Negative: Texas/Wisconsin gains are mostly raw-feature retention; Chameleon still narrowly misses the strict strong control after 10 splits; novelty is close to recent GCN-MLP / SimMLP-style work.

Next action: keep RFA as a required baseline and move the main method to **ORFA-GCL**, where the raw feature anchor is protected and the graph branch is explicitly forced to learn complementary residual information.
