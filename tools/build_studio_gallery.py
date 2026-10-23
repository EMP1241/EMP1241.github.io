"""Compose studio identity, current products and public engineering material as SVGs.

The embedded images are existing portfolio assets. The paper-cover PNG is a
render of page one of the public white paper, not a proposed application UI.
"""
from pathlib import Path
from base64 import b64encode
from html import escape
from io import BytesIO
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/studio'
BG, INK, MUTED = '#090b12', '#f5efe4', '#b9b6c5'
PURPLE, GOLD, BORDER = '#b694ef', '#e6c78b', '#383348'


class Art:
    def __init__(self, title, description):
        self.nodes = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="800" viewBox="0 0 1280 800" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>',
            '<defs><radialGradient id="glow"><stop stop-color="#39264e"/><stop offset="1" stop-color="#090b12"/></radialGradient><linearGradient id="edge"><stop stop-color="#b694ef"/><stop offset="1" stop-color="#e6c78b"/></linearGradient></defs>',
            f'<rect width="1280" height="800" fill="{BG}"/>']

    def rect(self, x, y, w, h, fill='#13141f', stroke=BORDER, radius=16):
        self.nodes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>')

    def text(self, x, y, text, size=24, color=INK, weight=400, mono=False):
        font = 'Consolas,monospace' if mono else 'Segoe UI,Arial,sans-serif'
        self.nodes.append(f'<text x="{x}" y="{y}" xml:space="preserve" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(text)}</text>')

    def image(self, path, x, y, w, h, extra=''):
        # PNG embedding works in browsers and standalone SVG renderers.
        buf = BytesIO()
        Image.open(path).save(buf, format='PNG')
        mime = 'image/png'
        data = b64encode(buf.getvalue()).decode('ascii')
        self.nodes.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" href="data:{mime};base64,{data}" {extra}/>')

    def line(self, x1, y1, x2, y2, color=BORDER):
        self.nodes.append(f'<path d="M{x1} {y1}H{x2}" fill="none" stroke="{color}"/>' if y1 == y2 else f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color}"/>')

    def save(self, name):
        OUT.mkdir(exist_ok=True)
        (OUT/name).write_text('\n'.join(self.nodes+['</svg>']),encoding='utf-8')


def identity():
    a=Art('PhalAInx independent software studio', 'The existing PhalAInx emblem, with its metallic rings, purple light and gold arrow, paired with the studio name and its founder Brandon Santor. Studio identity artwork, not an application screenshot.')
    a.nodes.append('<rect width="700" height="800" fill="url(#glow)"/>')
    a.nodes.append((ROOT/'assets/icons/phalainx-logo-fitted.svg').read_text(encoding='utf-8').replace('<svg ', '<svg x="75" y="115" ', 1).replace('width="974" height="963"', 'width="520" height="550"', 1))
    a.line(640,180,640,620)
    a.text(60,68,'PHALAINX / STUDIO IDENTITY',18,PURPLE,700)
    a.nodes.append(f'<text x="700" y="330" font-family="Segoe UI,Arial,sans-serif" font-size="72" font-weight="650" fill="{INK}">Phal<tspan fill="{GOLD}">AI</tspan>nx</text>')
    a.text(700,399,'Independent software studio',31,INK)
    a.text(700,453,'Created by Brandon Santor',25,MUTED)
    a.line(700,492,1200,492,'url(#edge)')
    a.text(700,543,'Product design',25,MUTED)
    a.text(700,585,'Research systems',25,MUTED)
    a.text(700,627,'Software development',25,MUTED)
    a.line(60,721,1220,721)
    a.text(60,762,'Research Architect',23,PURPLE,600)
    a.text(1015,762,'High Command',23,GOLD,600)
    a.save('studio-identity-20261022.svg')


