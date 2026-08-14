# TaskForge behavior evals

This directory tests observable TaskForge behavior with deterministic graders. It doesn't treat a persuasive final answer as proof.

## What the suite checks

The current [`suite.yml`](suite.yml) covers:

- a routine question that should not create TaskForge artifacts;
- a small reversible edit;
- material questions that must remain in `GRILL`;
- a DEEP run with durable proof;
- attempts to game protected verifiers;
- an action that must stop at an approval boundary;
- repeated no-progress state that must end safely.

Graders inspect final text, changed files, protected inputs, and `.taskforge` state. They run after the agent and remain outside its writable workspace.

## Run the suite

The suite uses the [skill-optimizer](https://github.com/fastxyz/skill-optimizer) workbench, Docker, and an OpenRouter model reference. A real run requires `OPENROUTER_API_KEY`.

From a local skill-optimizer checkout:

```bash
npm install
npm run build
npx tsx src/cli.ts run-suite /path/to/task-forge/evals/suite.yml --trials 3
```

The suite's `references: ..` setting copies this repository into the isolated `/work` directory. Pin the model entries in `suite.yml` before publishing results.

## Reporting a baseline

Don't report a single aggregate number without the material needed to reproduce it. A baseline report should include:

| Field | Required detail |
| --- | --- |
| Repository | TaskForge commit SHA and dirty/clean state |
| Runner | skill-optimizer commit or release |
| Models | Exact OpenRouter model identifiers |
| Trials | Trial count per case and model |
| Environment | Date, Docker version, operating system, timeout |
| Results | Per-case passes, failures, and grader evidence |
| Artifacts | `suite-result.json`, failed `result.json`, `summary.json`, and relevant traces |
| Cost | Token or monetary totals when the runner records them |

Store published artifacts under a dated, commit-addressed location such as `evals/results/<date>-<short-sha>/`. Remove secrets and personal data from traces before publishing them.

## Comparing changes

Use the same models, trial count, runner commit, and environment for both sides. Compare a pinned baseline commit with the candidate commit. Report per-case changes, not only the mean, because a skill can improve task completion while regressing an approval boundary.

Useful signals include pass rate by case, false `DONE` rate, approval-boundary violations, protected-verifier modifications, no-progress exit correctness, and the share of runs with valid durable state.

## Adding a case

A new case should look like a real user request and have a local deterministic grader. Keep hidden answers and grader internals outside `/work`. Add failure cases that test a specific boundary; avoid an LLM judge unless the behavior can't be checked from files, state, commands, or final text.

Benchmark results are welcome in pull requests when the raw artifacts and reproduction details accompany the summary.
