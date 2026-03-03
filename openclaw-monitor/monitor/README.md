# OpenClaw Agents 任务监控面板（MVP）

## 产物
- `monitor/agents-dashboard.html`：本地静态监控面板
- `monitor/data/tasks.json`：任务状态与详情源数据
- `monitor/data/code_changes.json`：代码动态快照（脚本生成）
- `monitor/scripts/refresh_status.py`：快照刷新脚本（真实 git 数据）

## 功能覆盖
1. **任务动态状态**：支持 `TODO / DOING / DONE / BLOCKED`，并可展开查看目标、阻塞、ETA、验收标准。
2. **代码动态变化**：每个任务按 `repo_path` 关联 git 仓库，展示：
   - `git status --porcelain` 文件变化（tracked/untracked）
   - 最近提交（默认取最近 5 条）
   - 未提交增删行统计（`git diff --numstat` + staged）
3. **自动刷新**：页面默认每 10 秒刷新，可在页面右上角开关。
4. **状态变化高亮**：同一浏览器会话内若任务状态变更，卡片边框高亮。

## 2026-03-02 布局优化（OC-MONITOR-UX-OPT-003）
为提升同屏信息密度并保持可读性，已完成以下改造：

1. **紧凑信息卡布局（密度提升）**
   - 改为更紧凑的间距与字号，减少卡片留白。
   - 顶部与卡片模块统一蓝白风格，保留状态色标签。
   - 默认采用双栏卡片布局，1080p 同屏可展示更多任务。

2. **任务列表双栏/表格/员工视图切换**
   - 视图切换控件：`双栏卡片` / `表格总览` / `员工视图`。
   - 表格模式提供固定表头与横向滚动，便于快速比对关键字段。
   - 员工视图按 `agent_id` 聚合，展示员工中文名、职责、当前任务、状态、ETA、阻塞原因与任务数。
   - 同一员工多任务按状态优先级排序：`BLOCKED > DOING > TODO > DONE`（无任务显示 `IDLE`）。

3. **详情区折叠 + 关键字段固定**
   - 每个任务详情区默认折叠（`展开详情`）。
   - 详情区内部加入粘性关键字段条（状态/负责人/ETA/阻塞），滚动阅读时保持可见。

4. **代码变化按任务聚合，默认摘要**
   - 代码变化按任务（`repo_path`）聚合呈现。
   - 默认只显示摘要：变更文件数、tracked/untracked、行增删。
   - 通过折叠面板展开查看文件明细与最近提交。

## 使用方式
```bash
# 进入你的 OpenClaw workspace 根目录（其下有 monitor/）
cd <your-openclaw-workspace>
python3 monitor/scripts/refresh_status.py
python3 monitor/server.py
# 打开 http://127.0.0.1:8793/monitor/agents-dashboard.html
```

### 一键启动
```bash
cd <package-or-workspace-root>
./start_monitor.sh
```

### 一键停止
```bash
cd <package-or-workspace-root>
./stop_monitor.sh
```

### 一键重启
```bash
cd <package-or-workspace-root>
./restart_monitor.sh
```

> 建议在另一个终端定时执行刷新脚本，保证 `code_changes.json` 持续更新。

例如：
```bash
while true; do
  python3 ./monitor/scripts/refresh_status.py
  sleep 10
done
```

## 主会话任务登记（让面板可见“全部进度”）

### 数据来源
- `monitor/data/tasks.json`：面板读取的最终任务快照（包含实时任务 + 台账任务）。
- `monitor/data/task_ledger.json`：人工登记的任务台账（含主会话 `agent_id=main`）。
- `monitor/scripts/refresh_status.py`：合并实时状态与台账，生成最终展示数据。

### 新增：主会话任务写入脚本
使用 `monitor/scripts/task_upsert.py` 新增或更新任务（按 `task_id` upsert）：

```bash
python3 ./monitor/scripts/task_upsert.py \
  --task-id OC-MONITOR-ALL-PROGRESS-002 \
  --agent-id main \
  --owner-cn 蛋蛋 \
  --duty 主会话调度与执行 \
  --status DOING \
  --task-content 让任务面板可见全部进度 \
  --eta 60分钟 \
  --blockers 无 \
  --refresh
```

支持字段：
- `task_id`
- `agent_id`
- `owner_cn`
- `duty`
- `status`
- `task_content`
- `eta`
- `blockers`

说明：
- 建议写入后带 `--refresh`，会立即刷新 `tasks.json`，页面刷新即可看到。
- 当某个 `agent_id` 在台账中有任务时，面板会优先展示该台账任务，避免与 `LIVE-*` 占位实时项重复。

## 环境变量
- `OC_MONITOR_ROOT`：workspace 根目录（默认自动推断）
- `OPENCLAW_HOME`：OpenClaw 主目录（默认 `~/.openclaw`）
- `MONITOR_PORT`：server 端口（默认 `8793`）

## 数据真实性说明（零 Mock）
- 面板不使用随机/伪造指标。
- 代码变化全部来自本地真实 git 命令。
- `tasks.json` 由实时状态与真实任务台账合并生成，不注入假任务。
