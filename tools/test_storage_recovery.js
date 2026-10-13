'use strict';
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'app', 'src', 'main', 'assets', 'index.html'), 'utf8');

function extract(startMarker, endMarker) {
  const start = html.indexOf(startMarker);
  const end = html.indexOf(endMarker, start);
  assert(start >= 0 && end > start, 'storage function markers must exist');
  return html.slice(start, end);
}

const storageCode = [
  extract('function loadState(){', '\nfunction persist(){'),
  extract('function persist(){', '\nfunction updateRecoveryNotice(){')
].join('\n');

function makeHarness(raw, failWrites = false, failPrimaryWrites = false) {
  const key = 'shadow-system-test';
  const store = new Map([[key, raw]]);
  const localStorage = {
    getItem(name) { return store.has(name) ? store.get(name) : null; },
    setItem(name, value) {
      if (failWrites || (failPrimaryWrites && name === key)) throw new Error('simulated storage quota');
      store.set(name, String(value));
    }
  };
  const context = {
    KEY: key,
    RECOVERY_KEY_SUFFIX: ':recovery',
    recoveredSave: null,
    recoveryBackupUnavailable: false,
    recoveryWarningShown: false,
    DAYS: 90,
    TASKS: Array(5).fill(null),
    defaults: () => ({ version: 19, grid: Array(450).fill(false), stats: {}, settings: {} }),
    localStorage,
    state: { version: 19 },
    toast() {},
    updateRecoveryNotice() {}
  };
  vm.createContext(context);
  vm.runInContext(storageCode, context);
  return { context, store, key };
}

const corrupt = '{"version":19,,}';
const preserved = makeHarness(corrupt);
const loaded = vm.runInContext('loadState()', preserved.context);
assert.strictEqual(loaded.version, 19);
assert.strictEqual(preserved.store.get(preserved.key + ':recovery'), corrupt);
assert.strictEqual(preserved.context.recoveredSave, corrupt);
assert.strictEqual(preserved.context.recoveryBackupUnavailable, false);
console.log('PASS corrupt save is copied before defaults are used');

const blocked = makeHarness(corrupt, true);
vm.runInContext('loadState()', blocked.context);
const saved = vm.runInContext('persist()', blocked.context);
assert.strictEqual(saved, false);
assert.strictEqual(blocked.store.get(blocked.key), corrupt);
assert.strictEqual(blocked.context.recoveryBackupUnavailable, true);
console.log('PASS saving remains blocked when a recovery copy cannot be stored');
const original = JSON.stringify({ version: 19, grid: Array(450).fill(false) });
const quota = makeHarness(original, false, true);
quota.context.state = vm.runInContext('loadState()', quota.context);
const quotaSaved = vm.runInContext('persist()', quota.context);
assert.strictEqual(quotaSaved, false);
assert.strictEqual(quota.context.recoveryBackupUnavailable, true);
assert.ok(quota.store.has(quota.key + ':recovery'));
assert.strictEqual(quota.store.get(quota.key), original);
console.log('PASS saving pauses after a storage failure while preserving the last in-memory state');