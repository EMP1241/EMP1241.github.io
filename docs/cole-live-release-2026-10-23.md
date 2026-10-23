# COLE 1.0 public website reconciliation

The official public address is https://costoflivingexplorer.onrender.com/.
Both web and Windows editions are released as 1.0.0. This supersedes the
previous portfolio's current-status labels (hosted 0.11.0, Windows 0.10.0,
and 1.0 in preparation); earlier dated audit records remain historical.

## Evidence inspected

- COLE owner records: `cole-app/output/releases/1.0.0-20261023/DELIVERY.md`
  and `cole-app/output/address-migration-20261023/DELIVERY.md`.
- Release tag v1.0.0 / commit b64f39a; official-address migration c417a67.
- New-host browser receipt: all ten suites passed, completed October 23,
  2026 at 19:48:35 UTC. Runtime calculations and final Windows ZIP did not
  change during the address migration.
- The resident COLE expert confirmed D083/F122 and D084/F123 already preserve
  these delivery and address updates in the shared project knowledge.

## Fresh portfolio-side inspection

Chrome loaded the new public website and displayed “COLE 1.0 · Free web edition.”
A synthetic scenario (one adult, no children, $60,000 annual take-home,
Texas) returned 254 counties. Cameron and Crosby county details loaded;
both were added to a two-county comparison. No console errors were captured
during these interactions. A 390-pixel viewport check showed stacked county
details and no document-level horizontal overflow (375-pixel client/scroll
width, excluding the scrollbar). This was browser resizing, not a physical
phone or comprehensive accessibility test. Cold-start duration was not timed.

The live landing screen was captured for the portfolio gallery and project
card. The two existing 0.10.0 detail captures remain explicitly dated historical
captures; their version labels were not relabeled as 1.0 screenshots.

## Portfolio changes

Added a hero launch link that opens the official website in a separate tab;
replaced the lower preview link; updated release status, meta description,
project directory copy, résumé HTML/PDF, and verification disclosures.
Retained concise free-host wake-up and input-processing information.
The desktop GitHub release is private, so no public download link was invented.

## App follow-up

The live results page's source-links paragraph still says “Links require
internet; the application does not.” That wording applies to the packaged
Windows edition, not the hosted edition. The COLE owner should render this
sentence conditionally for the web edition. No COLE application files or
hosting settings were changed during this portfolio update.

The original preview service remains active to preserve distributed links.
Both services share free hosting allowances. Removing the old service needs
an intentional migration decision; this update does not alter either service.
