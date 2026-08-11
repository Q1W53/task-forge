---
name: task-forge
description: Turn ambiguous, consequential, or unattended work into a bounded Task Contract, execute it through verified iterations, and close with checkable evidence. Use when the user explicitly says TaskForge; asks an agent to keep working until a testable result; requests a long-running, self-directed, or cross-session workflow; or gives consequential work whose scope, source of truth, acceptance tests, permissions, budgets, stop rules, or escalation path remain unclear. Do not invoke implicitly for routine questions, explanations, or small reversible edits that already have a clear outcome and authorization.
---

# TaskForge

Run six stages:

`GRILL -> CONTRACT -> CONFIRM -> LOOP -> PROVE | ESCALATE`

Choose the lightest rigor that keeps the work safe. Ask only questions whose answers can change the result, authority, verifier, or stopping behavior. Never call work complete without evidence for every acceptance criterion.

## 1. Select rigor

Choose before drafting a contract:

| Mode | Use | Required artifacts |
| --- | --- | --- |
| `LITE` | One-session, low-risk, reversible work with a clear outcome | No TaskForge files. Keep a compact contract in working context and use the user's request as authorization. |
| `STANDARD` | Multi-step work, material writes, several acceptance criteria, or work likely to cross a context reset | Create a run directory and the four durable files below. |
| `STRICT` | Unattended loops, external or irreversible actions, production changes, regulated work, or meaningful time/cost exposure | Use durable files, a deterministic verifier, controller-enforced budgets, verifier protection, and explicit approval gates. |

Do not inflate `LITE` work into a ceremony. Upgrade the mode when new information raises risk, duration, cost, or uncertainty. Record the upgrade as a contract amendment.

For `STANDARD` and `STRICT`, use `.taskforge/<run-id>/`:

```text
contract.md      confirmed agreement and amendments
state.json       machine-readable current state and controller limits
iterations.md    append-only action and verification record
completion.md    final evidence report
```

Read [loop-control.md](references/loop-control.md) before starting an unattended loop or creating `state.json`. Use `scripts/init_run.py` to create the directory when scripts can run. Validate it with `scripts/validate_run.py` before the first iteration and before declaring `DONE`.

## 2. GRILL: resolve material uncertainty

State the understood outcome, inspect available context, then probe only gaps that affect:

- the observable result and beneficiary;
- scope, non-goals, inputs, and source precedence;
- acceptance criteria, evidence, and verifier;
- authority, reversibility, budgets, exits, and escalation.

Batch independent questions. Recommend one answer with a reason and offer at most two alternatives when the trade-off matters. Wait only for answers that block the safe next step. Mark non-blocking unknowns `TBD`.

Skip the interview when the request is executable. Expose assumptions in the contract instead.

## 3. CONTRACT: define execution

Use [task-contract.md](references/task-contract.md). Every contract must contain:

1. an observable outcome;
2. scope and non-goals;
3. source-of-truth precedence;
4. constraints and protected invariants;
5. acceptance criteria mapped to evidence and named verifiers;
6. allowed actions, approval gates, and prohibited actions;
7. trigger, observation, smallest action, and checkpoints;
8. success, failure, budget, no-progress, and escalation exits;
9. assumptions and unresolved `TBD` items.

Set readiness to `READY`, `READY WITH TBDs`, or `NOT READY`. A `STRICT` contract is not ready until its success endpoint can be checked independently and its controller limits have concrete values.

## 4. CONFIRM: establish authority

Ask the user to confirm or revise the contract unless the current request already grants the exact authority needed for the next action. Silence never grants authority.

After confirmation, treat the contract as the boundary. Pause for an amendment when new information changes the outcome, scope, verifier, risk, cost, protected paths, or permissions. Do not repeat an approval already granted for the same action and scope.

## 5. LOOP: execute bounded iterations

Each cycle must start from durable state, not remembered chat history:

1. Re-read `contract.md` and `state.json` when they exist.
2. Check approval, budget, retry, and no-progress exits before acting.
3. Select one smallest safe action for one unmet criterion.
4. Execute inside the confirmed boundary.
5. Run the criterion's verifier.
6. Record the action and evidence with [iteration-log.md](references/iteration-log.md).
7. Update `state.json` atomically, including the state fingerprint.
8. Evaluate every exit before another cycle.

Controller code, not the model, must enforce iteration, time, token, monetary, rate, and no-progress limits for unattended work. Hook-driven loops also need idempotency, rate limiting, and backpressure.

Keep verifier code, protected tests, CI rules, and their configuration outside the execution loop's write authority. Reject changes that delete checks, lower coverage, skip failures, add `continue-on-error`, hard-code expected output, or otherwise make a weak result appear valid.

Default limits apply only when the contract omits stricter values:

- at most 3 failed attempts for one criterion;
- stop after 2 materially identical failures;
- stop after 2 consecutive iterations with the same state fingerprint;
- stop before any stated time, token, iteration, or monetary limit is crossed.

Trim tool output before it enters context. For long runs, store counts and status in `state.json`, decisions in `iterations.md`, and retrieve source material only when needed.

## 6. PROVE: close with evidence

Use [completion-report.md](references/completion-report.md). `DONE` requires:

- every acceptance criterion is `PASS`;
- every pass links to checkable evidence and its verifier;
- protected invariants and verifier fingerprints still match;
- required approvals exist;
- `scripts/validate_run.py` passes for a durable run.

Use `PARTIAL` when useful work exists but any criterion remains unmet. Never reconstruct missing evidence from memory.

## 7. ESCALATE: stop safely

Return `NEEDS_APPROVAL` when the next action crosses an approval gate. Return `BLOCKED` when an input or authority is unavailable, sources conflict without precedence, a limit fires, progress stalls, verification cannot distinguish success from failure, or continuing raises unacceptable security, privacy, legal, financial, reputational, or irreversible risk.

Name the trigger, completed work, collected evidence, exact missing condition, and smallest useful human decision.

## Output state

End a TaskForge cycle with one state only:

- `AWAITING_CONFIRMATION`
- `RUNNING`
- `DONE`
- `PARTIAL`
- `NEEDS_APPROVAL`
- `BLOCKED`
