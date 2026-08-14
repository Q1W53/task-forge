# TaskForge launch kit

Use these drafts after the README changes are merged. Replace bracketed fields with real links or results; don't remove the qualifiers around hypothetical examples or unrun benchmarks.

## GitHub description

Recommended:

```text
Make AI agents prove they're done. A verification-first Codex Skill with task contracts, bounded execution, and evidence-backed delivery.
```

Short alternative:

```text
Verification-first task contracts and evidence for AI coding agents.
```

## GitHub topics

Use topics that describe the actual project and match likely search terms:

```text
codex
codex-skill
agent-skill
ai-agents
coding-agents
agentic-workflow
verification
task-management
acceptance-criteria
developer-tools
```

Don't add unrelated high-volume topics. Search traffic that leaves immediately doesn't help the project.

## Suggested social post

```text
Coding agents are quick to say “done.” TaskForge makes them show their work.

It turns an unclear request into a confirmed task contract, keeps execution inside agreed limits, and requires evidence for every acceptance criterion. If approval, input, or a trustworthy verifier is missing, it stops instead of guessing.

TaskForge is an open-source Codex Skill with LIGHT and DEEP modes, durable run state, verifier protection, and deterministic behavior evals.

[REPOSITORY URL]
```

## Suggested launch post for developer communities

```text
I built TaskForge because “the agent changed the files” and “the task is complete” aren't the same statement.

TaskForge adds a small control layer around Codex tasks:

GRILL → CONTRACT → CONFIRM → LOOP → PROVE / ESCALATE

It asks questions that can change the result, shows the execution boundary before writing, and maps completion claims to named evidence. LIGHT mode keeps this compact for reversible work; DEEP mode adds durable context, decisions, budgets, approvals, iteration logs, and stopping rules.

The repository includes deterministic behavior eval cases. I haven't published a benchmark score yet because I want the first baseline to include repeated trials and raw artifacts.

Feedback on the stage gates, examples, and eval method is welcome: [REPOSITORY URL]
```

## Search snippets

Primary title:

```text
TaskForge: Verification-first execution for AI coding agents
```

One-line pitch:

```text
Turn vague agent requests into confirmed contracts, bounded work, and checkable proof.
```

## Release checklist

- Render the README on GitHub and inspect the first screen on desktop and mobile.
- Run the local Skill and validator checks.
- Confirm every installation command against a clean Codex setup.
- Update the GitHub description and topics.
- Publish one post first, answer real questions, then adapt later posts from the language users actually use.
- Add benchmark numbers only after raw artifacts and reproduction details are public.
