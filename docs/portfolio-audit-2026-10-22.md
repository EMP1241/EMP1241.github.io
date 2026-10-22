# Portfolio audit · October 22, 2026

Scope: the 15-page public portfolio, shared scripts and styles, current media presentation, résumé download, and internal navigation. This review checks how the portfolio presents the work; it is not a new validation of the underlying research or a fresh release audit of every application.

## Fixed

| Finding | Why it mattered | Correction |
| --- | --- | --- |
| A manually paused video restarted after scrolling away and returning. Lifecycle updates also reapplied mute. | Playback could override a visitor's explicit choice. | Mouse, touch, and playback-key interactions transfer playback control to the visitor. Visibility changes still stop offscreen media, but do not restart or remute a manually controlled clip. The same rule applies in the lightbox. |
| Keyboard video interaction left the carousel timer running. | A clip could disappear while someone used its native controls. | Keyboard playback interaction pauses slide rotation, as mouse/touch interaction already did. Tab navigation retains its normal behavior. |
| Homepage captions exceeded their fixed height on a 320-pixel screen. | Part of the explanation and project link required a separate scroll inside the caption. | Captions grow to fit their text. Stacked inactive slides reserve the largest height, keeping controls stationary while inactive content stays hidden from focus and accessibility navigation. |
| At 320 pixels, Resume wrapped alone beneath the other navigation links. | The header looked uneven and consumed another row. | Reduced the gaps at the narrowest breakpoint while retaining the 44-pixel navigation targets. |
| The résumé skipped from H1 to H3. | Heading-based navigation omitted a logical section level. | Sections now use H2; individual roles and projects use H3. The PDF builder reads the same corrected structure. |
| Scroll-reveal styles could hide unvisited content in browser print output. | Printing before scrolling through a long page could omit text. | Print styles explicitly reveal all animated content. |
| The 404 page put its base URL after relative stylesheets. Its fragment links resolved against that base. | Nested missing addresses could lose styling; Skip to content could navigate to the homepage. | Assets and page links use root-relative URLs. Local fragment links remain on the current missing-page address. The heading now says “Page not found.” |
| Projects metadata still said “Ten,” despite nine directory entries. | Search snippets could contradict the directory. | Removed the stale count. Project order is unchanged. |
| Mars described mosaics only as flat photographs. | The text contradicted the new Mont Mercou panoramic demonstration. | Described the interactive panorama and retained its distinction from the orbital-data 3D terrain. |
| Studio highlight copy implied HC already directed live models. | It overstated the implemented alpha compared with HC's detailed case study. | Described the working local project/conversation tools and identified live connections and execution as planned. |
| COLE used undated “current/latest” language for a retained release record. | A dated verification could be read as a perpetual claim about the newest build. | Tied the source, package, and screenshot statements to the October 17 verification. |
| The résumé omitted HTML/CSS, despite its use across the portfolio projects. | A supported part of the toolkit was missing. | Added HTML/CSS and rebuilt the matching two-page PDF. Six experience roles still have exactly three bullets each. |
| Workflow arrows used pale project colors in light mode. | Direction was harder to see against a light background. | Arrows use the theme's contrasting accent color. |

Changed shared assets have a release-specific URL query so repeat visitors fetch the updated CSS and gallery script.

## Checks

- Dependency-free site validation: all 15 pages, local links/assets/fragments, unique IDs, headings, gallery counts, public email links, and private-contact patterns.
- Added heading-balance and heading-level checks, plus root-relative 404 navigation checks.
- Gallery regression tests cover keyboard/mouse control, manual pause and sound preservation across visibility changes, lightbox cleanup, rotation, reduced motion, and lifecycle behavior. The keyboard regression failed against the old script before the fix.
- Browser checks at a 320-pixel content width found no horizontal overflow, caption overflow, or broken visible images across all 15 pages after the fixes. Each gallery retains three items.
- All nine project workflows changed stages, wrapped from stage 04 to 01 by keyboard, and maintained one active panel. Hero highlight controls changed the displayed content.
- Real-browser playback checks confirmed manual pause persists after scrolling away and back. Lightbox next/close restored focus to the visible slide, cleared its media source, and left the background clip paused.
- GNSS full-resolution image zoom, Escape dismissal, focus return, and image cleanup worked.
- The generated résumé passed its source-fingerprint and two-page checks; both pages were rendered and visually inspected. Public résumé and white-paper text scans found no phone-number patterns, local user paths, or unapproved email addresses.
- JavaScript syntax checks passed. No browser console errors were recorded during the final mobile traversal.

## Recommended next changes

1. **Make the résumé faster to scan.** Add in-page links for Experience, Education, Honors, Technical Toolkit, and Projects. Group the toolkit into languages, geospatial tools, application development, and research methods. Keep the existing project order and factual content.
2. **Reduce repeated validation prose.** NWSW, Research Architect, and the Workbench repeat explanations of hashes, human review, and what test counts do not establish. Keep one clear scope statement near each claim, then put detailed verification records behind an expandable section like HC already uses. Retain the actual boundaries of the evidence.
3. **Make implementation evidence easier to inspect.** The demos and RA white paper are useful. A reviewed code excerpt, small reproducible public example, or sanitized technical artifact would add evidence for engineering readers. Choose material explicitly cleared for public release; do not infer that private project repositories should be opened.

The main remaining weakness is reading effort. The site has substantial material, but several cases require a long read before a visitor reaches the result and its relevance. A short opening sequence of “problem, my contribution, demonstrated result” would improve those pages without inventing adoption or impact metrics.
