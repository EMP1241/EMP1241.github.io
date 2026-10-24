# RA public example: code, examples, result

The owner requested three equally wide images directly in the public technical-example section, while retaining the runnable download and instructions.

## Content

1. Existing `ra-code.svg`: the exact public `inspect_file` function.
2. New `ra-example-cases.svg`: the two actual synthetic note filenames/identities and five controlled test cases—unchanged, changed, missing, unexpected, and malformed.
3. Existing `ra-results.svg`: the five passing self-test results, typeset for readability.

All three images are 1400 × 900. Their inline cards have equal column widths, descriptive captions, and individual enlargement links. Below 800 CSS pixels they stack into one column. They remain visible together and do not rotate. The hero carousel remains separate.

## Reproduction and scope

`tools/build_integrity_walkthrough.py` extracts the public ZIP into a temporary directory, executes the normal verifier and self-test, checks that the downloaded files remain byte-identical, and verifies that the existing code/result images match the script and its output. It renders the middle image and refreshes the captured output text. The script reads no project research records. The example remains a standalone synthetic demonstration, not a release of the private RA runtime.

The first attempt was blocked by this host's restricted temporary-folder permissions. The authorized run outside that sandbox passed; this was an execution-environment restriction, not a verifier failure.

## Lightbox and validation

The existing shared lightbox now accepts static image sets as well as carousels. Static sets never enter the slideshow timer/state list or hide their inline frames. Modified link clicks retain their native behavior.

- The public ZIP source/manifest check passed.
- Running the ZIP produced the expected baseline and five PASS lines; all downloaded files remained unchanged.
- Gallery regressions passed, including static-only initialization, clicked-image identity, wrapping modal navigation, repeated open/close, no static rotation, and preservation of all visible frames.
- Static site checks passed for all 16 pages.
- Desktop browser inspection measured the three columns at approximately 382.66 pixels each, on the same row, with loaded images and no horizontal overflow.
- Browser interactions verified opening the second image, Next to the third, Escape, restored opener focus, and corrected caption spacing. No console errors were reported.
- A temporary 390-pixel iframe preview visually confirmed stacked cards at phone width. This is a responsive-layout check, not physical-device qualification.
