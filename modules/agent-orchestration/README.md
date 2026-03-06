# 🤖 Agent Orchestration - 六猫协作系统

## 概述

六猫协作系统是 DailyClaw 的核心架构，模拟六只不同品种的猫咪分工协作，共同完成复杂任务。

## 🐱 六猫角色

| 角色 | 猫种 | 职责 | 决策层级 |
|------|------|------|----------|
| 🍊 **Zeus** | 橘猫 | 主协调、任务拆解、最终决策 | L1 - 总指挥 |
| 🎀 **Athena** | 布偶猫 | 架构设计、技术选型 | L2 - 设计 |
| 🐯 **Hephaestus** | 狸花猫 | 代码实现、功能开发 | L2 - 执行 |
| 🔵 **Apollo** | 暹罗猫 | 测试验证、质量保证 | L2 - 验证 |
| 🧶 **Hermes** | 美短 | 消息路由、系统集成 | L3 - 集成 |
| ⚫ **Artemis** | 黑猫 | 安全审查、发布管理 | L3 - 安全 |

## 协作流程

```
用户请求
    ↓
🍊 Zeus 分析 & 拆解
    ↓
┌─────────┬─────────┬─────────┐
↓         ↓         ↓
🎀 Athena  🐯 Hephaestus  🔵 Apollo
架构设计   代码实现      测试验证
    ↓         ↓         ↓
└─────────┴─────────┴─────────┘
    ↓
🧶 Hermes 集成
    ↓
⚫ Artemis 安全审查
    ↓
🍊 Zeus 汇总交付
```

## 路由规则

### Discord 频道路由

| 频道 | 默认路由 |
|------|----------|
| #🍊-general-六猫广场 | Zeus |
| #🎀-architecture-雅典娜 | Athena |
| #🐯-coding-赫菲斯托斯 | Hephaestus |
| #🔵-testing-阿波罗 | Apollo |
| #🧶-messaging-赫尔墨斯 | Hermes |
| #⚫-releases-阿尔忒弥斯 | Artemis |

### @提及路由

用户可以通过 @角色 直接召唤对应的猫咪：
- `@Athena` → 转给 Athena 处理
- `@Hephaestus` → 转给 Hephaestus 处理

## 使用示例

```
用户：帮我设计一个爬虫系统

Zeus：这个任务需要架构设计，我派 Athena 来帮您

Athena：建议采用以下架构...

Zeus：Athena 已完成设计，Hephaestus 请开始实现

Hephaestus：代码已完成...

Apollo：测试通过 ✅

Zeus：任务完成！已交付完整方案
```

## 配置

系统配置位于 `config/team.json`：

```json
{
  "agents": [
    {"id": "zeus", "role": "coordinator", "model": "claude-opus-4.6"},
    {"id": "athena", "role": "architect", "model": "glm-5"},
    {"id": "hephaestus", "role": "implementer", "model": "minimax-m2.5"},
    {"id": "apollo", "role": "tester", "model": "minimax-m2.5"},
    {"id": "hermes", "role": "integrator", "model": "minimax-m2.5"},
    {"id": "artemis", "role": "security", "model": "glm-5"}
  ]
}
```

---

*六猫协作，让 AI 更智能 🐱*
