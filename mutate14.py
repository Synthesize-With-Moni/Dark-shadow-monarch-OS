from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import random, math, zipfile, os, re
root=Path(__file__).parent
html=root/'app/src/main/assets/index.html'
assets=root/'app/src/main/assets/assets'
random.seed(1414)
assets.mkdir(parents=True,exist_ok=True)

def make_item(name, seed, accent):
    random.seed(seed); W=900; H=900
    im=Image.new('RGB',(W,H),(4,3,10)); p=im.load()
    for y in range(H):
      for x in range(W):
        r=math.hypot(x-W/2,y-H/2)/(W*.72)
        glow=max(0,1-r)
        noise=random.random()*7
        p[x,y]=(int(5+accent[0]*glow+noise),int(3+accent[1]*glow+noise/2),int(10+accent[2]*glow+noise))
    d=ImageDraw.Draw(im,'RGBA')
    # radial rings / shards
    for rr in range(120,430,52): d.ellipse((W/2-rr,H/2-rr,W/2+rr,H/2+rr),outline=(*accent,35),width=3)
    for i in range(22):
      ang=random.random()*math.tau; length=random.randint(180,380); cx,cy=W/2,H/2
      x2=cx+math.cos(ang)*length; y2=cy+math.sin(ang)*length
      d.line((cx,cy,x2,y2),fill=(*accent,random.randint(40,110)),width=random.randint(2,8))
    # central sigil
    d.polygon([(450,180),(585,330),(540,610),(450,730),(360,610),(315,330)],outline=(*accent,190),fill=(10,6,20,100),width=8)
    d.ellipse((385,385,515,515),outline=(255,255,255,170),width=5)
    d.text((40,820),name,fill=(235,230,250,210))
    im=im.filter(ImageFilter.GaussianBlur(0.35)); im.save(assets/f'equipment_{name.lower().replace(" ","_")}.webp',quality=88,method=6)

items=[('void_blade',31,(140,100,255)),('eclipse_core',32,(110,180,255)),('night_mantle',33,(190,90,255)),('monarch_crown',34,(255,180,90)),('pressure_gauntlet',35,(255,90,110)),('focus_relic',36,(100,240,210)),('shadow_boots',37,(160,110,240)),('proof_sigil',38,(240,220,120))]
for n,s,c in items: make_item(n.replace('_',' ').upper(),s,c)

