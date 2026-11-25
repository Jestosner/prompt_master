# Risk Tiers & Evaluator Strictness (Customizable)

Edit this file to match your organization's default quality thresholds and compliance posture.

| Risk Level | Typical Use Cases | Default Stop Threshold (1-5) | Hard-Fail Gate | Recommended Mode / Checks |
| :--- | :--- | :--- | :--- | :--- |
| `low` | Drafts, internal brainstorming, ideation, rough summaries | **4.0** (or user-defined) | 0 hard fails across 2 consecutive versions | Lightweight deterministic format checks; simulation acceptable for early exploration (still labeled). |
| `medium` | Customer-facing copy, support replies, internal automation, standard structured extraction | **4.3** | 0 hard fails across 2 consecutive versions + 0 regressions | Deterministic schema/regex checks + blind judge; replace flagged synthetic tests with real samples before launch. |
| `high` | Legal, medical, financial, security, production code generation, high-stakes routing | **4.7** | 0 hard fails across 2 consecutive versions + 0 regressions | Strict grounding & abstention rules; mandatory deterministic validation; real-data test set required before production sign-off; pair with `domain-packs` (`high-risk-regulated` or `code-and-structured`). |

## Customization Notes

- **User override wins**: If the user specifies a custom score threshold (e.g., `4.5`), record it in `QUALITY BAR` and override the tier default.
- **Mode interaction**:
  - `strict` mode may raise the effective stop threshold by `+0.2` (capped at `4.9`) and narrows compression tolerance (see `mode-policies` / `skills/mode-policies`).
  - `lean` mode keeps the hard-fail gate unchanged (never compromise hard fails for tokens) while permitting standard `<= 0.1` compression tolerance.
