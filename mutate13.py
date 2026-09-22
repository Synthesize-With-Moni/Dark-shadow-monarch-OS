from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np, math, wave, struct, zipfile, os, re
root=Path('/mnt/data/c13/work'); htmlp=root/'app/src/main/assets/index.html'; assets=root/'app/src/main/assets/assets'
assets.mkdir(parents=True,exist_ok=True)
html=htmlp.read_text()
# Generate meaningful high-res encounter art
W,H=1600,1000
names=['void_hound','iron_wraith','pressure_golem','distraction_wraith','old_self_avatar','monarch_guardian']
for idx,name in enumerate(names):
    y,x=np.mgrid[0:H,0:W]; cx=W*(.5+(.04*math.sin(idx))); cy=H*.55
    r=np.sqrt((x-cx)**2+(y-cy)**2)
    base=np.zeros((H,W,3),dtype=np.float32)
    # atmospheric gradient
    base[:,:,0]=8+10*np.exp(-((x-W*.5)**2+(y-H*.5)**2)/(2*(W*.55)**2))
    base[:,:,1]=7+5*np.exp(-((x-W*.5)**2+(y-H*.5)**2)/(2*(W*.6)**2))
    base[:,:,2]=15+24*np.exp(-((x-W*.5)**2+(y-H*.5)**2)/(2*(W*.5)**2))
    im=Image.fromarray(np.uint8(np.clip(base,0,255)),'RGB')
    d=ImageDraw.Draw(im,'RGBA')
    # floor/runes
    for k in range(8):
        yy=int(H*.72+k*24)
        d.line((80,yy,W-80,yy),fill=(90,60,150,25),width=2)
    # silhouette body
    colors=[(80,55,150,230),(120,120,150,225),(100,75,110,230),(150,40,90,230),(55,45,70,240),(160,110,255,235)]
    c=colors[idx]
    d.ellipse((cx-170,cy-300,cx+170,cy+80),fill=(4,4,8,245),outline=c,width=10)
    d.polygon([(cx-120,cy-50),(cx-280,cy+260),(cx+280,cy+260),(cx+120,cy-50)],fill=(3,3,7,245),outline=c)
    # head/eyes
    d.ellipse((cx-90,cy-230,cx+90,cy-70),fill=(2,2,5,255),outline=c,width=8)
    d.ellipse((cx-52,cy-170,cx-18,cy-145),fill=(255,50,100,240))
    d.ellipse((cx+18,cy-170,cx+52,cy-145),fill=(255,50,100,240))
    # weapon/arms
    d.line((cx-120,cy, cx-360,cy+180),fill=c,width=18)
    d.line((cx+120,cy, cx+360,cy+180),fill=c,width=18)
    # aura rings
    for rr in (330,400,470): d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),outline=(*c[:3],55),width=4)
    # label plate
    d.rounded_rectangle((80,80,610,160),radius=18,fill=(5,4,10,220),outline=(*c[:3],100),width=2)
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',34)
    except: font=None
    d.text((110,102),name.upper().replace('_',' '),fill=(230,225,245,230),font=font)
    im=im.filter(ImageFilter.GaussianBlur(.15)).resize((1600,1000))
    im.save(assets/f'combat_{name}.webp','WEBP',quality=88,method=6)
# Combat effect spritesheets
for nm,kind in [('combat_fx_energy.webp','energy'),('combat_fx_impact.webp','impact'),('combat_fx_shield.webp','shield')]:
    im=Image.new('RGBA',(1200,600),(0,0,0,0)); d=ImageDraw.Draw(im,'RGBA')
    for i in range(9):
        cx=100+i*135; cy=300
        for rr in range(30,150,25):
            a=max(0,120-int(rr*.45))
            col=(120,80,255,a) if kind=='energy' else (255,50,100,a) if kind=='impact' else (90,180,255,a)
            d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),outline=col,width=5)
        d.line((cx-120,cy,cx+120,cy),fill=(230,225,255,90),width=3)
    im.save(assets/nm,'WEBP',quality=90)
