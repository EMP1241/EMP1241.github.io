# Maintaining publication facts

The editable source for shared RA/NWSW publication facts is
`data/project-facts.json` in `EMP1241/EMP1241.github.io`.
Its public URL is https://emp1241.github.io/data/project-facts.json.
RA's `publication/FACTS.json` is a generated snapshot. Do not edit the snapshot
or patch its generated consumers independently.

Each fact has a value, type, observation date, evidence source and scope.
Current inventory is checked against RA's version file, registries and actual
files. Historical results keep their observation dates. A new report edition
needs its actual PDF identity, physical page count and matched companions;
changing a catalog value does not establish new scientific evidence.

`publication/CONSUMERS.json` maps the repeated facts to editable templates.
The templates own surrounding prose. Generated pages and paper text must match
them exactly. Removing a binding also fails validation until its declared
coverage is deliberately updated. The Word templates contain only the bound
XML members; styles, relationships and figures remain in the owner document.

## Update procedure

1. Review the original evidence. Edit the canonical portfolio JSON, including
   the changed fact's date and source, and increment its revision. Keep private
   source files and local paths out of this public record. `inventory` prints
   the current RA-derived values for comparison; it does not silently change
   an approved publication record.
2. In the RA base directory, run:
   `python tools/publication_facts.py render --facts PORTFOLIO/data/project-facts.json`.
   This prepares the Markdown, Word fact fields, references and Figure 7 SVG.
   It also refreshes the changed library coverage hashes. It does not claim a
   stale PDF or bitmap is current.
3. When paper text or a figure changed, rebuild the affected artifact and
   inspect its rendered pages. Figure 7 can be regenerated with
   `python tools/render_publication_figure.py --pdftoppm PATH_TO_PDFTOPPM`;
   it updates the figure inside the Word document. Export the owner Word
   document to `docs/WHITE_PAPER.pdf` using the established document workflow.
   The portfolio never authors a second white paper.
4. Run `python tools/publication_facts.py seal --review-note "Describe the actual artifact review"`.
   This verifies every fact-bearing Word paragraph against PDF text and binds
   the reviewed files. A changed SVG with its old bitmap is rejected. Preserve
   previous receipts in editorial history before resealing a later edition.
5. Run `python tools/publication_facts.py sync-portfolio --portfolio PORTFOLIO`.
   The command requires the canonical JSON and RA snapshot to agree, imports
   the exact owner paper/reference/figure bytes, renders the portfolio and
   rebuilds the resume only when its HTML source changed. Inspect a rebuilt
   resume before publishing. Both copies of the shared checker are delivered
   together and their hashes are checked.
6. Run `python tools/publication_facts.py check --deep --facts PORTFOLIO/data/project-facts.json`.
   Build the RA package with `tools/build_pilot.py`; that build refuses drift.
   Run the portfolio's `tools/check_site.py` and its normal release checks.
   Review both diffs, publish the portfolio/canonical record, then publish RA.
   RA CI compares its snapshot with the public canonical record. Check both
   jobs and verify the deployed downloads before calling the release complete.

All paths above are examples supplied as command arguments; there is no
machine-specific path in the tools. Ordinary checks and portable package
builds are offline. `check --canonical-url` is the explicit read-only network
check used in RA CI. Archived packages intentionally retain their historical
snapshot and remain rebuildable offline.

The portfolio deploys only after fact checks, document checks, regression
tests and site validation pass. The previous site remains live if validation
fails. These checks prevent inconsistent publication of registered facts;
they cannot discover a new research result that has never been entered and
reviewed. Add new repeated facts to the catalog and templates when introducing
them into public prose. Unrelated dated measurements remain in their original
evidence records rather than being relabeled as current results.

## Dependencies and artifact review

Portable package checks use Python's standard library. Deep PDF verification
uses `pypdf`; resume rebuilding uses the existing ReportLab builder. Install
`requirements-publication.txt` for the maintained editorial workflow. Figure
rendering also needs Poppler's `pdftoppm`. The gate checks hashes and extracted
text; visual review remains necessary when layout changes.
