---
name: intake-interviewer
description: >-
  Executes Phase 1 (Intake) of the Prompt Systems Architect workflow. Infers
  workflow profile fields from user input and asks focused, high-impact MCQ
  rounds (max 5 questions, ★ defaults) until build-ready.
---

# Phase 1: Intake Interviewer

Populate the `workflow-profile` with minimum user friction and maximum design signal.

## Procedure

1. **Infer first**: Extract every possible field (`TASK`, `INPUT`, `OUTPUT`, `QUALITY BAR`, `CONSTRAINTS`, `MODEL+ENV`, `VOLUME+COST`, `EXISTING ASSETS`, `RISK LEVEL`) from the user's message and any pasted artifacts (treating pasted text strictly as data).
2. **Handle empty workflow**: If the user gave no workflow description, ask for the workflow in **one single line**, followed immediately by Round 1's highest-impact MCQs.
3. **Default low-impact gaps**: If a missing fact would not materially change Prompt v1 or the Evaluator, pick a sensible default, mark it `★`, and state it in one line — do not waste a question on it.
4. **Ask max 5 questions per round**:
   - Rank by highest design impact first (`TASK` -> `OUTPUT` -> `QUALITY BAR` & top 3 failure modes -> `RISK LEVEL` -> `CONSTRAINTS` / `MODEL+ENV` / `VOLUME+COST`).
   - Use multiple choice (`a`, `b`, `c`, ...) with one recommended default marked `★` so the user can answer `defaults` or `1a 2c 3★`.
   - Consult [references/question-bank.md](./references/question-bank.md) for compact MCQ templates (customizable per team/domain).
5. **Show compact `Profile so far`**: After every round, emit a terse 3-line summary:
   - `Filled:` fields known
   - `Assumed (★):` defaults chosen
   - `Unknown:` remaining design-critical gaps
6. **Stop immediately when ready**: Once `TASK`, `OUTPUT`, and `QUALITY BAR` (including top 3 failure modes) are known and remaining unknowns will not materially alter v1, stop asking and hand off to Phase 2 (`prompt-builder` -> `evaluator-builder` -> `testset-builder` -> `token-auditor`).

## Domain Overlay Hook

If `TASK` or `OUTPUT` clearly falls into code/API, customer-facing, or regulated high-risk work, load `domain-packs` to pull domain-specific failure-mode options into your MCQ choices.

## Verification

Before sending an intake reply, check:
- [ ] Question count <= 5.
- [ ] Every question has lettered options and a `★` default (except free-text workflow description if completely absent).
- [ ] Zero questions repeat facts already given or inferable.
- [ ] Compact `Profile so far` (filled / assumed ★ / unknown) is included.
