# Post-DCGCL Idea Discovery

**Date**: 2026-06-22  
**Direction**: graph contrastive / self-supervised learning for node classification  
**Status**: new route selected for minimal pilot; not yet empirically validated

## Constraints From Failed Routes

SRLP and DCGCL produced useful negative evidence:

- Do not optimize a residual or shortcut-resistant target unless its task relevance is directly protected.
- Do not use global prototype positives as the main objective unless a label-free activation rule is stable across datasets and splits.
- Do not expand split-0 positives. DCGCL V1 looked good on Texas/Wisconsin split 0, but failed 10-split on Chameleon and Texas.
- The next method should have a simple fallback to standard BGRL behavior on homophilous or high feature-topology agreement graphs.

## Recent-Literature Boundary

The next route should not be a spectral/frequency routing method or a generic multi-topology contrast method:

- HLCL already studies graph contrastive learning under heterophily with graph filters and homophilic/heterophilic subgraphs.
- MCGRL studies multi-topology contrastive graph representation learning.
- SFCLTA is listed as an ICML 2026 spectral fusion contrastive learning method with topology-adaptive graph augmentation.
- Recent graph SSL work also emphasizes capturing both structure and feature signals, so a new method must be more specific than "combine features and topology."

## Candidate Pool

| Rank | Idea | Core Mechanism | Why It Might Work | Main Risk | Status |
|---:|---|---|---|---|---|
| 1 | FTDR-BGRL: Feature-Topology Disagreement-Routed Bootstrap | Per-node route between topology teacher and feature-only teacher inside BGRL target construction | Avoids global prototypes; falls back to BGRL when feature/topology agree; activates feature teacher only where propagation is likely harmful | May collapse to feature-only MLP on heterophily or fail to beat FullLatent controls | ACTIVE |
| 2 | Jackknife-Influence Bootstrap | Estimate node sensitivity by edge jackknife/dropout and downweight unstable topology targets | Directly addresses topology shortcut and noisy edges without labels | Extra per-epoch teacher passes may be slow; sensitivity may not align with labels | SPECULATIVE |
| 3 | Local Rank-Agreement Contrast | Use node-specific top-k feature-neighbor and topology-neighbor rank overlap instead of global prototypes | Avoids DCGCL's global pseudo-class failure | Close to positive-sample mining literature; needs careful novelty separation from SPGCL/HEATS | DEPRIORITIZED |
| 4 | Environment-Split Consistency GCL | Treat augmentation families as environments and learn invariant representation plus disagreement residual | Could connect to invariant learning and heterophily | Prior invariant GCL work likely overlaps; needs a stronger setting | SPECULATIVE |
| 5 | Signed Compatibility Bootstrap | Learn separate same-class-like and different-class-like channels from feature/topology compatibility | Directly targets heterophily | Risky without labels; can become another unstable gating method | DEPRIORITIZED |

## Selected Idea: FTDR-BGRL

**Thesis**: For each node, a graph SSL target should be routed between a topology-preserving teacher and a feature-only teacher based on label-free feature-topology disagreement. When topology and feature teachers agree, the method reduces to BGRL-like bootstrapping. When they disagree, the target shifts toward feature-only semantics instead of forcing graph-propagated noise into the representation.

For node `v`:

```text
z_g(v) = stopgrad(target_encoder(G, X)_v)
z_f(v) = stopgrad(target_encoder(I, X)_v)
d_v = 1 - cosine(z_g(v), z_f(v))
w_v = sigmoid((d_v - tau_d) / temp)
y_v = normalize((1 - w_v) * z_g(v) + w_v * z_f(v))
L = mean_v [1 - cosine(p_v, y_v)]
```

Optional guardrails:

- warm up `w_v` from 0 to its routed value over the first 10% of epochs;
- clamp route weight with `w_max <= 0.5` in the first pilot;
- report route mean, route entropy, feature/topology cosine, effective rank, and no-collapse flags.

## Why This Is Different From SRLP/DCGCL

- Unlike SRLP, it does not remove a residual component and assume the residual is task-relevant.
- Unlike DCGCL, it does not create global pseudo-classes or global positives.
- Unlike spectral/frequency routing, it routes teacher targets in latent bootstrap space, not graph filters.
- Unlike generic attribute/structure preservation, the routing variable is node-level teacher disagreement and the fallback path is explicit BGRL behavior.

## First Fair Pilot

Implement inside `baselines/BGRL` as `target_mode=ftdr_bgrl`.

Run order:

| Run | Dataset | Split | Epochs | Purpose | Gate |
|---|---|---|---:|---|---|
| M0 | Cora, Chameleon | fixed seed0 / Geom-GCN split0 | 5 | smoke, route diagnostics, no collapse | no NaN/collapse |
| M1 | Cora, Chameleon, Texas, Wisconsin | split0 | 200 | first method signal | no Cora regression > 1.5 pt; improve or tie 2/3 heterophily |
| M2 | Chameleon/Texas/Wisconsin | splits 0-9 | 200 | decisive internal gate | beat best target-family mean on at least 2/3 datasets |

Decision rule: do not run external strong baselines unless M2 passes.

## Immediate Next Step

Implement the minimal FTDR-BGRL runner and smoke test. If M1 fails in the same pattern as DCGCL, stop and re-run a wider idea search rather than adding more routing variants.
