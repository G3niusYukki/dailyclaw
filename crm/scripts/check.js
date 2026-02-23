#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');

function ok(msg) { console.log(`✅ ${msg}`); }
function warn(msg) { console.log(`⚠️  ${msg}`); }

try {
  const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  ok(`package.json loaded (${pkg.name}@${pkg.version})`);
} catch (e) {
  console.error('❌ package.json invalid');
  process.exit(1);
}

for (const f of ['scripts/extract-contacts.js', 'scripts/sync-to-sheets.js', 'config.json']) {
  if (fs.existsSync(f)) ok(`${f} exists`);
  else {
    console.error(`❌ missing ${f}`);
    process.exit(1);
  }
}

try {
  const out = execSync('gog auth list', { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
  if (out) ok('gog auth detected');
  else warn('gog auth list returned empty');
} catch (e) {
  warn('gog not ready or needs approval/auth');
}

console.log('CRM local deploy check complete.');
