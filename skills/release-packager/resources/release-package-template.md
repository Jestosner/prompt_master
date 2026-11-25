# Final Deliverable Package Template

Emit all 6 sections in one cohesive handoff artifact.

---

## 1. Final Prompt (`<version_id>`)

```text
<Copy-paste ready final prompt, static prefix first, {{variables}} last>
```

### Variables Manifest
| Variable | Type | Source (Trusted/Untrusted) | Required | Truncation / Default |
| :--- | :--- | :--- | :---: | :--- |
| `{{var}}` | string | untrusted | yes | `<policy>` |

---

## 2. Evaluator

- **Rubric (Weights sum = 1.00)**: `<table with criterion, weight, 1 / 3 / 5 anchors>`
- **Binary Hard-Fail Checks**: `<ID -> rule>`
- **Deterministic Checks (Run First)**: `<regex/schema/JSON config>`
- **Blind Judge Prompt**: `<ready-to-use strict JSON prompt>`

---

## 3. Test Set (`<N>` Cases)

`<Final typical / edge / adversarial table; highlight any remaining [REPLACE WITH REAL DATA] items>`

---

## 4. Reusable Workflow Profile

```yaml
# Load with: profile: <paste this block>
<Filled canonical workflow_profile YAML>
```

---

## 5. Token & Cost Ledger Across Versions

- **Estimation method**: Approximate heuristic (`<method>`); not exact tokenizer.
- **Pricing assumptions**: `<model tier, $/1M input, $/1M cached, $/1M output, avg dynamic input, cache hit rate>`.

| Version | Prompt Tokens (approx) | Avg Output Tokens (approx) | Weighted Score | Est. Cost / 1,000 Calls |
| :--- | :---: | :---: | :---: | :---: |
| `v1` | — | — | — | — |
| `v_final` | — | — | — | — |

---

## 6. Known Limitations, Residual Risks & Production Monitoring

- **Verification status**: `<Real runs | SIMULATED, verify with real runs before production>`
- **Known limitations & residual risks**: `<bullet list — never promise zero errors>`
- **Drift signals to monitor**: `<from drift-monitor>`
- **Re-evaluation triggers**: `<exact events that mandate re-running the evaluator>`
