# Prompt Master; An Antigravity Plugin & Modular Prompt Systems Architect

A publishable **Antigravity Plugin** bundling **14 modular Agent Skills (`SKILL.md`)** implementing the **Prompt Systems Architect** methodology: designing, testing, evaluating, refining, and token-optimizing a production prompt and its evaluator for one workflow at a time.

## Quick Start

### Use as a Global Plugin (Recommended)
1. **Install globally**: Place this plugin folder at `~/.gemini/config/plugins/prompt-master/` (or install from your published repository with `agy plugin install <repo-url>`).
2. **Toggle anytime**: Enable or disable **Prompt Master** live from Antigravity's Customizations UI — once enabled, all 14 skills are available in **any** directory/workspace.
3. **Start a workflow**: Tell your agent to use `prompt-architect` and describe your workflow (or pick one of the plugin's starter prompts).

### Use Locally in a Single Workspace (Optional Preset Mode)
- [.agents/skills.json](.agents/skills.json) registers `skills/` for workspace auto-discovery if you open this repository directly without installing the global plugin.
- To load only a subset of skills in a workspace, copy any manifest from `presets/*.skills.json` into `.agents/skills.json`.

### Session Commands Available Anytime
- `profile: save` / `profile: <pasted block>` — export or resume a Workflow Profile
- `strict` / `lean` — toggle quality-first vs token-first policies
- `defaults` — accept all `★` MCQ options in the current intake round
- `skip to build` — jump straight to Phase 2 with explicit listed assumptions
- `new workflow` — reset state for a new workflow while keeping the framework

## Directory Layout

```text
prompt_master/
├── plugin.json                # Antigravity plugin manifest
├── assets/logo.svg            # Plugin icon (128x128 SVG)
├── skills/                    # 14 modular Agent Skills (flat 1-level plugin layout)
│   ├── prompt-architect/      # Core: orchestrator, operating laws & command router
│   ├── workflow-profile/      # Core: 9-field state contract & risk-tier calibration
│   ├── intake-interviewer/    # Core: Phase 1 inference-first MCQ intake
│   ├── prompt-builder/        # Build: Phase 2A production Prompt v1 authoring
│   ├── evaluator-builder/     # Build: Phase 2B rubric, hard-fails & blind judge
│   ├── testset-builder/       # Build: Phase 2C balanced & adversarial test set
│   ├── eval-runner/           # Iterate: Phase 3.1-3.3 scoring & failure clustering
│   ├── prompt-refiner/        # Iterate: Phase 3.4-3.6 minimal diffs & stop gate
│   ├── token-auditor/         # Optimize: Phase 2D baseline & cost ledger
│   ├── token-optimizer/       # Optimize: Phase 4 post-stability ablation & compression
│   ├── release-packager/      # Deliver: 6-part production handoff package
│   ├── drift-monitor/         # Deliver: residual risks, telemetry & drift triggers
│   ├── mode-policies/         # Extension: balanced / strict / lean policy overlays
│   └── domain-packs/          # Extension: code, customer-facing & regulated domain packs
├── .agents/skills.json        # Workspace auto-discovery fallback
├── presets/                   # Selective skill-subset manifests for workspace mode
│   ├── full.skills.json       # All 14 skills (end-to-end architect)
│   ├── quick-build.skills.json# Core + Build + Token Auditor + Domain Packs
│   ├── eval-audit.skills.json # Audit an existing prompt (Rubric + Tests + Runner + Drift)
│   ├── cost-cut.skills.json   # Optimize a stable prompt (Runner + Optimize + Modes)
│   └── high-risk.skills.json  # Full suite for strict/regulated workflows (use with 'strict')
├── COMPONENT_SETS.md          # Full dependency map, contracts & customization matrix
└── README.md
```

## Optional Zero-Dependency Helper Scripts (Python 3)

Three skills include runnable stdlib Python utilities for deterministic verification:

- **Deterministic Hard-Fail Checker**:
  `python skills/evaluator-builder/scripts/run_deterministic_checks.py --config checks.json --output out.txt`
- **Rubric Scorer, Regression & Stop-Gate Verifier**:
  `python skills/eval-runner/scripts/score_rubric.py --rubric rubric.json --results v2.json --prev v1.json --markdown`
- **Approximate Token & Cost/1k-Calls Estimator**:
  `python skills/token-auditor/scripts/estimate_tokens.py --prompt prompt.txt --dynamic-in 300 --avg-out 150`
