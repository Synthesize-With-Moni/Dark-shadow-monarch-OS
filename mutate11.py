from PIL import Image, ImageDraw, ImageFilter
import numpy as np, os, math, wave, struct, random, re
root='/mnt/data/c11/app/src/main/assets/assets'
os.makedirs(root,exist_ok=True)
random.seed(1107)
W,H=1536,1024
# Generate rich atmospheric scene layers: dark fantasy abstract, intentionally asset-backed.
scenes={
 'world_dawn':'WORLD DAWN','world_night':'WORLD NIGHT','world_storm':'VOID STORM','world_eclipse':'ECLIPSE EVENT',
 'world_awakening':'AWAKENING WILDS','world_pressure':'PRESSURE FORGE','world_monarch':'MONARCH DOMAIN','world_ascension':'ASCENSION SKY',
 'aura_void':'AURA VOID','aura_ember':'AURA EMBER','aura_royal':'AURA ROYAL','aura_monarch':'AURA MONARCH'
}
for name,label in scenes.items():
    y,x=np.mgrid[0:H,0:W]
    # dark base with multiscale noise
    base=np.zeros((H,W,3),dtype=np.float32)
    # palette varies by semantic
    if 'storm' in name: p=np.array([22,18,48]); q=np.array([72,35,120])
    elif 'eclipse' in name: p=np.array([8,6,18]); q=np.array([92,28,78])
    elif 'monarch' in name or 'royal' in name: p=np.array([10,8,26]); q=np.array([65,45,120])
    elif 'ember' in name or 'pressure' in name: p=np.array([25,8,10]); q=np.array([120,35,30])
    elif 'ascension' in name: p=np.array([10,12,28]); q=np.array([72,76,160])
    elif 'awakening' in name or 'dawn' in name: p=np.array([13,11,28]); q=np.array([58,35,85])
    else: p=np.array([5,5,16]); q=np.array([35,30,75])
    t=np.clip((y/H)*0.7 + 0.18*np.sin(x/210)+0.12*np.sin((x+y)/310),0,1)[...,None]
    base=p*(1-t)+q*t
    # radial aura
    cx,cy=W*.55,H*.46
    r=np.sqrt(((x-cx)/(W*.62))**2+((y-cy)/(H*.7))**2)
    glow=np.exp(-(r**2)*4)[...,None]
    base += glow*np.array([18,10,28])
    noise=np.random.default_rng(abs(hash(name))%2**32).normal(0,5,(H,W,1))
    base+=noise
    base=np.clip(base,0,255).astype(np.uint8)
    im=Image.fromarray(base,'RGB')
    d=ImageDraw.Draw(im,'RGBA')
    # distant pillars / silhouettes
    for i in range(18):
        px=int((i+random.random())*W/18); ph=random.randint(120,480); pw=random.randint(35,110)
        d.polygon([(px,H*.72),(px+pw,H*.72),(px+pw*.8,H*.72-ph),(px+pw*.25,H*.72-ph-random.randint(20,120))],fill=(3,2,10,210))
    # rings / eclipse / aura
    for rad,alpha in [(360,20),(260,30),(165,45)]:
        d.ellipse((cx-rad,cy-rad,cx+rad,cy+rad),outline=(170,130,255,alpha),width=5)
    for _ in range(900):
        px=random.randrange(W); py=random.randrange(int(H*.72)); rr=random.choice([1,1,2,3,5])
        a=random.randint(25,100); d.ellipse((px-rr,py-rr,px+rr,py+rr),fill=(180,160,255,a))
    # horizon
    d.rectangle((0,int(H*.72),W,H),fill=(2,2,8,110))
    d.text((55,55),label,fill=(235,230,255,150),stroke_width=2,stroke_fill=(0,0,0,130))
    im=im.filter(ImageFilter.GaussianBlur(0.25))
    im.save(os.path.join(root,name+'.webp'),'WEBP',quality=88,method=6)
# large high quality textures
for name,seed in [('world_clouds',21),('world_runes',22),('world_particles',23),('world_shadow_fog',24),('world_crystal_field',25),('world_stars_dense',26)]:
    rng=np.random.default_rng(seed)
    arr=rng.random((1536,1536,3))*255
    # smooth via PIL resized noise
    small=Image.fromarray(arr.astype('uint8')).resize((384,384),Image.Resampling.BICUBIC).resize((1536,1536),Image.Resampling.BICUBIC)
    d=ImageDraw.Draw(small,'RGBA')
    for _ in range(700):
        x=random.randrange(1536); y=random.randrange(1536); r=random.randint(1,8)
        d.ellipse((x-r,y-r,x+r,y+r),fill=(170,140,255,random.randint(20,120)))
    small.save(os.path.join(root,name+'.webp'),'WEBP',quality=90,method=6)
