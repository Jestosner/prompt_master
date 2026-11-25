---
name: testset-builder
description: >-
  Executes Phase 2C (Test Set Design). Generates 8-12 balanced test cases
  (50% typical, 25% edge, 25% adversarial) targeting stated failure modes,
  with pass/fail assertions and real-data replacement flags.
---

# Phase 2C: Test Set Builder

Deliver **Part C** of Phase 2 immediately after the Evaluator (or standalone to build a regression harness for an existing prompt).

## Composition Rules

Generate **8 to 12 test cases** distributed strictly as:

| Category | Share | Target Count (8 / 10 / 12) | Purpose |
| :--- | :--- | :--- | :--- |
| **Typical** | ~50% | 4 / 5 / 6 | Representative everyday production inputs across common variants |
| **Edge** | ~25% | 2 / 3 / 3 | Boundary lengths, missing/partial fields, contradictory inputs, empty/minimal payloads triggering `insufficient_input` fallback |
| **Adversarial** | ~25% | 2 / 2 / 3 | Directly attack the user's top 3 failure modes + prompt injection attempts embedded inside untrusted inputs |

## Required Fields Per Test Case

Use [resources/testset-template.md](./resources/testset-template.md). Every case MUST specify:
1. **Case ID & Type** (`T1..`, `E1..`, `A1..`) + targeted failure mode (for edge/adversarial).
2. **Input**: Concrete, realistic payload matching the prompt's `{{variables}}`.
3. **Must Contain (Pass Criteria)**: Specific observable facts, structure, or fallback behavior required to pass.
4. **Fails If (Fail Criteria)**: Specific error, hallucination, format break, or policy violation that fails the case.
5. **Data Provenance Flag**: Mark synthetic cases with `[REPLACE WITH REAL DATA]` whenever realism materially affects accuracy (especially domain jargon, noisy formatting, or high-risk inputs).

## Verification

Before handing off to `token-auditor` (Phase 2D), verify:
- [ ] Total cases between 8 and 12, matching ~50% / ~25% / ~25% split.
- [ ] Every stated failure mode from `QUALITY BAR` is targeted by at least one adversarial or edge case.
- [ ] At least one edge case explicitly tests the `"insufficient input"` fallback.
- [ ] At least one adversarial case tests untrusted-input prompt injection (if inputs contain external/user text).
- [ ] Synthetic cases needing production examples are explicitly flagged `[REPLACE WITH REAL DATA]`.
