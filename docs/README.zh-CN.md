# TaskForge｜任务锻造

## 让 AI Agent 证明它真的做完了

[English](../README.md)

TaskForge 是一个面向 Codex 的 verification-first Agent Skill。它把模糊请求变成可确认的任务契约，在约定边界内执行，并用可检查的证据结束任务。

不静默猜测，不隐藏契约，不修改验证器来换取通过，也不轻易说“完成”。

`GRILL → CONTRACT → CONFIRM → LOOP → PROVE / ESCALATE`

## 它改变了什么

假设你要求 Agent 重构认证系统并加入 GitHub 登录。

| 没有 TaskForge | 使用 TaskForge |
| --- | --- |
| 立即修改代码 | 先确认哪些登录方式必须兼容 |
| 自行猜测“完成”的含义 | 把每条验收标准映射到证据 |
| 可能遗漏迁移、回滚和既有登录路径 | 记录受保护行为与审批边界 |
| 最后给出工作摘要 | 给出测试、Schema 检查和剩余风险 |

```text
普通交付

Agent：完成。我重构了认证并加入 GitHub OAuth。

TaskForge 交付

PROVE
✓ 原有密码登录：验证通过
✓ GitHub 回调流程：验证通过
✓ Schema diff：没有未批准变更
✓ 验收标准：8/8 通过
```

这是示意案例，不是公开 benchmark 结果。完整过程见[认证重构示例](../examples/auth-refactor.md)。

## 安装

在 Codex 中要求 skill-installer 从这个仓库安装：

```text
$skill-installer Install the task-forge skill from https://github.com/Q1W53/task-forge/tree/main/task-forge
```

随后直接使用：

```text
$task-forge 帮我重构认证系统。先问清会改变结果的问题，展示任务契约，等我确认后执行；所有验收项都有证据才能说完成。
```

Codex 会在 `$HOME/.agents/skills` 和仓库内的 `.agents/skills` 查找 Skill。手动安装时，把仓库内层 [`task-forge/`](../task-forge/) 复制到其中一个位置；若没有自动出现，重启 Codex。最新目录规则见 OpenAI 官方的 [Build skills](https://developers.openai.com/plugins/build/skills) 文档。

## 六个阶段

| 阶段 | 实际行为 |
| --- | --- |
| `GRILL` | 复述现状，只追问会改变目标、范围、权限、证据、预算或停止规则的问题。 |
| `CONTRACT` | 展示结果、非目标、受保护内容、允许动作、审批门槛、验收证据和退出条件。 |
| `CONFIRM` | 用户确认可见契约；沉默不算授权，不完整的契约不能进入执行。 |
| `LOOP` | 每轮执行一个最小安全动作，立刻验证、记录，并检查重试和无进展限制。 |
| `PROVE` | 所有验收项必须有可检查证据，业务正确性与技术正确性分别判断。 |
| `ESCALATE` | 权限、输入、预算或可靠验证不足时停止，不猜测成功。 |

## LIGHT 与 DEEP

两种模式都会提问、展示契约、等待确认，并以证据结束。区别在于任务需要多少控制和持久状态。

| 模式 | 适用情况 | 交付形式 |
| --- | --- | --- |
| `LIGHT` | 单次会话、低风险、可逆、结果基本清楚 | 简短访谈、聊天内契约、最终证据矩阵 |
| `DEEP` | 多步骤、含义复杂、长期运行、对外写入、成本高或难回退 | 持久上下文、决策、状态、审批、预算、迭代记录和完成证据 |

DEEP 运行记录保存在 `.taskforge/<run-id>/`，包含上下文、术语、决策、契约、机器状态、迭代记录和完成报告。

## 适用场景

TaskForge 适合迁移、发布准备、认证改动、多文件重构、外部系统写入、无人值守任务和带有业务含义的工作。只要误解的代价高于几分钟访谈，它就有用。

如果只是回答事实问题，或者执行结果已经精确、可逆的小修改，就不必使用。TaskForge 的作用是给高风险任务加控制，不是给每条提示增加仪式。

更多可复制提示见 [`examples/`](../examples/)。

## Evals 与 benchmark

仓库已有行为评测套件，覆盖阶段门禁、持久证据、审批边界、验证器保护、无进展停止和不应触发 Skill 的对照场景。Grader 只检查文件、状态与最终输出。

目前不在 README 中声明任何 benchmark 分数。可比较结果必须包含重复试验、固定模型标识、环境信息和原始产物。方法与报告模板见 [`evals/README.md`](../evals/README.md)。

## 参与项目

路线图见 [`docs/ROADMAP.md`](ROADMAP.md)，贡献方式见 [`CONTRIBUTING.md`](../CONTRIBUTING.md)。如果 TaskForge 帮你拦住过一次假的“完成”，请给[仓库点一个 Star](https://github.com/Q1W53/task-forge)，让更多人能找到它。

本项目采用 [MIT License](../LICENSE)。
