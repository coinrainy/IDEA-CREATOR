# Idea Candidates: Role-Signature Restart

| Rank | Candidate | Mechanism | Current Evidence | Risk | Status |
|---:|---|---|---|---|---|
| 0 | TD-GCL | training-dynamics positives from similar embedding update trajectories | Cora +0.035533, CiteSeer +0.016905, Chameleon +0.010965 over no-dyn split-0 | novelty/robustness unverified; WebKB no gain | SPECULATIVE_INCUBATE |
| 1 | RSP-GCL | Role/WL/landmark signatures define nonlocal structure-equivalent positives for GCL | Chameleon training 10-split `0.573684`; gate `0.574781` | GALE/WLGCL novelty overlap; WebKB raw-dominant | DIAGNOSTIC_ONLY_AFTER_GATE |
| 2 | Validation-gated RSP | choose role branch only when validation supports it | Chameleon selects role 10/10; Texas/Wisconsin mostly fall back to raw | protects but does not improve raw-dominant graphs | DIAGNOSTIC_ONLY |
| 3 | Label-free role reliability gate | detect when role signatures are useful without labels | not implemented | difficult but publication-cleaner | SPECULATIVE |
| 4 | WL-only RSP | use WL-hash signature as the main role view | `graph_raw_wl` Chameleon 10-split `0.578290` | close to structural role/WL prior work | BACKUP |
| 5 | Landmark diffusion RSP | use landmark position response as a positional view | only helps in full combination on Chameleon | close to positional encoding papers | HOLD |
| 6 | Training-dynamics curriculum GCL | choose positives from stable/unstable representation dynamics | not tested | separate family, compute cost unclear | SPECULATIVE |
| 7 | Role-conditioned invariance | enforce augmentation invariance conditioned on role bins | not tested | likely an ablation of RSP, not standalone | BACKUP |
| 8 | DCA/AnchorBank | frozen raw/low/high/DCA representation family | Chameleon `0.505044`, Cora/CiteSeer positive | novelty score about 3/10 | DIAGNOSTIC_ONLY |
| 9 | CIG/CLEAR | counterfactual edge masks | Texas/Wisconsin 10-split failed vs raw | close to adaptive augmentation/edge pruning | STOP |
| 10 | VST-GCL | sparse local transport target | split-0 and low-aux gates failed | weak semantic-kNN-like signal | STOP |
| 11 | SBN-GCL | semantic kNN positives plus boundary negatives | split-0 heterophily failure | close to positive-sample prior | STOP |

## Immediate Gate

RSP-GCL completed its immediate gates and did not promote to `READY_TO_REFINE`.

- Chameleon 10-split training passed narrowly: role-fused `0.573684 +/- 0.026265`.
- Role gate protects Texas/Wisconsin only by falling back to raw, without gains.
- Direct novelty check found strong overlap with GALE, WLGCL, and SPGCL.

Next action: keep TD-GCL as a small incubated route, but do not promote it
until multi-seed/split homophily validation and a direct novelty check pass.
In parallel, continue idea discovery for a more broadly positive mechanism.
