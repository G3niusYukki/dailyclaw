# DailyClaw API Documentation

> 🐱 AI Agent Evolution System API Reference
> 
> 本文档提供 DailyClaw 项目的 API 接口说明和使用示例。

---

## 📑 Table of Contents

- [概述 / Overview](#概述--overview)
- [认证 / Authentication](#认证--authentication)
- [核心 API / Core APIs](#核心-api--core-apis)
  - [Agent Orchestration](#agent-orchestration)
  - [Evolution Tracking](#evolution-tracking)
  - [Metrics & Analytics](#metrics--analytics)
- [错误处理 / Error Handling](#错误处理--error-handling)
- [速率限制 / Rate Limiting](#速率限制--rate-limiting)
- [SDK & 客户端 / SDK & Clients](#sdk--客户端--sdk--clients)

---

## 概述 / Overview

DailyClaw API 提供与六猫协作系统的程序化交互能力，支持：

- 🤖 **代理管理** - 创建、配置和管理 AI Agent
- 📅 **进化追踪** - 记录和查询每日进展
- 📊 **指标分析** - 获取项目度量数据
- 🔌 **MCP 集成** - 与外部工具生态对接

### 基础信息

| 项目 | 值 |
|------|-----|
| **Base URL** | `https://api.dailyclaw.dev/v1` (示例) |
| **Protocol** | HTTPS |
| **数据格式** | JSON |
| **字符编码** | UTF-8 |

### HTTP 状态码

| 状态码 | 含义 | 说明 |
|--------|------|------|
| 200 | OK | 请求成功 |
| 201 | Created | 创建成功 |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未认证 |
| 403 | Forbidden | 权限不足 |
| 404 | Not Found | 资源不存在 |
| 429 | Too Many Requests | 请求过于频繁 |
| 500 | Internal Server Error | 服务器内部错误 |

---

## 认证 / Authentication

DailyClaw API 使用 API Key 进行认证。

### 请求头格式

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

### 获取 API Key

```bash
# 通过 CLI 生成
dailyclaw auth generate-key --name "my-app"

# 响应
{
  "key": "dc_live_xxxxxxxxxxxxxxxx",
  "name": "my-app",
  "created_at": "2026-03-07T01:00:00Z",
  "expires_at": "2027-03-07T01:00:00Z"
}
```

---

## 核心 API / Core APIs

### Agent Orchestration

#### 列出所有代理

```http
GET /agents
```

**响应示例：**

```json
{
  "agents": [
    {
      "id": "zeus-001",
      "name": "Zeus",
      "role": "orchestrator",
      "breed": "orange_cat",
      "status": "active",
      "channels": ["general", "announcements"],
      "created_at": "2026-02-22T00:00:00Z"
    },
    {
      "id": "athena-001",
      "name": "Athena",
      "role": "architect",
      "breed": "ragdoll",
      "status": "active",
      "channels": ["architecture"],
      "created_at": "2026-02-22T00:00:00Z"
    }
  ],
  "total": 6,
  "page": 1,
  "per_page": 20
}
```

#### 获取代理详情

```http
GET /agents/{agent_id}
```

**响应示例：**

```json
{
  "id": "hephaestus-001",
  "name": "Hephaestus",
  "role": "implementer",
  "breed": "tabby",
  "status": "active",
  "channels": ["coding"],
  "capabilities": ["code_review", "refactoring", "debugging"],
  "stats": {
    "tasks_completed": 42,
    "lines_of_code": 15000,
    "review_count": 128
  },
  "created_at": "2026-02-22T00:00:00Z",
  "updated_at": "2026-03-07T12:00:00Z"
}
```

#### 分配任务给代理

```http
POST /agents/{agent_id}/tasks
```

**请求体：**

```json
{
  "title": "优化 README 文档",
  "description": "添加更多 badges 和改进排版",
  "priority": "high",
  "tags": ["docs", "readme", "enhancement"],
  "due_date": "2026-03-08T23:59:59Z"
}
```

**响应示例：**

```json
{
  "task_id": "task-123",
  "agent_id": "hephaestus-001",
  "status": "assigned",
  "created_at": "2026-03-07T01:00:00Z"
}
```

---

### Evolution Tracking

#### 获取进化记录

```http
GET /evolution/{year}/{month}/{day}
```

**示例：** `GET /evolution/2026/03/07`

**响应示例：**

```json
{
  "date": "2026-03-07",
  "focus": "仓库重构和文档优化",
  "completed": [
    "引入六猫协作系统",
    "优化 README 排版",
    "添加 CI/CD 流程"
  ],
  "in_progress": [
    "完善 API 文档",
    "添加更多测试"
  ],
  "insights": [
    "清晰的架构设计有助于团队协作",
    "自动化流程可以提升开发效率"
  ],
  "metrics": {
    "commits": 15,
    "files_changed": 23,
    "lines_added": 1200,
    "lines_removed": 300
  },
  "agents_involved": ["zeus-001", "athena-001", "hephaestus-001"]
}
```

#### 列出进化记录

```http
GET /evolution?from=2026-03-01&to=2026-03-07&agent=hephaestus-001
```

**查询参数：**

| 参数 | 类型 | 描述 |
|------|------|------|
| `from` | string | 起始日期 (YYYY-MM-DD) |
| `to` | string | 结束日期 (YYYY-MM-DD) |
| `agent` | string | 按代理筛选 |
| `tag` | string | 按标签筛选 |

#### 创建进化记录

```http
POST /evolution
```

**请求体：**

```json
{
  "date": "2026-03-07",
  "focus": "今日主要目标",
  "completed": ["完成任务1", "完成任务2"],
  "in_progress": ["进行中任务"],
  "insights": ["今日感悟"],
  "metrics": {
    "commits": 5,
    "files_changed": 10
  },
  "tags": ["refactor", "docs"]
}
```

---

### Metrics & Analytics

#### 获取项目指标

```http
GET /metrics
```

**响应示例：**

```json
{
  "overview": {
    "total_agents": 6,
    "total_evolutions": 14,
    "total_tasks": 128,
    "active_tasks": 12
  },
  "activity": {
    "daily_commits": 15,
    "weekly_commits": 89,
    "monthly_commits": 320
  },
  "agents": {
    "zeus-001": {
      "tasks_completed": 56,
      "efficiency": 0.95
    },
    "athena-001": {
      "tasks_completed": 34,
      "efficiency": 0.92
    }
  },
  "generated_at": "2026-03-07T12:00:00Z"
}
```

#### 获取代理统计

```http
GET /metrics/agents/{agent_id}
```

#### 获取时间线数据

```http
GET /metrics/timeline?period=7d&metric=commits
```

**响应示例：**

```json
{
  "period": "7d",
  "metric": "commits",
  "data": [
    {"date": "2026-03-01", "value": 12},
    {"date": "2026-03-02", "value": 8},
    {"date": "2026-03-03", "value": 15},
    {"date": "2026-03-04", "value": 20},
    {"date": "2026-03-05", "value": 10},
    {"date": "2026-03-06", "value": 18},
    {"date": "2026-03-07", "value": 15}
  ]
}
```

---

## 错误处理 / Error Handling

### 错误响应格式

```json
{
  "error": {
    "code": "invalid_request",
    "message": "The request parameters are invalid",
    "details": [
      {
        "field": "date",
        "message": "Invalid date format, expected YYYY-MM-DD"
      }
    ],
    "request_id": "req_1234567890"
  }
}
```

### 错误代码

| 代码 | 描述 |
|------|------|
| `invalid_request` | 请求参数无效 |
| `unauthorized` | 认证失败 |
| `forbidden` | 权限不足 |
| `not_found` | 资源不存在 |
| `rate_limited` | 请求过于频繁 |
| `internal_error` | 服务器内部错误 |

---

## 速率限制 / Rate Limiting

API 请求受到速率限制，限制信息包含在响应头中：

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1646630400
```

### 限制规则

| 端点类型 | 限制 |
|---------|------|
| 读取操作 | 1000 请求/小时 |
| 写入操作 | 100 请求/小时 |
| 批量操作 | 10 请求/小时 |

---

## SDK & 客户端 / SDK & Clients

### Python SDK

```bash
pip install dailyclaw-sdk
```

```python
from dailyclaw import Client

# 初始化客户端
client = Client(api_key="dc_live_xxxxxxxx")

# 列出所有代理
agents = client.agents.list()
print(f"Total agents: {agents.total}")

# 获取代理详情
hephaestus = client.agents.get("hephaestus-001")
print(f"Tasks completed: {hephaestus.stats.tasks_completed}")

# 分配任务
task = client.agents.assign_task(
    agent_id="hephaestus-001",
    title="优化代码",
    priority="high"
)

# 获取进化记录
evolution = client.evolution.get("2026", "03", "07")
print(f"Focus: {evolution.focus}")

# 获取指标
metrics = client.metrics.get()
print(f"Total tasks: {metrics.overview.total_tasks}")
```

### JavaScript/TypeScript SDK

```bash
npm install @dailyclaw/sdk
```

```typescript
import { DailyClawClient } from '@dailyclaw/sdk';

const client = new DailyClawClient({
  apiKey: 'dc_live_xxxxxxxx'
});

// 异步操作
async function main() {
  // 列出代理
  const agents = await client.agents.list();
  console.log(`Total agents: ${agents.total}`);
  
  // 获取进化记录
  const evolution = await client.evolution.get('2026', '03', '07');
  console.log(`Focus: ${evolution.focus}`);
}

main();
```

### cURL 示例

```bash
# 设置 API Key
API_KEY="dc_live_xxxxxxxx"

# 列出代理
curl -H "Authorization: Bearer $API_KEY" \
     https://api.dailyclaw.dev/v1/agents

# 获取进化记录
curl -H "Authorization: Bearer $API_KEY" \
     https://api.dailyclaw.dev/v1/evolution/2026/03/07

# 创建任务
curl -X POST \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "新任务",
       "priority": "high",
       "tags": ["feature"]
     }' \
     https://api.dailyclaw.dev/v1/agents/hephaestus-001/tasks
```

---

## 贡献 / Contributing

API 文档持续完善中。如有建议或发现问题，请提交 [Issue](https://github.com/G3niusYukki/dailyclaw/issues)。

---

## 更新日志 / Changelog

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.0.0 | 2026-03-07 | 初始 API 文档框架 |

---

<div align="center">

**🐱 DailyClaw - 每天进步一点点**

[GitHub](https://github.com/G3niusYukki/dailyclaw) • [文档](https://dailyclaw.dev/docs) • [Discord](https://discord.gg/dailyclaw)

</div>
