# Domain Pack Template: `<Your Domain Name>` (`<pack-slug>`)

Copy this file into `skills/domain-packs/references/<pack-slug>.md` and register it in `skills/domain-packs/SKILL.md`.

- **Default Risk Level**: `low | medium | high`
- **Consumer**: `<human / API / internal analyst>`

## High-Impact Intake Defaults (★)
- `<Default assumption 1>`
- `<Default assumption 2>`

## Mandatory Hard-Fail & Deterministic Checks
- `HF_<CHECK_1>`: `<exact binary failure rule>`
- `HF_<CHECK_2>`: `<exact binary failure rule>`

## Adversarial Test Archetypes (`A` Cases)
- `<Adversarial trap targeting top domain fear #1>`
- `<Adversarial trap targeting top domain fear #2>`

## Production Drift Focus
- `<Key deterministic telemetry + judge sampling cadence>`
