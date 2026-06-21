# Round 1 Refinement

## Problem Anchor

- **Bottom-line problem**: 设计一个用于节点分类的图对比学习方法，使自监督正目标真正提供有用学习信号，而不是被普通消息传递或同节点增强视图对齐提前平凡化。
- **Must-solve bottleneck**: 当前 GCL 常把同一节点的两个增强视图当作正样本；在图编码器消息传递后，这种正样本相似性可能已经由邻域平滑自然产生，导致对比目标学习到低信息量一致性，尤其难以解释异配图上的收益。
- **Non-goals**: 不继续 NFR-GCL 的节点级频率路由主线；不声称通用图 JEPA 或 latent prediction 本身新；不引入 LLM 文本教师、大图预训练或新的大模型栈；不把复杂实验矩阵当作贡献。
- **Constraints**: 第一版必须能嵌入现有 `baselines/` 节点分类评测；异配图必须使用 Geom-GCN 官方固定划分；本地 12GB GPU 友好；优先单进程顺序运行；新训练组件最多两个。
- **Success condition**: 残差隐目标预测在 Cora/Chameleon 单 split pilot 中不 collapse，且在异配图官方 split 0 上比全隐表示预测、普通 BGRL/GRACE 对齐更有信号；正式评测中在 Actor/Chameleon/Squirrel/Cornell/Texas/Wisconsin 上相对强本地基线有稳定提升或清晰互补优势。

## Anchor Check

- **Original bottleneck**: 普通 GCL 正目标可能被消息传递平凡化，导致自监督信号弱。
- **Why the revised method still addresses it**: 修订后不再把正目标定义为 `Z - PZ`，而是把教师目标分解为“可见上下文子空间能解释的部分”和“上下文无法直接解释的残差部分”；在线分支必须在硬遮蔽目标节点后预测这个残差。
- **Reviewer suggestions rejected as drift**: 不引入 LLM/VLM/Diffusion/RL；不转向纯环境不变学习；不把 conditional negative mining 作为主贡献。

## Simplicity Check

- **Dominant contribution after revision**: context-projected residual target，即可见上下文投影残差目标。
- **Components removed or merged**: 删除 conditional InfoNCE 主分支；删除 learned alpha；删除 predictor 输入里的结构标量；删除目标侧 covariance regularizer。
- **Reviewer suggestions rejected as unnecessary complexity**: 不加入 context estimator 训练器；不加入 OT 软分配；不引入多环境不变正则。
- **Why the remaining mechanism is still the smallest adequate route**: 只保留 EMA teacher、硬遮蔽在线上下文、投影残差目标、一个 MLP predictor 和可选的轻量 variance 防 collapse。

## Changes Made

### 1. Residual target 从高通差分改为上下文投影残差

- **Reviewer said**: `Z - PZ` 像 high-frequency signal 换名，和 ASPECT/SPGCL 风险过近。
- **Action**: 改为从教师目标 `z_bar(v)` 中扣除它在可见上下文教师子空间上的正交投影，只移除可见上下文能线性解释的分量。
- **Reasoning**: 这把叙事从“频率/平滑”转成“conditional unpredictability”，更贴近问题锚点。
- **Impact on core method**: 主目标现在是 `r_bar(v) = normalize((I - Q_v Q_v^T) z_bar(v))`，其中 `Q_v` 是可见上下文教师表示的低秩正交基。

### 2. 泄漏控制从软 dropout 改为硬目标隔离

- **Reviewer said**: mask target feature + 20% edge dropout 不足以防止 transductive leakage。
- **Action**: 在线编码图中对目标节点特征完全 mask，并移除所有 target incident edges；在线分支只编码上下文节点，再通过原图中的邻接索引聚合目标的可见邻居上下文。
- **Reasoning**: 预测器仍能看到“目标由哪些上下文邻居定义”，但不能通过 GNN 消息传递直接读到目标特征或目标边内流动的信息。
- **Impact on core method**: context vector 从 `H_masked(v)` 改为 `mean_{u in N(v)} H_ctx(u)`，不再使用目标节点隐藏状态或结构标量。

