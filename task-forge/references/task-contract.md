# Task Contract template

## 1. Identity and rigor

- Run ID:
- Mode: `LIGHT` or `DEEP`
- Owner:
- Readiness: `READY`, `READY WITH TBDs`, or `NOT READY`

`NOT READY` means the task remains in `GRILL`. Do not ask the user to confirm this contract. Resolve every material question first; only non-blocking `TBD` items may remain when readiness advances.

## 2. Goal and observable outcome

- Current state:
- Objective:
- Beneficiary:
- Observable outcome:

## 3. Scope and non-goals

- In scope:
- Out of scope:

## 4. Inputs and source of truth

- Required inputs:
- Trusted sources, in priority order:
- Conflict-resolution rule:

## 5. Constraints and protected invariants

- Deadline and budgets:
- Format or technology:
- Security, privacy, legal, or policy constraints:
- Protected files, tests, verifier configuration, and other invariants:

## 6. Acceptance and evidence

| ID | Observable pass/fail criterion | Required evidence | Independent verifier |
| --- | --- | --- | --- |
| AC-1 |  |  |  |

## 7. Permissions and approval gates

- Allowed without another approval:
- Requires approval:
- Prohibited:
- Rollback or recovery requirement:

## 8. Loop control

For `LIGHT`, complete only the fields relevant to the bounded manual task. For `DEEP`, complete every applicable field; unattended or high-risk work requires concrete controller limits.

- Trigger pattern: `goal`, `heartbeat`, `cron`, `hook`, or `manual`
- Observation checked each cycle:
- Smallest action per cycle:
- Success exit:
- Failure exit:
- Maximum iterations:
- Maximum failures for one criterion:
- Wall-clock, token, and monetary limits:
- No-progress fingerprint and threshold:
- Rate limit, backpressure, and idempotency rule when event-driven:
- Escalation target and notification path:

## 9. Execution checkpoints

1. First safe action:
2. Per-iteration verification:
3. Terminal verification:

## 10. Assumptions and open questions

- Confirmed assumptions:
- Unresolved `TBD` items:
- Reason for readiness status:

## 11. Confirmation and amendments

- Confirmed by:
- Confirmation evidence and time:
- Amendments:
