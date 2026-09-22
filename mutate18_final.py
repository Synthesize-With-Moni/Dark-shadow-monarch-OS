from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math, random, wave, struct, shutil, zipfile, re, os

ROOT=Path('/mnt/data/c18')
HTML=ROOT/'app/src/main/assets/index.html'
AS=ROOT/'app/src/main/assets/assets'
AS.mkdir(parents=True,exist_ok=True)

# --- meaningful final-chamber visual library ---
random.seed(18090)
def make_scene(name, title, subtitle, seed, size=(1800,1100)):
    random.seed(seed)
    w,h=size
    im=Image.new('RGB',(w,h),(5,4,12))
    px=im.load()
    # cinematic radial/vertical gradient + subtle grain
    cx,cy=w*.52,h*.45
    for y in range(h):
        for x in range(w):
            dx=(x-cx)/w; dy=(y-cy)/h
            r=(dx*dx+dy*dy)**0.5
            glow=max(0,1-r*2.2)
            edge=max(0,1-abs(y/h-.5)*1.5)
            n=random.randint(0,5)
            px[x,y]=(min(28,int(4+20*glow)+n),min(18,int(3+12*glow)+n//2),min(52,int(12+40*glow+12*edge)+n))
    d=ImageDraw.Draw(im,'RGBA')
    # rings / eclipse / particles
    for i in range(12):
        rr=120+i*70
        d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),outline=(112,86,255,18),width=3)
    d.ellipse((cx-170,cy-170,cx+170,cy+170),fill=(3,2,8,235),outline=(180,120,255,170),width=5)
    for i in range(420):
        x=random.randrange(w); y=random.randrange(h); a=random.randrange(20,150); s=random.choice([1,1,2,2,3])
        d.ellipse((x,y,x+s,y+s),fill=(150,120,255,a))
    # horizon architecture
    base=int(h*.73)
    for i in range(13):
        x=i*w/13+random.randint(-40,40); ww=random.randint(70,170); hh=random.randint(80,300)
        d.rectangle((x,base-hh,x+ww,base),fill=(8,7,18,210),outline=(96,76,170,80),width=2)
    # title card
    d.rounded_rectangle((70,h-210,w-70,h-70),radius=28,fill=(3,3,10,180),outline=(145,115,255,90),width=2)
    d.text((105,h-185),title,fill=(235,230,255,255))
    d.text((105,h-135),subtitle,fill=(168,155,205,230))
    im.save(AS/name,quality=92)

scenes=[
('ascension_gate_final.webp','ASCENSION GATE','THE ARC HAS ENDED. THE RECORD REMAINS.',1),
('monarch_audit_final.webp','MONARCH AUDIT','90 DAYS OF REAL ACTION, REVIEWED.',2),
('identity_chamber_final.webp','IDENTITY CHAMBER','WHAT YOU BUILT BECOMES WHAT YOU CAN CARRY.',3),
('capability_crown_final.webp','CAPABILITY CROWN','SKILLS ARE SHOWN THROUGH EVIDENCE.',4),
('proof_constellation_final.webp','PROOF CONSTELLATION','PROJECTS, RECEIPTS, MILESTONES, REFLECTIONS.',5),
('before_after_final.webp','BEFORE / AFTER','THE BASELINE IS NO LONGER THE ENDPOINT.',6),
('arc_rewind_final.webp','ARC REWIND','DAY 01 → DAY 90.',7),
('legacy_vault_final.webp','LEGACY VAULT','THE DOSSIER IS PORTABLE.',8),
('monarch_domain_final.webp','MONARCH DOMAIN','NOT A GAME ENDING. A CAPABILITY RECORD.',9),
('final_seal_final.webp','FINAL SEAL','SEAL ONLY WHEN THE EVIDENCE IS TRUE.',10),
('dossier_cover_final.webp','MONARCH DOSSIER','A 90-DAY RECORD OF BECOMING.',11),
('return_to_reality_final.webp','RETURN','THE SYSTEM CLOSES. REAL LIFE CONTINUES.',12),
]
for args in scenes:
    p=AS/args[0]
    if not p.exists(): make_scene(*args)

