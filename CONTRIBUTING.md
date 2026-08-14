# Contributing to TaskForge

TaskForge accepts documentation fixes, reproducible bug reports, realistic examples, deterministic eval cases, and behavior changes with evidence.

## Before you open a pull request

1. Explain the failure or user need with a concrete prompt.
2. Keep the installable Skill under `task-forge/`; public project documentation belongs at the repository root, in `docs/`, `examples/`, or `evals/`.
3. Don't weaken stage gates, approval boundaries, retry limits, or verifier protection to make a case pass.
4. Add or update deterministic checks when behavior changes.
5. Run the local checks below and report what you actually ran.

## Local checks

TaskForge's runtime validator uses only the Python standard library:

```bash
python task-forge/scripts/validate_run.py --self-test
```

If you have the OpenAI skill-creator tools available, validate the installable folder too:

```bash
python /path/to/skill-creator/scripts/quick_validate.py task-forge
```

Behavior evals require Docker, skill-optimizer, and an OpenRouter key. See [`evals/README.md`](evals/README.md); contributors don't need to run paid model evals for a documentation-only change.

## Eval case rules

- Write the task as a user would ask it. Don't mention hidden graders or expected internal actions.
- Keep setup and graders deterministic whenever files, state, or command output can decide the result.
- Put protected tests and verifier configuration outside the Agent's writable boundary.
- Include the reproduction environment and raw artifacts with any benchmark claim.

## Pull request description

State what changed, why it matters, which behavior or documents it affects, and the exact checks run. If a check wasn't run, say so. Screenshots and copied terminal summaries help when the change affects rendered Markdown or installation steps.

By contributing, you agree that your contribution can be distributed under this repository's [MIT License](LICENSE).
