"""Build the NWSW architecture, research-sequence and continuity illustrations.

SVGs are published assets. Optional PNG previews are for visual inspection.
Requires Pillow and Windows Segoe UI fonts, like build_research_network.py.
"""
from pathlib import Path
from html import escape
import argparse
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BG, PANEL, BORDER = '#0b151b', '#14252c', '#3d5965'
WHITE, MUTED = '#f3f0e7', '#c0ced3'
PINK, TEAL, GOLD = '#e4a5ab', '#88d5d2', '#e9c38b'


class Diagram:
    def __init__(self, title, description):
        self.image = Image.new('RGB', (2560, 1600), BG)
        self.draw = ImageDraw.Draw(self.image)
        self.svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="800" viewBox="0 0 1280 800" role="img" aria-labelledby="title desc">',
                    f'<title id="title">{escape(title)}</title>',
                    f'<desc id="desc">{escape(description)}</desc>',
                    f'<rect width="1280" height="800" fill="{BG}"/>']

    def rect(self, box, fill=PANEL, stroke=BORDER, radius=16):
        x, y, x2, y2 = box
        self.draw.rounded_rectangle(tuple(int(v * 2) for v in box), radius=radius * 2, fill=fill, outline=stroke, width=3)
        self.svg.append(f'<rect x="{x}" y="{y}" width="{x2-x}" height="{y2-y}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')

    def line(self, points, color=TEAL, width=3):
        self.draw.line([(int(x * 2), int(y * 2)) for x, y in points], fill=color, width=width * 2, joint='curve')
        self.svg.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in points)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')

    def circle(self, x, y, radius, fill=PANEL, stroke=BORDER, width=2):
        self.draw.ellipse(tuple(int(v * 2) for v in (x-radius, y-radius, x+radius, y+radius)),
                          fill=fill, outline=stroke, width=width * 2)
        self.svg.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')

    def arrow(self, points, color=TEAL):
        self.line(points, color)
        x, y = points[-1]
        px, py = points[-2]
        a = math.atan2(y-py, x-px)
        vertices = [(x, y), (x-12*math.cos(a)+6*math.sin(a), y-12*math.sin(a)-6*math.cos(a)),
                    (x-12*math.cos(a)-6*math.sin(a), y-12*math.sin(a)+6*math.cos(a))]
        self.draw.polygon([(int(x*2), int(y*2)) for x, y in vertices], fill=color)
        self.svg.append(f'<polygon points="{" ".join(f"{x},{y}" for x,y in vertices)}" fill="{color}"/>')

    def text(self, x, y, value, size=24, color=WHITE, bold=False, max_width=None):
        font = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf', size * 2)
        width = self.draw.textlength(value, font=font)/2
        if max_width is not None:
            assert width <= max_width, f'Text exceeds its column: {value} ({width:.1f} > {max_width})'
        assert 0 <= x and x + width < 1280 and 0 <= y < 800, value
        self.draw.text((x*2, y*2), value, font=font, fill=color, anchor='lt')
        self.svg.append(f'<text x="{x}" y="{y+size*.8}" font-family="Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(value)}</text>')

    def save(self, name, preview_dir):
        (ROOT/'assets'/f'{name}.svg').write_text('\n'.join(self.svg+['</svg>']), encoding='utf-8')
        if preview_dir:
            preview_dir.mkdir(parents=True, exist_ok=True)
            self.image.resize((1280, 800), Image.Resampling.LANCZOS).save(preview_dir/f'{name}.png')


