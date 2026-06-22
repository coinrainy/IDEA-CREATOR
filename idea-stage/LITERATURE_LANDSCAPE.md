# 图对比学习节点分类文献地形图

**日期**: 2026-06-22 09:56  
**阶段**: `research-pipeline` Stage 1 / `idea-discovery` Phase 1  
**方向**: 图对比学习（GCL）节点分类，目标是找到 2026 年仍有新颖性和效果潜力的 paper-level idea。  
**检索来源**: Web/arXiv、`arxiv_fetch.py`、`semantic_scholar_fetch.py`、`openreview_fetch.py`。本地 `papers/` 和 `literature/` 不存在，因此没有本地 PDF 输入。

## 总结判断

2025-2026 的 GCL 文献已经把常规路线挤得很满：正样本挖掘、PU 式采样校正、谱/高低频融合、传播算子、简单双视图、反事实视图、语义一致性判别都已有强近邻。当前项目最新的 TD-GCL 不应被立即杀掉，因为“训练更新方向正样本”还没有被检索到直接同款；但它的论文空间很窄，必须证明自己不是普通动态正样本/表示相似度挖掘的变体，而是利用训练轨迹中尚未被 message passing 平凡化的学习信号。

下一轮 idea discovery 应避免只说“更好的正样本”。更有希望的机制应该满足至少一条：

- 利用训练过程的二阶或轨迹信息，而不只是当前 embedding 相似度；
- 显式绕开 SPGCL 提出的 message passing positive trivialization；
- 能在异配图上给出 raw-dominant 保护，而不是让 Texas/Wisconsin 再次被图分支拖累；
- 能和 PROPGCL / Less is More 这样的简单强基线区分，而不是仅做更复杂的 BGRL 辅助损失。

## 关键文献边界

