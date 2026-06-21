# Experiment Tracker: SRLP 4060 Small-Graph Pilot

| Run ID | Milestone | Purpose | System / Variant | Dataset / Split | Metrics | Priority | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| R001 | M0 | Smoke | SRLP hard | Cora fixed split seed 0 | JSON/CSV, skipped ratio, rank | MUST | DONE | `test@best=0.76927`, `skipped_ratio=0.04613`, no NaN/collapse. |
| R002 | M0 | Smoke | SRLP hard | Chameleon Geom-GCN split 0 | JSON/CSV, skipped ratio, rank | MUST | DONE | Initial directed-context run had high skipped ratio; undirected context fixed it to `0.00879`. Strict target self-loop isolation is now enforced. |
| R003 | M1 | Mechanism pilot | FullLatent-Iso | Chameleon split 0, 200 epochs | valid/test + diagnostics | MUST | DONE | `test@best=0.41886`. |
| R004 | M1 | Mechanism pilot | ZPZ-Iso | Chameleon split 0, 200 epochs | valid/test + diagnostics | MUST | DONE | `test@best=0.40132`. |
| R005 | M1 | Mechanism pilot | SRLP hard | Chameleon split 0, 200 epochs | valid/test + diagnostics | MUST | DONE | `test@best=0.42325`, `skipped_ratio=0.02857`; target-family positive but below BGRL. |
| R006 | M1 | Leakage control | SRLP-NoIso | Chameleon split 0, 200 epochs | valid/test + diagnostics | MUST | DONE | `test@best=0.41886`. |
| R007 | M1 | Baseline comparison | BGRL | Chameleon split 0, 200 epochs | valid/test + diagnostics | MUST | DONE | `test@best=0.43860`. |
| R008 | M5 | Leakage probe | SRLP hard | Chameleon split 0 checkpoint | probe cosine/MSE | MUST | DONE | probe cosine `0.27185`, MSE `0.00362`. |
| R009 | M5 | Leakage probe | SRLP-NoIso | Chameleon split 0 checkpoint | probe cosine/MSE | MUST | DONE | probe cosine `0.63130`, MSE `0.00236`. |
| R010 | M1 | Mechanism pilot | 5 variants | Cora fixed split seed 0, 200 epochs | valid/test + diagnostics | MUST | TODO | Next after implementation checkpoint. |
| R011 | M1 | Mechanism pilot | 5 variants | CiteSeer fixed split seed 0, 200 epochs | valid/test + diagnostics | MUST | TODO | Next after Cora M1. |
| R012 | M3 | Heterophily split-0 expansion | 4 target variants | Cornell/Texas/Wisconsin/Actor/Chameleon split 0 | valid/test + diagnostics | MUST | TODO | Run only after deciding Chameleon signal is worth expanding. |

## Output Locations

- Smoke and M1 results: `baselines/BGRL/runs/srlp*/`
- Chameleon M1 summary CSV: `baselines/BGRL/runs/srlp_m1_chameleon200_fixed_selfloops/results.csv`
- SRLP implementation files: `baselines/BGRL/bgrl/srlp_utils.py`, `baselines/BGRL/train_srlp_transductive.py`, `baselines/BGRL/reproduce_srlp.py`, `baselines/BGRL/probe_srlp_leakage.py`

Note: `baselines/BGRL/` is an ignored nested repository in the outer project, so implementation code is local to that nested checkout unless separately committed there.
