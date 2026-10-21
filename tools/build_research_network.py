from pathlib import Path
from html import escape
import math
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / 'assets'
W, H, S = 3200, 1980, 2
BG = '#0b1216'
WHITE = '#f3f0e7'
MUTED = '#b3c1c6'
HUB = '#d59a9f'
POD = '#69c5c2'
ING = '#e0bd82'
LIB = '#8cb9ef'
im = Image.new('RGB', (W*S, H*S), BG)
d = ImageDraw.Draw(im)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
       '<title id="title">How the NWSW research system connects</title>',
       '<desc id="desc">Three checks: Pod human review, Hub human review, and Ingestor verification and scoped reproduction. The same Hub makes the final acceptance decision. Accepted material enters the Library as shared context. Contributors retrieve reviewed findings, corrections and methods for subsequent work.</desc>',
       f'<rect width="{W}" height="{H}" fill="{BG}"/>']

def rect(box, fill, border=None, radius=0, width=2):
    x,y,x2,y2=box
    d.rounded_rectangle(tuple(round(v*S) for v in box), radius=radius*S, fill=fill, outline=border, width=width*S)
    svg.append(f'<rect x="{x}" y="{y}" width="{x2-x}" height="{y2-y}" rx="{radius}" fill="{fill}" stroke="{border or "none"}" stroke-width="{width}"/>')

def line(points, color, width=3):
    d.line([(round(x*S),round(y*S)) for x,y in points],fill=color,width=width*S,joint='curve')
    svg.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in points)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')

