# Domain Pack: Code & Structured Outputs (`code-and-structured`)

- **Default Risk Level**: `high` (production code) or `medium` (internal structured data)
- **Consumer**: Downstream compiler, parser, or API

## High-Impact Intake Defaults (★)
- Output must be raw structured JSON/code with **zero markdown fences and zero prose preamble** (unless compiler/formatter explicitly expects fenced blocks).
- Never invent APIs, imports, column names, or IDs not present in provided schemas/context.

## Mandatory Hard-Fail & Deterministic Checks
- `HF_SYNTAX_OR_SCHEMA_INVALID`: Fails parser (`json.loads`, AST parse, SQL/schema validator).
- `HF_PREAMBLE_OR_FENCE_LEAK`: Leading/trailing prose or unintended ```` ``` ```` wrappers.
- `HF_FABRICATED_SYMBOL`: References undefined APIs, table columns, or field names not in input schema.
- `HF_UNSAFE_CODE_PATTERN`: Hardcoded secrets, unparameterized SQL interpolation, shell injection (`eval`/unsanitized input).

## Adversarial Test Archetypes (`A` Cases)
- Input schema with subtle breaking type change or missing optional field.
- Untrusted input field containing JSON-breaking quotes, escaped characters, or prompt injection.
- Request referencing a non-existent function/column -> must trigger `insufficient_input` rather than hallucinating.

## Production Drift Focus
- 100% deterministic schema/AST validation gate before downstream execution; immediate alert on `> 0.1%` parse errors.
