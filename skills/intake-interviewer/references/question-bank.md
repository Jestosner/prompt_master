# High-Impact Intake Question Bank (Customizable)

Select only questions targeting **unknown, design-changing fields**. Never ask more than 5 in one round. Re-rank dynamically by impact.

## Priority 1 — Consumer & Output Contract (`OUTPUT`)

- **Output consumer & format**:
  - a) Downstream code/API (strict JSON/schema, zero prose)
  - b) Human end-user (structured markdown/plain text) ★
  - c) Internal analyst/reviewer (table + brief rationale)
  - d) Custom format (specify)

## Priority 2 — Quality Bar & Top 3 Failure Modes (`QUALITY BAR`)

- **Primary failure modes to eliminate (pick up to 3)**:
  - a) Hallucination / inventing facts not in input ★
  - b) Wrong format / broken schema / missing required fields ★
  - c) Verbose filler, hedging, or wrong tone
  - d) Missing edge-case handling or failing to abstain on insufficient input ★
  - e) Policy / safety / compliance violation
  - f) Other (list your top 3 fears)

- **What separates `excellent` from `acceptable`?**
  - a) Concise, exact adherence to input facts + zero post-editing needed ★
  - b) High recall / thorough coverage even if slightly longer
  - c) Creative / persuasive phrasing matching a brand voice

## Priority 3 — Risk Level & Strictness (`RISK LEVEL`)

- **Blast radius if output is wrong**:
  - a) Low — internal drafts/brainstorming (stop bar 4.0)
  - b) Medium — customer-facing or automated internal ops (stop bar 4.3) ★
  - c) High — legal, medical, financial, security, or production code (stop bar 4.7)

## Priority 4 — Input Shape & Insufficient-Input Policy (`INPUT`, `CONSTRAINTS`)

- **When input is incomplete, ambiguous, or contradictory, the prompt should**:
  - a) Abstain / return structured `insufficient_input` with missing fields listed ★
  - b) Answer what is supported and flag gaps explicitly
  - c) Ask clarifying questions (interactive flows only)

## Priority 5 — Runtime, Model & Scale (`MODEL+ENV`, `VOLUME+COST`)

- **Runtime scale & optimization priority**:
  - a) Low volume (<1k calls/mo) — optimize quality first (`strict`)
  - b) Medium volume (1k-100k calls/mo) — balance quality and tokens ★
  - c) High volume (>100k calls/mo) — aggressively optimize cost/caching (`lean`)

- **Model & caching environment**:
  - a) Frontier model, prompt caching supported ★
  - b) Fast/small model (strict instructions, simpler schema)
  - c) Multi-model router (cheap default + frontier escalation)
  - d) Specify exact model + constraints

## Customization Notes

Teams can append org-specific MCQ blocks (e.g., PII redaction rules, localization languages, internal schema standards) directly below or via the `domain-packs` skill (`skills/domain-packs`).
