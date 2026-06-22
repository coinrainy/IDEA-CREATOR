# Experiment Tracker: Post-TDGCL Pilot Queue

**Date**: 2026-06-22 18:46  
**Subagent reviewer policy**: disabled for ad-hoc reviewer/code-review subagents only.  

| Run ID | Candidate | Variant | Dataset(s) | Split(s) | Status | Result | Notes |
|---|---|---|---|---|---|---|---|
| R049 | NPG-GCL | npg smoke | Cora, Chameleon | 0 | done | passed | no NaN/collapse |
| R050 | NPG-GCL | bgrl_control | Cora, CiteSeer, Chameleon, Texas, Wisconsin | 0 | done | control logged | same-run no-gain control |
| R051 | NPG-GCL | npg | Cora, CiteSeer, Chameleon, Texas, Wisconsin | 0 | done | weak signal | Cora +0.0037, Chameleon +0.0044, WebKB tie |
| R052 | NPG-GCL | uniform_gain | Cora, Chameleon | 0 | done | mixed | Cora close to NPG, Chameleon equals control |
| R053 | NPG-GCL | random_gain | Cora, Chameleon | 0 | done | mixed/fail | random beats NPG on Cora; NPG beats random on Chameleon |
| R054 | NPG-GCL | npg 3-split | Cora, CiteSeer, Chameleon, Texas, Wisconsin | 0,1,2 | skipped | not promoted | NPG did not pass split-0 strength gate |
| R055 | SC-BGRL | fixed-sign smoke | Cora, Chameleon | 0 | done | passed | initial sign threshold degenerated on Chameleon |
| R056 | SC-BGRL | rank-fix smoke | Chameleon | 0 | done | passed | forced 50/50 same/different edge split |
| R057 | SC-BGRL | rank-fix fair pilot | Cora, Chameleon, Texas, Wisconsin | 0 | done | failed | Cora/Chameleon regress; WebKB tie |
| R058 | GDC-GCL+ | gdc smoke | Cora, Chameleon | 0 | done | passed | no NaN/collapse |
| R059 | GDC-GCL+ | bgrl_control vs gdc_residual | Cora, CiteSeer, Chameleon, Texas, Wisconsin | 0 | done | failed | only weak Chameleon gain; Cora/CiteSeer fail; WebKB tie |
| R060 | GDC-GCL+ | td_direction comparison | Cora, CiteSeer, Chameleon | 0 | done | failed | no meaningful recovery of earlier TD-GCL signal |
| R061 | GDC-GCL+ | 3-split expansion | Cora, CiteSeer, Chameleon | 0,1,2 | skipped | not promoted | GDC did not pass split-0 strength gate |
| R062 | LIFT-PROP-GCL | factor-token proxy | Cora, CiteSeer, Chameleon, Texas, Wisconsin | mixed | done | diagnostic | feature-token useful but not lead; GRAPHITE novelty risk |
| R063 | LIFT-PROP-GCL | raw/graph/feature hetero10 core | Chameleon, Texas, Wisconsin | 0-9 | done | positive | Chameleon `P^2X` 0.685526; WebKB raw dominates |
| R064 | LIFT-PROP-GCL | raw/graph/feature homophily split0 | Cora, CiteSeer | 0 | done | positive | graph/feature propagation beats raw |
| R065 | LIFT-PROP-GCL | K=0..3 lift sweep | Cora, CiteSeer, Chameleon, Texas, Wisconsin | mixed | done | active | K2 edge-lift gate selects oracle K on 4/5 datasets |
| R066 | LIFT-PROP-GCL | novelty check | PROPGCL, Less is More, ASPECT, GRAPHITE, GNNEvaluator, When Do GNNs Help, GLANCE, HLCL | - | done | proceed with caution | novelty `5.5/10`; direct PROPGCL-facing validation required |
| R067 | LIFT-PROP-GCL | formal runner smoke | Cornell | 0 | done | passed | `reproduce_lift_prop.py` summary selects K=0 oracle |
| R068 | LIFT-PROP-GCL | extra hetero10 attempt | Cornell, Actor, Squirrel | 0-9 | partial | Cornell done; Actor slow | interrupted after Cornell due slow Actor linear eval |
| R069 | LIFT-PROP-GCL | extra split-0 check | Actor, Squirrel | 0 | done | positive | Actor selects raw oracle; Squirrel selects K=2 oracle |
| R070 | LIFT-PROP-GCL | fast-grid extra 10-split | Actor, Squirrel | 0-9 | done | mixed-positive | Actor K0 oracle; Squirrel K2 beats raw but K1 is oracle |
| R071 | LIFT-PROP-GCL | selector v1 fast-grid | Actor, Squirrel | 0-9 | done | positive | plateau-aware K1/K2 selector hits oracle on both |
| R072 | LIFT-PROP-GCL | selector v1 aggregate summary | 8 observed settings | mixed | done | positive | v1 hits oracle on 7/8; Cora near miss by 0.0088 |
| R073 | LIFT-PROP-GCL | validation-selected comparison | 8 observed settings | mixed | done | positive | v1 matches validation-selected K on 7/8 without labels |
| R074 | LIFT-PROP-GCL | metric ablation first pass | 8 observed settings | mixed | done | positive | `delta_lift_k2_k0` Pearson 0.915 / Spearman 0.881 with K2 gain |
| R076 | LIFT-PROP-GCL | PROPGCL-facing selector comparison | 8 observed settings | mixed | done-first-pass | positive | v1 mean oracle gap 0.0011 vs PROPGCL reported-step heuristic 0.0111 |
| R077 | LIFT-PROP-GCL | edge-NCE learned propagation mix | Cora, CiteSeer, Chameleon, Texas, Wisconsin | 0 | done | failed | Cora improves locally, but CiteSeer/Chameleon regress; LIFT gate only protects WebKB by falling back to raw |
| R078 | LIFT-PROP-GCL | node-wise LIFT routing | Cora, CiteSeer, Chameleon, Texas, Wisconsin | 0 fast grid | done | failed | Cora node-soft improves, but Chameleon/WebKB regress; row-wise K routing breaks broad representation consistency |
| R079 | LIFT-Stack | split-0 fast gate | Cora, CiteSeer, Chameleon, Texas, Wisconsin | 0 | done | positive | LIFT-gated stack improves Cora/CiteSeer and weakly Chameleon; protects WebKB raw |
| R080 | LIFT-Stack | heterophily fast gate | Chameleon, Texas, Wisconsin, Cornell, Actor, Squirrel | 0-9 | done | positive/low-novelty | Chameleon +0.0070, Squirrel +0.0233, raw-dominant graphs protected |
| R081 | LIFT-Stack | homophily 10-seed gate | Cora, CiteSeer | 0-9 random splits | done | positive/low-novelty | Cora +0.0158 and CiteSeer +0.0305 vs global LIFT; SIGN/FAF/PROPGCL novelty risk high |
| R082 | LIFT-HC-GCL | hop-drop contrastive smoke | Cora, Chameleon | 0 | done | passed/mixed | script works; short smoke showed Cora/Chameleon local gains but needed formal gate |
| R083 | LIFT-HC-GCL | main split-0 gate | Cora, CiteSeer, Chameleon, Texas, Wisconsin | 0 | done | failed/mixed | Cora/Wisconsin positive, Texas protected, CiteSeer/Chameleon regress vs LIFT-Stack |
| R084 | LIFT-HC-GCL | short-training probe | Cora, CiteSeer, Chameleon | 0 | done | failed/mixed | 20 epoch helps Cora/CiteSeer slightly but still hurts Chameleon; 5 epoch not robust |
| R085 | LIFT-Stack + checkpoint residual | existing BGRL/GDC/TD encoder concat | Cora, CiteSeer, Chameleon, Texas, Wisconsin | 0 | done | failed | Cora improves, but CiteSeer/Chameleon/WebKB regress; learned checkpoint branch is not a stable complement to LIFT-Stack |
| R086 | LIFT Channel Gate | channel-wise edge-lift weights over LIFT-Stack | Cora, CiteSeer, Chameleon, Squirrel, WebKB, Actor | mixed | done | failed/diagnostic | Chameleon split-0 softplus improves, but 10-split is neutral and Squirrel relu regresses; keep as diagnostic only |
| R087 | LIFT interaction features | fixed `X*P^kX`, `|P^kX-X|`, and delta blocks | Cora, CiteSeer, Chameleon | 0 fast grid | done | failed | Cora/CiteSeer get tiny variant-specific gains, but Chameleon fails; do not expand fixed-feature micro-tuning |
| R088 | LIFT-Portfolio | raw/P2/stack selector with low-raw-lift guard | Cora, CiteSeer, Chameleon, Squirrel, WebKB, Actor, Cornell | mixed | done | positive baseline | fixes Chameleon full-grid by choosing P2, keeps Cora/CiteSeer/Squirrel stack gains and raw protection; still low novelty |
| R089 | EPI-BGRL | GPU smoke for label-free environment-balanced BGRL | Cora, Chameleon | 0 | done | passed | CUDA training confirmed; no NaN/collapse; smoke only, environment loss mostly inactive |
| R090 | EPI-BGRL | `epi_balanced_rex` vs BGRL control | Cora, CiteSeer, Chameleon, Texas, Wisconsin | 0 | done | failed | Cora improves over BGRL but remains below LIFT-Portfolio; CiteSeer/Chameleon regress; WebKB ties BGRL and is far below raw/LIFT |
| R091 | PAB-BGRL | `pab_soft` CUDA smoke | Cora, Chameleon | 0 | done | passed | CUDA training confirmed; no NaN/collapse; smoke only |
| R092 | PAB-BGRL | `pab_soft` vs BGRL control | Cora, CiteSeer, Chameleon, Texas, Wisconsin | 0 | done | internal signal only | CiteSeer/Chameleon/Texas improve over BGRL, but all remain far below LIFT-Portfolio/raw controls; no 10-split |
| R093 | CCR-GCL | LIFT-Portfolio teacher + orthogonal residual smoke | Cora, Chameleon | 0 | done | passed/risky | CUDA training confirmed; Cora pipeline works; Chameleon residual concat already hurts P2 teacher |
| R094 | CCR-GCL | `ccr_orth_var` split-0 residual gate | Cora, CiteSeer, Chameleon, Texas, Wisconsin | 0 | done | failed certification | Cora improves over portfolio, but certification admits harmful residuals on CiteSeer/Chameleon/WebKB; no 10-split |
| R095 | CCR-SAFE | label-free residual safety policies over R094 checkpoints | Cora, CiteSeer, Chameleon, Texas, Wisconsin | 0 | done | promising diagnostic | `stack_moderate_residual` accepts only Cora and protects CiteSeer/Chameleon/WebKB, but thresholds need fresh-split validation |
| R096 | CCR-SAFE | fixed-threshold fresh-split validation | Cora 1-2, CiteSeer 1 | partial-stopped | failed | CUDA training completed for 3 fresh checkpoints; `stack_moderate_residual` hurts Cora splits 1-2, protects only CiteSeer split 1; remaining queue stopped |
| R097 | SBB-BGRL | spillover-blocked message stop-gradient | Cora, CiteSeer, Chameleon, Texas, Wisconsin | 0 | done | failed | CUDA smoke and M1 passed engineering, but Cora/CiteSeer/Chameleon regress; WebKB gains are weak and far below LIFT/raw |
| R098 | LIFT View-Set Dispersion | fixed propagation-view uncertainty/statistics proxy | Cora, CiteSeer, Chameleon | 0 | partial-stopped | failed | Cora tiny gain, CiteSeer and Chameleon regress; stopped before full grid due decisive proxy failure |
| R099 | LIFT Low-Rank Bottleneck | randomized-SVD low-rank proxy over LIFT-Portfolio | Cora, CiteSeer, Chameleon | 0 | partial-stopped | failed | CiteSeer small-rank gain, but Cora no gain and Chameleon drops sharply; no learned low-rank GCL |
