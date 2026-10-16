# Brandon Santor · Geospatial Research & Software

Static personal portfolio with nine case studies: NWSW research, the independent Spatial Evidence Workbench, Mars Explorer, COLE, Tree-Ring Atlas Explorer, Thermal Vent Atlas Explorer, PhalAInx, smartphone GNSS research, and High Command. PhalAInx is Brandon's independent software studio. Research Architect and High Command are separate products. High Command is in active testing.

Open `index.html` in a modern browser or serve the repository root with a static HTTP server. No build or package installation is required.

- `index.html` features NWSW's broader research, GIS, and evidence-integration work.
- `about.html`, `projects.html`, and `resume.html` provide the main sections.
- Nine `project-*.html` files provide detailed case studies and galleries, each with three images. The NWSW research page uses architecture diagrams; the workbench page shows real QA application captures. The established `project-research-architect.html` URL presents the PhalAInx studio and its products.
- `resume.pdf` is a sanitized public résumé created from reviewed portfolio facts.
- `assets/documents/research-architect-white-paper.pdf` is the author-provided revised white paper; explicit links open it in a separate browser tab without an embedded PDF viewer.
- `site.js` provides the saved theme preference, legacy fragment redirects, and résumé print control.
- `gallery.js` provides manual carousels and a keyboard-accessible native-dialog image viewer with fit/full-resolution controls, loading/error feedback, and focus restoration.
- `project-intro.js` starts the PhalAInx introduction when a visitor opens its project link, with Skip, native playback controls, replay, reduced-motion handling, and failed-playback recovery.
- `style.css` contains responsive layouts, dark/light themes, reduced-motion support, and print styles.
- `research.css` adds project-specific decorative motifs, workflow diagrams, studio branding, and the expanded résumé layout.
- `workflow.js` changes the headline and input/process/output diagram for each 01–04 stage, with keyboard navigation. All stages remain readable without JavaScript.
- `motion.js` provides bounded parallax and slow hero fades, with a persistent pause control. Motion respects reduced-motion preferences and stops while hidden; hero rotation pauses on hover, focus, and outside the viewport.
- `assets/icons/` contains original TRAE, TVAE, PhalAInx, and author-supplied Research Architect artwork. Mars and COLE use interface-derived marks.
- `assets/screenshots/` contains reviewed application captures and author-supplied research figures. Its README records provenance and limitations.
- `assets/video/` contains the original PhalAInx branded introduction clip and its provenance.
- `assets/tamu-white.svg` is the official white university mark used in the header.

Dark mode is the default. Theme and optional effects preferences are saved locally in the visitor’s browser. Core navigation, case-study content, image links, and native video playback work without JavaScript. Image galleries do not advance automatically. Portfolio links to PhalAInx include `?intro=1`: its 10-second clip starts muted in a native dialog and reveals the project when it ends or is skipped. The query is consumed so a refresh does not repeat it. Direct visits retain manual playback and replay. Reduced-motion visitors get manual Play; failed autoplay keeps controls and Skip available. Playback pauses when the page becomes hidden. Old home-page fragments redirect to corresponding pages.

The public pages, images, and résumé omit visible private contact information, phone numbers, and postal addresses. Private CV/résumé originals, raw research packages, private evidence records, and imported user datasets are excluded. Both QR codes in the author-selected GNSS figures are preserved: they link to the author's existing public research PDFs, whose original contents are outside this repository. Screenshot controls are static illustrations, not embedded running applications.

GNSS figures distinguish the measured campus study from an illustrative present-day New Orleans scenario. The companion layout shows how overlapping modeled buffers form an approximately 50-acre footprint; it is not a reconstruction of historical Katrina calls.

Before publishing, run `python tools/check_site.py`, `node --check site.js`, `node --check gallery.js`, `node --check project-intro.js`, `node --check workflow.js`, `node --check motion.js`, and `git diff --check`. The validator checks the exact gallery count and thumbnail indices. Browser checks should cover desktop/mobile layout, gallery wrapping and thumbnails, repeated lightbox open/close, keyboard/focus behavior, zoom, failed-image recovery, theme persistence, project-entry video, skip/replay/end cleanup, and navigation.

GitHub Pages serves the repository root from `main`. Push using an account with write access.

High Command has its own `project-high-command.html` case study, a four-stage command workflow, and three author-supplied application screenshots. The Command Deck and Settings screenshots carry v0.5.6 labels; the home-screen image is a still from the live animated application, as identified by the creator. Product descriptions are based on the supplied executive summary; the owner’s current status, Active testing, supersedes its older Proposed / In Development label.

Product audiences: High Command is for an individual coordinating multiple models across projects; Research Architect generates individual AI kits for members of a human team working within a shared research system. The owner confirmed HC’s current core stack as Tauri 2, React/TypeScript, Rust, and SQLite. Other tooling and QA items from the supplied setup plan are identified as development/validation plans rather than completed verification.
