# LIFT-Stack Results

**Date**: 2026-06-22  
**Status**: `STRONG_BASELINE_LOW_NOVELTY`  
**Candidate**: LIFT-gated multi-hop feature stack

## Method

LIFT-Stack keeps the global LIFT selector from LIFT-PROP, but changes the
representation used when propagation is reliable.

```text
if selector_v1 chooses K = 0:
    use X
else:
    use concat(normalize(X), normalize(PX), normalize(P2X), normalize(P3X))
```

`lift_stack_012` uses `[X, PX, P2X]`; `lift_stack_0123` uses
`[X, PX, P2X, P3X]`. This is deliberately treated as a strong baseline because
multi-hop fixed feature stacks overlap with SIGN/SGC/FAF-style graph
tabularization and PROPGCL-style training-free propagation.

## Split-0 Gate

Command:

```bash
python evaluate_lift_stack.py \
  --datasets=cora,citeseer,chameleon,texas,wisconsin \
  --splits=0 \
  --c_powers=-4,0,4 \
  --output_dir=runs/lift_stack_split0_fast_20260622
```

| Dataset | Global LIFT | LIFT-Stack 012 | LIFT-Stack 0123 | Decision |
|---|---:|---:|---:|---|
| Cora | 0.825565 | 0.838025 | 0.842640 | positive |
| CiteSeer | 0.709617 | 0.729902 | 0.725770 | positive |
| Chameleon | 0.668860 | 0.671053 | 0.668860 | weak positive / tie |
| Texas | 0.810811 | 0.810811 | 0.810811 | protected |
| Wisconsin | 0.823529 | 0.823529 | 0.823529 | protected |

## Homophily 10-Seed Gate

Command:

```bash
python evaluate_lift_stack.py \
  --datasets=cora,citeseer \
  --splits=0,1,2,3,4,5,6,7,8,9 \
  --variants=fixed_k0,fixed_k1,fixed_k2,fixed_k3,global_v1,lift_stack_012,lift_stack_0123 \
  --output_dir=runs/lift_stack_homo10_20260622
```

| Dataset | Global LIFT | LIFT-Stack 012 | LIFT-Stack 0123 | Best delta |
|---|---:|---:|---:|---:|
| Cora | 0.832995 | 0.844947 | 0.848823 | +0.015828 |
| CiteSeer | 0.700301 | 0.730841 | 0.727310 | +0.030540 |

## Heterophily 10-Split Gate

Commands:

```bash
python evaluate_lift_stack.py \
  --datasets=chameleon,texas,wisconsin,cornell,actor,squirrel \
  --splits=0,1,2,3,4,5,6,7,8,9 \
  --c_powers=-4,0,4 \
  --output_dir=runs/lift_stack_hetero10_fast_20260622

python evaluate_lift_stack.py \
  --datasets=actor,squirrel \
  --splits=0,1,2,3,4,5,6,7,8,9 \
  --c_powers=-4,0,4 \
  --output_dir=runs/lift_stack_actor_squirrel10_fast_20260622
```

| Dataset | Global LIFT | LIFT-Stack 012 | LIFT-Stack 0123 | Best delta |
|---|---:|---:|---:|---:|
| Chameleon | 0.655482 +/- 0.019790 | 0.657456 +/- 0.014938 | 0.662500 +/- 0.010464 | +0.007018 |
| Texas | 0.805405 +/- 0.049014 | 0.805405 +/- 0.049014 | 0.805405 +/- 0.049014 | +0.000000 |
| Wisconsin | 0.841176 +/- 0.041799 | 0.841176 +/- 0.041799 | 0.841176 +/- 0.041799 | +0.000000 |
| Cornell | 0.786486 +/- 0.056189 | 0.786486 +/- 0.056189 | 0.786486 +/- 0.056189 | +0.000000 |
| Actor | 0.347566 +/- 0.011488 | 0.347566 +/- 0.011488 | 0.347566 +/- 0.011488 | +0.000000 |
| Squirrel | 0.520365 +/- 0.020104 | 0.528626 +/- 0.021409 | 0.543708 +/- 0.018271 | +0.023343 |

## Novelty Boundary

The effect is useful, but the novelty risk is high.

- **SIGN** already precomputes multi-hop graph filters and concatenates them
  for scalable node classification.
- **SGC** already reduces GCN-style learning to fixed propagation plus a simple
  classifier.
- **Fixed Aggregation Features (FAF, arXiv 2601.19449v2)** is a very recent
  2026 paper arguing that fixed aggregation features can rival GNNs and graph
  transformers.
- **PROPGCL** directly argues that training-free propagation is a strong GCL
  baseline and learns propagation coefficients without transformation layers.

The defensible delta is not the feature stack itself. The possible delta is the
LIFT gate that decides when to activate a multi-hop stack and when to abstain
to raw features.

## Decision

LIFT-Stack is stronger than LIFT-PROP on Cora, CiteSeer, Chameleon, and
Squirrel while preserving raw-dominant WebKB/Actor/Cornell. It should become a
required strong baseline and a possible selector-only paper route.

It is **not yet** the final requested GCL idea because novelty against
SIGN/FAF/PROPGCL is likely too weak unless the paper is explicitly framed as a
label-free reliability gate for fixed aggregation features.

Next action:

1. Treat LIFT-Stack as the current strongest training-free control.
2. Restart main-method idea discovery with LIFT-Stack included as a required
   baseline.
3. If no more novel GCL mechanism survives, consider a selector-only paper
   framing and run a deeper novelty check against FAF/PROPGCL/GLANCE.
