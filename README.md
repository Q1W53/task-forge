# TaskForge｜任务锻造

`GRILL -> CONTRACT -> CONFIRM -> LOOP -> PROVE | ESCALATE`

TaskForge is a Codex skill for work that is ambiguous, consequential, unattended, or difficult to verify. It turns the request into an executable agreement, runs bounded iterations, and accepts completion only when every criterion has checkable evidence.

TaskForge（任务锻造）是一个面向 Codex 的任务工程 Skill，适合处理目标模糊、影响较大、需要持续运行或难以验收的工作。它先把请求整理成可执行协议，再按有限循环推进；只有每项标准都有可检查证据时，才允许宣布完成。

## Why it exists｜为什么需要它

Agent failures often begin before execution: “done” has no objective meaning, the source of truth is unclear, authority is assumed, or the loop has no hard exit. TaskForge puts those decisions into a Task Contract before expensive work begins.

许多 Agent 任务在执行前就已经埋下问题：“完成”没有客观定义、真相源不明确、权限靠猜测，或者循环没有硬性出口。TaskForge 会在高成本执行开始前，把这些决定写入任务契约。

It also protects small tasks from process overhead. A one-session reversible edit stays light; a production loop receives durable state, controller limits, verifier protection, and approval gates.

它也避免用重流程拖慢小任务。单次会话内的可逆编辑走轻量路径；生产级循环则必须具备持久状态、控制器限制、验证器保护和审批门槛。

## Three rigor modes｜三级严格度

| Mode | English | 中文 |
| --- | --- | --- |
| `LITE` | Clear, low-risk, reversible work. No TaskForge files. | 目标清楚、低风险且可逆；不创建 TaskForge 文件。 |
| `STANDARD` | Multi-step work or material writes. Persist contract, state, iterations, and completion evidence. | 多步骤任务或实质性写入；持久保存契约、状态、迭代和完成证据。 |
| `STRICT` | Unattended, external, irreversible, production, regulated, or costly work. Controller-enforced limits and protected verifiers are mandatory. | 无人值守、对外、不可逆、生产、受监管或成本较高的工作；必须由控制器强制限制并保护验证器。 |

## Six stages｜六个阶段

| Stage | English | 中文 |
| --- | --- | --- |
| `GRILL` | Ask only questions that can change the result, authority, verifier, or stopping behavior. | 只追问会改变结果、权限、验证方式或停止行为的问题。 |
| `CONTRACT` | Define scope, source precedence, acceptance criteria, evidence, permissions, budgets, and exits. | 写清范围、真相源优先级、验收标准、证据、权限、预算和出口。 |
| `CONFIRM` | Obtain authority for the actual action and scope; never treat silence as approval. | 针对实际动作和范围取得授权；沉默不代表同意。 |
| `LOOP` | Take one bounded action, verify it, persist state, then evaluate every exit. | 每轮只做一个有限动作，随后验证、保存状态并检查全部出口。 |
| `PROVE` | Require independent evidence for every passing criterion. | 每个通过项都必须有独立证据。 |
| `ESCALATE` | Stop on risk, missing authority, exhausted budgets, conflicting sources, or no progress. | 遇到风险、权限不足、预算耗尽、真相源冲突或无进展时停止并交还人工。 |

## Durable run layout｜持久运行目录

`STANDARD` and `STRICT` runs use `.taskforge/<run-id>/` inside the working repository.

`STANDARD` 与 `STRICT` 运行会在工作仓库中使用 `.taskforge/<run-id>/`。

```text
.taskforge/<run-id>/
├── contract.md      # confirmed agreement｜已确认契约
├── state.json       # controller state and limits｜控制器状态与限制
├── iterations.md    # append-only evidence log｜只追加的证据日志
└── completion.md    # final evidence matrix｜最终证据矩阵
```

Initialize and validate a run with the bundled scripts. The validator uses only the Python standard library.

使用自带脚本初始化并检查运行目录。验证器只依赖 Python 标准库。

```bash
python task-forge/scripts/init_run.py /path/to/workspace --run-id contract-review --mode STANDARD
python task-forge/scripts/validate_run.py /path/to/workspace/.taskforge/contract-review
python task-forge/scripts/validate_run.py --self-test
```

## Verification and loop safety｜验证与循环安全

TaskForge checks acceptance criteria with named verifiers, stores real progress fingerprints, and stops when retries, time, iterations, tokens, cost, or no-progress limits fire. Unattended controllers must enforce these limits outside the model call.

TaskForge 使用具名验证器检查验收标准，保存能反映真实进展的状态指纹；当重试、时间、迭代、Token、费用或无进展限制触发时立即停止。无人值守控制器必须在模型调用之外执行这些限制。

Verifier code, protected tests, CI rules, and their configuration must stay outside the execution loop’s write authority. A passing signal is rejected if the loop weakened the mechanism that produced it.

验证器代码、受保护测试、CI 规则及其配置不能处于执行循环的写权限内。如果循环削弱了产生通过信号的检查机制，即使结果显示通过，也必须拒绝接受。

## Behavior evals｜行为评测

The `evals/` suite contains six deterministic cases: trigger restraint, a LITE edit, a STANDARD durable run, verifier tampering, an approval boundary, and a no-progress exit. Real model runs require Docker, `skill-optimizer`, and an `OPENROUTER_API_KEY`.

`evals/` 套件包含六个确定性案例：克制触发、轻量编辑、标准持久运行、验证器篡改、审批边界和无进展退出。运行真实模型矩阵需要 Docker、`skill-optimizer` 和 `OPENROUTER_API_KEY`。

```bash
npx tsx src/cli.ts run-suite /path/to/task-forge/evals/suite.yml --trials 3
```

## Install｜安装

Install directly from GitHub:

直接从 GitHub 安装：

```bash
python install-skill-from-github.py --repo Q1W53/task-forge --path task-forge
```

Or clone the repository and copy the inner `task-forge` directory into `$CODEX_HOME/skills/task-forge`.

也可以克隆仓库，再把内层 `task-forge` 目录复制到 `$CODEX_HOME/skills/task-forge`。

## Use｜使用

```text
$task-forge Turn this request into the lightest safe Task Contract, execute within explicit limits, and prove completion with evidence.
```

```text
$task-forge 用最轻但足够安全的严格度处理这个任务，在明确限制内执行，并用证据证明完成。
```

TaskForge may trigger implicitly for unattended or consequential work with missing acceptance tests, authority, budgets, stop rules, or escalation paths. It should not trigger implicitly for routine questions, explanations, or small reversible edits whose outcome is already clear.

当无人值守或影响较大的任务缺少验收测试、权限、预算、停止规则或升级路径时，TaskForge 可以隐式触发。对于普通问答、解释，以及目标已经清楚的小型可逆编辑，它不应自行触发。

## Repository structure｜仓库结构

```text
task-forge/
├── README.md
├── LICENSE
├── evals/
└── task-forge/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/
    └── scripts/
```

The repository root contains public documentation and the MIT license. The inner directory is the installable Codex skill.

仓库根目录存放公开说明和 MIT 许可证；内层目录是可直接安装的 Codex Skill。

## License｜开源协议

Released under the [MIT License](LICENSE). You may use, modify, redistribute, and use TaskForge commercially while retaining the copyright and license notice.

本项目采用 [MIT License](LICENSE)。保留版权与许可证声明后，你可以使用、修改、再分发，也可以用于商业项目。

© 2026 Q1W53
