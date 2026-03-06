<div align="center">

# Security Policy | 安全政策

</div>

---

## 🔒 Supported Versions | 支持的版本

The following versions of DailyClaw are currently being supported with security updates:

以下版本的 DailyClaw 目前正在接受安全更新支持：

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1.0 | :x:                |

---

## 🚨 Reporting a Vulnerability | 报告漏洞

### English

If you discover a security vulnerability in DailyClaw, please report it to us as soon as possible. We take security issues seriously and will respond promptly.

**Please DO NOT:**
- Open a public issue on GitHub
- Disclose the vulnerability publicly before it is fixed

**Please DO:**
- Email us at **security@dailyclaw.dev** (placeholder - use GitHub Security Advisory)
- Use [GitHub Security Advisory](https://github.com/G3niusYukki/dailyclaw/security/advisories/new) for private reporting
- Provide a detailed description of the vulnerability
- Include steps to reproduce the issue
- Suggest a fix if possible

### 中文

如果您在 DailyClaw 中发现安全漏洞，请尽快向我们报告。我们认真对待安全问题，并将及时响应。

**请不要：**
- 在 GitHub 上公开创建 issue
- 在漏洞修复前公开披露漏洞

**请：**
- 发送邮件至 **security@dailyclaw.dev**（占位符 - 请使用 GitHub Security Advisory）
- 使用 [GitHub Security Advisory](https://github.com/G3niusYukki/dailyclaw/security/advisories/new) 进行私密报告
- 提供漏洞的详细描述
- 包含重现问题的步骤
- 如有可能，建议修复方案

---

## ⏱️ Response Timeline | 响应时间线

| Phase | Time | Description |
|-------|------|-------------|
| Acknowledgment | Within 48 hours | We will acknowledge receipt of your report |
| Initial Assessment | Within 7 days | We will provide an initial assessment |
| Fix Development | Variable | Depends on complexity |
| Disclosure | After fix | Coordinated disclosure with reporter |

| 阶段 | 时间 | 描述 |
|------|------|------|
| 确认收到 | 48小时内 | 我们将确认收到您的报告 |
| 初步评估 | 7天内 | 我们将提供初步评估 |
| 修复开发 | 视情况而定 | 取决于复杂程度 |
| 披露 | 修复后 | 与报告者协调披露 |

---

## 🛡️ Security Measures | 安全措施

DailyClaw implements the following security measures:

DailyClaw 实施以下安全措施：

### 1. AI Safety Guardrails | AI 安全护栏

- Built-in prompt injection detection | 内置提示词注入检测
- Response filtering and sanitization | 响应过滤和清理
- Human oversight for critical operations | 关键操作的人工监督

### 2. Data Protection | 数据保护

- No sensitive data logging | 不记录敏感数据
- Encrypted storage for credentials | 凭据加密存储
- Regular security audits | 定期安全审计

### 3. Access Control | 访问控制

- Role-based permissions | 基于角色的权限
- Multi-agent approval for high-risk actions | 高风险操作的多代理审批
- Audit trail for all actions | 所有操作的审计跟踪

### 4. Network Security | 网络安全

- Secure API communications | 安全的 API 通信
- Certificate validation | 证书验证
- Rate limiting | 速率限制

---

## 🔐 Best Practices | 最佳实践

### For Users | 对于用户

1. **Keep your API keys secure** | 保持 API 密钥安全
   - Never commit keys to version control | 永远不要将密钥提交到版本控制
   - Use environment variables | 使用环境变量
   - Rotate keys regularly | 定期轮换密钥

2. **Review AI-generated content** | 审查 AI 生成的内容
   - Always verify before publishing | 发布前始终验证
   - Use draft mode by default | 默认使用草稿模式

3. **Monitor system logs** | 监控系统日志
   - Watch for unusual activity | 关注异常活动
   - Set up alerts | 设置警报

### For Contributors | 对于贡献者

1. **Follow secure coding practices** | 遵循安全编码实践
2. **Run security tests before submitting PRs** | 提交 PR 前运行安全测试
3. **Report security concerns immediately** | 立即报告安全问题

---

## 📋 Security Checklist | 安全检查清单

Before deploying DailyClaw, ensure:

在部署 DailyClaw 之前，请确保：

- [ ] API keys are stored securely (not in code) | API 密钥安全存储（不在代码中）
- [ ] Environment variables are configured | 环境变量已配置
- [ ] Logging level is appropriate | 日志级别适当
- [ ] Human oversight is enabled for critical actions | 关键操作启用了人工监督
- [ ] Network connections use HTTPS | 网络连接使用 HTTPS
- [ ] Dependencies are up to date | 依赖项是最新的

---

## 🙏 Security Acknowledgments | 安全致谢

We would like to thank the following security researchers who have helped improve DailyClaw's security:

我们要感谢以下帮助改进 DailyClaw 安全性的安全研究人员：

*None yet - be the first!* | *暂无 - 成为第一个！*

---

## 📞 Contact | 联系方式

- 🐛 Security Issues: [GitHub Security Advisory](https://github.com/G3niusYukki/dailyclaw/security/advisories/new)
- 📧 Email: security@dailyclaw.dev (placeholder)
- 💬 Discord: #security channel

---

<div align="center">

**🔒 Security is a shared responsibility | 安全是共同的责任**

</div>
