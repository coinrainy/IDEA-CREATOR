# PAB-BGRL M0/M1 结果：BGRL 内部有小信号，但不能作为主方法

**日期**：2026-06-22  
**候选**：PAB-BGRL（Prealignment-Abstention BGRL）  
**状态**：`BGRL_INTERNAL_SIGNAL_NOT_MAIN_METHOD`  
**代码**：`baselines/BGRL/train_npg_transductive.py`，`baselines/BGRL/reproduce_npg.py`  

## 动机

EPI-BGRL 说明单纯做环境均衡不足以突破 LIFT-Portfolio。PAB-BGRL 切回 BGRL 的核心失效点：message passing 会让一部分节点在训练前就已经被自动对齐，普通 BGRL 仍然把这些“平凡正样本”纳入同等权重，可能稀释真正有效的训练信号。

PAB 使用 NPG 里已有的无标签 `prealign` 诊断：

```text
prealign_i = 1 - cos(anchor_i, P anchor_i)
```

其中 `anchor` 是原始特征经固定随机投影后的归一化表示，`P anchor` 是一次规范化邻域传播后的表示。`pab_soft` 使用 `prealign` 的中位数作为软门控阈值，让高非平凡节点获得更大 BGRL loss 权重，低非平凡节点只保留弱权重防止坍塌。

## 新颖性警报

这个机制方向风险较高。2026 年 6 月的 SPGCL 已经明确提出 GCL 中的 `pre-alignment effect`：message passing 会让正样本在优化前变相相似，从而削弱正样本学习，并用 Dirichlet energy 分离传播和正样本构造。PAB 的区别只是节点级 loss abstention 而不是特征维度能量分离；如果没有强实验结果，不足以支撑论文级新颖性。

## GPU 与评估协议

- M0 smoke 和 M1 split-0 均记录 `device=cuda`。
- 所有 M1 run 的 `stdout.log` 都包含 `Using cuda for training.`。
- 最终节点分类保持原 BGRL/sklearn CPU 线性探针口径。
- 无 NaN，无表示坍塌。

## M0 smoke

命令：

```bash
python baselines/BGRL/reproduce_npg.py \
  --datasets=cora,chameleon \
  --variants=bgrl_control,pab_soft \
  --splits=0 --epochs=5 --eval_epochs=5 \
  --device=auto \
  --output_dir=runs/pab_smoke_20260622 --clean
```

结果：工程链路通过，CUDA 训练与 CSV/JSON 输出正常。5 epoch 只作为工程 smoke，不解释方法效果。

## M1 split-0 gate

命令：

```bash
python baselines/BGRL/reproduce_npg.py \
  --datasets=cora,citeseer,chameleon,texas,wisconsin \
  --variants=bgrl_control,pab_soft \
  --splits=0 --epochs=200 --eval_epochs=50 \
  --device=auto \
  --output_dir=runs/pab_m1_split0_20260622 --clean
```

| Dataset | BGRL control | PAB soft | Delta vs BGRL | LIFT-Portfolio split-0 | Decision |
|---|---:|---:|---:|---:|---|
| Cora | 0.832949 | 0.832949 | +0.000000 | 0.842640 | tie, below required control |
| CiteSeer | 0.693464 | 0.695342 | +0.001878 | 0.725770 | tiny internal gain, below required control |
| Chameleon | 0.438596 | 0.449561 | +0.010965 | 0.699561 | internal gain, far below required control |
| Texas | 0.621622 | 0.648649 | +0.027027 | 0.810811 | internal gain, far below raw control |
| Wisconsin | 0.549020 | 0.549020 | +0.000000 | 0.823529 | tie, far below raw control |

Diagnostics:

- `nan_flag=0` and `collapse_flag=0` across all rows.
- PAB soft creates nontrivial loss reweighting (`weight_std` roughly 0.28-0.56), but does not produce a representation competitive with fixed raw/propagation controls.
- The best local signal is Texas over BGRL, but Texas remains raw-dominant and raw/LIFT is much stronger.

## 判定

PAB-BGRL 不进入主方法扩展。

原因：

1. 它是 BGRL 内部改进，不是对当前最强 LIFT-Portfolio 控制的有效挑战。
2. Chameleon/Texas 的增益虽然真实，但绝对水平仍远低于 P2/raw。
3. 该方向与 SPGCL 的 2026 pre-alignment/message-passing 分析高度邻近；没有强结果时，新颖性不足。

## 决策

- 保留 `pab_soft` / `pab_hard` 代码作为诊断变体。
- 不跑 PAB 10-split，不做外部 baseline。
- 下一轮需要找比“BGRL loss 节点权重”更强的机制，最好能直接在表示空间保留 LIFT-Portfolio 的有效固定信号，同时引入明确互补的新学习目标。
