# Review Summary

**Problem**: 图对比学习节点分类，重点是 heterophily 场景。  
**Date**: 2026-06-21  
**Reviewer**: Codex 子智能体 `019ee957-c111-7e42-ada2-d9f9f216e59c`  
**Final status**: READY_TO_PILOT  

## Reviewer Verdict

Codex reviewer 建议首选 I1+I4，即 **Node-wise Frequency Routed GCL with Mixed-Frequency Consistency**。I6 是 backup。I2/I11/I16 不建议 standalone。

## Resolution Log

| Concern | Resolution |
|---|---|
| I1 可能只是 PolyGCL/HLCL 加门控 | 主方法必须包含 global-router、random-router、feature-only-router、graph-level-router ablations。 |
| I2 standalone 太像 GCA/EDA-GCL | 降级为 router 的 edge compatibility 输入，不作为贡献。 |
| I11 hard negative 可能制造 false negatives | 只作为后续 auxiliary ablation，不进入首个 pilot。 |
| I16 BGRL+filter 太 incremental | 暂缓，除非补齐 BGRL heterophily baseline 后能打过 PolyGCL/GRASS。 |
| 小图方差大 | 使用 official 10 splits 和 paired split analysis；不过 go/no-go threshold 不写强 claim。 |

## Final Recommendation

先实现 **NFR-GCL**：一个干净的 node-local spectral routing paper。若 Actor/Chameleon/Squirrel pilot 不能平均超过当前 best local baseline +1.5 points，则停止主线并切到 GRASS-based heterophilous edge reconstruction backup。

