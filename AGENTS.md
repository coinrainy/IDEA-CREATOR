<!-- ARIS-CODEX:BEGIN -->
## ARIS Codex Skill Scope
ARIS Codex packages installed in this project: skills-codex
Managed entries: 80
Manifest: `.aris/installed-skills-codex.txt`
ARIS repo root: `/root/aris_repo`
Project skill path: `.agents/skills/<skill-name>`
For ARIS Codex workflows, prefer the project-local skills under `.agents/skills/`.
When a skill needs ARIS helper scripts, resolve the repo root from the manifest or set it explicitly:
`ARIS_REPO=$(awk -F'\t' '$1=="repo_root"{print $2; exit}' "/root/autodl-tmp/IDEA-CREATOR/.aris/installed-skills-codex.txt")`
Do not edit or delete symlinked skills in place; update upstream or rerun:
`bash /root/aris_repo/tools/install_aris_codex.sh "/root/autodl-tmp/IDEA-CREATOR" --reconcile`
For copied Codex installs, use:
`bash /root/aris_repo/tools/smart_update_codex.sh --project "/root/autodl-tmp/IDEA-CREATOR"`
<!-- ARIS-CODEX:END -->

## Project Handoff Notes

Last reviewed: 2026-06-21.

Latest task sync:
- 2026-06-21: Implemented the post-review SRLP-Aux revision and ran the 5-run
  Go/Kill gate. SRLP-Aux uses a single-head mixed target
  `normalize(z_hat + lambda_t * w * r_hat)` with `lambda_max=0.1`, `tau=0.15`,
  and 10% warmup. Smoke passed. Gate results passed: SRLP-Aux improved over
  old SRLP hard on Chameleon/Texas/Wisconsin/Actor/CiteSeer (5/5), reached or
  matched the strongest target-family result on Chameleon and Texas (2/4
  heterophily gate), and had no NaN/collapse. Current canonical proposal is
  `refine-logs/FINAL_PROPOSAL.md` for SRLP-Aux. Next step: limited 10-split
  target-family internal ablation; keep external strong-baseline paper table
  paused.
- 2026-06-21: Completed a method-only strict review of SRLP after the M2
  pilot results. Verdict: DOWNGRADE. Hard isolation does reduce leakage, but
  the residual-only target is internally misaligned with the reachable online
  signal and loses task-relevant latent information. Recommended revision is to
  demote SRLP from a standalone objective to an energy-gated residual auxiliary
  on top of a FullLatent primary objective, with a 3-5 run Go/Kill gate before
  abandoning the standalone SRLP claim.
- 2026-06-21: Continued the SRLP experiment bridge through M2. Cora/CiteSeer
  200-epoch pilots completed, Chameleon was extended to 1000 epochs, and
  Cornell/Texas/Wisconsin/Actor split-0 1000-epoch target-family ablations
  completed sequentially on the 4060. Engineering and leakage checks pass, but
  the method-effect criterion does not: SRLP has 0/5 clear wins over the
  strongest target-family ablation across Cornell/Texas/Wisconsin/Actor/
  Chameleon split 0, with Cornell only tied. Pause 10 split and external
  strong-baseline expansion until the residual target design is revised.
- 2026-06-21: User preference update: experiment progress and results should
  be reported in Chinese by default, with numeric metrics shown in tables when
  possible and a clear pass/fail/next-step interpretation after each batch.
- 2026-06-21: Implemented the SRLP 4060 small-graph experiment bridge inside
  the nested `baselines/BGRL` checkout. Added SRLP utilities, training runner,
  sequential reproducer, leakage probe, Cora/CiteSeer fixed split files, and
  JSON/CSV output protocol. Codex subagent review verdict was PASS_WITH_FIXES;
  fixes applied include strict hard-isolation self-loop control, expanded CSV
  traceability fields, CiteSeer split pre-generation, and dataset path casing.
  M0 Cora/Chameleon smoke passed; Chameleon 200-epoch target-family pilot is
  positive for SRLP against FullLatent/ZPZ/NoIso but still below BGRL.
- 2026-06-21: Organized the SRLP idea-discovery and refinement artifacts for
  Git tracking and pushed them to `origin/master`. Commit scope includes the
  latest SRLP idea report, reviewer/refinement logs, formula-tightened final
  proposal, research-wiki notes, manifest entries, and this handoff update.
- 2026-06-21: Tightened SRLP final formulas in
  `refine-logs/FINAL_PROPOSAL.md`: added teacher-side stop-gradient, normalized
  context direction, `epsilon`/`T_valid`/`skipped_ratio`, explicit
  `A_online` target-incident-edge masking, online context normalization, and
  made `L_var` a collapse-only fallback rather than part of the main method.
- 2026-06-21: Completed a first-round senior-reviewer method audit of
  `refine-logs/round-0-initial-proposal.md` for SRLP-GCL. Verdict: REVISE,
  weighted score 5.95/10. Main required revisions are to make the residual
  target explicitly context-unpredictable rather than merely `Z - alpha PZ`,
  strengthen target leakage control, and demote conditional InfoNCE from the
  first implementation. Review saved at
  `refine-logs/round-0-method-review.md`.
