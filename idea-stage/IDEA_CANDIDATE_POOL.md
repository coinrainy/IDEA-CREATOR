# Idea Candidate Pool

**方向**: 图对比学习，节点分类  
**生成时间**: 2026-06-21T08:39:08Z  
**目标**: 生成 30 个候选，覆盖至少 6 个机制桶；优先正向方法论文，实验以本地 `baselines/` 框架可落地为约束。

## 机制桶概览

| 桶 | 候选编号 | 主题 |
|---|---|---|
| B1 频带/滤波路由 | I1-I5 | 节点级 high/low-pass、混合频率、频带一致性 |
| B2 边/子图视图构造 | I6-I10 | edge compatibility、masked-edge、path view |
| B3 负样本/目标函数 | I11-I15 | hard negatives、within-view negatives、方差控制 |
| B4 bootstrap/augmentation-free | I16-I19 | BGRL/AF-GCL 式无增强视图 |
| B5 表征解耦/原型 | I20-I23 | label-free prototype、role/class disentanglement |
| B6 跨数据集/元学习 | I24-I26 | dataset-conditioned routing、transfer |
| B7 Graph transformer / tokenization | I27-I28 | tokenized GCL、long-range |
| B8 诊断与 benchmark | I29-I30 | 可解释诊断或 benchmark 扩展 |

## 30 个候选

### I1. Node-wise Frequency Routed GCL
- **一句话**: 为每个节点学习一个 high-pass / low-pass / identity 路由权重，用不同 contrastive view 对待同配区域和异配区域。
- **方法**: 复用 PolyGCL 的 ChebNetII high/low-pass encoder；用 feature similarity、edge disagreement 和 local label-free compatibility 估计节点级频率偏好；对同配节点做低通对齐，对异配节点做高通-低通互补对齐。
- **MVE**: 在 PolyGCL 上加节点级门控，Chameleon/Squirrel/Actor 单 seed 或 3 splits。
- **公平测试条件**: 必须直接对比 PolyGCL/GRASS/EDA-GCL，且使用 official heterophily splits。
- **状态**: ACTIVE。
- **风险**: MEDIUM；最接近 HLCL/AF-GCL，但差异在节点级路由而非全局滤波。

### I2. Compatibility-Calibrated Contrastive Edges
- **一句话**: 不再随机 drop edge，而是为每条边估计“同类兼容/异类兼容/噪声”类型，并按类型生成 contrastive views。
- **方法**: 用特征相似、Common-neighbor、PPMI、短程结构角色估计 edge compatibility；同配边保留到低通 view，异配边进入高通 view，噪声边作为 hard negative 或 masked reconstruction。
- **MVE**: 在 GCA/GRACE 的 edge drop 权重处替换为 compatibility-aware 权重。
- **公平测试条件**: 至少在 Chameleon/Squirrel/Texas 上比 GCA 和 GRACE 明显提升，并与 PolyGCL 比较。
- **状态**: ACTIVE。
- **风险**: MEDIUM；容易被质疑只是更复杂的 GCA。

### I3. Local Spectral Temperature Scaling
- **一句话**: 根据节点局部频率偏好动态调 InfoNCE temperature，异配区域减少错误拉近，同配区域保持稳定对齐。
- **方法**: 估计每个节点的 local heterophily score；high-frequency 节点使用更高温度或 margin loss，同配节点使用常规低温对齐。
- **MVE**: 修改 GRACE/GCA `tau` 为节点权重版本。
- **公平测试条件**: 需要证明不是单纯调参，必须有 per-node temperature ablation。
- **状态**: ACTIVE。
- **风险**: LOW-MEDIUM；实现简单但 novelty 较薄。

### I4. Mixed-Frequency View Consistency without Graph Augmentation
- **一句话**: 不做 edge/feature dropout，用同一图的多项式频带响应构造两个 view，并约束其互补而不是完全一致。
- **方法**: Chebyshev 多项式产生 low/mid/high-band embedding；同配节点 low-mid 对齐，异配节点 mid-high 对齐；加入 decorrelation 防塌缩。
- **MVE**: 基于 PolyGCL 改 loss，不改 backbone。
- **公平测试条件**: 对 AF-GCL/HLCL/PolyGCL 做直接 ablation。
- **状态**: ACTIVE。
- **风险**: MEDIUM；与 HLCL 接近，需要强调 mid-band 与节点级选择。

