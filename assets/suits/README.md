# NASA SUITS proposal visuals

These illustrations describe Brandon Santor’s 2021–2022 student challenge design: BLE local positioning, a central command hub, shared crew locations and pins, and terrain cues in a HoloLens 2 interface.

## Active gallery

1. `lunar-ar-tin-concept-20261023.webp`: the lunar AR view, also used for the project card. A terrain-following triangulated irregular network (TIN) outlines surface shape. Waypoint, crew, and personal/team pin markers show the navigation cues.
2. `proposed-system.svg`: the system architecture. Wearable tags and known fixed spikes supply position estimates to a command hub. The hub maintains crew locations and shared pins, distributes updates to connected headsets, and receives pin changes. Local depth sensing supplies terrain cues.
3. `crew-positioning-hub-300m-20261023.webp`: the crew-positioning illustration. Sixteen anchors form a four-by-four grid at 100 m intervals across a 300 × 300 m work area. Each wearer uses nearby anchors; the hub maintains and distributes the shared position records. RSSI provides estimated ranges for trilateration. Crew labels and colors identify separate positions and link groups.

The central command hub and shared updates are part of the original system design. The portfolio illustrations communicate that design. Their production dates describe the assets, not the invention or addition of system features.

## Illustration scope and provenance

The two raster illustrations were created with the built-in image-generation tool under the designer’s direction. The architecture diagram is editable SVG. The raster art uses an imagined lunar setting; it has no measured lunar terrain, geographic reference, or derived elevation surface. Dimensions describe the conceptual layout. Radio coverage, positioning accuracy, and update latency are not measured results. The project remains a student proposal and evaluation plan.

The October 23 editorial pass removed inaccurate chronology labels and aligned the positioning diagram with the proposal’s BLE/RSSI method. The generated source was `exec-5e4e100e-94c6-41ea-93b8-b9530d08fa12.png`; the website uses a WebP conversion with the same 1426 × 1103 dimensions. Superseded positioning drafts and their prompts are retained in a local working archive outside the published site. The production prompt for this pass is retained with that archive.

The source proposal and concept deck remain private because they contain contact information. The visible page captions use “illustrated.” Public visuals omit phone numbers, addresses, student emails, and local filesystem paths.

## Other retained assets

- `waypoint-concept.webp`: a concept-deck excerpt using EA Games’ Mass Effect: Andromeda imagery; not part of the active gallery.
- `planned-evaluation.svg`: the proposed route, task, terrain-recognition, and voice-interface checks.
- `lunar-ar-concept-20261023.webp` and `lunar-ar-concept-prompt.txt`: the earlier lunar-art version and production record. The active gallery uses the TIN version.

The page uses the standard animated project hero with its signal-pattern motif. The lunar scene remains in the gallery and project card.
