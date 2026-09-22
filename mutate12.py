from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os, math, random, json, zipfile, shutil
root='/mnt/data/c12'; assets=os.path.join(root,'app/src/main/assets/assets'); os.makedirs(assets,exist_ok=True)
random.seed(12)
forms=[('e','AWAKENED SHADOW',(75,59,107)),('d','HUNTER',(61,102,140)),('c','EXECUTOR',(78,111,163)),('b','NIGHTBLADE',(106,79,176)),('a','ELITE SHADOW',(155,60,255)),('s','S-RANK SOVEREIGN',(43,140,255)),('monarch','SHADOW MONARCH',(210,168,255))]
for idx,(slug,title,base) in enumerate(forms):
    W,H=1800,2400; im=Image.new('RGB',(W,H),(4,4,10)); d=ImageDraw.Draw(im)
    # layered radial-ish aura bands
    cx,cy=W//2,980
    for r in range(850,80,-18):
        f=(850-r)/770
        col=tuple(int(base[i]*(0.12+0.42*f)) for i in range(3))
        d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=col,width=10)
    # stars / motes
    for _ in range(650):
        x=random.randrange(W); y=random.randrange(H); rr=random.choice([1,1,2,3,4])
        d.ellipse((x-rr,y-rr,x+rr,y+rr),fill=tuple(min(255,c+random.randrange(10,45)) for c in base))
    # silhouette
    head=260+idx*10; bodyw=220+idx*45; bodyh=620+idx*55
    d.ellipse((cx-head//2,cy-260,cx+head//2,cy-260+head),fill=(7,7,14),outline=base,width=8)
    d.polygon([(cx-bodyw//2,cy+20),(cx-bodyw//3,cy+bodyh),(cx-bodyw//2-180,cy+bodyh+500),(cx,cy+bodyh+230),(cx+bodyw//2+180,cy+bodyh+500),(cx+bodyw//3,cy+20)],fill=(5,5,11),outline=base)
    # eyes / rank crown
    eye=24+idx*3
    d.ellipse((cx-80,cy-155,cx-80+eye,cy-155+eye),fill=base); d.ellipse((cx+55,cy-155,cx+55+eye,cy-155+eye),fill=base)
    crown_y=cy-420
    pts=[]
    for k in range(7):
        x=cx-220+k*73; y=crown_y-(170 if k in (1,3,5) else 55)
        pts.append((x,y))
    pts += [(cx+220,crown_y+100),(cx-220,crown_y+100)]
    d.polygon(pts,fill=(10,8,20),outline=base)
    # weapon aura arc for higher forms
    if idx>=3:
        d.arc((cx-650,cy-500,cx+650,cy+800),190,350,fill=base,width=20)
    if idx>=5:
        d.arc((cx-760,cy-610,cx+760,cy+950),10,170,fill=(220,220,255),width=10)
    # title plate
    d.rectangle((130,H-360,W-130,H-130),fill=(6,6,14),outline=base,width=5)
    d.text((190,H-315),title,fill=(235,235,255))
    d.text((190,H-255),f'EVOLUTION FORM // {idx+1}',fill=base)
    im=im.filter(ImageFilter.GaussianBlur(0.35))
    im.save(os.path.join(assets,f'evolution_{slug}_1800.webp'),quality=88,method=6)
# transformation sequence frames: meaningful animation assets
for i in range(12):
    W=900; H=900; im=Image.new('RGBA',(W,H),(3,3,8,0)); d=ImageDraw.Draw(im); cx=cy=W//2
    t=i/11; rad=int(90+600*t)
    for k in range(7):
        a=2*math.pi*k/7 + t*4
        x=cx+math.cos(a)*rad; y=cy+math.sin(a)*rad
        rr=int(10+40*(1-t)); d.ellipse((x-rr,y-rr,x+rr,y+rr),fill=(110+int(100*t),70,255,180))
    d.ellipse((cx-rad//2,cy-rad//2,cx+rad//2,cy+rad//2),outline=(150,100,255,180),width=12)
    im.save(os.path.join(assets,f'transform_{i:02d}.webp'),quality=86,method=6)
# codex data
codex={"forms":[{"rank":r.upper(),'title':t,'level':lv,'passive':p} for r,t,lv,p in [
('E','Awakened Shadow',1,'Base form. Every completed quest is foundational.'),('D','Hunter',5,'Momentum becomes more stable.'),('C','Executor',12,'Pressure chapters yield stronger execution.'),('B','Nightblade',20,'Equipment and skills begin to compound.'),('A','Elite Shadow',30,'High-difficulty quests become the normal training ground.'),('S','S-Rank Sovereign',40,'Presence is backed by deep execution history.'),('MONARCH','Shadow Monarch',55,'Final form. The system audits what was actually built.')]]}
open(os.path.join(assets,'evolution_codex.json'),'w').write(json.dumps(codex,indent=2))
# HTML
p=os.path.join(root,'app/src/main/assets/index.html'); s=open(p,encoding='utf-8').read()
css='''\n/* ===== MUTATION 12 · TRUE EVOLUTION ENGINE ===== */\n.evolution-forge{margin-top:18px;border:1px solid rgba(150,100,255,.28);border-radius:26px;padding:18px;background:linear-gradient(145deg,rgba(20,13,40,.9),rgba(5,5,14,.96));box-shadow:0 20px 80px rgba(45,20,100,.18)}\n.evolution-hero{display:grid;grid-template-columns:260px 1fr;gap:18px;align-items:stretch}.evolution-hero-art{width:100%;height:330px;object-fit:cover;border-radius:20px;border:1px solid rgba(180,130,255,.3);box-shadow:0 0 60px rgba(100,60,220,.2)}\n.evolution-info{display:flex;flex-direction:column;justify-content:center;gap:10px}.evolution-kicker{font:700 11px Orbitron;letter-spacing:3px;color:#9f8cff}.evolution-title{font:900 30px Orbitron;letter-spacing:2px}.evolution-passive{font-size:13px;line-height:1.65;color:#bdb6d4}.evolution-meter{height:10px;border-radius:999px;background:#12101d;overflow:hidden;border:1px solid rgba(180,130,255,.2)}.evolution-meter>i{display:block;height:100%;background:linear-gradient(90deg,#6949ff,#b99aff);box-shadow:0 0 22px #744dff}.form-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;margin-top:16px}.form-node{min-height:100px;padding:8px;border-radius:14px;border:1px solid rgba(150,120,210,.16);background:#090811;text-align:center;opacity:.45}.form-node.active{opacity:1;border-color:rgba(190,150,255,.6);box-shadow:0 0 25px rgba(100,60,220,.18)}.form-node img{width:100%;height:68px;object-fit:cover;border-radius:10px}.form-node b{display:block;font:700 9px Orbitron;margin-top:6px}.form-node small{font-size:9px;color:#8f89a4}.evolution-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin-top:14px}.evo-stat{padding:12px;border-radius:14px;background:rgba(255,255,255,.025);border:1px solid rgba(150,120,210,.12)}.evo-stat span{display:block;font:700 9px Orbitron;color:#8f89a4}.evo-stat b{font-size:18px}.transform-overlay{position:fixed;inset:0;background:rgba(2,2,7,.94);z-index:9999;display:none;align-items:center;justify-content:center;flex-direction:column;gap:16px}.transform-overlay.show{display:flex}.transform-overlay img{width:min(78vw,620px);height:min(78vw,620px);object-fit:cover;border-radius:30px;box-shadow:0 0 120px rgba(110,70,255,.4)}.transform-overlay .big{font:900 28px Orbitron;letter-spacing:5px}.transform-overlay .sub{color:#aaa3bd;font-size:12px;letter-spacing:2px}@media(max-width:760px){.evolution-hero{grid-template-columns:1fr}.evolution-hero-art{height:300px}.form-grid{grid-template-columns:repeat(4,1fr)}.evolution-stats{grid-template-columns:repeat(2,1fr)}}\n'''
s=s.replace('</style>',css+'</style>',1)
# Add panel after status section's stats grid close by targeting exact snippet
needle='''        <div id="statsGrid" class="stats-grid"></div>\n      </section>'''
panel='''        <div id="statsGrid" class="stats-grid"></div>\n        <div class="evolution-forge" id="evolutionForge">\n          <div class="section-head"><div><div class="section-title">EVOLUTION FORGE // TRUE FORM</div><div class="section-sub">Rank is no longer a label. Each form changes the character's presence, passive and visual identity.</div></div><span class="v6-chip" id="evolutionStateChip">AWAKENED</span></div>\n          <div class="evolution-hero"><img id="evolutionHeroArt" class="evolution-hero-art" src="assets/evolution_e_1800.webp" alt="Current evolution form"><div class="evolution-info"><div class="evolution-kicker" id="evolutionKicker">FORM 01 · E-RANK</div><div class="evolution-title" id="evolutionTitle">AWAKENED SHADOW</div><div class="evolution-passive" id="evolutionPassive">Base form. Every completed quest is foundational.</div><div class="small" id="evolutionRequirement">NEXT FORM · D-RANK · LEVEL 5</div><div class="evolution-meter"><i id="evolutionMeter" style="width:0%"></i></div><div class="small" id="evolutionMeterText">0% toward next evolution</div><button class="control-btn primary" id="evolutionPreviewBtn" onclick="previewEvolution()">ENTER EVOLUTION CHAMBER</button></div></div>\n          <div class="form-grid" id="formGrid"></div>\n          <div class="evolution-stats"><div class="evo-stat"><span>FORM POWER</span><b id="evoFormPower">0</b></div><div class="evo-stat"><span>PRESENCE</span><b id="evoPresence">0</b></div><div class="evo-stat"><span>MASTERY</span><b id="evoMastery">0%</b></div><div class="evo-stat"><span>EVOLUTIONS</span><b id="evoCount">0 / 6</b></div></div>\n        </div>\n      </section>'''
s=s.replace(needle,panel,1)
# overlay before </body>
overlay='''\n<div class="transform-overlay" id="transformOverlay"><img id="transformFrame" src="assets/transform_00.webp" alt="Evolution chamber"><div class="big" id="transformTitle">EVOLUTION CHAMBER</div><div class="sub" id="transformSub">THE SYSTEM IS RECOGNIZING YOUR FORM</div></div>\n'''
s=s.replace('</body>',overlay+'</body>',1)
# JS insert before renderShadowSystems
js='''\n// ===== MUTATION 12 · TRUE EVOLUTION ENGINE =====\nconst EVOLUTION_FORMS=[\n {r:'E',slug:'e',level:1,title:'AWAKENED SHADOW',passive:'Base form. Every completed quest is foundational.'},\n {r:'D',slug:'d',level:5,title:'HUNTER',passive:'Momentum becomes more stable. The character begins to operate with intent.'},\n {r:'C',slug:'c',level:12,title:'EXECUTOR',passive:'Pressure chapters yield stronger execution and deeper proof.'},\n {r:'B',slug:'b',level:20,title:'NIGHTBLADE',passive:'Equipment and skills begin to compound into a recognizable build.'},\n {r:'A',slug:'a',level:30,title:'ELITE SHADOW',passive:'High-difficulty quests become the normal training ground.'},\n {r:'S',slug:'s',level:40,title:'S-RANK SOVEREIGN',passive:'Presence is backed by deep execution history, not a cosmetic badge.'},\n {r:'MONARCH',slug:'monarch',level:55,title:'SHADOW MONARCH',passive:'Final form. The system audits what was actually built across the Arc.'}\n];\nfunction evolutionIndex(){const lv=levelFromXP(state.xp);let i=0;EVOLUTION_FORMS.forEach((f,n)=>{if(lv>=f.level)i=n});return i}\nfunction renderEvolutionForge(){const idx=evolutionIndex(),f=EVOLUTION_FORMS[idx],next=EVOLUTION_FORMS[idx+1];const lv=levelFromXP(state.xp);const img=document.getElementById('evolutionHeroArt');if(img)img.src='assets/evolution_'+f.slug+'_1800.webp';const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v};set('evolutionKicker',`FORM ${String(idx+1).padStart(2,'0')} · ${f.r}-RANK`);set('evolutionTitle',f.title);set('evolutionPassive',f.passive);set('evolutionStateChip',f.r==='MONARCH'?'MONARCH FORM':'FORM ACTIVE');set('evolutionRequirement',next?`NEXT FORM · ${next.r}-RANK · LEVEL ${next.level}`:'FINAL FORM · ASCENSION AUDIT');let pct=next?Math.max(0,Math.min(100,((lv-f.level)/(next.level-f.level))*100)):100;const bar=document.getElementById('evolutionMeter');if(bar)bar.style.width=pct+'%';set('evolutionMeterText',next?`${Math.round(pct)}% toward ${next.r}-RANK`:'100% · FINAL FORM');set('evoFormPower',Math.round((idx+1)*100 + lv*3 + (state.skillPoints||0)*7));set('evoPresence',auraPower()+idx*9);set('evoMastery',Math.min(100,Math.round((totalDone()/TOTAL_MISSIONS)*60 + idx*7))+'%');set('evoCount',`${idx} / 6`);const grid=document.getElementById('formGrid');if(grid)grid.innerHTML=EVOLUTION_FORMS.map((x,n)=>`<div class="form-node ${n<=idx?'active':''}"><img src="assets/evolution_${x.slug}_1800.webp" alt="${x.title}"><b>${x.r}</b><small>${n<=idx?'UNLOCKED':'LV '+x.level}</small></div>`).join('');}\nlet evolutionPreviewTimer=null;function previewEvolution(){const overlay=document.getElementById('transformOverlay'),frame=document.getElementById('transformFrame'),title=document.getElementById('transformTitle'),sub=document.getElementById('transformSub');if(!overlay)return;overlay.classList.add('show');let i=0;clearInterval(evolutionPreviewTimer);evolutionPreviewTimer=setInterval(()=>{if(i<12){frame.src=`assets/transform_${String(i).padStart(2,'0')}.webp`;i++}else{clearInterval(evolutionPreviewTimer);overlay.classList.remove('show')}},120);title.textContent=EVOLUTION_FORMS[evolutionIndex()].title;sub.textContent='THE SYSTEM IS RECOGNIZING YOUR FORM';setTimeout(()=>overlay.classList.remove('show'),2300)}\n'''
s=s.replace('function renderShadowSystems(){',js+'\nfunction renderShadowSystems(){',1)
s=s.replace('function renderShadowSystems(){renderEnvironment();renderRankVisual();renderWorld();','function renderShadowSystems(){renderEnvironment();renderRankVisual();renderWorld();renderEvolutionForge();',1)
# version
b=os.path.join(root,'app/build.gradle'); bs=open(b).read().replace('versionCode 7','versionCode 8').replace("versionName '2.5.0'","versionName '2.6.0'");open(b,'w').write(bs)
# manifest label
m=os.path.join(root,'app/src/main/AndroidManifest.xml'); ms=open(m).read().replace('Shadow System // Winter Arc','Shadow System // Winter Arc');open(m,'w').write(ms)
# README
rp=os.path.join(root,'README.md'); rs=open(rp).read(); rs += '\n\n## Mutation 12 — True Evolution Engine\nRank forms are now distinct visual states with level gates, passive identity, evolution mastery, form power, evolution preview frames, and a dedicated Evolution Forge UI. Assets include seven high-resolution evolution forms and a 12-frame transformation sequence.\n';open(rp,'w').write(rs)
