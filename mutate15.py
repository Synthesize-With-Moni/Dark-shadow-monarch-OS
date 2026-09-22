from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import random, math, re, os, zipfile
root=Path('/mnt/data/c15fresh')
html=root/'app/src/main/assets/index.html'
assets=html.parent/'assets'; assets.mkdir(exist_ok=True)
random.seed(1515)

def font(sz):
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
        if os.path.exists(p): return ImageFont.truetype(p,sz)
    return ImageFont.load_default()

def skill_art(name, seed, a,b):
    random.seed(seed); W=900; H=900
    im=Image.new('RGB',(W,H),(3,3,9)); pix=im.load()
    for y in range(H):
        for x in range(W):
            dx=x-W/2; dy=y-H/2; rr=(dx*dx+dy*dy)**0.5/(W*.72)
            g=max(0,1-rr); n=random.random()*5
            pix[x,y]=(int(4+a*g+n),int(4+b*g+n*.4),int(10+min(80,(a+b)*.35)*g+n))
    d=ImageDraw.Draw(im,'RGBA'); cx=450; cy=400
    for r in range(90,390,48): d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=(a,b,255,40),width=3)
    for i in range(30):
        ang=random.random()*math.tau; ln=random.randint(120,410)
        d.line((cx,cy,cx+math.cos(ang)*ln,cy+math.sin(ang)*ln),fill=(a,b,255,random.randint(30,100)),width=random.randint(2,7))
    d.polygon([(450,160),(570,300),(530,520),(450,650),(370,520),(330,300)],fill=(a,b,255,25),outline=(a,b,255,170))
    d.text((40,760),name,fill=(240,235,250,225),font=font(34))
    d.text((40,815),'CAPABILITY MASTERY',fill=(150,145,165,200),font=font(18))
    im=im.filter(ImageFilter.GaussianBlur(.25)); im.save(assets/f'mastery_{seed}.webp',quality=92,method=6)

def banner(name, seed, a,b):
    random.seed(seed); W=1500; H=820
    im=Image.new('RGB',(W,H),(3,3,9)); p=im.load()
    for y in range(H):
      for x in range(W):
        dx=(x-W/2)/(W*.8); dy=(y-H/2)/(H*.8); g=max(0,1-(dx*dx+dy*dy)**.5); n=random.random()*4
        p[x,y]=(int(4+a*g+n),int(4+b*g+n*.3),int(12+(a+b)*.2*g+n))
    d=ImageDraw.Draw(im,'RGBA')
    for i in range(45):
      x=random.randrange(W); y=random.randrange(H); r=random.randrange(2,8); d.ellipse((x-r,y-r,x+r,y+r),fill=(a,b,255,random.randrange(30,130)))
    for i in range(12):
      x=random.randrange(W); d.line((x,H,x+random.randrange(-300,300),random.randrange(50,600)),fill=(a,b,255,random.randrange(30,90)),width=random.randrange(2,8))
    d.text((55,650),name,fill=(245,240,250,230),font=font(54)); d.text((58,715),'REAL-LIFE CAPABILITY DOMAIN',fill=(150,145,165,210),font=font(20))
    im=im.filter(ImageFilter.GaussianBlur(.3)); im.save(assets/f'domain_{seed}.webp',quality=92,method=6)

