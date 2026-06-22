# Experiment Tracker

| Run ID | Milestone | Purpose | System / Variant | Split | Metrics | Priority | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| R001 | M0 | sanity | NFR-GCL full | Chameleon split0 | loss, acc | MUST | TODO | Confirm router not collapsed |
| R002 | M1 | main pilot | NFR-GCL full | Actor 10 official splits | Acc/F1Mi | MUST | TODO | Compare PolyGCL/GRASS/EDA-GCL |
| R003 | M1 | main pilot | NFR-GCL full | Chameleon 10 official splits | Acc/F1Mi | MUST | TODO | Primary heterophily anchor |
| R004 | M1 | main pilot | NFR-GCL full | Squirrel 10 official splits | Acc/F1Mi | MUST | TODO | Hardest larger heterophily graph |
| R005 | M2 | ablation | global-router | Actor/Chameleon/Squirrel | Acc/F1Mi | MUST | TODO | Tests node-local value |
| R006 | M2 | ablation | random-router | Actor/Chameleon/Squirrel | Acc/F1Mi | MUST | TODO | Tests learned routing |
| R007 | M2 | ablation | no-mid-band | Actor/Chameleon/Squirrel | Acc/F1Mi | MUST | TODO | Tests mixed-frequency consistency |
| R008 | M2 | ablation | no-compatibility | Actor/Chameleon/Squirrel | Acc/F1Mi | MUST | TODO | Tests I2 signal as input only |
| R009 | M3 | no-regression | NFR-GCL full | Cora/CiteSeer smoke | Acc/F1Mi | MUST | TODO | Drop must be <=1 point |
| R010 | M4 | backup | I6 GRASS-based | Cornell/Texas/Wisconsin | Acc/F1Mi | BACKUP | TODO | Run only if NFR-GCL misses gate |

