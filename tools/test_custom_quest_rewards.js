'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const html = fs.readFileSync(require('node:path').join(__dirname, '..', 'app', 'src', 'main', 'assets', 'index.html'), 'utf8');
const start = html.indexOf('function toggleCustomDeep(');
const end = html.indexOf('\ntoggleCustom=toggleCustomDeep;', start);
assert.ok(start >= 0 && end > start, 'custom quest toggle exists in the Change 19 source');
const source = html.slice(start, end);

const context = {
  state: {
    customQuests: [], xp: 200, essence: 40, proofs: 12, level: 1,
    settings: { multiplier: 1 }
  },
  requireArcStart: () => true,
  isCustomQuestDone: (quest, day) => quest.cadence === 'once'
    ? !!quest.done
    : Array.isArray(quest.completions) && quest.completions.includes(quest.cadence + ':' + day),
  questPeriodKey: (quest, day) => quest.cadence + ':' + day,
  addEvent: () => {},
  toast: () => {},
  levelFromXP: () => 1,
  persist: () => {},
  renderAll: () => {}
};
vm.createContext(context);
vm.runInContext(source + '\nglobalThis.testToggle = toggleCustomDeep;', context);

const quest = { id: 'zero-xp', cadence: 'daily', xp: 0, enabled: true, completions: [], completionRewards: {} };
context.state.customQuests.push(quest);
context.testToggle(0, 3);
assert.equal(context.state.xp, 200, 'zero-XP quest awards no XP');
assert.equal(context.state.essence, 50, 'quest awards Essence once');
assert.equal(context.state.proofs, 13, 'quest awards one proof once');
assert.equal(quest.completionRewards['daily:3'].xp, 0, 'zero XP is recorded without falling back to a default');

quest.xp = 80;
context.testToggle(0, 3);
assert.equal(context.state.xp, 200, 'undo uses the originally recorded zero XP after the definition changes');
assert.equal(context.state.essence, 40, 'undo reverses the recorded Essence');
assert.equal(context.state.proofs, 12, 'undo reverses the recorded proof');
assert.equal(quest.completions.length, 0, 'recurring completion is removed');

const paidQuest = { id: 'paid', cadence: 'weekly', xp: 35, enabled: true, completions: [], completionRewards: {} };
context.state.customQuests.push(paidQuest);
context.testToggle(1, 8);
assert.equal(context.state.xp, 235, 'configured XP is awarded');
paidQuest.xp = 70;
context.testToggle(1, 8);
assert.equal(context.state.xp, 200, 'undo removes the amount earned before the edit');
assert.equal(context.state.essence, 40, 'weekly quest undo restores Essence');
assert.equal(context.state.proofs, 12, 'weekly quest undo restores proof count');

console.log('CUSTOM QUEST REWARD TEST PASS — zero, edited, and recurring rewards complete and undo without reward drift.');
