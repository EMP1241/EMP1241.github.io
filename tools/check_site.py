"""Dependency-free pre-publish checks for the static portfolio."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_EMAIL = 'brandon.santor@tamu.edu'
errors = []

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids, self.refs, self.images, self.headings, self.links = [], [], [], [], []
        self.open_heading = None
        self.gallery_count, self.gallery_slides, self.gallery_thumbnails = 0, 0, []
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'data-gallery' in attrs:
            self.gallery_count += 1
        if tag == 'figure' and 'gallery-slide' in attrs.get('class', '').split():
            self.gallery_slides += 1
        if 'data-slide' in attrs:
            self.gallery_thumbnails.append(attrs['data-slide'])
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag in ('a', 'link') and attrs.get('href'):
            self.refs.append(attrs['href'])
        if tag in ('img', 'script', 'source', 'track', 'video') and attrs.get('src'):
            self.refs.append(attrs['src'])
        if tag == 'video' and attrs.get('poster'):
            self.refs.append(attrs['poster'])
        if tag == 'img':
            self.images.append(attrs)
        if re.fullmatch('h[1-6]', tag):
            self.headings.append(int(tag[1]))
            if self.open_heading:
                errors.append(f'{self.path.name}: nested or unclosed heading')
            self.open_heading = tag
        if tag == 'a':
            self.links.append(attrs)

    def handle_endtag(self, tag):
        if re.fullmatch('h[1-6]', tag):
            if tag != self.open_heading:
                errors.append(f'{self.path.name}: mismatched heading end tag {tag}')
            self.open_heading = None

pages = {p.name: Page(p) for p in ROOT.glob('*.html')}
expected = {'index.html', 'about.html', 'projects.html', 'resume.html', 'project-nwsw.html',
            'project-trae.html', 'project-tvae.html', 'project-phalainx.html', 'project-research-architect.html', 'project-gnss.html',
            'project-mars.html', 'project-cole.html', 'project-nwsw-workbench.html', 'project-high-command.html', 'project-suits.html', '404.html'}
if set(pages) != expected:
    errors.append(f'Unexpected page set: {set(pages) ^ expected}')
email = re.compile(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}', re.I)
phone = re.compile(r'(?<!\d)(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\d)')
listed_projects = ['project-nwsw.html', 'project-research-architect.html', 'project-mars.html',
                   'project-trae.html', 'project-tvae.html', 'project-high-command.html',
                   'project-nwsw-workbench.html', 'project-cole.html', 'project-gnss.html', 'project-suits.html']
if 'projects.html' in pages:
    directory_order = list(dict.fromkeys(urlsplit(a.get('href', '')).path for a in pages['projects.html'].links
                                        if urlsplit(a.get('href', '')).path.startswith('project-')))
    if directory_order != listed_projects:
        errors.append('projects.html: requires ten ordered project entries; the studio is unlisted')
studio_products = {'project-research-architect.html', 'project-high-command.html'}
for name, page in pages.items():
    studio_links = [a for a in page.links if urlsplit(a.get('href', '')).path == 'project-phalainx.html']
    if name in studio_products and not studio_links:
        errors.append(f'{name}: missing studio attribution link')
    if name not in studio_products | {'project-phalainx.html'} and studio_links:
        errors.append(f'{name}: the studio should be reached from its product pages')
    if page.gallery_count and (page.gallery_count != 1 or page.gallery_slides != 3 or page.gallery_thumbnails != ['0', '1', '2']):
        errors.append(f'{name}: requires exactly three gallery items with matching thumbnails')
    if page.headings.count(1) != 1:
        errors.append(f'{name}: requires exactly one h1')
    if any(next_level > level + 1 for level, next_level in zip(page.headings, page.headings[1:])):
        errors.append(f'{name}: heading outline skips a level')
    if any(n > 1 for n in Counter(page.ids).values()):
        errors.append(f'{name}: duplicate IDs')
    if 'main' not in page.ids or 'top' not in page.ids:
        errors.append(f'{name}: missing skip-link or top target')
    for img in page.images:
        if not all(key in img for key in ('alt', 'width', 'height')):
            errors.append(f'{name}: image missing alt or dimensions')
    text = page.path.read_text(encoding='utf-8')
    if name == '404.html':
        if '<base ' in text:
            errors.append('404.html: base URL would redirect same-page skip links')
        for ref in page.refs:
            url = urlsplit(ref)
            if not url.scheme and not url.netloc and url.path and not url.path.startswith('/'):
                errors.append(f'404.html: nested missing URLs require root-relative assets and links: {ref}')
    if any(address.lower() != PUBLIC_EMAIL for address in email.findall(text)):
        errors.append(f'{name}: unapproved email address')
    mail_links = [a.get('href', '') for a in page.links
                  if urlsplit(a.get('href', '')).scheme.lower() == 'mailto']
    if not mail_links or any(href != 'mailto:' + PUBLIC_EMAIL for href in mail_links):
        errors.append(f'{name}: missing or incorrect public email link')
    if phone.search(text) or 'tel:' in text or '[ADD]' in text:
        errors.append(f'{name}: private contact detail or unfinished placeholder')
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
        if not any(a.get('href', '').lstrip('/') == href for a in page.links):
            errors.append(f'{name}: navigation missing {href}')

if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages; local links/assets/fragments; IDs/headings; image descriptions; contact-detail patterns.')
