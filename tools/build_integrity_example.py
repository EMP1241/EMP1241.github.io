"""Build/check the public synthetic example with deterministic ZIP contents."""
from argparse import ArgumentParser
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'assets/examples/handoff-integrity'
ZIP = ROOT / 'assets/examples/handoff-integrity.zip'
FILES = ('README.md', 'verify.py', 'manifest.json', 'sample/source-note.txt', 'sample/method-note.txt')


def expected_outputs():
    # Git newline normalization cannot silently stale the downloadable package.
    content = {name: (EXAMPLE / name).read_bytes().replace(b'\r\n', b'\n')
               for name in FILES if name != 'manifest.json'}
    manifest = {'format': 'portfolio-integrity-example/1', 'files': {
        name: sha256(content[name]).hexdigest() for name in FILES if name.startswith('sample/')
    }}
    content['manifest.json'] = (json.dumps(manifest, indent=2) + '\n').encode('utf-8')
    memory = BytesIO()
    with ZipFile(memory, 'w') as archive:
        for name in FILES:
            info = ZipInfo('handoff-integrity/' + name, (2026, 10, 22, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, content[name])
    return content, memory.getvalue()


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    content, zipped = expected_outputs()
    if args.check:
        if any(not (EXAMPLE / name).is_file() or (EXAMPLE / name).read_bytes() != data
               for name, data in content.items()) or not ZIP.is_file() or ZIP.read_bytes() != zipped:
            raise SystemExit('Example source or ZIP is stale; rebuild tools/build_integrity_example.py.')
        print('PASS: manifest, source files and deterministic public ZIP agree.')
    else:
        for name, data in content.items():
            (EXAMPLE / name).write_bytes(data)
        ZIP.write_bytes(zipped)
        print('Built public example ZIP and matching manifest.')


if __name__ == '__main__':
    main()
