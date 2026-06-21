# Gap Map

_Field gaps with stable IDs._
# Research Gap Map

**Updated**: 2026-06-21T08:39:08Z

## G1: Node-local frequency routing is missing in GCL

- **Status**: unresolved
- **Summary**: Existing graph contrastive learning methods usually apply global augmentation, global filtering, or dataset-level assumptions. AF-GCL and HLCL show that frequency matters, but the current design space still lacks a node-level mechanism that decides when a node should be aligned through low-pass signals, high-pass signals, identity signals, or their mixture.
- **Evidence**: Local results show PolyGCL dominates many heterophily datasets, while BGRL dominates homophily datasets but collapses on heterophily. This suggests one graph-level objective is not enough.
- **Linked papers**: paper:wang2022_augmentationfree_graph_contrastive, paper:yang2023_graph_contrastive_learning, paper:thakoor2021_largescale_representation_learning
- **Candidate ideas**: I1, I4, I16

## G2: Edge compatibility is not separated from edge existence

- **Status**: unresolved
- **Summary**: Most GCL view constructors either keep/drop edges or reconstruct masked edges as binary structure. Heterophily needs a richer edge type: homophilic-compatible, heterophilic-compatible, and noisy/non-informative.
- **Evidence**: GRASS performs strongly on Cornell/Texas/Wisconsin through masked-edge reconstruction, while GCA's centrality-based edge dropping is weaker on heterophily. This points to edge semantics rather than edge presence alone.
- **Linked papers**: paper:zhu2020_graph_contrastive_learning, paper:yang2023_graph_contrastive_learning
- **Candidate ideas**: I2, I6

## G3: Hard negatives need heterophily-aware safeguards

- **Status**: unresolved
- **Summary**: Recent contrastive learning theory emphasizes negative similarity distributions and hard negatives, but node classification on heterophilous graphs has a false-negative/false-positive trap: connected different-label nodes can be useful structure, and distant similar-label nodes may be positives.
- **Evidence**: 2025 contrastive similarity work suggests negative-pair variance matters; Khan-GCL uses hard negatives, but the local benchmark needs node-level safeguards tied to graph compatibility.
- **Linked papers**: paper:lee2025_similarities_embeddings_contrastive, paper:wang2025_khangcl_kolmogorovarnold_network
- **Candidate ideas**: I11, I12, I14

## G4: Homophily performance is near saturated, heterophily is the main method opportunity

- **Status**: unresolved
- **Summary**: Cora/CiteSeer/Amazon-Photo have several methods within roughly one point, while heterophily datasets show large spreads between PolyGCL/GRASS and classic GCL. A publishable method should anchor on heterophily gains and use homophily only as a no-regression check.
- **Evidence**: Best local heterophily methods are PolyGCL or GRASS; classic GRACE/GCA/DGI often trail substantially.
- **Linked papers**: paper:yang2023_graph_contrastive_learning
- **Candidate ideas**: I1, I6, I11

## G5: Strong ideas must be testable inside the existing baseline harness

- **Status**: unresolved
- **Summary**: The project already has reproducible scripts and official splits. A useful idea should require small edits to PolyGCL, GRASS, GCA/GRACE, or BGRL rather than a new graph transformer stack or new modality.
- **Evidence**: Many cells are already OOM/TODO on a 12GB local GPU; methods requiring new large-scale training or text encoders are not fair first-pass candidates.
- **Linked papers**: paper:chen2024_leveraging_contrastive_learning
- **Candidate ideas**: I1, I6, I11, I16

## G6: Positive alignment can be trivialized by message passing

- **Status**: unresolved
- **Summary**: Recent 2026 work argues that ordinary positive sample maximization in graph contrastive learning may be made too easy by message passing. A new GCL method should avoid targets that are already recoverable by simple neighborhood smoothing.
- **Evidence**: SPGCL analyzes this issue from the perspective of Dirichlet energy. This motivates predictive targets that remove the low-information smoothed component before contrastive alignment.
- **Linked papers**: paper:shan2026_revisiting_positive_samples, paper:thakoor2021_largescale_representation_learning
- **Candidate ideas**: SRLP-GCL
