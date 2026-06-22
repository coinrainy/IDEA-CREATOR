# Research Findings

## 2026-06-22: Pair-level positive abstention also fails the BGRL gate

**Verdict**: `FAILED_SPLIT0_GATE`.

Worker B tested PUAB-GCL (`puab_soft`, `puab_hard`) in an isolated fork. The
idea calibrated or abstained positive pairs using label-free pair utility
signals, but kept final evaluation on canonical CPU sklearn.

| Dataset | BGRL control | `puab_soft` | `puab_hard` |
|---|---:|---:|---:|
| Cora | 0.833410 | 0.832026 | 0.829257 |
| CiteSeer | 0.692712 | 0.691585 | 0.688580 |
| Chameleon | 0.438596 | 0.414474 | 0.418860 |

Conclusion: pair-level abstention does not rescue BGRL; it slightly hurts
Cora/CiteSeer and clearly hurts Chameleon. Do not merge the worker code or run
10-split.

## 2026-06-22: Direct no-self BGRL does not recover Positive-Path LIFT

**Verdict**: `FAILED_SPLIT0_GATE`.

Ego-NoSelf BGRL disables automatic self-loops in every GCNConv layer. This
tested whether the strong fixed Positive-Path / no-self LIFT signal can become
a trained encoder objective.

| Dataset | BGRL control | Ego-NoSelf | Required reference |
|---|---:|---:|---:|
| Cora | 0.832949 | 0.815874 | LIFT 0.842640 |
| CiteSeer | 0.693088 | 0.663411 | LIFT 0.725770 |
| Chameleon | 0.438596 | 0.287281 | Positive-Path 0.725877 |

Conclusion: no-self propagation is useful as a fixed feature/channel under
LIFT gating, but direct no-self message passing destroys too much identity
signal during BGRL training. Future ego-shortcut methods need a protected
raw/identity branch.

## 2026-06-22: Missing-feature stress is not enough for a main GCL method

**Verdict**: `FAILED_SPLIT0_GATE`.

MFS-GCL tested node-wise independent feature-entry dropout in the online view,
aligned to a clean teacher target. Training and representation extraction ran
on CUDA; the final linear probe stayed on the canonical CPU sklearn protocol.

| Dataset | BGRL control | Best MFS | Required reference |
|---|---:|---:|---:|
| Cora | 0.832949 | 0.840794 | LIFT 0.842640 |
| CiteSeer | 0.693088 | 0.693839 | LIFT 0.725770 |
| Chameleon | 0.438596 | 0.449561 | Positive-Path 0.725877 |

Conclusion: node-wise missing-feature stress gives only BGRL-internal gains
and does not challenge the current required controls. The novelty lane is also
crowded by random feature masking, FDAGCL, and masked/adversarial feature GCL.
Do not expand this route to 10-split or external baselines.

## 2026-06-22: CCR-GCL shows learned residual complementarity is a safety problem

**Verdict**: `FAILED_CERTIFICATION_GATE`.

CCR-GCL trained a residual GNN branch orthogonal to a fixed LIFT-Portfolio
teacher. This produced the strongest learned-residual local signal so far on
Cora, but failed cross-dataset safety.

| Dataset | Portfolio | Certified residual concat | Delta |
|---|---:|---:|---:|
| Cora | 0.842640 | 0.855099 | +0.012460 |
| CiteSeer | 0.725770 | 0.714125 | -0.011645 |
| Chameleon | 0.699561 | 0.629386 | -0.070175 |
| Texas | 0.810811 | 0.783784 | -0.027027 |
| Wisconsin | 0.823529 | 0.803922 | -0.019608 |

Conclusion: learned residual branches can contain useful information, but
current label-free certification is too weak. Residual edge-lift and
orthogonality to a teacher anchor did not prevent harmful residuals from being
added. Do not continue learned-residual expansion without a better residual
safety criterion.

## 2026-06-22: PAB-BGRL has BGRL-internal signal but is not a main method

**Verdict**: `BGRL_INTERNAL_SIGNAL_NOT_MAIN_METHOD`.

PAB-BGRL directly tests prealignment abstention: nodes whose positive
alignment is likely already trivialized by message passing receive lower BGRL
loss weight. This produced small improvements over BGRL on several split-0
datasets, but not enough to challenge LIFT-Portfolio.

| Dataset | BGRL control | PAB soft | LIFT-Portfolio split-0 |
|---|---:|---:|---:|
| Cora | 0.832949 | 0.832949 | 0.842640 |
| CiteSeer | 0.693464 | 0.695342 | 0.725770 |
| Chameleon | 0.438596 | 0.449561 | 0.699561 |
| Texas | 0.621622 | 0.648649 | 0.810811 |
| Wisconsin | 0.549020 | 0.549020 | 0.823529 |

Conclusion: PAB can be kept as a diagnostic for BGRL positive trivialization,
but it is not worth 10-split expansion. It also has high novelty risk near the
2026 SPGCL pre-alignment/message-passing analysis.

## 2026-06-22: EPI-BGRL failed the split-0 main-method gate

**Verdict**: `FAILED_MIXED_SPLIT0_GATE`.

EPI-BGRL tested a GPU-trained route outside the fixed LIFT family. It partitions
nodes into label-free environments using degree and raw-feature neighborhood
drift, then balances BGRL node losses across environments with a REx-style
penalty.

M0 smoke and M1 split-0 all ran with `device=cuda`; final linear probes kept
the canonical CPU sklearn protocol. The result is not strong enough:

| Dataset | BGRL control | EPI-BGRL | LIFT-Portfolio split-0 |
|---|---:|---:|---:|
| Cora | 0.833872 | 0.840794 | 0.842640 |
| CiteSeer | 0.693839 | 0.690834 | 0.725770 |
| Chameleon | 0.438596 | 0.425439 | 0.699561 |
| Texas | 0.621622 | 0.621622 | 0.810811 |
| Wisconsin | 0.549020 | 0.549020 | 0.823529 |

