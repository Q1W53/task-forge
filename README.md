# TaskForge｜任务锻造

**Grill → Contract → Confirm → Loop → Prove → Escalate**<br>
**问清楚 → 写成契约 → 确认授权 → 循环执行 → 证据验收 → 升级人工**

TaskForge is a Codex skill that turns ambiguous requests into confirmed Task Contracts, executes them within explicit boundaries, and proves completion with checkable evidence.

TaskForge（任务锻造）是一个面向 Codex 的任务工程 Skill：它把模糊需求整理成经用户确认的任务契约，在明确边界内执行，并用可检查的证据证明任务完成。

## Why TaskForge｜为什么需要 TaskForge

Most agent failures begin before execution: the goal is vague, “done” is subjective, permissions are implicit, or the loop has no exit. TaskForge combines requirements discovery and loop engineering into one end-to-end workflow.

许多 Agent 任务在执行前就已经埋下失败原因：目标模糊、“完成”依赖主观判断、权限边界没有写明，或者循环根本没有出口。TaskForge 把需求澄清与循环工程合并成一条端到端工作流。

| Stage | English | 中文 |
| --- | --- | --- |
| **GRILL** | Clarify only uncertainties that materially affect the outcome. | 只追问真正影响结果的关键不确定性。 |
| **CONTRACT** | Define scope, sources of truth, acceptance criteria, evidence, permissions, and limits. | 写清范围、真相源、验收标准、证据、权限与执行限制。 |
| **CONFIRM** | Obtain explicit authority before consequential work. | 在执行重要操作前获得用户明确确认。 |
| **LOOP** | Execute the smallest safe increment, verify it, record evidence, and correct failures. | 按最小安全单元执行、验证、留证，并定向修正失败项。 |
| **PROVE** | Require checkable evidence for every acceptance criterion. | 每一项验收条件都必须有可检查的证据。 |
| **ESCALATE** | Stop on risk, missing authority, exhausted budgets, or no progress. | 遇到风险、权限不足、预算耗尽或无进展时停止并升级人工。 |

## Install｜安装

Clone this repository, then copy the inner `task-forge` directory into your Codex skills directory.

克隆本仓库，然后把内层的 `task-forge` 目录复制到 Codex 的 skills 目录中。

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

Restart Codex if the skill does not appear immediately after installation.

如果安装后没有立即看到该 Skill，请重启 Codex。

## Use｜使用

Invoke TaskForge explicitly with an English request:

使用英文请求显式调用 TaskForge：

```text
$task-forge Turn this rough idea into an executable Task Contract, confirm it with me, then keep working within clear limits until every acceptance criterion has evidence.
```

Invoke TaskForge explicitly with a Chinese request:

使用中文请求显式调用 TaskForge：

```text
$task-forge 把这个模糊需求整理成可执行的任务契约，和我确认后在明确边界内持续执行，直到每项验收条件都有证据。
```

TaskForge can also trigger implicitly for complex or autonomous tasks that lack clear acceptance criteria, permissions, budgets, stop rules, or escalation paths.

对于缺少明确验收标准、权限、预算、停止条件或升级路径的复杂任务与自主任务，TaskForge 也可以被隐式触发。

## What it produces｜交付内容

TaskForge produces:

TaskForge 会交付：

- an executable Task Contract｜一份可执行的任务契约；
- a permission and approval boundary｜明确的权限与审批边界；
- bounded iteration records｜有边界的循环执行记录；
- an acceptance-to-evidence matrix｜验收条件与证据的对应矩阵；
- a final `DONE`, `PARTIAL`, `NEEDS APPROVAL`, or `BLOCKED` state｜最终状态：`DONE`、`PARTIAL`、`NEEDS APPROVAL` 或 `BLOCKED`。

Reusable templates live in [`task-forge/references`](task-forge/references).

可复用模板位于 [`task-forge/references`](task-forge/references)。

## Safety model｜安全模型

TaskForge favors semi-autonomous execution. Reversible, in-scope work may proceed after contract confirmation. Publishing, sending, deleting, purchasing, production changes, and other irreversible or outward-facing actions require explicit authority. Limits are enforced by the control process rather than trusted to the agent's self-report.

TaskForge 倾向于半自主执行。任务契约确认后，可逆且在范围内的工作可以继续；发布、发送、删除、购买、生产环境变更以及其他不可逆或对外操作必须获得明确授权。执行限制由控制流程强制执行，而不是依赖 Agent 自我声明。

## Repository structure｜仓库结构

```text
task-forge/
├── README.md
├── LICENSE
└── task-forge/
    ├── SKILL.md
    ├── agents/openai.yaml
    └── references/
```

The repository root contains public documentation and the license. The inner `task-forge` directory is the installable Codex skill.

仓库根目录存放公开说明和许可证；内层 `task-forge` 目录是可直接安装的 Codex Skill。

## License｜开源协议

Released under the [MIT License](LICENSE). You may use, modify, distribute, and use TaskForge commercially as long as the copyright and license notice are retained.

本项目采用 [MIT License](LICENSE) 开源。任何人都可以使用、修改、分发或用于商业项目，但需要保留原版权声明和许可证文本。

© 2026 Q1W53
