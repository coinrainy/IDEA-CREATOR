# Research Proposal: SRLP-GCL

## Problem Anchor

- **Bottom-line problem**: 设计一个用于节点分类的图对比学习方法，使自监督正目标真正提供有用学习信号，而不是被普通消息传递或同节点增强视图对齐提前平凡化。
- **Must-solve bottleneck**: 当前 GCL 常把同一节点的两个增强视图当作正样本；在图编码器消息传递后，这种正样本相似性可能已经由邻域平滑自然产生，导致对比目标学习到低信息量一致性，尤其难以解释异配图上的收益。
- **Non-goals**: 不继续 NFR-GCL 的节点级频率路由主线；不声称通用图 JEPA 或 latent prediction 本身新；不引入 LLM 文本教师、大图预训练或新的大模型栈；不把复杂实验矩阵当作贡献。
- **Constraints**: 第一版必须能嵌入现有 `baselines/` 节点分类评测；异配图必须使用 Geom-GCN 官方固定划分；本地 12GB GPU 友好；优先单进程顺序运行；新训练组件最多两个。
- **Success condition**: 残差隐目标预测在 Cora/Chameleon 单 split pilot 中不 collapse，且在异配图官方 split 0 上比全隐表示预测、普通 BGRL/GRACE 对齐更有信号；正式评测中在 Actor/Chameleon/Squirrel/Cornell/Texas/Wisconsin 上相对强本地基线有稳定提升或清晰互补优势。

## Technical Gap

现有图自监督有三条相近路线，但都没有直接解决这里的问题。

第一，BGRL 式 bootstrap 预测让在线编码器预测目标编码器的另一个增强视图，避免负样本成本，但正目标仍然是同节点视图一致性。若 GNN 的消息传递已经让两个视图在低频邻域统计上接近，预测任务会变得太容易。

第二，GraphMAE2 和 Graph-JEPA 证明隐空间预测可行，但它们的目标多是完整隐表示、特征重建正则或图级子图目标。完整隐表示里既包含消息传递已经恢复的平滑成分，也包含更难的节点特异成分；直接预测完整隐表示无法说明方法到底学到了什么。

第三，SPGCL 和 ASPECT 分别从正样本有效性、节点级频谱融合方向推进了 GCL，但如果继续写成“高频/低频路由”，会和 ASPECT 过近；如果只写成“能量更高的正样本”，又会和 SPGCL 过近。

SRLP-GCL 的技术缝隙是：**不改变编码器主干，而改变正目标的定义**。把教师隐表示拆成邻域平滑成分和残差成分，训练在线编码器在看不到目标节点完整输入的情况下预测残差成分。这样正目标不再是消息传递天然容易得到的平滑一致性。

## Method Thesis

- **One-sentence thesis**: SRLP-GCL 通过预测去除邻域平滑成分后的教师残差隐表示，把图对比学习的正样本目标从“同节点视图一致性”改造成“反消息传递捷径的目标节点信息预测”。
- **Why this is the smallest adequate intervention**: 不新增复杂骨干，不做频率路由，不引入外部教师；只在训练目标层面加入 EMA 教师、残差目标构造和一个预测头。
- **Why this route is timely**: 近期工作已经指出普通 GCL 正样本可能被消息传递平凡化；SRLP-GCL 把这个诊断转成一个可实现、可 ablation 的目标设计。

## Contribution Focus

- **Dominant contribution**: 残差隐目标构造，即从教师节点隐表示中显式扣除邻域平滑成分，再把剩余残差作为正目标。
- **Optional supporting contribution**: 条件残差对比采样，即在相近度数、相近局部同配率、相近残差强度的节点中选负样本，避免模型靠结构难度差异区分正负。
- **Explicit non-contributions**: 不提出新的 GNN backbone；不提出节点级频谱 policy；不提出 LLM 语义增强；不把方差/协方差 collapse 防护当主贡献。

## Proposed Method

### Complexity Budget

- **Frozen / reused backbone**: 复用现有 GCN/GRACE/BGRL 风格编码器和线性评估流程。
- **New trainable components**: 一个在线预测头 `g_theta`；一个 EMA 教师编码器 `f_bar` 由在线编码器滑动平均得到，不反向传播。
- **Tempting additions intentionally not used**: 不加 Transformer context aggregator；不加 OT 软匹配；不加 LLM 特征；不学频率路由；首轮不做多环境不变正则。

