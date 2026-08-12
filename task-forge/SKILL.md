---
name: task-forge
description: Turn ambiguous, consequential, or unattended work into a visible Task Contract, execute it through verified iterations, and close with checkable evidence. Use when the user explicitly says TaskForge; asks the agent to question assumptions before acting; requests work that must continue until a testable result; or gives work whose meaning, scope, acceptance tests, permissions, budgets, stop rules, or escalation path need clarification.
---

# TaskForge

Run six stages:

`GRILL -> CONTRACT -> CONFIRM -> LOOP -> PROVE | ESCALATE`

Never skip GRILL, hide the contract, or call work complete without evidence for every acceptance criterion. Ask proportionately: lightweight work receives a short interview; complex or risky work receives a deeper interview and durable controls.

### Hard stage gates

Keep exactly one active stage in each response. A later stage may be explained, but its artifact or action must not be produced early.

- If any unanswered question could materially change the goal, business meaning, scope, authority, acceptance evidence, verifier, budget, or stopping rule, remain in `GRILL` and end with `AWAITING_INPUT`.
- Do not present a confirmable Task Contract in the same response that asks unanswered material questions. A gap summary or draft notes may be shown, but label them `NOT READY` and do not ask for contract confirmation.
- Enter `CONTRACT` only after every material question is answered. Only genuinely non-blocking items may remain as `TBD` in a `READY WITH TBDs` contract.
- Enter `CONFIRM` only after the complete, visible contract is `READY` or `READY WITH TBDs`. `NOT READY` is a `GRILL` result, not a contract the user can confirm.
- Enter TaskForge's execution `LOOP` only after explicit confirmation. A loop or iteration node inside the requested product is part of the artifact design; it does not advance the TaskForge stage.

## 1. Select one of two modes

| Mode | Use | Required behavior and artifacts |
| --- | --- | --- |
| `LIGHT` | One-session, low-risk, reversible work with a mostly clear outcome | Ask a short batch of material questions. Show a compact contract and evidence matrix in chat. Wait for confirmation. Files are optional. |
| `DEEP` | Multi-step or consequential work; several acceptance criteria; ambiguous business meaning; cross-session, unattended, external, irreversible, regulated, or meaningful time/cost exposure | Conduct a structured interview. Create `.taskforge/<run-id>/` with `contract.md`, `state.json`, `iterations.md`, and `completion.md`. Use deterministic verification, explicit approvals, budgets, stop rules, and verifier protection when risk requires them. |

Default to `LIGHT` only when every item below is already substantially clear:

- current state and desired state;
- beneficiary and observable deliverable;
- scope, non-goals, and source precedence;
- acceptance criteria and evidence;
- authority and reversibility.

Choose `DEEP` when any item is materially unclear or when an incorrect interpretation would change a business decision, workflow, external system, protected artifact, cost, or deadline. Reversibility reduces operational risk but does not excuse semantic uncertainty. Upgrade from `LIGHT` to `DEEP` when new information increases ambiguity, scope, risk, duration, or verification burden; show the amendment and reconfirm it.

For `DEEP`, use:

```text
.taskforge/<run-id>/
  context.md
  glossary.md
  decisions.md
  contract.md
  state.json
  iterations.md
  completion.md
```

`DEEP` borrows the documentation discipline of `grill-with-docs`: put confirmed background and open questions in `context.md`, shared terms in `glossary.md`, and consequential choices with alternatives and rationale in `decisions.md`. Update these documents during GRILL before amending the execution contract. Do not mix unconfirmed assumptions with confirmed facts.

Choose the language of every user-facing TaskForge document from the user's primary language. A user-specified language overrides detection. Chinese-dominant requests use Chinese templates; English-dominant requests use English templates. For balanced bilingual input without an explicit preference, use the current conversation language and record the choice in `contract.md`. Keep filenames and machine-readable state keys stable in English.

Read [loop-control.md](references/loop-control.md) before creating durable state or starting an unattended loop. Use `scripts/init_run.py` and validate with `scripts/validate_run.py` before the first iteration and before declaring `DONE`.

## 2. GRILL: make misunderstanding visible

Start by stating:

1. what you believe the current state is;
2. what result you believe the user wants;
3. which assumptions could change the result.

Then ask questions whose answers affect the result, business meaning, scope, authority, verifier, evidence, or stopping behavior.

### LIGHT interview

