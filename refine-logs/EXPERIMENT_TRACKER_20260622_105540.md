# Experiment Tracker: Post-TDGCL Pilot Queue

**Date**: 2026-06-22 10:55  
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
