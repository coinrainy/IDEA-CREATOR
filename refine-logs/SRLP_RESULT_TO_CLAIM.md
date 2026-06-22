# SRLP Result-to-Claim Verdict

**日期**: 2026-06-22  
**评估对象**: SRLP / SRLP-Aux / Adaptive-Aux  
**评估方式**: Codex 子智能体 result-to-claim 判定  
**结论**: `claim_supported = no`

## Intended Claim

SRLP / Adaptive-Aux 作为 shortcut-resistant latent prediction 图自监督主方法，能够在小图和异配图上稳定优于 target-family 消融，并值得继续扩展到外部强基线和论文主表。

## Verdict

当前结果不支持上述强 claim。SRLP 系列不应继续作为论文主方法推进。

## What Results Support

- Hard isolation 能降低 leakage：Chameleon 上 NoIso probe cosine 为 `0.63130`，hard isolation 为 `0.27185`。
- SRLP-Aux 比 residual-only SRLP hard 更合理，5-run gate 中相对旧 SRLP hard 有提升。
- 工程实现稳定：当前主要 run 无 NaN/collapse。
- 目标诊断有价值：不同数据集对 projection、residual、FullLatent、ZPZ 的偏好不同，label-free gate 能部分区分 Chameleon 与 Texas/Wisconsin。

## What Results Do Not Support

- 不支持 residual-only SRLP 作为主目标：M2 split 0 在 5 个小异配图上对最强 target-family 消融是 `0/5` clear wins。
- 不支持 SRLP-Aux 稳定优于 target-family：10 split 中只有 Chameleon 有极小正增益 `+0.00395`，Texas/Wisconsin/Actor 为负或持平。
- 不支持 Adaptive-Aux 当前 gate：200-epoch split-0 fair pilot 只有 Wisconsin 为正，Chameleon/Texas 为负。
- 不支持“降低 shortcut leakage 会自然转化为下游准确率提升”。
- 不支持继续外部强基线、10 split 扩展或大图主表。

## Suggested Claim Revision

可保留的弱 claim：

> Target-incident-edge isolation 能有效减少图 latent prediction 中的一类 shortcut leakage；但 residual-only 或 adaptive auxiliary residual 目前不能稳定提升节点分类性能。SRLP 系列更适合作为 target decomposition / leakage diagnostic 的负结果观察，而不是主方法。

## Next Action

停止 SRLP 主线扩展。建议先把 SRLP 写成 negative findings / lessons learned，然后重新启动 idea discovery，带着这次失败约束寻找新方向。

如果还要补一个很小的收尾动作，最多做已有 10-split per-split paired test 和失败模式整理；这只服务于负结果记录，不用于救主 claim。

## Confidence

`high`

完整性备注：未发现 `EXPERIMENT_AUDIT.json`，因此完整性审计状态为 `unavailable`。但基于多轮 split/dataset 结果，否定原始 claim 的置信度仍然高。
