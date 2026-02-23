#!/usr/bin/env node

/**
 * Sync contacts.json -> Google Sheets using gog CLI
 * Usage:
 *   node scripts/sync-to-sheets.js --sheet <SPREADSHEET_ID> --input contacts.json
 */

const fs = require('fs');
const { execSync } = require('child_process');

const args = process.argv.slice(2);
const getArg = (name, def) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : def;
};

const SHEET_ID = getArg('--sheet', process.env.SPREADSHEET_ID || '');
const INPUT = getArg('--input', 'contacts.json');

if (!SHEET_ID) {
  console.error('❌ Missing --sheet <SPREADSHEET_ID>');
  process.exit(1);
}

if (!fs.existsSync(INPUT)) {
  console.error(`❌ Input not found: ${INPUT}`);
  process.exit(1);
}

const data = JSON.parse(fs.readFileSync(INPUT, 'utf8'));
const contacts = data.contacts || [];

const headers = [[
  'Email', 'Name', 'Interaction Count', 'First Seen', 'Last Seen',
  'Value Score', 'Tags', 'Last Subject'
]];

const rows = contacts.map(c => [
  c.email || '',
  c.name || '',
  c.interactionCount || 0,
  c.firstSeen || '',
  c.lastSeen || '',
  c.valueScore || 0,
  (c.tags || []).join(', '),
  c.lastSubject || ''
]);

function run(cmd) {
  return execSync(cmd, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
}

function q(json) {
  return JSON.stringify(json).replace(/'/g, "'\\''");
}

try {
  // Use default first tab (Sheet1) for maximum compatibility
  run(`gog sheets clear ${SHEET_ID} "Sheet1!A:Z"`);
  run(`gog sheets update ${SHEET_ID} "Sheet1!A1:H1" --values-json '${q(headers)}' --input USER_ENTERED`);

  if (rows.length > 0) {
    run(`gog sheets append ${SHEET_ID} "Sheet1!A:H" --values-json '${q(rows)}' --insert INSERT_ROWS`);
  }

  console.log(`✅ Synced ${rows.length} contacts to https://docs.google.com/spreadsheets/d/${SHEET_ID}/edit#gid=0`);
} catch (e) {
  console.error('❌ Sync failed');
  console.error(e.stderr?.toString() || e.message);
  process.exit(1);
}
