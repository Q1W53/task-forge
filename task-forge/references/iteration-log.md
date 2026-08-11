# Iteration log template

Append one block after each attempted state change. Never rewrite earlier blocks.

## Iteration N

- Started from contract SHA-256:
- Target criterion:
- Pre-action exit checks:
- Intended state change:
- Action taken:
- Files or systems changed:
- Verification command or method:
- Result: `PASS` or `FAIL`
- Evidence:
- Protected verifier and invariant checks:
- State fingerprint:
- Remaining gap:
- Iteration, time, token, and cost consumed / remaining:
- Next decision: `CONTINUE`, `DONE`, `NEEDS_APPROVAL`, or `BLOCKED`

Compare the fingerprint with recent entries. Stop when the contract's no-progress threshold is reached.
