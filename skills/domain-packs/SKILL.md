---
name: domain-packs
description: >-
  Loads swappable domain specialization overlays (code/API, customer-facing,
  high-risk regulated, or custom) that inject domain-specific intake defaults,
  hard-fail checks, adversarial test patterns, and drift signals.
---

# Extension: Domain Packs (Swappable Domain Overlays)

Enrich Intake, Evaluator, Test Set, and Drift Monitoring with domain-proven defaults without bloating core skills.

## Available Packs (Load Only the Matching Reference)

| Domain Pack | When to Load | Reference File |
| :--- | :--- | :--- |
| **`code-and-structured`** | Production code generation, SQL/JSON/API payloads, deterministic tool orchestration | [references/code-and-structured.md](./references/code-and-structured.md) |
| **`customer-facing`** | Customer support replies, sales/UX copy, user-visible summaries, helpdesk triage | [references/customer-facing.md](./references/customer-facing.md) |
| **`high-risk-regulated`** | Legal, medical, financial, compliance, security review, policy adjudication | [references/high-risk-regulated.md](./references/high-risk-regulated.md) |
| **`custom`** | User-authored domain overlay | Copy [references/custom-domain-template.md](./references/custom-domain-template.md) |

## Procedure

1. Match `TASK` / `OUTPUT` / `RISK LEVEL` to at most **one primary pack** (or combine `code-and-structured` + `high-risk-regulated` if building regulated production code).
2. Read ONLY the selected reference file (progressive disclosure).
3. Inject its:
   - **Intake failure-mode defaults** into `intake-interviewer`,
   - **Hard-fail & deterministic checks** into `evaluator-builder`,
   - **Adversarial test archetypes** into `testset-builder`,
   - **Production drift checks** into `drift-monitor`.
4. Record the active pack in `workflow_profile.domain_pack`.

## Adding Your Own Pack

Duplicate `references/custom-domain-template.md`, rename it (e.g., `references/ecommerce-catalog.md`), and add a row to the table above. No core skill edits required.
