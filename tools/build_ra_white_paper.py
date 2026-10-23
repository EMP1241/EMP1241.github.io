"""Build the public RA white paper from its reviewed Markdown source.

Requires reportlab and pypdf. --check verifies the embedded source/builder hashes.
Deliberate page breaks keep the technical diagrams and their explanation together.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import io
import re
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/research-architect-white-paper.md'
OUTPUT = ROOT / 'assets/documents/research-architect-white-paper.pdf'
MAROON = colors.HexColor('#500000')
INK = colors.HexColor('#20262b')
MUTED = colors.HexColor('#53616b')
TEAL = colors.HexColor('#246c74')
PALE = colors.HexColor('#f0f4f5')
WIDTH = 516


def fingerprint(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rich(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',
                  r'<link href="\2" color="#246c74"><u>\1</u></link>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
    return text


STYLES = {
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=10,
                           leading=14.2, textColor=INK, spaceAfter=9),
    'title': ParagraphStyle('title', fontName='Times-Bold', fontSize=34,
                            leading=36, textColor=MAROON, spaceAfter=8),
    'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=18,
                         leading=22, textColor=MAROON, spaceAfter=14,
                         keepWithNext=True),
    'h3': ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=11.4,
                         leading=15, textColor=INK, spaceBefore=9,
                         spaceAfter=6, keepWithNext=True),
    'cell': ParagraphStyle('cell', fontName='Helvetica', fontSize=9.1,
                           leading=12.6, textColor=INK),
    'head': ParagraphStyle('head', fontName='Helvetica-Bold', fontSize=9,
                           leading=12.5, textColor=colors.white),
    'caption': ParagraphStyle('caption', fontName='Helvetica', fontSize=8.5,
                              leading=11.6, textColor=MUTED, spaceAfter=10),
    'reference': ParagraphStyle('reference', fontName='Helvetica', fontSize=9.2,
                                leading=12.7, textColor=INK, spaceAfter=8),
}


class Architecture(Flowable):
    def __init__(self):
        super().__init__()
        self.width, self.height = WIDTH, 197

    def draw(self):
        c = self.canv

        def box(x, y, w, h, title, subtitle='', fill=PALE):
            c.setFillColor(fill)
            c.setStrokeColor(colors.HexColor('#cbd5d8'))
            c.roundRect(x, y, w, h, 5, fill=1, stroke=1)
            c.setFillColor(INK)
            c.setFont('Helvetica-Bold', 9)
            c.drawCentredString(x+w/2, y+h-17, title)
            if subtitle:
                c.setFont('Helvetica', 8)
                c.setFillColor(MUTED)
                c.drawCentredString(x+w/2, y+10, subtitle)

        def arrow(x1, y1, x2, y2):
            c.setStrokeColor(TEAL)
            c.setFillColor(TEAL)
            c.setLineWidth(1.1)
            c.line(x1, y1, x2, y2)
            p = c.beginPath()
            p.moveTo(x2, y2)
            if y1 == y2:
                p.lineTo(x2-4, y2+2.5); p.lineTo(x2-4, y2-2.5)
            else:
                p.lineTo(x2-2.5, y2+4); p.lineTo(x2+2.5, y2+4)
            p.close()
            c.drawPath(p, fill=1, stroke=0)

        box(0, 148, WIDTH, 44, 'Reviewed project design + Architect / compiler',
            'Question, methods, responsibilities, dependencies, review requirements')
        for i, (name, desc) in enumerate([
            ('Hub kit', 'Coordination and acceptance'),
            ('Spoke / pod kit', 'Participant work and review'),
            ('Ingestor kit', 'Verification and reproduction'),
        ]):
            x = i * 176
            arrow(x+82, 148, x+82, 130)
            box(x, 83, 164, 47, name, desc)
        c.setFont('Helvetica-Bold', 8)
        c.setFillColor(MUTED)
        c.drawString(0, 62, 'REVIEWED EVIDENCE FLOW IN THE NWSW DEPLOYMENT')
        labels = [('Participant', 'human review'), ('Hub', 'scope + review'),
                  ('Ingestor', 'check / reproduce'), ('Hub', 'final acceptance'),
                  ('Library', 'publish in scope')]
        for i, (name, detail) in enumerate(labels):
            x = i * 105
            box(x, 4, 96, 44, name, detail)
            if i < 4:
                arrow(x+96, 26, x+105, 26)


class Benchmark(Flowable):
    def __init__(self):
        super().__init__()
        self.width, self.height = WIDTH, 111

    def draw(self):
        c = self.canv
        for label, value, y, color in [
            ('Repeated-context baseline', 773391, 74, MUTED),
            ('Selective representation', 119362, 26, TEAL),
        ]:
            c.setFillColor(INK)
            c.setFont('Helvetica', 9)
            c.drawString(0, y+20, label)
            c.setFont('Helvetica-Bold', 9)
            c.drawRightString(WIDTH, y+20, f'{value:,} characters')
            c.setFillColor(PALE)
            c.rect(0, y, WIDTH, 13, fill=1, stroke=0)
            c.setFillColor(color)
            c.rect(0, y, WIDTH*value/773391, 13, fill=1, stroke=0)


class Mechanism(Flowable):
    """Vector explanations; labels describe behavior without invented screen UI."""
    def __init__(self, kind):
        super().__init__()
        self.kind = kind
        self.width = WIDTH
        self.height = {'context': 184, 'library': 176, 'recovery': 151, 'paging': 182, 'knowledge': 166}[kind]

    def draw(self):
        c = self.canv

        def box(x, y, w, h, title, lines=(), accent=False):
            c.setFillColor(colors.HexColor('#e8f2f2') if accent else PALE)
            c.setStrokeColor(TEAL if accent else colors.HexColor('#cbd5d8'))
            c.roundRect(x, y, w, h, 5, stroke=1, fill=1)
            c.setFont('Helvetica-Bold', 9)
            c.setFillColor(INK)
            c.drawCentredString(x+w/2, y+h-16, title)
            c.setFont('Helvetica', 8)
            c.setFillColor(MUTED)
            for i, line in enumerate(lines):
                c.drawCentredString(x+w/2, y+h-30-i*11, line)

        def path(points, arrow=True):
            c.setLineWidth(1.2)
            c.setStrokeColor(TEAL)
            p = c.beginPath(); p.moveTo(*points[0])
            for pt in points[1:]: p.lineTo(*pt)
            c.drawPath(p)
            if arrow:
                x1,y1=points[-2];x2,y2=points[-1]
                dx,dy=x2-x1,y2-y1
                mag=(dx*dx+dy*dy)**.5
                ux,uy=dx/mag,dy/mag
                p=c.beginPath();p.moveTo(x2,y2)
                p.lineTo(x2-5*ux+2.5*uy,y2-5*uy-2.5*ux)
                p.lineTo(x2-5*ux-2.5*uy,y2-5*uy+2.5*ux);p.close()
                c.setFillColor(TEAL);c.drawPath(p,fill=1,stroke=0)

        if self.kind == 'context':
            box(0,124,158,56,'Resolve current state',('Checkpoint + instructions','Selected original evidence'))
            box(180,124,156,56,'Encode selected context',('Literal text or exact','duplicate references'))
            box(358,124,158,56,'Reconstruct + check',('Complete selected text','Matching source hashes'),True)
            path([(158,152),(180,152)]);path([(336,152),(358,152)])
            box(0,9,244,69,'Before a later request',('Same conversation? Matching context?','Actually read and still retained?'))
            box(296,57,220,35,'Yes: explicit reuse',accent=True)
            box(296,7,220,35,'No / uncertain: restore context')
            path([(244,56),(273,56),(273,74),(296,74)])
            path([(244,32),(273,32),(273,24),(296,24)])
        elif self.kind == 'library':
            box(0,111,146,57,'Version 1 retained',('Original record','Its own source identity'))
            box(178,111,160,57,'Review the correction',('Affected version + evidence','Human acceptance'))
            box(370,111,146,57,'Version 2 published',('Links back to version 1','Current use conditions'),True)
            path([(146,140),(178,140)]);path([(338,140),(370,140)])
            box(0,10,146,53,'Topic A',('Discovery reference',))
            box(186,10,146,53,'Topic B',('Discovery reference',))
            box(370,10,146,53,'One canonical version',('Dependencies + corrections',),True)
            path([(146,37),(166,37),(166,84),(443,84),(443,63)])
            path([(332,37),(370,37)])
            path([(443,111),(443,63)])
        elif self.kind == 'recovery':
            labels=['Prepared','Verified','In progress','Complete']
            for i,label in enumerate(labels):
                box(i*136,110,108,36,label,accent=i==3)
                if i<3:path([(i*136+108,128),(i*136+136,128)])
            box(0,12,148,62,'Unknown outcome',('A reply or final record','is missing'))
            box(179,12,158,62,'Reconcile',('Inspect request identity','and actual postconditions'))
            box(368,12,148,62,'Guarded next step',('Record completion or','finish pending finalization'),True)
            path([(326,110),(326,90),(74,90),(74,74)])
            path([(148,43),(179,43)]);path([(337,43),(368,43)])
        elif self.kind == 'knowledge':
            box(0,102,152,58,'Select research methods',('Question + analysis unit','Review responsibilities'))
            box(182,102,152,58,'Resolve dependencies',('Method + specialist guides','Sources + reuse rights'))
            box(364,102,152,58,'Generate the role kit',('Pinned selected material','Long texts outside startup'),True)
            path([(152,131),(182,131)]);path([(334,131),(364,131)])
            box(0,4,240,57,'Read when needed',('Local catalog / search / exact read','Bounded UTF-8 responses'))
            box(276,4,240,57,'Continue until complete',('Same source hash on every part','Original source remains inspectable'),True)
            path([(440,102),(440,83),(120,83),(120,61)])
            path([(240,32),(276,32)])
        elif self.kind == 'paging':
            box(0,117,152,58,'Run one scoped lookup',('Or read one message result','Keep completeness status'))
            box(190,111,326,70,'Retain the complete result',('Findings + source pins + review conditions','A fixed result hash identifies every continuation'),True)
            path([(152,146),(190,146)])
            for i,(label,detail) in enumerate([('Page 1','Bounded response'),('Page 2','Same result hash'),('Page N','All content retrievable')]):
                x=i*177
                box(x,10,162,52,label,(detail,))
                path([(353,111),(353,91),(x+81,91),(x+81,62)])


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(MAROON)
    canvas.setLineWidth(1.4)
    canvas.line(48, 751, 564, 751)
    canvas.setFillColor(MUTED)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(48, 762, 'RESEARCH ARCHITECT  /  TECHNICAL WHITE PAPER')
    canvas.setStrokeColor(colors.HexColor('#d5dcde'))
    canvas.setLineWidth(.5)
    canvas.line(48, 42, 564, 42)
    canvas.drawString(48, 28, 'Public edition 5  |  October 23, 2026  |  RA 2.4 revision 2')
    canvas.drawRightString(564, 28, str(doc.page))
    canvas.restoreState()


def table(rows):
    count = len(rows[0])
    widths = [155, WIDTH-155] if count == 2 else [122, 188, WIDTH-310]
    data = [[Paragraph(rich(cell.strip()), STYLES['head' if n == 0 else 'cell'])
             for cell in row] for n, row in enumerate(rows)]
    t = Table(data, colWidths=widths, hAlign='LEFT', repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), MAROON),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [PALE, colors.white]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, -1), (-1, -1), .5, colors.HexColor('#cbd5d8')),
    ]))
    return t


def build():
    story = []
    sections = SOURCE.read_text(encoding='utf-8').split('<!-- page -->')
    for page, section in enumerate(sections):
        if page:
            story.append(PageBreak())
        blocks = re.split(r'\n\s*\n', section.strip())
        for block in blocks:
            if block == '<!-- architecture -->':
                story.extend([Architecture(), Spacer(1, 7)])
            elif block == '<!-- benchmark -->':
                story.append(Benchmark())
            elif block in ['<!-- context-flow -->','<!-- library-flow -->',
                           '<!-- recovery-flow -->','<!-- paging-flow -->','<!-- knowledge-flow -->']:
                kind = block.removeprefix('<!-- ').removesuffix('-flow -->')
                story.extend([Mechanism(kind), Spacer(1, 7)])
            elif block.startswith('|'):
                rows = [[cell.strip() for cell in row.strip().strip('|').split('|')]
                        for row in block.splitlines()]
                rows = [row for row in rows if not all(re.fullmatch(r'[-: ]+', c) for c in row)]
                story.extend([table(rows), Spacer(1, 10)])
            elif block.startswith('# '):
                story.append(Paragraph(rich(block[2:]), STYLES['title']))
            elif block.startswith('## '):
                story.append(Paragraph(rich(block[3:]), STYLES['h2']))
            elif block.startswith('### '):
                story.append(Paragraph(rich(block[4:]), STYLES['h3']))
            elif re.match(r'^\d+\. ', block):
                for line in block.splitlines():
                    story.append(Paragraph(rich(line), STYLES['body']))
            else:
                style = 'reference' if page == len(sections)-1 else 'body'
                if block.startswith(('Figure ', 'Brandon Santor', 'October 23, 2026')):
                    style = 'caption'
                story.append(Paragraph(rich(block.replace('\n', ' ')), STYLES[style]))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            leftMargin=48, rightMargin=48, topMargin=57,
                            bottomMargin=55, title='Research Architect: Continuity, coordination, and review',
                            author='Brandon Santor',
                            subject='RA 2.4.0 revision 2; public edition 5; October 23, 2026')
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    buffer.seek(0)
    reader = PdfReader(buffer)
    if len(reader.pages) != len(sections):
        for index, page in enumerate(reader.pages, 1):
            content = page.extract_text()
            print(index, repr(content[105:210]), repr(content[-120:]))
    assert len(reader.pages) == len(sections), f'Unexpected overflow: {len(reader.pages)} pages for {len(sections)} sections'
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer.add_metadata({'/RASourceSHA256': fingerprint(SOURCE),
                         '/RABuilderSHA256': fingerprint(Path(__file__))})
    for i, title in enumerate(re.findall(r'^## (.+)', SOURCE.read_text(encoding='utf-8'), re.M)):
        writer.add_outline_item(title, i)
    temporary = OUTPUT.with_suffix('.pending.pdf')
    with temporary.open('wb') as stream:
        writer.write(stream)
    temporary.replace(OUTPUT)
    print(f'Built {len(reader.pages)} pages: {OUTPUT}')


def check():
    reader = PdfReader(OUTPUT)
    assert reader.metadata.get('/RASourceSHA256') == fingerprint(SOURCE), 'White-paper source changed; rebuild PDF'
    assert reader.metadata.get('/RABuilderSHA256') == fingerprint(Path(__file__)), 'Builder changed; rebuild PDF'
    print(f'White paper current: {len(reader.pages)} pages, matching source and builder fingerprints')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    check() if args.check else build()