def architecture(preview_dir):
    g = Diagram('Research Architect generates the NWSW role kits',
                'Research Architect generates three project role kits: Hub, contributor Pods with individual AI Spokes, and Ingestor. Branch arrows indicate generation, not a sequence of review steps. The independently built Spatial Evidence Workbench is used alongside the coordination system; it is not a generated kit or an asserted automated integration.')
    g.text(60, 48, 'NWSW / SYSTEM ARCHITECTURE', 18, PINK, True)
    g.text(60, 94, 'From framework to research roles.', 46, bold=True)
    g.text(60, 158, 'Branch arrows show which role kits the framework generates.', 25, MUTED)
    g.rect((60, 230, 370, 560), stroke=PINK)
    g.text(88, 262, 'REUSABLE FRAMEWORK', 17, PINK, True, 255)
    g.text(88, 320, 'Research', 39, bold=True, max_width=255)
    g.text(88, 371, 'Architect', 39, bold=True, max_width=255)
    g.text(88, 449, 'Roles, methods', 24, MUTED)
    g.text(88, 484, 'and review controls', 24, MUTED, max_width=255)

    # A single directed branch encodes generation of each role kit.
    g.line([(370, 395), (440, 395)], PINK)
    g.line([(440, 275), (440, 515)], PINK)
    for y in (275, 395, 515):
        g.arrow([(440, y), (520, y)], PINK)
    g.text(520, 205, 'GENERATED NWSW ROLE KITS', 17, PINK, True)
    roles = [
        (230, 'Hub', 'Assignments, research review and final acceptance.', PINK),
        (350, 'Contributor kits', 'Individual AI Spokes for human-led Pods.', TEAL),
        (470, 'Ingestor', 'File checks and specified reproduction steps.', GOLD),
    ]
    for y, name, detail, accent in roles:
        g.rect((520, y, 1220, y+90), stroke=accent)
        g.text(548, y+13, name, 30, accent, True, 645)
        g.text(548, y+54, detail, 22, MUTED, max_width=645)

    # Deliberately no connector: this application is independently built.
    g.rect((60, 630, 1220, 750), stroke=BORDER)
    g.text(86, 649, 'INDEPENDENT APPLICATION', 16, GOLD, True)
    g.text(86, 684, 'Spatial Evidence Workbench', 31, bold=True, max_width=570)
    g.text(720, 657, 'Mapped investigations and exports.', 23, MUTED, max_width=470)
    g.text(720, 696, 'Used alongside the research system.', 23, MUTED, max_width=470)
    g.text(60, 773, 'Brandon Santor / Research system architecture', 15, MUTED)
    g.save('nwsw-system', preview_dir)


def investigation(preview_dir):
    g = Diagram('NWSW source-to-evidence research sequence',
                'Four stages connected by downward arrows: reconcile source records; prepare geography; check geographic relationships; integrate reviewed contributions. Preserve source definitions, boundary versions, documented joins, methods, attribution and uncertainty. This is a research workflow, not a claim of completed biological findings.')
    g.text(60, 48, 'NWSW / THE INVESTIGATION', 18, PINK, True)
    g.text(60, 94, 'From source records to spatial evidence.', 43, bold=True)
    g.text(60, 155, 'A clear path from source review to cross-team synthesis.', 25, MUTED)
    stages = [
        ('01', 'Reconcile source records', 'Check versions, dates and reporting definitions.'),
        ('02', 'Prepare the geography', 'Retain boundary versions, identifiers and coordinate systems.'),
        ('03', 'Check geographic relationships', 'Document joins, geographic support and unresolved gaps.'),
        ('04', 'Integrate reviewed contributions', 'Keep methods, attribution and uncertainty with the synthesis.'),
    ]
    for i, (number, title, detail) in enumerate(stages):
        y = 212 + i*135
        g.rect((60, y, 1220, y+100))
        g.text(86, y+31, number, 30, TEAL, True)
        g.text(155, y+12, title, 31, bold=True, max_width=1025)
        g.text(155, y+57, detail, 24, MUTED, max_width=1025)
        if i < 3:
            g.arrow([(105, y+100), (105, y+135)], TEAL)
    g.text(60, 768, 'Brandon Santor / Research leadership, GIS development and synthesis', 17, MUTED)
    g.save('nwsw-research', preview_dir)


