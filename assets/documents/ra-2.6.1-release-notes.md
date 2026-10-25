# RA 2.6.1 preview, distribution revision 1

24 October 2026. This factory patch makes review of the exact project-plan PDFs an executable prerequisite for kit creation. RA 2.6.0 generated and delivered PDFs but did not enforce their prior review. That gap is closed in the supported preparation workflow.

## Changes

- Finalized plan export now saves both PDF editions, their source projection, all six configuration inputs and the actual checklist snapshot in a hash-pinned review bundle. Export alone records no approval. Early discussion previews remain available while intake is incomplete.
- The accountable human must supply a distinct response approving both exact PDFs. The new `record-pdf-review` action binds that response to the configuration, bundle and PDF hashes. Earlier configuration approval cannot be relabeled as PDF review. Missing review blocks configuration binding and kit creation.
- Configuration changes, reopened/changed intake, missing or altered PDFs, source snapshots, projection or manifest invalidate review. A changed preview needs a new actual human-response reference. No earlier review is used as a fallback. Repeating the same current response is idempotent.
- Explicit refusal or withdrawal is recorded as a new event and blocks creation even after a prior approval. A subsequent approval needs another actual response. Prior responses and approvals remain in the ledger.
- Compilation copies the reviewed PDF bytes unchanged instead of rendering replacements. A separate PDF_PLAN_REVIEW.json receipt records the later review. Original PDF labels and pre-review checklist state remain part of the reviewed snapshot; they do not reopen closed work. Current workflow records carry later progress.
- The coordinator retains the complete recorded response. Every kit receives a scoped receipt and the team PDF; only the Hub also receives the Hub PDF. PDF and receipt bytes are verified and sealed before publication. Review inputs and the located checklist are checked again immediately before publication.
- Draft and legacy compilation cannot bypass the review gate. The old standalone generator CLI is disabled; unfinished planning uses PDF exports and kits use the reviewed project compiler. This is an intentional compatibility change, not a migration of deployed kits.
- Current startup, workflow and setup instructions now describe the enforced sequence and remove conflicting advice to generate unreviewed draft kits or regenerate a final PDF after review.

## Preservation and scope

An unchanged historical configuration approval can remain intact while the new PDF review is appended. Prior releases, deployed kits, scientific approvals, closed work orders and research evidence are untouched. Changed configurations still require reconfirmation through the existing intake rules. Historical completed builds are not retroactively marked reviewed.

Factory version is 2.6.1. The operational runtime remains 2.4.0 and the scientific library remains revision 1.9; neither was changed by this patch. The 3–100-kit range, one-Hub/one-Ingestor architecture and Hub publication authority remain unchanged. The existing white paper retains its stated edition and is not relabeled as evidence for this patch.

PDF export uses the existing ReportLab dependency. Review recording and compilation add no model calls, polling or PDF rendering. Routine context remains scoped; no entire PDF or review bundle is injected into normal status checks. The complete review bundle is coordinator-only and must remain available through preparation and walkthrough.

This gate checks recorded evidence tied to exact files. It cannot authenticate a person's identity, prove that they read or understood the PDF, or prevent fabrication by someone with unrestricted code/file access. Agents must record the actual human response. No scientific approval or service permission is granted by kit preparation.

## Verification

Eleven focused review-to-build test groups passed, including one successful four-role build that copied the reviewed PDFs while rendering was disabled, and one injected PDF change during generation that blocked publication. A separate five-check refusal/renewal test exercised the actual CLI and stopped rejected normal/draft builds before the generator. All responses were synthetic fixtures, not real human approvals.

Existing rendering/layout, runtime, scientific and model-conversation suites were not rerun. Package inventory, source preservation and archive hashes were checked separately. See VERIFICATION_2_6_1.md for scope. No portfolio message was sent.
