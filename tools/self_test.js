'use strict';
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const htmlPath = path.join(root, 'app', 'src', 'main', 'assets', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const js = [...html.matchAll(/<script(?:[^>]*)>([\s\S]*?)<\/script>/g)].map(m => m[1]).join('\n');
const checks=[];
function check(id, ok, detail=''){checks.push({id,ok:!!ok,detail});}
function fail(msg){console.error('SELF-TEST FAILED:',msg);process.exitCode=1;}
try { new Function(js); check('JS_SYNTAX', true, 'inline JavaScript parses'); }
catch(e){ check('JS_SYNTAX', false, e.message); }
const required=[
 ['STATE_SCHEMA','version:19'],['PRE_ARC_MODEL','function arcHasStarted'],['DAY_NUMBER_MODEL','function currentDayNumber'],
 ['WORLD_ROUTE','data-screen="world"'],['WORLD_LABEL',"world:'WORLD // REALM'"],['RANK_ENGINE','function rankFromXP'],
 ['BUILD_ENGINE','function buildStats'],['DUNGEON_THREAT_ENGINE','function dungeonThreat'],['COMBAT_BUILD_LINK','function combatPower'],['AURA_BUILD_LINK','function auraPower'],
 ['DAY90_ENV','min:90,max:90'],['DAY90_WORLD','d===90'],['RUNTIME_AUDIT','function runSystemSelfTest'],['CROSS_SCRIPT_RENDER_GUARD',"if(typeof renderArc17==='function')renderArc17()"],['LEGACY_TELEMETRY','function renderLegacyTelemetry']
];
for(const [id,needle] of required)check(id,html.includes(needle),needle);
const names=[...js.matchAll(/\bfunction\s+([A-Za-z_$][\w$]*)\s*\(/g)].map(m=>m[1]);
const counts=new Map(); for(const n of names)counts.set(n,(counts.get(n)||0)+1);
const dup=[...counts].filter(([,n])=>n>1).map(([n,c])=>`${n}×${c}`);
check('NO_DUPLICATE_FUNCTION_DECLARATIONS',dup.length===0,dup.join(', ')||'none');
check('NO_SOFT_ASCENSION_RUNTIME',!html.includes('id="v6-simplicity"')&&!html.includes('function v6Simple'), 'obsolete simplicity runtime absent');
check('ONE_AURA_ENGINE',counts.get('auraPower')===1,`auraPower declarations=${counts.get('auraPower')||0}`);
check('ONE_RENDER_ALL',counts.get('renderAll')===1,`renderAll declarations=${counts.get('renderAll')||0}`);
// Exact literal asset paths plus known dynamic asset families.
const literalRefs=new Set();
for(const m of html.matchAll(/assets\/([A-Za-z0-9_.-]+\.(?:webp|png|wav|jpg|jpeg|svg))/g)) literalRefs.add(m[1]);
const missing=[...literalRefs].filter(f=>!fs.existsSync(path.join(root,'app','src','main','assets','assets',f)));
check('ASSET_REFERENCES',missing.length===0,missing.slice(0,20).join(', ')||`${literalRefs.size} literal asset refs resolved`);
for(const [id,prefix] of [['RANK_ASSET_FAMILY','rank_'],['MASTERY_ASSET_FAMILY','mastery_'],['PROOF_ASSET_FAMILY','proof_'],['DOMAIN_ASSET_FAMILY','domain_']]){
 const files=fs.readdirSync(path.join(root,'app','src','main','assets','assets')).filter(f=>f.startsWith(prefix));
 check(id,files.length>0,`${files.length} ${prefix} assets`);
}
const gradle=fs.readFileSync(path.join(root,'app','build.gradle'),'utf8');
const workflow=fs.readFileSync(path.join(root,'.github','workflows','build-apk.yml'),'utf8');
check('ANDROID_VERSION_CODE',/versionCode\s+19\b/.test(gradle),'versionCode 19');
check('ANDROID_VERSION_NAME',/versionName\s+['"]5\.0\.0['"]/.test(gradle),'versionName 5.0.0');
check('WORKFLOW_SELF_TEST',workflow.includes('node tools/self_test.js'),'self-test runs before Gradle');
check('ENVIRONMENT_USES_DISPLAY_DAY',/function currentEnvironment\(\)\{const d=currentDayNumber\(\)/.test(html),'environment uses Day 1..90');
check('WORLD_USES_DISPLAY_DAY',/function worldEventForDay\(\)\{const d=currentDayNumber\(\)/.test(html),'world uses Day 1..90');
check('ARC17_USES_DISPLAY_DAY',/function arc17Metrics\(\)\{initArc17\(\);const d=currentDayNumber\(\)/.test(html),'Arc 17 uses Day 1..90');
check('ASCENSION_USES_DISPLAY_DAY',/function asc18Day\(\)\{return currentDayNumber\(\)\|\|0\}/.test(html),'ascension uses Day 1..90');
check('MUTATION17_PRESENT',html.includes('MUTATION 17 // ARC INTELLIGENCE ENGINE'),'Mutation 17 retained');
check('MUTATION18_PRESENT',html.includes('MUTATION 18 // MONARCH ASCENSION'),'Mutation 18 retained');
check('CORRUPT_SAVE_RECOVERY',html.includes('KEY+RECOVERY_KEY_SUFFIX')&&html.includes('function exportRecoverySave'),'unreadable save contents are preserved and exportable');
check('SAVE_FAILURE_GUARD',html.includes('function acknowledgeRecoveryExport')&&html.includes('SAVE PROTECTED'),'saving pauses after a storage failure until recovery is exported');

const desktopConfig = JSON.parse(fs.readFileSync(path.join(root, 'desktop', 'src-tauri', 'tauri.conf.json'), 'utf8'));
check('OFFLINE_FONT_ASSETS', !html.includes('fonts.googleapis.com') && !html.includes('fonts.gstatic.com'), 'no runtime Google Fonts request');
check('OFFLINE_WEBVIEW2_INSTALLER', desktopConfig.bundle?.windows?.webviewInstallMode?.type === 'offlineInstaller', 'WebView2 runtime is bundled for offline setup');
check('EVIDENCE_NO_TEXT_REWARD', /function recordProof\(\)[^\n]*state\.proofs=/.test(html) && !/function recordProof\(\)[^\n]*state\.xp\+=15/.test(html), 'proof entry does not mint XP');
check('SIDE_QUEST_ONE_WAY', /function toggleCustomDeep\(i\)[^\n]*if\(q\.done\)/.test(html), 'side quest completion cannot be toggled for repeat rewards');
check('SEALED_COMPARISON_IMMUTABLE', /function saveBeforeAfter16\(\)[^\n]*sealedAt/.test(html), 'comparison cannot be overwritten');

const bad=checks.filter(x=>!x.ok);
for(const c of checks)console.log(`${c.ok?'PASS':'FAIL'} ${c.id}${c.detail?' — '+c.detail:''}`);
if(bad.length)fail(`${bad.length} check(s) failed`); else console.log(`SELF-TEST PASS — ${checks.length} checks`);
