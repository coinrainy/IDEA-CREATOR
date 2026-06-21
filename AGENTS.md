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

This workspace is a research project for graph contrastive learning node
classification. The current selected research direction is NFR-GCL
(Node-Frequency Routed Graph Contrastive Learning): add node-wise routing over
low/mid/high frequency views, implemented as a minimal PolyGCL/ChebNetII-based
extension rather than a new model stack.

Key artifacts:
- `MANIFEST.md` tracks ARIS-generated outputs.
- `idea-stage/IDEA_REPORT.md` is the idea-discovery report; NFR-GCL is active
  and ready for pilot, with masked heterophilous edge reconstruction as backup.
- `refine-logs/FINAL_PROPOSAL.md` contains the refined NFR-GCL method thesis.
- `refine-logs/EXPERIMENT_PLAN.md` and `refine-logs/EXPERIMENT_TRACKER.md`
  define the go/no-go experiment plan.
- `research-wiki/` stores paper notes, gap map, idea pages, and graph edges.
- `baselines/` contains local baseline code, datasets, split files, run logs,
  and reproduction summaries.

Implementation orientation:
- Prefer editing/adding code under `baselines/PolyGCL` for NFR-GCL pilots.
- The most relevant PolyGCL files are `model.py`,
  `reproduce_10run_101080.py`, and `reproduce_hetero_fixed_splits.py`.
- Preserve the protocol in `baselines/reproduction_protocol.md`: heterophily
  datasets must use Geom-GCN official fixed splits from
  `baselines/dataset_splits/heterophily/geom-gcn/`, not random splits.
- Run baseline experiments sequentially with CPU thread caps unless there is an
  explicit protocol exception.
- Main pilot target: Actor, Chameleon, and Squirrel official 10 splits.
  Success requires average improvement over the best local baseline by at least
  1.5 accuracy points and wins on at least 2 of 3 datasets.
- Homophily no-regression checks are Cora/CiteSeer smoke runs with no drop over
  1 point.

Repository status note:
- This checkout was initialized locally. The outer repository should track
  research documents, protocol files, fixed split masks, and result summaries.
- Baseline method directories under `baselines/` are nested Git repositories
  and are ignored by the outer repository to avoid accidental gitlink commits.
- GitHub/PR status still requires a configured `origin` remote.