### I5. Frequency Dropout Curriculum
- **一句话**: 训练早期保持低频稳定，后期逐步引入高频 contrastive pressure，缓解异配图训练震荡。
- **方法**: 按 epoch 调整 high-pass 权重和 edge mask；用 validation-free schedule 或 local compatibility 自适应 schedule。
- **MVE**: 在 PolyGCL/GRASS 上加 curriculum。
- **状态**: DEPRIORITIZED。
- **风险**: 贡献像训练 trick，paper story 弱。

### I6. Masked Heterophilous Edge Reconstruction
- **一句话**: 把 GRASS 的 masked-edge reconstruction 改成区分同配边、异配边和噪声边的三类重构任务。
- **方法**: mask edge 后预测 edge compatibility type，而不仅是存在性；正例包括结构边和高相似非边，负例分随机负和 hard negative。
- **MVE**: 在 GRASS 中替换 `random_negative_sampler` 和 loss。
- **公平测试条件**: 与 GRASS 在 Cornell/Texas/Wisconsin 比较，不能只赢传统 GRACE。
- **状态**: ACTIVE。
- **风险**: MEDIUM；可落地，异配小图有强机会。

### I7. Path-Contrastive Views for Heterophily
- **一句话**: 用短路径而不是单边构造 view，让异配图中的同类远邻通过 2-hop/3-hop 路径成为正信号。
- **方法**: 复用 GRASS 的 `mask_path`，把 masked path embedding 和 endpoint embedding 做 contrast。
- **MVE**: 在 Actor/Chameleon/Squirrel 上测试 2-hop/3-hop path。
- **状态**: SPECULATIVE。
- **风险**: HIGH；可能只是高阶邻域 smoothing。

### I8. Ego-Neighbor Disagreement Views
- **一句话**: 对异配节点，不要求 ego 与邻居相似，而是学习 ego-view 与 neighbor-disagreement-view 的可预测关系。
- **方法**: 建两个 view：ego feature view 和 neighbor residual view；contrastive 目标改为预测 residual signature。
- **MVE**: 在 GRACE encoder 外加 residual projection。
- **状态**: SPECULATIVE。
- **风险**: MEDIUM-HIGH；novelty 可能高，但需要设计好 loss。

### I9. Structure-Preserving Feature Masking
- **一句话**: feature masking 不是按维度随机，而是保护能解释局部结构角色的 feature，扰动 class-spurious feature。
- **方法**: 用 feature-to-PPMI/degree/role correlation 生成 mask 权重。
- **MVE**: 替换 GCA/BGRL feature drop。
- **状态**: DEPRIORITIZED。
- **风险**: 容易变成 GCA feature-drop 小改。

### I10. Edge-Denoised BGRL for Heterophily
- **一句话**: 用 edge compatibility view 替代 BGRL 的随机 augmentation，让 bootstrapping 在异配图不被低频 bias 拖垮。
- **方法**: target encoder 输入 denoised/mixed-frequency graph，online encoder 输入原图或 high-pass graph；加 stop-gradient compatibility consistency。
- **MVE**: 在 BGRL transform 层增加 compatibility edge transform。
- **状态**: ACTIVE。
- **风险**: MEDIUM；BGRL 异配弱，提升空间大。

### I11. Heterophily-Aware Hard Negative Mining
- **一句话**: hard negative 只从“结构相近但兼容性冲突”的节点中选，避免把真实异配邻居错误推远。
- **方法**: 负样本池按 local compatibility 分层；同配区域选 feature-similar 不相连节点，异配区域选 role-similar 但 residual-signature 不同节点。
- **MVE**: 修改 GRACE semi_loss 的 negative weighting。
- **状态**: ACTIVE。
- **风险**: MEDIUM；与 Khan-GCL/2025 similarity theory相关，需要强调节点分类异配约束。

### I12. Within-View Negative Variance Regularizer for GCL on Graphs
- **一句话**: 把 2025 contrastive similarity 理论中的 negative similarity variance 控制迁移到节点级 GCL。
- **方法**: 在 mini-batch 或 full-batch negative matrix 上加入方差正则，异配节点单独分桶统计。
- **MVE**: GRACE/GCA/BGRL 上加 loss 项。
- **状态**: ACTIVE。
- **风险**: LOW-MEDIUM；简单且有理论锚，但可能不是 graph-specific。

