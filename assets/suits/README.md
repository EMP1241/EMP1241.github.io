# NASA SUITS proposal visuals

These assets describe Brandon Santor's 2021–2022 student challenge proposal, not a deployed astronaut system or completed human trial.

- `proposed-system.svg`: the proposed local positioning → command hub → connected headsets architecture, with return updates for shared pins and a separate depth-sensing input. Based on the October 26, 2021 proposal and the owner’s 2026-10-23 clarification that a central hub would maintain and distribute current locations.
- `lunar-ar-tin-concept-20261023.webp`: new AI-generated illustration made with the built-in image-generation tool. It reconstructs the owner’s clarified design intent: lunar navigation in low visibility, waypoints, other astronauts, and personal/shared pins. Lunar shadow provides the low-visibility setting; the graphic does not depict an atmospheric dust storm. A terrain-following irregular triangular mesh illustrates the intended terrain-depth overlay; it is not a TIN derived from measured lunar data. Labels and distances are illustrative. This is not an application capture or evidence of a tested navigation system. The exact generation prompt is retained in `lunar-ar-concept-prompt.txt`.
- `waypoint-concept.webp`: the superseded page-12 concept-deck excerpt, retained as an archival asset. It uses EA Games’ Mass Effect: Andromeda reference imagery. It is no longer in the active gallery.
- `planned-evaluation.svg`: an archived summary of the route, task, terrain-recognition, and voice-interface checks planned in the proposal. No completed measurements are implied.

The original proposal contains personal contact details and is not published. Public visuals were checked for phone numbers, street addresses, student email addresses, and local filesystem paths. The source proposal and deck remain in the owner's project records.

The first generated version, `lunar-ar-concept-20261023.webp`, is retained as an archive. The active first gallery image uses the revised TIN overlay.

The final edit increases mesh contrast in shadow, replaces the angular route with a winding ground-following path around rocks and over low rises, and removes the embedded bottom disclaimer. The provenance and prompts are retained here; visible page captions call the scene illustrated.

## Modernized crew-positioning illustration

`crew-positioning-hub-300m-20261023.webp` is the active third gallery image, extending the earlier grid illustration with a central command hub and continuous shared-state update loop. Built-in image generation produced this schematic from the owner's requested 300 × 300 m layout: 16 spikes on a four-by-four lattice, 100 m spacing, and three astronauts using their nearby anchors. The main map uses small point locators for crew and spikes rather than oversized human or hardware renderings; the right panels are explicitly enlarged details. Locator rings and dots mark positions, not physical footprints. The plan view illustrates horizontal spacing; it does not establish vertical positioning geometry, radio visibility, or coverage across real lunar terrain.

This is a contemporary Channel Sounding extension of the design idea, distinct from the historical 2021 proposal's RSSI method. Channel Sounding uses phase-based ranging and round-trip timing; the illustrated spacing is a design assumption, not a validated hardware recommendation or measured positioning result. Official method reference, checked 2026-10-23: https://www.bluetooth.com/learn-about-bluetooth/feature-enhancements/channel-sounding/

The exact generation prompt is saved in `crew-positioning-prompt.txt`. The figure has 16 spikes, three crew identities, three local four-anchor link groups, a labeled 100 m grid, and a 300 m extent on each axis. Color is supplemented by crew labels and distinct person/spike symbols. Lunar terrain is illustrative and has no measured lunar CRS or elevation provenance.

The superseded `crew-positioning-grid-300m-20261023.webp` is retained as an archival draft. The active v2 corrects the oversized main-map people and hardware. Panel 03 now illustrates four anchors A–D contributing ranges for one wearer (Crew 01), repeated separately for each tag, instead of mixing three crew identities into one solution.

## Command hub clarification

On 2026-10-23 the designer clarified that the intended system included a hub/command center maintaining and distributing current locations. The source proposal, pages 2–3, describes processing positions on the fly, real-time distance changes, mission-control awareness, and real-time shared spatial anchors. It does not explicitly detail a server architecture, storage implementation, network protocol, refresh frequency, or measured latency. The public page distinguishes that documentary evidence from the designer's clarification and keeps the architecture in proposed tense.

The active generated illustration adds a fourth logical stage: position updates (wearer identity, coordinates, timestamp) → command hub (current crew state and shared pins) → connected headsets. New pins and changes return from headsets to the hub. These arrows describe information flow, not a verified direct radio link or demonstrated mesh topology. The historical RSSI proposal remains distinct from the modernized Channel Sounding illustration.

Exact hub-edit prompt: `crew-positioning-hub-prompt.txt`. Earlier grid-only assets remain archival. Main-map crew and spike positions remain small locators; enlarged hardware appears only in explanatory panels. There are still three gallery items.

The lunar AR/TIN scene is now gallery item 1, the Projects card image, and a decorative SUITS hero backdrop. The command-hub architecture diagram is item 2; the expanded positioning-and-hub illustration is item 3. Public captions use “illustrated,” while these source notes retain the creation method. Hero highlights, the project summary, four-stage workflow, project-directory description, and résumé project entry now explain the central hub and shared navigation design. The Channel Sounding layout remains identified as a modernized illustration rather than a historical implemented capability.