# audio: final seal + soft chamber pulse
def make_wav(path, seconds, notes, seed):
    random.seed(seed); sr=44100; n=int(sr*seconds)
    with wave.open(str(path),'w') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
        frames=[]
        for i in range(n):
            t=i/sr
            amp=min(1,t/.8)*min(1,(seconds-t)/1.8)*0.22
            v=0
            for freq,weight in notes:
                v += math.sin(2*math.pi*freq*t)*weight
                v += math.sin(2*math.pi*(freq*2.01)*t)*weight*.13
            v += (random.random()-.5)*.008
            frames.append(struct.pack('<h',int(max(-1,min(1,v*amp))*32767)))
        wf.writeframes(b''.join(frames))
make_wav(AS/'ascension_seal.wav',18,[(110,1),(165,.6),(220,.45),(330,.25)],180)
make_wav(AS/'dossier_chamber.wav',24,[(55,1),(82.5,.6),(110,.4),(220,.15)],181)

html=HTML.read_text()
# CSS
css=r'''
<style id="mutation18-css">
.asc18-locked{filter:saturate(.45);opacity:.72}.asc18-grid{display:grid;grid-template-columns:1.25fr .75fr;gap:14px}.asc18-hero{position:relative;overflow:hidden;min-height:340px;border:1px solid rgba(170,130,255,.3);border-radius:28px;background:#05040c}.asc18-hero img{width:100%;height:340px;object-fit:cover;display:block;opacity:.72}.asc18-overlay{position:absolute;inset:0;padding:28px;display:flex;align-items:flex-end;background:linear-gradient(180deg,transparent 25%,rgba(3,2,9,.96) 100%)}.asc18-kicker{font:700 10px 'DM Mono';letter-spacing:2px;color:#a89bff}.asc18-title{font:900 34px Orbitron,system-ui;letter-spacing:1px;margin:8px 0}.asc18-sub{color:#b8afc9;max-width:720px;line-height:1.55}.asc18-chiprow{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}.asc18-chip{padding:7px 10px;border:1px solid rgba(150,120,255,.25);border-radius:999px;background:rgba(20,16,35,.72);font:700 9px 'DM Mono';color:#d7d0e8}.asc18-audit{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}.asc18-metric{padding:14px;border-radius:18px;background:rgba(255,255,255,.025);border:1px solid rgba(160,130,255,.15)}.asc18-metric span{display:block;color:#817894;font:700 9px 'DM Mono';letter-spacing:1px}.asc18-metric b{display:block;font:800 22px Orbitron;margin-top:6px}.asc18-bar{height:7px;border-radius:99px;background:#11101b;overflow:hidden;margin-top:9px}.asc18-bar em{display:block;height:100%;width:0;background:linear-gradient(90deg,#684bff,#c48cff,#67e8ff);transition:width .5s}.asc18-section{margin-top:14px;padding:18px;border-radius:22px;background:rgba(255,255,255,.022);border:1px solid rgba(160,130,255,.13)}.asc18-section h3{margin:0 0 5px;font:800 13px Orbitron;letter-spacing:1px}.asc18-section p{color:#8f879f;font-size:11px;line-height:1.55}.asc18-timeline{display:grid;grid-template-columns:repeat(7,1fr);gap:7px;margin-top:14px}.asc18-node{min-height:105px;padding:10px;border-radius:15px;border:1px solid rgba(150,120,255,.12);background:#0a0911;cursor:pointer;text-align:left}.asc18-node.active{border-color:rgba(130,105,255,.6);box-shadow:0 0 24px rgba(110,80,255,.12)}.asc18-node.complete{background:rgba(100,70,180,.08)}.asc18-node b{display:block;font:800 9px Orbitron}.asc18-node small{display:block;color:#777087;font-size:8px;margin-top:7px;line-height:1.4}.asc18-compare{display:grid;grid-template-columns:1fr 1fr;gap:10px}.asc18-box{min-height:150px;padding:15px;border-radius:18px;border:1px solid rgba(150,120,255,.12);background:#080710}.asc18-box b{font:800 9px 'DM Mono';color:#9e91ba}.asc18-box p{white-space:pre-wrap;color:#d8d1e4;line-height:1.6;font-size:11px;margin:10px 0}.asc18-proofgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.asc18-proof{padding:12px;border-radius:16px;background:rgba(255,255,255,.02);border:1px solid rgba(150,120,255,.1)}.asc18-proof b{font-size:11px}.asc18-proof small{display:block;color:#777087;margin-top:5px}.asc18-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}.asc18-seal{position:relative;overflow:hidden;text-align:center;padding:28px;border-radius:26px;border:1px solid rgba(200,170,255,.3);background:radial-gradient(circle at 50% 20%,rgba(110,80,255,.14),transparent 55%),#07060d}.asc18-seal img{width:min(280px,70%);border-radius:22px;opacity:.8}.asc18-seal h2{font:900 24px Orbitron;margin:8px 0}.asc18-seal p{color:#928aa0;font-size:11px;line-height:1.5}.asc18-sealed{border-color:rgba(120,255,210,.35);box-shadow:0 0 35px rgba(90,255,200,.08)}.asc18-modal{position:fixed;inset:0;z-index:10001;display:none;align-items:center;justify-content:center;padding:18px;background:rgba(0,0,0,.82);backdrop-filter:blur(18px)}.asc18-modal.open{display:flex}.asc18-modal-box{width:min(900px,100%);max-height:90vh;overflow:auto;background:#07060e;border:1px solid rgba(160,130,255,.28);border-radius:28px;box-shadow:0 35px 100px rgba(0,0,0,.8)}.asc18-modal-box img{width:100%;max-height:420px;object-fit:cover}.asc18-modal-copy{padding:22px}.asc18-modal-copy h2{font:900 26px Orbitron}.asc18-finalword{font:900 17px Orbitron;letter-spacing:2px;color:#ddd4ff}.asc18-note{font-size:10px;color:#777087;line-height:1.55}.asc18-receipt{display:flex;justify-content:space-between;gap:12px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,.06)}.asc18-receipt span{font-size:10px;color:#bdb5ca}.asc18-receipt b{font-size:10px;color:#e4ddf1}@media(max-width:760px){.asc18-grid,.asc18-compare{grid-template-columns:1fr}.asc18-timeline{grid-template-columns:repeat(2,1fr)}.asc18-proofgrid{grid-template-columns:1fr}.asc18-title{font-size:26px}}
</style>
'''
html=html.replace('</head>',css+'</head>',1)
# add nav
needle='<button class="nav-item" data-screen="vault"><span class="nav-icon">▣</span><span class="nav-label">VAULT</span></button>'
repl=needle+'<button class="nav-item" data-screen="ascension"><span class="nav-icon">♕</span><span class="nav-label">ASCEND</span></button>'
html=html.replace(needle,repl,1)
# add shadow screen before main close: just before aside
section=r'''
<section class="card section shadow-screen" data-shadow-screen="ascension">
  <div class="asc18-grid">
    <div>
      <div class="asc18-hero"><img id="asc18Scene" src="assets/ascension_gate_final.webp" alt="Final Ascension Chamber"><div class="asc18-overlay"><div><div class="asc18-kicker">MUTATION 18 // FINAL SYSTEM</div><div class="asc18-title">MONARCH ASCENSION</div><div class="asc18-sub">The 90-day protocol ends here. The interface stops measuring a future character and audits the person who actually completed the work.</div><div class="asc18-chiprow"><span class="asc18-chip" id="asc18Day">DAY 01 / 90</span><span class="asc18-chip" id="asc18Status">ASCENSION LOCKED</span><span class="asc18-chip" id="asc18Integrity">INTEGRITY 0%</span></div></div></div></div>
      <div class="asc18-section"><h3>THE FINAL AUDIT</h3><p>Nothing here is awarded for merely opening screens. The final record is calculated from execution, capability practice, projects, evidence, reflections and the immutable day history.</p><div class="asc18-audit">
        <div class="asc18-metric"><span>EXECUTION</span><b id="asc18Execution">0%</b><div class="asc18-bar"><em id="asc18ExecutionBar"></em></div></div>
        <div class="asc18-metric"><span>CAPABILITY</span><b id="asc18Capability">0%</b><div class="asc18-bar"><em id="asc18CapabilityBar"></em></div></div>
        <div class="asc18-metric"><span>PROOF COVERAGE</span><b id="asc18Proof">0%</b><div class="asc18-bar"><em id="asc18ProofBar"></em></div></div>
        <div class="asc18-metric"><span>ARC INTEGRITY</span><b id="asc18IntegrityMetric">0%</b><div class="asc18-bar"><em id="asc18IntegrityBar"></em></div></div>
      </div></div>
    </div>
    <div>
      <div class="asc18-seal" id="asc18SealPanel"><img src="assets/final_seal_final.webp" alt="Final seal"><h2 id="asc18SealTitle">THE SEAL IS WAITING</h2><p id="asc18SealText">Reach Day 90, review the record, and seal only when the evidence represents reality.</p><div class="asc18-actions"><button class="control-btn primary" onclick="openAsc18Audit()">OPEN AUDIT</button><button class="control-btn" onclick="exportMonarchDossier18()">EXPORT DOSSIER</button></div></div>
      <div class="asc18-section"><h3>THE IDENTITY RECORD</h3><p>These statements are derived from the final record and can be edited before the seal, then frozen permanently.</p><input class="text-input" id="asc18Identity1" maxlength="140" placeholder="I learned to…"><input class="text-input" id="asc18Identity2" maxlength="140" placeholder="I can now reliably…" style="margin-top:8px"><input class="text-input" id="asc18Identity3" maxlength="140" placeholder="The thing I built that matters most is…" style="margin-top:8px"></div>
    </div>
  </div>
  <div class="asc18-section"><h3>90-DAY REWIND</h3><p>Seven immutable gates tell the story of the Arc. Completed gates can be entered again; future gates remain locked by time.</p><div class="asc18-timeline" id="asc18Timeline"></div></div>
  <div class="asc18-section"><h3>BEFORE → AFTER</h3><div class="asc18-compare"><div class="asc18-box"><b>BASELINE</b><p id="asc18Before">No baseline sealed.</p></div><div class="asc18-box"><b>DEMONSTRATED CAPABILITY</b><p id="asc18After">No final capability statement sealed.</p></div></div></div>
  <div class="asc18-section"><h3>PROOF CONSTELLATION</h3><p>The final dossier selects concrete records instead of inventing a score.</p><div class="asc18-proofgrid" id="asc18ProofGrid"></div></div>
  <div class="asc18-section"><h3>FINAL LEGACY</h3><div id="asc18Legacy" class="asc18-note">The Legacy Vault will activate after the final seal.</div><div class="asc18-actions"><button class="control-btn primary" onclick="sealAscension18()" id="asc18SealButton">SEAL FINAL FORM</button><button class="control-btn" onclick="exportMonarchDossier18()">EXPORT MONARCH DOSSIER</button><button class="control-btn" onclick="exportAsc18JSON()">EXPORT FINAL JSON</button></div></div>
</section>
<div class="asc18-modal" id="asc18Modal"><div class="asc18-modal-box"><img id="asc18ModalImg" src="assets/monarch_audit_final.webp" alt="Final audit chamber"><div class="asc18-modal-copy"><div class="asc18-kicker">FINAL AUDIT CHAMBER</div><h2 id="asc18ModalTitle">MONARCH AUDIT</h2><p id="asc18ModalText"></p><div id="asc18ModalReceipts"></div><div class="asc18-actions"><button class="control-btn primary" onclick="closeAsc18Audit()">RETURN</button><button class="control-btn" onclick="sealAscension18()">SEAL FINAL FORM</button></div></div></div></div>
'''
html=html.replace('</main>\n\n    <aside class="sidecol">',section+'</main>\n\n    <aside class="sidecol">',1)
# state init + functions before closing script, and router mapping patch
js=r'''
/* ================= MUTATION 18 // MONARCH ASCENSION ================= */
const ASC18_GATES=[
 {day:1,title:'AWAKENING',file:'assets/ascension_gate_final.webp',desc:'The original baseline. What could you reliably do before the Arc changed the pattern?'},
 {day:10,title:'FOUNDATION',file:'assets/monarch_audit_final.webp',desc:'The first repeated behaviors. What stopped being accidental?'},
 {day:25,title:'PRESSURE',file:'assets/identity_chamber_final.webp',desc:'The point where consistency met resistance.'},
 {day:45,title:'EVOLUTION',file:'assets/capability_crown_final.webp',desc:'The midpoint: capability begins to replace intention.'},
 {day:65,title:'ELITE',file:'assets/proof_constellation_final.webp',desc:'Output and evidence become the center of the record.'},
 {day:80,title:'MONARCH',file:'assets/before_after_final.webp',desc:'The final stretch: protect what was built and prepare the audit.'},
 {day:90,title:'ASCENSION',file:'assets/legacy_vault_final.webp',desc:'The final record. No restart, no cosmetic victory—only the evidence that exists.'}
];
function initAsc18(){if(!state.ascension18)state.ascension18={sealed:false,sealedAt:null,identity:['','',''],baseline:'',capability:'',integrity:0,viewed:[],legacyId:null};}
function asc18Day(){return Math.min(90,currentDay()+1)}
function asc18Metrics(){initAsc18();const d=asc18Day(),days=Math.max(1,d),hist=(state.dayStates||[]).slice(0,Math.max(0,d-1));const locked=hist.filter(Boolean).length;const execution=Math.round(Math.min(100,(totalDone()/Math.max(1,(d)*5))*100));const practice=(state.practiceLog||[]).reduce((s,x)=>s+Number(x.minutes||0),0);const cap=CAP15.length?Math.round(Math.min(100,(CAP15.reduce((s,c)=>s+masteryPct15(masteryObj(c[0])),0)/(CAP15.length*100))*100)):0;const ev=(state.evidence16||[]).length, projects=(state.projects16||[]).length, proofs=(state.proofEntries||[]).length;const proof=Math.round(Math.min(100,ev*3+projects*7+proofs*2+(state.proofs||0)*1));const reflections=state.arc17?Object.keys(state.arc17.reflections||{}).length:0;const sealedDays=locked;const integrity=Math.round(Math.min(100,execution*.35+cap*.25+Math.min(100,proof)*.2+Math.min(100,(reflections/7)*100)*.1+Math.min(100,(sealedDays/89)*100)*.1));const readiness=Math.round(Math.min(100,integrity));return{d,execution,cap,proof,integrity,readiness,practice,ev,projects,proofs,reflections,locked};}
function asc18IdentityValues(){return [document.getElementById('asc18Identity1')?.value||state.ascension18.identity[0]||'',document.getElementById('asc18Identity2')?.value||state.ascension18.identity[1]||'',document.getElementById('asc18Identity3')?.value||state.ascension18.identity[2]||''];}
function openAsc18Audit(){initAsc18();const m=asc18Metrics();document.getElementById('asc18Modal').classList.add('open');document.getElementById('asc18ModalImg').src=m.d>=90?'assets/monarch_domain_final.webp':'assets/monarch_audit_final.webp';document.getElementById('asc18ModalTitle').textContent=m.d>=90?'MONARCH AUDIT // READY TO SEAL':'MONARCH AUDIT // PREVIEW';document.getElementById('asc18ModalText').textContent=m.d>=90?'The Arc has reached its final day. Review the receipts below, then seal the final identity record.':'The final chamber is visible early so the player understands what the 90-day system is building toward. It cannot be sealed before Day 90.';document.getElementById('asc18ModalReceipts').innerHTML=[['EXECUTION',m.execution+'%'],['CAPABILITY',m.cap+'%'],['PROOF COVERAGE',m.proof+'%'],['ARC INTEGRITY',m.integrity+'%'],['PROJECT DOSSIERS',m.projects],['EVIDENCE RECEIPTS',m.ev],['SEALED REFLECTIONS',m.reflections+'/7']].map(x=>`<div class="asc18-receipt"><span>${x[0]}</span><b>${x[1]}</b></div>`).join('');}
function closeAsc18Audit(){document.getElementById('asc18Modal')?.classList.remove('open');}
function sealAscension18(){initAsc18();const m=asc18Metrics();if(m.d<90){toast('ASCENSION LOCKED','The final form can only be sealed on Day 90. The Arc is still alive.');return;}if(state.ascension18.sealed){toast('FINAL FORM SEALED','The Monarch record is immutable. Export it or review the legacy.');return;}const vals=asc18IdentityValues();if(vals.some(x=>x.trim().length<8)){toast('IDENTITY INCOMPLETE','Write all three final statements before sealing the record.');return;}state.ascension18.sealed=true;state.ascension18.sealedAt=new Date().toISOString();state.ascension18.identity=vals;state.ascension18.baseline=state.beforeAfter16?.before||'No baseline statement was sealed.';state.ascension18.capability=state.beforeAfter16?.after||vals[1];state.ascension18.integrity=m.integrity;state.ascension18.legacyId='MONARCH-'+Date.now().toString(36).toUpperCase();state.proofs=(state.proofs||0)+10;state.xp+=500;state.artifacts=state.artifacts||[];if(!state.artifacts.includes('monarch_crown'))state.artifacts.push('monarch_crown');addEvent('FINAL FORM SEALED · MONARCH ASCENSION','♕');persist();playSystemSound('level');confetti(90);renderAll();closeAsc18Audit();toast('MONARCH ASCENSION SEALED','The 90-day record is now a permanent legacy artifact.');}
function exportAsc18JSON(){initAsc18();const payload={export:'SHADOW SYSTEM // MONARCH ASCENSION',version:1,generated:new Date().toISOString(),metrics:asc18Metrics(),final:state.ascension18,projects:state.projects16||[],evidence:state.evidence16||[],practice:state.practiceLog||[],mastery:state.mastery||{},dayStates:state.dayStates||[],events:state.events||[],arc17:state.arc17||null};const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='shadow-monarch-final-'+todayKey()+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),500);}
function exportMonarchDossier18(){initAsc18();const m=asc18Metrics(),s=state.ascension18,projects=state.projects16||[],evidence=state.evidence16||[],mastery=state.mastery||{};const capRows=CAP15.map(c=>{const x=mastery[c[0]]||{};return `<tr><td>${escapeHTML(c[1])}</td><td>${masteryTier15(x)}</td><td>${x.minutes||0} min</td><td>${x.evidence||0}</td></tr>`}).join('');const projRows=projects.map(p=>`<section><h3>${escapeHTML(p.name)}</h3><p>${escapeHTML(p.goal||'')}</p><small>${escapeHTML(p.status||'OPEN')} · ${p.evidence||0} evidence receipts</small></section>`).join('')||'<p>No project dossiers recorded.</p>';const evRows=evidence.slice(-100).map(x=>`<li>Day ${x.day||'?'} — ${escapeHTML(x.text||'')}</li>`).join('')||'<li>No evidence receipts.</li>';const html=`<!doctype html><html><head><meta charset="utf-8"><title>MONARCH DOSSIER</title><style>body{margin:0;background:#07060d;color:#eee;font-family:Inter,Arial;padding:42px;line-height:1.55}main{max-width:1000px;margin:auto}h1{font:900 44px Arial;letter-spacing:3px}h2{font-size:22px;margin-top:40px}h3{color:#d8ccff}small{color:#928aa0}section,.metric{border:1px solid #2b2540;border-radius:18px;padding:18px;margin:12px 0;background:#0b0913}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.metric b{display:block;font-size:25px}.seal{border:1px solid #6f5aa6;padding:28px;border-radius:22px;text-align:center;margin:25px 0}.seal b{font-size:25px;letter-spacing:3px}table{width:100%;border-collapse:collapse}td,th{padding:9px;border-bottom:1px solid #282235;text-align:left}li{margin:7px 0}</style></head><body><main><div class="seal"><b>SHADOW SYSTEM // MONARCH DOSSIER</b><p>90-DAY WINTER ARC FINAL RECORD</p><small>${s.sealed?'SEALED · '+s.sealedAt:'UNSEALED PREVIEW'}</small></div><div class="grid"><div class="metric"><small>EXECUTION</small><b>${m.execution}%</b></div><div class="metric"><small>CAPABILITY</small><b>${m.cap}%</b></div><div class="metric"><small>PROOF</small><b>${m.proof}%</b></div><div class="metric"><small>INTEGRITY</small><b>${m.integrity}%</b></div></div><h2>IDENTITY</h2><section><p>${escapeHTML(s.identity?.[0]||'')}</p><p>${escapeHTML(s.identity?.[1]||'')}</p><p>${escapeHTML(s.identity?.[2]||'')}</p></section><h2>BEFORE → AFTER</h2><section><h3>BASELINE</h3><p>${escapeHTML(s.baseline||state.beforeAfter16?.before||'Not sealed')}</p><h3>DEMONSTRATED CAPABILITY</h3><p>${escapeHTML(s.capability||state.beforeAfter16?.after||'Not sealed')}</p></section><h2>CAPABILITY RECORD</h2><table><tr><th>Capability</th><th>Tier</th><th>Practice</th><th>Evidence</th></tr>${capRows}</table><h2>PROJECT DOSSIERS</h2>${projRows}<h2>EVIDENCE RECEIPTS</h2><ul>${evRows}</ul><h2>FINAL LEGACY ID</h2><section><b>${escapeHTML(s.legacyId||'UNSEALED')}</b></section><h2>FINAL STATEMENT</h2><section><p>The system closes here. Real life does not.</p><p>The record is portable. The capability is yours.</p></section></main></body></html>`;const blob=new Blob([html],{type:'text/html'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='MONARCH-DOSSIER-'+todayKey()+'.html';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),500);}
function renderAsc18(){initAsc18();const m=asc18Metrics(),s=state.ascension18,set=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v};set('asc18Day','DAY '+String(m.d).padStart(2,'0')+' / 90');set('asc18Status',s.sealed?'FINAL FORM SEALED':m.d>=90?'READY TO SEAL':'ASCENSION LOCKED');set('asc18Integrity',s.sealed?'SEALED':('INTEGRITY '+m.integrity+'%'));set('asc18Execution',m.execution+'%');set('asc18Capability',m.cap+'%');set('asc18Proof',m.proof+'%');set('asc18IntegrityMetric',m.integrity+'%');['Execution','Capability','Proof','Integrity'].forEach((x,i)=>{const e=document.getElementById('asc18'+x+'Bar');if(e)e.style.width=[m.execution,m.cap,m.proof,m.integrity][i]+'%'});set('asc18SealTitle',s.sealed?'MONARCH RECORD SEALED':m.d>=90?'FINAL FORM READY':'THE SEAL IS WAITING');set('asc18SealText',s.sealed?'This record is immutable. Export it, keep it, and return to real life.':m.d>=90?'The final day has arrived. Review every receipt before sealing.':'Reach Day 90. The chamber is intentionally visible before it becomes available.');const panel=document.getElementById('asc18SealPanel');if(panel)panel.classList.toggle('asc18-sealed',s.sealed);const btn=document.getElementById('asc18SealButton');if(btn){btn.disabled=s.sealed||m.d<90;btn.textContent=s.sealed?'FINAL FORM SEALED':m.d>=90?'SEAL FINAL FORM':'LOCKED UNTIL DAY 90';}const before=document.getElementById('asc18Before'),after=document.getElementById('asc18After');if(before)before.textContent=s.baseline||state.beforeAfter16?.before||'No baseline sealed.';if(after)after.textContent=s.capability||state.beforeAfter16?.after||'No final capability statement sealed.';const ids=['asc18Identity1','asc18Identity2','asc18Identity3'];if(s.identity&&s.identity.length){ids.forEach((id,i)=>{const e=document.getElementById(id);if(e&&document.activeElement!==e)e.value=s.identity[i]||'';if(e)e.disabled=s.sealed;});}const tl=document.getElementById('asc18Timeline');if(tl)tl.innerHTML=ASC18_GATES.map(g=>{const unlocked=g.day<=m.d,viewed=(s.viewed||[]).includes(g.day);return `<button class="asc18-node ${unlocked?'active':''} ${g.day<m.d?'complete':''}" onclick="openAsc18Gate(${g.day})"><b>D${String(g.day).padStart(2,'0')} · ${g.title}</b><small>${unlocked?(viewed?'VIEWED · ENTER AGAIN':'ENTER CHAMBER'):'LOCKED · REACH DAY '+g.day}</small></button>`}).join('');const pg=document.getElementById('asc18ProofGrid');if(pg){const arr=[['PROJECTS',m.projects,'Concrete things built'],['EVIDENCE',m.ev,'Receipts in the archive'],['PRACTICE',m.practice+'m','Deliberate practice'],['REFLECTIONS',m.reflections+'/7','Chapter reflections'],['LOCKED DAYS',m.locked,'Immutable history'],['LEGACY',s.legacyId||'PENDING','Final identity record']];pg.innerHTML=arr.map(x=>`<div class="asc18-proof"><b>${x[0]}</b><strong style="display:block;font:800 20px Orbitron;margin-top:6px">${escapeHTML(String(x[1]))}</strong><small>${x[2]}</small></div>`).join('');}const lg=document.getElementById('asc18Legacy');if(lg)lg.innerHTML=s.sealed?`<div class="asc18-finalword">${escapeHTML(s.legacyId||'MONARCH')}</div><p class="asc18-note">The final record was sealed ${escapeHTML(s.sealedAt||'')}. It is no longer a quest. It is an archive.</p>`:'<p class="asc18-note">No legacy record exists yet. The system will create one only after the Day 90 audit is sealed.</p>';}
function openAsc18Gate(day){const g=ASC18_GATES.find(x=>x.day===day);if(!g)return;const m=asc18Metrics();if(day>m.d){toast('CHAMBER LOCKED','Reach Day '+String(day).padStart(2,'0')+' before entering this gate.');return;}initAsc18();state.ascension18.viewed=Array.from(new Set([...(state.ascension18.viewed||[]),day]));persist();const modal=document.getElementById('asc18Modal');document.getElementById('asc18ModalImg').src=g.file;document.getElementById('asc18ModalTitle').textContent='DAY '+String(day).padStart(2,'0')+' // '+g.title;document.getElementById('asc18ModalText').textContent=g.desc;modal.classList.add('open');}
// preserve older state and add the final subsystem without invalidating saves
initAsc18();
const _oldRenderAll18=renderAll;renderAll=function(){_oldRenderAll18();renderAsc18();};
const _oldSwitch18=switchSystemScreen;switchSystemScreen=function(name){if(name==='ascension'){initAsc18();renderAsc18();}return _oldSwitch18(name);};
'''
# insert JS before last script close
idx=html.rfind('</script>')
html=html[:idx]+js+'\n'+html[idx:]
# patch screen labels map
html=html.replace("more:'SYSTEM // COMMAND'","more:'SYSTEM // COMMAND',ascension:'ASCENSION // FINAL FORM'",1)
# update Android version
b=(ROOT/'app/build.gradle').read_text().replace("versionCode 13","versionCode 14").replace("versionName '3.1.0'","versionName '4.0.0'")
(ROOT/'app/build.gradle').write_text(b)
# README
readme='''# Shadow System // Winter Arc — Monster Change 18\n\n## Final Mutation — Monarch Ascension\n\nMutation 18 is the final 90-day audit and legacy layer. It turns the end of the Arc into a permanent record of real-world capability rather than a game-complete screen.\n\n### Major systems\n- Monarch Ascension final chamber\n- 90-day audit: execution, capability, proof coverage, Arc integrity\n- Seven-gate 90-day rewind\n- Before → After identity record\n- Final identity statements\n- Proof constellation and capability record\n- Immutable final seal available only on Day 90\n- Legacy ID generated at final seal\n- Portable Monarch Dossier HTML export\n- Final JSON archive export\n- Final chamber / audit / identity / proof / legacy visual library\n- Final seal and dossier chamber audio\n\n### Design law\nThe final mutation does not declare that a player “won.” It records what the player actually built, practiced, proved and reflected on. The system closes; real life continues.\n\nAndroid version: 4.0.0 / versionCode 14.\n\n## 18 / 18 COMPLETE\n'''
(ROOT/'README.md').write_text(readme)
# syntax check
script=Path('/tmp/shadow18.js')
text=re.search(r'<script>([\s\S]*)</script>',html)
# there are multiple scripts; use concatenate all non-src scripts
scripts=re.findall(r'<script[^>]*>([\s\S]*?)</script>',html)
script.write_text('\n'.join(scripts))
os.system('node --check /tmp/shadow18.js')
HTML.write_text(html)
# package
out='/mnt/data/ShadowSystem_WinterArc_Monster_Change18_FINAL.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in ROOT.rglob('*'):
        if p.is_file() and p.name not in ['ShadowSystem_WinterArc_Monster_Change18_FINAL.zip']:
            z.write(p,p.relative_to(ROOT))
print(out, os.path.getsize(out))
print('assets',len(list(AS.iterdir())), 'html',HTML.stat().st_size)
