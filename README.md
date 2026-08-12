# TaskForge｜任务锻造

`GRILL -> CONTRACT -> CONFIRM -> LOOP -> PROVE | ESCALATE`

TaskForge 是一个面向 Codex 的任务工程 Skill。它适合处理容易误解、影响较大、需要持续推进，或者“做完了”却很难证明的工作。它先追问，再展示任务契约；用户确认后才执行，最终用逐项证据收口。

## 为什么改成两个模式

旧版使用 `LITE`、`STANDARD`、`STRICT` 三档。实际使用中，`LITE` 容易被理解成“可以不提问、不展示契约”，而后两档在文档持久化上又有较多重叠。

现在只保留两种行为清楚的模式：

| 模式 | 适用情况 | 必须做到 |
| --- | --- | --- |
| `LIGHT` | 单次会话、低风险、可逆、目标基本明确 | 提出 2–5 个会改变结果的问题；在聊天中展示简版契约和验收表；得到确认后执行；最终给出证据矩阵。 |
| `DEEP` | 多步骤、业务语义复杂、跨会话、长期运行、对外写入、不可逆或成本较高 | 分轮深问；沉淀上下文、术语和决策；建立持久状态、审批、预算和停止条件；逐轮验证并保留证据。 |

两种模式都不能跳过提问，也不能把未展示的内部计划当成用户已确认的契约。区别只在提问深度和是否建立持久运行目录。

## DEEP 的文档体系

`DEEP` 吸收了 `grill-with-docs` 的做法。访谈不再只留在聊天记录里，而是把事实、共同语言和关键选择拆开保存：

```text
.taskforge/<run-id>/
├── context.md       # 当前状态、目标状态、事实来源、约束和待确认问题
├── glossary.md      # 术语、缩写、统一定义和负责人
├── decisions.md     # 决策问题、备选方案、选择理由和影响
├── contract.md      # 经确认的执行边界、权限、验收和退出条件
├── state.json       # 机器可读状态、预算、验收项和状态指纹
├── iterations.md    # 只追加的动作与验证记录
└── completion.md    # 最终证据矩阵、剩余风险和后续决定
```

`context.md` 只把已确认事实写成事实；没有确认的内容留在“待确认问题”中。`glossary.md` 用来处理同一个词在业务、技术和管理团队中含义不同的问题。`decisions.md` 记录为什么选 A 而没有选 B，避免后续 Agent 只看到结论却不知道限制条件。

契约保持精简。背景材料属于 `context.md`，术语属于 `glossary.md`，取舍属于 `decisions.md`；`contract.md` 只保留执行必须遵守的边界。

## 文档语言自动选择

TaskForge 根据用户的主要语言选择所有面向用户的文档：

- 中文请求生成中文契约、上下文、术语、决策、迭代和完成报告。
- 英文请求生成英文版本。
- 用户明确指定语言时，明确要求优先于自动判断。
- 中英文比例接近且没有指定时，沿用当前对话的主要语言，并把选择写进契约。
- 文件名和 `state.json` 的字段保持英文，方便脚本稳定读取。

初始化脚本支持显式语言，也可以根据请求文本判断：

```bash
python task-forge/scripts/init_run.py /path/to/workspace \
  --run-id sales-pipeline \
  --mode DEEP \
  --language auto \
  --user-text "梳理销售管线实施方案，并在确认后持续执行"
```

需要固定语言时使用 `--language zh-CN` 或 `--language en`。

## 六个阶段

| 阶段 | 实际行为 |
| --- | --- |
| `GRILL` | 先复述当前状态和目标，再追问会改变业务含义、范围、权限、验收或停止行为的问题。 |
| `CONTRACT` | 展示目标、范围、事实来源、受保护内容、权限、验收证据和退出条件。 |
| `CONFIRM` | 用户确认可见契约后才开始产生状态变化；沉默不算授权。 |
| `LOOP` | 每轮只处理一个未通过的验收项，执行最小动作，然后立即验证和记录。 |
| `PROVE` | 最终逐项列出标准、结果、证据和验证方式；业务正确性与技术正确性分开检查。 |
| `ESCALATE` | 遇到权限不足、来源冲突、预算耗尽、重复失败或无法判断成功时停止。 |

## 使用示例

轻量任务：

```text
$task-forge 用 LIGHT 模式帮我修改这份一页 PPT。先问清当前进度和验收要求，展示简版契约，我确认后再制作。
```

复杂任务：

```text
$task-forge 用 DEEP 模式设计并实施销售自动化工作流。把业务上下文、术语和架构决策分别沉淀，契约使用中文；没有通过验收前持续迭代，但不要越过审批和预算边界。
```

英文任务：

```text
$task-forge Use DEEP mode. Interview me in rounds, keep the contract and companion documents in English, and publish only after every acceptance criterion has evidence.
```

## 初始化与验证

验证器只使用 Python 标准库。完整 `DEEP` 目录必须包含七份文件，缺少任何一份都会失败；契约可以使用中文或英文标题。

```bash
python task-forge/scripts/init_run.py /path/to/workspace \
  --run-id contract-review \
  --mode DEEP \
  --language zh-CN

python task-forge/scripts/validate_run.py \
  /path/to/workspace/.taskforge/contract-review

python task-forge/scripts/validate_run.py --self-test
```

## 从旧版本迁移

| 旧模式 | 新模式 | 变化 |
| --- | --- | --- |
| `LITE` | `LIGHT` | 不再允许完全跳过访谈；必须展示简版契约和最终证据。 |
| `STANDARD` | `DEEP` | 保留持久契约、状态、迭代和完成报告，并增加上下文、术语和决策文档。 |
| `STRICT` | `DEEP` | 仍使用审批、硬预算、无进展停止和验证器保护；这些机制按风险启用，不再单独设模式。 |

旧的 `STANDARD` 或 `STRICT` 运行目录不会被自动重写。新任务应使用 `DEEP`；需要迁移旧状态时，先补齐三份新增文档，并把 `state.json` 中的模式改为 `DEEP`，随后运行验证器。

## 验证器保护与停止规则

验证器代码、受保护测试、CI 规则及其配置不能落入执行循环的写权限。Agent 不能靠删除检查、降低覆盖率、跳过失败或硬编码答案获得通过信号。

默认情况下，同一验收项最多失败三次；两个实质相同的失败，或连续两轮状态指纹相同，都会停止继续尝试。无人值守任务还必须由模型调用之外的控制器执行时间、迭代、Token、金额和速率限制。

## 安装

```bash
python install-skill-from-github.py --repo Q1W53/task-forge --path task-forge
```

也可以克隆仓库，然后把内层 `task-forge` 目录复制到 `$CODEX_HOME/skills/task-forge`。

## 仓库结构

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

仓库根目录存放公开说明和 MIT 许可证；内层目录是可直接安装的 Codex Skill。

## License

本项目采用 [MIT License](LICENSE)。保留版权与许可证声明后，可以使用、修改、再分发或用于商业项目。

© 2026 Q1W53
