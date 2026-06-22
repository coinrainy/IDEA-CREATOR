---
type: idea
node_id: idea:dca_gcl
title: "DCA-GCL: Deferred Complementary Anchor Graph Contrastive Learning"
stage: empirical_lead
status: novelty_review_pending
outcome: edge_positive_not_paper_ready
fair_test_status: partial_internal_gate
based_on: ["idea:rfa", "idea:fba_gcl", "paper:li2026_aspect", "paper:shan2026_revisiting_positive_samples"]
target_gaps: ["gap:G3", "gap:G4"]
added: 2026-06-22T13:35:00+08:00
---

# DCA-GCL: Deferred Complementary Anchor Graph Contrastive Learning

## Status

Empirical lead after FBA/SBN, but novelty review is pending. Do not treat as a final paper method yet.

## Hypothesis

Graph contrastive encoders can lose useful spectral-regime information when raw or filter anchors are forced into the training objective. Keeping raw, high-pass, and low-pass anchors deferred until representation time preserves complementarity and improves node classification on selected datasets.

## Proposed Method

Train the graph encoder with the existing BGRL/RFA objective. After training, build deterministic row-normalized anchors:

```text
raw = X
high1 = X - P X
high4 = X - P^4 X
low4 = P^4 X
```

Evaluate frozen candidates such as:

```text
dca_h1_p4 = normalize([z_g || raw || 0.5 high1 || low4])
dca_h1_h4_p4 = normalize([z_g || raw || 0.5 high1 || 0.5 high4 || low4])
```

## Current Evidence

Chameleon 10 official splits: `dca_h1_p4` and `dca_h1_h4_p4` both reach mean test `0.505044`, compared with graph_raw `0.496711` and FBA one-anchor `0.500219`.

Cora/CiteSeer fixed splits improve over graph_raw. Texas/Wisconsin are still raw-feature dominant.

## Closest Prior Work

ASPECT, FC-GSSL, SPGCL, Less is More, HLCL, GREET, and SIGNA are close enough that DCA needs strict novelty review before any main-method claim.

## Failure Notes

If review concludes deferred fusion is only a minor variant of graph-feature concatenation or spectral fusion, keep DCA as a diagnostic baseline rather than a paper method. Any future gate must report raw-only and graph_raw controls.

