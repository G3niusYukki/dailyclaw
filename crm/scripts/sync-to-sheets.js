#!/usr/bin/env node

/**
 * 同步联系人到Google Sheets
 * 将提取的联系人数据写入CRM Spreadsheet
 */

const fs = require('fs');
const { google } = require('googleapis');

class CRMSyncer {
  constructor(auth, spreadsheetId) {
    this.sheets = google.sheets({ version: 'v4', auth });
    this.spreadsheetId = spreadsheetId;
  }

  async init() {
    // 检查并创建必要的sheets
    const sheets = ['Contacts', 'Conversations', 'Tags'];
    
    for (const sheetName of sheets) {
      try {
        await this.sheets.spreadsheets.values.get({
          spreadsheetId: this.spreadsheetId,
          range: `${sheetName}!A1:A1`
        });
      } catch (error) {
        if (error.code === 400) {
          // Sheet不存在，创建它
          await this.createSheet(sheetName);
        }
      }
    }
  }

  async createSheet(sheetName) {
    if (sheetName === 'Contacts') {
      await this.sheets.spreadsheets.values.update({
        spreadsheetId: this.spreadsheetId,
        range: 'Contacts!A1:N1',
        valueInputOption: 'USER_ENTERED',
        requestBody: {
          values: [[
            'Email',
            'Name',
            'Company',
            'Title',
            'First Contact',
            'Last Contact',
            'Interaction Count',
            'Value Score',
            'Tags',
            'Notes',
            'Source',
            'Thread Count',
            'Auto Tags',
            'Updated At'
          ]]
        }
      });
    }
  }

  async syncContacts(contacts) {
    console.log(`开始同步 ${contacts.length} 个联系人...`);

    // 获取现有联系人
    const existing = await this.getExistingContacts();
    const existingEmails = new Set(existing.map(c => c.email));

    const toInsert = [];
    const toUpdate = [];

    for (const contact of contacts) {
      if (existingEmails.has(contact.email)) {
        toUpdate.push(contact);
      } else {
        toInsert.push(contact);
      }
    }

    // 插入新联系人
    if (toInsert.length > 0) {
      await this.insertContacts(toInsert);
      console.log(`✓ 新增 ${toInsert.length} 个联系人`);
    }

    // 更新现有联系人
    if (toUpdate.length > 0) {
      await this.updateContacts(toUpdate, existing);
      console.log(`✓ 更新 ${toUpdate.length} 个联系人`);
    }
  }

  async getExistingContacts() {
    const response = await this.sheets.spreadsheets.values.get({
      spreadsheetId: this.spreadsheetId,
      range: 'Contacts!A2:N'
    });

    const rows = response.data.values || [];
    return rows.map(row => ({
      email: row[0],
      name: row[1],
      company: row[2],
      title: row[3],
      firstContact: row[4],
      lastContact: row[5],
      interactionCount: parseInt(row[6]) || 0,
      valueScore: parseInt(row[7]) || 1,
      tags: row[8] || '',
      notes: row[9] || '',
      source: row[10] || 'email',
      threadCount: parseInt(row[11]) || 0,
      autoTags: row[12] || '',
      updatedAt: row[13],
      rowIndex: rows.indexOf(row) + 2
    }));
  }

  async insertContacts(contacts) {
    const values = contacts.map(c => [
      c.email,
      c.name,
      c.company || '',
      c.title || '',
      c.firstContact.toISOString().split('T')[0],
      c.lastContact.toISOString().split('T')[0],
      c.interactionCount,
      c.valueScore,
      c.autoTags.join(', '),
      c.snippets ? c.snippets.join(' | ') : '',
      'email',
      c.threadCount,
      c.autoTags.join(', '),
      new Date().toISOString()
    ]);

    await this.sheets.spreadsheets.values.append({
      spreadsheetId: this.spreadsheetId,
      range: 'Contacts!A:N',
      valueInputOption: 'USER_ENTERED',
      insertDataOption: 'INSERT_ROWS',
      requestBody: { values }
    });
  }

  async updateContacts(contacts, existing) {
    // 批量更新
    for (const contact of contacts) {
      const existingContact = existing.find(e => e.email === contact.email);
      if (!existingContact) continue;

      const rowIndex = existingContact.rowIndex;
      
      // 只更新变化的字段
      const updatedData = [
        existingContact.email,
        contact.name || existingContact.name,
        existingContact.company,
        existingContact.title,
        existingContact.firstContact,
        contact.lastContact.toISOString().split('T')[0],
        Math.max(existingContact.interactionCount, contact.interactionCount),
        Math.max(existingContact.valueScore, contact.valueScore),
        existingContact.tags,
        existingContact.notes,
        existingContact.source,
        existingContact.threadCount + contact.threadCount,
        contact.autoTags.join(', '),
        new Date().toISOString()
      ];

      await this.sheets.spreadsheets.values.update({
        spreadsheetId: this.spreadsheetId,
        range: `Contacts!A${rowIndex}:N${rowIndex}`,
        valueInputOption: 'USER_ENTERED',
        requestBody: { values: [updatedData] }
      });
    }
  }
}

module.exports = { CRMSyncer };
