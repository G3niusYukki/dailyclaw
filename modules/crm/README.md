# 📇 CRM - 客户关系管理

## 概述

CRM 模块集成 Google Sheets，实现联系人管理和数据同步。

## 功能特性

- 📊 Google Sheets 双向同步
- 👥 联系人导入/导出
- 🔍 智能搜索
- 📧 邮件集成

## 快速开始

### 1. 配置 Google API

```bash
cd modules/crm
npm install
```

创建 `credentials.json`：

```json
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "redirect_uris": ["http://localhost:3000/oauth2callback"]
}
```

### 2. 授权

```bash
node scripts/check.js
# 按提示完成 OAuth 授权
```

### 3. 同步数据

```bash
# 从 Google Sheets 导出
node scripts/extract-contacts.js

# 同步到 Google Sheets
node scripts/sync-to-sheets.js
```

## 数据结构

### 联系人格式

```json
{
  "id": "uuid",
  "name": "张三",
  "email": "zhangsan@example.com",
  "phone": "+86 138****8888",
  "tags": ["客户", "VIP"],
  "notes": "重要客户",
  "last_contact": "2026-03-01",
  "created_at": "2026-01-15"
}
```

## 脚本说明

| 脚本 | 用途 |
|------|------|
| `check.js` | 检查配置和授权状态 |
| `extract-contacts.js` | 从 Sheets 导出联系人 |
| `sync-to-sheets.js` | 同步联系人到 Sheets |

## Google Sheets 格式

| 姓名 | 邮箱 | 电话 | 标签 | 备注 | 最后联系 |
|------|------|------|------|------|----------|
| 张三 | ... | ... | ... | ... | ... |

---

*客户关系管理，让连接更有价值 📇*
