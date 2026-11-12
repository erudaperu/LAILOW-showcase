"""Render a finite visual study directly from the public synthetic fixture.

Optional documentation tool: requires Pillow >= 10.1. The analytics demo itself
has no third-party dependency. Available system fonts affect appearance only.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sys, math, json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from lailow_demo.sample import make_sample
from lailow_demo.analytics import summarize, opportunities
rows=make_sample(); totals=summarize(rows)
INK='#0D1117'; PANEL='#151C25'; LINE='#293441'; TEXT='#F2F4F5'; MUTED='#A1ADB9'; CYAN='#69D4D0'; GOLD='#E7B785'
REG='/usr/share/fonts/google-noto/NotoSans-Regular.ttf'; BOLD='/usr/share/fonts/google-noto/NotoSans-Bold.ttf'; MONO='/usr/share/fonts/google-noto/NotoSansMono-Regular.ttf'
def font(size,bold=False,mono=False):
    candidates=[MONO if mono else BOLD if bold else REG, 'DejaVuSansMono.ttf' if mono else 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf']
    for candidate in candidates:
        try: return ImageFont.truetype(candidate,size)
        except OSError: pass
    return ImageFont.load_default(size=size)
def draw_frame(day):
 im=Image.new('RGB',(1400,760),INK);d=ImageDraw.Draw(im)
 def txt(x,y,t,size=22,c=TEXT,b=False,m=False):d.text((x,y),t,font=font(size,b,m),fill=c)
 def line(a,b,c=LINE,w=1):d.line([a,b],fill=c,width=w)
 def box(x,y,w,h,c=PANEL):d.rounded_rectangle((x,y,x+w,y+h),radius=10,fill=c)
 txt(40,27,'FEATURED PROJECT',17,GOLD,True)
 txt(38,53,'LAILOW',68,TEXT,True)
 txt(42,143,'Campaign intelligence',25,MUTED)
 txt(42,188,'I make the numbers',28,TEXT,True)
 txt(42,229,'worth questioning.',28,TEXT,True)
 line((40,292),(344,292))
 txt(42,320,'42',55,TEXT,True);txt(42,386,'fictional records',20,MUTED)
 txt(215,320,'03',55,TEXT,True);txt(215,386,'campaigns',20,MUTED)
 txt(42,462,'PYTHON / ANALYTICS',17,CYAN,True)
 txt(42,496,'TRACEABLE SIGNALS',17,CYAN,True)
 txt(42,643,'SYNTHETIC DATA',18,GOLD,True)
 txt(42,679,'Animated explanation',17,MUTED)
 line((385,33),(385,716))
 txt(425,29,'NOVA / EXPLORATION',21,TEXT,True)
 txt(1080,32,f'DAY {day:02d} / 14',19,MUTED,m=True)
 txt(425,68,'Cumulative spend and sales · fictional fixture',18,MUTED)
 x0,y0=443,132;w,h=864,228
 for i in range(5):
  y=y0+h-i*h/4;line((x0,y),(x0+w,y));txt(x0+w+11,y-12,str(i*100),15,MUTED,m=True)
 seq=[r for r in rows if r.campaign=='NOVA / Exploration']
 acc=[];s=0
 for r in seq:s+=r.spend;acc.append(s)
 pts=[(x0+i*w/13,y0+h-acc[i]/400*h) for i in range(day)]
 if len(pts)>1:d.line(pts,fill=GOLD,width=5)
 px,py=pts[-1];d.ellipse((px-6,py-6,px+6,py+6),fill=GOLD)
 d.line([(x0,y0+h),(x0+(day-1)*w/13,y0+h)],fill=CYAN,width=4)
 txt(x0,372,'JAN 01',15,MUTED,m=True);txt(x0+w-80,372,'JAN 14',15,MUTED,m=True)
 line((443,418),(469,418),GOLD,4);txt(480,403,'Spend',17,MUTED)
 line((598,418),(624,418),CYAN,4);txt(635,403,'Sales',17,MUTED)
 spend=acc[day-1]
 box(425,455,915,99)
 txt(451,471,'SPEND',15,MUTED,True);txt(451,494,f'${spend:,.2f}',29,TEXT,True)
 txt(726,471,'SALES',15,MUTED,True);txt(726,494,'$0.00',29,TEXT,True)
 txt(1007,471,'ACOS',15,MUTED,True);txt(1007,494,'Undefined',29,TEXT,True)
 d.rounded_rectangle((425,580,1340,651),radius=10,outline=GOLD,width=1)
 txt(451,601,'REVIEW SIGNAL  /  spend without sales',23,GOLD,True)
 txt(425,685,'A prompt for human review. No automatic bid changes.',18,MUTED)
 return im
frames=[draw_frame(i) for i in range(1,15)]
out=ROOT/'assets';out.mkdir(exist_ok=True)
# A single finite play-through. GIF intentionally has no loop extension.
frames[0].save(out/'signal-study.gif',save_all=True,append_images=frames[1:],duration=[320]*13+[2500],optimize=True,disposal=2)
frames[-1].save(out/'signal-study.png',optimize=True)
(out/'signal-study-data.json').write_text(json.dumps({'records':len(rows),'summary':totals,'signals':opportunities(rows)},indent=2))
print('Rendered 14 frames directly from the public synthetic fixture; final NOVA spend',sum(r.spend for r in rows if r.campaign=='NOVA / Exploration'))
