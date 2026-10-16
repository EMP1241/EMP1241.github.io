# Brandon Santor · Geospatial Research & Software

Static personal portfolio featuring the NWSW Spatial Evidence Workbench, Tree-Ring Atlas Explorer, Thermal Vent Atlas Explorer, Research Architect, and smartphone GNSS field research.

Open `index.html` in a modern browser or serve this repository's root with a static HTTP server. No build or package installation is required.

- `index.html` is the home page with the featured NWSW project.
- `about.html`, `projects.html`, and `resume.html` provide the main portfolio sections.
- `project-*.html` contains five full case studies, linked from the project collection.
- `resume.pdf` is a sanitized public résumé created from the reviewed portfolio facts.
- `site.js` provides the saved theme preference, legacy fragment redirects, and résumé print control.
- `style.css` contains the responsive layouts, dark and light themes, reduced-motion support, and résumé print styles.
- `assets/icons/` contains the original TRAE, TVAE, and PhalAInx application artwork in web-compatible PNG files.
- `assets/screenshots/` contains reviewed, genuine application captures; see its README for provenance.
- `assets/tamu-white.svg` is the official white university mark used in the header.

Dark mode is the default. The theme control stores only the visitor's theme preference in their browser and persists across pages. Project links open individual case-study pages. The résumé page provides a PDF download and a browser print control. Core navigation and content work without JavaScript. Old home-page section fragments redirect to their new pages when JavaScript is available.

The site excludes phone numbers, postal addresses, email addresses, and original private CV/résumé documents. No source research packages, private evidence, or user-imported datasets are included. The TVAE screenshot shows the app's base atlas in offline mode, with no imported data. NWSW artwork is an explicitly labeled workflow illustration, not research records or an analysis result.

Run `python tools/check_site.py` to check page structure, local links and assets, image descriptions, and contact-detail patterns before publishing. Run `node --check site.js` to check JavaScript syntax. Browser checks should cover mobile widths, navigation, theme persistence, screenshot viewing, and résumé download/printing.

To publish to GitHub Pages, push these files to this repository and serve the repository root. Authentication must use an account with write access.
