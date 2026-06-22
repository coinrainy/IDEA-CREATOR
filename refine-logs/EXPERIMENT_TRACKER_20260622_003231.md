# SRLP 4060 小图实验 Tracker

| Run ID | 模块 | 目的 | 系统 / 变体 | 数据集 / Split | 指标 | 优先级 | 状态 | 备注 |
|---|---|---|---|---|---|---|---|---|
| R001 | M0 | Smoke | SRLP hard | Cora fixed split seed 0 | JSON/CSV, skipped ratio, rank | MUST | DONE | `test@best=0.76927`, `skipped_ratio=0.04613`, 无 NaN/collapse。 |
| R002 | M0 | Smoke | SRLP hard | Chameleon Geom-GCN split 0 | JSON/CSV, skipped ratio, rank | MUST | DONE | 初始 directed-context skipped ratio 偏高；改用无向 context 后为 `0.00879`。 |
| R003 | M1 | 机制预实验 | 5 variants | Cora fixed split seed 0, 200 epochs | valid/test + diagnostics | MUST | DONE | SRLP hard `test@best=0.76465`，低于 BGRL 和 FullLatent-Iso。 |
| R004 | M1 | 机制预实验 | 5 variants | CiteSeer fixed split seed 0, 200 epochs | valid/test + diagnostics | MUST | DONE | SRLP hard `test@best=0.67280`，优于 ZPZ/NoIso，但低于 BGRL 和 FullLatent-Iso。 |
| R005 | M1 | 机制预实验 | 5 variants | Chameleon split 0, 200 epochs | valid/test + diagnostics | MUST | DONE | SRLP hard `test@best=0.42325`，短训 target-family 弱正信号，但低于 BGRL。 |
| R006 | M2 | Chameleon 延长训练 | 5 variants | Chameleon split 0, 1000 epochs | valid/test + diagnostics | MUST | DONE | SRLP hard `test@best=0.46053`，低于 FullLatent-Iso `0.49781`。 |
| R007 | M2 | 小异配图扩展 | 4 target-family variants | Cornell split 0, 1000 epochs | valid/test + diagnostics | MUST | DONE | 四个变体均为 `test@best=0.54054`，SRLP 并列但没有独立优势。 |
| R008 | M2 | 小异配图扩展 | 4 target-family variants | Texas split 0, 1000 epochs | valid/test + diagnostics | MUST | DONE | 最强消融 `0.64865`，SRLP hard `0.62162`。 |
| R009 | M2 | 小异配图扩展 | 4 target-family variants | Wisconsin split 0, 1000 epochs | valid/test + diagnostics | MUST | DONE | 最强消融 ZPZ-Iso `0.58824`，SRLP hard `0.47059`。 |
| R010 | M2 | 小异配图扩展 | 4 target-family variants | Actor split 0, 1000 epochs | valid/test + diagnostics | MUST | DONE | 最强消融 FullLatent-Iso `0.27237`，SRLP hard `0.26776`。 |
| R011 | M5 | 泄漏探针 | SRLP hard | Chameleon split 0 checkpoint | probe cosine/MSE | MUST | DONE | probe cosine `0.27185`, MSE `0.00362`。 |
| R012 | M5 | 泄漏探针 | SRLP-NoIso | Chameleon split 0 checkpoint | probe cosine/MSE | MUST | DONE | probe cosine `0.63130`, MSE `0.00236`。 |
| R013 | M3 | 10 split 内部消融 | SRLP-Aux vs target-family variants | Chameleon/Texas/Wisconsin/Actor split 0-9 | mean/std | MUST | DONE | Chameleon 小幅正，Actor 近似打平，Texas/Wisconsin 不支持；不进入外部主表。 |
| R014 | 外部主表 | 强基线对比 | 外部 baselines | 小图 / 中小异配图 | paper table | NICE | PAUSED | 10 split 内部消融不足以支撑主表扩展。 |
| R015 | 修订实现 | 方法降级修订 | SRLP-Aux | Code + smoke | py_compile + 5 epoch smoke | MUST | DONE | 新增 `target_mode=srlp_aux`，单头混合 target；Cora/Chameleon 5 epoch smoke 通过。 |
| R016 | 修订 gate | 小 gate | SRLP-Aux | Chameleon/Texas/Wisconsin/Actor split 0, 1000 epochs | valid/test + diagnostics | MUST | DONE | 4/4 相对旧 SRLP hard 提升；Chameleon/Texas 达到或超过最强 target-family。 |
| R017 | 修订 gate | 同配 sanity | SRLP-Aux | CiteSeer fixed split seed 0, 200 epochs | valid/test + diagnostics | MUST | DONE | `test@best=0.67656`，高于旧 SRLP hard `0.67280`，无 NaN/collapse。 |

## 输出位置

- M0 smoke：`baselines/BGRL/runs/srlp_m0_fixed_selfloops/`
- M1 Cora/CiteSeer：`baselines/BGRL/runs/srlp_m1_cora_citeseer200/results.csv`
- M1 Chameleon 200：`baselines/BGRL/runs/srlp_m1_chameleon200_fixed_selfloops/results.csv`
- M2 Chameleon 1000：`baselines/BGRL/runs/srlp_m2_chameleon1000/results.csv`
- M2 小异配图 split 0：`baselines/BGRL/runs/srlp_m2_hetero_split0/results.csv`
- SRLP-Aux smoke：`baselines/BGRL/runs/srlp_aux_smoke/results.csv`
- SRLP-Aux heterophily gate：`baselines/BGRL/runs/srlp_aux_gate_hetero1000/results.csv`
- SRLP-Aux CiteSeer gate：`baselines/BGRL/runs/srlp_aux_gate_citeseer200/results.csv`
- SRLP-Aux 10 split 内部消融：`baselines/BGRL/runs/srlp_aux_10split_target_family_20260621_221832/results.csv`
- SRLP-Aux 10 split 汇总：`refine-logs/SRLP_AUX_10SPLIT_RESULTS.md`
- 泄漏探针：`baselines/BGRL/runs/srlp_m1_chameleon200_fixed_selfloops/chameleon/*/probe_*.json`
- SRLP 实现文件：`baselines/BGRL/bgrl/srlp_utils.py`, `baselines/BGRL/train_srlp_transductive.py`, `baselines/BGRL/reproduce_srlp.py`, `baselines/BGRL/probe_srlp_leakage.py`

## 当前决策

Residual-only SRLP 已降级，不再作为主方法。SRLP-Aux 小 gate 通过，但 10 split 内部消融未形成稳定优势；外部强基线主表和大图扩展继续暂停。下一步应回到方法层面修 target，而不是继续扩大实验。

备注：`baselines/BGRL/` 是外层项目忽略的 nested repository，实验实现代码目前保留在该 nested checkout 中，除非单独在 nested repo 里提交，否则外层 Git 不会跟踪这些脚本。
