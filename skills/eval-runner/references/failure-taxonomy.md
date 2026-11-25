# Root-Cause Failure Taxonomy (5 Categories)

Classify every failing or `revise` test case before proposing edits. Misclassifying root causes leads to bloated prompts that fix the wrong thing.

| Root Cause | Diagnostic Signal | Typical Fix (Minimal Edit) | Avoid |
| :--- | :--- | :--- | :--- |
| **`ambiguous instruction`** | Model interprets a rule inconsistently across similar cases or picks an unintended tie-break. | Replace vague adjective with a concrete observable condition or decision rule. | Adding 3 redundant restatements of the same vague rule. |
| **`missing context`** | Model fabricates or misclassifies because a domain definition, lookup rule, or boundary condition is absent. | Add the exact missing fact/definition to `[CONTEXT]` or tighten `[FALLBACK BEHAVIOR]`. | Blaming the model when the input/context lacked the fact. |
| **`format drift`** | Content is right, but JSON breaks, markdown fences leak, keys rename, or length exceeds cap. | Clarify `[OUTPUT FORMAT]` schema, add 1 minimal format example, or enforce API structured output mode. | Rewriting role/rules unrelated to formatting. |
| **`model limitation`** | Instruction is unambiguous and context is present, yet the target model consistently fails multi-step reasoning, strict counting, or long-context recall. | Decompose step, offload calculation/validation to code, or recommend model escalation/routing. | Piling on emphatic "CRITICAL! MUST!" prompt text. |
| **`bad test case`** | Output actually satisfies user intent, but the test case's pass/fail criteria or synthetic input is contradictory, unrealistic, or misaligned with the rubric. | Fix the test case or flag it `[REPLACE WITH REAL DATA]` — **do NOT edit the prompt** to overfit a broken test. | Bending the production prompt to satisfy a flawed test assertion. |