Conclusion: environment balancing produces a Cora-only local gain but fails the
decisive CiteSeer/Chameleon/WebKB settings and remains far below
LIFT-Portfolio. Do not expand EPI to 10-split or external baselines.

## 2026-06-22: LIFT-Portfolio is the strongest current fixed-propagation control

**Verdict**: `STRONG_BASELINE_LOW_NOVELTY`.

R088 audited a fast/full C-grid discrepancy. Chameleon full-grid 10-split
prefers single P2/global LIFT (`0.685746`) over `LIFT-Stack 0123` (`0.671053`),
even though fast-grid made stack look competitive. Cora/CiteSeer keep the stack
gains (`0.848869` / `0.726972`), Squirrel fast-grid keeps the stack gain
(`0.543708`), and Texas/Wisconsin/Cornell/Actor remain raw-protected.

Conclusion: the required baseline is now LIFT-Portfolio: raw for K0 graphs, P2
for low-raw-lift K2 graphs, and stack otherwise. This is not the final method
because it remains a fixed-propagation selector with high novelty risk.

## 2026-06-22: LIFT interaction features failed the Chameleon gate

**Verdict**: `FAILED_SPLIT0_GATE`.

R087 appended fixed nonlinear raw-propagation blocks to LIFT-Stack. Cora and
CiteSeer show tiny local gains (`0.845408` vs `0.842640`; `0.729527` vs
`0.725770`), but the useful variant differs by dataset and Chameleon fails
(`0.666667` best vs `0.668860`, with several variants much worse).

Conclusion: plain fixed-feature micro-tuning is not a paper-level route. Stop
adding deterministic product/difference/delta blocks on top of LIFT-Stack.

## 2026-06-22: LIFT Channel Gate has only a local Chameleon signal

**Verdict**: `FAILED_ROBUSTNESS_GATE`.

R086 weighted LIFT-Stack feature channels by a label-free channel edge-lift
score. It found a real Chameleon split-0 positive (`softplus 0.688596` vs
LIFT-Stack `0.668860`), but this did not generalize: Chameleon fast 10-split
is effectively neutral (`0.663377` best vs `0.662500`), and Squirrel ReLU
gating regresses (`0.525360` vs `0.543708`). Cora and CiteSeer also regress in
the split-0 gate.

Conclusion: simple channel pruning/weighting over fixed propagation stacks is
not robust enough. Keep channel edge-lift as a diagnostic for noisy Chameleon
channels, not as a main GCL method.

## 2026-06-22: LIFT-Stack checkpoint residuals failed the complementarity gate

**Verdict**: `FAILED_COMPLEMENTARITY_GATE`.

R085 tested whether existing trained BGRL/GDC/TD encoder checkpoints could be
used as a residual branch on top of LIFT-Stack. The answer is no for the
current method search. Cora improves (`0.852792` vs LIFT-Stack `0.842640`), but
CiteSeer regresses (`0.713749` vs `0.725770`), Chameleon regresses
(`0.638158` vs `0.668860`), and raw-protected Texas/Wisconsin are damaged
(`0.783784` / `0.803922` vs `0.810811` / `0.823529`).

Conclusion: a learned GNN checkpoint branch is not automatically complementary
to fixed propagation stacks. Future methods need a label-free residual
isolation or routing rule before adding trained representations to LIFT-Stack.

## 2026-06-22: LIFT-HC-GCL failed the mixed split-0 gate

**Verdict**: `FAILED_MIXED_SPLIT0_GATE`.

LIFT-HC-GCL tested whether adding a genuine contrastive branch to LIFT-Stack
can produce a paper-level GCL method. It trains an MLP encoder on two
hop/feature-drop views of `[X,PX,P2X,P3X]` with a SimSiam-style loss, then
evaluates the SSL embedding alone or concatenated with LIFT-Stack.

The 300-epoch split-0 gate is mixed: Cora improves (`0.850023` vs LIFT-Stack
`0.842640`) and Wisconsin improves locally (`0.843137` vs `0.823529`), while
Texas is protected by raw fallback. But CiteSeer regresses (`0.716754` vs
`0.725770`) and Chameleon regresses (`0.657895` vs `0.668860`). Short 5/20
epoch probes do not fix Chameleon.

Conclusion: a generic hop-drop contrastive transformation on top of fixed
multi-hop features is not robust enough. Keep LIFT-Stack as the required
control and restart with a mechanism that does not rely on unconstrained MLP
contrastive transformations.

## 2026-06-22: LIFT-Stack is the strongest current control, but novelty is weak

**Verdict**: `STRONG_BASELINE_LOW_NOVELTY`.

LIFT-Stack uses the global LIFT selector and activates a fixed multi-hop stack
only when propagation is reliable: raw fallback for K0 graphs, otherwise
`[X, PX, P2X, P3X]`. It improves over global LIFT on Cora, CiteSeer,
Chameleon, and Squirrel, while protecting Texas/Wisconsin/Cornell/Actor.

Key results:

| Dataset | Protocol | Global LIFT | LIFT-Stack 0123 |
|---|---|---:|---:|
| Cora | 10 random splits | 0.832995 | 0.848823 |
| CiteSeer | 10 random splits | 0.700301 | 0.727310 |
| Chameleon | 10 official splits, fast grid | 0.655482 | 0.662500 |
| Squirrel | 10 official splits, fast grid | 0.520365 | 0.543708 |
| Texas/Wisconsin/Cornell/Actor | 10 official splits, fast grid | raw selected | unchanged |

This is empirically useful, but fixed multi-hop feature stacks overlap with
SIGN/SGC, the very recent Fixed Aggregation Features paper, and PROPGCL's
training-free propagation thesis. Treat LIFT-Stack as the strongest baseline
to beat, not as the final GCL method unless the project pivots to a
selector-only reliability paper.

