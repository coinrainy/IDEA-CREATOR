# Research Wiki Query Pack

_Auto-generated. Do not edit._

## Open Gaps
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
## Failed Ideas (avoid repeating)
- **Compatibility-Calibrated Contrastive Edges**: KILLED as standalone. Kept only as a routing signal inside NFR-GCL.
## Key Papers (8 total)
- [paper:chen2024_leveraging_contrastive_learning] Leveraging Contrastive Learning for Enhanced Node Representations in Tokenized Graph Transformers: _TODO: fill in after reading._
- [paper:lee2025_similarities_embeddings_contrastive] On the Similarities of Embeddings in Contrastive Learning: _TODO: fill in after reading._
- [paper:thakoor2021_largescale_representation_learning] Large-Scale Representation Learning on Graphs via Bootstrapping: _TODO: fill in after reading._
- [paper:wang2022_augmentationfree_graph_contrastive] Augmentation-Free Graph Contrastive Learning with Performance Guarantee: _TODO: fill in after reading._
- [paper:wang2025_khangcl_kolmogorovarnold_network] Khan-GCL: Kolmogorov-Arnold Network Based Graph Contrastive Learning with Hard Negatives: _TODO: fill in after reading._
- [paper:yang2023_graph_contrastive_learning] Graph Contrastive Learning under Heterophily via Graph Filters: _TODO: fill in after reading._
- [paper:zhu2020_deep_graph_contrastive] Deep Graph Contrastive Representation Learning: _TODO: fill in after reading._
- [paper:zhu2020_graph_contrastive_learning] Graph Contrastive Learning with Adaptive Augmentation: _TODO: fill in after reading._
## Recent Relationships (8 total)
  idea:compatibility_calibrated_edges --inspired_by--> paper:zhu2020_graph_contrastive_learning
  idea:node_local_bgrl --inspired_by--> paper:thakoor2021_largescale_representation_learning
  idea:heterophily_hard_negative_aux --addresses_gap--> gap:G3
  idea:heterophilous_edge_reconstruction --addresses_gap--> gap:G2
  idea:nfr_gcl --inspired_by--> paper:wang2022_augmentationfree_graph_contrastive
  idea:nfr_gcl --inspired_by--> paper:yang2023_graph_contrastive_learning
  idea:nfr_gcl --addresses_gap--> gap:G4
  idea:nfr_gcl --addresses_gap--> gap:G1
