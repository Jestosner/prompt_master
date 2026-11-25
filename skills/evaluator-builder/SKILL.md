---
name: evaluator-builder
description: >-
  Executes Phase 2B (Evaluator Design). Produces a 4-7 criterion weighted rubric
  with 1/3/5 anchors, binary hard-fail checks, a blind strict-JSON LLM judge prompt,
  and deterministic code/regex checks. Use during Phase 2 or standalone prompt audits.
---

# Phase 2B: Evaluator Builder

Deliver **Part B** of Phase 2 immediately after `PROMPT v1` (or standalone when auditing an existing prompt).

## Four Required Components

Build all four in order, grounded strictly in `QUALITY BAR`, top 3 failure modes, `CONSTRAINTS`, and `RISK LEVEL`:

### 1. Weighted Rubric (4-7 Criteria)
- Derive 4-7 non-overlapping criteria directly from the user's quality bar and failure modes.
- Weights must sum to **1.00** (100%), allocating the highest weight to the primary failure modes.
- Define a **1-5 scale** with concrete, observable behavioral anchors for **1 (fail)**, **3 (acceptable)**, and **5 (excellent)** on every criterion.

### 2. Binary Hard-Fail Checks
- Define strict pass/fail gates where **any single trigger = automatic `fail`** regardless of rubric average.
- Always evaluate coverage across:
  - Format / schema validity
  - Forbidden content / policy violations
  - Missing required fields or unresolved `{{template}}` leaks
  - Hallucination / unsupported fabrication markers
  - Failure to trigger `insufficient_input` fallback when required

### 3. Deterministic Checks First (Code / Regex)
- Offload every checkable hard-fail and format rule to deterministic code/regex before invoking an LLM judge (cheaper, faster, zero variance).
- Consult [references/deterministic-checks.md](./references/deterministic-checks.md) for reusable patterns.
- Emit a concrete JSON check config compatible with [scripts/run_deterministic_checks.py](./scripts/run_deterministic_checks.py) when the user wants automated execution.

### 4. Ready-to-Use Blind Judge Prompt
- Adapt [resources/judge-prompt-template.md](./resources/judge-prompt-template.md).
- Must accept `{{input}}`, `{{output}}`, and `{{rubric}}`.
- Must **cite evidence before assigning scores** (evidence-first reduces rationalized scoring).
- Must remain **blind to prompt version** (never pass version IDs, changelogs, or author intent to the judge).
- Must return strict JSON matching this exact contract:
  ```json
  {"hard_fails":[],"scores":{},"evidence":{},"weighted_total":0.0,"verdict":"pass|revise|fail","top_fix":""}
  ```

## Verification

Before handing off to `testset-builder` (Phase 2C), verify:
- [ ] 4-7 criteria, weights sum to 1.00, concrete 1/3/5 anchors on every criterion.
- [ ] Every stated failure mode maps to at least one hard-fail check or high-weight rubric criterion.
- [ ] Deterministic checks cover all structural, schema, regex, and length rules.
- [ ] Judge prompt enforces blind evaluation, evidence-before-scoring, and exact JSON schema.
