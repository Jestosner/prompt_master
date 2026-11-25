---
name: prompt-refiner
description: >-
  Executes Phase 3 Steps 4-6 (Minimal-Edit Patching, Regression Check, and Stop Gate).
  Proposes minimal hypothesis-driven edits, emits PROMPT v(n+1) with structured changelog,
  blocks wholesale rewrites, and checks the iteration stop condition.
---

# Phase 3 (Steps 4-6): Prompt Refiner & Stop Gate

Turn root-cause failure clusters from `eval-runner` into minimal, verifiable prompt patches.

## Procedure

### 1. Propose the Minimal Edit Set
- **Never rewrite wholesale.** Change only the smallest set of lines required to address observed failures.
- Attach **one explicit hypothesis per edit**.
- Skip prompt edits for failures diagnosed as `bad test case` (fix the test case instead) or pure `model limitation` (flag model routing / code offloading instead).
- Preserve cache ordering (static prefix first, `{{variables}}` last).

### 2. Issue `PROMPT v(n+1)` + Structured Changelog
Use [resources/changelog-template.md](./resources/changelog-template.md). Every edit MUST log:
`[edit] -> [failure targeted (Case IDs + root cause)] -> [expected effect]`

### 3. Run Regression Check
- Re-evaluate **both** previously failing cases AND previously passing cases on `PROMPT v(n+1)`.
- Flag any previously passing case that drops below pass or introduces a hard fail as a **Regression**.
- If a regression occurs, revert or narrow the offending edit before advancing.

### 4. Evaluate Stop Condition
Stop Phase 3 and unlock Phase 4 (`token-optimizer`) or Final Delivery (`release-packager`) **only when ALL three hold**:
1. **Score bar**: Weighted mean score >= threshold (default `4.3` medium risk, `4.7` high risk, `4.0` low risk, or user-defined override / `mode-policies` override).
2. **Zero hard fails (sustained)**: `0` hard fails across **two consecutive versions** (e.g., `v2` and `v3`, or `v1` and a clean confirmation/patch pass).
3. **Zero regressions**: No previously passing test case regressed.

> Note: Simulated runs (`SIMULATED, verify with real runs`) can guide draft iterations, but for `medium`/`high` risk workflows, explicitly flag that real-run verification is required before declaring production sign-off.

## Verification

Before emitting `PROMPT v(n+1)`, verify:
- [ ] Zero unlinked edits (every single line change traces to a specific failure cluster & hypothesis).
- [ ] Static-first / variable-last caching boundary remains intact.
- [ ] Changelog uses exact `[edit] -> [failure targeted] -> [expected effect]` format.
- [ ] Regression status and explicit Stop Condition verdict (`CONTINUE` vs `STOP MET`) are stated.
