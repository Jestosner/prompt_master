---
name: release-packager
description: >-
  Compiles the final 6-part production deliverable package once the stop condition
  is met: copy-paste Final Prompt, complete Evaluator, Test Set, reusable Workflow
  Profile, cross-version Token/Cost table, and production monitoring plan.
---

# Final Deliverable: Release Packager

Compile one self-contained, production-ready handoff package once the iteration stop condition (and optional Phase 4 optimization) is complete.

## Prerequisite Gate

Confirm before packaging:
- [ ] Phase 3 stop condition met (score >= threshold, 0 hard fails across 2 consecutive versions, 0 regressions).
- [ ] If Phase 4 ran, final accepted prompt passed the `<= 0.1` score drop & `0` hard-fail regression gate.
- [ ] If any final scores came from simulation rather than real model runs, prominently mark the release `SIMULATED, verify with real runs before production deployment`.

## Required 6-Part Output Package

Use [resources/release-package-template.md](./resources/release-package-template.md) and include every section with zero omissions:

1. **Final Prompt**: Copy-paste ready, cache-ordered (static prefix first, dynamic `{{variables}}` last), with full Variables Manifest.
2. **Evaluator**: Weighted rubric (1/3/5 anchors), binary hard-fail list, deterministic code/regex checks, and blind strict-JSON judge prompt.
3. **Test Set**: Final 8-12 cases (typical / edge / adversarial) with remaining `[REPLACE WITH REAL DATA]` flags clearly called out.
4. **Reusable Workflow Profile Block**: Complete YAML block loadable via `profile: <pasted block>`.
5. **Token / Cost Table Across Versions**: `v1` through final accepted version (`version | prompt tokens | avg output tokens | weighted score | est. cost per 1,000 calls`) + approximate estimation method & pricing assumptions.
6. **Known Limitations & Production Monitoring**: Call `drift-monitor` to populate residual risks, drift signals, sampling cadence, and re-evaluation triggers. Never promise zero errors.

## Verification

Before sending the Final Deliverable, check:
- [ ] All 6 required sections are present and internally consistent (same variables, criteria, and version IDs).
- [ ] Zero unsupported quality claims; every metric references scored runs.
- [ ] Residual risks and real-data replacement actions are explicitly stated.
