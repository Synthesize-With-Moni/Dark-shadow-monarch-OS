from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import math, random, os, wave, struct
random.seed(10)
out='/mnt/data/c10/app/src/main/assets/assets'; os.makedirs(out,exist_ok=True)
W,H=2048,1152

def scene(name, title, subtitle, c0, c1, c2, seed):
    palette=(c0,c1,c2)
    random.seed(seed)
    im=Image.new('RGB',(W,H),palette[0]); p=im.load()
    for y in range(H):
        t=y/H
        for x in range(W):
            r=math.hypot(x-W*.5,y-H*.5)/max(W,H)
            glow=max(0,1-r*1.8)
            n=random.random()*3
            c=[]
            for i in range(3): c.append(int(palette[0][i]*(1-t)+palette[1][i]*t + palette[2][i]*glow + n))
            p[x,y]=tuple(max(0,min(255,v)) for v in c)
    d=ImageDraw.Draw(im,'RGBA')
    # eclipse
    cx,cy=int(W*.72),int(H*.30); R=260
    d.ellipse((cx-R,cy-R,cx+R,cy+R),fill=(4,3,10,230))
    d.ellipse((cx-R-10,cy-R-10,cx+R+10,cy+R+10),outline=(*palette[2],170),width=18)
    # architecture pillars / horizon
    for i in range(12):
        x=120+i*170+random.randint(-30,30); w=random.randint(45,95); h=random.randint(220,520)
        d.rectangle((x,H-150-h,x+w,H-150),fill=(2,2,8,180),outline=(*palette[2],70),width=3)
    # particles
    for _ in range(900):
        x=random.randrange(W); y=random.randrange(H); a=random.randrange(35,180); s=random.choice([1,1,2,3,5])
        d.ellipse((x,y,x+s,y+s),fill=(*palette[2],a))
    # title plate
    d.rounded_rectangle((70,H-250,900,H-65),30,fill=(2,2,8,180),outline=(*palette[2],120),width=3)
    d.text((105,H-215),title,fill=(235,230,255,240),stroke_width=1,stroke_fill=(0,0,0,180))
    d.text((105,H-155),subtitle,fill=(180,165,220,210))
    im=im.filter(ImageFilter.GaussianBlur(0.15))
    im.save(os.path.join(out,name),'WEBP',quality=94,method=6)

scene('env_shadow_citadel.webp','SHADOW CITADEL','AWAKENING // THE FIRST TERRITORY',(5,4,14),(25,20,38),(115,65,190),21)
scene('env_void_corridor.webp','VOID CORRIDOR','FOUNDATION // NO RETURN',(4,3,11),(14,8,30),(90,55,210),22)
scene('env_pressure_forge.webp','PRESSURE FORGE','PRESSURE // HEAT CREATES FORM',(8,3,9),(30,7,16),(180,35,65),23)
scene('env_eclipse_throne.webp','ECLIPSE THRONE','EVOLUTION // COMMAND THE SHADOW',(3,3,9),(18,7,30),(95,55,230),24)
scene('env_monarch_domain.webp','MONARCH DOMAIN','MONARCH // PRESENCE BECOMES POWER',(2,2,7),(15,8,28),(110,80,255),25)
scene('env_ascension_gate.webp','ASCENSION GATE','DAY 90 // BUILD THE SELF',(3,3,8),(10,6,22),(150,100,255),26)

# rank portraits as stylized silhouette plates
ranks=['E','D','C','B','A','S','MONARCH']
for idx,r in enumerate(ranks):
    im=Image.new('RGB',(1024,1024),(3,2,9)); d=ImageDraw.Draw(im,'RGBA')
    glow=(90+idx*18,55+idx*12,180+min(70,idx*10))
    for rr in range(430,220,-18): d.ellipse((512-rr,512-rr,512+rr,512+rr),outline=(*glow,max(10,130-(430-rr)//3)),width=8)
    # silhouette
    d.ellipse((392,200,632,440),fill=(2,2,7,245),outline=(*glow,200),width=5)
    d.polygon([(360,870),(390,500),(470,410),(554,410),(634,500),(664,870)],fill=(2,2,7,245),outline=(*glow,200))
    d.text((430,80),r,fill=(235,230,255,245),stroke_width=3,stroke_fill=(0,0,0,220))
    for _ in range(250):
        x=random.randrange(120,904); y=random.randrange(120,920); s=random.choice([2,3,5]); d.ellipse((x,y,x+s,y+s),fill=(*glow,random.randrange(20,130)))
    im.save(os.path.join(out,f'rank_{r.lower()}.webp'),'WEBP',quality=95,method=6)

# 2 texture atlases
for name,seed,base in [('environment_stars.webp',31,(8,6,20)),('environment_embers.webp',32,(18,4,8))]:
    random.seed(seed); im=Image.new('RGB',(2048,2048),base); d=ImageDraw.Draw(im,'RGBA')
    for _ in range(18000):
        x=random.randrange(2048); y=random.randrange(2048); s=random.choice([1,1,2,3,5,8]); a=random.randrange(30,150)
        col=(120,90,255,a) if 'stars' in name else (255,55,45,a)
        d.ellipse((x,y,x+s,y+s),fill=col)
    im.save(os.path.join(out,name),'WEBP',quality=92,method=6)

# ambient audio: 45s evolving low drone + shimmer, stereo PCM16 44.1k
sr=44100; sec=45; frames=sr*sec
for fname,kind in [('shadow_ambience.wav','shadow'),('monarch_ambience.wav','monarch')]:
    path=os.path.join(out,fname)
    with wave.open(path,'wb') as wf:
        wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(sr)
        for n in range(frames):
            t=n/sr
            fade=min(1,t/3,(sec-t)/3)
            base=42+8*math.sin(2*math.pi*0.07*t)
            if kind=='monarch': base=55+10*math.sin(2*math.pi*0.045*t)
            v=(math.sin(2*math.pi*base*t)*0.20 + math.sin(2*math.pi*(base*1.503)*t)*0.08)
            v += math.sin(2*math.pi*(110+7*math.sin(t*.17))*t)*0.03
            if n%997==0: v += random.uniform(-.06,.06)
            v*=fade
            s=max(-1,min(1,v))*0.55
            wf.writeframes(struct.pack('<hh',int(s*32767),int(s*32767)))
