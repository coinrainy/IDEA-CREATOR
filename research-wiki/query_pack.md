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
- [paper:chen2024_leveraging_contrastive_learning] Leveraging Contrastive Learning for Enhanced Node Representations in Tokenized Graph Transformers: GCFormer 用正负 token 序列和 contrastive learning 提升 tokenized graph Transformer 的节点表示。
- [paper:hou2023_graphmae2] GraphMAE2: A Decoding-Enhanced Masked Self-Supervised Graph Learner
- [paper:lee2025_similarities_embeddings_contrastive] On the Similarities of Embeddings in Contrastive Learning: 该文用 cosine similarity 统一分析 contrastive embeddings，并提出降低 mini-batch negative similarity 方差的辅助损失。
- [paper:li2026_aspect] ASPECT: Node-Level Adaptive Spectral Fusion for Graph Contrastive Learning
- [paper:shan2026_revisiting_positive_samples] Revisiting Positive Samples in Graph Contrastive Learning: From the Perspective of Message Passing
- [paper:skenderi2023_graph_jepa] Graph-level Representation Learning with Joint-Embedding Predictive Architectures
- [paper:srinivasan2025_predict_cluster_refine] Predict, Cluster, Refine: A Joint Embedding Predictive Self-Supervised Framework for Graph Representation Learning
- [paper:thakoor2021_largescale_representation_learning] Large-Scale Representation Learning on Graphs via Bootstrapping: BGRL 用 bootstrap prediction 替代负样本对比，在图表示学习中实现可扩展的自监督训练。
- [paper:wang2022_augmentationfree_graph_contrastive] Augmentation-Free Graph Contrastive Learning with Performance Guarantee: AF-GCL 用 GNN 聚合特征构造自监督信号，避免传统 graph augmentations 对高频异配信息的破坏。
- [paper:wang2025_khangcl_kolmogorovarnold_network] Khan-GCL: Kolmogorov-Arnold Network Based Graph Contrastive Learning with Hard Negatives: Khan-GCL 将 KAN encoder 与语义 hard negatives 结合，用于提升 graph-level contrastive representation。
## Recent Relationships (31 total)
  idea:dca_gcl --addresses_gap--> gap:G4
  idea:dca_gcl --addresses_gap--> gap:G3
  idea:dca_gcl --boundary_condition--> paper:shan2026_revisiting_positive_samples
  idea:dca_gcl --boundary_condition--> paper:li2026_aspect
  idea:dca_gcl --supersedes--> idea:dcgcl
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
