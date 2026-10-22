# A file-integrity check you can run

This public portfolio example makes one handoff control inspectable: comparing
received files with an expected file list and SHA-256 fingerprints. It was written
for the portfolio on October 22, 2026, using synthetic notes. It is a standalone
demonstration of the method described in the Research Architect case study, not
an extract or a release of the private RA or Spatial Evidence Workbench runtime.

## Run it

Requires Python 3.10 or newer. No packages, network connection, account, or API key
are needed. Extract the ZIP, open a terminal in the `handoff-integrity` folder,
and run:

```text
python verify.py
```

Expected output:

```text
MATCH: both sample files match the supplied manifest
```

Exercise the failure cases:

```text
python verify.py --self-test
```

Five `PASS` lines cover an intact package, changed bytes, a missing file, an
unexpected file, and an invalid digest. Tests change temporary copies and leave
the downloaded files alone. The verifier exits with status 1 on discrepancies
and status 0 when the expected files match.

## Inspect it

- `verify.py` contains the complete verifier and its small test exercise.
- `manifest.json` records the expected SHA-256 digest for each sample file.
- `sample/` contains two fictional text notes. No project datasets are included.

The manifest names exactly these two files. Unexpected entries in the sample
folder are reported. The verifier rejects symbolic links for the manifest,
sample folder, and named files; it does not follow them into other directories.
It reads original bytes, including line endings, so editing or converting a file
changes its fingerprint.

## What the result means

`MATCH` means the inspected bytes match this manifest. It does not establish who
created a file, whether a source is correct, whether an analysis is valid, or
whether a human has approved its use. A trusted expected manifest must be retained
separately in a real workflow: someone who replaces both files and manifest can
make a new matching pair. This example is not an authenticity or access-control
system and does not model concurrent writes to an active project.

Research Architect's full workflow also carries versions, review records,
receipts, and recovery state. This example isolates the byte-checking step so a
visitor can inspect and repeat it without access to private research.