- 2026-06-21: Completed a second-round review of
  `refine-logs/round-1-refinement.md`. Verdict: READY for pilot, weighted
  score 7.35/10. The context-projected residual and target-isolated online
  encoding are sufficient for a small BGRL-based pilot; remaining risk is
  empirical predictability of the residual after hard isolation. Review saved
  at `refine-logs/round-1-method-review.md`.

Communication preference:
- Use Chinese when explaining research ideas, novelty, experiment status, and
  implementation decisions. Avoid unnecessary English terminology; when a
  technical term, paper title, file name, or command must stay in English,
  explain it in Chinese immediately.
- For literature search and novelty checks, prioritize recent papers from the
  last two years and always check the most recent 6 months. Only use older
  papers when they are foundational or uniquely representative.
- For experiment reporting, describe each run batch in Chinese. Prefer compact
  tables for metrics such as validation accuracy, test accuracy, prediction
  cosine, residual norm, skipped ratio, effective rank, probe cosine, and MSE;
  after the table, add a short interpretation: passed / failed / inconclusive
  and the recommended next action.

This workspace is a research project for graph contrastive learning node
classification. The previous selected research direction was NFR-GCL
(Node-Frequency Routed Graph Contrastive Learning), but it was abandoned on
2026-06-21 before implementation because the chance of making it a strong new
paper contribution is low after novelty checking.

Key artifacts:
- `MANIFEST.md` tracks ARIS-generated outputs.
- `idea-stage/IDEA_REPORT.md` now contains the latest latent-prediction idea
  report for SRLP-GCL. Older timestamped reports still preserve the historical
  NFR-GCL discovery state.
- `idea-stage/IDEA_CANDIDATES.md` contains the 2026-06-21 candidate pool for
  latent-prediction graph contrastive learning.
- `refine-logs/FINAL_PROPOSAL.md` now contains the refined SRLP proposal.
- `refine-logs/EXPERIMENT_PLAN.md` is historical. `refine-logs/EXPERIMENT_TRACKER.md`
  marks NFR-GCL runs as cancelled and keeps the I6 backup pending decision.
- `research-wiki/` stores paper notes, gap map, idea pages, and graph edges.
- `baselines/` contains local baseline code, datasets, split files, run logs,
  and reproduction summaries.

Implementation orientation:
- Do not implement NFR-GCL unless the user explicitly reverses the decision.
- If the user wants to continue from the old backup, inspect
  `research-wiki/ideas/heterophilous_edge_reconstruction.md` first and reassess
  novelty before writing code.
- If a new method is selected later, prefer a small pilot inside the existing
  `baselines/` harness rather than starting a new large code stack.
- The currently selected paper-only candidate is SRLP
  (Shortcut-Resistant Latent Prediction), documented in
  `research-wiki/ideas/srlp_gcl.md`. It is refined and ready for a small
  BGRL-based pilot, but has not been implemented or empirically validated yet.
- Preserve the protocol in `baselines/reproduction_protocol.md`: heterophily
  datasets must use Geom-GCN official fixed splits from
  `baselines/dataset_splits/heterophily/geom-gcn/`, not random splits.
- Run baseline experiments sequentially with CPU thread caps unless there is an
  explicit protocol exception.

Novelty status update:
- 2026-06-21 novelty scan found ASPECT (arXiv 2604.01878, 2026), which directly
  overlaps with node-level adaptive spectral fusion for graph contrastive
  learning. Original NFR-GCL should be treated as LOW-to-MEDIUM novelty unless
  reframed around a clear delta: mid-band routing, label-free compatibility
  router features, stronger diagnostics, and direct comparison to ASPECT.
- Do not claim NFR-GCL is the first node-wise spectral/frequency routing GCL
  method. Add ASPECT as required closest prior work/baseline for any paper plan.
- User decision on 2026-06-21: abandon NFR-GCL rather than spend experiment time
  on a low-novelty direction.
- 2026-06-21 cross-domain transfer survey saved at
  `idea-stage/CROSS_DOMAIN_TRANSFER_GCL_20260621.md`. Strongest directions to
  investigate next are latent-prediction graph contrastive learning,
  invariant-environment graph contrastive learning, and optimal-transport soft
  alignment for edge/semantic compatibility.
- 2026-06-21 latent-prediction scan selected SRLP as the next active idea. A
  two-round reviewer refinement changed the target from `Z - alpha PZ` to a
  context-projected residual: remove only the component of the target teacher
  latent explained by the visible context subspace, then predict that residual
  from a target-isolated online graph. Closest risks are Graph-JEPA,
  GraphMAE2, BGRL, JPEB-GSSL/Predict-Cluster-Refine, ASPECT, and SPGCL. Do not
  claim generic graph latent prediction is novel; the novelty claim must be
  target construction for shortcut-resistant node-level graph SSL.

Repository status note:
- This checkout was initialized locally. The outer repository should track
  research documents, protocol files, fixed split masks, and result summaries.
- Baseline method directories under `baselines/` are nested Git repositories
  and are ignored by the outer repository to avoid accidental gitlink commits.
- GitHub remote is configured as
  `origin=https://github.com/coinrainy/IDEA-CREATOR.git`; `master` tracks
  `origin/master`.
