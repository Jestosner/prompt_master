---
name: token-auditor
description: >-
  Executes Phase 2D (Token Report) and cross-version cost tracking across all
  prompt revisions. Estimates prompt/output tokens with explicit approximate methods,
  identifies primary cost drivers, and builds the per-1,000-calls cost ledger.
---

# Token Auditor (Phase 2D & Cross-Version Cost Ledger)

Quantify token footprint and runtime economics cleanly without pretending heuristic estimates are exact tokenizer counts.

## When Used

1. **Phase 2D (Build Baseline)**: Immediately after `testset-builder` (Phase 2C), report `v1` prompt tokens, expected dynamic input tokens, expected output tokens, and primary cost drivers.
2. **Phase 4 & Delivery**: Track every prompt revision and compression candidate in the cross-version token/cost table.

## Procedure

1. **Estimate Tokens Transparently**:
   - Run [scripts/estimate_tokens.py](./scripts/estimate_tokens.py) on the prompt file, OR calculate manually using `ceil(chars / 4)` cross-checked with `words * 1.33`.
   - **Always state the estimation method explicitly as approximate, not exact** (e.g., `"Approximate heuristic: ~4 chars/token blended with word/punctuation count; not exact model tokenizer"`).
   - Separate **static cacheable prefix tokens** from **dynamic `{{variable}}` payload tokens**.
2. **Identify Primary Cost Drivers**:
   - Rank top drivers (e.g., output verbosity, uncached large input payloads, redundant examples, model tier price ratio, evaluation/retry loops).
3. **Compute Cost per 1,000 Calls**:
   - Load pricing assumptions from `workflow-profile` (`MODEL+ENV`, `VOLUME+COST`) or customizable defaults in [references/pricing-assumptions.md](./references/pricing-assumptions.md).
   - State every pricing assumption explicitly (model name/tier, $/1M input, $/1M cached input, $/1M output, expected avg input & output tokens).
4. **Maintain Version Ledger**:
   Emit this exact table across versions:
   ```markdown
   | Version | Prompt Tokens (approx) | Avg Output Tokens (approx) | Weighted Score | Est. Cost / 1,000 Calls |
   | :--- | :---: | :---: | :---: | :---: |
   ```

## Verification

Before emitting any Token Report, verify:
- [ ] Estimation method is explicitly stated as **approximate, not exact**.
- [ ] Static vs dynamic prompt tokens and expected output tokens are reported separately.
- [ ] Cost-per-1,000-calls states exact pricing and average payload assumptions.
- [ ] Primary cost drivers are explicitly named.
