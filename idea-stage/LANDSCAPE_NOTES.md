# 图对比学习节点分类：景观与实验锚点

**方向**: 图对比学习，节点分类  
**生成时间**: 2026-06-21T08:39:08Z  
**本地实验依据**: `baselines/reproduction_results.xlsx`, `baselines/reproduction_results.md`, `baselines/reproduction_protocol.md`

## 1. 当前实验台

本项目已经复现或部分复现 9 类 GCL baseline：DGI、MVGRL、GRACE、GCA、BGRL、PolyGCL、GRASS、EPAGCL、EDA-GCL。任务统一为节点分类，数据集分两张主表：

- Homophily: Cora、CiteSeer、PubMed、Amazon-Photo、Amazon-Computers、Coauthor-CS、Coauthor-Physics、Wiki-CS。
- Heterophily: Actor、Chameleon、Squirrel、Cornell、Texas、Wisconsin，采用 Geom-GCN official 10 fixed splits。

本地结果显示，homophily 上强者分散，而 heterophily 上存在清晰结构性差异：

| 数据集 | 当前最佳本地结果 | 观察 |
|---|---:|---|
| Cora | MVGRL 84.74±0.88 | 多数方法接近，提升空间小且容易被方差吞掉。 |
| CiteSeer | MVGRL 73.28±0.41 | DGI/EDA-GCL 接近，属于饱和-ish 区域。 |
| PubMed | GRACE 86.06±0.37 | 本地只完成少数 baseline，OOM/TODO 较多。 |
| Amazon-Photo | BGRL 93.29±0.23 | DGI/EDA-GCL/BGRL 都很强，提升需要低方差证据。 |
| Amazon-Computers | BGRL 90.69±0.18 | BGRL/EDA-GCL/GCA 可作为强直接基线。 |
| Actor | PolyGCL 37.11±1.34 | 异配小幅空间，PolyGCL/GRASS 明显强于传统 GRACE/GCA。 |
| Chameleon | PolyGCL 70.68±2.02 | PolyGCL 与 EDA-GCL 最强，频带/边感知路线有效。 |
| Squirrel | PolyGCL 55.87±1.60 | PolyGCL 明显领先 EDA-GCL，传统方法弱。 |
| Cornell | GRASS 81.35±3.91 | 小图方差大，GRASS 的 masked-edge reconstruction 有强信号。 |
| Texas | PolyGCL 81.08±4.36 | PolyGCL/GRASS 强，EDA-GCL 次之。 |
| Wisconsin | GRASS 82.55±3.33 | GRASS/PolyGCL 强，传统低通增强方法明显不足。 |

Baseline 平均趋势：

| Baseline | Homophily 平均 | Heterophily 平均 | 结论 |
|---|---:|---:|---|
| BGRL | 85.17 | 39.59 | 同配强，异配弱；augmentation/bootstrapping 未感知频率偏好。 |
| GCA | 82.75 | 44.30 | 中心性自适应增强不足以处理异配。 |
| GRACE | 80.06 | 45.63 | 经典双视图 InfoNCE 在异配图上弱。 |
| EDA-GCL | 85.04 | 56.25 | edge-aware 思路有效但不稳定。 |
| GRASS | 77.85 | 59.48 | masked-edge reconstruction 在小异配图强。 |
| PolyGCL | 76.85 | 65.87 | 多项式/频带路线是当前异配最强锚点。 |

## 2. 关键文献锚点

| Paper | Link | 对本项目的意义 |
|---|---|---|
| GRACE: Deep Graph Contrastive Representation Learning | https://arxiv.org/abs/2006.04131 | 经典 augmentation-based GCL 基线。 |
| GCA: Graph Contrastive Learning with Adaptive Augmentation | https://arxiv.org/abs/2010.14945 | 用中心性/特征重要性控制增强，是“全局增强调参”的代表。 |
| BGRL: Large-Scale Representation Learning on Graphs via Bootstrapping | https://arxiv.org/abs/2102.06514 | 不用显式负样本，同配图强，是轻量 backbone 候选。 |
| AF-GCL: Augmentation-Free Graph Contrastive Learning with Performance Guarantee | https://arxiv.org/abs/2204.04874 | 明确指出常规 augmentation 保低频、扰动中高频；这解释了异配图失败。 |
| HLCL: Graph Contrastive Learning under Heterophily via Graph Filters | https://arxiv.org/abs/2303.06344 | 低通/高通滤波生成异配图 views，是最接近“频带感知 GCL”的 prior work。 |
| GCFormer: Contrastive Learning for Tokenized Graph Transformers | https://arxiv.org/abs/2406.19258 | 说明 GCL 可服务于 graph transformer/tokenized node representation。 |
| On the Similarities of Embeddings in Contrastive Learning | https://arxiv.org/abs/2506.09781 | 指出负样本相似度分布/mini-batch 方差会影响 representation quality，可转化为 hard-negative 调度。 |
| Khan-GCL | https://arxiv.org/abs/2505.15103 | 2025 hard-negative GCL，风险是 KAN/graph-level 机制与节点分类异配图不完全重合。 |

## 3. 可发表缺口

**G1: 现有 GCL 的 view construction 多为图级全局策略，缺少节点级局部频率/兼容性自适应。**  
AF-GCL 和 HLCL 已经指出频率问题，但大多以全局滤波或全图 homophily 假设处理。实际数据中一个图内部可能同时有同配区域、异配区域、边噪声和局部结构角色。

**G2: 异配图最强 baseline 分散于 PolyGCL/GRASS/EDA-GCL，但缺少统一的“何时对齐、何时分离、何时重构边”的机制。**  
PolyGCL 强在频带，GRASS 强在 masked-edge reconstruction，EDA-GCL 强在 edge-aware 设计；这些机制可被统一为节点/边级路由，而不是并列堆模块。

**G3: 负样本在节点级 GCL 中仍然粗糙。**  
2025 contrastive similarity 理论和 Khan-GCL 都指向 hard negative，但节点分类中 hard negative 应该被 homophily/heterophily 兼容性约束；否则会把真实异类邻居误推远或把同类远邻误当负样本。

**G4: 本地实验提示同配图已经饱和，异配图才有方法空间。**  
如果新方法只在 Cora/CiteSeer/Amazon-Photo 上微涨，很难成故事；应把主锚点放在 Actor/Chameleon/Squirrel/WebKB，homophily 只证明不退化。

**G5: 需要可在现有 baseline 框架内快速落地。**  
最可行的工程路线是复用 PolyGCL 的 ChebNetII high/low-pass encoder、GCA/GRACE 的 contrastive loss/eval 管线、GRASS 的 masked-edge reconstruction 或 BGRL 的 bootstrapping。避免引入大模型或新数据依赖。

## 4. 推荐搜索/实验边界

- 主任务：transductive node classification；不扩展到 graph classification 或 recommendation。
- 主数据集：Chameleon、Squirrel、Actor、Cornell、Texas、Wisconsin；homophily 用 Cora/CiteSeer/Amazon-Photo/Amazon-Computers 验证不退化。
- 强基线：PolyGCL、GRASS、EDA-GCL、BGRL；传统 baseline 可保留但不作为唯一比较。
- 首个公平 pilot：优先选择 Chameleon/Squirrel/Actor 三个异配图，单 seed 或 3 fixed splits，目标是相对 PolyGCL/GRASS 至少 +1.0 到 +2.0 accuracy point，且 homophily 不明显下降。