def circle(x,y,r,color,fill=BG,width=3):
    d.ellipse(((x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S),fill=fill,outline=color,width=width*S)
    svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{color}" stroke-width="{width}"/>')

def text(x,y,value,size=34,color=WHITE,bold=False,anchor='left'):
    font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',size*S)
    tw=d.textlength(value,font=font)/S
    xx=x-tw/2 if anchor=='middle' else x-tw if anchor=='right' else x
    d.text((round(xx*S),round(y*S)),value,font=font,fill=color,anchor='lt')
    svg.append(f'<text x="{xx}" y="{y+size*.80}" fill="{color}" font-family="Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}">{escape(value)}</text>')
    return tw

def arrow(points,color,width=5):
    line(points,color,width)
    x,y=points[-1]; px,py=points[-2]
    angle=math.atan2(y-py,x-px)
    pts=[(x,y),(x-21*math.cos(angle)+11*math.sin(angle),y-21*math.sin(angle)-11*math.cos(angle)),(x-21*math.cos(angle)-11*math.sin(angle),y-21*math.sin(angle)+11*math.cos(angle))]
    d.polygon([(round(a*S),round(b*S)) for a,b in pts],fill=color)
    svg.append(f'<polygon points="{" ".join(f"{a},{b}" for a,b in pts)}" fill="{color}"/>')

def badge(x,y,n,color):
    circle(x,y,25,color,BG,2)
    text(x,y-17,n,28,color,True,'middle')

def panel(x,y,w,h,color):
    rect((x,y,x+w,y+h),'#141f25','#304047',30,2)
    rect((x+2,y+30,x+7,y+h-30),color,radius=2)

def bullet(x,y,value,color,size=32):
    circle(x+4,y+16,4,color,color,1)
    text(x+25,y,value,size,MUTED)


for x in range(0,W,100): line([(x,0),(x,H)],'#101c22',1)
for y in range(0,H,100): line([(0,y),(W,y)],'#101c22',1)
text(120,80,'NEW WORLD SCREWWORM (NWSW) PROJECT',30,HUB,True)
text(120,150,'A research network with shared memory',78,WHITE,True)
text(120,265,'Three checks. Final human acceptance. Reviewed context feeds the next round of work.',36,MUTED)
line([(120,355),(3080,355)],'#304047',2)

# Continuous connectors: labels sit beside the lines, never overpaint them.
arrow([(920,790),(1200,790)],HUB,6)
text(1060,700,'Reviewed',28,HUB,True,'middle')
text(1060,742,'submission',28,HUB,False,'middle')
arrow([(2000,790),(2280,790)],ING,6)
text(2140,700,'Authorized',28,ING,True,'middle')
text(2140,742,'checks',28,ING,False,'middle')
arrow([(2680,1150),(2680,1400)],ING,6)
text(2730,1220,'Results +',29,ING,True)
text(2730,1265,'limitations',29,ING)
arrow([(2280,1610),(2000,1610)],LIB,6)
text(2140,1515,'Accepted',28,LIB,True,'middle')
text(2140,1557,'for sharing',28,LIB,False,'middle')
arrow([(520,1400),(520,1150)],POD,6)
text(570,1215,'Retrieve shared context',33,POD,True)
text(570,1265,'Apply reviewed lessons to the next task',30,MUTED)

# Three review checks, ordered left-to-right.
panel(120,500,800,650,POD)
text(170,545,'CHECK 01 / POD',28,POD,True)
text(170,605,'Pod human review',51,WHITE,True)
text(170,690,'Contributor + individual AI',32,POD)
bullet(170,780,'Review evidence and reasoning',POD,31)
bullet(170,840,'Correct issues and record uncertainty',POD,31)
bullet(170,900,'Send the human-reviewed contribution',POD,31)
line([(170,985),(870,985)],'#304047',2)
text(170,1025,'Parallel Pods, accountable people.',30,WHITE,True)
text(170,1080,'Each contribution retains its sources.',29,MUTED)

panel(1200,500,800,650,HUB)
text(1250,545,'CHECK 02 / HUB',28,HUB,True)
text(1250,605,'Hub human review',51,WHITE,True)
text(1250,690,'Project-level research oversight',32,HUB)
bullet(1250,780,'Assess scope, methods and evidence',HUB,31)
bullet(1250,840,'Resolve questions or request revisions',HUB,31)
bullet(1250,900,'Define what the Ingestor must check',HUB,31)
line([(1250,985),(1950,985)],'#304047',2)
text(1250,1025,'Research decisions stay human-led.',30,WHITE,True)
text(1250,1080,'The Hub also coordinates assignments.',29,MUTED)

panel(2280,500,800,650,ING)
text(2330,545,'CHECK 03 / INGESTOR',28,ING,True)
text(2330,605,'Verify + reproduce',51,WHITE,True)
text(2330,690,'Within the authorized scope',32,ING)
bullet(2330,780,'Check manifests, versions and hashes',ING,31)
bullet(2330,840,'Rerun the specified reproducible steps',ING,31)
bullet(2330,900,'Report matches, failures and limits',ING,31)
line([(2330,985),(3030,985)],'#304047',2)
text(2330,1025,'Checks produce an inspectable record.',29,WHITE,True)
text(2330,1080,'Results return to the Hub for acceptance.',28,MUTED)

panel(2280,1400,800,420,HUB)
text(2330,1445,'FINAL ACCEPTANCE',28,HUB,True)
text(2330,1505,'Back to the Hub',51,WHITE,True)
text(2330,1590,'The same Hub reviews the check results.',30,MUTED)
text(2330,1645,'Human authority accepts or returns work',30,MUTED)
text(2330,1690,'and sets the approved sharing scope.',30,MUTED)
text(2330,1760,'Acceptance controls Library publication.',28,HUB)

panel(120,1400,1880,420,LIB)
text(170,1445,'LIBRARY / SHARED PROJECT MEMORY',28,LIB,True)
text(170,1505,'Reviewed knowledge accumulates.',49,WHITE,True)
text(170,1590,'Findings, corrections, methods and review history',31,MUTED)
text(170,1640,'remain linked to their sources and versions.',31,MUTED)
text(170,1730,'Available in Library',29,POD,True)
text(170,1771,'Approved material within its recorded scope',26,MUTED)
text(825,1730,'Request from Hub',29,ING,True)
text(825,1771,'Held material remains request-only',26,MUTED)

# A small knowledge network illustrates linked context, not model neurons.
for xy in [(1600,1490),(1850,1510),(1850,1720),(1570,1740)]:
    line([(1720,1610),xy],LIB,3)
for x,y in [(1600,1490),(1850,1510),(1850,1720),(1570,1740)]:
    circle(x,y,18,LIB,'#1b303e',3)
circle(1720,1610,85,LIB,'#1b303e',3)
text(1720,1574,'Shared',27,WHITE,True,'middle')
text(1720,1615,'context',27,WHITE,True,'middle')
text(1600,1440,'Sources',24,MUTED,False,'middle')
text(1850,1460,'Methods',24,MUTED,False,'middle')
text(1850,1755,'Decisions',24,MUTED,False,'middle')
text(1555,1775,'Corrections',24,MUTED,False,'middle')

text(120,1895,'Iterative contextual learning: later work uses the reviewed record when agents retrieve current context.',31,POD)
text(120,1950,'Brandon Santor / Research systems',24,MUTED)
text(3080,1950,'Logical review and reuse flow / 21 Oct 2026',24,MUTED,anchor='right')
svg.append('</svg>')
im.resize((W,H),Image.Resampling.LANCZOS).save(OUT/'nwsw-research-network.png',optimize=True)
(OUT/'nwsw-research-network.svg').write_text('\n'.join(svg),encoding='utf-8')
print(OUT/'nwsw-research-network.png')
