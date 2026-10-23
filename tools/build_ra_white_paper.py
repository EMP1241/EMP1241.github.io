"""Verify the owner-supplied RA white paper; portfolio authoring is retired.

The Agent Builder project maintains the PDF and its matching Markdown text.
Keep the historical command name for existing verification workflows. Import
reviewed deliveries unchanged and update docs/ra-white-paper-delivery.json;
never rebuild the owner-authored PDF from the former portfolio template.
"""
from pathlib import Path
import argparse
import hashlib
import json
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


def check():
    receipt = json.loads((ROOT / 'docs/ra-white-paper-delivery.json').read_text(encoding='utf-8'))
    targets = {
        'pdf_sha256': ROOT / 'assets/documents/research-architect-white-paper.pdf',
        'source_sha256': ROOT / 'docs/research-architect-white-paper.md',
    }
    for key, path in targets.items():
        if hashlib.sha256(path.read_bytes()).hexdigest() != receipt[key]:
            raise SystemExit(f'Owner delivery mismatch: {path.name}; review the delivered artifact before publication')
    pages = len(PdfReader(targets['pdf_sha256']).pages)
    if pages != receipt['pages']:
        raise SystemExit('Owner delivery page count mismatch')
    print(f'Owner white paper verified: {pages} pages; PDF and source hashes match the delivery receipt')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if not args.check:
        parser.error('Authoring is maintained in Agent Builder. Use --check to verify the imported delivery.')
    check()
