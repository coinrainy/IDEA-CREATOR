# Research Proposal: NFR-GCL

## Problem Anchor

- **Bottom-line problem**: 图对比学习在节点分类中对 homophily 与 heterophily 的局部结构差异处理不够；全图级 augmentation 或全局频带组合无法同时适配一个图内部的同配区域、异配区域和噪声边。
- **Must-solve bottleneck**: 现有 GCL 常把所有节点放进同一种 view construction / contrastive objective，导致异配节点被错误低通平滑，或同配节点被不必要高频扰动。
- **Non-goals**: 不做 graph classification、recommendation、text-attributed graph、graph transformer 新栈；不引入标签构造 routing signal；不把 hard-negative mining 作为主贡献。
- **Constraints**: 复用本地 `baselines/`，优先在 PolyGCL/ChebNetII 框架内实现；节点分类；official heterophily fixed splits；先做 <=1 天 decisive pilot。
- **Success condition**: 在 Actor/Chameleon/Squirrel official 10 splits 上，平均超过当前 best local baseline 至少 +1.5 accuracy points，至少 2/3 数据集胜出，同时 Cora/CiteSeer smoke 不下降超过 1 point。

## Technical Gap

AF-GCL 和 HLCL 说明频率偏好是 GCL 在 heterophily 上成败的关键；PolyGCL 在本地结果中也验证了频带路线的强度。但这些方法仍主要使用全局滤波、全图固定 high/low 组合，或 dataset-level 假设。真实图中，一个节点附近可能同配，另一个节点附近可能异配；同一个数据集还可能混有噪声边、结构角色边和远程同类节点。因此，缺失的是 **node-local frequency routing**：用无标签局部统计决定每个节点更应该对齐低频、中频还是高频视图。

## Method Thesis

- **One-sentence thesis**: NFR-GCL learns node-wise frequency routing weights to contrast low/mid/high-pass views differently for each node, preserving homophilic smoothness where useful and heterophilic high-frequency signal where necessary.
- **Smallest adequate intervention**: 不换任务、不换大模型、不堆多个新模块；只在 PolyGCL 的 high/low-pass encoder 上增加 mid-band view、node router 和 mixed-frequency consistency loss。
- **Dominant contribution**: 节点级频带路由的 GCL objective。
- **Optional supporting contribution**: 无标签 edge compatibility features 作为 router 输入。

## Proposed Method

### 1. Multi-band encoder

复用 ChebNetII / polynomial filtering。对每个节点得到三种 embedding：

- `z_low`: low-pass view，强调同配平滑。
- `z_mid`: mid-band view，作为桥接频带，减少 high/low 直接对齐的不稳定。
- `z_high`: high-pass view，保留异配/边界节点的差异信号。

### 2. Label-free node router

为每个节点构造无标签 routing features：

- local feature similarity mean/std over incident edges；
- PPMI 或 common-neighbor 结构兼容性；
- high-frequency energy，例如 `||x_i - lowpass(x)_i||`；
- degree / clustering / ego-neighbor residual statistics。

小 MLP 或参数量很小的 linear router 输出 `r_i = softmax([r_low, r_mid, r_high])`。训练时不使用 train/val/test labels。

### 3. Mixed-frequency consistency

对每个节点，按 `r_i` 加权三种 contrastive pressure：

- low-oriented nodes: align `z_low` and `z_mid`；
- high-oriented nodes: align `z_high` and `z_mid`；
- ambiguous nodes: enforce decorrelation/uniformity rather than over-alignment。

主 loss 是 weighted InfoNCE / bootstrap consistency 加一个轻量 orthogonality/decorrelation term，避免所有节点路由塌缩到同一频带。

### 4. Inference

下游线性评估使用 fused embedding：

`z_i = r_low_i * z_low_i + r_mid_i * z_mid_i + r_high_i * z_high_i`

也保留 `z_low + z_high` 全局融合和 PolyGCL 原始融合做 ablation。

## Claim-Driven Validation Sketch

### Claim 1: Node-local routing beats global high/low mixing on heterophily

- **Minimal experiment**: Actor、Chameleon、Squirrel official 10 splits。
- **Baselines**: PolyGCL、GRASS、EDA-GCL、GCA、GRACE。
- **Ablations**: global-router、random-router、feature-only-router、graph-level-router、no-mid-band、no-compatibility。
- **Metric**: Accuracy/F1Mi mean±std, paired split analysis。
- **Expected evidence**: Average +1.5 points over current best local baseline and wins on at least 2/3 datasets。

### Claim 2: The gain comes from routing, not parameter count or tuning

- **Minimal experiment**: Match parameter budget, same epochs/evaluator/splits; compare router variants and fixed global weights。
- **Metric**: Accuracy/F1Mi, parameter count, wall-clock。
- **Expected evidence**: Learned node router beats global/random router under matched compute。

## Risks

- Router collapses to one global frequency. Mitigation: entropy floor, router usage diagnostics, random/global router ablations.
- Compatibility features behave like noisy hyperparameters. Mitigation: freeze features before training; report feature-only vs full router.
- Small heterophily datasets have high variance. Mitigation: official 10 splits, paired split table, no strong claim unless go/no-go threshold is met.

## Verdict

**READY_TO_PILOT**, not READY_TO_CLAIM. The method is concrete enough for a decisive pilot, but no empirical improvement has been established yet.