### System Overview

```text
Clean graph (X, A)
  -> EMA teacher f_bar
  -> teacher latent Z_bar
  -> neighbor smoother S_bar = P Z_bar
  -> residual target R_bar = normalize(Z_bar - alpha(v) S_bar)

Masked context graph (X_masked, A_masked)
  -> online encoder f_theta
  -> context latent H
  -> target context extractor q(v)
  -> predictor g_theta(q(v))
  -> residual prediction P_v

Loss:
  residual cosine prediction
  + conditional residual InfoNCE
  + light variance/covariance stabilizer
```

### Core Mechanism

#### 1. Teacher latent and smoother

Let `f_theta` be the online encoder and `f_bar` the EMA teacher. On the clean graph:

```text
Z_bar = f_bar(X, A)
P = row_normalize(A + I)
S_bar = P Z_bar
```

`S_bar(v)` is the one-hop smoothed teacher latent. For heterophily, use a convex smoother that can be attenuated:

```text
alpha(v) = clip(sigmoid(a0 + a1 * h_local(v) + a2 * deg_norm(v)), alpha_min, alpha_max)
R_bar(v) = normalize(Z_bar(v) - alpha(v) * S_bar(v))
```

`h_local(v)` is an unsupervised local compatibility score computed from feature cosine similarity across edges around `v`, not from labels. In the simplest pilot, set `alpha(v)=1` for all nodes and ablate learned/heuristic alpha later.

#### 2. Target masking and leakage control

Sample target node set `T` with probability `rho`. For `v in T`:

- Replace `X_v` with a learned `[MASK]` vector or zero feature plus mask bit.
- Drop a fraction `eta` of incoming edges to `v` during online encoding only.
- Keep teacher graph clean and stop-gradient.

The online encoder receives `(X_masked, A_masked)`. This prevents direct feature copying and weakens the path where target information leaks through its incident edges.

#### 3. Context extraction

For each target `v`, build:

```text
c(v) = concat(
  H_masked(v),
  mean_{u in N_visible(v)} H_masked(u),
  log_degree(v),
  local_feature_compatibility(v),
  mask_ratio_context(v)
)
P_v = normalize(g_theta(c(v)))
```

This uses only quantities available in the masked online graph. The structural scalars are optional but useful for conditioning; if they do not help, remove them.

#### 4. Residual prediction loss

```text
L_pred = mean_{v in T} [1 - cosine(P_v, stopgrad(R_bar(v)))]
```

This is the minimal non-contrastive objective.

#### 5. Conditional residual InfoNCE

For each target `v`, define a candidate pool:

```text
C(v) = {u != v | bin(deg(u)) = bin(deg(v)),
                 bin(local_compat(u)) = bin(local_compat(v)),
                 bin(||R_bar(u)||) = bin(||R_bar(v)||)}
```

If the bin is too small, relax conditions in order: residual norm, compatibility, degree. Then:

```text
L_ctr(v) = -log exp(sim(P_v, R_bar(v)) / tau)
           / sum_{u in {v} union Neg(v)} exp(sim(P_v, R_bar(u)) / tau)
```

This component is supporting, not mandatory. The main ablation should show whether residual target prediction alone already helps.

#### 6. Stabilizer

Use a light variance/covariance stabilizer on online predictions and teacher residual targets:

```text
L_stab = L_var(P_T) + L_cov(P_T)
```

This is included only to prevent collapse in small graphs. It should be removed in an ablation if unnecessary.

### Training Objective

```text
L = L_pred + lambda_ctr * L_ctr + beta * L_stab
```

Default pilot settings:

- `rho = 0.25`
- `eta = 0.2`
- `lambda_ctr = 0.2`
- `beta = 0.01`
- EMA momentum `m = 0.99`
- temperature `tau = 0.4`
- predictor: 2-layer MLP with hidden size equal to encoder hidden size

### Inference Path

At inference, discard `g_theta`, target masking, conditional negatives, and teacher residual target construction. Use `f_theta(X, A)` node embeddings for the existing linear evaluation protocol.

### Modern Primitive Usage

No external foundation model is used. The modern primitive is JEPA/BYOL-style joint-embedding prediction with an EMA target encoder, adapted to graph message-passing failure modes through residual target construction.

## Failure Modes and Diagnostics

