---
type: paper
node_id: paper:hou2023_graphmae2
title: "GraphMAE2: A Decoding-Enhanced Masked Self-Supervised Graph Learner"
year: 2023
venue: WWW
arxiv: "2304.04779"
url: "https://arxiv.org/abs/2304.04779"
---

# GraphMAE2

GraphMAE2 improves masked graph autoencoding with multi-view random re-mask decoding and latent representation prediction. It shows that predicting in embedding space can improve masked graph self-supervised learning.

## Relevance

This is a close prior for latent prediction on masked graphs. SRLP-GCL must avoid becoming a GraphMAE2 variant; it should not reconstruct raw features or full hidden states, and should emphasize residual targets designed to remove message-passing shortcuts.
