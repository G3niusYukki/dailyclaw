# 🔌 MCP Integration - MCP 生态集成

## 概述

MCP (Model Context Protocol) 是 OpenClaw 的工具调用标准。本模块负责 MCP 服务器的管理和集成。

## 什么是 MCP？

MCP 是 OpenClaw 定义的协议，用于标准化 AI Agent 与外部工具的交互：

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   AI Agent  │←───────→│  MCP Server │←───────→│  External   │
│             │  JSON   │             │  HTTP   │   Tools     │
└─────────────┘         └─────────────┘         └─────────────┘
```

## 支持的 MCP 工具

| 工具 | 类型 | 状态 |
|------|------|------|
| 文件系统 | stdio | ✅ 可用 |
| 浏览器 | stdio | ✅ 可用 |
| GitHub | http | ✅ 可用 |
| 数据库 | stdio | 📅 计划中 |
| 搜索引擎 | http | 📅 计划中 |

## 配置 MCP 服务器

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

## 使用 mcporter CLI

```bash
# 列出配置的 MCP 服务器
mcporter list

# 调用 MCP 工具
mcporter call filesystem --tool read_file --params '{"path": "/tmp/test.txt"}'

# 添加新的 MCP 服务器
mcporter add --name myserver --command "python" --args "server.py"
```

## 开发自定义 MCP 服务器

```python
# my_mcp_server.py
from mcp.server import Server

app = Server("my-server")

@app.tool()
def my_tool(param: str) -> str:
    """工具描述"""
    return f"Result: {param}"

if __name__ == "__main__":
    app.run()
```

## 路线图

- [x] MCP 基础集成
- [ ] 可视化 MCP 管理界面
- [ ] MCP 市场/仓库
- [ ] 自定义 MCP 开发工具

---

*MCP - 让工具调用标准化 🔌*