- **Failure mode: residual target is just high frequency and too noisy.**
  Diagnostic: compare `R_bar` norm and label homophily bins; if residual targets are label-random, accuracy and target cosine will both fail.
  Mitigation: use attenuated `alpha(v)` or two-hop smoother `P2 Z_bar` ablation.

- **Failure mode: online encoder still leaks target information.**
  Diagnostic: train a feature-copy probe from `H_masked(v)` to `X_v`; if too strong, masking is leaky.
  Mitigation: increase feature mask ratio or incident-edge dropout for targets.

- **Failure mode: conditional negatives add noise.**
  Diagnostic: compare `L_pred` only vs `L_pred + L_ctr`.
  Mitigation: keep InfoNCE as optional supporting component and do not rely on it as the core claim.

- **Failure mode: collapse on small graphs.**
  Diagnostic: representation rank, per-dimension variance, cosine similarity histogram.
  Mitigation: use `L_stab`, EMA momentum warmup, or lower mask ratio.

## Novelty and Elegance Argument

The novelty claim is deliberately narrow: **residualizing the teacher latent target against graph neighborhood smoothing makes graph predictive contrastive learning less vulnerable to message-passing shortcuts**.

This avoids overclaiming:

- It does not claim graph latent prediction is new, because Graph-JEPA, GraphMAE2, and JPEB-GSSL are close.
- It does not claim node-wise spectral routing is new, because ASPECT is close and recent.
- It does not claim to discover positive-sample trivialization, because SPGCL already makes that diagnosis.

The paper's delta is the target interface: what exactly the online model is asked to predict, why that target is less trivial for message passing, and whether that improves heterophilous node classification.

## Claim-Driven Validation Sketch

### Claim 1: Residual targets make positive learning less trivial than full-latent targets

- **Minimal experiment**: Cora and Chameleon single split, compare full teacher latent target vs residual teacher latent target under identical encoder/predictor/masking.
- **Baselines / ablations**: full-latent prediction, residual with `alpha=0`, residual with `alpha=1`, residual with no edge masking.
- **Metric**: linear eval accuracy, target cosine gap, representation rank, positive/negative residual similarity distribution.
- **Expected evidence**: residual target avoids collapse and gives better Chameleon signal than full target without hurting Cora badly.

### Claim 2: The method improves heterophilous node classification under official fixed splits

- **Minimal experiment**: Actor, Chameleon, Squirrel split 0 first; then official 10 fixed splits if signal is positive.
- **Baselines / ablations**: GRACE, GCA, BGRL, PolyGCL, GRASS, EDA-GCL local results; SRLP without conditional InfoNCE; SRLP without target edge dropout.
- **Metric**: Accuracy / F1Mi, mean +/- std for full run.
- **Expected evidence**: at least 2/3 split-0 wins over classic GCL baselines and competitive signal against PolyGCL/GRASS/EDA-GCL.

### Claim 3: The gain comes from residual target construction, not added complexity

- **Minimal experiment**: deletion ablations on Chameleon and Texas.
- **Baselines / ablations**: remove conditional InfoNCE, remove structural scalars, remove stabilizer, replace residual target with raw teacher target.
- **Metric**: accuracy and collapse diagnostics.
- **Expected evidence**: raw teacher target and no-masking variants underperform; conditional InfoNCE may help but is not required for all gains.

## Experiment Handoff Inputs

- **Must-prove claims**: residual targets are nontrivial; residual targets help heterophily; gains are not from extra modules.
- **Must-run ablations**: full-latent target, residual alpha variants, target feature masking, target edge dropout, no conditional InfoNCE.
- **Critical datasets / metrics**: Cora no-regression; Chameleon/Actor/Squirrel pilot; full Actor/Chameleon/Squirrel/Cornell/Texas/Wisconsin official splits.
- **Highest-risk assumptions**: residual target is not too noisy; local feature compatibility is label-free and stable; 12GB GPU can handle memory bank or batch negative sampling.

## Compute & Timeline Estimate

- **Estimated GPU-hours**: Pilot 0 about 2-4 GPU-hours; split-0 heterophily pilot about 6-10 GPU-hours; full 10-split formal table about 40-80 GPU-hours depending baseline integration.
- **Data / annotation cost**: none; use existing datasets and fixed split masks.
- **Timeline**: one day for pilot implementation, one day for split-0 signal, two to four days for formal multi-split run if pilot is positive.
