---
name: task-forge
description: Turn ambiguous or consequential requests into confirmed, executable Task Contracts, then run bounded execution loops and prove completion with checkable evidence. Use when a user says TaskForge, asks to combine requirements discovery with autonomous execution, wants an agent to keep working until a verifiable outcome, or provides a complex task without clear scope, sources of truth, acceptance criteria, permissions, budgets, stop conditions, or escalation paths.
---

# TaskForge

Forge a request through six stages:

`GRILL -> CONTRACT -> CONFIRM -> LOOP -> PROVE | ESCALATE`

Ask only what can materially change the outcome. Convert the answers into a Task Contract. Obtain confirmation before consequential execution. Work in bounded, verifiable increments. Declare completion only when every acceptance criterion has evidence.

## Operating rules

- Match rigor to impact. Keep low-risk, well-specified tasks lightweight.
- Batch independent questions and recommend a default for each.
- Never invent missing requirements. Mark unresolved items `TBD`.
- Treat read-only discovery as safe unless the user restricts it.
- Require confirmation before writes, publication, external communication, purchases, deletion, production changes, or other consequential actions not already authorized.
- Make each acceptance criterion observable and name its verifier.
- Prefer deterministic checks over the agent's own judgment.
- Keep the verifier, its configuration, and protected tests outside the execution loop's authority.
- Record evidence as work proceeds; do not reconstruct it from memory at the end.
- Stop on success, limits, no progress, risk, or an approval boundary.

## 1. GRILL: resolve material uncertainty

Start with a concise statement of the understood outcome. Inspect available context before asking questions.

Probe only relevant gaps:

- outcome and beneficiary;
- scope and explicit non-goals;
- inputs and source-of-truth precedence;
- constraints, deadline, budget, and required format;
- acceptance criteria, evidence, and verifier;
- permissions, approval gates, and reversibility;
- retry, stop, failure, and escalation conditions.

Ask independent questions in one batch. For each question provide one recommended answer with a short reason and up to two alternatives with trade-offs. Wait for the reply before asking a dependent batch.

Skip the interview when the request is already executable. Draft the contract directly and expose any assumptions.

## 2. CONTRACT: write the executable agreement

Use [task-contract.md](references/task-contract.md). Ensure the contract includes:

1. an observable outcome;
2. in-scope work and non-goals;
3. required inputs and source-of-truth rules;
4. constraints and invariants;
5. acceptance criteria mapped to evidence and verifiers;
6. allowed actions, approval gates, and prohibited actions;
7. execution checkpoints;
8. concrete budgets, stop rules, and escalation triggers;
9. assumptions and unresolved `TBD` items.

Set readiness to:

- `READY` when execution can start after confirmation;
- `READY WITH TBDs` when remaining unknowns do not block the safe next step;
- `NOT READY` when a material ambiguity or missing authority blocks execution.

## 3. CONFIRM: establish authority

Ask the user to confirm or revise the Task Contract. Do not treat silence as approval.

After confirmation, regard the contract as the execution boundary. If new information materially changes outcome, scope, risk, cost, or permissions, pause and propose a contract amendment.

## 4. LOOP: execute in bounded increments

For each iteration:

1. Re-read the Task Contract and durable state.
2. Select the smallest safe unit that advances an unmet criterion.
3. Execute only within granted permissions.
4. Run the specified verifier.
5. Record the action, result, evidence, changed state, and remaining gap using [iteration-log.md](references/iteration-log.md).
6. Preserve passed work and target only unmet criteria.
7. Evaluate every exit before continuing.

For long-running work, keep a compact state file in the workspace. Reconstruct each iteration from that file and current artifacts instead of relying on conversation memory.

Default limits when the contract does not specify stricter ones:

- maximum 3 iterations for the same failed criterion;
- stop after 2 materially identical failures;
- stop when two consecutive iterations produce no measurable state change;
- stop before exceeding any stated time, token, or monetary budget.

Do not weaken tests, remove checks, alter verifier configuration, reduce coverage, or hard-code expected output merely to obtain a passing result. Treat such changes as an approval-gated contract amendment.

## 5. PROVE: close with evidence

Completion requires all of the following:

- every acceptance criterion is `PASS`;
- each pass links to checkable evidence;
- protected invariants still hold;
- no unresolved blocker is disguised as success;
- consequential actions have the required approvals.

Use [completion-report.md](references/completion-report.md). Report the outcome first, then the evidence matrix, important changes, residual risks, and any follow-up.

Use `DONE` only for verified completion. Use `PARTIAL` when useful work exists but one or more criteria remain unmet.

## 6. ESCALATE: stop safely

Stop and return `NEEDS APPROVAL` when the next action crosses a permission gate.

Stop and return `BLOCKED` when any of these applies:

- a required input or authority is unavailable;
- sources of truth conflict and no precedence rule resolves them;
- the retry, time, token, cost, or iteration limit is reached;
- no-progress detection fires;
- verification cannot distinguish success from failure;
- continuing could create security, privacy, legal, compliance, financial, reputational, or irreversible risk.

State the trigger, work completed, evidence collected, exact missing condition, and smallest useful human decision. Never silently continue after escalation.

## Output states

End each TaskForge cycle with exactly one state:

- `AWAITING_CONFIRMATION`: contract is ready but not approved;
- `RUNNING`: bounded work remains and continuation is authorized;
- `DONE`: every criterion passed with evidence;
- `PARTIAL`: useful output exists but completion is not proven;
- `NEEDS_APPROVAL`: an authorization gate must be crossed;
- `BLOCKED`: progress cannot continue safely under the contract.
