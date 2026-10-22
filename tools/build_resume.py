"""Build the public resume from resume.html. Requires reportlab and pypdf.

Run: python tools/build_resume.py
Check the public download against its source: python tools/build_resume.py --check
Render and visually review a newly generated PDF before publication.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from hashlib import sha256
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'resume.html'
PUBLIC_EMAIL = 'brandon.santor@tamu.edu'


@dataclass
class Element:
    tag: str
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    def text(self):
        pieces = [child.text() if isinstance(child, Element) else child for child in self.children]
        return re.sub(r'\s+', ' ', ' '.join(pieces)).strip()

    def find(self, predicate):
        for child in self.children:
            if isinstance(child, Element):
                if predicate(child):
                    yield child
                yield from child.find(predicate)

    def direct(self, tag):
        return [child for child in self.children if isinstance(child, Element) and child.tag == tag]


class Document(HTMLParser):
    void = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Element('document')
        self.stack = [self.root]
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = Element(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in self.void:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Element(tag, dict(attrs)))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, text):
        self.stack[-1].children.append(text)


def one(root, predicate):
    matches = list(root.find(predicate))
    if len(matches) != 1:
        raise ValueError(f'Expected one source element, got {len(matches)}')
    return matches[0]


def classed(node, name):
    return name in node.attrs.get('class', '').split()


def plain(text):
    replacements = {'\u2010': '-', '\u2011': '-', '\u2012': '-', '\u2013': '-', '\u2014': ' - ', '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u00b7': ' | ', '\u2192': '', '\u2197': ''}
    for old, new in replacements.items():
        text = text.replace(old, new)
    return re.sub(r'\s+', ' ', text).strip()


def article_data(node):
    headings = node.direct('h3')
    metas = [p for p in node.direct('p') if classed(p, 'meta')]
    lists = node.direct('ul')
    links = list(node.find(lambda n: n.tag == 'a' and n.attrs.get('href', '').startswith('project-')))
    return {
        'title': headings[0].text() if headings else '',
        'meta': metas[0].text() if metas else '',
        'bullets': [li.text() for ul in lists for li in ul.direct('li')],
        'link': 'https://emp1241.github.io/' + links[0].attrs['href'] if links else '',
    }


def read_source():
    # Git may check out CRLF on Windows; fingerprints should ignore that change.
    raw = SOURCE.read_bytes().replace(b'\r\n', b'\n')
    document = Document(raw.decode('utf-8')).root
    email_link = one(document, lambda n: n.tag == 'a' and n.attrs.get('id') == 'resume-email')
    if email_link.text() != PUBLIC_EMAIL or email_link.attrs.get('href') != 'mailto:' + PUBLIC_EMAIL:
        raise ValueError('Resume requires the approved public TAMU email link.')
    resume = one(document, lambda n: n.attrs.get('id') == 'resume')
    experience = one(resume, lambda n: n.attrs.get('id') == 'research-professional-experience')
    jobs = [article_data(n) for n in experience.direct('article')]
    if len(jobs) != 6 or any(len(job['bullets']) != 3 for job in jobs):
        raise ValueError('Every research/professional experience role must have three bullets; expected six roles.')
    selected = one(resume, lambda n: n.tag == 'section' and any(h.text() == 'Selected software & research' for h in n.direct('h2')))
    projects = [article_data(n) for n in selected.find(lambda n: n.tag == 'article' and classed(n, 'resume-item'))]
    sidebar = one(resume, lambda n: n.tag == 'aside')
    sections = {n.direct('h2')[0].text(): n for n in sidebar.direct('section') if n.direct('h2')}
    honor_rows = []
    for row in sections['Honors & scholarships'].find(lambda n: n.tag == 'li'):
        parts = row.direct('strong') + row.direct('span')
        honor_rows.append(' | '.join(part.text() for part in parts) if parts else row.text())
    skill_groups = [
        {'title': group.direct('h3')[0].text(),
         'skills': [n.text() for n in group.find(lambda n: n.tag == 'li')]}
        for group in sections['Technical toolkit'].direct('div') if classed(group, 'toolkit-group')
    ]
    skills = [n.text() for n in sections['Technical toolkit'].find(lambda n: n.tag == 'li')]
    if len(skill_groups) != 4 or [skill for group in skill_groups for skill in group['skills']] != skills:
        raise ValueError('Technical toolkit requires four groups containing every listed skill.')
    return {
        'digest': sha256(raw).hexdigest(),
        'email': email_link.text(),
        'summary': one(document, lambda n: n.tag == 'p' and classed(n, 'resume-summary')).text(),
        'jobs': jobs,
        'projects': projects,
        'education': [article_data(n) for n in sections['Education'].direct('article')],
        'honors': honor_rows,
        'skill_groups': skill_groups,
        'communication': sections['Research communication'].direct('p')[0].text(),
    }


def build(output, data):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether, PageBreak, Table, TableStyle
    from pypdf import PdfReader

    maroon = colors.HexColor('#500000')
    muted = colors.HexColor('#535b60')
    ink = colors.HexColor('#182126')
    styles = {
        'name': ParagraphStyle('name', fontName='Helvetica-Bold', fontSize=24, leading=27, textColor=maroon, spaceAfter=5),
        'subtitle': ParagraphStyle('subtitle', fontName='Helvetica-Bold', fontSize=8.2, leading=11, textColor=muted, spaceAfter=5),
        'body': ParagraphStyle('body', fontName='Helvetica', fontSize=9, leading=11.6, textColor=ink, spaceAfter=6),
        'section': ParagraphStyle('section', fontName='Helvetica-Bold', fontSize=10.2, leading=13, textColor=maroon, spaceBefore=8, spaceAfter=7),
        'role': ParagraphStyle('role', fontName='Helvetica-Bold', fontSize=9.3, leading=11.5, textColor=ink, spaceAfter=2),
        'meta': ParagraphStyle('meta', fontName='Helvetica', fontSize=8, leading=10, textColor=muted, spaceAfter=4),
        'bullet': ParagraphStyle('bullet', fontName='Helvetica', fontSize=8.6, leading=10.6, textColor=ink, leftIndent=8, bulletIndent=0, spaceAfter=3),
        'small': ParagraphStyle('small', fontName='Helvetica', fontSize=8.1, leading=10.2, textColor=ink, spaceAfter=5),
        'support-title': ParagraphStyle('support-title', fontName='Helvetica-Bold', fontSize=9.1, leading=11, textColor=maroon, spaceBefore=7, spaceAfter=5),
    }

    def p(text, style='body'):
        return Paragraph(escape(plain(text)), styles[style])

    def record(item):
        title = escape(plain(item['title']))
        if item['link']:
            title = '<link href="' + escape(item['link'], quote=True) + '" color="#500000">' + title + '</link>'
        flow = [Paragraph(title, styles['role'])]
        if item['meta']:
            flow.append(p(item['meta'], 'meta'))
        flow += [Paragraph(escape(plain(text)), styles['bullet'], bulletText='-') for text in item['bullets']]
        flow.append(Spacer(1, 5))
        return KeepTogether(flow)

    contact = '<link href="mailto:' + escape(data['email'], quote=True) + '" color="#500000">' + escape(data['email']) + '</link> | <link href="https://emp1241.github.io" color="#500000">emp1241.github.io</link>'
    story = [p('BRANDON SANTOR', 'name'), p('GEOSPATIAL RESEARCH | SCIENTIFIC SOFTWARE | U.S. MARINE CORPS VETERAN', 'subtitle'), Paragraph(contact, styles['meta']), p(data['summary']), p('RESEARCH & PROFESSIONAL EXPERIENCE', 'section')]
    story += [record(item) for item in data['jobs']]
    story += [PageBreak(), p('SELECTED SOFTWARE & RESEARCH', 'section')]
    story += [record(item) for item in data['projects']]

    left, right = [p('EDUCATION', 'support-title')], [p('TECHNICAL TOOLKIT', 'support-title')]
    for item in data['education']:
        left.append(p(item['title'], 'role'))
        left.append(p(' | '.join(x for x in [item['meta'], *item['bullets']] if x), 'small'))
    left.append(p('HONORS & SCHOLARSHIPS', 'support-title'))
    left += [p(text, 'small') for text in data['honors']]
    for group in data['skill_groups']:
        label = escape(plain(group['title']))
        skills = escape(plain('; '.join(group['skills'])))
        right.append(Paragraph('<b>' + label + ':</b> ' + skills + '.', styles['small']))
    right.append(p('RESEARCH COMMUNICATION', 'support-title'))
    right.append(p(data['communication'], 'small'))
    support = Table([[left, right]], colWidths=[258, 258], hAlign='LEFT')
    support.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (0, 0), 18), ('RIGHTPADDING', (1, 0), (1, 0), 0), ('TOPPADDING', (0, 0), (-1, -1), 1), ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
    story.append(support)

    def furniture(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(maroon)
        canvas.rect(0, 780, 612, 12, fill=1, stroke=0)
        canvas.setStrokeColor(colors.HexColor('#b59b68'))
        canvas.line(42, 33, 570, 33)
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(muted)
        canvas.drawString(42, 22, 'Brandon Santor | Geospatial research and scientific software')
        canvas.drawRightString(570, 22, str(doc.page))
        canvas.restoreState()

    output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(output), pagesize=letter, rightMargin=42, leftMargin=42, topMargin=32, bottomMargin=41, title='Brandon Santor - Public Resume', author='Brandon Santor', subject='resume.html SHA-256: ' + data['digest'], invariant=1)
    doc.build(story, onFirstPage=furniture, onLaterPages=furniture)
    reader = PdfReader(output)
    if len(reader.pages) != 2:
        raise ValueError(f'Expected a two-page resume, got {len(reader.pages)}; review layout before publication.')
    extracted = '\n'.join(page.extract_text() for page in reader.pages)
    if re.search(r'\b\d{3}[ .-]\d{3}[ .-]\d{4}\b|mailto:|C:\\Users\\', extracted, re.I):
        raise ValueError('Unexpected private contact/path content in generated resume.')
    addresses = re.findall(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}', extracted, re.I)
    mail_links = [str(annotation.get_object().get('/A', {}).get('/URI', ''))
                  for page in reader.pages for annotation in page.get('/Annots', [])
                  if str(annotation.get_object().get('/A', {}).get('/URI', '')).startswith('mailto:')]
    if addresses != [PUBLIC_EMAIL] or mail_links != ['mailto:' + PUBLIC_EMAIL]:
        raise ValueError('Generated resume must contain exactly one approved, clickable TAMU email.')
    print(f'Built {len(reader.pages)} pages from resume.html: {output}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'resume.pdf')
    parser.add_argument('--check', action='store_true', help='Verify PDF source fingerprint without writing.')
    args = parser.parse_args()
    data = read_source()
    output = args.output.resolve()
    if args.check:
        from pypdf import PdfReader
        if not output.is_file() or PdfReader(output).metadata.subject != 'resume.html SHA-256: ' + data['digest']:
            raise SystemExit('Resume PDF is stale or missing; rebuild from resume.html and visually inspect it.')
        print('PASS: resume.pdf matches its resume.html source fingerprint.')
    else:
        build(output, data)


if __name__ == '__main__':
    main()