### 3. 删除 conditional InfoNCE 主分支

- **Reviewer said**: conditional InfoNCE 会让贡献发散，负样本设计可能反客为主。
- **Action**: v1 主方法只保留 residual cosine prediction，加可选 variance floor；InfoNCE 仅作为后续 appendix 备选，不进入核心 claim。
- **Reasoning**: 如果残差目标本身不成立，负样本再漂亮也救不了主张；如果残差目标成立，论文更干净。
- **Impact on core method**: 方法从“GCL 目标设计”收敛为“graph predictive SSL 目标设计”，GCL 作为问题来源和对比背景。

### 4. 删除 learned alpha 和结构标量输入

- **Reviewer said**: learned alpha 可能退回 full-latent prediction，结构标量可能泄漏 ID。
- **Action**: 不再使用 alpha；不把 degree、local compatibility、mask ratio 输入 predictor。
- **Reasoning**: 先做最小机制，避免调参驱动或 dataset-specific trick。
- **Impact on core method**: 版本更容易在 BGRL harness 中低成本实现和解释。

## Revised Proposal

# Research Proposal: SRLP

## Problem Anchor

- **Bottom-line problem**: 设计一个用于节点分类的图自监督方法，使正目标真正提供有用学习信号，而不是被普通消息传递或同节点增强视图对齐提前平凡化。
- **Must-solve bottleneck**: 当前 GCL 常把同一节点的两个增强视图当作正样本；在图编码器消息传递后，这种正样本相似性可能已经由邻域平滑自然产生，导致目标学习低信息量一致性，尤其难以解释异配图上的收益。
- **Non-goals**: 不继续 NFR-GCL 的节点级频率路由主线；不声称通用图 JEPA 或 latent prediction 本身新；不引入 LLM 文本教师、大图预训练或新的大模型栈；不把复杂实验矩阵当作贡献。
- **Constraints**: 第一版必须能嵌入现有 `baselines/` 节点分类评测；异配图必须使用 Geom-GCN 官方固定划分；本地 12GB GPU 友好；优先单进程顺序运行；新训练组件最多两个。
- **Success condition**: 上下文投影残差目标在 Cora/Chameleon 单 split pilot 中不 collapse，且在异配图官方 split 0 上比全隐表示预测、普通 BGRL/GRACE 对齐更有信号；正式评测中在 Actor/Chameleon/Squirrel/Cornell/Texas/Wisconsin 上相对强本地基线有稳定提升或清晰互补优势。

## Technical Gap

已有图自监督方法证明了两个事实：BGRL 类 EMA 预测很稳定，Graph-JEPA/GraphMAE2/JPEB-GSSL 类隐空间预测是可行路线。但这些方法大多把目标设成完整隐表示或同节点增强视图。完整目标中包含大量可由局部消息传递恢复的上下文成分；同节点增强正样本也可能由 GNN 的平滑机制自然拉近。

SRLP 的缝隙是把目标定义成 **visible context 不能直接解释的那部分教师隐表示**。它不是说邻居无用，也不是把邻居信息整体删掉；它只从目标节点教师表示里扣除对可见上下文子空间的投影。若异配邻居携带有用信息但不能被简单线性上下文子空间解释，它仍留在目标残差中。这样可以避免把方法写成高频滤波或节点级频谱路由。

## Method Thesis

- **One-sentence thesis**: SRLP 通过预测目标节点教师表示中无法由可见上下文子空间直接解释的残差成分，把图自监督正目标从“平凡视图一致性”改成“反消息传递捷径的上下文条件预测”。
- **Why this is the smallest adequate intervention**: 只改变训练目标和遮蔽方式，复用 BGRL 风格 EMA teacher、现有 GNN 编码器和线性评估。
- **Why this route is timely**: 近期 SPGCL 暴露了普通 GCL 正样本的消息传递平凡化风险；SRLP 给出一个更直接的目标层修复。

## Contribution Focus

