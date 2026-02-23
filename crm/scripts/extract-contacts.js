#!/usr/bin/env node

/**
 * Gmail联系人提取脚本
 * 从Gmail API获取邮件，过滤并提取有价值的联系人
 * 
 * 用法：node extract-contacts.js --days 90 --output contacts.json
 */

const fs = require('fs');
const { google } = require('googleapis');

// 配置
const CONFIG = {
  daysToLookBack: 90,
  maxResults: 500,
  excludePatterns: [
    /noreply@/i,
    /no-reply@/i,
    /newsletter@/i,
    /marketing@/i,
    /unsubscribe/i,
    /mailer-daemon@/i,
    /postmaster@/i,
    /donotreply@/i,
    /notification@/i,
    /alert@/i,
    /automated@/i
  ],
  highValueKeywords: [
    'project', '合作', '项目', 'meeting', '会议', 'contract', '合同',
    'proposal', '方案', 'investment', '投资', 'partnership', '伙伴'
  ],
  personalEmailDomains: [
    'gmail.com', 'outlook.com', 'hotmail.com', 'yahoo.com', 
    'icloud.com', 'foxmail.com', 'qq.com', '163.com', '126.com'
  ]
};

// 邮件解析
class EmailParser {
  constructor() {
    this.contacts = new Map();
  }

  parseMessage(message) {
    const headers = message.payload.headers;
    const from = this.getHeader(headers, 'From');
    const subject = this.getHeader(headers, 'Subject');
    const date = new Date(this.getHeader(headers, 'Date'));
    const threadId = message.threadId;

    if (!from) return null;

    // 提取邮箱和姓名
    const { email, name } = this.parseEmailAddress(from);
    
    // 检查是否应该排除
    if (this.shouldExclude(email)) return null;

    return {
      email,
      name,
      subject,
      date,
      threadId,
      snippet: message.snippet || ''
    };
  }

  parseEmailAddress(fromHeader) {
    const match = fromHeader.match(/(?:"?([^"]*)"?\s)?(?:<?(.+?@[^>,]+)>?)/);
    if (!match) return { email: '', name: '' };
    
    let email = match[2] || '';
    let name = match[1] || '';
    
    // 如果没有姓名，尝试从邮箱提取
    if (!name && email) {
      name = email.split('@')[0];
    }

    return { email: email.toLowerCase(), name: name.trim() };
  }

  getHeader(headers, name) {
    const header = headers.find(h => h.name.toLowerCase() === name.toLowerCase());
    return header ? header.value : '';
  }

  shouldExclude(email) {
    return CONFIG.excludePatterns.some(pattern => pattern.test(email));
  }

  isPersonalEmail(email) {
    const domain = email.split('@')[1];
    return CONFIG.personalEmailDomains.includes(domain);
  }

  hasHighValueKeywords(text) {
    const lowerText = text.toLowerCase();
    return CONFIG.highValueKeywords.some(keyword => 
      lowerText.includes(keyword.toLowerCase())
    );
  }

  calculateValueScore(contact) {
    let score = 0;

    // 基础分
    if (this.isPersonalEmail(contact.email)) score += 2;
    else if (contact.email.includes('@')) score += 1;

    // 互动分
    const interactionScore = Math.min(contact.interactionCount * 0.5, 3);
    score += interactionScore;

    // 内容分
    if (contact.hasHighValueContent) score += 2;
    if (contact.hasProjectKeywords) score += 1;

    // 时效分
    const daysSinceLast = (Date.now() - new Date(contact.lastContact)) / (1000 * 60 * 60 * 24);
    if (daysSinceLast < 30) score += 1;
    else if (daysSinceLast > 180) score -= 1;

    return Math.max(1, Math.min(10, Math.round(score)));
  }
}

// 主提取器
class ContactExtractor {
  constructor(auth) {
    this.gmail = google.gmail({ version: 'v1', auth });
    this.parser = new EmailParser();
    this.contacts = new Map();
  }

  async extract() {
    console.log(`开始提取最近 ${CONFIG.daysToLookBack} 天的邮件...`);

    const query = `newer_than:${CONFIG.daysToLookBack}d -category:promotions -category:updates`;
    
    let pageToken = null;
    let totalProcessed = 0;

    do {
      const response = await this.gmail.users.messages.list({
        userId: 'me',
        q: query,
        maxResults: 100,
        pageToken: pageToken
      });

      const messages = response.data.messages || [];
      console.log(`获取到 ${messages.length} 封邮件`);

      for (const message of messages) {
        await this.processMessage(message.id);
        totalProcessed++;
        
        if (totalProcessed % 50 === 0) {
          console.log(`已处理 ${totalProcessed} 封邮件...`);
        }
      }

      pageToken = response.data.nextPageToken;
    } while (pageToken && totalProcessed < CONFIG.maxResults);

    console.log(`总共处理 ${totalProcessed} 封邮件`);
    return this.finalizeContacts();
  }

