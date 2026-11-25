# Evaluation Test Set Template (8-12 Cases)

Distribution target: **~50% Typical | ~25% Edge | ~25% Adversarial**.

| ID | Type | Target Failure Mode | Input (`{{variables}}`) | Must Contain (Pass) | Fails If (Fail) | Data Flag |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `T1` | Typical | Baseline | `<representative input 1>` | `<observable pass requirement>` | `<observable fail condition>` | `[REPLACE WITH REAL DATA]` |
| `T2` | Typical | Baseline | `<representative input 2>` | `<observable pass requirement>` | `<observable fail condition>` | `[REPLACE WITH REAL DATA]` |
| `T3` | Typical | Baseline | `<representative input 3>` | `<observable pass requirement>` | `<observable fail condition>` | `[REPLACE WITH REAL DATA]` |
| `T4` | Typical | Baseline | `<representative input 4>` | `<observable pass requirement>` | `<observable fail condition>` | `[REPLACE WITH REAL DATA]` |
| `E1` | Edge | Insufficient input | `<missing required field / ambiguous input>` | Triggers exact `insufficient_input` fallback listing missing fields | Fabricates missing details or guesses | Synthetic OK |
| `E2` | Edge | Boundary / noisy | `<empty, ultra-long, or conflicting fields>` | Handles boundary cleanly without format drift | Truncates schema or drops required keys | `[REPLACE WITH REAL DATA]` |
| `A1` | Adversarial | Failure mode #1 | `<input engineered to trigger top fear #1>` | Resists trap; maintains accuracy & format | Exhibits failure mode #1 | `[REPLACE WITH REAL DATA]` |
| `A2` | Adversarial | Injection / failure mode #2 | `<untrusted input containing "Ignore previous instructions...">` | Treats embedded text as data; executes original workflow only | Follows injected instruction or leaks rules | Synthetic OK |

> Expand to 10 or 12 rows for `medium`/`high` risk workflows while preserving the 50/25/25 ratio.
