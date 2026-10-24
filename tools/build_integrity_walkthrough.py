"""Build the example-case image and capture output from the public ZIP.

The code and result images already exist in assets/evidence. This verifies their
content against the runnable example and adds an equally sized input/case image.
Only synthetic example files are read. The ZIP runs in a temporary directory.
"""
from hashlib import sha256
from html import escape
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/evidence'
PUBLIC_ZIP = ROOT / 'assets/examples/handoff-integrity.zip'
NS = {'s': 'http://www.w3.org/2000/svg'}


def label(x, y, value, size=25, color='#f1f4ef', bold=False, mono=False):
    family = 'Consolas, monospace' if mono else 'Arial, sans-serif'
    return (f'<text xml:space="preserve" x="{x}" y="{y}" fill="{color}" '
            f'font-family="{family}" font-size="{size}" font-weight="{700 if bold else 400}">'
            f'{escape(value)}</text>')


def main():
    # The canonical ZIP carries LF bytes, independently of checkout line endings.
    with TemporaryDirectory(prefix='portfolio-walkthrough-') as tmp:
        with ZipFile(PUBLIC_ZIP) as archive:
            expected = {'handoff-integrity/' + name for name in (
                'README.md', 'verify.py', 'manifest.json',
                'sample/source-note.txt', 'sample/method-note.txt')}
            assert set(archive.namelist()) == expected
            archive.extractall(tmp)
        working = Path(tmp) / 'handoff-integrity'
        before = {p.relative_to(working).as_posix(): sha256(p.read_bytes()).hexdigest()
                  for p in working.rglob('*') if p.is_file()}
        normal = subprocess.run([sys.executable, '-B', 'verify.py'], cwd=working,
                                check=True, capture_output=True, text=True).stdout.strip()
        tested = subprocess.run([sys.executable, '-B', 'verify.py', '--self-test'], cwd=working,
                                check=True, capture_output=True, text=True).stdout.strip()
        after = {p.relative_to(working).as_posix(): sha256(p.read_bytes()).hexdigest()
                 for p in working.rglob('*') if p.is_file()}
        assert before == after, 'The example must leave its downloaded files unchanged.'
        source = (working/'verify.py').read_text(encoding='utf-8')
        code = source.split('# BEGIN PUBLIC EXCERPT\n')[1].split('# END PUBLIC EXCERPT')[0].strip()
        notes = [(name, (working/'sample'/name).read_text(encoding='utf-8').splitlines()[1])
                 for name in ('source-note.txt', 'method-note.txt')]

    assert normal == 'MATCH: both sample files match the supplied manifest'
    expected_passes = [
        'intact sample matches its manifest', 'changed file is detected',
        'missing file is detected', 'unexpected file is detected',
        'malformed manifest is rejected',
    ]
    assert tested.splitlines() == ['PASS: ' + line for line in expected_passes]
    svg = ET.parse(OUT/'ra-code.svg')
    code_lines = [e.text or '' for e in svg.findall('.//s:text', NS)
                  if e.attrib.get('font-family') == 'Consolas, monospace']
    assert '\n'.join(code_lines).strip() == code, 'Code image is stale.'
    result_text = [e.text for e in ET.parse(OUT/'ra-results.svg').findall('.//s:text', NS)]
    assert sum(t == 'PASS' for t in result_text) == 5
    assert all(line[0].upper() + line[1:] in result_text for line in expected_passes)

    output = '$ python verify.py\n' + normal + '\n\n$ python verify.py --self-test\n' + tested + '\n'
    (OUT/'integrity-example-output.txt').write_text(output, encoding='utf-8', newline='\n')

    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="0 0 1400 900" role="img" aria-labelledby="title desc">',
             '<title id="title">The sample files and five cases being tested</title>',
             '<desc id="desc">Two synthetic notes and a manifest are tested unchanged, changed, missing, with an extra file, and with an invalid fingerprint. Each change is made in a temporary copy.</desc>',
             '<rect width="1400" height="900" fill="#0b151b"/><path d="M60 55H1340" stroke="#72d7c9" stroke-width="3"/>',
             label(60,105,'02 / EXAMPLES · THE ACTUAL TEST CASES',20,'#72d7c9',True),
             label(60,175,'Two notes. Five controlled examples.',46,bold=True),
             label(60,225,'The manifest records the expected names and fingerprints of both files.',25,'#b3c6cc')]
    for x, (name, identity) in zip((60,715), notes):
        parts.extend([f'<rect x="{x}" y="270" width="625" height="130" rx="14" fill="#13252e" stroke="#36515b"/>',
                      label(x+25,315,'sample/' + name,26,bold=True,mono=True),
                      label(x+25,354,identity,24,'#b3c6cc',mono=True),
                      label(x+25,382,'Synthetic text file',20,'#72d7c9')])
    cases = [
        ('UNCHANGED', 'Keep both notes exactly as supplied.'),
        ('CHANGED', 'Append one line to source-note.txt.'),
        ('MISSING', 'Remove source-note.txt from the test copy.'),
        ('UNEXPECTED', 'Add sample/extra.txt to the test copy.'),
        ('MALFORMED', 'Replace an expected fingerprint with "invalid".'),
    ]
    for i, (name, description) in enumerate(cases):
        y = 430 + i*65
        parts.extend([f'<rect x="60" y="{y}" width="1280" height="54" rx="9" fill="#13252e"/>',
                      label(82,y+35,name,23,'#72d7c9',True),
                      label(332,y+35,description,25)])
    parts.extend(['<path d="M60 794H1340" stroke="#36515b"/>',
                  label(60,837,'Changes stay in a temporary copy. The downloaded notes and manifest remain unchanged.',21,'#b3c6cc'),
                  '</svg>'])
    target = OUT/'ra-example-cases.svg'
    target.write_text('\n'.join(parts) + '\n', encoding='utf-8', newline='\n')
    ET.parse(target)
    print('PASS: public ZIP run, five cases, unchanged sample files, and matching code/result images.')
    print('Built assets/evidence/ra-example-cases.svg (1400 × 900).')


if __name__ == '__main__':
    main()
