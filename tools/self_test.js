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
 ['ROUTER_SEPARATES_SHADOW_SCREENS',".layout .card.section:not(.shadow-screen)"],
 ['BUILD_ENGINE','function buildStats'],['DUNGEON_THREAT_ENGINE','function dungeonThreat'],['COMBAT_BUILD_LINK','function combatPower'],['AURA_BUILD_LINK','function auraPower'],
 ['DAY90_ENV','min:90,max:90'],['DAY90_WORLD','d===90'],['RUNTIME_AUDIT','function runSystemSelfTest'],['CROSS_SCRIPT_RENDER_GUARD',"if(typeof renderArc17==='function')renderArc17()"],['LEGACY_TELEMETRY','function renderLegacyTelemetry']
];
for(const [id,needle] of required)check(id,html.includes(needle),needle);
// Run the actual screen router against a tiny DOM double. This catches a
// regression where the newer mutation screens are hidden by the legacy route.
try {
 const makeEl=(dataset={})=>({dataset,classList:{values:new Set(),toggle(name,on){on?this.values.add(name):this.values.delete(name);},contains(name){return this.values.has(name);}},handlers:{},addEventListener(name,fn){this.handlers[name]=fn;},querySelector(){return null;},scrollTo(){}});
 const nav=[...['home','quests','dungeon','skills','character','world','inventory','arc','vault','ascension','more'].map(screen=>makeEl({screen}))];
 const shadow=[...['dungeon','skills','vault','world','inventory','ascension'].map(shadowScreen=>makeEl({shadowScreen}))];
 const legacy=[makeEl({})],side=makeEl(),layout=makeEl(),body=makeEl();
 const doc={body,querySelectorAll(selector){if(selector==='.nav-item[data-screen]')return nav;if(selector==='.layout .card.section:not(.shadow-screen)')return legacy;if(selector==='.shadow-screen')return shadow;return[];},querySelector(selector){if(selector==='.layout .sidecol')return side;if(selector==='.app>.layout')return layout;return null;},getElementById(){return null;}};
 const start=js.indexOf('(function initSystemRouter(){'),end=js.indexOf('})();',start)+5;
 const router=js.slice(start,end).replace('window.switchSystemScreen=function(name){','switchSystemScreen=function(name){window.switchSystemScreen=switchSystemScreen;');
 new Function('document','window','switchSystemScreen',router)(doc,{},undefined);
 for(const screen of ['dungeon','skills','vault','world','inventory','ascension']){
   nav.find(x=>x.dataset.screen===screen).handlers.click();
   const target=shadow.find(x=>x.dataset.shadowScreen===screen);
   if(!target.classList.contains('screen-visible')||target.classList.contains('screen-hidden'))throw Error(`${screen} screen is not visible after navigation`);
 }
 check('ROUTER_SHADOW_DESTINATIONS_CLICKABLE',true,'all six mutation screens become visible when selected');
} catch(e) { check('ROUTER_SHADOW_DESTINATIONS_CLICKABLE',false,e.message); }
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
const rewardFree=['equipGear14','saveLoadout','recordProof','createProject16','addEvidence16','saveBeforeAfter16','sealReflection17'].every(name=>{const line=html.match(new RegExp('function '+name+'\\([^\\r\\n]*'))?.[0]||'';return line&&!/state\.(?:xp|essence)\s*\+=/.test(line)});
check('NO_REWARD_FOR_RECORDING_OR_SAVING',rewardFree,'evidence, reflections, projects, and equipment cannot mint progression rewards');
check('SEALED_RECORDS_IMMUTABLE',/function saveBeforeAfter16\([^\r\n]*sealedAt/.test(html)&&/function sealReflection17\([^\r\n]*reflections\[ch\]/.test(html),'sealed comparisons and chapter reflections cannot be overwritten');
const desktopConfig=JSON.parse(fs.readFileSync(path.join(root,'desktop','src-tauri','tauri.conf.json'),'utf8'));
check('OFFLINE_ASSETS',!html.includes('fonts.googleapis.com')&&!html.includes('fonts.gstatic.com')&&desktopConfig.bundle?.windows?.webviewInstallMode?.type==='offlineInstaller','no remote fonts; WebView2 offline runtime is bundled');

const bad=checks.filter(x=>!x.ok);
for(const c of checks)console.log(`${c.ok?'PASS':'FAIL'} ${c.id}${c.detail?' — '+c.detail:''}`);
if(bad.length)fail(`${bad.length} check(s) failed`); else console.log(`SELF-TEST PASS — ${checks.length} checks`);
