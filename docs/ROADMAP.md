# TaskForge roadmap

The roadmap tracks observable behavior, not release dates. An item moves to complete only when its acceptance notes are satisfied.

## Available now

- `LIGHT` and `DEEP` select the amount of interview and durable control a task needs.
- Hard stage gates prevent execution before a complete, visible contract is confirmed.
- DEEP runs keep context, definitions, decisions, state, iterations, and completion evidence.
- English and Chinese templates follow the user's working language.
- Deterministic eval cases cover stage gates, approvals, protected verifiers, durable proof, and no-progress stopping.

## Next

### Publish a repeatable baseline

Run the existing suite across pinned model identifiers with multiple trials. Publish raw runner artifacts, environment details, per-case results, and failures. No aggregate score should appear without those materials.

### Expand real-work examples

Add permission-safe examples for migrations, document production, release preparation, and external-system writes. Each example must identify its source of truth, approval boundary, verifier, and expected terminal state.

### Package for distribution

Evaluate a Codex plugin package so users can install TaskForge through a maintained distribution path. The direct Skill folder remains the authoring source until that package exists.

### Add repository checks

Run skill validation, Python self-tests, Markdown link checks, and eval schema checks in CI. Verifier configuration must stay outside the Agent execution loop's write boundary during evals.

## Later candidates

- A small library of reusable acceptance-criterion patterns.
- More controller examples for heartbeat, cron, and hook-triggered work.
- Report adapters that turn `completion.md` into a PR or issue summary without changing evidence.
- Cross-agent compatibility notes, tested separately from Codex behavior.

Open an issue before implementing a large roadmap item so its acceptance evidence can be agreed first.