def continuity(preview_dir):
    g = Diagram('NWSW research context restored for a new session',
                'Two inputs support a resumed research session. The selected saved checkpoint supplies decisions and open work. Source-linked context is retrieved in needed pages and checked using identity and hashes. The numbered pages are schematic, with no fixed page count. Original records remain retained. This illustrates explicit retrieval and restoration, not automatic synchronization or guaranteed AI recall.')
    g.text(60, 48, 'NWSW / RESEARCH CONTINUITY', 18, PINK, True)
    g.text(60, 94, 'Keep the thread across sessions.', 46, bold=True)
    g.text(60, 158, 'Restore saved state. Retrieve the evidence the next task needs.', 25, MUTED)

    # Two distinct inputs converge on a session: saved state and source retrieval.
    # The checkpoint is a bookmark, not an assertion that all sources fit in memory.
    g.circle(195, 300, 90, fill=BG, stroke=BORDER)
    g.circle(195, 300, 72, fill=PANEL, stroke=PINK, width=3)
    g.rect((172, 265, 218, 326), fill='#26333c', stroke=PINK, radius=4)
    g.line([(183, 277), (207, 277)], PINK, 3)
    g.line([(183, 290), (207, 290)], PINK, 3)
    g.line([(183, 303), (198, 303)], PINK, 3)
    g.circle(244, 351, 19, fill=BG, stroke=PINK)
    g.line([(235, 352), (241, 358), (253, 344)], PINK, 3)
    g.text(60, 410, 'Selected checkpoint', 31, PINK, True, 365)
    g.text(60, 455, 'Decisions and open work', 23, MUTED, max_width=365)
    g.arrow([(285, 300), (545, 300), (545, 278), (640, 278)], PINK)
    g.text(350, 264, 'Load state', 22, PINK, True, 180)

    # Stacked source pages communicate a retained archive without fake records.
    for offset, color in [(0, BORDER), (14, '#55757f'), (28, TEAL)]:
        g.rect((60+offset, 530-offset, 365+offset, 674-offset), fill=PANEL, stroke=color, radius=8)
    g.text(112, 530, 'Original records', 28, TEAL, True, 255)
    g.text(112, 577, 'Retained originals', 21, MUTED, max_width=255)
    for x, length in [(112, 105), (235, 125)]:
        g.line([(x, 620), (x+length, 620)], BORDER, 5)
    g.arrow([(393, 586), (550, 586), (550, 486), (640, 486)], TEAL)
    g.text(414, 620, 'Retrieve', 22, TEAL, True, 180)

    # A large open work surface keeps the image readable at gallery scale.
    g.rect((640, 222, 1220, 700), fill='#101f28', stroke='#68828f', radius=18)
    g.line([(640, 278), (1220, 278)], BORDER, 2)
    g.text(670, 240, 'NEW SESSION', 18, MUTED, True, 390)
    for x in (1140, 1162, 1184):
        g.circle(x, 250, 5, fill=BORDER, stroke=BORDER, width=1)
    g.text(674, 310, 'Restore the selected state', 29, PINK, True, 512)
    g.rect((674, 362, 1186, 408), fill='#25303a', stroke=BORDER, radius=6)
    g.text(693, 374, 'Decisions', 22, WHITE, True, 190)
    g.line([(901, 375), (901, 395)], BORDER, 2)
    g.text(928, 374, 'Open work', 22, WHITE, True, 235)
    g.text(674, 446, 'Retrieve context as needed', 26, TEAL, True, 512)
    for i, x in enumerate((674, 852, 1030), 1):
        g.rect((x+6, 500, x+146, 570), fill=BG, stroke=BORDER, radius=6)
        g.rect((x, 494, x+140, 564), fill='#1b333b' if i == 1 else PANEL,
               stroke=TEAL if i == 1 else BORDER, radius=6)
        g.text(x+20, 513, f'0{i}' if i < 3 else '...', 27, TEAL, True, 60)
        g.line([(x+69, 523), (x+116, 523)], BORDER, 3)
        g.line([(x+69, 539), (x+101, 539)], BORDER, 3)
    g.text(674, 605, 'Check source identity and hashes', 24, MUTED, max_width=512)
    g.text(674, 650, 'Continue the assignment', 26, WHITE, True, 512)

    g.line([(60, 736), (1220, 736)], BORDER, 1)
    g.text(60, 761, 'Illustrated mechanism / Context is retrieved when a session resumes.', 19, MUTED, max_width=1160)
    g.save('nwsw-context-recovery', preview_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview-dir', type=Path)
    args = parser.parse_args()
    architecture(args.preview_dir)
    investigation(args.preview_dir)
    continuity(args.preview_dir)
    print('Built NWSW architecture, research sequence and context recovery illustrations.')
