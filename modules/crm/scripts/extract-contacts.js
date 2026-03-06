#!/usr/bin/env node

/**
 * CRM extractor (gog-based, no custom OAuth code needed)
 * Usage:
 *   node scripts/extract-contacts.js --days 90 --max 500 --account you@gmail.com --output contacts.json
 */

const { execSync } = require('child_process');
const fs = require('fs');

const args = process.argv.slice(2);
const getArg = (name, def) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : def;
};

const DAYS = Number(getArg('--days', 90));
const MAX = Number(getArg('--max', 500));
const ACCOUNT = getArg('--account', process.env.GOG_ACCOUNT || 'haoyang056@gmail.com');
const OUTPUT = getArg('--output', 'contacts.json');

const excludeEmailPatterns = [
  /noreply@/i, /no-reply@/i, /newsletter@/i, /marketing@/i,
  /notification@/i, /alert@/i, /mailer-daemon@/i, /postmaster@/i
];
const excludeSubjectPatterns = [
  /unsubscribe/i, /promotion/i, /sale/i, /discount/i, /优惠/i, /促销/i,
  /验证码/i, /verification code/i
];
const valuableKeywords = [
  'project', '合作', '项目', 'meeting', '会议', 'contract', '合同', 'proposal', '方案'
];

function run(cmd) {
  return execSync(cmd, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
}

function parseEmail(from) {
  const m = from.match(/(?:"?([^"]*)"?\s*)?<([^>]+)>/);
  if (m) return { name: (m[1] || '').trim(), email: m[2].toLowerCase() };
  return { name: '', email: (from || '').trim().toLowerCase() };
}

function isExcluded(from, subject) {
  return excludeEmailPatterns.some(r => r.test(from || '')) ||
         excludeSubjectPatterns.some(r => r.test(subject || ''));
}

function score(record) {
  let s = 1;
  if (record.interactionCount >= 2) s += 2;
  if (record.interactionCount >= 5) s += 1;
  const text = `${record.subjects.join(' ')} ${record.lastSubject || ''}`.toLowerCase();
  if (valuableKeywords.some(k => text.includes(k.toLowerCase()))) s += 2;
  if (!/noreply|notification|alert/i.test(record.email)) s += 1;
  return Math.min(10, s);
}

function main() {
  const q = `newer_than:${DAYS}d -category:promotions -category:social`;
  const cmd = `gog gmail messages search '${q}' --max ${MAX} --json --account ${ACCOUNT}`;
  const raw = run(cmd);
  const data = JSON.parse(raw);
  const messages = data.messages || [];

  const contacts = new Map();

  for (const m of messages) {
    const from = m.from || '';
    const subject = m.subject || '';
    if (isExcluded(from, subject)) continue;

    const { name, email } = parseEmail(from);
    if (!email || email.length < 3) continue;

    const row = contacts.get(email) || {
      email,
      name,
      interactionCount: 0,
      firstSeen: m.date || '',
      lastSeen: m.date || '',
      subjects: [],
      lastSubject: ''
    };

    row.interactionCount += 1;
    row.lastSeen = m.date || row.lastSeen;
    row.lastSubject = subject || row.lastSubject;
    if (subject && row.subjects.length < 5 && !row.subjects.includes(subject)) row.subjects.push(subject);
    if (!row.name && name) row.name = name;

    contacts.set(email, row);
  }

  const out = [...contacts.values()].map(c => ({
    ...c,
    valueScore: score(c),
    tags: [c.valueScore >= 6 ? '重要' : '一般', c.interactionCount >= 3 ? '活跃' : '低频']
  })).sort((a, b) => b.valueScore - a.valueScore || b.interactionCount - a.interactionCount);

  fs.writeFileSync(OUTPUT, JSON.stringify({
    generatedAt: new Date().toISOString(),
    account: ACCOUNT,
    days: DAYS,
    totalMessages: messages.length,
    totalContacts: out.length,
    contacts: out
  }, null, 2));

  console.log(`✅ Extracted ${out.length} contacts from ${messages.length} emails -> ${OUTPUT}`);
}

main();