## 2026-06-22: LIFT-PROP training extensions failed; keep as selector baseline

**Verdict**: `SELECTOR_BASELINE_NOT_MAIN_METHOD`.

LIFT-PROP remains a strong label-free propagation selector, but two compact
attempts to promote it into a full GCL method failed.

R077 learned soft propagation coefficients over `[X, PX, P2X, P3X]` using an
edge-positive/random-negative contrastive loss. It improved Cora locally
(`0.831103` vs fixed selector `0.825565`) but damaged CiteSeer (`0.684072` vs
`0.709617`) and Chameleon (`0.622807` vs `0.699561`). Texas/Wisconsin would be
badly damaged by the learned mix, and the only useful behavior was the global
LIFT gate falling back to raw.

R078 tested node-wise LIFT routing. It again produced a Cora-only signal
(`node_soft_k02=0.836641` vs global `0.825565`) but regressed on Chameleon,
Texas, and Wisconsin. The likely reason is that row-wise propagation-depth
selection breaks representation-space consistency for a shared linear
classifier.

Recommended next action: do not continue LIFT-PROP as the main GCL method
unless the project deliberately pivots to a selector-only paper. Use global
LIFT-PROP as a required training-free baseline for the next idea-discovery
restart.

## 2026-06-22: Fixed-sign SC-BGRL failed the fair split-0 gate

**Verdict**: `FAILED_FIXED_SIGN_PILOT`.

SC-BGRL was implemented with fixed same-compatible and different-compatible
edge views based on raw-feature endpoint cosine. An initial threshold split
collapsed on Chameleon because many edge similarities were exactly zero; this
was fixed by rank-based top/bottom splitting before making the final decision.

Fair rank-split result:

| Dataset | Control | SC | Delta |
|---|---:|---:|---:|
| Cora | 0.832487 | 0.828334 | -0.004153 |
| Chameleon | 0.438596 | 0.436404 | -0.002193 |
| Texas | 0.621622 | 0.621622 | +0.000000 |
| Wisconsin | 0.549020 | 0.549020 | +0.000000 |

No NaN/collapse occurred, but the method has no positive signal. Stop
fixed-sign SC-BGRL and move to GDC-GCL+.

## 2026-06-22: NPG-GCL weak signal, move to SC-BGRL

**Verdict**: `WEAK_SIGNAL_DEPRIORITIZED`, not `READY_TO_REFINE`.

NPG-GCL was implemented as a response to SPGCL-style positive-alignment
trivialization. It weights BGRL node alignment by nontrivial gain over a cheap
message-passing prealignment baseline. Engineering passed: py_compile, dry-run,
and Cora/Chameleon 5-epoch smoke all completed with no NaN/collapse.

The 200-epoch split-0 signal is too weak for promotion:

| Dataset | Control | NPG | Delta |
|---|---:|---:|---:|
| Cora | 0.830641 | 0.834333 | +0.003692 |
| CiteSeer | 0.692712 | 0.691210 | -0.001503 |
| Chameleon | 0.438596 | 0.442982 | +0.004386 |
| Texas | 0.621622 | 0.621622 | +0.000000 |
| Wisconsin | 0.549020 | 0.549020 | +0.000000 |

Ablations weaken the claim. Cora random weighting (`0.838948`) beats NPG,
though Chameleon NPG (`0.442982`) beats uniform (`0.438596`) and random
(`0.429825`). Conclusion: NPG has a small Chameleon mechanism signal, but it
is not broad or strong enough for 3-split/refinement under the positive-method
goal.

Recommended next action: stop NPG as the lead and implement SC-BGRL, the
signed-compatibility backup route.

## 2026-06-22: TD-GCL implemented and kept as speculative incubate

**Verdict**: `SPECULATIVE_INCUBATE`, not `READY_TO_REFINE`.

After RSP was downgraded, a new mechanism family was implemented:
TD-GCL, Training-Dynamics Graph Contrastive Learning. It defines positives
from similar node embedding update directions during BGRL training, avoiding
static edges, raw-feature kNN, WL/role signatures, filters, prototypes, and
edge masks.

The split-0 signal is real but narrow. Against the same trainer with
`lambda_dynamics=0`, TD-GCL improves Cora from `0.807107` to `0.842640`,
CiteSeer from `0.712622` to `0.729527`, and Chameleon from `0.467105` to
`0.478070`. Texas/Wisconsin show no gain and remain below raw-only
(`0.810811` / `0.823529`). No NaN/collapse occurred.

Quick novelty check found moderate risk: IFL-GCL (SIGIR 2025) and DGCL-PU
already frame GCL as positive-unlabeled semantic positive mining, and dynamic
positive mining exists in graph contrastive/clustering literature. TD-GCL's
possible delta is specifically using embedding update directions across
training, not static representation similarity.

Recommended next action: keep TD-GCL as an incubated route only. Before any
paper-level refinement, run a deeper novelty check for training-trajectory
positives/dynamic positive mining, validate Cora/CiteSeer robustness beyond
one split, and add a label-free reliability rule for raw-dominant WebKB graphs.

## 2026-06-22: RSP-GCL downgraded after M2-M4 gate and novelty check

**Verdict**: diagnostic-only, not a final 2026 paper-level method.

RSP-GCL completed the required Chameleon 10-split training, validation-selected
raw/role gate, and direct novelty check. The empirical signal is real but too
conditional: Chameleon role-fused training reaches `0.573684 +/- 0.026265`, and
the validation gate selects `graph_raw_role` in 10/10 splits with
`0.574781 +/- 0.023321`. However, Texas and Wisconsin are raw-dominant:
RSP role-fused is `0.727027` / `0.774510` while raw is `0.829730` / `0.839216`.
Validation selection mostly falls back to raw (`0.827027` Texas,
`0.827451` Wisconsin), which protects against damage but does not create a
broad method gain.

