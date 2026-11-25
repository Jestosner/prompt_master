# Prompt Iteration Changelog & Regression Ledger

## `PROMPT v(n+1)` Changelog

| Edit ID | Exact Diff (`[edit]`) | Failure Targeted (`[Case IDs + root cause]`) | Hypothesis (`[expected effect]`) |
| :--- | :--- | :--- | :--- |
| `E1` | `<add/modify/remove exact line>` | `A1, E2` (`ambiguous instruction`) | `<measurable expected score/pass change>` |
| `E2` | `<add/modify/remove exact line>` | `T3` (`format drift`) | `<measurable expected score/pass change>` |

## Regression & Stop-Gate Check

| Gate Criterion | Current (`v(n+1)`) | Previous (`v(n)`) | Status |
| :--- | :---: | :---: | :---: |
| Mean Weighted Score (>= `<threshold>`) | `0.00` | `0.00` | PASS / FAIL |
| Hard Fails (`0` across 2 consecutive versions) | `0` | `0` | PASS / FAIL |
| Regressions on Previously Passing Cases | `0` | — | PASS / FAIL |
| Verification Source | Real / `SIMULATED, verify with real runs` | Real / Simulated | — |

**Iteration Decision**: `CONTINUE (Phase 3)` | `STOP MET -> Unlock Phase 4 (token-optimizer) or Deliver (release-packager)`