text=html.read_text()
# Add CSS once
css='''\n<style>\n/* MUTATION 14 // EQUIPMENT + BUILD FORGE */\n.build-forge{display:grid;grid-template-columns:1.15fr .85fr;gap:14px;margin-top:14px}.loadout-panel,.affix-panel,.set-panel{padding:16px;border:1px solid rgba(150,110,255,.18);border-radius:18px;background:rgba(255,255,255,.025)}.loadout-tabs{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:12px}.loadout-tab{padding:8px 10px;border-radius:12px;border:1px solid rgba(255,255,255,.1);background:rgba(255,255,255,.03);font:700 9px Orbitron;cursor:pointer}.loadout-tab.active{border-color:rgba(160,120,255,.55);background:rgba(130,90,255,.1)}.gear-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}.gear-slot{min-height:132px;border:1px solid rgba(255,255,255,.08);border-radius:15px;padding:9px;background:rgba(0,0,0,.18);position:relative}.gear-slot img{width:100%;height:72px;object-fit:cover;border-radius:10px;opacity:.9}.gear-slot b{display:block;font-size:9px;margin-top:6px}.gear-slot small{color:#887f99;font-size:8px}.gear-slot.active{border-color:rgba(150,110,255,.55);box-shadow:0 0 24px rgba(120,80,220,.12)}.build-stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:12px}.build-stat{padding:10px;border-radius:13px;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.06)}.build-stat span{display:block;color:#81788f;font:700 8px 'DM Mono';letter-spacing:.12em}.build-stat b{display:block;font:800 17px Orbitron;margin-top:4px}.affix-list{display:grid;gap:7px;margin-top:10px}.affix{padding:9px 10px;border-left:2px solid rgba(160,120,255,.55);background:rgba(255,255,255,.025);border-radius:9px;font-size:10px}.set-progress{display:flex;align-items:center;gap:10px;margin-top:10px}.set-progress .bar{flex:1}.loadout-actions{display:flex;gap:7px;flex-wrap:wrap;margin-top:12px}.build-summary{margin-top:12px;padding:12px;border-radius:14px;background:linear-gradient(135deg,rgba(120,80,220,.08),rgba(255,255,255,.02));border:1px solid rgba(150,110,255,.16);font-size:10px;line-height:1.6;color:#bdb3cb}.gear-codex{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin-top:14px}.gear-codex .codex-item{padding:9px;border:1px solid rgba(255,255,255,.07);border-radius:14px;background:rgba(255,255,255,.02)}.codex-item img{width:100%;height:85px;object-fit:cover;border-radius:10px}.codex-item b{font-size:9px;display:block;margin-top:6px}.codex-item small{color:#81788f;font-size:8px}.build-rank{font:800 11px Orbitron;color:#c9b7ff;letter-spacing:.12em}.synergy{color:#86f7d2;font-size:9px;margin-top:5px}\n@media(max-width:850px){.build-forge{grid-template-columns:1fr}.gear-grid,.gear-codex{grid-template-columns:repeat(2,1fr)}}\n</style>\n'''
text=text.replace('</head>',css+'</head>',1)
# Insert build forge into inventory before proof vault
marker='<div class="proof-vault">'
block='''<div class="build-forge">\n<div class="loadout-panel"><div class="section-head"><div><div class="section-title">BUILD FORGE</div><div class="section-sub">Equipment changes capability, not just appearance.</div></div><span class="v6-chip" id="buildRankChip">E BUILD</span></div><div class="loadout-tabs" id="loadoutTabs"></div><div class="gear-grid" id="gearGrid"></div><div class="build-stat-grid"><div class="build-stat"><span>POWER</span><b id="buildPower">0</b></div><div class="build-stat"><span>AURA</span><b id="buildAura">0</b></div><div class="build-stat"><span>RESILIENCE</span><b id="buildResilience">0</b></div><div class="build-stat"><span>FOCUS</span><b id="buildFocus">0</b></div><div class="build-stat"><span>EXECUTION</span><b id="buildExecution">0</b></div><div class="build-stat"><span>SYNERGY</span><b id="buildSynergy">0%</b></div></div><div class="loadout-actions"><button class="control-btn primary" onclick="saveLoadout()">SAVE LOADOUT</button><button class="control-btn" onclick="clearLoadout()">CLEAR BUILD</button></div><div class="build-summary" id="buildSummary14">No equipment build assembled yet.</div></div>\n<div class="affix-panel"><div class="section-title">BUILD INTELLIGENCE</div><div class="section-sub">Your equipment creates a playstyle profile.</div><div class="affix-list" id="affixList14"></div><div class="set-panel" style="margin-top:10px"><div class="section-title" style="font-size:11px">SET RESONANCE</div><div class="section-sub" id="setName14">No set resonance</div><div class="set-progress"><div class="bar"><div class="fill" id="setBar14" style="width:0%"></div></div><b id="setCount14">0/3</b></div><div class="synergy" id="setBonus14">Equip matching pieces to unlock a set effect.</div></div></div>\n</div>\n<div class="gear-codex" id="gearCodex14"></div>\n'''
text=text.replace(marker,block+marker,1)
# Extend state base
text=text.replace("world:{phase:'NIGHT',weather:'CLEAR',resonance:0,corruption:0,heat:0,event:'NONE',lastEventDay:-1}","world:{phase:'NIGHT',weather:'CLEAR',resonance:0,corruption:0,heat:0,event:'NONE',lastEventDay:-1},loadouts:{active:0,sets:[{}, {}, {}]},equipmentXP:{},gearMastery:{},buildHistory:[]",1)
# load parse after world assignment
text=text.replace("s.world=Object.assign(base.world,parsed.world||{});", "s.world=Object.assign(base.world,parsed.world||{});s.loadouts=Object.assign(base.loadouts,parsed.loadouts||{});s.loadouts.sets=Array.isArray(s.loadouts.sets)?s.loadouts.sets.slice(0,3):[{}, {}, {}];while(s.loadouts.sets.length<3)s.loadouts.sets.push({});s.loadouts.active=Number(s.loadouts.active||0);s.equipmentXP=Object.assign({},parsed.equipmentXP||{});s.gearMastery=Object.assign({},parsed.gearMastery||{});s.buildHistory=Array.isArray(parsed.buildHistory)?parsed.buildHistory.slice(-30):[];",1)
# Add equipment catalog/functions before renderShadowSystems
needle='function renderShadowSystems(){'
js=r'''const GEAR14=[
{id:'void_blade',name:'VOID BLADE',slot:'WEAPON',set:'VOID HUNTER',file:'assets/equipment_void_blade.webp',power:14,aura:8,resilience:2,focus:3,execution:8,affix:'Execution damage rises after a completed core quest.'},
{id:'eclipse_core',name:'ECLIPSE CORE',slot:'CORE',set:'ECLIPSE SOVEREIGN',file:'assets/equipment_eclipse_core.webp',power:8,aura:16,resilience:5,focus:5,execution:2,affix:'Aura scales with proof and completed focus sessions.'},
{id:'night_mantle',name:'NIGHT MANTLE',slot:'ARMOR',set:'NIGHT HUNTER',file:'assets/equipment_night_mantle.webp',power:6,aura:9,resilience:15,focus:2,execution:3,affix:'Partial days reduce momentum loss by a small amount.'},
{id:'monarch_crown',name:'MONARCH CROWN',slot:'CROWN',set:'MONARCH',file:'assets/equipment_monarch_crown.webp',power:20,aura:25,resilience:8,focus:8,execution:8,affix:'Final-form artifact amplifies every equipped matching piece.'},
{id:'pressure_gauntlet',name:'PRESSURE GAUNTLET',slot:'GLOVES',set:'PRESSURE FORGE',file:'assets/equipment_pressure_gauntlet.webp',power:12,aura:3,resilience:10,focus:4,execution:15,affix:'Pressure-room completion increases Execution for the day.'},
{id:'focus_relic',name:'FOCUS RELIC',slot:'RELIC',set:'ECLIPSE SOVEREIGN',file:'assets/equipment_focus_relic.webp',power:4,aura:12,resilience:3,focus:18,execution:4,affix:'Focus sessions generate additional Essence.'},
{id:'shadow_boots',name:'SHADOW BOOTS',slot:'BOOTS',set:'NIGHT HUNTER',file:'assets/equipment_shadow_boots.webp',power:9,aura:4,resilience:8,focus:7,execution:10,affix:'Momentum decay is reduced while the build is active.'},
{id:'proof_sigil',name:'PROOF SIGIL',slot:'SIGIL',set:'PROOF ARCHIVE',file:'assets/equipment_proof_sigil.webp',power:5,aura:18,resilience:5,focus:10,execution:6,affix:'Every new proof entry contributes to build resonance.'}
];
function activeLoadout(){return (state.loadouts&&state.loadouts.sets&&state.loadouts.sets[state.loadouts.active])||{} }
function equippedGear14(){const l=activeLoadout();return GEAR14.filter(g=>l[g.slot]);}
function gearStats14(){return equippedGear14().reduce((a,g)=>{a.power+=g.power;a.aura+=g.aura;a.resilience+=g.resilience;a.focus+=g.focus;a.execution+=g.execution;return a},{power:0,aura:0,resilience:0,focus:0,execution:0})}
function gearSynergy14(){const gs=equippedGear14();const sets={};gs.forEach(g=>sets[g.set]=(sets[g.set]||0)+1);return Math.min(100,Math.round(gs.length/8*60+Object.values(sets).filter(v=>v>=2).length*8))}
function equipGear14(id){const g=GEAR14.find(x=>x.id===id);if(!g)return;state.artifacts=state.artifacts||[];if(!state.artifacts.includes(id)){state.artifacts.push(id);state.proofs=(state.proofs||0)+1;}const l=activeLoadout();if(l[g.slot]===id)delete l[g.slot];else l[g.slot]=id;state.gearMastery[id]=(state.gearMastery[id]||0)+1;state.buildHistory.unshift({time:Date.now(),gear:id,loadout:state.loadouts.active});state.buildHistory=state.buildHistory.slice(0,30);persist();renderAll();toast('BUILD FORGE',g.name+(l[g.slot]?' equipped.':' removed.'))}
function switchLoadout14(i){state.loadouts.active=Math.max(0,Math.min(2,i));persist();renderAll();}
function saveLoadout(){const l=activeLoadout();state.loadouts.sets[state.loadouts.active]=Object.assign({},l);state.essence=(state.essence||0)+12;state.buildHistory.unshift({time:Date.now(),save:true,loadout:state.loadouts.active});persist();renderAll();toast('LOADOUT SAVED','Build profile locked into slot '+(state.loadouts.active+1)+'.')}
function clearLoadout(){state.loadouts.sets[state.loadouts.active]={};persist();renderAll();toast('BUILD CLEARED','The active loadout is empty.')}
function renderBuildForge14(){
 const tabs=document.getElementById('loadoutTabs');if(tabs)tabs.innerHTML=[0,1,2].map(i=>`<button class="loadout-tab ${state.loadouts.active===i?'active':''}" onclick="switchLoadout14(${i})">LOADOUT ${i+1}</button>`).join('');
 const l=activeLoadout(),grid=document.getElementById('gearGrid');if(grid)grid.innerHTML=GEAR14.map(g=>{const equipped=l[g.slot]===g.id;return `<div class="gear-slot ${equipped?'active':''}"><img src="${g.file}" alt="${g.name}"><b>${g.name}</b><small>${g.slot} · PWR ${g.power}</small><button class="control-btn ${equipped?'primary':''}" style="margin-top:6px;font-size:9px;padding:6px 8px" onclick="equipGear14('${g.id}')">${equipped?'REMOVE':'EQUIP'}</button></div>`}).join('');
 const st=gearStats14(),sy=gearSynergy14(); const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v};set('buildPower',st.power);set('buildAura',st.aura);set('buildResilience',st.resilience);set('buildFocus',st.focus);set('buildExecution',st.execution);set('buildSynergy',sy+'%');set('buildRankChip',(rankForLevel(levelFromXP(state.xp))||'E')+' BUILD');
 const aff=document.getElementById('affixList14');if(aff){const gs=equippedGear14();aff.innerHTML=gs.length?gs.map(g=>`<div class="affix"><b>${g.name}</b><br>${g.affix}</div>`).join(''):'<div class="small">Equip artifacts to reveal your build profile.</div>'}
 const sets={};equippedGear14().forEach(g=>sets[g.set]=(sets[g.set]||0)+1);const best=Object.entries(sets).sort((a,b)=>b[1]-a[1])[0];const setCount=best?best[1]:0;set('setName14',best?best[0]:'No set resonance');set('setCount14',Math.min(3,setCount)+'/3');const bar=document.getElementById('setBar14');if(bar)bar.style.width=Math.min(100,setCount/3*100)+'%';set('setBonus14',best&&setCount>=3?`SET ACTIVE · ${best[0]} resonance grants +${best[1]*4}% build efficiency.`:best?`Resonance building · ${3-setCount} more matching piece(s) for the set effect.`:'Equip matching pieces to unlock a set effect.');
 const sum=document.getElementById('buildSummary14');if(sum)sum.textContent=equippedGear14().length?`Loadout ${state.loadouts.active+1} is shaping a ${best?best[0]:'hybrid'} build. Power ${st.power}, Aura ${st.aura}, Resilience ${st.resilience}, Focus ${st.focus}, Execution ${st.execution}. This build affects combat and character power.`:'No equipment build assembled yet.';
 const cod=document.getElementById('gearCodex14');if(cod)cod.innerHTML=GEAR14.map(g=>`<div class="codex-item"><img src="${g.file}" alt="${g.name}"><b>${g.name}</b><small>${g.set} · mastery ${(state.gearMastery[g.id]||0)}</small></div>`).join('');
}
'''
text=text.replace(needle,js+needle,1)
# call render build inside shadow systems and render all
text=text.replace('function renderShadowSystems(){renderEnvironment();renderRankVisual();renderWorld();','function renderShadowSystems(){renderEnvironment();renderRankVisual();renderWorld();renderBuildForge14();',1)
# enhance combatPower function by gear stats
text=text.replace("function combatPower(){return Math.round((levelFromXP(state.xp)*8)+auraPower()+skillPower()+equipmentBonus('str'));}","function combatPower(){const g=gearStats14();return Math.round((levelFromXP(state.xp)*8)+auraPower()+skillPower()+equipmentBonus('str')+g.power+Math.round(g.execution*.5)+Math.round(g.focus*.25));}")
# enhance auraPower if exact function exists
text=text.replace("function auraPower(){return Math.round(totalDone()*2 + (state.bossDamage||0)*3 + levelFromXP(state.xp)*12 + (state.proofs||0)*5)}", "function auraPower(){const g=gearStats14();return Math.round(totalDone()*2 + (state.bossDamage||0)*3 + levelFromXP(state.xp)*12 + (state.proofs||0)*5 + g.aura*2 + g.synergy*0);}",1)
# version
text=text.replace("versionCode 9\n        versionName '2.7.0'","versionCode 10\n        versionName '2.8.0'",1)
# README append via write later
html.write_text(text)
# README
readme=root/'README.md'
readme.write_text('''# Shadow System // Winter Arc — Monster Change 14\n\nMajor Mutation 14 adds the Build Forge / Equipment 2.0 layer.\n\n## Build Forge\n- Three persistent loadout slots\n- Eight equipment pieces with real stats and visual assets\n- Build statistics: Power, Aura, Resilience, Focus, Execution\n- Equipment affixes that describe how the build interacts with the real-life progression systems\n- Set resonance and matching-piece bonuses\n- Equipment mastery tracking\n- Build history and saved loadout state\n- Combat and Aura calculations now incorporate the active build\n\nThis is intentionally a real-life progression layer: equipment represents capabilities, habits, proof and build choices rather than replacing real-world action with a game economy.\n\nAndroid version: 2.8.0 / versionCode 10.\n''')
