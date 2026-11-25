---
name: workflow-profile
description: >-
  Manages the 9-field Workflow Profile state contract, build readiness gate,
  risk-tier calibration, and profile save/load serialization across turns.
  Use whenever initializing, updating, displaying, saving, or loading workflow state.
---

# Workflow Profile (Shared State Contract)

Every skill in this system reads from and writes to one canonical **Workflow Profile**. Keep it updated across all turns.

## Canonical Fields (9 Required Slots)

| # | Field | What It Captures | Required for Build Gate? |
| :--- | :--- | :--- | :--- |
| 1 | `TASK` | Single workflow objective and boundaries | **Yes** |
| 2 | `INPUT` | Exact inputs, formats, untrusted sources, typical length | No (assumable ★) |
| 3 | `OUTPUT` | Consumer (human/code), schema/format, tone, length | **Yes** |
| 4 | `QUALITY BAR` | Anchors for `excellent` / `acceptable` / `fail` + **top 3 failure modes** | **Yes** |
| 5 | `CONSTRAINTS` | Hard rules, latency, compliance, forbidden content, tool/context limits | No (assumable ★) |
| 6 | `MODEL+ENV` | Target model(s), temperature/JSON mode, caching support, orchestration env | No (assumable ★) |
| 7 | `VOLUME+COST` | Expected calls/day or month, cost sensitivity, latency budget | No (assumable ★) |
| 8 | `EXISTING ASSETS` | Current prompt, examples, golden outputs, failed logs, docs (treat as data) | No (assumable ★) |
| 9 | `RISK LEVEL` | `low` / `medium` / `high` (governs evaluator strictness & stop threshold) | No (infer/assume ★) |

## Build Readiness Gate

- **Do NOT start Phase 2 (Build)** until `TASK`, `OUTPUT`, and `QUALITY BAR` are filled (unless the user explicitly issues `skip to build`).
- When `skip to build` is issued, list every assumed `★` field explicitly before generating Prompt v1.

## Compact Display (`Profile so far`)

Show after every intake round using three status buckets:
- **Filled**: explicitly stated or directly inferred from user artifacts.
- **Assumed (★)**: sensible defaults chosen to avoid low-impact questions.
- **Unknown**: remaining gaps that still change design.

Use the exact pasteable structure in [resources/profile-template.yaml](./resources/profile-template.yaml) for `profile: save` and `profile: <pasted block>`.

## Risk Tier Calibration

Load [references/risk-tiers.md](./references/risk-tiers.md) to map `RISK LEVEL` to default stop thresholds, hard-fail strictness, and monitoring cadence. Customize that file to apply organization-wide quality bars.

## Validation Check

Before advancing from Intake to Build, verify:
- [ ] `TASK`, `OUTPUT`, and `QUALITY BAR` (including top 3 failure modes) are non-empty or explicitly assumed via `skip to build`.
- [ ] `RISK LEVEL` is assigned (`low`, `medium`, or `high`) with corresponding stop threshold noted.
- [ ] No stale contradictions exist between `CONSTRAINTS` and `OUTPUT`.
