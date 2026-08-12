# 更新日志

## 2026-08-12

### 修复

- 强化 `GRILL -> CONTRACT -> CONFIRM -> LOOP` 阶段门禁：关键问题未回答时必须停留在 `GRILL`，不得提前生成待确认契约。
- 新增 `AWAITING_INPUT` 状态，区分“等待用户补充材料”和“等待用户确认完整契约”。
- 修正 DEEP 运行初始化状态，空白契约不再被错误标记为 `AWAITING_CONFIRMATION`。
- 明确产品内部的 Dify Loop/Iteration 节点与 TaskForge 执行循环是两个不同层级。
- 验证器新增契约准备状态检查：只有 `READY` 或 `READY WITH TBDs` 才能进入 `AWAITING_CONFIRMATION`。

### 测试

- 新增阶段门禁行为用例，防止 Agent 在关键问题尚未回答时越过 GRILL 或请求确认契约。
- 扩展验证器自测，覆盖不完整契约被错误送入确认阶段的回归场景。