def emblem(name, seed, a,b):
    random.seed(seed); W=700; H=700; im=Image.new('RGB',(W,H),(3,3,9)); d=ImageDraw.Draw(im,'RGBA')
    for r in range(280,40,-30): d.ellipse((350-r,350-r,350+r,350+r),outline=(a,b,255,max(20,120-r//3)),width=4)
    pts=[]
    for i in range(8):
      ang=math.tau*i/8-math.pi/2; pts.append((350+250*math.cos(ang),350+250*math.sin(ang)))
    d.polygon(pts,outline=(a,b,255,180),fill=(a,b,255,25)); d.text((70,580),name,fill=(245,240,250,230),font=font(30))
    im.save(assets/f'spec_{seed}.webp',quality=94,method=6)

skills=[('FOCUS ENGINE',21,100,160),('DEEP WORK',22,80,190),('LEARNING LOOP',23,100,220),('BUILDING',24,180,90),('SHIP FAST',25,210,120),('PROBLEM SOLVING',26,160,190),('PHYSICAL DISCIPLINE',27,220,90),('RECOVERY',28,100,210),('COMMUNICATION',29,210,150),('NETWORKING',30,180,220),('COLLABORATION',31,120,230),('LEADERSHIP',32,220,180),('CREATIVE OUTPUT',33,190,120),('WRITING',34,130,220),('SYSTEM THINKING',35,170,250),('RESILIENCE',36,230,110),('SELF-DIRECTION',37,200,200),('PROOF CRAFT',38,240,150)]
for n,s,a,b in skills: skill_art(n,s,a,b)
domains=[('MIND',41,110,220),('CRAFT',42,220,110),('BODY',43,230,90),('SOCIAL',44,200,150),('CREATOR',45,150,230),('LEAD',46,230,190)]
for n,s,a,b in domains: banner(n,s,a,b)
for n,s,a,b in [('FOCUS SPECIALIST',51,100,230),('BUILDER SPECIALIST',52,220,100),('ATHLETE SPECIALIST',53,230,80),('CONNECTOR SPECIALIST',54,200,150),('CREATOR SPECIALIST',55,150,230),('COMMANDER SPECIALIST',56,230,190)]: emblem(n,s,a,b)

text=html.read_text()
css='''\n<style>/* MUTATION 15 // CAPABILITY MASTERY */
.mastery-hero{margin-top:14px;border:1px solid rgba(150,110,255,.2);border-radius:20px;overflow:hidden;position:relative;background:#05040d}.mastery-hero img{width:100%;height:220px;object-fit:cover;opacity:.62}.mastery-hero .mh-copy{position:absolute;inset:0;padding:22px;display:flex;flex-direction:column;justify-content:flex-end;background:linear-gradient(180deg,transparent 20%,rgba(3,3,9,.95) 100%)}.mh-title{font:800 22px Orbitron;letter-spacing:.08em}.mh-sub{font-size:10px;color:#a8a0b4;margin-top:6px;max-width:680px}.mastery-kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:10px}.mkpi{padding:12px;border:1px solid rgba(255,255,255,.07);border-radius:14px;background:rgba(255,255,255,.025)}.mkpi span{display:block;color:#82798c;font:700 8px 'DM Mono';letter-spacing:.1em}.mkpi b{display:block;font:800 18px Orbitron;margin-top:4px}.domain-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:14px}.domain-card{border:1px solid rgba(255,255,255,.07);border-radius:16px;overflow:hidden;background:rgba(255,255,255,.02)}.domain-card img{width:100%;height:110px;object-fit:cover}.domain-card .dc{padding:10px}.domain-card b{font:800 11px Orbitron}.domain-card small{display:block;color:#82798c;font-size:9px;margin-top:4px}.mastery-bar{height:7px;background:rgba(255,255,255,.07);border-radius:99px;overflow:hidden;margin-top:8px}.mastery-bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,#7c5cff,#b78cff);border-radius:99px}.skill-mastery-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:14px}.mastery-card{border:1px solid rgba(255,255,255,.07);border-radius:16px;background:rgba(255,255,255,.02);overflow:hidden}.mastery-card img{width:100%;height:135px;object-fit:cover}.mastery-card .mc{padding:11px}.mastery-card b{font:800 11px Orbitron}.mastery-card .tier{color:#9e91b3;font:700 8px 'DM Mono';margin-top:4px}.mastery-card p{font-size:9px;color:#aaa1b2;line-height:1.5;min-height:28px}.mastery-actions{display:flex;gap:7px;flex-wrap:wrap;margin-top:8px}.practice-panel{margin-top:14px;padding:16px;border:1px solid rgba(150,110,255,.18);border-radius:18px;background:rgba(255,255,255,.02)}.practice-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:9px;margin-top:10px}.practice-grid input,.practice-grid select{width:100%;box-sizing:border-box}.special-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-top:12px}.special-card{border:1px solid rgba(255,255,255,.07);border-radius:15px;overflow:hidden;background:rgba(255,255,255,.02)}.special-card img{width:100%;height:100px;object-fit:cover}.special-card .sc{padding:9px}.special-card b{font:800 9px Orbitron}.special-card small{display:block;color:#81788f;font-size:8px;margin-top:4px}.practice-log{margin-top:12px;display:grid;gap:7px;max-height:260px;overflow:auto}.practice-entry{padding:9px 10px;border-left:2px solid rgba(150,110,255,.5);background:rgba(255,255,255,.025);border-radius:8px;font-size:9px}.practice-entry small{color:#82798c;float:right}@media(max-width:850px){.mastery-kpis{grid-template-columns:repeat(2,1fr)}.domain-grid,.skill-mastery-grid,.special-grid{grid-template-columns:1fr 1fr}.practice-grid{grid-template-columns:1fr}.mastery-card img{height:110px}}</style>\n'''
text=text.replace('</head>',css+'</head>',1)
# insert capability lab after skill section
marker='''      </section>\n\n      <div class="asset-strip"><img src="assets/rank_emblems_1024.png"'''
block='''      </section>\n\n<section class="card section shadow-screen" data-shadow-screen="skills">\n<div class="section-head"><div><div class="section-title">CAPABILITY LAB // MASTERY</div><div class="section-sub">Skills are not unlocked by fantasy points. They are developed through repeated real-world practice, evidence and reflection.</div></div><span class="v6-chip" id="masteryTierCount">0 MASTERS</span></div>\n<div class="mastery-hero"><img src="assets/domain_45.webp" alt="Creator capability domain"><div class="mh-copy"><div class="mh-title">BUILD THE PERSON, NOT THE AVATAR</div><div class="mh-sub">Log actual practice. Attach proof when it exists. The system measures repetition and evidence, while your real work remains the source of progression.</div></div></div>\n<div class="mastery-kpis"><div class="mkpi"><span>TOTAL PRACTICE</span><b id="masteryMinutes">0m</b></div><div class="mkpi"><span>CAPABILITIES</span><b id="masteryCapabilities">0/18</b></div><div class="mkpi"><span>MASTERED</span><b id="masteryMasters">0</b></div><div class="mkpi"><span>EVIDENCE RATE</span><b id="masteryEvidence">0%</b></div></div>\n<div class="section-head" style="margin-top:18px"><div><div class="section-title">REAL-LIFE DOMAINS</div><div class="section-sub">Your character is a map of capabilities, not a combat class.</div></div></div><div class="domain-grid" id="domainGrid15"></div>\n<div class="section-head" style="margin-top:18px"><div><div class="section-title">CAPABILITY MASTERY</div><div class="section-sub">Each practice session contributes to one capability. Mastery requires time, repetition and evidence.</div></div></div><div class="skill-mastery-grid" id="masteryGrid15"></div>\n<div class="practice-panel"><div class="section-title">LOG REAL PRACTICE</div><div class="section-sub">Example: 45 minutes of coding, 30 minutes of communication practice, 60 minutes of gym training, or a completed project milestone.</div><div class="practice-grid"><select id="practiceSkill15"></select><input class="text-input" id="practiceMinutes15" type="number" min="5" max="600" placeholder="Minutes"><input class="text-input" id="practiceEvidence15" maxlength="160" placeholder="Evidence / output / link note (optional)"></div><div class="mastery-actions"><button class="control-btn primary" onclick="logPractice15()">LOG PRACTICE</button><button class="control-btn" onclick="logMilestone15()">LOG MILESTONE</button></div><div class="practice-log" id="practiceLog15"></div></div>\n<div class="section-head" style="margin-top:18px"><div><div class="section-title">SPECIALIZATION PATHS</div><div class="section-sub">Specialization emerges from what you repeatedly practice, not what you select at the beginning.</div></div></div><div class="special-grid" id="specialGrid15"></div>\n</section>\n\n      <div class="asset-strip"><img src="assets/rank_emblems_1024.png"'''
if marker not in text: raise SystemExit('marker not found')
text=text.replace(marker,block,1)
# state defaults
text=text.replace("buildHistory:[]", "buildHistory:[],mastery:{},practiceLog:[],specializations:{},masteryMilestones:[]",1)
# state load line
old="s.buildHistory=Array.isArray(parsed.buildHistory)?parsed.buildHistory.slice(-30):[];"
new=old+"s.mastery=Object.assign({},parsed.mastery||{});s.practiceLog=Array.isArray(parsed.practiceLog)?parsed.practiceLog.slice(-200):[];s.specializations=Object.assign({},parsed.specializations||{});s.masteryMilestones=Array.isArray(parsed.masteryMilestones)?parsed.masteryMilestones.slice(-50):[];"
text=text.replace(old,new,1)
# add JS before deepRenderShadowSystems
needle='function deepRenderShadowSystems(){'
js=r'''
const CAP15=[
['focus','FOCUS ENGINE','MIND','Train concentration through deliberate sessions.',21],['deepwork','DEEP WORK','MIND','Build the ability to work without fragmentation.',22],['learning','LEARNING LOOP','MIND','Practice retrieval, explanation and iteration.',23],['building','BUILDING','CRAFT','Turn ideas into functioning artifacts.',24],['shipping','SHIP FAST','CRAFT','Finish and release instead of endlessly polishing.',25],['problem','PROBLEM SOLVING','CRAFT','Break ambiguous problems into solvable parts.',26],['physical','PHYSICAL DISCIPLINE','BODY','Train consistency through physical practice.',27],['recovery','RECOVERY','BODY','Recover deliberately so effort can compound.',28],['communication','COMMUNICATION','SOCIAL','Practice clarity, listening and expression.',29],['networking','NETWORKING','SOCIAL','Create genuine connections through useful interaction.',30],['collab','COLLABORATION','SOCIAL','Build with other people and handle shared constraints.',31],['leadership','LEADERSHIP','SOCIAL','Take responsibility for outcomes and coordination.',32],['creative','CREATIVE OUTPUT','CREATOR','Turn ideas into original work.',33],['writing','WRITING','CREATOR','Develop clear written thinking.',34],['systems','SYSTEM THINKING','CREATOR','See relationships, feedback loops and leverage.',35],['resilience','RESILIENCE','LEAD','Continue intelligently through setbacks.',36],['direction','SELF-DIRECTION','LEAD','Choose priorities and act without external pressure.',37],['proofcraft','PROOF CRAFT','LEAD','Document meaningful work so progress remains visible.',38]
];
const SPEC15=[['FOCUS SPECIALIST','focus','Build around attention, deep work and learning.','assets/spec_51.webp'],['BUILDER SPECIALIST','building','Build around shipping and problem solving.','assets/spec_52.webp'],['ATHLETE SPECIALIST','physical','Build around physical discipline and recovery.','assets/spec_53.webp'],['CONNECTOR SPECIALIST','networking','Build around communication, collaboration and leadership.','assets/spec_54.webp'],['CREATOR SPECIALIST','creative','Build around creation, writing and systems thinking.','assets/spec_55.webp'],['COMMANDER SPECIALIST','direction','Build around self-direction, resilience and proof.','assets/spec_56.webp']];
function masteryObj(id){return state.mastery[id]||{minutes:0,sessions:0,evidence:0,lastDay:0,streak:0,best:0};}
function masteryTier15(m){const x=m.minutes||0;return x>=300?'MASTER':x>=200?'ADVANCED':x>=120?'SKILLED':x>=60?'PRACTICED':x>=20?'INITIATE':'UNTRAINED'}
function masteryPct15(m){return Math.min(100,Math.round((m.minutes||0)/300*100));}
function logPractice15(){const id=document.getElementById('practiceSkill15')?.value;let mins=Number(document.getElementById('practiceMinutes15')?.value||0);const ev=String(document.getElementById('practiceEvidence15')?.value||'').trim();if(!id)return;if(!Number.isFinite(mins)||mins<5||mins>600){toast('PRACTICE INVALID','Use 5–600 minutes.');return;}mins=Math.round(mins);const m=masteryObj(id);const d=currentDay()+1;m.minutes+=mins;m.sessions++;if(ev)m.evidence++;if(m.lastDay===d-1)m.streak++;else m.streak=1;m.best=Math.max(m.best||0,m.streak);m.lastDay=d;state.mastery[id]=m;state.practiceLog.push({id,minutes:mins,evidence:ev,day:d,time:new Date().toISOString()});state.practiceLog=state.practiceLog.slice(-200);state.essence=(state.essence||0)+Math.min(25,Math.ceil(mins/20));state.xp+=Math.min(35,Math.ceil(mins/30));if(ev)state.proofs=(state.proofs||0)+1;state.masteryMilestones.push({id,day:d,tier:masteryTier15(m),minutes:m.minutes});persist();renderAll();toast('PRACTICE RECORDED',`${mins} minutes added to ${CAP15.find(x=>x[0]===id)?.[1]||id}.`);}
function logMilestone15(){const id=document.getElementById('practiceSkill15')?.value;if(!id)return;const m=masteryObj(id);m.evidence++;m.sessions++;m.minutes+=30;state.mastery[id]=m;state.practiceLog.push({id,minutes:30,evidence:'MILESTONE',day:currentDay()+1,time:new Date().toISOString()});state.proofs=(state.proofs||0)+1;state.xp+=30;state.essence=(state.essence||0)+20;persist();renderAll();toast('MILESTONE LOGGED','A real output has been added to the capability record.');}
function renderMastery15(){
 const total=CAP15.reduce((n,x)=>n+(masteryObj(x[0]).minutes||0),0), masters=CAP15.filter(x=>masteryTier15(masteryObj(x[0]))==='MASTER').length, evs=CAP15.reduce((n,x)=>n+(masteryObj(x[0]).evidence||0),0), sessions=CAP15.reduce((n,x)=>n+(masteryObj(x[0]).sessions||0),0);const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v};set('masteryMinutes',total+'m');set('masteryCapabilities',CAP15.filter(x=>(masteryObj(x[0]).minutes||0)>0).length+'/'+CAP15.length);set('masteryMasters',masters);set('masteryEvidence',sessions?Math.round(evs/sessions*100)+'%':'0%');set('masteryTierCount',masters+' MASTERS');
 const dg=document.getElementById('domainGrid15');if(dg){const domains={MIND:['focus','deepwork','learning'],CRAFT:['building','shipping','problem'],BODY:['physical','recovery'],SOCIAL:['communication','networking','collab','leadership'],CREATOR:['creative','writing','systems'],LEAD:['resilience','direction','proofcraft']};dg.innerHTML=[['MIND',41],['CRAFT',42],['BODY',43],['SOCIAL',44],['CREATOR',45],['LEAD',46]].map(([name,seed])=>{const ids=domains[name];const mins=ids.reduce((n,id)=>n+masteryObj(id).minutes,0);const pct=Math.min(100,Math.round(mins/900*100));return `<div class="domain-card"><img src="assets/domain_${seed}.webp" alt="${name} domain"><div class="dc"><b>${name}</b><small>${mins} minutes across ${ids.length} capabilities</small><div class="mastery-bar"><i style="width:${pct}%"></i></div><small>${pct}% domain development</small></div></div>`}).join('');}
 const mg=document.getElementById('masteryGrid15');if(mg)mg.innerHTML=CAP15.map(x=>{const m=masteryObj(x[0]),tier=masteryTier15(m),pct=masteryPct15(m);return `<div class="mastery-card"><img src="assets/mastery_${x[4]}.webp" alt="${x[1]}"><div class="mc"><b>${x[1]}</b><div class="tier">${x[2]} · ${tier} · ${m.minutes} MIN</div><p>${x[3]}</p><div class="mastery-bar"><i style="width:${pct}%"></i></div><div class="mastery-actions"><small>${m.sessions} sessions · ${m.evidence} evidence · best streak ${m.best||0}</small></div></div></div>`}).join('');
 const sel=document.getElementById('practiceSkill15');if(sel){const cur=sel.value;sel.innerHTML=CAP15.map(x=>`<option value="${x[0]}">${x[1]} · ${x[2]}</option>`).join('');if(cur)sel.value=cur;}
 const lg=document.getElementById('practiceLog15');if(lg)lg.innerHTML=(state.practiceLog||[]).slice().reverse().slice(0,20).map(x=>`<div class="practice-entry"><b>${CAP15.find(c=>c[0]===x.id)?.[1]||x.id}</b> · ${x.minutes} min · ${x.evidence?'EVIDENCE':'PRACTICE'}<small>D${String(x.day).padStart(2,'0')}</small></div>`).join('')||'<div class="small">No practice logged yet. Your first real session becomes the first mark in the capability record.</div>';
 const sg=document.getElementById('specialGrid15');if(sg)sg.innerHTML=SPEC15.map(s=>{const m=masteryObj(s[1]);const tier=masteryTier15(m);const unlock=(m.minutes>=180&&m.evidence>=2);return `<div class="special-card"><img src="${s[3]}" alt="${s[0]}"><div class="sc"><b>${s[0]}</b><small>${unlock?'EMERGING SPECIALIZATION':'Develop through '+Math.max(0,180-m.minutes)+' more minutes and evidence.'}</small><small>${s[2]}</small></div></div>`}).join('');
}
'''
text=text.replace(needle,js+needle,1)
# add render call near renderBuildForge14
text=text.replace('renderBuildForge14();', 'renderBuildForge14();renderMastery15();',1)
# version 2.9.0 / 11
text=text.replace("versionCode 10\n        versionName '2.8.0'","versionCode 11\n        versionName '2.9.0'",1)
html.write_text(text)
(root/'README.md').write_text('''# Shadow System // Winter Arc — Monster Change 15\n\nMajor Mutation 15 adds the Capability Mastery system.\n\nThis is deliberately real-life-first: the player logs actual practice time, milestones, and optional evidence. Mastery is derived from repeated practice and evidence rather than simply spending RPG points.\n\n## Capability domains\n- Mind: focus, deep work, learning\n- Craft: building, shipping, problem solving\n- Body: physical discipline, recovery\n- Social: communication, networking, collaboration, leadership\n- Creator: creative output, writing, systems thinking\n- Lead: resilience, self-direction, proof craft\n\n## Mastery\n- 18 capabilities\n- Practice minutes and session counts\n- Evidence counts\n- Streak and best-streak tracking\n- Five mastery tiers: Untrained, Initiate, Practiced, Skilled, Advanced, Master\n- Domain development summaries\n- Emerging specialization paths\n- Practice log and milestone logging\n\nThe system explicitly treats real-world action as the source of progression; the game layer is only the visualization and feedback system.\n\nAndroid version: 2.9.0 / versionCode 11.\n''')