Novelty is also too crowded. GALE already uses node equivalence as a central
self-supervised graph learning principle, WLGCL directly uses WL structural
similarity to construct GCL positives, and SPGCL shows positive-sample GCL is
still an active 2026 direction. RSP should remain a diagnostic baseline for
Chameleon-like role signatures, not a main method for external baseline
expansion.

Recommended next action: restart idea discovery with a different mechanism
family. Avoid generic node-equivalence/WL-positive claims and avoid methods
whose only gain comes from concatenating static handcrafted signatures.

## 2026-06-22: RSP-GCL is the new active role-signature candidate

**Verdict**: active with scope limit, not paper-ready yet.

After CIG/CLEAR failed, a fresh idea-discovery pass moved to structural role equivalence rather than spectral fusion, semantic kNN, local transport, prototypes, residual targets, or edge masks. The new candidate is RSP-GCL: Role-Signature Positive Graph Contrastive Learning. It builds label-free role/WL/landmark signatures and uses them to define nonlocal role-equivalent positives for a BGRL-style objective.

Key evidence:

- Chameleon 10-split zero-training proxy: `graph_raw_role_wl_landmark = 0.585965 +/- 0.026073`, far above `graph_raw = 0.496711` and previous DCA best `0.505044`.
- RSP-GCL training split-0: Chameleon role-fused `0.596491`, no NaN/collapse.
- Texas/Wisconsin remain raw-dominant: full role proxy `0.678378` / `0.719608` vs raw `0.829730` / `0.839216`.

Recommended next action: run Chameleon 10-split RSP training, add a role gate over `{0, role}` to protect raw-dominant graphs, and run a direct novelty check against Str-GCL, CoRep, H3GNNs/HarmonyGNNs, structural encoders, and WL/role-positive GCL.

## 2026-06-22: SRLP main-method claim invalidated

**Verdict**: negative, high confidence.

The SRLP / SRLP-Aux / Adaptive-Aux line should not continue as a main graph SSL method. Residual-only SRLP failed the small heterophily split-0 gate, SRLP-Aux did not beat target-family ablations across 10 Geom-GCN splits, and Adaptive-Aux only produced a local Wisconsin split-0 positive signal while hurting Chameleon and Texas.

What remains useful:

- target-incident-edge hard isolation reduces leakage;
- shortcut leakage reduction does not automatically imply better downstream node classification;
- projection/residual target components have dataset-dependent semantic value.

Constraint for future ideas: do not assume that removing context-predictable latent components is beneficial. Any future latent-prediction GCL idea must show that its target remains task-relevant, not merely shortcut-resistant.

Recommended next action: re-run idea discovery with this failure mode as a constraint.

## 2026-06-22: Fresh idea discovery selected DCGCL for pilot

**Verdict**: paper-only active route, no GPU evidence yet.

The new candidate is DCGCL, Disagreement-Calibrated Prototype Graph Contrastive Learning. It replaces SRLP-style residual latent prediction with a label-free prototype objective built from two weak teachers: a feature-only teacher and a propagation-view teacher. Agreement between their soft prototype assignments defines reliable global positives; disagreement is kept through dual semantic/topology heads and a gate instead of being forced into one pseudo-class.

Why it was selected: it directly addresses the SRLP lesson that shortcut resistance is not enough; the target must be task-relevant for node classification. It also avoids the abandoned frequency-routing line and does not require LLM/text data.

Next action: implement only the M0/M1/M2 pilot from `refine-logs/EXPERIMENT_PLAN.md`. Do not launch 10-split expansion unless split-0 DCGCL beats or matches the best local controls and the no-dual/no-gate ablations confirm the mechanism.

## 2026-06-22: DCGCL V0 initial pilot did not pass M2

**Verdict**: engineering pass, method gate fail.

DCGCL V0 is implemented and stable in the BGRL harness, but the first split-0 gate is insufficient. It has a small positive signal on Chameleon (`0.4276` vs best local control `0.4232`), ties Wisconsin (`0.5882`), and regresses on Texas (`0.6216` vs `0.6486`) and Cora (`0.7790` vs BGRL `0.8090`). No NaN or collapse occurred.

Lesson: disagreement-calibrated prototypes are not enough in their current shared-bank form. The method likely needs separate aligned feature/topology prototype banks and a stricter high-confidence agreement mask before another M2 run. Do not launch 10-split expansion for DCGCL V0.

## 2026-06-22: DCGCL V1 10-split gate invalidated the main method

**Verdict**: negative for main method, partial diagnostic signal.

DCGCL V1 added separate feature/topology prototype banks, greedy alignment, and a high-confidence agreement mask. Split-0 looked promising on Texas and Wisconsin, but 10-split validation did not hold: Chameleon `0.40658` vs best control `0.50044`, Texas `0.58649` vs `0.61351`, Wisconsin `0.60392` vs `0.55490`. Run integrity was clean: 30/30 rows, no NaN/collapse.

What remains useful: low feature/topology prototype alignment may identify a subset of graphs where dual prototype supervision helps, as Wisconsin improved on 8/10 splits. This is not enough for a 2026 paper-level graph contrastive learning method.

Recommended next action: stop DCGCL as a main route and restart idea discovery with two hard constraints: avoid residual targets whose label alignment is unproven, and avoid global prototype positives unless the method has a dataset-robust, label-free activation rule validated before training.

## 2026-06-22: FTDR-BGRL was stable but not positive

**Verdict**: weak / deprioritized.

FTDR-BGRL routed each node's bootstrap target between a topology teacher and a feature-only teacher using feature-topology disagreement. It avoided the exact SRLP/DCGCL failure modes, but split-0 evidence was not positive: Cora nearly tied BGRL (`0.8076` vs `0.8090` after raising `route_tau`), Chameleon remained below control (`0.4035` vs `0.4232`), and Texas/Wisconsin only tied control (`0.6486`, `0.5882`). No NaN/collapse occurred.

