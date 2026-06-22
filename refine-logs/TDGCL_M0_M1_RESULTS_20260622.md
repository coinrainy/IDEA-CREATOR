# TD-GCL M0-M1 Results

**Date**: 2026-06-22  
**Status**: `SPECULATIVE_INCUBATE`  
**Candidate**: TD-GCL, Training-Dynamics Graph Contrastive Learning  

## Idea

TD-GCL avoids static positive definitions such as edges, raw-feature kNN,
WL/role equivalence, filters, prototypes, and counterfactual edge masks.
During BGRL training it keeps an EMA memory of node embeddings and uses nodes
with similar embedding update directions as dynamic positives.

Core auxiliary:

```text
m_i^t = beta m_i^{t-1} + (1 - beta) stopgrad(z_i^t)
d_i^t = normalize(z_i^t - m_i^{t-1})
P_i^t = top-k nodes by cosine(d_i^t, d_j^t)
L_dyn = InfoNCE(z_i^t, m_j^{t-1}, positives=P_i^t)
L = L_BGRL + lambda_dyn L_dyn
```

## Implementation

New code:

```text
baselines/BGRL/train_tdgcl_transductive.py
baselines/BGRL/reproduce_dcgcl.py --variants tdgcl
```

Verification:

```text
python -m py_compile .\train_tdgcl_transductive.py .\reproduce_dcgcl.py
python .\reproduce_dcgcl.py --datasets chameleon --variants tdgcl --epochs 5 --eval_epochs 5 --dry_run --output_dir runs/tdgcl_dryrun
```

Both passed.

## M0 Smoke

CSV:

```text
baselines/BGRL/runs/tdgcl_m0_smoke_20260622/results.csv
```

5-epoch smoke on Cora and Chameleon completed with no runtime error, NaN, or
collapse. The dynamic loss is intentionally inactive during the 20-epoch warmup.

## M1 Split-0 Pilot

Main dynamic run:

```text
baselines/BGRL/runs/tdgcl_m1_split0_20260622/results.csv
```

Direct no-dynamics control:

```text
baselines/BGRL/runs/tdgcl_ablate_no_dyn_20260622/results.csv
```

Lambda 0.5 ablation:

```text
baselines/BGRL/runs/tdgcl_ablate_lambda05_20260622/results.csv
```

CiteSeer check:

```text
baselines/BGRL/runs/tdgcl_citeseer_ablate_20260622/results.csv
baselines/BGRL/runs/tdgcl_citeseer_lambda05_20260622/results.csv
```

| Dataset | No Dynamics | Dyn 0.2 | Dyn 0.5 | Best Delta | Best Graph | Raw | NaN/Collapse |
|---|---:|---:|---:|---:|---:|---:|---|
| Cora | 0.807107 | 0.838025 | 0.842640 | +0.035533 | 0.844024 | 0.659437 | 0/0 |
| CiteSeer | 0.712622 | n/a | 0.729527 | +0.016905 | 0.725394 | 0.670173 | 0/0 |
| Chameleon | 0.467105 | 0.478070 | 0.478070 | +0.010965 | 0.442982 | 0.440789 | 0/0 |
| Texas | 0.756757 | 0.756757 | 0.729730 | +0.000000 | 0.675676 | 0.810811 | 0/0 |
| Wisconsin | 0.803922 | 0.803922 | 0.803922 | +0.000000 | 0.568627 | 0.823529 | 0/0 |

## Interpretation

TD-GCL is not dead. It gives a clean split-0 dynamic-effect signal on Cora and
CiteSeer, and a small Chameleon gain over its own no-dynamics control.

It is also not paper-ready:

- gains are mostly homophily-side and currently evaluated on fixed split-0 only;
- Texas/Wisconsin still require raw fallback and show no method gain;
- Chameleon remains below the strongest role-signature/DCA diagnostic results;
- dynamic positive mining is not obviously unique, so novelty needs deeper
  checking against dynamic positive graph clustering, Graph Contrastive PU
  Learning, and adaptive augmentation / dynamic sampling GCL.

## Quick Novelty Boundary

Closest visible risks from the quick search:

- IFL-GCL, **InfoNCE is a Free Lunch for Semantically guided Graph Contrastive
  Learning** (SIGIR 2025 / arXiv:2505.06282), frames GCL as positive-unlabeled
  learning and uses InfoNCE-estimated semantic similarity to correct sampling
  bias.
- DGCL-PU, **Debiased graph contrastive learning based on positive and
  unlabeled learning** (IJMLC 2024), also addresses false negatives with PU
  learning.
- Dynamic positive mining appears in graph contrastive / graph clustering
  literature, usually based on representation similarity, thresholding, or
  retraining confidence.
- Dynamic-graph contrastive learning uses historical embeddings as samples, but
  targets evolving graphs rather than static node classification.

TD-GCL's current defensible delta is narrower: positives are mined from
**embedding update directions across training**, not from static representation
similarity, feature similarity, WL/role equivalence, or graph evolution events.
This is promising enough to incubate but not enough to claim novelty without a
deeper check.

Sources checked:

```text
https://arxiv.org/html/2505.06282v1
https://dl.acm.org/doi/abs/10.1145/3726302.3730007
https://www.researchgate.net/publication/376616057_Debiased_graph_contrastive_learning_based_on_positive_and_unlabeled_learning
https://dl.acm.org/doi/pdf/10.1145/3637528.3671777
```

## Decision

TD-GCL is `SPECULATIVE_INCUBATE`, not `READY_TO_REFINE`.

Next fair test if we keep it:

1. Run Cora/CiteSeer multi-seed or additional fixed splits if available.
2. Add a label-free reliability rule that disables dynamics on raw-dominant
   WebKB-style graphs before claiming generality.
3. Run a direct novelty check for training-trajectory positives in graph SSL.

Do not launch external baselines or large graphs yet.
