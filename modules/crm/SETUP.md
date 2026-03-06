# 轻量CRM - 快速开始

## 📋 前置要求

1. **Google Cloud项目**（需要自己创建）
   - 访问 [Google Cloud Console](https://console.cloud.google.com/)
   - 创建新项目
   - 启用以下API：
     - Gmail API
     - Google Sheets API
     - Google People API（可选）
   - 创建OAuth 2.0凭证（桌面应用）
   - 下载凭证JSON文件

2. **Node.js环境**
   ```bash
   node --version  # 需要 >= 14.0.0
   ```

3. **安装依赖**
   ```bash
   cd ~/.openclaw/workspace/crm
   npm init -y
   npm install googleapis
   ```

## 🚀 快速开始

### 方式1：使用gog CLI（推荐）

如果你已经配置好gog：

```bash
# 1. 认证
gog auth add haoyang056@gmail.com --services gmail,sheets

# 2. 创建CRM表格
gog sheets create --title "我的CRM"

# 3. 运行提取脚本
cd ~/.openclaw/workspace/crm
node scripts/extract-contacts.js --days 90 --output contacts.json

# 4. 同步到Sheets
SPREADSHEET_ID="你的表格ID" node scripts/sync-to-sheets.js
```

### 方式2：手动方式

```bash
# 1. 配置凭证
export GOOGLE_CLIENT_ID="your-client-id"
export GOOGLE_CLIENT_SECRET="your-client-secret"
export GOOGLE_REDIRECT_URI="http://localhost"

# 2. 获取access token
# 访问OAuth URL，获取code，然后换取token

# 3. 创建表格
# 在Google Sheets中手动创建，或使用API

# 4. 运行脚本
node scripts/extract-contacts.js
node scripts/sync-to-sheets.js
```

## 📊 使用流程

### 1. 初次设置（一次性）

```bash
# 安装
npm install

# 认证（会打开浏览器）
npm run auth
```

### 2. 日常使用

```bash
# 提取最近90天的联系人
npm run extract

# 同步到Google Sheets
npm run sync

# 查看统计
npm run stats
```

### 3. 定期维护

```bash
# 每周运行一次，更新联系人
crontab -e
# 添加：
# 0 9 * * 1 cd ~/.openclaw/workspace/crm && npm run sync
```

## 🎨 Google Sheets模板

[点击这里创建CRM模板](https://docs.google.com/spreadsheets/create?title=我的CRM)

手动创建的表头：

**Contacts表：**
| Email | Name | Company | Title | First Contact | Last Contact | Interaction Count | Value Score | Tags | Notes | Source | Thread Count | Auto Tags | Updated At |

**Conversations表：**
| Email | Date | Subject | Summary | Type | Tags | Created At |

**Tags表：**
| Tag Name | Category | Description | Color | Count |

## ⚙️ 配置选项

编辑 `config.json`：

```json
{
  "daysToLookBack": 90,
  "maxResults": 500,
  "excludePatterns": [
    "noreply@",
    "newsletter@",
    "marketing@"
  ],
  "highValueKeywords": [
    "project", "合作", "项目",
    "meeting", "会议", "合同"
  ],
  "personalEmailDomains": [
    "gmail.com", "outlook.com",
    "foxmail.com", "qq.com"
  ]
}
```

## 📈 数据分析

### 价值评分分布
```sql
SELECT 
  CASE 
    WHEN value_score >= 8 THEN '高价值'
    WHEN value_score >= 5 THEN '中价值'
    ELSE '低价值'
  END as category,
  COUNT(*) as count
FROM contacts
GROUP BY category
```

### 互动频率
```sql
SELECT 
  email,
  name,
  interaction_count,
  last_contact
FROM contacts
WHERE interaction_count > 5
ORDER BY interaction_count DESC
LIMIT 20
```

### 需要激活的联系人
```sql
SELECT 
  email,
  name,
  last_contact,
  value_score
FROM contacts
WHERE 
  value_score >= 7 
  AND last_contact < DATE('now', '-90 days')
ORDER BY value_score DESC
```

## 🔧 故障排除

### OAuth错误
```
Error: Project #xxx has been deleted
```
**解决**：使用自己的Google Cloud项目，不要用gog默认的项目。

### 权限不足
```
Error: Request had insufficient authentication scopes
```
**解决**：重新授权，确保包含 `gmail.readonly` 和 `spreadsheets` scope。

### API配额超限
```
Error: Quota exceeded for quota metric
```
**解决**：减少请求频率，或申请更高配额。

## 📚 相关文档

- [Gmail API文档](https://developers.google.com/gmail/api)
- [Sheets API文档](https://developers.google.com/sheets/api)
- [Google Cloud Console](https://console.cloud.google.com/)

## 💡 提示

1. **隐私优先**：所有数据存储在你的Google账号中，不会被第三方访问
2. **定期备份**：建议每周导出一次CSV备份
3. **手动审核**：自动提取的联系人建议手动审核，避免误判
4. **标签管理**：善用标签体系，方便后续筛选和分析
5. **价值评分**：评分算法可以自定义，根据你的业务调整权重

## 🆘 需要帮助？

- 查看 [CRM-DESIGN.md](./CRM-DESIGN.md) 了解详细设计
- 查看 [scripts/](./scripts/) 目录的脚本代码
- 遇到问题随时问我～
