# EPI-BGRL M0/M1 结果：无标签环境均衡没有通过主方法 gate

**日期**：2026-06-22  
**候选**：EPI-BGRL（Environment-Partition Invariant BGRL）  
**状态**：`FAILED_MIXED_SPLIT0_GATE`  
**代码**：`baselines/BGRL/train_epi_transductive.py`，`baselines/BGRL/reproduce_epi.py`  

## 动机

LIFT-Portfolio 已经成为强训练自由基线，但它的新颖性不足。EPI-BGRL 尝试切换到一个不同机制族：不再继续调固定传播特征，而是在 BGRL 训练中用无标签环境分区约束自监督损失。

环境分区只使用图和特征，不使用标签：

- `degree_score = log(1 + degree)`；
- `feature_drift = 1 - cos(X_i, mean_neighborhood(X)_i)`；
- 默认将二者各切成 2 个分位桶，形成最多 4 个隐环境；
- 训练目标为 BGRL node loss 的环境均衡平均，加上环境 loss 方差惩罚。

核心假设：如果 BGRL 的自监督目标只优化易学的同质/高度区域，它会忽略异质图或 raw-dominant 图上的关键节点；环境均衡可能让表示在不同结构-特征环境上更稳定。

## GPU 与评估协议

- M0 smoke 和 M1 split-0 均记录 `device=cuda`。
- `stdout.log` 明确包含 `Using cuda for training.`。
- 运行中 `nvidia-smi` 曾观测到 RTX 3060 约 54% GPU 利用率。
- 最终节点分类仍使用原 BGRL/sklearn 线性探针口径；这部分是 CPU-only，用于保持结果可比。

## M0 smoke

命令：

```bash
python baselines/BGRL/reproduce_epi.py \
  --datasets=cora,chameleon \
  --variants=bgrl_control,epi_balanced_rex \
  --splits=0 --epochs=5 --eval_epochs=5 \
  --device=auto \
  --output_dir=runs/epi_smoke_20260622 --clean
```

结果：工程链路通过，CUDA 训练、环境分区、JSON/CSV 输出均正常；无 NaN，无坍塌。5 epoch 下环境损失尚未激活，因此不作为方法效果证据。

## M1 split-0 gate

命令：

```bash
python baselines/BGRL/reproduce_epi.py \
  --datasets=cora,citeseer,chameleon,texas,wisconsin \
  --variants=bgrl_control,epi_balanced_rex \
  --splits=0 --epochs=200 --eval_epochs=50 \
  --device=auto --env_bins=2 --env_warmup_epochs=20 \
  --lambda_env=0.5 \
  --output_dir=runs/epi_m1_split0_20260622 --clean
```

| Dataset | BGRL control | EPI-BGRL | Delta vs BGRL | LIFT-Portfolio split-0 | Decision |
|---|---:|---:|---:|---:|---|
| Cora | 0.833872 | 0.840794 | +0.006922 | 0.842640 | local positive, below required control |
| CiteSeer | 0.693839 | 0.690834 | -0.003005 | 0.725770 | fail |
| Chameleon | 0.438596 | 0.425439 | -0.013158 | 0.699561 | fail |
| Texas | 0.621622 | 0.621622 | +0.000000 | 0.810811 | tie, far below raw control |
| Wisconsin | 0.549020 | 0.549020 | +0.000000 | 0.823529 | tie, far below raw control |

Diagnostics:

- 所有 M1 runs 均为 `device=cuda`。
- `nan_flag=0`，`collapse_flag=0`。
- Cora/CiteSeer 环境分区较稳定；Chameleon 即使使用 2x2 分区仍存在一个 2-node 小环境，说明 degree × drift 的硬分区在异质图上不够稳。
- EPI 让训练 loss 更环境均衡，但这种均衡没有转化为节点分类增益，尤其损害 Chameleon。

## 判定

EPI-BGRL 不通过主方法 gate。

原因：

1. 只在 Cora 有小幅正信号，且仍低于 LIFT-Portfolio split-0。
2. CiteSeer 和 Chameleon 直接低于同 run BGRL control。
3. Texas/Wisconsin 与 BGRL 持平，但远低于 raw/LIFT-Portfolio。
4. 当前无标签环境划分存在极小环境，若继续调参需要引入合并/软环境机制，但这会进入 graph OOD / invariant learning 已拥挤方向，并且没有足够实验证据支撑。

## 决策

- 保留 EPI 代码与结果作为负证据。
- 不做 10-split，不扩外部 baseline。
- 将 `EPI-GCL` 从 `ACTIVE_BACKUP` 降级为 `FAILED_MIXED_SPLIT0_GATE`。
- 下一步继续机制族切换；避免继续围绕 LIFT 固定特征、正样本采样、谱融合、或简单环境均衡做小修小补。
