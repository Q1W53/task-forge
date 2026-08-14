# Authentication refactor walkthrough

This hypothetical example shows the behavior TaskForge is designed to produce. It isn't a transcript from a benchmark run.

## The request

```text
Refactor authentication and add GitHub login.
```

An agent can interpret that sentence in several incompatible ways. It doesn't say which login flows must survive, whether database changes are allowed, who can create OAuth credentials, or what proves the rollout is safe.

## GRILL

TaskForge stays in `AWAITING_INPUT` and asks questions that can change the implementation:

```text
1. Which existing login methods and session formats must remain compatible?
2. May the task change the database schema or add environment variables?
3. Who owns the GitHub OAuth app and secret provisioning?
4. What evidence must pass before rollout, and who approves production changes?
```

It doesn't present a confirmable contract in the same response because the material answers are still missing.

## CONTRACT

After the user answers, TaskForge maps each requirement to evidence:

| Criterion | Evidence | Verifier |
| --- | --- | --- |
| Password login still works | Existing login integration test passes | Test runner outside the edit boundary |
| GitHub callback handles success and denial | Callback integration tests pass | Protected OAuth test suite |
| No unapproved schema change | Empty schema diff | Migration diff command |
| Secrets remain outside source control | Secret scan has no findings | Repository secret scanner |
| Rollback remains possible | Previous login route can be restored | Staging rollback rehearsal |

The contract also records non-goals, allowed files, approval gates, retry limits, and a stop rule. The user must confirm it before execution.

## LOOP

Each iteration targets one unmet criterion. TaskForge changes the smallest relevant surface, runs the named verifier, records the result, and checks whether another attempt is allowed.

A failing verifier doesn't become a pass because the implementation looks plausible. Protected tests and their configuration remain outside the loop's write authority.

## PROVE

The completion report contains the evidence matrix, approvals, protected-invariant checks, and remaining risk. If the OAuth credentials or production approval never arrive, TaskForge stops at `NEEDS_APPROVAL` or `PARTIAL`; it doesn't rename preparation as completion.