Lesson: the project should stop exploring simple latent-target routing variants for now. The next idea search should move to a different mechanism family rather than adding more route thresholds.

## 2026-06-22: RFA-BGRL exposed feature-signal forgetting but is not final

**Verdict**: strongest current diagnostic baseline, not yet a 2026 paper-level method.

After FTDR, CFR-BGRL tested a learned graph channel plus learned feature channel. It was stable but failed split-0: Cora `0.8002` vs BGRL `0.8090`, Chameleon `0.4079` vs `0.4232`, Texas tied `0.6486`, and Wisconsin regressed to `0.5294`. The key lesson was that a learned bootstrap feature channel can still forget raw-feature label signal.

RFA-BGRL then preserved raw features as an explicit anchor and concatenated them with a BGRL graph branch. It is stable and strong on Texas/Wisconsin: 10-split 200-epoch means are Texas `0.7622` and Wisconsin `0.8098`, far above prior local GCL controls. However, raw-only is still stronger on those datasets (`0.8297` and `0.8392`), so this is mostly feature retention rather than a new graph-contrastive mechanism.

Chameleon remains the decisive weakness. RFA improves over raw-only and graph-only, and 1000-epoch split-0 reaches `0.5022`, but 10-split 1000-epoch mean is `0.4928`, slightly below the strict prior control around `0.5004`.

Recommended next action: keep RFA as a required baseline and move the method to ORFA-GCL: a protected raw-feature anchor plus an explicitly complementary graph residual branch. Do not claim RFA itself as the final paper method.

## 2026-06-22: ORFA and BiFilter failed; FBA-GCL is the next focused gate

**Verdict**: ORFA-GCL and BiFilter-BGRL are stopped; FBA-GCL is diagnostic-only after the training gate failed.

ORFA-GCL preserved a raw-feature anchor and tried to train the graph branch as a complementary residual. It was stable, but the decisive results were not enough: Chameleon 1000 split-0 reached only `0.484649`, below RFA; Texas stayed below raw-only; Wisconsin only tied raw-only.

BiFilter-BGRL added a trainable low-pass GCN branch and high-pass residual-feature MLP branch. It also stayed stable but failed split-0: Cora `0.702815`, Chameleon `0.458333`, Texas `0.729730`, Wisconsin `0.666667`. A naive high-pass branch is not a good method.

The useful signal came from deterministic filter anchors. Training-free diagnostics show Cora/CiteSeer benefit from `P^2X`, Texas can benefit from `X-P^4X`, and Chameleon improves only when a learned graph view is combined with raw plus a small low/high filter anchor. Re-evaluating existing RFA Chameleon 1000 checkpoints across 10 official splits gives:

- `graph+raw`: `0.496711 +/- 0.022175`;
- `graph+raw+0.5H1`: `0.500219 +/- 0.020769`;
- `graph+raw+P4`: `0.500219 +/- 0.018697`.

The reusable FBA evaluator and trainable FBA implementation were added. The post-hoc filterbank signal reproduced, but the trainable anchor auxiliary failed the strict Chameleon 10-split gate:

- FBA-high1 train: `0.487061 +/- 0.025714`;
- same-run graph_raw: `0.493202 +/- 0.025013`;
- NaN/collapse: 0.

Recommended next action: keep FBA as a diagnostic/post-hoc filterbank baseline, or redesign the anchor selection/training objective before any new 10-split run. Do not launch a main-table expansion or claim a 2026 paper-level method from current FBA.

## 2026-06-22: SBN failed; DCA-GCL is the current empirical lead

**Verdict**: DCA is edge-positive but not paper-ready; novelty/method review is mandatory.

After FBA training failed, a fresh idea-discovery pass tested a different mechanism family, SBN-GCL: semantic raw-feature kNN positives plus low-similarity edge boundary negatives. SBN was stable but failed the split-0 gate: Chameleon fused `0.462719`, Texas `0.729730`, and Wisconsin `0.784314`, all below the relevant raw or local controls. Chameleon ablations without boundary loss or with larger positive neighborhoods also failed, so SBN should stop.

The useful signal came from deferred complementary anchors. DCA-GCL keeps filter anchors out of the training objective and fuses them only after the graph encoder is trained. On Chameleon 10 official splits, DCA improved over graph_raw and one-anchor FBA:

- `graph_raw`: `0.496711 +/- 0.022175`;
- `fba_h1`: `0.500219 +/- 0.020769`;
- `dca_h1_p4`: `0.505044 +/- 0.022791`;
- `dca_h1_h4_p4`: `0.505044 +/- 0.019908`.

Cora and CiteSeer also improve over graph_raw, but Texas/Wisconsin remain raw-dominant (`raw 0.829730/0.839216`, best DCA/FBA family below raw). Recommended next action: strict novelty/method review against ASPECT, FC-GSSL, SPGCL, Less is More, HLCL/GREET/SIGNA, and simple graph-feature fusion. Do not expand DCA to external baselines or claim a final paper method yet.

## 2026-06-22: DCA novelty failed; restart from a transport-style speculative route

**Verdict**: DCA is diagnostic-only, no active ready method yet.

The DCA novelty check scored only `3/10`. Closest work already covers the major pieces: ASPECT and LOHA cover low/high spectral GCL, HLCL covers heterophily-aware graph filters, FC-GSSL covers frequency-aware graph SSL, Less is More and FB-GCL cover graph/feature complementary fusion, and GCL-GroW/GWGCL cover whitening-style rescue ideas. The only defensible DCA contribution is a diagnostic finding: training-time filter-anchor alignment can hurt, while deferred anchors can be a useful baseline.