# synthesize 3 useful audio loops
def tone(path,dur,base,mod):
    sr=22050; n=int(sr*dur); frames=[]
    for i in range(n):
        t=i/sr
        env=min(1,t*2,(dur-t)*2)
        v=(0.42*math.sin(2*math.pi*base*t)+0.18*math.sin(2*math.pi*(base*1.5)*t)+0.12*math.sin(2*math.pi*(base*0.5)*t))
        v+=0.08*math.sin(2*math.pi*mod*t*t)
        v*=max(0,env)*0.6
        frames.append(struct.pack('<h',int(max(-1,min(1,v))*32767)))
    with wave.open(path,'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(b''.join(frames))
tone(os.path.join(root,'world_pulse.wav'),42,55,0.7)
tone(os.path.join(root,'eclipse_rumble.wav'),28,38,1.1)
tone(os.path.join(root,'ascension_chime.wav'),24,220,0.35)
# Modify HTML
p='/mnt/data/c11/app/src/main/assets/index.html'
s=open(p,encoding='utf-8').read()
# add world screen before inventory
needle='<section class="card section shadow-screen" data-shadow-screen="inventory">'
world_html='''<section class="card section shadow-screen" data-shadow-screen="world">\n<div class="section-head"><div><div class="section-title">LIVING WORLD // REALM STATE</div><div class="section-sub">The territory responds to the character instead of remaining a static background.</div></div><span class="v6-chip" id="worldPhase">NIGHT</span></div>\n<div class="world-stage" id="worldStage"><img id="worldScene" src="assets/world_night.webp" alt="Living Shadow System world"><div class="world-overlay"><div class="world-kicker">LIVE REALM TELEMETRY</div><div class="world-title" id="worldTitle">SHADOW NIGHT</div><div class="world-desc" id="worldDesc">The world is quiet. Your next action will change its state.</div><div class="world-chips"><span id="worldWeather">CLEAR</span><span id="worldResonance">RESONANCE 0</span><span id="worldCorruption">CORRUPTION 0%</span></div></div></div>\n<div class="world-grid"><div class="world-stat"><b id="worldClock">00:00</b><small>WORLD PHASE</small></div><div class="world-stat"><b id="worldAura">0</b><small>AURA PRESSURE</small></div><div class="world-stat"><b id="worldHeat">0</b><small>EXECUTION HEAT</small></div><div class="world-stat"><b id="worldEvent">NONE</b><small>ACTIVE EVENT</small></div></div>\n<div class="event-banner" id="worldEventBanner"><b>WORLD EVENT</b><span>Awaiting the next environmental shift.</span></div>\n</section>\n\n'''
s=s.replace(needle,world_html+needle)
# nav add world, replacing 8 nav items grid issue handled CSS
s=s.replace('<button class="nav-item" data-screen="inventory">','<button class="nav-item" data-screen="world"><span class="nav-icon">◉</span><span class="nav-label">WORLD</span></button><button class="nav-item" data-screen="inventory">')
# css append
css='''<style>\n.world-stage{position:relative;min-height:330px;border-radius:24px;overflow:hidden;border:1px solid rgba(145,100,255,.22);background:#04030a;box-shadow:0 20px 80px rgba(0,0,0,.55)}\n.world-stage:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 35%,rgba(3,2,10,.85));pointer-events:none}.world-stage img{width:100%;height:330px;object-fit:cover;display:block;transition:filter .8s,transform 6s}.world-overlay{position:absolute;left:22px;right:22px;bottom:18px;z-index:2}.world-kicker{font-size:10px;letter-spacing:3px;color:#bca9ff}.world-title{font-size:30px;font-weight:900;letter-spacing:2px}.world-desc{max-width:650px;color:#c5bfd6;margin:5px 0 10px}.world-chips{display:flex;gap:7px;flex-wrap:wrap}.world-chips span{font-size:10px;letter-spacing:1.4px;padding:6px 9px;border:1px solid rgba(150,120,255,.22);border-radius:999px;background:rgba(5,4,13,.72)}.world-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:12px}.world-stat{padding:15px;border:1px solid rgba(150,120,255,.15);border-radius:16px;background:rgba(8,6,18,.72)}.world-stat b{display:block;font-size:20px}.world-stat small{color:#8e879d;font-size:9px;letter-spacing:1.5px}.event-banner{margin-top:12px;padding:14px 16px;border-radius:16px;border:1px solid rgba(145,100,255,.2);background:linear-gradient(90deg,rgba(90,50,150,.16),rgba(20,12,40,.35));display:flex;justify-content:space-between;gap:10px}.event-banner b{font-size:10px;letter-spacing:2px}.event-banner span{color:#aaa2b9;font-size:12px}@media(max-width:560px){.world-grid{grid-template-columns:repeat(2,1fr)}.world-stage,.world-stage img{min-height:280px;height:280px}.world-title{font-size:24px}.event-banner{display:block}.event-banner span{display:block;margin-top:5px}}</style>'''
s=s.replace('</head>',css+'</head>')
# extend state defaults and load
s=s.replace("recoveryTokens:0\n});","recoveryTokens:0,world:{phase:'NIGHT',weather:'CLEAR',resonance:0,corruption:0,heat:0,event:'NONE',lastEventDay:-1}\n});")
s=s.replace("s.recoveryTokens=Number(parsed.recoveryTokens||0);","s.recoveryTokens=Number(parsed.recoveryTokens||0);s.world=Object.assign(base.world,parsed.world||{});")
# add world funcs before renderShadowSystems
marker='function renderShadowSystems(){'
world_js=r'''const WORLD_EVENTS=[
 {key:'ECLIPSE',name:'ECLIPSE VEIL',desc:'A rare veil covers the realm. Aura pressure rises and every completed quest resonates harder.',img:'assets/world_eclipse.webp',weather:'ECLIPSE'},
 {key:'STORM',name:'VOID STORM',desc:'The territory becomes unstable. Pressure quests generate extra execution heat.',img:'assets/world_storm.webp',weather:'STORM'},
 {key:'EMBER',name:'EMBERFALL',desc:'The forge wakes. Physical and focus execution leaves a visible ember trail.',img:'assets/world_pressure.webp',weather:'EMBER'},
 {key:'QUIET',name:'SHADOW QUIET',desc:'The realm settles. Recovery actions become more valuable.',img:'assets/world_night.webp',weather:'QUIET'}
];
function worldPhase(){const h=new Date().getHours();return h<6?'VOID':h<12?'DAWN':h<18?'DAY':'NIGHT'}
function worldEventForDay(){const d=currentDay(); if(d===89)return WORLD_EVENTS[0]; if(d===90)return {key:'ASCENSION',name:'ASCENSION SKY',desc:'The realm opens for the final audit. Every proof and capability becomes part of the record.',img:'assets/world_ascension.webp',weather:'ASCENSION'}; return WORLD_EVENTS[Math.floor(d/3)%WORLD_EVENTS.length]}
function updateWorldState(){const d=currentDay(), ev=worldEventForDay(); state.world=state.world||defaults().world; state.world.phase=worldPhase(); state.world.event=ev.name; state.world.weather=ev.weather; state.world.resonance=Math.min(999, totalDone()*2 + state.skillPoints*8 + (state.proofs||0)*12 + (state.bossDamage||0)); state.world.corruption=Math.max(0,Math.min(100,Math.round(dungeonThreat()*.65 - state.world.resonance/45))); state.world.heat=Math.min(999, totalDone()+state.focusMinutes/5+(state.bossDamage||0)*2); state.world.lastEventDay=d; }
function renderWorld(){updateWorldState();const ev=worldEventForDay();const img=document.getElementById('worldScene');if(img){img.src=ev.img;img.style.filter=state.world.corruption>60?'saturate(.75) contrast(1.15)':'saturate(1.05)';img.style.transform='scale('+(1.02+Math.min(0.04,state.world.resonance/25000))+')'}; const set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v};set('worldPhase',state.world.phase);set('worldTitle',ev.name);set('worldDesc',ev.desc);set('worldWeather',state.world.weather);set('worldResonance','RESONANCE '+state.world.resonance);set('worldCorruption','CORRUPTION '+state.world.corruption+'%');set('worldClock',String(new Date().getHours()).padStart(2,'0')+':'+String(new Date().getMinutes()).padStart(2,'0'));set('worldAura',auraPower());set('worldHeat',state.world.heat);set('worldEvent',ev.key);const b=document.getElementById('worldEventBanner');if(b)b.innerHTML='<b>WORLD EVENT · '+ev.key+'</b><span>'+ev.desc+'</span>';persist()}
'''
s=s.replace(marker,world_js+marker)
# call render world in deep render if exists, otherwise main render
s=s.replace('function renderShadowSystems(){renderEnvironment();renderRankVisual();','function renderShadowSystems(){renderEnvironment();renderRankVisual();renderWorld();')
# if deep wrapper overwrites, inject into deepRenderShadowSystems body start
s=s.replace('function deepRenderShadowSystems(){','function deepRenderShadowSystems(){renderWorld();')
# add nav mapping and ensure screen sections visible through existing router (data-shadow-screen works)
# fix grid for 9 nav items
s=s.replace('grid-template-columns:repeat(5,1fr);','grid-template-columns:repeat(9,minmax(62px,1fr));')
# version key and app version handled outside
open(p,'w',encoding='utf-8').write(s)
