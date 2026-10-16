# Brandon Santor · Geospatial Research & Software

Static personal portfolio with seven case studies: NWSW research and spatial evidence, Mars Explorer, COLE, Tree-Ring Atlas Explorer, Thermal Vent Atlas Explorer, PhalAInx AI, and smartphone GNSS research. PhalAInx AI is Brandon's independent brand; Research Architect and a multi-LLM collaboration workspace are distinct software products under it. The collaboration workspace remains in development.

Open `index.html` in a modern browser or serve the repository root with a static HTTP server. No build or package installation is required.

- `index.html` features NWSW's broader research, GIS, and evidence-integration work.
- `about.html`, `projects.html`, and `resume.html` provide the main sections.
- Seven `project-*.html` files provide detailed individual case studies and captioned galleries, each with exactly three images. The established `project-research-architect.html` URL now presents the PhalAInx AI brand and its products.
- `resume.pdf` is a sanitized public résumé created from reviewed portfolio facts.
- `site.js` provides the saved theme preference, legacy fragment redirects, and résumé print control.
- `gallery.js` provides manual carousels and a keyboard-accessible native-dialog image viewer with fit/full-resolution controls, loading/error feedback, and focus restoration.
- `project-intro.js` starts the PhalAInx introduction when a visitor opens its project link, with Skip, native playback controls, replay, reduced-motion handling, and failed-playback recovery.
- `style.css` contains responsive layouts, dark/light themes, reduced-motion support, and print styles.
- `assets/icons/` contains original TRAE, TVAE, and PhalAInx artwork. Mars and COLE use marks derived from their original interface styles.
- `assets/screenshots/` contains reviewed application captures and author-supplied research figures. Its README records provenance and limitations.
- `assets/video/` contains the original PhalAInx branded introduction clip and its provenance.
- `assets/tamu-white.svg` is the official white university mark used in the header.

Dark mode is the default. The theme control stores only a theme preference in the visitor's browser. Core navigation, case-study content, image links, and native video playback work without JavaScript. Image galleries do not advance automatically. Portfolio links to PhalAInx include `?intro=1`: its 10-second clip starts muted in a native dialog and reveals the project when it ends or is skipped. The query is consumed so a refresh does not repeat it. Direct visits retain manual playback and replay. Reduced-motion visitors get manual Play; failed autoplay keeps controls and Skip available. Playback pauses when the page becomes hidden. Old home-page fragments redirect to corresponding pages.

The public pages, images, and résumé omit visible private contact information, phone numbers, and postal addresses. Private CV/résumé originals, raw research packages, private evidence records, and imported user datasets are excluded. Both QR codes in the author-selected GNSS figures are preserved: they link to the author's existing public research PDFs, whose original contents are outside this repository. Screenshot controls are static illustrations, not embedded running applications.

GNSS figures distinguish the measured campus study from an illustrative present-day New Orleans scenario. The companion layout shows how overlapping modeled buffers form an approximately 50-acre footprint; it is not a reconstruction of historical Katrina calls.

Before publishing, run `python tools/check_site.py`, `node --check site.js`, `node --check gallery.js`, `node --check project-intro.js`, and `git diff --check`. The validator checks the exact gallery count and thumbnail indices. Browser checks should cover desktop/mobile layout, gallery wrapping and thumbnails, repeated lightbox open/close, keyboard/focus behavior, zoom, failed-image recovery, theme persistence, project-entry video, skip/replay/end cleanup, and navigation.

GitHub Pages serves the repository root from `main`. Push using an account with write access.