Two quick rescue probes did not produce a new main route. Semantic kNN anchors were weak: Cora/CiteSeer had small signal, but Chameleon did not beat graph_raw and Texas/Wisconsin remained raw-dominant. ZCA/whitening timed out in the quick loop and is not cleanly novel.

Recommended next action: do not tune DCA. The next eligible candidate is VST-GCL, a sparse local transport target between topology-neighborhood mass and raw-feature semantic mass. Treat it as speculative; run only a split-0 proxy before any 10-split or baseline expansion.

## 2026-06-22: VST-GCL transport target failed the split-0 gate

**Verdict**: stop VST; restart idea discovery.

VST-GCL implemented a sparse local transport target between raw-feature semantic neighbors and graph topology support. Engineering passed: smoke ran on Cora/Chameleon with no NaN/collapse. The 200-epoch split-0 gate failed:

- Cora fused `0.814490`, below prior anchor controls;
- Chameleon fused `0.469298`, below graph_raw/DCA controls;
- Texas fused `0.729730`, below raw `0.810811`;
- Wisconsin fused `0.803922`, below raw `0.823529`.

A low-auxiliary ablation (`lambda_bgrl=1.0`, `lambda_transport=0.1`) also failed: Cora fused `0.810337`, Chameleon fused `0.467105`. Transport diagnostics showed low stable support mass on Chameleon/Texas, so the method mostly degenerates toward semantic-kNN-like positives, which were already weak.

Recommended next action: do not tune VST. Restart idea discovery with a genuinely different mechanism family.

## 2026-06-22: CIG/CLEAR edge-influence route failed as a main method

**Verdict**: stop CIG/CLEAR.

A counterfactual edge-mask evaluator was added before implementing a full training objective. On split 0, edge masks did not improve Cora or Chameleon; Texas improved over fused RFA but stayed below raw; Wisconsin showed a local positive (`0.843137` vs raw `0.823529`).

The Wisconsin signal did not survive the 10-split check. On Wisconsin, the best fixed mask reached `0.823529` and validation-selected masks reached `0.827451`, both below raw `0.839216`. On Texas, the best fixed mask reached `0.794595` and validation-selected masks reached `0.805405`, both below raw `0.829730`.

Recommended next action: do not implement CIG/CLEAR training. Restart wide idea discovery with a different mechanism family.

## 2026-06-22: NPG, fixed-sign SC-BGRL, and GDC-GCL+ failed local promotion gates

**Verdict**: no active route remains from the post-TDGCL candidate batch.

NPG-GCL tested whether positive alignment should be weighted by nontrivial gain
over message-passing prealignment. It passed smoke and stayed stable, but the
signal was too weak for promotion: Cora improved only from `0.830641` to
`0.834333`, Chameleon from `0.438596` to `0.442982`, CiteSeer regressed, and
Texas/Wisconsin tied. The Cora ablation was decisive because random weighting
reached `0.838948`, above NPG.

Fixed-sign SC-BGRL then tested same-compatible / different-compatible views
using rank-based edge splitting. After fixing the Chameleon sign split so it no
longer degenerated, the fair pilot failed: Cora `0.828334` vs control
`0.832487`, Chameleon `0.436404` vs `0.438596`, and Texas/Wisconsin tied.

GDC-GCL+ tested gradient-residual dynamics positives to rescue the earlier
TD-GCL signal with a cleaner novelty claim. It was stable and non-collapsed,
but split-0 failed: Cora `0.830641` vs BGRL `0.833410`, CiteSeer `0.691210` vs
`0.693464`, Chameleon only `0.442982` vs `0.438596`, and Texas/Wisconsin tied.
TD-direction comparison was also too weak under this runner.

Recommended next action: restart wide idea discovery. Avoid treating dynamic
positives, nontrivial gain weighting, fixed signed views, role/WL positives,
filter anchors, or raw-retention baselines as main contributions unless a
fresh mechanism changes the fair-test setting.

## 2026-06-22: LIFT-PROP-GCL emerges as an active propagation-reliability route

**Verdict**: active with novelty risk; direct novelty check required.

The post-GDC restart found that deterministic propagation is a much stronger
signal than the recent training losses. On Chameleon, `P^2X` with the official
Geom-GCN splits reaches `0.685746 +/- 0.021187`, far above the old RSP/DCA/FBA
diagnostics. On Texas/Wisconsin, propagation is harmful and raw features remain
dominant (`0.829730 +/- 0.051042` and `0.839216 +/- 0.043157`).

The useful idea is not feature-token propagation: it is weaker than `P^2X` on
Chameleon and weaker than raw on WebKB, and GRAPHITE already covers feature-node
graph construction. The useful idea is a label-free propagation reliability
gate:

```text
if mean_edge_cos(P^2X) - mean_random_pair_cos(P^2X) >= 0.35:
    use P^2X
else:
    use X
```

This K2 edge-lift gate selects K=2 for Cora/CiteSeer/Chameleon and K=0 for
Texas/Wisconsin. It matches the oracle K on 4/5 datasets; Cora's oracle is K=3
(`0.835256`) while the gate selects K=2 (`0.826488`).

Recommended next action: novelty-check the reliability gate against PROPGCL,
Less is More, ASPECT, GRAPHITE, and graph-adaptive propagation/filtering. If
the gate survives, turn it into a formal runner and extend to Cornell/Actor/
Squirrel before method refinement.

## 2026-06-22: LIFT-PROP-GCL novelty check is cautious, not paper-ready

**Verdict**: proceed with caution; novelty score `5.5/10`.

The direct novelty check found that LIFT-PROP cannot be framed as "using
propagation for GCL" because PROPGCL already establishes training-free
propagation as a strong graph contrastive learning mechanism. It also cannot
claim feature-token graph construction because GRAPHITE covers that boundary.
Other close risks include GNNEvaluator and When Do GNNs Help for label-free
GNN usefulness estimation, GLANCE for label-free homophily routing, Less is
More for graph/raw dual views, ASPECT for adaptive spectral GCL, and HLCL for
feature-cosine heterophily filtering.