### I13. False-Negative Guard via Pseudo-Compatibility
- **一句话**: 训练中动态识别潜在同类远邻，降低它们作为 negatives 的权重。
- **方法**: 用 EMA embedding similarity + local structure role 估计 false-negative risk。
- **MVE**: 在 GRACE negative denominator 中加 mask。
- **状态**: DEPRIORITIZED。
- **风险**: 已有 false-negative CL literature，graph novelty不足。

### I14. Margin-Split Contrastive Loss
- **一句话**: 对同配/异配节点使用不同 margin：同配拉近，异配保持可分但不过度推远。
- **方法**: 用 compatibility score 插值 alignment/uniformity loss。
- **MVE**: 修改 GRACE loss。
- **状态**: ACTIVE。
- **风险**: MEDIUM；需要有强理论或可视化支撑。

### I15. Prototype-Guided Hard Negatives without Labels
- **一句话**: 聚类得到 label-free prototypes，负样本只在相邻 prototype 边界采样。
- **方法**: 定期 k-means embedding，构造 prototype graph；边界节点使用 hard negative，核心节点使用普通 contrast。
- **MVE**: Chameleon/Squirrel 单 seed。
- **状态**: SPECULATIVE。
- **风险**: HIGH；聚类不稳定。

### I16. Augmentation-Free Node-Local BGRL
- **一句话**: 不做任何 graph augmentation，只让 online embedding 预测 target 的 local-filtered embedding。
- **方法**: target view 是 local high/low filtered embedding；online view 是原图 embedding；节点路由选择 target filter。
- **MVE**: BGRL + ChebNetII filter target。
- **状态**: ACTIVE。
- **风险**: MEDIUM；与 AF-GCL/BGRL 相近但组合清晰。

### I17. Collapse-Resistant Decorrelation for Heterophily
- **一句话**: 用 Barlow/orthonormal decorrelation 替代部分 InfoNCE，避免异配图错误 positives 导致塌缩或过平滑。
- **方法**: 同配节点做 alignment，异配节点只做 dimension decorrelation 和 uniformity。
- **MVE**: GRACE/AF-GCL loss 替换。
- **状态**: ACTIVE。
- **风险**: MEDIUM；需要证明异配场景独有。

### I18. Teacher-Free Consistency between Propagation Depths
- **一句话**: 把不同传播深度 K 的 embedding 作为 views，让节点自己选择最有用的 K。
- **方法**: 低 K 保局部，高 K 捕捉远邻；用 routing loss 学 K-mixture。
- **MVE**: PolyGCL ChebNetII K ablation。
- **状态**: SPECULATIVE。
- **风险**: MEDIUM-HIGH；与多尺度 GNN 很接近。

### I19. Low-Rank Compatibility Prior
- **一句话**: 学一个低秩 compatibility matrix，把全图节点关系压缩成少量“同配/异配/角色”通道，再用于 GCL。
- **方法**: SVD/low-rank factorization of PPMI + features；生成 contrastive positives/negatives。
- **MVE**: 小图上先做 Chameleon/Texas。
- **状态**: SPECULATIVE。
- **风险**: HIGH；实现和解释都更复杂。

### I20. Role-Class Disentangled GCL
- **一句话**: 将节点 embedding 拆成 class-signal 和 role-signal，避免异配图中结构角色与类别混淆。
- **方法**: 两个投影头；class head 对齐 feature-compatible nodes，role head 对齐 structure-compatible nodes；下游线性评估使用融合。
- **MVE**: 在 GRACE projection head 上加双头。
- **状态**: ACTIVE。
- **风险**: MEDIUM-HIGH；需要清楚证明 disentanglement。

### I21. Label-Free Class Prototype Contrast
- **一句话**: 用局部兼容性构造软原型，让节点与原型而不是所有节点做 contrast，减少 O(N^2) 噪声。
- **方法**: prototype memory bank + EMA 更新；同配和异配原型分离。
- **MVE**: 大图 Amazon/Coauthor 可验证效率，小图验证异配。
- **状态**: SPECULATIVE。
- **风险**: MEDIUM；工程稍重。

### I22. Confidence-Gated Linear Evaluation Feedback
- **一句话**: 用无标签 pseudo-eval confidence 反向调 GCL view，而不直接用标签。
- **方法**: 周期性训练轻量 probe，使用高置信一致节点更新 augmentation/negative weights。
- **状态**: DEPRIORITIZED。
- **风险**: 容易被认为半监督泄漏或过拟合验证集。

