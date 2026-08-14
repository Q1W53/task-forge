# TaskForge examples

These examples show where verification-first execution earns its keep. Copy a prompt, replace the project details, and let TaskForge interview you before it writes.

## Refactor with compatibility requirements

```text
$task-forge Use DEEP mode to refactor our authentication module and add GitHub login. Existing password login and session cookies must keep working. Ask me for missing compatibility, rollout, rollback, and acceptance details; show the contract before changing code.
```

See [`auth-refactor.md`](auth-refactor.md) for an illustrative Before/After walkthrough.

## Release preparation with an approval boundary

```text
$task-forge Prepare version 2.4.0 for release. You may update the changelog, build artifacts, and run release checks. Publishing, tagging, and registry writes require my separate approval. Stop with NEEDS_APPROVAL when the package is ready.
```

## Data cleanup with a protected verifier

```text
$task-forge Use DEEP mode to normalize customers.csv according to SPEC.md. Treat tests/ and validate_customers.py as read-only. Keep a durable run record, stop after two identical state fingerprints, and report evidence for every acceptance criterion.
```

## Small reversible task

```text
$task-forge Use LIGHT mode to rename the Settings heading to Preferences. Confirm the exact file and expected text, show a compact contract, make only that change, and include the diff as evidence.
```

Examples are prompts and hypothetical transcripts. They are not performance claims.
