# Deterministic Check Patterns (Pre-Judge Layer)

Always run deterministic checks **before** calling an LLM judge. If any hard-fail deterministic check triggers, fail immediately and save judge tokens.

## Reusable Check Categories

| Category | Deterministic Mechanism | Example Hard-Fail ID |
| :--- | :--- | :--- |
| **JSON validity** | `json.loads(output)` with strict no-fence requirement | `HF_INVALID_JSON` |
| **Required keys** | Set difference `required_keys - parsed.keys()` | `HF_MISSING_KEY` |
| **Allowed enum values** | Membership check `parsed["status"] in allowed` | `HF_INVALID_ENUM` |
| **No template leaks** | Regex `\{\{[^}]+\}\}` must NOT match | `HF_TEMPLATE_LEAK` |
| **No preamble / wrapper** | Leading/trailing regex check (e.g., no ```` ``` ```` or `"Sure,"`) | `HF_PREAMBLE_LEAK` |
| **Length / budget cap** | Word count <= `max_words` or char count <= `max_chars` | `HF_LENGTH_EXCEEDED` |
| **Forbidden phrases / PII** | Case-insensitive regex list (e.g., SSN, API keys, banned claims) | `HF_FORBIDDEN_CONTENT` |
| **Required sections / citations** | Regex presence check (e.g., `\[source:\s*\d+\]`) | `HF_MISSING_CITATION` |
| **Exact ID preservation** | Extract IDs from output; verify subset of IDs in input | `HF_FABRICATED_ID` |

## Example Check Config for `scripts/run_deterministic_checks.py`

```json
{
  "require_json": true,
  "required_keys": ["summary", "status", "missing_fields"],
  "max_words": 200,
  "forbid_template_leaks": true,
  "forbidden_regex": [
    {"id": "HF_PREAMBLE", "pattern": "^(sure|here is|certainly)[,!:\\s]"},
    {"id": "HF_CODE_FENCE", "pattern": "```"}
  ],
  "required_regex": []
}
```
