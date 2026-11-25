# Pricing & Estimation Assumptions (Customizable)

Edit these reference rates to match your actual provider contract and model tier. Always state which row/custom rate was used in every Token Report.

## Approximate Tokenization Heuristics

- **English prose / instructions**: ~4.0 characters/token (~1.33 tokens/word).
- **JSON / code / punctuation-heavy schemas**: ~3.2-3.6 characters/token.
- **Non-Latin scripts**: often 1.5x-3.0x higher token density than English; calibrate against the provider's official tokenizer before high-volume launch.

> **Mandatory Disclosure**: Heuristic counts are **approximate, not exact**. Validate final production budgets with the target provider's official `countTokens` / tokenizer API.

## Editable Reference Model Tiers (USD per 1M Tokens — Illustrative Placeholders)

Replace with live provider pricing for your deployment:

| Tier Label | Input ($ / 1M) | Cached Input ($ / 1M) | Output ($ / 1M) | Typical Role |
| :--- | :---: | :---: | :---: | :--- |
| `tier-fast` (small/flash) | `0.15` | `0.04` | `0.60` | High-volume classification, extraction, Tier-1 router |
| `tier-standard` (mid) | `1.25` | `0.31` | `5.00` | General customer-facing & structured synthesis |
| `tier-frontier` (flagship) | `3.00` | `0.75` | `15.00` | High-risk reasoning, complex code, escalation Tier-2 |

## Cost Formula (per 1,000 calls)

- **Uncached**: `((static_in + dynamic_in) * price_in + avg_out * price_out) / 1000`
- **With static prefix caching** (assuming steady-state hit rate `h`, e.g., `0.85`):
  `((static_in * (h * price_cached + (1 - h) * price_in) + dynamic_in * price_in) + avg_out * price_out) / 1000`
