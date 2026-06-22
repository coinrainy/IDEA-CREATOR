# Experiment Tracker: DCGCL

| Run ID | Milestone | Purpose | System / Variant | Split | Metrics | Priority | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| R001 | M0 | prototype diagnostics | feature teacher, propagation teacher | Cora seed0; Chameleon/Texas/Wisconsin split0 | NMI, ARI, entropy, agreement ratio | MUST | TODO | 不训练 encoder，先验证分歧是否有用 |
| R002 | M1 | smoke | DCGCL | Cora seed0, Chameleon split0 | NaN, rank, entropy, valid/test | MUST | TODO | 5 epochs |
| R003 | M2 | first hetero gate | BGRL, FullLatent, ZPZ, SRLP-Aux, DCGCL | Chameleon split0 | valid@best, test@best | MUST | TODO | 200 epochs |
| R004 | M2 | hetero gate | same as R003 | Texas split0 | valid@best, test@best | MUST | TODO | only after R003 is non-collapse |
| R005 | M2 | hetero gate | same as R003 | Wisconsin split0 | valid@best, test@best | MUST | TODO | compare against adaptive aux Wisconsin positive |
| R006 | M2 | homophily no-regression | BGRL, DCGCL | Cora seed0 | valid@best, test@best | MUST | TODO | ensure no homophily regression |
| R007 | M3 | ablation | DCGCL no-dual-head | Chameleon/Texas/Wisconsin split0 | test@best, bucket accuracy | MUST | TODO | run only if R003-R005 pass |
| R008 | M3 | ablation | DCGCL single-teacher | Chameleon/Texas/Wisconsin split0 | test@best, entropy | MUST | TODO | isolates dual-teacher contribution |
| R009 | M3 | ablation | DCGCL no-gate | Chameleon/Texas/Wisconsin split0 | test@best, high-disagreement accuracy | MUST | TODO | isolates disagreement gate |
| R010 | M4 | 10-split gate | best control vs DCGCL | Chameleon splits 0-9 | mean +/- std | MUST-GATED | TODO | only after M2/M3 pass |
| R011 | M4 | 10-split gate | best control vs DCGCL | Texas splits 0-9 | mean +/- std | MUST-GATED | TODO | only after M2/M3 pass |
| R012 | M4 | 10-split gate | best control vs DCGCL | Wisconsin splits 0-9 | mean +/- std | MUST-GATED | TODO | only after M2/M3 pass |
| R013 | M4 | 10-split gate | best control vs DCGCL | Actor splits 0-9 | mean +/- std | NICE | TODO | Actor was weak for SRLP; don't lead with it |