# combat ambience and hit sounds
sr=22050
def wav(path,dur,kind):
    n=int(sr*dur); t=np.arange(n)/sr
    if kind=='ambient':
        sig=.08*np.sin(2*np.pi*55*t)+.04*np.sin(2*np.pi*82*t)+.02*np.sin(2*np.pi*110*t)
        env=np.minimum(1,t/.5)*np.minimum(1,(dur-t)/.8)
        sig*=env
    elif kind=='hit':
        sig=.22*np.sin(2*np.pi*(180-120*t/dur)*t)*np.exp(-10*t)
    else:
        sig=.18*np.sin(2*np.pi*(420+500*t/dur)*t)*np.exp(-7*t)
    data=np.int16(np.clip(sig,-1,1)*32767)
    with wave.open(str(path),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(data.tobytes())
wav(assets/'combat_ambient.wav',18,'ambient'); wav(assets/'combat_hit.wav',.55,'hit'); wav(assets/'combat_execute.wav',.8,'execute')
# CSS
css='''\n.combat-panel{margin-top:16px;padding:16px;border:1px solid rgba(139,92,246,.24);border-radius:18px;background:radial-gradient(circle at 50% 20%,rgba(90,50,160,.14),rgba(3,3,7,.94));box-shadow:0 0 50px rgba(55,30,100,.12);display:none}.combat-panel.active{display:block;animation:panelIn .35s ease}.combat-stage{position:relative;min-height:300px;overflow:hidden;border-radius:15px;border:1px solid rgba(255,255,255,.07);background:#030307}.combat-stage img{width:100%;height:300px;object-fit:cover;opacity:.82;filter:saturate(.85) contrast(1.12)}.combat-overlay{position:absolute;inset:0;padding:18px;display:flex;flex-direction:column;justify-content:space-between;background:linear-gradient(180deg,rgba(0,0,0,.2),rgba(0,0,0,.78))}.combat-top{display:flex;justify-content:space-between;gap:12px}.combat-name{font:900 20px Orbitron;color:#f1eaff}.combat-type{font:600 9px "DM Mono";letter-spacing:2px;color:#8f86a8}.combat-bars{display:grid;gap:8px;min-width:220px}.combat-bar{height:9px;background:rgba(255,255,255,.07);border-radius:99px;overflow:hidden}.combat-bar i{display:block;height:100%;transition:.35s}.enemy-hp i{background:linear-gradient(90deg,#ff3158,#a42cff)}.player-energy i{background:linear-gradient(90deg,#4da6ff,#9b7dff)}.combat-bottom{display:grid;grid-template-columns:1fr auto;gap:12px;align-items:end}.combat-log{font-size:11px;color:#b9b0ca;line-height:1.6;max-height:74px;overflow:auto}.combat-actions{display:flex;gap:7px;flex-wrap:wrap;justify-content:flex-end}.combat-actions button{min-width:94px}.combat-statline{display:flex;gap:10px;flex-wrap:wrap;font:600 9px "DM Mono";color:#a59ab6;margin-top:7px}.combat-win{border:1px solid rgba(90,220,150,.25);background:rgba(50,180,120,.05)}@media(max-width:720px){.combat-bottom{grid-template-columns:1fr}.combat-bars{min-width:0}.combat-actions{justify-content:flex-start}.combat-stage img{height:260px}}\n'''
html=html.replace('</style>',css+'</style>',1)
# Insert combat panel after dungeon grid
needle='<div class="dungeon-grid" id="dungeonRooms"></div>'
panel='''<div class="combat-panel" id="combatPanel"><div class="section-head"><div><div class="section-title">COMBAT INSTANCE</div><div class="section-sub" id="combatSubtitle">The dungeon is responding to your current build.</div></div><span class="v6-chip" id="combatStateChip">READY</span></div><div class="combat-stage"><img id="combatEnemyArt" src="assets/combat_void_hound.webp" alt="Dungeon enemy"><div class="combat-overlay"><div class="combat-top"><div><div class="combat-type" id="combatEnemyType">DUNGEON ENCOUNTER</div><div class="combat-name" id="combatEnemyName">VOID HOUND</div><div class="combat-statline"><span id="combatEnemyRank">E-RANK</span><span id="combatEnemyMod">PRESSURE</span></div></div><div class="combat-bars"><div><small>ENEMY HP <b id="combatEnemyHpText">100%</b></small><div class="combat-bar enemy-hp"><i id="combatEnemyHp"></i></div></div><div><small>YOUR ENERGY <b id="combatEnergyText">100%</b></small><div class="combat-bar player-energy"><i id="combatEnergy"></i></div></div></div></div><div class="combat-bottom"><div class="combat-log" id="combatLog">Encounter initialized. Choose an action.</div><div class="combat-actions"><button class="control-btn primary" onclick="combatAction('attack')">ATTACK</button><button class="control-btn" onclick="combatAction('focus')">FOCUS</button><button class="control-btn" onclick="combatAction('skill')">SKILL</button><button class="control-btn" onclick="combatAction('defend')">DEFEND</button><button class="control-btn" onclick="combatAction('execute')">EXECUTE</button></div></div></div></div></div>'''
html=html.replace(needle,needle+panel,1)
# State default/load injection: easiest ensure dungeon combat in init
old="function initDungeon(){const key=dungeonKey();if(!state.dungeon||state.dungeon.key!==key){state.dungeon={key,rooms:{},charge:0,recoveryClaimed:false};persist();}return state.dungeon}"
new="function initDungeon(){const key=dungeonKey();if(!state.dungeon||state.dungeon.key!==key){state.dungeon={key,rooms:{},charge:0,recoveryClaimed:false,combat:null};persist();}if(!state.dungeon.combat)state.dungeon.combat=null;return state.dungeon}"
html=html.replace(old,new)
# Add combat functions before initDungeon
marker='function dungeonKey(){return state.arcStartDate+\'-\'+currentDay()}'
combat=r'''function combatRankMultiplier(){const r=rankForLevel(levelFromXP(state.xp));return r==='MONARCH'?1.8:r==='S'?1.55:r==='A'?1.4:r==='B'?1.28:r==='C'?1.18:r==='D'?1.08:1}
const COMBAT_ENCOUNTERS=[
 {id:'void_hound',name:'VOID HOUND',type:'DUNGEON BEAST',mod:'SPEED',hp:100,damage:8,file:'assets/combat_void_hound.webp'},
 {id:'iron_wraith',name:'IRON WRAITH',type:'ARMORED SHADE',mod:'ARMOR',hp:115,damage:10,file:'assets/combat_iron_wraith.webp'},
 {id:'pressure_golem',name:'PRESSURE GOLEM',type:'PRESSURE CONSTRUCT',mod:'FORTITUDE',hp:135,damage:12,file:'assets/combat_pressure_golem.webp'},
 {id:'distraction_wraith',name:'DISTRACTION WRAITH',type:'MENTAL ENEMY',mod:'DISRUPTION',hp:125,damage:11,file:'assets/combat_distraction_wraith.webp'},
 {id:'old_self_avatar',name:'OLD SELF',type:'IDENTITY ENCOUNTER',mod:'RESISTANCE',hp:150,damage:14,file:'assets/combat_old_self_avatar.webp'},
 {id:'monarch_guardian',name:'MONARCH GUARDIAN',type:'ASCENSION GUARD',mod:'SOVEREIGN',hp:180,damage:17,file:'assets/combat_monarch_guardian.webp'}
];
function combatEnemyFor(day){return COMBAT_ENCOUNTERS[Math.min(COMBAT_ENCOUNTERS.length-1,Math.floor((Math.max(1,day)-1)/16))]}
function combatPower(){return Math.round((state.stats.int+state.stats.per+state.stats.wil+state.stats.str+state.stats.foc)/5 + levelFromXP(state.xp)*2 + skillPower()*2 + auraPower()*.35 + equippedArtifacts().reduce((n,a)=>n+(a.bonus.str||0)+(a.bonus.wil||0),0))}
function startCombat(room){const d=initDungeon(), day=currentDay()+1, e=combatEnemyFor(day), mult=combatRankMultiplier();if(d.combat&&d.combat.active){toast('COMBAT ACTIVE','Finish the current encounter first.');return;}d.combat={active:true,room,enemy:e.id,hp:Math.round(e.hp*(1+(day/180))),maxHp:Math.round(e.hp*(1+(day/180))),energy:100,turn:0,guard:0,log:['The gate manifests '+e.name+'.','Your build power is '+combatPower()+'.']};persist();renderCombat();document.getElementById('combatPanel')?.scrollIntoView({behavior:'smooth',block:'center'});}
function combatAction(action){const c=initDungeon().combat;if(!c||!c.active)return;const e=COMBAT_ENCOUNTERS.find(x=>x.id===c.enemy)||COMBAT_ENCOUNTERS[0];let cost=0,damage=0,heal=0,log='';const power=combatPower()*combatRankMultiplier();c.turn++;if(action==='attack'){cost=12;damage=Math.max(5,Math.round(power*.16+(state.stats.str||0)*.35));log='Basic strike lands.'}else if(action==='focus'){cost=8;heal=18;damage=Math.round(power*.05);log='Focus restores energy and sharpens the next exchange.'}else if(action==='skill'){cost=25;damage=Math.max(12,Math.round(power*.28+skillPower()*2));log='A mastered skill tears through the encounter.'}else if(action==='defend'){cost=10;c.guard=35;damage=Math.round(power*.03);log='Guard stance reduces incoming pressure.'}else if(action==='execute'){cost=40;damage=Math.round(power*.5);log='EXECUTE attempts a decisive finish.'}if(c.energy<cost){toast('ENERGY LOW','Recover energy before using that action.');return;}c.energy=Math.max(0,c.energy-cost);c.energy=Math.min(100,c.energy+(action==='focus'?25:0));c.hp=Math.max(0,c.hp-damage);c.log.unshift('TURN '+c.turn+' · '+log+' -'+damage+' HP');if(c.hp<=0){finishCombat(true);return;}let incoming=Math.max(2,Math.round(e.damage*(1-(state.stats.wil||0)/160)*(1-c.guard/100)));if(action==='focus')incoming=Math.round(incoming*1.1);c.guard=0;c.energy=Math.max(0,c.energy-incoming*.35);c.log.unshift(e.name+' retaliates · -'+incoming+' pressure');if(c.energy<=0){c.energy=20;c.log.unshift('Your energy collapses, but the system forces a recovery pulse.');}if(action==='execute'&&damage>c.maxHp*.32&&c.hp<c.maxHp*.35){finishCombat(true);return;}persist();renderCombat();}
function finishCombat(win){const c=initDungeon().combat;if(!c)return;const room=c.room;const d=initDungeon();if(win){d.rooms[room]=true;d.charge=Math.min(5,Object.values(d.rooms).filter(Boolean).length);const reward=18+(c.turn<=5?8:0)+Math.round(combatPower()/20);state.essence=(state.essence||0)+reward;state.xp+=reward;state.skillXP=state.skillXP||{};state.skillPoints=(state.skillPoints||0)+(c.turn<=4?1:0);if(room==='boss'){state.bossDamage=Math.min(100,(state.bossDamage||0)+Math.round(reward*.7));}state.dungeon.combat=null;persist();toast('ENCOUNTER DEFEATED','+'+reward+' XP · +'+reward+' ESSENCE');addEvent('Dungeon encounter defeated · '+room.toUpperCase(),'⚔');playSystemSound('strike');renderAll();}else{c.active=false;c.energy=35;state.essence=Math.max(0,(state.essence||0)-4);state.dungeon.combat=c;persist();toast('ENCOUNTER SURVIVED','The dungeon remains active. Re-enter after recovering.');renderCombat();}}
function renderCombat(){const p=document.getElementById('combatPanel'),c=state.dungeon&&state.dungeon.combat;if(!p)return;if(!c||!c.active){p.classList.remove('active');return;}p.classList.add('active');const e=COMBAT_ENCOUNTERS.find(x=>x.id===c.enemy)||COMBAT_ENCOUNTERS[0];const set=(id,v)=>{const el=document.getElementById(id);if(el)el.textContent=v};const art=document.getElementById('combatEnemyArt');if(art)art.src=e.file;set('combatEnemyName',e.name);set('combatEnemyType',e.type);set('combatEnemyMod',e.mod);set('combatEnemyRank',rankForLevel(levelFromXP(state.xp))+' ENCOUNTER');set('combatEnemyHpText',Math.round(c.hp/c.maxHp*100)+'%');set('combatEnergyText',Math.round(c.energy)+'%');const hp=document.getElementById('combatEnemyHp');if(hp)hp.style.width=Math.max(0,c.hp/c.maxHp*100)+'%';const en=document.getElementById('combatEnergy');if(en)en.style.width=Math.max(0,c.energy)+'%';const lg=document.getElementById('combatLog');if(lg)lg.innerHTML=c.log.slice(0,5).map(x=>'<div>'+x+'</div>').join('');set('combatSubtitle','ROOM // '+String(c.room).toUpperCase()+' · TURN '+c.turn+' · POWER '+combatPower());set('combatStateChip','ENGAGED')}
'''
html=html.replace(marker,combat+'\n'+marker)
# Override clearDungeonRoom by insert after original definition line, to intercept
needle2="function strikeBoss(){"
over=r'''const _clearDungeonRoom=clearDungeonRoom;clearDungeonRoom=function(id){if(id==='boss'){return startCombat('boss')}const d=initDungeon();if(d.rooms[id])return;startCombat(id)};
'''
html=html.replace(needle2,over+needle2,1)
# render combat on deep render
html=html.replace('function deepRenderShadowSystems(){renderWorld();','function deepRenderShadowSystems(){renderWorld();renderCombat();',1)
# Add asset strip in dungeon after boss card
html=html.replace('</div></div>\n      </section>\n\n      <section class="card section shadow-screen" data-shadow-screen="skills">','</div></div><div class="asset-strip"><img src="assets/combat_fx_energy.webp" alt="Combat energy effects"><img src="assets/combat_fx_impact.webp" alt="Combat impact effects"><img src="assets/combat_fx_shield.webp" alt="Combat shield effects"></div>\n      </section>\n\n      <section class="card section shadow-screen" data-shadow-screen="skills">',1)
# README update
htmlp.write_text(html)
# update build version
bp=root/'app/build.gradle'; s=bp.read_text(); s=s.replace("versionCode 8","versionCode 9").replace("versionName '2.6.0'","versionName '2.7.0'"); bp.write_text(s)
# README
rp=root/'README.md'; txt=rp.read_text(); txt += '\n\n## Mutation 13 — Combat + Dungeon Engine\nDungeon rooms now launch persistent combat encounters with enemy-specific stats, player energy, attack/focus/skill/defend/execute actions, turn logs, victory rewards, boss integration, and high-resolution encounter/effect assets.\n'; rp.write_text(txt)
