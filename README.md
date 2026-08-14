# TaskForge

## Make AI agents prove they're done.

[![License: MIT](https://img.shields.io/badge/License-MIT-111827.svg)](LICENSE)
[![Codex Skill](https://img.shields.io/badge/Codex-Agent%20Skill-111827.svg)](task-forge/SKILL.md)

[中文说明](docs/README.zh-CN.md)

TaskForge is a verification-first Agent Skill for Codex. It turns an unclear request into an explicit task contract, waits for your confirmation, works inside the agreed boundary, and closes with checkable evidence.

No silent assumptions. No invisible contracts. No verifier gaming. No fake "done."

`GRILL → CONTRACT → CONFIRM → LOOP → PROVE / ESCALATE`

## See the difference

Suppose you ask an agent to refactor authentication and add GitHub login.

| Without TaskForge | With TaskForge |
| --- | --- |
| Starts editing immediately | Asks what must remain compatible |
| Guesses what "done" means | Maps acceptance criteria to evidence |
| May skip migrations or existing login paths | Records protected behavior and approval boundaries |
| Reports a summary | Reports test output, schema checks, and unresolved risks |

```text
Before

Agent: Done. I refactored authentication and added GitHub OAuth.

After

TaskForge: PROVE
✓ Existing password login: verifier passed
✓ GitHub callback flow: verifier passed
✓ Schema diff: no unapproved changes
✓ Acceptance criteria: 8/8 passed
```

The example above is illustrative, not a published benchmark result. See the full [authentication refactor walkthrough](examples/auth-refactor.md).

## Install

Ask Codex to install the skill from this repository:

```text
$skill-installer Install the task-forge skill from https://github.com/Q1W53/task-forge/tree/main/task-forge
```

Then start a task:

```text
$task-forge Help me refactor this authentication system. Ask what could change the result, show me the task contract, wait for confirmation, and prove every acceptance criterion before calling it done.
```

Codex detects skills in `$HOME/.agents/skills` and in a repository's `.agents/skills` directory. For a manual install, copy the inner [`task-forge/`](task-forge/) folder to one of those locations. Restart Codex if the skill doesn't appear. See OpenAI's [Build skills](https://developers.openai.com/plugins/build/skills) documentation for the current discovery rules.

## What happens next

### 1. GRILL

TaskForge restates the current state and asks only the questions that could change the goal, scope, authority, evidence, budget, or stopping rule. Material gaps keep the task in `AWAITING_INPUT`.

### 2. CONTRACT

It shows the execution boundary: outcome, non-goals, protected invariants, allowed actions, approval gates, acceptance criteria, evidence, and exits.

### 3. CONFIRM

You confirm the visible contract. Silence never grants permission, and an incomplete contract can't advance to execution.

### 4. LOOP

Each iteration takes the smallest safe action, runs the named verifier, records evidence, and checks retry and no-progress limits before continuing.

### 5. PROVE or ESCALATE

`PROVE` requires every criterion to pass with checkable evidence. When permission, input, budget, or trustworthy verification is missing, TaskForge stops with `NEEDS_APPROVAL`, `PARTIAL`, or `BLOCKED` instead of inventing success.

## LIGHT or DEEP

Both modes ask questions, show a contract, wait for confirmation, and finish with evidence. The difference is how much control and durable state the task needs.

| Mode | Use it for | What it adds |
| --- | --- | --- |
| `LIGHT` | One-session, low-risk, reversible work with a mostly clear outcome | A short interview, compact contract, and evidence matrix in chat |
| `DEEP` | Multi-step, ambiguous, long-running, external, costly, or hard-to-reverse work | Durable context, decisions, state, approvals, budgets, iteration logs, and completion evidence |

A DEEP run keeps its record under `.taskforge/<run-id>/`:

```text
context.md      confirmed facts and open questions
glossary.md     shared definitions
decisions.md    consequential choices and reasons
contract.md     confirmed execution boundary
state.json      machine-readable limits and criterion state
iterations.md   append-only actions and verifier results
completion.md   final evidence matrix and remaining risk
```

## Why TaskForge

Coding agents are good at producing changes, but a completion claim is still only a claim. TaskForge makes four failure modes visible:

- The request contains a business or technical ambiguity that would change the result.
- The agent acts beyond the authority the user intended to grant.
- A task keeps retrying without progress, spending time or tokens without a reliable exit.
- The agent weakens tests, skips checks, or treats implementation output as proof.

TaskForge keeps verifier code, protected tests, CI rules, and their configuration outside the execution loop's write authority. An agent can't pass by deleting the check.

## Good fits

Use TaskForge for migrations, release preparation, authentication changes, multi-file refactors, external-system writes, unattended work, business workflows, and any request where a wrong interpretation costs more than a short interview.

Skip it for a factual question or a tiny reversible edit whose expected result is already exact. TaskForge should add control where control matters, not ceremony to every prompt.

More prompts live in [`examples/`](examples/).

## Evals and benchmark method

The repository includes a behavior suite for stage gates, durable proof, approval boundaries, verifier protection, no-progress stopping, and a no-trigger control. Deterministic graders inspect files, state, and final responses.

No benchmark score is claimed in this README. Model results vary, and a useful comparison needs repeated trials, pinned model identifiers, recorded environment details, and published raw artifacts.

Read [`evals/README.md`](evals/README.md) for the suite layout, run method, reporting template, and contribution rules.

## Roadmap

- [x] LIGHT and DEEP modes
- [x] Hard stage gates and explicit confirmation
- [x] Durable DEEP state with language-aware templates
- [x] Deterministic behavior eval cases
- [ ] Publish repeatable multi-model baseline runs with raw artifacts
- [ ] Add more examples from real, permission-safe workflows
- [ ] Package TaskForge for easier plugin distribution
- [ ] Add CI checks for skill validation and Markdown links

Roadmap items describe intended work, not promised dates. See [`docs/ROADMAP.md`](docs/ROADMAP.md) for acceptance notes.

## Repository layout

```text
task-forge/
├── README.md                 product overview and quick start
├── docs/                     Chinese guide, roadmap, and launch copy
├── examples/                 copyable prompts and walkthroughs
├── evals/                    behavior suite and deterministic graders
└── task-forge/               installable Codex Skill
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/
    └── scripts/
```

## Contributing

Bug reports, sharper examples, failure cases, documentation fixes, and deterministic eval cases are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

If TaskForge helps you catch one false "done," [star the repository](https://github.com/Q1W53/task-forge) so other people can find it.

MIT licensed. See [LICENSE](LICENSE).