The remaining defensible delta is narrow but real enough to test: a simple
edge-lift statistic for raw-vs-`P^2X` abstention that uses no labels and matches
the oracle K on 4/5 pilot datasets. This should be developed only if it can
beat or complement PROPGCL's propagation-depth selection and transfer beyond
the current five datasets.

Recommended next action: build a formal `reproduce_lift_prop.py` runner, expand
to Cornell/Actor/Squirrel, and compare the edge-lift gate against
validation-selected K and simple graph metrics. Do not move to full paper
writing yet.

## 2026-06-22: LIFT-PROP extra validation is positive but incomplete

**Verdict**: positive transfer signal; full Actor/Squirrel 10-split still needed.

The formal `reproduce_lift_prop.py` runner was added and smoke-tested on
Cornell split 0. Cornell 10-split then completed before the broader
Cornell/Actor/Squirrel run was interrupted for runtime: the K2 edge-lift gate
chooses raw K=0, matching oracle K and reaching `0.816216 +/- 0.059487`.

Actor and Squirrel were checked on split 0. Actor behaves like WebKB: K=0 raw
is best (`0.348684`) and the gate selects K=0 because `lift(P2X)=0.249076`.
Squirrel behaves like Chameleon: K=2 is best (`0.571566`) and the gate selects
K=2 because `lift(P2X)=0.446390`.

Recommended next action: optimize the evaluator for Actor/Squirrel 10-split
or use a faster C-grid, then compare LIFT-PROP against validation-selected K
and PROPGCL-style propagation baselines.

Follow-up fast-grid check (`C in {2^-4, 1, 2^4}`) completed Actor/Squirrel
10-split. Actor remains a clean raw-protection hit: gate K=0 and oracle K=0,
`0.347566`. Squirrel remains propagation-positive, but the fixed K2 gate is a
near miss under the fast grid: K2 `0.509030` beats raw `0.328530`, while K1 is
oracle at `0.520365`. This suggests LIFT-PROP should keep the edge-lift
abstention gate but add a label-free K1/K2 selector when propagation is enabled.

Selector v1 implements that fix: if `lift(P2X)<0.35`, choose K=0; otherwise if
`lift(P2X) <= lift(PX)+0.02`, choose K=1; else choose K=2. On Actor/Squirrel
fast-grid 10-split, v1 selects Actor K0 and Squirrel K1, matching oracle on
both. Across the currently observed datasets/settings, v1 matches oracle on
7/8 and validation-selected K on 7/8, with only Cora preferring K3 over
selected K2 by `0.008768`.

## 2026-06-22: CCR-SAFE residual safety is a diagnostic lead, not a method yet

**Verdict**: promising diagnostic; not paper-ready.

CCR-GCL produced a useful learned residual on Cora, but the first certificate
accepted harmful residuals on CiteSeer, Chameleon, Texas, and Wisconsin. R095
therefore tested safety policies on existing CCR checkpoints. The best rule,
`stack_moderate_residual`, accepts residuals only when LIFT-Portfolio selected
the stack and the residual has moderate graph alignment: residual edge-lift
`>=0.2` and residual edge cosine `<=0.8`.

On split 0, this accepts only Cora and improves LIFT-Portfolio from `0.842640`
to `0.851869`; it rejects CiteSeer, Chameleon, Texas, and Wisconsin, preserving
their portfolio results. The rule is still overfit-risky because thresholds
were selected after inspecting the same diagnostic batch. Next action, if CCR
continues, is fixed-threshold validation on fresh splits with CPU sklearn final
probe numbers and GPU-only tensor diagnostics.

## 2026-06-22: CCR-SAFE fails fresh-split validation

**Verdict**: failed; restart main-method search.

R096 froze the R095 `stack_moderate_residual` thresholds and trained fresh CCR
checkpoints with CUDA. The route fails immediately on Cora: split 1 goes from
LIFT-Portfolio `0.844024` to `0.832949` when the residual is accepted, and
split 2 goes from `0.854638` to `0.850023`. CiteSeer split 1 is protected
(`0.732156` preserved) because its residual edge cosine remains too high
(`0.862810`) and the rule rejects the residual.

This shows the split-0 Cora gain was not a stable learned complement. The
remaining queue was stopped intentionally after three completed fresh
checkpoints. CCR-SAFE should be kept only as negative evidence: residual
complementarity must be validated on fresh splits before being used in any
paper claim.

## 2026-06-22: Spillover-Blocked BGRL fails split-0 gate

**Verdict**: failed.

SBB-BGRL preserves low raw-cosine neighbor messages in the GCN forward pass but
stop-gradients those message paths. CUDA smoke passed and M1 split-0 completed.
However, Cora drops from BGRL `0.832949` to `0.815413`, CiteSeer drops from
`0.692712` to `0.688204`, and Chameleon drops from `0.438596` to `0.427632`.
Texas/Wisconsin improve only over weak BGRL (`0.648649`, `0.568627`) and remain
far below LIFT/raw (`0.810811`, `0.823529`).

The lesson is that low raw edge cosine alone is too blunt for deciding which
message paths should train. Do not tune SBB edge quantiles or expand to
10-split.

## 2026-06-22: LIFT view-set dispersion proxy fails

**Verdict**: failed proxy; do not train.

R098 appended propagation-view uncertainty/statistics over `[X,PX,P2X,P3X]` to
LIFT-Portfolio. Cora has only a tiny local improvement with `portfolio_mean_std`
(`0.842640 -> 0.844947`), while CiteSeer regresses (`0.725770 -> 0.720135`,
and richer stats drop to `0.710368`) and Chameleon regresses strongly
(`0.699561 -> 0.662281`). The run was stopped after Chameleon because the proxy
had already failed.

