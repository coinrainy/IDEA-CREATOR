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

Communication preference:
- Use Chinese when explaining research ideas, novelty, experiment status, and
  implementation decisions. Avoid unnecessary English terminology; when a
  technical term, paper title, file name, or command must stay in English,
  explain it in Chinese immediately.

This workspace is a research project for graph contrastive learning node
classification. The previous selected research direction was NFR-GCL
(Node-Frequency Routed Graph Contrastive Learning), but it was abandoned on
2026-06-21 before implementation because the chance of making it a strong new
paper contribution is low after novelty checking.

Key artifacts:
- `MANIFEST.md` tracks ARIS-generated outputs.
- `idea-stage/IDEA_REPORT.md` is the historical idea-discovery report; it still
  says NFR-GCL was active at generation time, but that status is now stale.
- `refine-logs/FINAL_PROPOSAL.md` contains the refined NFR-GCL method thesis.
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

Repository status note:
- This checkout was initialized locally. The outer repository should track
  research documents, protocol files, fixed split masks, and result summaries.
- Baseline method directories under `baselines/` are nested Git repositories
  and are ignored by the outer repository to avoid accidental gitlink commits.
- GitHub remote is configured as
  `origin=https://github.com/coinrainy/IDEA-CREATOR.git`; `master` tracks
  `origin/master`.
