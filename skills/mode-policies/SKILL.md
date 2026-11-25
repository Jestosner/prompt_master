---
name: mode-policies
description: >-
  Applies customizable optimization policies — balanced (default), strict
  (quality over tokens), lean (tokens over quality), or custom org policies.
  Use when the user issues the "strict" or "lean" command or configures custom budgets.
---

# Extension: Mode Policies (`strict` | `lean` | `balanced`)

Provides swap-in policy overlays that tune thresholds, example budgets, output caps, and ablation tolerances across all phases **without modifying core skills**.

## How to Apply

1. Read [references/policy-presets.yaml](./references/policy-presets.yaml).
2. Activate the policy matching `workflow_profile.mode`:
   - **`balanced` (default)**: Standard Prompt Systems Architect defaults (tier thresholds `4.0 / 4.3 / 4.7`, compression drop limit `<= 0.1`).
   - **`strict` (command: `strict`)**: Favor output quality and safety over token savings. Raise stop threshold by `+0.2` (max `4.9`), tighten Phase 4 acceptable score drop to `<= 0.05` (or skip aggressive compression), allow up to 3 minimal examples if helpful, retain explicit verification/fallback phrasing.
   - **`lean` (command: `lean`)**: Favor minimum prompt + runtime tokens while **never waiving hard-fail gates**. Cap examples at `0-1`, prefer terse schema/table directives from `v1`, enforce tight output length caps, prioritize runtime savings (tier-fast routing, static caching, input truncation), keep `<= 0.1` compression tolerance.
3. Record the active mode in `workflow_profile.mode` and state any changed numeric thresholds in one line.

## Customization Hook

Teams can add named org policies (e.g., `enterprise-compliance`, `edge-device-tiny`) directly into `references/policy-presets.yaml` and activate them without editing any other skill.