This also has novelty risk near IJCAI 2025 UGCL, which already uses sample
uncertainty to coordinate graph augmentation and contrastive loss. Do not
implement a GPU-trained view-set dispersion/conformal objective from this
proxy.

## 2026-06-22: LIFT low-rank bottleneck proxy fails

**Verdict**: failed proxy; do not train.

R099 tested randomized-SVD low-rank projections of LIFT-Portfolio before
implementing a learned low-rank GCL objective. CiteSeer improves locally at
rank 32 (`0.725770 -> 0.731781`), but Cora has no gain (`0.842640 -> 0.842178`
best tested rank) and Chameleon regresses sharply (`0.699561 -> 0.651316`).
Whitened low-rank coordinates are broadly harmful.

This looks like a dataset-specific linear-probe regularization effect rather
than a robust representation-learning mechanism. Low-rank GCL is also a nearby
prior direction, so the novelty margin is weak. Do not spend GPU time on a
learned low-rank objective from this proxy.

## 2026-06-22: Sharpness-stable alignment is only a weak BGRL diagnostic

**Verdict**: weak internal signal; not a main method.

SSA-BGRL weights node-level BGRL alignment by stability under temporary
online-parameter perturbations. CUDA smoke passed on Cora/Chameleon, and the
200-epoch split-0 gate ran on Cora, CiteSeer, and Chameleon. Cora improves only
from `0.832949` to `0.834333`, CiteSeer from `0.693088` to `0.696093`, and
Chameleon is unchanged at `0.438596`. All are far below LIFT-Portfolio
(`0.842640`, `0.725770`, `0.699561`).

This shows that parameter-stability is measurable but too mild as a training
signal. Stop SSA before Texas/Wisconsin and 10-split expansion.

## 2026-06-22: LIFT-PROP metric ablation supports edge-lift

**Verdict**: positive diagnostic.

Across the eight observed settings, `lift(P2X)-lift(X)` correlates strongly
with propagation gain `Acc(P2X)-Acc(X)`: Pearson `0.915337`, Spearman
`0.880952`. Raw lift alone is weak, and propagated edge cosine alone is
negatively correlated with gain because it also rises under global smoothing.

This supports the mechanism: LIFT-PROP should not be framed as selecting high
smoothness, but as selecting edge-specific alignment beyond random-pair
alignment. Next diagnostic should add degree/density/effective-rank baselines
and bootstrap uncertainty.

## 2026-06-22: LIFT-PROP beats PROPGCL reported-step heuristic, but not learned PROPGCL yet

**Verdict**: R076 first pass positive; learned PROPGCL remains the next prior.

PROPGCL defines PROP as `A_hat^K X` and reports in Appendix E that K=1 is best
for Cora/CiteSeer/Chameleon/Squirrel, while K=0 is enough for
Texas/Wisconsin/Cornell/Actor/CS. Using that reported-step heuristic on our
current K-sweep settings gives mean test `0.686911` and mean oracle gap
`0.011052`.

LIFT-PROP v1 reaches mean test `0.696868`, mean oracle gap `0.001096`, exact
oracle hits `7/8`, and within-0.02 oracle `8/8`. The main gains over the
PROPGCL reported heuristic are Cora (`+0.022612`), CiteSeer (`+0.011645`), and
Chameleon (`+0.045395`), where current protocol prefers K2 over K1.

This supports LIFT-PROP as a label-free selector / reliability gate, but it
does not beat learned `PROP-GRACE` or `PROP-DGI`. Next step should compare
against learned propagation coefficients or position PROPGCL as the learned
upper-neighbor and LIFT-PROP as a training-free abstention selector.

## 2026-06-22: Cycle-Balance Gated LIFT is downgraded after sign controls

**Verdict**: positive-path baseline only; not a main method.

R102/R103 tested feature-induced signed path channels on top of the protected
LIFT-Portfolio baseline. The method activates only when the portfolio selects
`single_k2_low_raw_lift`; otherwise it falls back to the exact portfolio
representation. On Chameleon, the full C-grid 10-split result improves from
`0.685526 +/- 0.021292` to `0.725877 +/- 0.019174`. Split-0 checks protect
Cora/CiteSeer/Texas/Wisconsin, and extra split-0 checks protect
Squirrel/Actor/Cornell.

R104/R105 invalidated the signed/balance-theory mechanism. The median-cosine
threshold on Chameleon degenerates to all-positive signs (`pos_ratio=1.0`), so
the strongest result is better explained as positive/no-self propagation-path
augmentation. True rank-based 50/50 signs reach only `0.685526` fast-grid;
random signs reach `0.642763`; rank-global shuffle reaches `0.645395`; and
rank-node shuffle reaches `0.667105`.

Do not implement a trained Cycle-Balance objective. Keep Positive-Path /
No-self LIFT as a required diagnostic baseline and restart the main-method
search.

## 2026-06-22: Depth-disagreement BGRL fails split-0 gate

**Verdict**: failed split-0 gate; do not expand.

R106/R107 implemented DDC-BGRL with a depth-trace encoder. The variants either
weight BGRL node losses by shallow/deep representation disagreement or add an
auxiliary shallow-depth alignment target. CUDA smoke passed, but the 200-epoch
split-0 evidence is weak or negative:

| Dataset | Control | Best DDC | Delta | Decision |
|---|---:|---:|---:|---|
| Cora | 0.802953 | 0.811260 | +0.008306 | weak internal only |
| CiteSeer | 0.677310 | 0.678062 | +0.000751 | fail |
| Chameleon | 0.394737 | 0.385965 | -0.008772 | fail |

The route is also close to oversmoothing/depth-aware GCL prior work such as
BlockGCL and stage-aware GCL. Do not run DDC 10-split or WebKB.
