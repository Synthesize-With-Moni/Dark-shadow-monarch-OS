'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { prepareFrontend } = require('../desktop/prepare-frontend.cjs');

const root = path.resolve(__dirname, '..');
const dashboardJs = fs.readFileSync(path.join(root, 'desktop', 'desktop-dashboard.js'), 'utf8');
const dashboardCss = fs.readFileSync(path.join(root, 'desktop', 'desktop-dashboard.css'), 'utf8');
new Function(dashboardJs);
assert.match(dashboardJs, /data-task-index/);
assert.match(dashboardJs, /closest\('#desktopTasks \[data-task-index\]'\)/);
assert.match(dashboardJs, /setTask\(protocolDay\(\), Number\(taskButton\.dataset\.taskIndex\)\)/);
assert.match(dashboardJs, /closest\('#desktopSideQuests \[data-quest-index\]'\)/);
assert.match(dashboardJs, /toggleCustomDeep\(Number\(questButton\.dataset\.questIndex\), protocolDay\(\)\)/);
assert.match(dashboardJs, /desktopQuestCadence/);
assert.match(dashboardJs, /desktopQuestReward/);
assert.match(dashboardJs, /forgeQuestDeep\(\)/);
assert.match(dashboardJs, /saveDesktopJournal/);
assert.match(dashboardJs, /toggleTimer\(\)/);
assert.match(dashboardJs, /window\.switchSystemScreen/);
assert.match(dashboardJs, /state\.events/);
assert.match(dashboardCss, /#desktopDashboard\.screen-visible/);
assert.match(dashboardCss, /@media \(prefers-reduced-motion: reduce\)/);
assert.doesNotMatch(dashboardCss, /nav-item\[data-screen="(?:world|arc|ascension)"\][^\n]*display:\s*none/);
for (const route of ['world', 'arc', 'ascension']) assert.match(dashboardJs, new RegExp(route + ':'));
const appHtml = fs.readFileSync(path.join(root, 'app', 'src', 'main', 'assets', 'index.html'), 'utf8');
assert.match(appHtml, /id="questCadenceSetting"/);
assert.match(appHtml, /id="questRewardSetting"/);
assert.match(appHtml, /function questDateKey\(day\)\{return addDaysISO\(state\.arcStartDate,Number\(day\)\|\|0\)\}/);
assert.match(appHtml, /toggleCustomDeep\(\$\{i\},protocolDay\(\)\)/);
assert.match(appHtml, /completionRewards\[key\]=\{xp,essence:10,proofs:1\}/);
assert.match(appHtml, /state\.essence=Math\.max\(0,\(state\.essence\|\|0\)-Math\.max\(0,Number\(reward\.essence\)\|\|0\)\)/);
assert.match(appHtml, /function restoreArchivedQuestSetting\(index\)/);
assert.match(appHtml, /state\.archivedQuests\.push\(Object\.assign\(\{\},q,\{enabled:false,archivedAt:/);
assert.doesNotMatch(appHtml, /Number\(q\.xp\)\|\|20/);

const fixture = fs.mkdtempSync(path.join(os.tmpdir(), 'shadow-desktop-'));
try {
  const source = path.join(fixture, 'app', 'src', 'main', 'assets');
  const desktop = path.join(fixture, 'desktop');
  fs.mkdirSync(path.join(source, 'assets'), { recursive: true });
  fs.mkdirSync(desktop, { recursive: true });
  const originalHtml = '<!doctype html><html><head></head><body><main>Change 19</main></body></html>';
  fs.writeFileSync(path.join(source, 'index.html'), originalHtml);
  fs.writeFileSync(path.join(source, 'assets', 'sample.webp'), 'asset');
  fs.writeFileSync(path.join(desktop, 'desktop-dashboard.css'), '/* desktop only */');
  fs.writeFileSync(path.join(desktop, 'desktop-dashboard.js'), '/* desktop only */');
  const result = prepareFrontend(fixture);
  const generatedHtml = fs.readFileSync(path.join(result.output, 'index.html'), 'utf8');
  assert.match(generatedHtml, /desktop-dashboard\.css/);
  assert.match(generatedHtml, /desktop-dashboard\.js/);
  assert.equal(fs.readFileSync(path.join(source, 'index.html'), 'utf8'), originalHtml, 'Android source remains unchanged');
  assert.equal(fs.readFileSync(path.join(result.output, 'assets', 'sample.webp'), 'utf8'), 'asset', 'bundled assets are copied');
  assert.equal(fs.readFileSync(path.join(result.output, 'desktop-dashboard.js'), 'utf8'), '/* desktop only */');
} finally {
  fs.rmSync(fixture, { recursive: true, force: true });
}

console.log('DESKTOP FRONTEND TEST PASS — dashboard actions parse and the generated Windows copy stays separate from Android.');