### I23. Minority/Boundary Node Preserving GCL
- **一句话**: 在 class-imbalanced 或边界节点上减少随机扰动，提高少数/边界类别表征。
- **方法**: 用 local density 与 embedding uncertainty 识别边界节点。
- **状态**: NEEDS_SETTING。
- **风险**: 当前本地数据没有显式 imbalance 主线。

### I24. Dataset-Conditioned GCL Router
- **一句话**: 给定一个图的统计特征，自动选择 BGRL/PolyGCL/GRASS 风格的 objective mixing。
- **方法**: 手工 meta-features 或小 MLP 预测 loss 权重。
- **MVE**: 14 个数据集上 leave-one-dataset-out。
- **状态**: SPECULATIVE。
- **风险**: 数据集数量太少，容易过拟合。

### I25. Cross-Dataset Frequency Prior Transfer
- **一句话**: 在多个异配图上学习通用的 frequency routing prior，再迁移到新图。
- **方法**: meta-train routing head，base encoder 每图训练。
- **状态**: NEEDS_SETTING。
- **风险**: 需要更多图和统一实现。

### I26. Hyperparameter-Free GCL Selection Rule
- **一句话**: 根据图统计预测用 GRACE/GCA/BGRL/PolyGCL/GRASS 哪个目标或组合。
- **方法**: 不是新模型而是选择器/recipe。
- **状态**: DEPRIORITIZED。
- **风险**: 更像 empirical guide，不是方法论文。

### I27. Contrastive Token Routing for Graph Transformer Node Classification
- **一句话**: 把节点分成 frequency/role tokens，在 tokenized graph transformer 中做局部 contrast。
- **方法**: 借鉴 GCFormer，但加入异配 frequency routing。
- **状态**: NEEDS_SETTING。
- **风险**: 需要新代码栈，超过最快 pilot。

### I28. Long-Range Positive Mining for Graph Transformers
- **一句话**: 用 transformer attention 找同类远邻 positives，解决异配图同类节点不相邻问题。
- **状态**: NEEDS_SETTING。
- **风险**: 需要 graph transformer baseline；当前 baselines 不完整。

### I29. GCL Failure Taxonomy for Node Classification
- **一句话**: 系统诊断不同 GCL 在同配/异配/小图/大图上的失败模式。
- **状态**: DEPRIORITIZED。
- **风险**: 默认目标是正向方法论文；诊断论文不优先。

### I30. Heterophily Fair-Test Benchmark Harness
- **一句话**: 将本地 baseline 复现实验整理为公平测试 harness，并加入所有方法统一 splits/eval。
- **状态**: DEPRIORITIZED。
- **风险**: 工具贡献，非核心方法；可作为附录支撑。

## 初筛排序

| Rank | Idea | Status | 为什么排在这里 |
|---:|---|---|---|
| 1 | I1 Node-wise Frequency Routed GCL | ACTIVE | 正中本地结果缺口，能复用 PolyGCL/HLCL/AF-GCL，又有节点级新意。 |
| 2 | I6 Masked Heterophilous Edge Reconstruction | ACTIVE | 贴合 GRASS 强项，小图异配可能最快出信号。 |
| 3 | I11 Heterophily-Aware Hard Negative Mining | ACTIVE | 结合 2025 similarity theory 与节点级异配，容易作为 loss 插件。 |
| 4 | I16 Augmentation-Free Node-Local BGRL | ACTIVE | BGRL 同配强异配弱，有清楚提升空间。 |
| 5 | I2 Compatibility-Calibrated Contrastive Edges | ACTIVE | 工程简单，但要避免沦为 GCA 小改。 |
| 6 | I12 Negative Variance Regularizer | ACTIVE | 简单稳定，但 graph novelty 弱于 I1/I6/I11。 |
| 7 | I20 Role-Class Disentangled GCL | ACTIVE | 新意较高，风险较高。 |
| 8 | I4 Mixed-Frequency View Consistency | ACTIVE | 与 I1 可合并为主方法的一部分。 |

## 推荐进入 Codex reviewer 的 top ideas

1. **I1 + I4 合并**: Node-wise Frequency Routed GCL with Mixed-Frequency Consistency。
2. **I6**: Masked Heterophilous Edge Reconstruction。
3. **I11**: Heterophily-Aware Hard Negative Mining。
4. **I16**: Augmentation-Free Node-Local BGRL。
5. **I2**: Compatibility-Calibrated Contrastive Edges。

