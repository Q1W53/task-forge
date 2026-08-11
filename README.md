# TaskForge

**Grill → Contract → Confirm → Loop → Prove → Escalate**

TaskForge is a Codex skill for turning an ambiguous request into a confirmed Task Contract, executing it within explicit limits, and proving completion with checkable evidence.

TaskForge 是一个面向 Codex 的任务工程 skill：先追问真正影响结果的不确定性，再形成任务契约，经用户确认后有边界地循环执行，最后用证据而不是一句“完成了”交付结果。

## Why TaskForge

Most agent failures begin before execution: the goal is vague, “done” is subjective, permissions are implicit, or the loop has no exit. TaskForge joins requirements discovery and loop engineering into one workflow:

1. **GRILL** — clarify only material uncertainty.
2. **CONTRACT** — define scope, truth sources, acceptance, evidence, permissions, and limits.
3. **CONFIRM** — obtain explicit authority before consequential work.
4. **LOOP** — execute the smallest safe increment, verify, record, and correct.
5. **PROVE** — require evidence for every acceptance criterion.
6. **ESCALATE** — stop on risk, missing authority, exhausted budgets, or no progress.

## Install

Clone the repository, then copy the inner `task-forge` directory into your Codex skills directory.

### macOS / Linux

```bash
git clone https://github.com/Q1W53/task-forge.git
cp -R task-forge/task-forge "${CODEX_HOME:-$HOME/.codex}/skills/task-forge"
```

### Windows PowerShell

```powershell
git clone https://github.com/Q1W53/task-forge.git
Copy-Item -Recurse task-forge\task-forge "$env:USERPROFILE\.codex\skills\task-forge"
```

Restart Codex after installation if the skill does not appear immediately.

## Use

Invoke it explicitly:

```text
$task-forge Turn this rough idea into an executable plan and keep working until every acceptance criterion has evidence.
```

中文示例：

```text
$task-forge 把这个模糊需求整理成任务契约，确认后有边界地执行，并用证据证明完成。
```

TaskForge can also trigger implicitly for complex or autonomous tasks that lack clear acceptance criteria, permissions, budgets, stop rules, or escalation paths.

## What it produces

- an executable Task Contract;
- a permission and approval boundary;
- bounded iteration records;
- an acceptance-to-evidence matrix;
- a final `DONE`, `PARTIAL`, `NEEDS APPROVAL`, or `BLOCKED` state.

Templates live in [`task-forge/references`](task-forge/references).

## Safety model

TaskForge favors semi-autonomous execution. Reversible, in-scope work can proceed after contract confirmation. Publishing, sending, deleting, purchasing, production changes, and other irreversible or outward-facing actions require explicit authority. Limits are enforced by the control process, not trusted to the agent's self-report.

## Repository structure

```text
task-forge/
├── README.md
├── LICENSE
└── task-forge/
    ├── SKILL.md
    ├── agents/openai.yaml
    └── references/
```

## License

[MIT](LICENSE) © 2026 Q1W53