- **Dominant contribution**: context-projected residual target，用可见上下文教师表示张成的低秩子空间解释目标教师表示，并把正目标设为正交残差。
- **Optional supporting contribution**: target-isolated context encoding，即在线分支完全隔离目标节点，只从目标的可见上下文邻居表示预测残差。
- **Explicit non-contributions**: 不提出新的 GNN backbone；不提出节点级频谱 policy；不提出 conditional negative mining；不提出外部语义教师。

## Proposed Method

### Complexity Budget

- **Frozen / reused backbone**: 复用现有 BGRL/GRACE 风格 GCN 编码器、优化器和线性评估流程。
- **New trainable components**: 一个 online predictor `g_theta`；EMA teacher `f_bar` 由 online encoder 滑动平均得到，不是额外可训练模块。
- **Deleted from v1**: learned alpha、conditional InfoNCE、degree/compatibility/mask-ratio predictor input、Transformer context aggregator、OT soft assignment。

### System Overview

```text
Teacher branch, clean graph:
  Z_bar = f_bar(X, A)
  For each target v:
    C_bar(v) = teacher latents of visible context nodes around v
    Q_v = low-rank orthonormal basis of C_bar(v)
    R_bar(v) = normalize((I - Q_v Q_v^T) Z_bar(v))

Online branch, target-isolated context graph:
  Mask target node features
  Remove all edges incident to target nodes
  H_ctx = f_theta(X_masked, A_without_target_incident_edges)
  c(v) = mean of H_ctx over original visible context nodes of v
  P_v = normalize(g_theta(c(v)))

Loss:
  L = mean_v [1 - cosine(P_v, stopgrad(R_bar(v)))] + optional variance floor
```

### Representation Design

For target node `v`, define a visible context set:

```text
N_ctx(v) = one-hop neighbors of v not in target set
```

If `N_ctx(v)` is empty, fall back to two-hop neighbors or skip `v` for this batch. The teacher context matrix is:

```text
C_bar(v) = [Z_bar(u1), ..., Z_bar(uk)]^T, u_i in N_ctx(v)
```

For v1, use a rank-1 context basis for simplicity:

```text
q_v = normalize(mean_{u in N_ctx(v)} Z_bar(u))
R_raw(v) = Z_bar(v) - q_v q_v^T Z_bar(v)
R_bar(v) = normalize(R_raw(v))
```

Rank-1 is deliberately simple. A rank-k QR basis is an ablation only if rank-1 fails.

### Target-Isolated Online Encoding

Sample target set `T` with mask ratio `rho`. Build online graph:

```text
X_online[v] = MASK_VECTOR for v in T
A_online = A with every edge (v, u) removed if v in T or u in T
H_ctx = f_theta(X_online, A_online)
```

The predictor input for target `v` is:

```text
c(v) = mean_{u in N_ctx(v)} H_ctx(u)
P_v = normalize(g_theta(c(v)))
```

This uses the original graph only as an index telling which visible context nodes belong to `v`; it does not let messages pass through the target node during online encoding.

### Loss

Main loss:

```text
L_pred = mean_{v in T_valid} [1 - cosine(P_v, stopgrad(R_bar(v)))]
```

Optional collapse guard:

```text
L_var = mean_j max(0, gamma - std(P_T[:, j]))
L = L_pred + beta * L_var
```

No covariance term in v1 unless collapse appears. No loss is applied to teacher residual targets.

### Training Recipe

1. Initialize online encoder from the baseline GCN/BGRL encoder.
2. Optional warmup for 20-50 epochs with full-latent BYOL/BGRL loss only to stabilize teacher; report this as engineering warmup, not a contribution.
3. Train SRLP objective with target mask ratio `rho=0.15-0.30`.
4. Use EMA momentum `m=0.99` or BGRL default.
5. Monitor residual raw norm; skip targets whose `||R_raw(v)|| < epsilon` to avoid pure noise targets.

### Inference Path

At inference, discard teacher, predictor, masking, projection residual computation, and variance guard. Use `f_theta(X, A)` node embeddings in the existing linear evaluation pipeline.