| 方向 | 代表工作 | 时间/状态 | 与本项目的关系 |
|---|---|---:|---|
| 正样本机制反思 | [Revisiting Positive Samples in GCL / SPGCL](https://arxiv.org/abs/2606.10284) | 2026-06 arXiv | 直接挑战“正样本有效性”假设：message passing 会平凡化正样本最大化。任何 TD-GCL 后续版本都要解释其动态正样本为何仍有有效信号。 |
| PU/语义采样校正 | [IFL-GCL](https://arxiv.org/abs/2505.06282) | SIGIR 2025 | 将 GCL 建模为 Positive-Unlabeled 学习，用 InfoNCE 估计语义正样本概率。压缩“表示相似度/语义正样本挖掘”的新颖性空间。 |
| 自适应正样本采样 | [HEATS](https://openaccess.thecvf.com/content/CVPR2024/papers/Zhuo_Improving_Graph_Contrastive_Learning_via_Adaptive_Positive_Sampling_CVPR_2024_paper.pdf) | CVPR 2024 | 用 block-diagonal / idempotent affinity matrix 学全局正样本。说明“global adaptive positive sampling”已经是强先验。 |
| 校准式 GCL | [CaliGCL](https://openreview.net/forum?id=aAxHUzTdhe) | NeurIPS 2025 | 用 partitioned similarity 和 semantic-consistency discriminator 校正相似度估计偏差和语义漂移。压缩“动态判别正样本是否可靠”的空间。 |
| 传播强基线 | [PROPGCL](https://openreview.net/forum?id=i4qdY4vQU9) | ICLR 2026 submission | 认为简单 training-free propagation 已能和复杂 GCL 竞争，并指出 GCL 中 transformation weights 可能学得不好。后续方法必须打过传播/图原型强控制。 |
| 简化双视图强基线 | [Less is More](https://openreview.net/forum?id=RvCkgg7pdt) | ICLR 2026 withdrawn | GCN 结构视图 + MLP 特征视图、不用 augmentation/negative sampling，在异配 benchmark 上很强。后续方法要避免“只是更复杂的 graph/raw 双分支”。 |
| 谱/频率自适应 | [ASPECT](https://arxiv.org/abs/2604.01878) | 2026-04 arXiv | node-wise spectral gating、低/高频自适应已经覆盖 NFR/DCA/FBA 一类路线。不要重启谱融合作为主贡献。 |
| 异配因果/结构捷径 | [CD-GNN](https://arxiv.org/abs/2604.19186) | 2026-04 arXiv | 从 inductive subgraph shortcuts 解释异配误分类。提示“结构捷径/反捷径”的方向可用，但不能和 CIG/CLEAR 的 edge-mask 失败重复。 |
| 反事实视图 | [G-Censor](https://openreview.net/forum?id=LiWGbK8_iOB) | ICLR 2023 submission | task-oriented counterfactual positive/negative views 已存在；CIG/CLEAR 已本地失败，不宜回到边反事实视图。 |
| 异配滤波 GCL | [HLCL](https://openreview.net/forum?id=NzcUQuhEGef) | ICLR 2023 submission | 高通/低通视图用于异配 GCL，和 ASPECT 一起封住简单 filter route。 |
| 超图异配 SSL | [BHyGNN+](https://arxiv.org/abs/2602.14919) | 2026-02 arXiv | hypergraph duality 是另一类结构转换；除非切换到 hypergraph benchmark，否则不适合作为当前节点分类主线。 |
| 噪声/核复杂度 | [KCR-GCL](https://openreview.net/forum?id=mm0ghNJIXo) | ICLR 2026 withdrawn | noisy node classification + kernel complexity reduction；提示“噪声鲁棒 GCL”拥挤但仍可作为 baseline/负面边界。 |

## 对当前 TD-GCL 的判定

TD-GCL 当前状态仍应是 `SPECULATIVE_INCUBATE`，不是 `READY_TO_REFINE`。

有利点：

- split-0 有清晰动态损失信号：Cora、CiteSeer、Chameleon 都优于 no-dynamics control；
- 当前检索没有发现完全相同的“embedding update direction positives”；
- 训练轨迹角度比静态 feature/WL/role/prototype/spectral positive 更不拥挤。

主要风险：

- SPGCL 已经从 message passing 角度讨论正样本学习信号被平凡化，TD-GCL 必须证明 update-direction positive 不是同样被平凡化；
- IFL-GCL、HEATS、CaliGCL 已覆盖“语义/动态/校准式正样本”的大叙事；
- Texas/Wisconsin raw-dominant 没有被解决，当前仅能说明“动态正样本在部分图上有益”；
- 现有证据仍是 split-0 pilot，不足以进入论文级实验计划。

## 下一轮候选生成约束

候选池必须避开以下已失败或强重叠机制：

1. residual latent prediction；
2. prototype / pseudo-class positives；
3. feature-teacher routing；
4. fixed low/high spectral filters 或 node-wise spectral gating；
5. raw/graph/filter deferred fusion；
6. semantic kNN positives；
7. local transport targets；
8. counterfactual edge masks；
9. whitening/uniformity rescue；
10. role/WL/landmark positives 作为主贡献；
11. 普通 adaptive positive sampling / PU correction；
12. 简单 GCN+MLP 双视图。

优先生成的机制家族：

- 训练轨迹信号：update direction、loss curvature、alignment velocity、forgetting/relearning；
- 传播平凡化逃逸：只对 high-energy 或 non-trivial residual signal 做动态对比，但不能落回 ASPECT/HLCL；
- raw-dominant 可靠性保护：label-free 预检，决定是否启用图对比辅助；
- 节点级难度/偏置：degree bias、hard-to-learn nodes、class-imbalance without labels，但需避开 HAR/imbalance GCL；
- 结构捷径反证：不是删边，而是识别图编码中稳定但任务无关的 shortcut mode；
- 评估协议创新：用 PROPGCL、Less is More、RFA/RSP/DCA 作为内部强控制，先做公平 split-0 或 3-split gate。

## Stage 1 结论

文献地形与项目历史一致：当前没有 `READY_TO_REFINE` 方法。最接近可继续孵化的是 TD-GCL，但必须先过两道门：

1. 深查“training trajectory / optimization dynamics positives”是否已有直接先例；
2. 设计一个比普通 dynamic positive sampling 更窄、更能解释 SPGCL 挑战的改版，并做小规模公平 pilot。

若查新失败，应重启 `idea-creator` 宽搜索，机制中心从“正样本选择”转向“训练信号选择 / 平凡化逃逸 / label-free 可靠性门控”。
