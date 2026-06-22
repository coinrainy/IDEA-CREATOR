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
- **NFR-GCL: Node-Frequency Routed Graph Contrastive Learning**: ABANDONED / ARCHIVED. After a novelty scan on 2026-06-21, the idea was judged too close to recent node-level adaptive spectral fusion work for graph contrastive learning.
## Key Papers (14 total)
- [paper:chen2024_leveraging_contrastive_learning] Leveraging Contrastive Learning for Enhanced Node Representations in Tokenized Graph Transformers: _TODO: fill in after reading._
- [paper:hou2023_graphmae2] GraphMAE2: A Decoding-Enhanced Masked Self-Supervised Graph Learner
- [paper:lee2025_similarities_embeddings_contrastive] On the Similarities of Embeddings in Contrastive Learning: _TODO: fill in after reading._
- [paper:li2026_aspect] ASPECT: Node-Level Adaptive Spectral Fusion for Graph Contrastive Learning
- [paper:shan2026_revisiting_positive_samples] Revisiting Positive Samples in Graph Contrastive Learning: From the Perspective of Message Passing
- [paper:skenderi2023_graph_jepa] Graph-level Representation Learning with Joint-Embedding Predictive Architectures
- [paper:srinivasan2025_predict_cluster_refine] Predict, Cluster, Refine: A Joint Embedding Predictive Self-Supervised Framework for Graph Representation Learning
- [paper:thakoor2021_largescale_representation_learning] Large-Scale Representation Learning on Graphs via Bootstrapping: _TODO: fill in after reading._
- [paper:wang2022_augmentationfree_graph_contrastive] Augmentation-Free Graph Contrastive Learning with Performance Guarantee: _TODO: fill in after reading._
- [paper:wang2025_khangcl_kolmogorovarnold_network] Khan-GCL: Kolmogorov-Arnold Network Based Graph Contrastive Learning with Hard Negatives: _TODO: fill in after reading._
- [paper:yang2023_graph_contrastive_learning] Graph Contrastive Learning under Heterophily via Graph Filters: _TODO: fill in after reading._
- [paper:zhu2020_deep_graph_contrastive] Deep Graph Contrastive Representation Learning: _TODO: fill in after reading._
## Recent Relationships (26 total)
  idea:dcgcl --addresses_gap--> gap:G4
  idea:dcgcl --addresses_gap--> gap:G3
  idea:dcgcl --addresses_gap--> gap:G2
  idea:dcgcl --supersedes--> idea:srlp_gcl
  idea:dcgcl --inspired_by--> paper:li2026_aspect
  idea:dcgcl --inspired_by--> paper:yang2023_graph_contrastive_learning
  idea:dcgcl --inspired_by--> paper:shan2026_revisiting_positive_samples
  idea:dcgcl --inspired_by--> paper:zhuo2024_improving_graph_contrastive_learning
  idea:srlp_gcl --inspired_by--> paper:li2026_aspect
  idea:srlp_gcl --inspired_by--> paper:shan2026_revisiting_positive_samples
  idea:srlp_gcl --inspired_by--> paper:srinivasan2025_predict_cluster_refine
  idea:srlp_gcl --inspired_by--> paper:hou2023_graphmae2
  idea:srlp_gcl --inspired_by--> paper:skenderi2023_graph_jepa
  idea:srlp_gcl --inspired_by--> paper:thakoor2021_largescale_representation_learning
  idea:srlp_gcl --addresses_gap--> gap:G6
