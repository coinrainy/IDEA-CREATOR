# Reproduction Protocol

Updated: 2026-06-19

This document is the authoritative protocol for all runs in `baselines/`.
Do not infer split rules from a baseline source file when that conflicts with
the rules below; update this document first, then run experiments from it.

Implementation precedence: every baseline driver must implement the split and
aggregation rule documented here. Repository defaults, command-line defaults,
or data-loader defaults are not valid protocol evidence when they differ from
this file.

## Unified Repeat Count

Use **10 reproduction units** for every baseline-dataset result unless this
document defines a dataset-specific official multi-split protocol.

Report every final number as:

`mean ± std`

and record:

- `runs`: number of reproduction units.
- `seeds`: seed list or split IDs.
- `protocol`: split/evaluation protocol.
- `log`: raw log path.

## Seed List

Use this fixed seed list for random-split homophily datasets and any baseline requiring stochastic training seeds:

`[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`

Execution policy update (2026-06-18): run baseline experiments sequentially as a single training process at a time. Do not launch multiple baseline/seed jobs concurrently, even when GPU memory usage is low.
Strict single-thread update (2026-06-18): launch subsequent runs with CPU thread caps such as `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1`, and `TORCH_NUM_THREADS=1` unless a baseline cannot run correctly under those settings.

## Dataset Protocols

Important: **not every result uses 1:1:8 / 10/10/80**. Use the
dataset/baseline-specific rule below. Correction (2026-06-19): heterophily
datasets have their own official fixed-split protocol and must not be run with
random 1:1:8 splits. This also applies to PolyGCL.

| Dataset group | Repeat / split rule | Final aggregation |
|---|---|---|
| Default homophily protocol: Cora, CiteSeer, PubMed | 10 random 10/10/80 splits using seeds 0-9, full official training epochs each run, unless another row in this table names the dataset/baseline explicitly | mean±std over 10 runs |
| Default Amazon protocol: Amazon-Photo, Amazon-Computers | 10 random 10/10/80 splits using seeds 0-9, full official training epochs each run, unless another row in this table names the dataset/baseline explicitly | mean±std over 10 runs |
| PolyGCL on Cora/CiteSeer/PubMed | user override: 10 random 10/10/80 splits using seeds 0-9 | mean±std over 10 runs |
| BGRL Amazon-Photo/Amazon-Computers | paper BGRL 20/80 split protocol per seed, not 10/10/80 | mean±std over 10 seeds |
| Coauthor-CS | temporary exception: keep the completed one-round result only and defer remaining runs at the user's request. Do not launch Coauthor-CS for additional baselines until this exception is lifted. | report the single completed run separately; leave deferred cells marked `deferred-user-request` |
| Coauthor-Physics | 10 random 10/10/80 splits using seeds 0-9, full official training epochs each run | mean±std over 10 runs |
| Wiki-CS | use official WikiCS masks/splits, not random 10/10/80. If a method has stochastic training, train with seeds 0-9 and evaluate on official WikiCS splits. | primary: mean±std over 10 seed-level official-split means; also keep raw official-split logs |
| Actor, Chameleon, Squirrel, Cornell, Texas, Wisconsin | use the Geom-GCN official 10 public fixed splits from `baselines/dataset_splits/heterophily/geom-gcn/<dataset>_split_0.6_0.2_<0..9>.npz`, not random 10/10/80. Although the file names contain `0.6_0.2`, the public masks have the commonly used heterophily benchmark ratio of about 48/32/20 train/validation/test. Applies to every baseline, including PolyGCL. | mean±std over 10 official splits |

## Result Acceptance

A result is considered paper-style reproduced only if:

1. It uses the baseline paper/repository's official hyperparameters and full epoch count.
2. It follows the dataset protocol above.
3. It reports `mean±std` over the required 10 units, except Wiki-CS where official split masks are preserved.
4. The reproduced mean is close to the paper result, or any gap is explained in the log notes.

Smoke tests, single-seed runs, and official-pretrained single evaluations must not be entered as final reproduced results.
