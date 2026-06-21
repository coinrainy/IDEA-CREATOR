# Baseline Code Snapshot

Pulled on 2026-06-18 for the required GCL node-classification baselines.

| Baseline | Local path | Source | PDF |
|---|---|---|---|
| DGI | `baselines/DGI` | https://github.com/PetarV-/DGI.git | `baselines/DGI/paper.pdf` |
| MVGRL | `baselines/MVGRL` | https://github.com/kavehhassani/mvgrl.git | `baselines/MVGRL/paper.pdf` |
| GRACE | `baselines/GRACE` | https://github.com/CRIPAC-DIG/GRACE.git | `baselines/GRACE/paper.pdf` |
| GCA | `baselines/GCA` | https://github.com/CRIPAC-DIG/GCA.git | `baselines/GCA/paper.pdf` |
| BGRL | `baselines/BGRL` | https://github.com/nerdslab/bgrl.git | `baselines/BGRL/paper.pdf` |
| PolyGCL | `baselines/PolyGCL` | https://github.com/ChenJY-Count/PolyGCL.git | `baselines/PolyGCL/paper.pdf` |
| GRASS | `baselines/GRASS` | https://github.com/YukunCai/GRASS.git | `baselines/GRASS/paper.pdf` |
| EPAGCL | `baselines/EPAGCL` | https://github.com/hyzhang98/EPAGCL.git | `baselines/EPAGCL/paper.pdf` |
| EDA-GCL | `baselines/EDA-GCL` | https://github.com/CCChen-GEEX/EDA-GCL.git | `baselines/EDA-GCL/paper.pdf` |

## Paper PDF Sources

| Baseline | PDF source |
|---|---|
| DGI | https://openreview.net/pdf/67df6b5ffbf0ef252ee5f21442c63f5a1bab1023.pdf |
| MVGRL | https://proceedings.mlr.press/v119/hassani20a/hassani20a.pdf |
| GRACE | https://arxiv.org/pdf/2006.04131.pdf |
| GCA | https://arxiv.org/pdf/2010.14945.pdf |
| BGRL | https://arxiv.org/pdf/2102.06514.pdf |
| PolyGCL | https://openreview.net/pdf?id=y21ZO6M86t |
| GRASS | https://www.ijcai.org/proceedings/2025/0393.pdf |
| EPAGCL | https://ojs.aaai.org/index.php/AAAI/article/download/35488/37643 |
| EDA-GCL | https://ojs.aaai.org/index.php/AAAI/article/download/39085/43047 |

## Not Pulled

| Baseline | Reason |
|---|---|
| AF-GCL | No confirmed public official implementation found for "Augmentation-Free Graph Contrastive Learning with Performance Guarantee". Do not confuse it with AFGRL. |
| GCL-JAM | The AAAI 2025 paper page and author homepage mention the paper, but no confirmed public code URL was found. |

## Required Datasets

Use two separate main tables. Do not mix random homophily splits with official heterophily fixed splits. The authoritative protocol is `baselines/reproduction_protocol.md`.

| Table | Dataset | Split / Protocol | Role |
|---|---|---|---|
| Homophily | Cora | random 10/10/80 | classic citation graph |
| Homophily | CiteSeer | random 10/10/80 | classic citation graph |
| Homophily | PubMed | random 10/10/80 | classic citation graph |
| Homophily | Amazon-Photo | random 10/10/80 | common recent GCL benchmark |
| Homophily | Amazon-Computers | random 10/10/80 | common recent GCL benchmark |
| Homophily | Coauthor-CS | random 10/10/80 | larger homophilic graph |
| Homophily | Coauthor-Physics | random 10/10/80 | larger homophilic graph |
| Homophily | Wiki-CS | official WikiCS 20 splits / masks | common GCL/BGRL benchmark; do not use random 10/10/80 |
| Heterophily | Actor | Geom-GCN official 10 fixed public splits in `baselines/dataset_splits/heterophily/geom-gcn/actor_split_0.6_0.2_<0..9>.npz`; masks are 3648/2432/1520, about 48/32/20 | standard heterophily benchmark |
| Heterophily | Chameleon | Geom-GCN official 10 fixed public splits in `baselines/dataset_splits/heterophily/geom-gcn/chameleon_split_0.6_0.2_<0..9>.npz`; masks are 1092/729/456, about 48/32/20 | standard heterophily benchmark |
| Heterophily | Squirrel | Geom-GCN official 10 fixed public splits in `baselines/dataset_splits/heterophily/geom-gcn/squirrel_split_0.6_0.2_<0..9>.npz`; masks are 2496/1664/1041, about 48/32/20 | standard heterophily benchmark |
| Heterophily | Cornell | Geom-GCN official 10 fixed public splits in `baselines/dataset_splits/heterophily/geom-gcn/cornell_split_0.6_0.2_<0..9>.npz`; masks are 87/59/37, about 48/32/20 | small heterophily benchmark |
| Heterophily | Texas | Geom-GCN official 10 fixed public splits in `baselines/dataset_splits/heterophily/geom-gcn/texas_split_0.6_0.2_<0..9>.npz`; masks are 87/59/37, about 48/32/20 | small heterophily benchmark |
| Heterophily | Wisconsin | Geom-GCN official 10 fixed public splits in `baselines/dataset_splits/heterophily/geom-gcn/wisconsin_split_0.6_0.2_<0..9>.npz`; masks are 120/80/51, about 48/32/20 | small heterophily benchmark |

Minimum required set: Cora, CiteSeer, PubMed, Amazon-Photo, Amazon-Computers, Coauthor-CS, Coauthor-Physics, Wiki-CS, Actor, Chameleon, Squirrel, Cornell, Texas, Wisconsin.

Optional datasets: DBLP, Crocodile, ogbn-arxiv, CoraFull, Reddit, ogbn-products. Use them only for dataset coverage, scalability, or special-setting experiments.
