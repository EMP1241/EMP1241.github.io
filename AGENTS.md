# Portfolio maintenance

Shared RA/NWSW facts are authoritative in data/project-facts.json. Read
docs/publication-facts.md before changing these facts or their consumers.
Edit publication/templates for surrounding prose, then render; do not patch
generated pages or the imported owner white paper. Keep observation dates,
source scope and historical measurements intact. Never add private evidence,
local paths, personal contact details or credentials to the public catalog.

Before publishing, run tools/check_site.py, tools/build_ra_white_paper.py
--check, tools/build_resume.py --check, the publication regression tests,
the JavaScript/gallery checks in README.md and git diff --check. Rebuilt PDF
artifacts require visual review. Pages deployment must depend on successful
validation; do not bypass a failed fact or artifact check.
