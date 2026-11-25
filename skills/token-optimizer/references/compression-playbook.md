# Prompt, Output & Runtime Compression Playbook

## 1. Prompt Compression Patterns (Input Tokens)

| Bloated Pattern | Compact Replacement | Typical Savings |
| :--- | :--- | :---: |
| Multi-sentence prose describing output fields | Inline JSON schema with type comments | 40-65% |
| "Please make sure that you never invent or hallucinate..." | `Use only facts in <input_data>; return null if absent.` | 50-70% |
| 3 verbose full-length few-shot examples | 1 minimal synthetic example targeting only the tricky format edge | 60-80% |
| Repeated rules in Role, Rules, and Output sections | Single canonical rule in `[RULES]` | 20-40% |
| Inline conditional prose ("If X then Y, else if Z...") | 2-column decision table | 30-50% |

## 2. Output Compression Patterns (Highest Dollar Leverage)

- **Zero wrapper**: `"Output raw JSON only; no markdown fences, no commentary."`
- **Reasoning suppression (when not needed by consumer)**: Return final fields directly instead of prose explanations; if chain-of-thought is required for accuracy, cap reasoning field (e.g., `<= 25 words`) or drop it for `tier-standard`/`tier-fast` once verified via ablation.
- **Compact enums & booleans**: Replace descriptive strings (`"The input did not have enough information"`) with `status: "insufficient_input"` + `missing: [...]`.
- **Hard caps**: Bound list sizes (`max 3 bullets, <= 12 words each`).

## 3. Runtime Cost Levers (System Architecture)

| Lever | When to Recommend | Expected Savings | Guardrail |
| :--- | :--- | :---: | :--- |
| **Static Prefix Caching** | Static prompt >= provider cache min & repeated across calls | 50-90% on static input | Never inject timestamps/IDs above the dynamic boundary. |
| **Cheaper Model + Escalation** | High volume, >70% easy typical cases | 40-80% total cost | Escalate on deterministic fail, low confidence enum, or high-risk input flag. |
| **Batch API** | Non-real-time / offline jobs (nightly evals, backfills) | ~50% API rate | Confirm latency SLA tolerates 1-24h turnaround. |
| **Pre-Filtering & Truncation** | Long noisy inputs (HTML, transcripts, logs) | 30-75% dynamic input | Strip boilerplate deterministically in code before LLM call; verify recall on edge tests. |
