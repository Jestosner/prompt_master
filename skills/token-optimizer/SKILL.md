---
name: token-optimizer
description: >-
  Executes Phase 4 (Token Optimization). Runs strictly AFTER quality is stable:
  performs 1-by-1 ablation, compresses prompt and output tokens, recommends
  runtime savings, and enforces the <= 0.1 score-drop / 0 hard-fail acceptance gate.
---

# Phase 4: Token Optimizer (Post-Stability Only)

**Hard Prerequisite**: Run Phase 4 **ONLY AFTER** the Phase 3 stop condition is met (quality is stable, 0 hard fails across 2 consecutive versions, 0 regressions). Never compress an unstable prompt.

## Procedure

Consult [references/compression-playbook.md](./references/compression-playbook.md) for concrete patterns.

### 1. One-by-One Ablation
- Test removing each instruction, rule clause, context sentence, and example **one at a time**.
- Keep a line **only if** removing it lowers the weighted score or introduces a hard fail/regression.
- Log every ablation trial: `[item removed] -> [delta tokens] -> [delta score / hard fails] -> [KEEP or DROP]`.

### 2. Prompt Compression
- Replace prose paragraphs with terse directives, key-value tables, or compact schemas.
- Merge overlapping or duplicate rules.
- Shorten retained examples to the smallest token footprint that still prevents drift.
- Preserve the static-prefix / trailing-`{{variables}}` caching boundary.

### 3. Output Token Reduction (Often Highest ROI)
Output tokens typically cost 3x-5x input tokens. Cut them systematically:
- Enforce explicit length caps (words/items/chars).
- Ban preamble, polite filler, restatements, and closing recaps.
- Use compact structured output (JSON/enums/short keys) whenever the downstream consumer is code.

### 4. Runtime Architecture Savings
Recommend only levers relevant to `MODEL+ENV` and `VOLUME+COST`:
- **Prompt caching**: lock static prefix above provider minimum cache threshold.
- **Model tiering + escalation**: run a cheaper/faster model by default and escalate to a frontier model only on low confidence, complex inputs, or deterministic-check failure.
- **Batching**: use async batch APIs for non-interactive workloads.
- **Input pre-filtering / truncation**: strip HTML/boilerplate, extract only relevant fields, or pre-filter out-of-scope requests in deterministic code before calling the LLM.

### 5. Cross-Version Cost Table & Strict Acceptance Gate
Invoke `token-auditor` to emit:
`version | prompt tokens | avg output tokens | weighted score | est. cost per 1,000 calls` (with stated assumptions).

**Acceptance Rule (Non-Negotiable)**:
- Accept a compression candidate **ONLY IF**:
  1. Weighted score drops by **<= 0.1** (or tighter tolerance if `strict` mode is active via `mode-policies`), AND
  2. **Zero hard-fail regressions** occur.
- Otherwise **revert immediately** and state the exact score drop / failing case ID.

## Verification

Before advancing to `release-packager`, verify:
- [ ] Phase 3 stability gate was confirmed prior to optimization.
- [ ] Ablation tested instructions/examples individually (no blind bulk stripping).
- [ ] Accepted version satisfies `score_drop <= 0.1` and `0` hard-fail regressions.
- [ ] Cross-version token/cost table includes all assumptions and approximate-method disclosure.
