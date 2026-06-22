# Experiment Tracker: NPG-GCL Pilot

**Date**: 2026-06-22 10:10  
**Subagent reviewer policy**: disabled for ad-hoc reviewer/code-review subagents only.  

| Run ID | Candidate | Variant | Dataset(s) | Split(s) | Status | Result | Notes |
|---|---|---|---|---|---|---|---|
| R049 | NPG-GCL | npg smoke | Cora, Chameleon | 0 | pending | - | 5 epochs |
| R050 | NPG-GCL | bgrl_control | Cora, CiteSeer, Chameleon, Texas, Wisconsin | 0 | pending | - | same-run no-gain control |
| R051 | NPG-GCL | npg | Cora, CiteSeer, Chameleon, Texas, Wisconsin | 0 | pending | - | main split-0 pilot |
| R052 | NPG-GCL | uniform_gain | Cora, Chameleon | 0 | pending | - | ablation |
| R053 | NPG-GCL | random_gain | Cora, Chameleon | 0 | pending | - | ablation |
| R054 | NPG-GCL | npg 3-split | Cora, CiteSeer, Chameleon, Texas, Wisconsin | 0,1,2 | blocked | - | run only if R051 passes |