  async processMessage(messageId) {
    try {
      const response = await this.gmail.users.messages.get({
        userId: 'me',
        id: messageId,
        format: 'metadata',
        metadataHeaders: ['From', 'Subject', 'Date']
      });

      const parsed = this.parser.parseMessage(response.data);
      if (!parsed) return;

      this.updateContact(parsed);
    } catch (error) {
      console.error(`处理邮件 ${messageId} 失败:`, error.message);
    }
  }

  updateContact(parsed) {
    const existing = this.contacts.get(parsed.email) || {
      email: parsed.email,
      name: parsed.name,
      firstContact: parsed.date,
      lastContact: parsed.date,
      interactionCount: 0,
      subjects: [],
      snippets: [],
      threadIds: new Set(),
      hasHighValueContent: false,
      hasProjectKeywords: false
    };

    // 更新信息
    existing.interactionCount++;
    existing.lastContact = new Date(Math.max(
      new Date(existing.lastContact),
      new Date(parsed.date)
    ));
    existing.firstContact = new Date(Math.min(
      new Date(existing.firstContact),
      new Date(parsed.date)
    ));

    // 保存主题和摘要
    if (parsed.subject && existing.subjects.length < 5) {
      existing.subjects.push(parsed.subject);
    }
    if (parsed.snippet && existing.snippets.length < 3) {
      existing.snippets.push(parsed.snippet);
    }

    existing.threadIds.add(parsed.threadId);

    // 检查高价值关键词
    const allText = (parsed.subject + ' ' + parsed.snippet).toLowerCase();
    if (this.parser.hasHighValueKeywords(allText)) {
      existing.hasHighValueContent = true;
    }
    if (/项目|project|合作|partnership/i.test(allText)) {
      existing.hasProjectKeywords = true;
    }

    this.contacts.set(parsed.email, existing);
  }

  finalizeContacts() {
    const finalContacts = [];
    
    for (const contact of this.contacts.values()) {
      // 清理数据
      contact.threadCount = contact.threadIds.size;
      delete contact.threadIds;
      
      // 计算价值评分
      contact.valueScore = this.parser.calculateValueScore(contact);
      
      // 自动标签
      contact.autoTags = this.generateAutoTags(contact);
      
      finalContacts.push(contact);
    }

    // 按价值评分排序
    finalContacts.sort((a, b) => b.valueScore - a.valueScore);

    return finalContacts;
  }

  generateAutoTags(contact) {
    const tags = [];

    // 基于域名判断
    const domain = contact.email.split('@')[1];
    if (!this.parser.isPersonalEmail(contact.email)) {
      tags.push('商务');
    } else {
      tags.push('个人');
    }

    // 基于互动频率
    if (contact.interactionCount > 10) {
      tags.push('活跃');
    } else if (contact.interactionCount < 3) {
      tags.push('低频');
    }

    // 基于价值
    if (contact.valueScore >= 7) {
      tags.push('重要');
    }
    if (contact.hasProjectKeywords) {
      tags.push('项目相关');
    }

    // 基于时间
    const daysSinceLast = (Date.now() - new Date(contact.lastContact)) / (1000 * 60 * 60 * 24);
    if (daysSinceLast > 90) {
      tags.push('需激活');
    }

    return tags;
  }
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  const daysIndex = args.indexOf('--days');
  const outputIndex = args.indexOf('--output');

  if (daysIndex !== -1) {
    CONFIG.daysToLookBack = parseInt(args[daysIndex + 1]);
  }

  const outputFile = outputIndex !== -1 ? args[outputIndex + 1] : 'contacts.json';

  // 这里需要认证逻辑，由使用者提供
  console.log('请在代码中提供Google Auth凭证');
  console.log('使用方式：');
  console.log('1. 创建Google Cloud项目并启用Gmail API');
  console.log('2. 下载OAuth凭证文件');
  console.log('3. 在此脚本中配置auth');

  // 示例：
  // const auth = new google.auth.OAuth2(clientId, clientSecret);
  // auth.setCredentials(tokens);
  // const extractor = new ContactExtractor(auth);
  // const contacts = await extractor.extract();
  // fs.writeFileSync(outputFile, JSON.stringify(contacts, null, 2));
}

if (require.main === module) {
  main();
}

module.exports = { ContactExtractor, EmailParser };
