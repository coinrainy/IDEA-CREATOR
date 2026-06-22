# Post-FTDR Idea Discovery: RFA-BGRL

**Date**: 2026-06-22  
**Skill**: idea-discovery  
**Scope**: graph contrastive learning for node classification  

## Failure Constraints From Previous Routes

SRLP, DCGCL, and FTDR created useful negative constraints:

- Do not assume a harder latent target is more class-relevant.
- Do not use global prototype positives unless their activation rule is robust across official splits.
- Do not add another teacher-routing threshold after FTDR; simple routing tied or regressed.
- Do not trust split-0 positives without a 10-split gate.

The CFR-BGRL pilot added one more constraint: a learned feature channel trained by bootstrap invariance can still forget the raw feature signal that is already linearly useful for node classification.

## Literature Boundary

Recent closest work makes this direction crowded:

- **Less is More: Towards Simple Graph Contrastive Learning** (arXiv 2509.25742) uses GCN and MLP views and argues for simple feature/structure complementarity on heterophilic graphs: <https://arxiv.org/abs/2509.25742>.
- **Training MLPs on Graphs without Supervision / SimMLP** (arXiv 2412.03864) aligns GNN and MLP representations to integrate structural information into MLPs: <https://arxiv.org/abs/2412.03864>.
- **SPGCL / Revisiting Positive Samples in GCL** (arXiv 2606.10284) argues message passing can trivialize positives and separates feature propagation by Dirichlet energy: <https://arxiv.org/abs/2606.10284>.
- **GCL-OT** (arXiv 2511.16778) addresses heterophilic text-attributed graphs through structure-text optimal transport: <https://arxiv.org/abs/2511.16778>.

Therefore a raw-feature/graph dual-channel method is not novel by itself. The viable novelty angle must be **feature-retention as anti-forgetting**, not generic two-view GCL.

## Candidate Pool

| Rank | Candidate | Mechanism | Strength | Risk | Decision |
|---:|---|---|---|---|---|
| 1 | RFA-BGRL: Raw-Feature Anchored Bootstrap GCL | BGRL graph branch plus a protected raw-feature anchor in the final representation | Strongly exposes feature forgetting; very strong on Texas/Wisconsin | Close to GCN-MLP/SimMLP and partly raw-feature baseline | ACTIVE-DIAGNOSTIC |
| 2 | ORFA-GCL: Orthogonal Raw-Feature Anchor | Preserve raw anchor, force graph branch to learn only residual information not linearly explained by raw features | Better novelty; can justify complementarity | Needs careful implementation; current RFA does not yet prove residual gain | NEXT |
| 3 | Drift-Calibrated Anchor Fusion | Choose anchor weight from unsupervised graph-feature drift | Could fix Chameleon/Texas scale mismatch | Current drift features do not cleanly explain best scale | HOLD |
| 4 | Validation-Calibrated Anchor Fusion | Treat anchor scale as a validation-selected representation hyperparameter | Practical and strong | Less methodologically clean; may be considered tuning | HOLD |
| 5 | Raw Feature Only Control | No GCL, linear probe on raw features | Essential sanity baseline | Not a graph contrastive learning method | CONTROL |

## Selected Candidate

The selected candidate is **RFA-BGRL**, best understood as a feature-retentive graph contrastive baseline:

```text
z_g = BGRL_GCN(A, X)
z_x = normalize(X)
z_final = normalize([z_g || alpha z_x])
```

It deliberately protects raw node features from being overwritten by graph contrastive augmentation. The paper-level version should become **ORFA-GCL**: retain the raw anchor and train the graph branch to add orthogonal graph residual information, not to relearn or corrupt the anchor.

## Minimal Gate

RFA-BGRL is worth keeping because it passes an empirical diagnostic that the previous candidates missed:

- Chameleon 200-epoch split-0: RFA `0.4671`, raw `0.4408`, graph `0.4123`.
- Texas 10-split 200-epoch: RFA mean `0.7622`, best prior local control `0.6135`.
- Wisconsin 10-split 200-epoch: RFA mean `0.8098`, best prior local control `0.6039`.
- No NaN/collapse in all RFA runs.

But it is not yet a final method:

- Chameleon 10-split 1000-epoch mean is `0.4928`, below the strict prior control `0.5004`.
- Texas/Wisconsin gains are largely explained by raw features; raw-only is stronger than RFA on average.
- Anchor scale is dataset-dependent, which means fixed fusion is not enough.

## Decision

Keep RFA-BGRL as the current strongest diagnostic candidate and baseline. Do not claim a 2026 paper-level method yet. The next method step should be ORFA-GCL or drift-calibrated feature retention, with the hard requirement that it beats raw-only on Texas/Wisconsin while retaining the Chameleon gain.
