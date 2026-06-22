# Research Wiki Log

_Append-only timeline._
- `2026-06-21T08:31:17Z` Wiki initialized
- `2026-06-21T08:38:37Z` ingest_paper: ingested paper:wang2022_augmentationfree_graph_contrastive (arxiv:2204.04874)
- `2026-06-21T08:38:37Z` ingest_paper: ingested paper:yang2023_graph_contrastive_learning (arxiv:2303.06344)
- `2026-06-21T08:38:37Z` ingest_paper: ingested paper:zhu2020_graph_contrastive_learning (arxiv:2010.14945)
- `2026-06-21T08:38:37Z` ingest_paper: ingested paper:zhu2020_deep_graph_contrastive (arxiv:2006.04131)
- `2026-06-21T08:38:37Z` ingest_paper: ingested paper:thakoor2021_largescale_representation_learning (arxiv:2102.06514)
- `2026-06-21T08:38:37Z` ingest_paper: ingested paper:chen2024_leveraging_contrastive_learning (arxiv:2406.19258)
- `2026-06-21T08:38:37Z` ingest_paper: ingested paper:lee2025_similarities_embeddings_contrastive (arxiv:2506.09781)
- `2026-06-21T08:38:37Z` ingest_paper: ingested paper:wang2025_khangcl_kolmogorovarnold_network (arxiv:2505.15103)
- `2026-06-21T08:42:11Z` idea-discovery updated gap_map for GCL node-classification idea search
- `2026-06-21T08:52:24Z` idea-discovery wrote 5 reviewed ideas (1 active, 1 backup, 2 deprioritized/auxiliary, 1 killed standalone)
- `2026-06-21` decision: abandoned NFR-GCL before implementation because novelty risk is high after finding close node-level adaptive spectral fusion prior work; next direction requires a fresh idea or explicit pivot to a backup.
- `2026-06-21` idea-discovery survey: mapped cross-domain methods transferable to graph contrastive learning; strongest follow-up directions are latent prediction, invariant-environment contrast, and optimal-transport soft alignment.
- `2026-06-21T18:53:14+08:00` idea-discovery selected SRLP-GCL as the active latent-prediction GCL direction; status is paper-only ACTIVE / ready for pilot, with no GPU result yet.
- `2026-06-21T19:15:58+08:00` research-refine completed two reviewer rounds for SRLP; final score 7.35/10, verdict READY for pilot, with final proposal saved at `refine-logs/FINAL_PROPOSAL.md`.
- `2026-06-22T13:35:00+08:00` idea-discovery added DCA-GCL as the current empirical lead after SBN failed and DCA showed Chameleon/Cora/CiteSeer edge-positive results; `research_wiki.py` was not available in the Windows session, so `index.md` and `query_pack.md` were not rebuilt.
- `2026-06-22T05:22:53Z` wiki-enrich: enriched paper:chen2024_leveraging_contrastive_learning from alphaxiv-abs (filled 10/10 sections)
- `2026-06-22T05:22:53Z` wiki-enrich: enriched paper:lee2025_similarities_embeddings_contrastive from alphaxiv-abs (filled 10/10 sections)
- `2026-06-22T05:22:54Z` wiki-enrich: enriched paper:thakoor2021_largescale_representation_learning from alphaxiv-abs (filled 10/10 sections)
- `2026-06-22T05:22:54Z` wiki-enrich: enriched paper:wang2022_augmentationfree_graph_contrastive from alphaxiv-abs (filled 10/10 sections)
- `2026-06-22T05:22:54Z` wiki-enrich: enriched paper:wang2025_khangcl_kolmogorovarnold_network from alphaxiv-abs (filled 10/10 sections)
- `2026-06-22T05:22:54Z` wiki-enrich: enriched paper:yang2023_graph_contrastive_learning from alphaxiv-abs (filled 10/10 sections)
- `2026-06-22T05:22:54Z` wiki-enrich: enriched paper:zhu2020_deep_graph_contrastive from alphaxiv-overview (filled 10/10 sections)
- `2026-06-22T05:22:54Z` wiki-enrich: enriched paper:zhu2020_graph_contrastive_learning from alphaxiv-abs (filled 10/10 sections)
- `2026-06-22T13:25:53Z` experiment-bridge: MFS-GCL R108/R109 CUDA smoke passed but split-0 gate failed; status `FAILED_SPLIT0_GATE`, report `refine-logs/MFS_R108_R109_RESULTS_20260622.md`.
- `2026-06-22T13:34:58Z` experiment-bridge: Ego-NoSelf BGRL R110/R111 CUDA smoke passed but direct no-self training failed split-0; status `FAILED_SPLIT0_GATE`, report `refine-logs/EGO_NOSELF_R110_R111_RESULTS_20260622.md`.
- `2026-06-22T13:45:00Z` experiment-bridge: added evaluation backend policy; canonical node-classification probe remains CPU sklearn, optional `torch_gpu_fast` is screening-only.