- Ask one concise batch, normally 2–5 questions.
- Cover at least current state, desired outcome, and acceptance evidence.
- Recommend a default when a trade-off matters.
- Mark genuinely non-blocking unknowns `TBD`.
- If a material answer is missing, ask the questions and stop at `AWAITING_INPUT`; do not draft the compact contract yet.
- Do not begin state-changing work before showing the compact contract and receiving confirmation.

### DEEP interview

- Probe current and target state, beneficiary, business workflow, source precedence, scope/non-goals, edge cases, acceptance and evidence, permissions, reversibility, budgets, exits, and escalation.
- Batch independent questions in rounds; do not overwhelm the user with a long unprioritized questionnaire.
- Continue until the contract is `READY` or `READY WITH TBDs`. A material semantic gap makes it `NOT READY`.
- When readiness is `NOT READY`, update interview documents if useful, show the unresolved gap summary, and stop at `AWAITING_INPUT`. Do not advance to `CONTRACT` or `CONFIRM` in that response.
- High-risk or unattended work is not ready until success is independently checkable and controller limits are concrete.
- Persist confirmed context, terminology, and decisions as the interview progresses; show meaningful document changes before contract confirmation.

Questions are mandatory in both modes. If the user's message already answers a topic, verify it in the understood-state summary instead of asking it again.

## 3. CONTRACT: show the execution boundary

Use [task-contract.md](references/task-contract.md).

Every contract, including `LIGHT`, must be visible to the user before execution and contain:

1. observable outcome and beneficiary;
2. scope and non-goals;
3. current-state assumptions and source precedence;
4. constraints and protected invariants;
5. acceptance criteria mapped to evidence and named verifiers;
6. allowed actions, approval gates, and prohibited actions;
7. checkpoints and success/failure/escalation exits;
8. unresolved `TBD` items.

For `LIGHT`, present a compact chat contract with an acceptance/evidence table. For `DEEP`, create the durable files and show the user a concise contract summary plus file path. Set readiness to `READY`, `READY WITH TBDs`, or `NOT READY`.

## 4. CONFIRM: establish authority

Always ask the user to confirm or revise the visible contract before any state-changing execution. A request to use TaskForge is not itself confirmation of an unseen contract, and silence never grants authority.

After confirmation, treat the contract as the boundary. Pause for an amendment when new information changes the current state, outcome, business meaning, scope, verifier, risk, cost, protected paths, or permissions. Show the amendment and reconfirm only the changed boundary.

## 5. LOOP: execute bounded iterations

For each unmet criterion:

1. Read the confirmed contract and durable state when present.
2. Check approval, budget, retry, and no-progress exits.
3. Take the smallest safe action.
4. Run the criterion's verifier.
5. Record the action and evidence; in `LIGHT`, keep a concise in-context record, and in `DEEP`, append [iteration-log.md](references/iteration-log.md) and atomically update `state.json`.
6. Evaluate every exit before continuing.

Controller code, not the model, must enforce limits for unattended work. Keep verifier code, protected tests, CI rules, and their configuration outside execution-loop write authority. Reject attempts to weaken, bypass, delete, or hard-code verifiers.

Default limits when the contract omits stricter values:

- at most 3 failed attempts for one criterion;
- stop after 2 materially identical failures;
- stop after 2 consecutive iterations with the same state fingerprint;
- stop before any stated time, token, iteration, or monetary limit is crossed.

## 6. PROVE: close with visible evidence

Use [completion-report.md](references/completion-report.md). The final response must include an evidence matrix even in `LIGHT` mode.

`DONE` requires:

- every acceptance criterion is `PASS`;
- each pass names checkable evidence and its verifier;
- semantic/content checks and technical checks are separate when both matter;
- protected invariants and required approvals still hold;
- `scripts/validate_run.py` passes for a `DEEP` run.

Use `PARTIAL` when useful work exists but any criterion remains unmet. Never substitute technical validity for semantic correctness, and never reconstruct missing evidence from memory.

## 7. ESCALATE: stop safely

Return `NEEDS_APPROVAL` when the next action crosses an approval gate. Return `BLOCKED` when required input or authority is unavailable, sources conflict without precedence, a limit fires, progress stalls, verification cannot distinguish success from failure, or continuing raises unacceptable risk.

Name the trigger, completed work, evidence, exact missing condition, and smallest useful human decision.

## Output state

End a TaskForge cycle with exactly one state:

- `AWAITING_INPUT`
- `AWAITING_CONFIRMATION`
- `RUNNING`
- `DONE`
- `PARTIAL`
- `NEEDS_APPROVAL`
- `BLOCKED`
