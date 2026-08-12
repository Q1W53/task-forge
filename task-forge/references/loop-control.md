# Loop control and durable state

Read this file for `DEEP` runs that create durable state.

## Controller boundary

Keep the loop body small: observe one state, take one bounded action, verify it, persist the result, then evaluate exits. The controller must enforce limits before asking the model for another action. Do not rely on the model to stop itself.

Use one trigger pattern:

| Pattern | Wake-up condition | Required protection |
| --- | --- | --- |
| `manual` | A user starts each cycle | Contract and approval check |
| `goal` | Continue until a verified endpoint | Hard budgets and no-progress detection |
| `heartbeat` | Fixed interval | Idempotency and overlap lock |
| `cron` | Scheduled time | Prompt/version review date |
| `hook` | External event | Idempotency key, rate limit, queue, and backpressure |

## State contract

Store current machine state at `.taskforge/<run-id>/state.json`. A complete DEEP run also requires `context.md`, `glossary.md`, `decisions.md`, `contract.md`, `iterations.md`, and `completion.md`.

```json
{
  "schema_version": 1,
  "run_id": "example-run",
  "mode": "DEEP",
  "status": "RUNNING",
  "contract_sha256": "64 lowercase hexadecimal characters",
  "iteration": 0,
  "limits": {
    "max_iterations": 12,
    "max_failures_per_criterion": 3,
    "max_identical_fingerprints": 2,
    "wall_clock_seconds": 3600,
    "token_budget": null,
    "monetary_budget": null
  },
  "criteria": [
    {
      "id": "AC-1",
      "status": "PENDING",
      "verifier": "python -m pytest",
      "evidence": [],
      "failure_count": 0
    }
  ],
  "fingerprints": [],
  "verifier_protection": {
    "method": "read-only paths plus diff rejection",
    "paths": ["tests", ".github/workflows"],
    "baseline_sha256": ""
  },
  "approvals": [],
  "updated_at": "2026-08-11T00:00:00Z"
}
```

Allowed status values are `AWAITING_CONFIRMATION`, `RUNNING`, `DONE`, `PARTIAL`, `NEEDS_APPROVAL`, and `BLOCKED`. Criterion status values are `PENDING`, `PASS`, and `FAIL`.

Build a fingerprint from facts that show real progress, such as artifact hashes, failing-test identifiers, open-criterion IDs, and external resource versions. Do not use timestamps, iteration counters, random IDs, or prose summaries; they change even when the work does not.

Write state atomically: create a sibling temporary file, flush it, then replace `state.json`. Keep `iterations.md` append-only. If state and log disagree, stop and reconcile from checkable artifacts rather than guessing.

## Exit order

Evaluate exits in this order before and after every action:

1. approval or risk boundary;
2. hard budget or wall-clock limit;
3. retry limit;
4. no-progress threshold;
5. deterministic success;
6. otherwise continue.

A `DONE` state is invalid if any criterion lacks evidence, a required approval is missing, or protected verifier material changed without a confirmed amendment.