### Integration into Existing Baselines

Best initial implementation target is `baselines/BGRL` because it already has an EMA/target encoder pattern. Required changes:

- add target node sampler;
- build target-isolated online graph per epoch/batch;
- compute teacher clean embeddings;
- compute rank-1 context-projected residual targets;
- replace BGRL view prediction loss with SRLP residual prediction loss;
- keep the existing linear evaluator and split protocol.

## Failure Modes and Diagnostics

- **Residual target becomes pure high-frequency noise**
  Monitor `||R_raw||`, representation rank, and label separability of residual targets. If too noisy, reduce mask ratio or use rank-1 projection only.

- **Target is impossible to predict after hard isolation**
  Compare one-hop vs two-hop context sets. If one-hop isolated context is too weak, use two-hop context summaries but keep target incident edges removed in online encoding.

- **Teacher-online collusion or collapse**
  Monitor prediction variance, residual cosine histogram, and embedding rank. Add `L_var` only if collapse appears.

- **No heterophily gain**
  Compare full-latent target vs SRLP residual target under identical masking. If SRLP loses consistently, kill or demote the route.

## Novelty and Elegance Argument

SRLP's novelty is not graph JEPA, not BGRL, not high-frequency filtering, and not negative mining. The exact contribution is a target interface:

> construct the self-supervised target as the component of the teacher node representation that is orthogonal to the visible context subspace, then force an isolated online context encoder to predict that component.

This is more defensible than `Z - PZ`: it removes only the component directly explainable by visible context, rather than assuming all neighbor-smoothed signal is bad.

## Claim-Driven Validation Sketch

### Claim 1: Context-projected residual target is less trivial than full-latent prediction

- **Minimal experiment**: Cora and Chameleon split 0 / seed 0.
- **Baselines / ablations**: full-latent target; `Z - PZ` residual; context-projected residual; no incident-edge removal.
- **Metric**: linear eval accuracy, residual norm distribution, target-prediction cosine, embedding rank.
- **Expected evidence**: context-projected residual avoids collapse and improves Chameleon relative to full-latent target or `Z - PZ`.

### Claim 2: Hard target isolation is necessary

- **Minimal experiment**: Chameleon and Actor split 0.
- **Baselines / ablations**: soft 20% edge dropout; full incident-edge removal; feature mask only; incident-edge removal only.
- **Metric**: linear eval accuracy and leakage probe accuracy from online target state.
- **Expected evidence**: hard isolation improves or preserves downstream accuracy while reducing leakage probe success.

### Claim 3: The gain is from the residual target, not auxiliary modules

- **Minimal experiment**: Chameleon/Texas small table.
- **Baselines / ablations**: no variance guard, no warmup, rank-1 vs rank-k projection, full-latent target.
- **Metric**: accuracy and collapse diagnostics.
- **Expected evidence**: rank-1 residual target is the main contributor; variance guard and warmup are engineering stabilizers.

## Experiment Handoff Inputs

- **Must-prove claims**: context-projected residual is nontrivial; hard target isolation matters; gains survive against full-latent and `Z-PZ` ablations.
- **Must-run ablations**: full-latent target, `Z-PZ` target, rank-1 context projection, no incident-edge removal, no variance guard.
- **Critical datasets / metrics**: Cora no-regression; Chameleon/Actor/Squirrel pilot; full Actor/Chameleon/Squirrel/Cornell/Texas/Wisconsin official splits only if pilot is positive.
- **Highest-risk assumptions**: isolated context still contains enough information; rank-1 projection is not too weak; BGRL harness can be modified without memory blowup.

## Compute & Timeline Estimate

- **Estimated GPU-hours**: Pilot 0 about 2-4 GPU-hours; split-0 heterophily pilot about 6-10 GPU-hours; full formal table about 40-80 GPU-hours only after positive signal.
- **Data / annotation cost**: none.
- **Timeline**: one day for BGRL-based pilot implementation, one day for split-0 signal, two to four days for official 10-split table if positive.
