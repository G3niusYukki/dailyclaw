# 轻量CRM系统设计

## 目标
从Gmail提取有价值的联系人和对话，建立可维护的关系管理系统。

## 架构

### 数据存储：Google Sheets
- **主表：Contacts** - 所有联系人信息
- **对话记录：Conversations** - 重要对话摘要
- **标签管理：Tags** - 自定义标签体系

### 数据流程
```
Gmail → 过滤提取 → AI分类评分 → Google Sheets → 自动化提醒
```

## Contacts表结构

| 字段 | 类型 | 说明 |
|------|------|------|
| email | string | 主键 |
| name | string | 联系人姓名 |
| company | string | 公司/组织 |
| title | string | 职位 |
| first_contact | date | 首次联系时间 |
| last_contact | date | 最近互动时间 |
| interaction_count | number | 互动次数 |
| value_score | number | 价值评分(1-10) |
| tags | array | 标签(客户/朋友/合作等) |
| notes | string | 备注 |
| source | string | 来源(email/manual) |
| created_at | timestamp | 创建时间 |
| updated_at | timestamp | 更新时间 |

## 过滤规则

### 自动排除（低价值）
- 发件人包含：noreply, no-reply, newsletter, marketing, unsubscribe
- 域名：mailer-daemon, postmaster
- 促销分类邮件
- 无实质内容的自动回复

### 保留（高价值）
- 有来回对话（thread > 1）
- 包含项目/合作关键词
- 来自个人邮箱域名
- 有会议/电话讨论
- 来自已知重要联系人

## 价值评分算法

```python
score = 0

# 基础分
if is_personal_email: score += 2
if has_company_email: score += 1

# 互动分
score += min(interaction_count * 0.5, 3)  # 最多3分

# 内容分
if has_project_discussion: score += 2
if has_meeting_mention: score += 1
if has_business_keywords: score += 1

# 时效分
days_since_last = (now - last_contact).days
if days_since_last < 30: score += 1
elif days_since_last > 180: score -= 1

# 最终评分（1-10）
final_score = max(1, min(10, round(score)))
```

## 标签体系

### 关系类型
- `客户` - 付费客户
- `潜在客户` - 有转化可能
- `合作伙伴` - 业务合作
- `供应商` - 服务提供方
- `同事` - 工作关系
- `朋友` - 私人关系
- `行业` - 行业联系
- `其他` - 未分类

### 状态标签
- `活跃` - 3个月内有互动
- `沉睡` - 3-6个月无互动
- `流失` - 6个月以上无互动
- `重要` - 高优先级

### 自定义标签
- 项目名（如：`项目A`）
- 兴趣标签（如：`AI`、`投资`）
- 地区标签（如：`北京`、`海外`）

## 自动化功能

### 定期任务
1. **周报生成** - 每周一生成本周需要跟进的联系人
2. **沉睡提醒** - 检测30天+未联系的重要联系人
3. **生日提醒** - 如有生日信息，提前3天提醒
4. **价值重算** - 每月重新计算所有联系人价值评分

### 邮件触发
- 新邮件到达 → 自动识别发件人 → 更新互动记录
- 新联系人 → 自动创建记录并标记为待确认

## 隐私考虑

- 敏感信息加密存储
- 访问日志记录
- 数据本地备份
- 符合GDPR/个人信息保护法
