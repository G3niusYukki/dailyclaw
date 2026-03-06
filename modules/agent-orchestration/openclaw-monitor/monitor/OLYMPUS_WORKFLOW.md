# Olympus 多 Agent 协作体系（Greek Myth）

## 角色编组

- **Zeus（总指挥）**：目标拆解、优先级裁决、冲突仲裁
- **Athena（架构）**：方案设计、边界定义、评审基线
- **Hephaestus（工程）**：核心开发、脚本实现、重构落地
- **Apollo（质量）**：测试、验收、发布前质量门禁
- **Hermes（调度）**：任务分发、状态回填、日报同步
- **Artemis（运维）**：上线、回滚、稳定性与监控

## 标准工作流（并行可扩展）

1. **需求受理（Zeus）**  
   输入需求，拆成可执行任务，写入 `task_ledger.json`。
1.1 **自动派单（Zeus Dispatcher）**  
   刷新脚本会自动把 `TODO` 且 `agent_id=zeus/main/unassigned` 的任务按关键词分配到对应成员。
2. **方案评审（Athena）**  
   给出实现方案、风险、验收标准。
3. **并行实现（Hephaestus + Hermes）**  
   Hermes 负责调度，Hephaestus 实施开发与脚本变更。
4. **质量门禁（Apollo）**  
   核验功能、边界、回归风险，更新任务状态为 `DONE/BLOCKED`。
5. **发布与守护（Artemis）**  
   执行启动/停止/重启，监控运行状态。
6. **闭环复盘（Zeus）**  
   汇总收益与问题，沉淀到 README/流程文档。

## 状态规范

- `TODO`：待处理
- `DOING`：进行中
- `DONE`：已完成
- `BLOCKED`：阻塞中
- `IDLE`：当前无任务（用于实时在线态）

## 数据落点

- 任务台账：`monitor/data/task_ledger.json`
- 展示快照：`monitor/data/tasks.json`
- 代码变化：`monitor/data/code_changes.json`
- 团队编组：`monitor/config/team.json`

> 面板展示逻辑：先显示台账任务；无台账时显示实时 `LIVE-*` 状态任务。
