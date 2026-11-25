# Session Command Router

Commands work at any turn without resetting the session or losing framework rules.

| Command | Action | State Transition |
| :--- | :--- | :--- |
| `profile: save` | Emit current Workflow Profile using `workflow-profile/resources/profile-template.yaml` format. | Stay in current phase. |
| `profile: <pasted block>` | Parse all 9 fields + version/mode metadata; summarize loaded state in 1 compact block; resume from earliest incomplete phase. | Jump to matching phase (Intake / Build / Iterate / Optimize / Deliver). |
| `strict` | Activate `strict` policy in `mode-policies` (raise quality priority, tighten ablation tolerance, preserve edge-case safeguards). | Stay in current phase; record `MODE: strict`. |
| `lean` | Activate `lean` policy in `mode-policies` (favor lower token footprint, stricter output caps, aggressive compression within safety bounds). | Stay in current phase; record `MODE: lean`. |
| `new workflow` | Reset Workflow Profile, version ledger, and test set; retain active skill set and custom policies. | Jump to Phase 1 (Intake). |
| `defaults` | Accept every `★` recommended option from the most recent intake round and update Workflow Profile. | Advance to next intake round or Phase 2 if build gate is met. |
| `skip to build` | Fill all remaining unknown fields with sensible `★` assumptions, list every assumption explicitly, and start Phase 2 (A -> B -> C -> D). | Jump to Phase 2 (Build). |

## Shorthand Reply Parsing

During Phase 1 intake, accept compact shorthand replies alongside commands:
- `1a 2c 3★` -> apply choice `a` to Q1, `c` to Q2, recommended default to Q3.
- `defaults, except 2b` -> apply `★` to all except Q2 (`b`).
- `defaults + skip to build` -> apply `★` to current round and assume defaults for any remaining unknowns, then build.
