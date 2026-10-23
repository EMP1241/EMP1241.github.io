# NASA SUITS proposal visuals

These assets describe Brandon Santor's 2021–2022 student challenge proposal, not a deployed astronaut system or completed human trial.

- `proposed-system.svg`: a new diagram summarizing the proposed local positioning, depth sensing, HoloLens 2 interface, and human evaluation documented in the 15-page team proposal dated October 26, 2021.
- `lunar-ar-tin-concept-20261023.webp`: new AI-generated illustration made with the built-in image-generation tool. It reconstructs the owner’s clarified design intent: lunar navigation in low visibility, waypoints, other astronauts, and personal/shared pins. Lunar shadow provides the low-visibility setting; the graphic does not depict an atmospheric dust storm. A terrain-following irregular triangular mesh illustrates the intended terrain-depth overlay; it is not a TIN derived from measured lunar data. Labels and distances are illustrative. This is not an application capture or evidence of a tested navigation system. The exact generation prompt is retained in `lunar-ar-concept-prompt.txt`.
- `waypoint-concept.webp`: the superseded page-12 concept-deck excerpt, retained as an archival asset. It uses EA Games’ Mass Effect: Andromeda reference imagery. It is no longer in the active gallery.
- `planned-evaluation.svg`: an archived summary of the route, task, terrain-recognition, and voice-interface checks planned in the proposal. No completed measurements are implied.

The original proposal contains personal contact details and is not published. Public visuals were checked for phone numbers, street addresses, student email addresses, and local filesystem paths. The source proposal and deck remain in the owner's project records.

The first generated version, `lunar-ar-concept-20261023.webp`, is retained as an archive. The active second gallery image uses the revised TIN overlay.

The final edit increases mesh contrast in shadow, replaces the angular route with a winding ground-following path around rocks and over low rises, and removes the embedded bottom disclaimer. The page caption retains the generated-image provenance.

## Modernized crew-positioning illustration

`crew-positioning-grid-300m-20261023.webp` replaces the planned-evaluation figure in gallery slot 3. Built-in image generation produced this schematic from the owner's requested 300 × 300 m layout: 16 spikes on a four-by-four lattice, 100 m spacing, and three astronauts using their nearby anchors. People and spikes are enlarged symbols for legibility, not scale models. The plan view illustrates horizontal spacing; it does not establish vertical positioning geometry, radio visibility, or coverage across real lunar terrain.

This is a contemporary Channel Sounding extension of the design idea, distinct from the historical 2021 proposal's RSSI method. Channel Sounding uses phase-based ranging and round-trip timing; the illustrated spacing is a design assumption, not a validated hardware recommendation or measured positioning result. Official method reference, checked 2026-10-23: https://www.bluetooth.com/learn-about-bluetooth/feature-enhancements/channel-sounding/

The exact generation prompt is saved in `crew-positioning-prompt.txt`. The figure has 16 spikes, three crew identities, three local four-anchor link groups, a labeled 100 m grid, and a 300 m extent on each axis. Color is supplemented by crew labels and distinct person/spike symbols. Lunar terrain is illustrative and has no measured lunar CRS or elevation provenance.
