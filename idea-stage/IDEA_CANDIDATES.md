# 隐空间预测式图对比学习候选池

**方向**: 隐空间预测式图对比学习，用于节点分类，优先异配图。
**日期**: 2026-06-21
**状态**: 纸面候选池；未运行 GPU pilot。

## 设计约束

- 不继续 NFR-GCL 主线；ASPECT 已经覆盖节点级自适应谱融合，不能再把“节点级频率路由”当主贡献。
- 不做普通 Graph-JEPA 迁移；已有 Graph-JEPA、GraphMAE2、BGRL、JPEB-GSSL 等隐空间/预测式图 SSL 近邻。
- 第一版必须能嵌入现有 `baselines/` 节点分类评测，异配图使用 Geom-GCN 官方 10 个固定划分。
- 目标论文应是正向方法论文，而不是纯诊断或负结果论文。

## 候选池

| # | 候选机制 | 机制桶 | 状态 | 主要原因 |
|---|---|---|---|---|
| 1 | **SRLP-GCL: 残差隐目标预测式图对比学习** | 目标构造 / 反捷径 | ACTIVE | 预测去平滑后的目标隐表示，回应“正样本被消息传递平凡化”的新问题。 |
| 2 | 全隐表示目标预测 | 目标构造 | DEPRIORITIZED | 太接近 GraphMAE2 / Graph-JEPA / JPEB-GSSL，容易被认为是重命名。 |
| 3 | 原始特征遮蔽重建 + 对比 | 目标构造 | KILLED | GraphMAE/GraphMAE2 路线已成熟，新颖性不足。 |
| 4 | 多跳未来节点隐表示预测 | 目标构造 | SPECULATIVE | 有潜力，但容易退化成 context prediction，需要更强查新。 |
| 5 | 结构角色相似节点作为预测目标 | 目标选择 | SPECULATIVE | 适合异配图，但目标噪声高，首轮可作为 SRLP-GCL 的采样策略。 |
| 6 | 同层级/同难度负样本 InfoNCE | 对比目标 | ACTIVE-COMPONENT | 能减少过于容易的负样本，适合作为 SRLP-GCL 组成部分。 |
| 7 | 不确定性加权正目标 | 对比目标 | DEPRIORITIZED | 和不确定性 GCL、伪标签 GCL 接近，适合辅助不适合主线。 |
| 8 | OT 软目标分配 | 软对齐 | SPECULATIVE | 可连接 GCL-OT，但文本属性图已有近邻，普通属性图还需找清楚增量。 |
| 9 | 兼容性条件遮蔽 | 异配图机制 | ACTIVE-COMPONENT | 根据边兼容性/局部同配率决定遮哪些目标，适合嵌入 SRLP-GCL。 |
| 10 | 异配关系类型残差预测 | 异配图机制 | SPECULATIVE | 可能较强，但关系类型伪标签本身不稳。 |
| 11 | 边兼容性预测替代节点预测 | 异配图机制 | BACKUP | 接近旧备选 Masked Heterophilous Edge Reconstruction。 |
| 12 | 图距离解耦目标 | 异配图机制 | DEPRIORITIZED | 容易只是“远邻正样本”变体。 |
| 13 | 去邻域平滑残差目标 | 反捷径 | ACTIVE-COMPONENT | SRLP-GCL 的关键组件；把普通正样本对齐变成非平凡预测。 |
| 14 | 消息传递泄漏判别器 | 反捷径 | SPECULATIVE | 概念漂亮，但可能引入训练不稳；先做删除式 ablation。 |
| 15 | 只传播高残差信号 | 反捷径 | DEPRIORITIZED | 太接近 SPGCL / ASPECT 的能量或频率叙事。 |
| 16 | 残差强度课程学习 | 优化动态 | ACTIVE-COMPONENT | 可低成本加入，先预测中等难度目标，再加高残差目标。 |
| 17 | BGRL 式 EMA 目标编码器 | 架构 | ACTIVE-COMPONENT | 已有成熟 collapse 防护，适合作为 SRLP-GCL 骨架。 |
| 18 | GRACE 式双视图预测头 | 架构 | DEPRIORITIZED | 容易落回普通增强视图对齐。 |
| 19 | 无解码器 GraphMAE 变体 | 架构 | KILLED | 容易被 GraphMAE2 覆盖。 |
| 20 | 上下文 token 小 Transformer | 架构 | NEEDS_SETTING | 可能好看但复杂度上升，不适合第一轮 pilot。 |
| 21 | 同配图 no-regression 评测 | 评测 | REQUIRED | Cora/CiteSeer/PubMed/Amazon-Photo 只作为不退化检查。 |
| 22 | 异配图官方划分评测 | 评测 | REQUIRED | Actor/Chameleon/Squirrel/Cornell/Texas/Wisconsin 必须用 Geom-GCN 固定划分。 |
| 23 | 文本属性图语义目标扩展 | 设置扩展 | NEEDS_SETTING | 要原始文本或 LLM 特征，当前基线栈不宜首轮做。 |
| 24 | OGB 大图预训练扩展 | 设置扩展 | NEEDS_SETTING | 计算和数据成本较高；等小图 pilot 有信号再考虑。 |

## 入选路线

首选路线是 **SRLP-GCL: Shortcut-Resistant Residual Latent Prediction for Graph Contrastive Learning**。中文可称为“反捷径残差隐目标预测式图对比学习”。

它的核心不是“再预测一个隐表示”，而是让模型预测 **消息传递不能轻易抹平的目标残差信息**：

1. 用 EMA 教师编码干净图，得到每个节点的教师隐表示。
2. 从教师隐表示中减去邻域平滑部分，构造残差目标。
3. 在线编码器只看遮蔽后的上下文图，预测目标节点残差隐表示。
4. 在残差目标空间做条件 InfoNCE，同层级负样本来自相近度数、局部同配率或残差强度的节点。

## 纸面结论

SRLP-GCL 是目前最值得先做 pilot 的隐空间预测式 GCL 方向。它和 Graph-JEPA/GraphMAE2/JPEB-GSSL 的差别在于目标不是全隐表示或特征重建，而是为图消息传递设计的“反捷径残差目标”；和 ASPECT/SPGCL 的差别在于它不学习节点频率路由，而是改造预测任务本身，让正目标不再被普通消息传递提前完成。
