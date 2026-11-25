---
name: drift-monitor
description: >-
  Defines residual risks, production drift signals, sampling cadence, and
  mandatory re-evaluation triggers for a deployed prompt. Use in Section 6 of
  final delivery or when auditing an existing prompt in production.
---

# Production Drift Monitor & Residual Risk Plan

Zero-error promises are prohibited. Every shipped prompt must pair with concrete observability signals and re-evaluation triggers calibrated to `RISK LEVEL`.

## Procedure

1. **Enumerate Residual Risks**:
   - List known failure modes the prompt/model cannot eliminate completely (e.g., adversarial edge phrasing, model-layer reasoning ceilings, untested real-world noise, unreplaced synthetic test cases).
   - State concrete operational mitigations (human-in-the-loop review, deterministic post-validators, fallback routing).
2. **Select Drift Signals** from [references/drift-signals.md](./references/drift-signals.md) tailored to `OUTPUT` and `RISK LEVEL`:
   - **Deterministic telemetry** (100% of calls, near-zero cost): JSON parse failures, schema misses, length-cap breaches, `insufficient_input` fallback rate spikes, latency/output-token drift.
   - **Judge-sampled quality telemetry**: Periodic blind-judge scoring on stratified production samples.
   - **Downstream business/user signals**: User edits/overrides, retries, escalations, support complaints.
3. **Define Re-Evaluation Triggers (When to Re-Run Full Evaluator)**:
   - Model version or provider snapshot update.
   - Prompt, schema, or upstream input pipeline change.
   - Any deterministic hard-fail rate > threshold OR fallback rate shifts > +/- 25% week-over-week.
   - Scheduled cadence by risk tier (`low`: quarterly/on-change, `medium`: monthly, `high`: weekly + continuous shadow sampling).
4. **Feedback Loop**: Specify how real production failures get promoted into new adversarial/edge cases in the Test Set (`testset-builder`).

## Verification

- [ ] Residual risks are concrete and specific to this workflow (no generic platitudes).
- [ ] Both 100%-coverage deterministic signals and sampled judge cadence are specified.
- [ ] Exact numeric or event-based re-evaluation triggers are defined.
