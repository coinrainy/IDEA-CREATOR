# LIFT-Stack + Checkpoint Residual R085 Results

**Date**: 2026-06-22  
**Status**: `FAILED_COMPLEMENTARITY_GATE`  
**Script**: `baselines/BGRL/evaluate_lift_stack_plus_checkpoint.py`  
**Raw CSV**: `baselines/BGRL/runs/lift_stack_plus_checkpoint_split0_20260622/results.csv`

## Question

LIFT-Stack is the strongest current control, but it is low-novelty. R085 tests
whether existing trained BGRL/GDC/TD checkpoints contain complementary residual
information that can be concatenated with LIFT-Stack to form a stronger method
candidate without retraining.

Command:

```bash
python evaluate_lift_stack_plus_checkpoint.py \
  --datasets=cora,citeseer,chameleon,texas,wisconsin \
  --splits=0 \
  --checkpoint_split=0 \
  --c_powers=-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10 \
  --output_dir=runs/lift_stack_plus_checkpoint_split0_20260622 \
  --device=auto
```

## Main Result

| Dataset | LIFT-Stack | Best Stack + Checkpoint | Best source | Delta | Decision |
|---|---:|---:|---|---:|---|
| Cora | 0.842640 | 0.852792 | BGRL control / TD direction | +0.010152 | local positive |
| CiteSeer | 0.725770 | 0.713749 | TD direction | -0.012021 | fail |
| Chameleon | 0.668860 | 0.638158 | BGRL control | -0.030702 | fail |
| Texas | 0.810811 | 0.783784 | BGRL control / GDC residual | -0.027027 | fail |
| Wisconsin | 0.823529 | 0.803922 | BGRL control / GDC residual | -0.019608 | fail |

Checkpoint-only representations are also weak relative to LIFT-Stack:
Cora best checkpoint `0.830641`, CiteSeer `0.693464`, Chameleon `0.442982`,
Texas `0.621622`, Wisconsin `0.549020`.

## Interpretation

The Cora improvement shows that trained GNN representations can sometimes add
information to fixed propagation features. However, the effect is not stable:
CiteSeer regresses, Chameleon loses the main LIFT-Stack gain, and WebKB raw
protection is damaged by concatenating the checkpoint embedding.

The dynamic variants do not provide a distinct advantage over ordinary BGRL:
on Cora the BGRL and TD concatenations tie, while on Chameleon the GDC/TD
concatenations are worse than BGRL concatenation.

## Decision

Do not promote LIFT-Stack + checkpoint residuals. Treat the result as another
boundary: a learned GNN branch cannot simply be appended to LIFT-Stack. A
future method would need a robust label-free routing or residual-isolation
mechanism before using trained checkpoint information, and it must beat
LIFT-Stack on CiteSeer/Chameleon without breaking WebKB raw protection.
