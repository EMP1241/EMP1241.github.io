# Portfolio refresh — October 24, 2026

## Changes

- Added the NWSW **research project** to the résumé's selected research, separate from its application. Its existing professional-experience entry retains three bullets.
- Added a native, sticky section-navigation bar to all 15 content pages. The short 404 page has no section directory. Narrow layouts scroll the link row horizontally instead of wrapping it over the content. Anchor clearance and print hiding are shared CSS rules.
- Rewrote the RA case study around current capabilities: role-specific kits, persistent planning, scoped written plans, recorded approval of exact PDFs, delivery, evidence retrieval, diagnostics, and recovery. Version/check history is expandable. Current factory: 2.6.1 preview r1; runtime 2.4.0 and scientific library 1.9 remain distinct.
- Updated the studio product-family graphic and its generator to the current RA version and planning workflow.
- Added the supplied synthetic team and Hub plan PDFs as separate new-tab links. They retain their original 2.6.0 draft labels and unresolved setup items; they are not represented as approved studies or newly generated 2.6.1 output.
- Retained the portfolio's newer Edition 10 white paper. The supplied 2.6.1 ZIP contains an older Edition 9 paper; replacing Edition 10 with it would regress the document. The current PDF-review gate is documented separately, not attributed to the earlier paper.
- Updated Mars Explorer for the public 0.9.2 web edition and separate Windows preview, with fresh application screenshots, station/imagery coverage, gallery scope, direct access links, and setup instructions.
- Kept the résumé download at two pages by arranging its selected project records in two columns, preserving their text and links.

## Sources

- User-supplied `RA_2_6_1_CHANGELOG.md`, `Research_Architect_v2_6_1_preview_r1.zip`, and the two synthetic plan PDFs. Read source documents and package contents; did not execute delivered code.
- Mars Explorer resident expert consultation against the current application, deployment records, expanded-gallery report, portable manifest, and exact archive.
- Public browser edition: <https://marsexplorer.onrender.com/>. The supplied `onrenderer.com` spelling was incorrect.
- Windows binary and SHA-256: [public download receipt](mars-desktop-public-download.json). The 640,853,236-byte clean archive is a GitHub release asset, not a Git-tracked website file. GitHub's returned digest matches the qualified source archive; anonymous range retrieval returned HTTP 206 and a ZIP signature.

## Validation

- Static checks passed across 16 root pages: assets, links, fragments, headings, IDs, image descriptions, and contact-detail patterns.
- All 15 content pages have exactly one section bar with valid native fragment targets; no JavaScript is required for the links.
- Browser inspection confirmed sticky placement, target-heading clearance, gallery content, and the Mars access links. Three 390-pixel iframe layouts showed NWSW, RA, and Mars section bars remaining at the top with horizontally scrollable links. Early geometry samples during smooth scrolling were not treated as settled-position measurements.
- Existing gallery lifecycle, playback, static image-set navigation, and lightbox-cleanup checks passed.
- Résumé PDF source fingerprint matched; both regenerated pages were rendered and visually inspected. The two supplied plan cover pages were rendered and inspected without changing their bytes.
- No new scientific findings or model-performance claims were inferred. Current desktop qualification limits and RA onboarding/review limits remain visible in the appropriate detailed scope statements.
