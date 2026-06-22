# SRLP Label-Alignment Method Review

**Date**: 2026-06-22  
**Scope**: method-level judgment only, based on target-family 10-split results and label-alignment diagnostics. This review does not recommend external baselines or large-graph expansion.

## Verdict

**RETHINK**, not yet **KILL**.

The unified rank-1 residual hypothesis is no longer defensible. However, the diagnostics still show usable structure: Chameleon benefits from context-projected signal, while Texas and Wisconsin expose stronger multi-direction residual signal. The viable next step is not "stronger SRLP", but an adaptive decomposition target that decides, without labels, whether to emphasize context-aligned signal, residual signal, or mostly keep the full latent target.

## Core Interpretation

1. **Rank-1 residual is not a universal target.** Chameleon rank-k residual remains below full latent, while Texas/Wisconsin rank-k residual is clearly above full latent.

2. **Context projection is not always a shortcut.** On Chameleon, the projection component has much stronger label alignment than the residual, so subtracting it destroys useful task signal.

3. **Texas/Wisconsin failures are target-interface failures, not residual-signal absence.** Their residual components are useful, but the current weak single rank-1 SRLP-Aux mixture does not transfer that signal reliably.

4. **Actor should not drive the redesign.** All components are near the same low alignment regime, so Actor is mostly a robustness/no-harm check.

## Minimal Next Method

Keep full latent as the primary target and add only a small label-free adaptive decomposition. For node \(v\), teacher latent \(z_v\), local context subspace \(U_{v,k}\), define:

```text
p_{v,k} = U_{v,k} U_{v,k}^T z_v
r_{v,k} = z_v - p_{v,k}
```

Use small \(k \in \{1,2,4\}\), selected by context effective rank and capped to avoid a new large module:

```text
k(v) = min { k in {1,2,4} : sum_{i<=k} sigma_i^2 / sum_i sigma_i^2 >= gamma }
```

The next target should preserve projection by default:

```text
y_v = normalize(
  z_v
  + lambda_r * g_r(v) * normalize(r_{v,k(v)})
  + lambda_p * g_p(v) * normalize(p_{v,k(v)})
)
```

with small fixed weights, for example `lambda_r <= 0.1`, `lambda_p <= 0.1`. Do not use residual-only training.

One simple label-free gate is:

```text
rho_r(v) = ||r_{v,k}||^2 / (||p_{v,k}||^2 + ||r_{v,k}||^2 + eps)
rho_p(v) = ||p_{v,k}||^2 / (||p_{v,k}||^2 + ||r_{v,k}||^2 + eps)
s_r(v)   = cos(r_{v,k}^{aug1}, r_{v,k}^{aug2})
s_p(v)   = cos(p_{v,k}^{aug1}, p_{v,k}^{aug2})
a_r(v)   = cos(normalize(r_{v,k}), normalize(z_v - Pz_v))

g_r(v) = clip((rho_r(v)-tau_r)/(1-tau_r), 0, 1)
         * clip((s_r(v)-tau_s)/(1-tau_s), 0, 1)
         * clip((a_r(v)-tau_a)/(1-tau_a), 0, 1)

g_p(v) = clip((rho_p(v)-tau_p)/(1-tau_p), 0, 1)
         * clip((s_p(v)-tau_s)/(1-tau_s), 0, 1)
```

Interpretation:

- Use multi-direction residual only when the residual has enough energy, perturbation stability, and agreement with propagation residual.
- Keep projection through the base \(z_v\), and optionally reinforce it when the projection is stable.
- If this gate cannot separate Chameleon from Texas/Wisconsin without labels, SRLP should be downgraded to a diagnostic rather than a paper method.

## Claims To Downgrade

- Downgrade "residual-only / rank-1 residual is the right shortcut-resistant target" to "residual signal can be useful only under label-free evidence of residual reliability."
- Downgrade "context-projected information is a shortcut to remove" to "context-projected and residual components have dataset-dependent semantic value."
- Downgrade "SRLP-Aux is a general node-classification improvement" to "SRLP-Aux is a weak auxiliary target with limited positive evidence."
- Do not claim broad heterophily robustness, SOTA readiness, or external-baseline competitiveness from the current evidence.

## Minimal Verification Gate

No expanded main table.

1. **Pure diagnostic gate check on existing checkpoints.** Pass only if the label-free gate gives low residual weight on Chameleon/Actor and higher residual weight on Texas/Wisconsin, while projection weight remains high on Chameleon.

2. **Three-run pilot only if the diagnostic passes.** Run adaptive target on Chameleon, Texas, and Wisconsin split 0. Pass if Chameleon is not worse than FullLatent/SRLP-Aux beyond noise, and Texas or Wisconsin shows a clear improvement over current SRLP-Aux without collapse.

3. **Kill condition.** If the gate cannot predict when residual is useful, or the three-run pilot improves only the diagnostic target but not learned online representations, stop method expansion and keep this line as a diagnostic observation.
