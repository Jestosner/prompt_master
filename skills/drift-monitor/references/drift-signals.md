# Production Drift Signals & Re-Eval Thresholds (Customizable)

Customize these alert thresholds and review cadences to match your team's SLOs.

## 1. Deterministic Telemetry (Run on 100% of Production Calls)

| Signal | What It Detects | Default Alert Trigger |
| :--- | :--- | :--- |
| **Format / Schema Failure Rate** | Model update drift, prompt truncation, edge-case input breakage | `> 0.5%` (medium) / `> 0.1%` (high) |
| **`insufficient_input` Fallback Rate** | Upstream data pipeline break OR overly conservative prompt | Shifts `> ±25%` vs 7-day baseline |
| **Output Token Length Drift** | Verbosity creep, cost blowup, reasoning-loop regressions | P95 output tokens `> +20%` vs baseline |
| **Template / Delimiter Leak** | Broken variable interpolation or prompt-injection breakthrough | `> 0` occurrences (immediate alert) |
| **Latency / Escalation Spike** | Tier-1 model degradation triggering Tier-2 fallback | Escalation rate `> +15%` vs baseline |

## 2. Blind-Judge Sampling Cadence by Risk Level

| Risk Level | Production Sample Size | Cadence | Mandatory Full-Suite Re-Eval Triggers |
| :--- | :---: | :---: | :--- |
| `low` | 20-30 calls | Monthly or on-change | Model swap, schema edit, user complaint spike |
| `medium` | 50-100 calls | Bi-weekly / Monthly | Any deterministic alert, model snapshot bump, input distribution change |
| `high` | 100-200 calls (stratified incl. edge inputs) | Weekly | Any single hard-fail in production, any model/provider change, policy update |

## 3. Regression Dataset Growth Rule

Every confirmed production failure should be scrubbed of PII and added as a permanent regression case (`E` or `A`) in the workflow's Test Set before shipping the next prompt patch.