def products():
    a=Art('Research Architect and High Command, software from PhalAInx', 'The current Research Architect icon and published technical white paper represent the framework for human research teams. A current High Command Command Deck capture represents the desktop application for individuals. Research Architect is a development preview; High Command is in alpha testing.')
    a.text(60,68,'PHALAINX / THE PRODUCT FAMILY',18,PURPLE,700)
    a.text(60,130,'Two products. Different working contexts.',43,INK,650)
    a.rect(60,178,555,540)
    a.rect(645,178,575,540)
    a.image(ROOT/'assets/icons/research-architect.webp',85,205,90,90)
    a.text(195,247,'Research Architect',32,INK,650)
    a.text(195,282,'For human research teams',22,PURPLE)
    a.rect(92,320,210,252,fill='#0b0d15')
    a.image(OUT/'ra-whitepaper-cover-20261023.png',100,328,194,236)
    a.text(333,367,'Individual kits',23,INK,650)
    a.text(333,410,'Shared methods',23,MUTED)
    a.text(333,453,'Research context',23,MUTED)
    a.text(333,496,'Human review',23,MUTED)
    a.line(92,600,583,600)
    a.text(92,646,'Framework + continuity tools',25,INK,600)
    a.text(92,687,'RA 2.4 development preview',21,PURPLE)
    a.image(ROOT/'assets/icons/high-command.webp',670,205,90,90)
    a.text(780,247,'High Command',32,INK,650)
    a.text(780,282,'For individual project work',22,GOLD)
    a.rect(675,322,515,290,fill='#080c12',radius=8)
    a.image(ROOT/'assets/screenshots/hc-command-deck-20261018.webp',680,327,505,280)
    a.text(675,655,'Local desktop workspace',25,INK,600)
    a.text(675,695,'Active alpha testing',21,GOLD)
    a.text(60,763,'RA 2.4 revision 2 / Technical white paper: October 23, 2026',19,MUTED)
    a.save('studio-products-20261022.svg')


def engineering():
    a=Art('Published design and a runnable public integrity example', 'The actual first page of the revised Research Architect technical white paper, an exact excerpt of the public synthetic integrity example, and output from its five self-checks. The example was written for the portfolio and is not private RA runtime code.')
    a.text(60,68,'PHALAINX / DEVELOPMENT MATERIAL',18,PURPLE,700)
    a.text(60,130,'Published design. Runnable checks.',46,INK,650)
    a.rect(60,180,395,535,fill='#191722',stroke='#5d4c78')
    a.image(OUT/'ra-whitepaper-cover-20261023.png',79,196,357,463)
    a.text(82,692,'Technical white paper / 14 pages',21,PURPLE,600)
    a.rect(485,180,735,335)
    a.text(510,214,'PUBLIC INTEGRITY EXAMPLE / SYNTHETIC FILES',16,GOLD,700)
    source=(ROOT/'assets/examples/handoff-integrity/verify.py').read_text(encoding='utf-8')
    excerpt=source.split('# BEGIN PUBLIC EXCERPT\n',1)[1].split('# END PUBLIC EXCERPT',1)[0].strip()
    for i,line in enumerate(excerpt.splitlines()):
        a.text(510,246+i*21,line,16,MUTED,mono=True)
    a.rect(485,540,735,175,fill='#0e191c',stroke='#375458')
    a.text(510,574,'python verify.py --self-test',18,'#8ed5d1',600,mono=True)
    # Exact output from the included deterministic synthetic fixture checks.
    for i,line in enumerate(('PASS: intact sample matches its manifest','PASS: changed file is detected','PASS: missing file is detected','PASS: unexpected file is detected','PASS: malformed manifest is rejected')):
        a.text(510,602+i*23,line,17,'#bdcccf',mono=True)
    a.text(60,763,'Public design documentation and a portfolio example you can inspect and run.',19,MUTED)
    a.save('studio-engineering-20261022.svg')


if __name__ == '__main__':
    identity()
    products()
    engineering()
    print('Built three studio gallery SVGs from current public portfolio material.')
