"""Dependency-free pre-publish checks for the static portfolio."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors = []

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids, self.refs, self.images, self.headings, self.links = [], [], [], [], []
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag in ('a', 'link') and attrs.get('href'):
            self.refs.append(attrs['href'])
        if tag in ('img', 'script') and attrs.get('src'):
            self.refs.append(attrs['src'])
        if tag == 'img':
            self.images.append(attrs)
        if re.fullmatch('h[1-6]', tag):
            self.headings.append(int(tag[1]))
        if tag == 'a':
            self.links.append(attrs)

pages = {p.name: Page(p) for p in ROOT.glob('*.html')}
expected = {'index.html', 'about.html', 'projects.html', 'resume.html', 'project-nwsw.html',
            'project-trae.html', 'project-tvae.html', 'project-research-architect.html', 'project-gnss.html', '404.html'}
if set(pages) != expected:
    errors.append(f'Unexpected page set: {set(pages) ^ expected}')
email = re.compile(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}', re.I)
phone = re.compile(r'(?<!\d)(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\d)')
for name, page in pages.items():
    if page.headings.count(1) != 1:
        errors.append(f'{name}: requires exactly one h1')
    if any(n > 1 for n in Counter(page.ids).values()):
        errors.append(f'{name}: duplicate IDs')
    if 'main' not in page.ids or 'top' not in page.ids:
        errors.append(f'{name}: missing skip-link or top target')
    for img in page.images:
        if not all(key in img for key in ('alt', 'width', 'height')):
            errors.append(f'{name}: image missing alt or dimensions')
    text = page.path.read_text(encoding='utf-8')
    if email.search(text) or phone.search(text) or 'mailto:' in text or 'tel:' in text or '[ADD]' in text:
        errors.append(f'{name}: contact detail or unfinished placeholder')
    if re.search(r'C:\\Users\\|C:/Users/|localhost|127\.0\.0\.1', text, re.I):
        errors.append(f'{name}: local-only path or URL')
    for ref in page.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            continue
        target = (ROOT / unquote(url.path).lstrip('/')) if url.path else page.path
        if not target.is_file() or not target.resolve().is_relative_to(ROOT):
            errors.append(f'{name}: broken local reference {ref}')
        elif url.fragment and target.suffix == '.html':
            linked = pages.get(target.name)
            if linked is None or unquote(url.fragment) not in linked.ids:
                errors.append(f'{name}: broken fragment {ref}')
    # Main navigation must consistently link to the four sections.
    required = ('index.html', 'about.html', 'projects.html', 'resume.html')
    for href in required:
        if not any(a.get('href') == href for a in page.links):
            errors.append(f'{name}: navigation missing {href}')

if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages; local links/assets/fragments; IDs/headings; image descriptions; contact-detail patterns.')
