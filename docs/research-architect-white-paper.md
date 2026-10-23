# Research Architect

## Continuity, coordination, and review for AI-assisted research

Brandon Santor | Creator and principal designer | PhalAInx independent software studio

October 23, 2026 | Public edition 4 | RA 2.3.0 development preview, distribution revision 2

### Executive summary

Research Architect (RA) builds a shared operating structure for human teams that use individual AI assistants. A reviewed project design becomes role-specific kits, source references, work assignments, review requirements, and persistent project records. The framework helps a team resume work, exchange evidence, preserve decisions, and recover after an interrupted operation.

RA has been used in the New World Screwworm (NWSW) research project. Its coordinating Hub and shared Library are operational systems with retained execution and verification records. The reusable RA 2.3 revision-2 distribution has also been packaged, checked, and delivered. These are separate artifacts: a generic release does not automatically replace an existing project's customized installation.

### What the current framework provides

| Research problem | Implemented response |
| --- | --- |
| A new session loses the basis for a decision | Restore the selected checkpoint, governing instructions, source versions, and unresolved work. |
| Team members produce disconnected outputs | Generate coordinated Hub, Spoke, and Ingestor kits with explicit responsibilities and handoff contracts. |
| A save, transfer, or update stops midway | Retain operation state and inspect the recorded outcome before retrying. |
| Shared evidence changes over time | Preserve exact versions, dependency references, corrections, review status, and permitted uses. |

### What the evidence shows

The NWSW case includes verified exchanges, file preservation through a Hub upgrade, and an isolated whole-project restore. The 2.3 release adds scoped diagnostics, selective context reconstruction, persistent owner decisions, guarded upgrades, and a shared Library client. Checks on kits generated from the delivered archive passed for all three roles.

A repeated-context fixture reduced emitted prompt text from 773,391 to 119,362 characters while reconstructing the selected sources exactly. This is a measured reduction in repeated text for that fixture, not a measured token bill or an increase in research accuracy.

<!-- page -->
## 1. Architecture and responsibilities

The Architect establishes the research question, scope, methods, dependencies, outputs, and human review responsibilities. A compiler turns that reviewed design into individual kits. Each kit carries its role, starting assignment, selected research guidance, and continuity tools. The AI host provides inference and available file or connector access; authorized human operators determine what may be executed and released.

<!-- architecture -->

Figure 1. The reusable framework generates coordinated role kits. The shared Library stores accepted, versioned material for later retrieval. Human review accompanies the workflow; technical checks alone do not authorize scientific use.

| Component | Responsibility |
| --- | --- |
| Hub | Coordinate work, retain decisions and dependencies, and manage authorized handoffs and final acceptance. |
| Spoke / participant pod | Carry out an assigned workstream with its human operator and prepare evidence for review. |
| Ingestor | Check incoming files, reproduce applicable processing, preserve provenance, and return findings for acceptance. |
| Shared Library | Register and publish reviewed versions within their allowed audience and use; expose discovery metadata and correction links. |

In NWSW, a participant reviews a submission before it reaches the Hub. The Hub reviews scope and authorizes verification; the Ingestor checks or reproduces the applicable work; the Hub then makes the final acceptance decision. Accepted material enters the Library for shared use. Held material can remain discoverable through permitted metadata without releasing its underlying contents.

The Library client shipped with RA is a consumer and submission interface. The maintaining Hub and authorized host retain publication and access authority. The separately developed Spatial Evidence Workbench supplies GIS and evidence-inspection tools; its code and application tests are not part of the RA distribution.

<!-- page -->
## 2. Preserving context without losing its meaning

### Resolve the current state

Startup resolves an explicit current designation and checks the expected identity and manifest. It does not choose a folder merely because its timestamp is newest. A successor checkpoint retains its starting version and records changed state. Missing or changed governing material stops the affected operation instead of quietly substituting a convenient copy.

### Reconstruct selected evidence

RA 2.3's selective reader identifies exact repeated material and can emit backward references instead of duplicate text. Reconstruction restores the complete selected sources and verifies their fingerprints. When references would cost more than literal text, the reader keeps the complete literal rendering. The optimization changes delivery of context, not the underlying evidence.

Same-conversation reuse requires an explicit assertion that the matching context was actually read and remains available. New, changed, lost, or uncertain context is reconstructed. A successful disk check does not establish that a model has read or retained the material.

### Keep large results complete

Output budgets apply to serialized UTF-8 bytes, including the response envelope. A short response points to a retained full result when it cannot contain every finding. Continuation pages are bound to the expected result hash, so a later page cannot silently come from a different result. Paging preserves source references and review qualifications. An input limit produces an explicit incomplete or blocked result, rather than a false claim that no evidence exists.

### Carry decisions and corrections forward

Owner decisions use append-only close and reopen events tied to the original authority evidence. A stale imported status cannot reopen completed work. An authorized reopening records a new event and preserves the previous closure. The current-decision index makes these controls available during restoration without repeatedly emitting every historical event.

Library discovery follows pinned metadata to exact artifact versions, dependencies, corrections, and permitted uses. A file can be associated with several topics while keeping one canonical identity. A corrected version remains linked to the version it supersedes, allowing later work to inspect both the change and its basis.

### How the team becomes better informed

Reviewed findings, errors, and corrections accumulate in shared records. A subsequent assistant can retrieve a more complete account of what is supported, disputed, or ruled out. This is improvement in available project context. It depends on retrieving and applying the relevant record; it is not automatic learning in model weights or proof that every participant adopted a correction.

<!-- page -->
## 3. Context and corrections in practice

### Restore the evidence needed for this task

<!-- context-flow -->

Figure 2. Context follows an explicit checkpoint and selected evidence. Exact references reduce duplication in the delivered representation; reconstruction recovers the selected source text. The reuse branch requires matching context that was actually read and remains in the same conversation. Neither branch proves that the assistant interpreted the evidence correctly.

For example, a participant returning to an unfinished analysis needs the current task, governing instructions, accepted inputs, decisions, and unresolved questions. Reopening every unrelated project file adds overhead. Restoring only a convenient summary can omit a qualification. The reader instead preserves the selected sources and their identities, with lossless continuation when they exceed a display budget.

### A correction changes what later work should use

<!-- library-flow -->

Figure 3. Illustrative version history, not a real research record. A reviewed correction creates a linked successor. Earlier evidence remains inspectable, and several topics can point to the same canonical artifact version. Discovery exposes the recorded review and use conditions before a participant retrieves the material.

If a shared table used the wrong unit label, its correction should identify the affected version, its replacement, and dependent outputs needing review. A second file with a similar name leaves users guessing. The Library client retains those version and dependency links. Human acceptance and downstream adoption remain recorded separately.

<!-- page -->
## 4. Diagnostics, recovery, and safe change

### A shared Doctor and local interface

The Doctor runs scoped, deterministic checks through the existing validators. Its local browser interface is normally launched by an agent; direct recovery access binds an explicit installation when normal startup is unavailable. Reports retain exact targets and findings. Repeated refreshes reuse the recorded result rather than repeat an operation. Routine diagnostics require no model calls.

The interface diagnoses problems and directs recovery. It does not execute arbitrary scripts or automatically perform every repair. Revision 2 fixes failed-run replay, request-only unknown outcomes, UTF-8 output budgeting, and stale release-title metadata.

### An interruption is a state to resolve

<!-- recovery-flow -->

Figure 4. Normal completion and recovery after an uncertain result. A lost reply does not prove that an operation failed. Reconciliation checks the recorded request and actual postconditions before a guarded next step. "Finalization pending" retains established work while required closing records or selection changes are completed.

These distinctions prevent a missing response from becoming an automatic repeat of a consequential action. Reconciliation inspects pinned postconditions. A prior completion receipt describes that operation; it does not certify that a remote service is healthy now.

### Upgrade without discarding history

The updater prepares a separate candidate against an exact starting version, protects state and history, and uses a controlled active-runtime selection. Rollback retains prior work. The supplied schema migration was exercised on retained RA 2.1 Hub and Spoke fixtures moving to 2.3, with installed-runtime checks afterward. This establishes that tested path, not a universal migration for customized installations.

Existing owner decisions must be supplied and reconciled during an upgrade. An empty replacement decision register cannot stand in for a project's history. Existing NWSW installations retain their own reviewed activation procedures and scientific controls.

### Preserve recovery and messaging tools

Backup and restore capabilities predate 2.3 and remain available. Message-only requests use scoped checks without restoring the full research project. Partial listings retain their incomplete status; they cannot yield a misleading "no new messages." Authorized host tools remain responsible for remote reads and sends.

<!-- page -->
## 5. Operational case: the NWSW research team

RA-generated kits support a coordinating Hub and participant workstreams in the New World Screwworm project. Brandon Santor configured the system and reported onboarding eight people by October 16, 2026. This is one creator-supported deployment, with eight participants, rather than eight independent installations of the Architect by separate project leads.

The Hub and finalized Library have been activated and exercised through their own operational controls. On October 23, two additional improvements were installed: complete lookup paging and complete retained message-journal summaries. The Hub keeps its project-specific configuration; this targeted deployment did not replace it with the generic 2.3 runtime or change contributor kits.

### Recorded engineering outcomes

| Dated exercise | What happened | What it demonstrates |
| --- | --- | --- |
| October 16 exchange inventory | 262 unique transfer IDs: 98 incoming and 164 outgoing. | Traceable exchange records. Separate dispatch and readback receipts establish actual delivery. |
| October 13 Hub upgrade | 701 exchange files, about 1.66 GB, preserved and rehashed. | The recorded upgrade retained accumulated exchange content. |
| October 15 context-repair fixture | A 466,824-character startup section reconstructed through bounded parts. | Exact reconstruction of that large fixture, including Unicode and CRLF checks. |
| October 11 isolated restore | 123,098 files, about 20.88 GB, restored and verified without live project sources. | A tested recovery path for that captured project and its recorded dependencies. |

The exchange inventory counts handoffs, not completed research tasks. The restoration count describes one captured project, not a research sample. These dated observations are retained as operational evidence; they are not estimates of the current total volume of work.

### From field problems to reusable mechanisms

Operational work exposed concrete requirements: stable checkpoint selection, exact instruction delivery, Windows-safe publication, growing context, and recovery after interrupted exchanges. Recorded defects and their corrections informed the reusable framework. Recipient diagnostic reports and exported execution records support the specific scenarios they document, including participant-side setup and restoration.

The October 23 selective update extends that operating history with complete evidence delivery, described on the next page. The study's scientific findings and restricted contributor records remain outside this public engineering case.

<!-- page -->
## 6. Deployed improvement: complete results, one scan

The October 23 Hub update addresses a practical failure mode: a useful lookup can produce more evidence than one tool response can display. Cutting the result short hides findings; rerunning the same lookup to get more text wastes work and can return a changed result. The installed adapter retains one complete result and delivers its contents through hash-bound pages.

<!-- paging-flow -->

Figure 5. The retained result is the common source for every continuation page. Source pins, review conditions, and result identity travel with the lookup. Page limits regulate transport; they do not reduce the set of findings. Retrieving a continuation does not repeat the original lookup or message scan.

### What was demonstrated

| Check | Result and practical meaning |
| --- | --- |
| Large Unicode lookup | All 297,516 characters reconstructed across 188 pages. The old fixed 99-page ceiling no longer truncates this case. |
| Actual Library lookup | All 11 sources retained in a 172,948-character result, with their current review qualifications. |
| Complete journal summary | A 14,419-character fixture summary was delivered in full rather than only its earlier 640-character excerpt; continuation caused zero rescans. |
| Installed preservation | The native Doctor found 1,652 files consistent, all 24 protected hashes matched, and the active Hub designation stayed unchanged. |

Twelve targeted checks, an independent agent review of the exact files, and installed checks passed. Complete error reports are also retained when their displayed response must be short. The existing message writer, approval rules, closed work orders, and Library publication authority remain in place.

This is a tested deployment to the customized Hub, not a new generic RA ZIP revision. No Library republication or contributor rollout was needed. Additional deduplication saved zero characters on the already compacted Hub context, so the working reader was preserved. That result does not invalidate RA's separate repeated-context fixture; the two measurements use different starting material and answer different questions.

<!-- page -->
## 7. RA 2.3 release verification and measured scope

### Check the artifact that users receive

The delivered development preview is RA 2.3.0, distribution revision 2: 289 archive members and 626,241 bytes. Hub, Spoke, and Ingestor kits generated from that archive passed installed-runtime integrity, runtime delivery hashes, startup routing, selective reconstruction, and explicit reuse checks. This tests the distributed artifact, rather than assuming a successful source checkout proves package completeness.

### Reduce repeated context in a defined fixture

<!-- benchmark -->

Figure 6. Emitted prompt characters in the retained repeated-context fixture. The selective representation reduced emitted text by 84.6% with exact reconstruction. Explicit warm reuse emitted 277 characters. The measurement does not include a complete research task or provider token/billing accounting.

### Evidence groups remain separate

| Evidence | Established result |
| --- | --- |
| Revision-2 follow-up | Five focused checks passed for failure replay, request-only unknown outcomes, UTF-8 limits, repeated checks, and timeout handling. |
| Targeted integration | Checks cover the Doctor, operation journal, updater, messages, selective reader, owner decisions, Library client, and generated-kit recovery. |
| Library interoperability | A synthetic reviewed submission, identical replay, and correction passed through the finalized backend and were discoverable by a second kit. |
| Retained baseline | 171 earlier tests in 11 groups, with 278 source pins verified. Unchanged behavior reused its evidence; the 171 tests were not all rerun for revision 2. |

Failed attempts and corrected reruns remain in the engineering record. Examples include candidate-manifest sequencing, reference overhead on small contexts, and a Library fixture connection left open at cleanup. The published result refers to the corrected, checked scope; it does not erase earlier failures.

Deterministic runtime checks use local synthetic data and require no model calls or production remote transfers. Fresh Python processes test software restoration; fresh model conversations are a separate evaluation. The broader live-agent research and coordination matrix remains open.

<!-- page -->
## 8. Research practice and the literature behind it

RA retains 30 universal research rules and 16 method modules. Version 2.3 adds seven research-practice instructions that make task scope, shared evidence, alternatives, coordination, cost controls, and closeout explicit. These are workflow rules implemented in the framework, not claims that prompting alone guarantees scientific reliability.

### Seven expectations carried into the role kits

1. **State the task.** Identify the question, unit of analysis, evidence, method, assumptions, deliverable, and stopping condition.
2. **Retrieve shared evidence.** Inspect relevant versions and corrections before repeating work or making a consequential inference.
3. **Preserve evidential meaning.** Keep dates, units, conditions, and distinctions among observations, execution reports, and independent replication.
4. **Test competing interpretations.** Use a discriminating check when an alternative explanation could change the conclusion.
5. **Coordinate selectively.** Give separable work clear ownership and acceptance criteria; avoid handoffs that add overhead without useful separation.
6. **Bound cost while retaining evidence.** Use scoped checks, exact reuse, and complete continuation; record unresolved work when a budget is exhausted.
7. **Close with inspectable outcomes.** Record what ran, its source/version, result, limits, decision owner, and next dependency.

### Selected design connections

Studies of agent-system scaling examine how task structure and coordination overhead affect outcomes. RA uses that context to require task-specific delegation rather than assume that adding agents always helps. Failure analyses distinguish system design, inter-agent alignment, and verification problems; RA's task contracts and closeout requirements address those classes of risk. These are design connections, not measured RA effect sizes. [4, 5]

LongMemEval separates indexing, retrieval, and reading, and tests temporal updates and abstention. That distinction informs RA's separation of a file being available, a source being retrieved, and context actually being read. STORM studies perspective-driven questioning and grounded synthesis for article preparation; RA applies related ideas to source-linked questions and alternative interpretations while retaining human scientific review. [6, 7]

Earlier guidance on agent components, configurable conversations, and deployed research systems provides additional architectural context. [1-3] The references are selected foundations, not an exhaustive inventory of the creator's research. Performance reported by these authors is not transferred to RA.

<!-- page -->
## 9. Deployment boundaries and the next evaluation

### Configure the project, not just the files

New kits need real owner, project, storage, Library, and messaging bindings. Configuration does not grant remote access or create scientific approval. A cached Library view must be identified as offline or stale. Discovery of permitted metadata does not authorize retrieval of a restricted payload.

Existing projects need a reviewed change against their actual state. The NWSW Hub is a customized operational system. Its local improvements must preserve closures, approvals, scientific restrictions, and existing publication authority. The generic 2.1-to-2.3 migration cannot be assumed to apply directly to every earlier customized Hub.

### Keep authority and evidence distinct

Fingerprints establish byte agreement with an expected manifest. Owner-decision records retain evidence of an instruction, not cryptographic proof of a person's identity. File access, review, delivery, acknowledgement, and permitted downstream use are different states. System design can make these distinctions visible; human operators still decide whether evidence supports a conclusion.

Operation journals and selection checks do not create a single transaction across every external upload and unrelated writer. Recovery therefore checks actual outcomes before retrying. A controlled cutover must account for current writers and the installation's existing procedures.

### Evaluate complete work, not only convenient counters

| Next question | Evaluation needed |
| --- | --- |
| Can another lead configure and operate RA? | A new project setup with recorded support needs, startup checks, and completed handoffs. |
| Do corrections survive fresh model sessions? | Fresh and resumed sessions across selected hosts, with exact loaded guidance and evidence-use checks. |
| Does selective context reduce total cost? | Matched end-to-end tasks including initialization, tool outputs, checkpoint creation, restoration, retries, failures, and provider accounting. |
| Does coordination improve research quality? | Frozen tasks and authorized evidence, explicit grading criteria, citation and uncertainty review, and comparison with simpler workflows. |

The delivered preview and operational case establish useful engineering behavior: generated roles, traceable exchanges, preserved state, recoverable operations, and exact reconstruction. Those results justify further evaluation. They do not settle comparative productivity, cross-model reliability, or the quality of scientific conclusions.

### Edition note

This newly written paper replaces the October 22 public document. It covers RA 2.3 revision 2, the deployed Library and owner-decision mechanisms, and the October 23 Hub improvements, with new architecture and measurement figures. Historical operational results retain their original dates and scope.

<!-- page -->
## References and evidence

### Selected primary literature and engineering sources

[1] OpenAI. *A practical guide to building agents*. Technical guide. [Read guide](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf).

[2] Wu, Q., and colleagues. *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversations*. COLM 2024. [Read paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2023/08/LLM_agent.pdf).

[3] Anthropic. *How we built our multi-agent research system*. Engineering report, June 13, 2025. [Read report](https://www.anthropic.com/engineering/multi-agent-research-system).

[4] *Towards a Science of Scaling Agent Systems*. Version 3, arXiv:2512.08296. [Read version 3](https://arxiv.org/html/2512.08296v3).

[5] *Why Do Multi-Agent LLM Systems Fail?* Version 3, arXiv:2503.13657. [Read version 3](https://arxiv.org/html/2503.13657v3).

[6] Wu, D., and colleagues. *LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory*. ICLR 2025. [Read paper](https://proceedings.iclr.cc/paper_files/paper/2025/file/d813d324dbf0598bbdc9c8e79740ed01-Paper-Conference.pdf).

[7] Shao, Y., and colleagues. *Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models*. NAACL 2024, pp. 6252-6278. [Read paper and metadata](https://aclanthology.org/2024.naacl-long.347/).

### Release identity

Research_Architect_v2_3_0_preview_r2.zip | 626,241 bytes | 289 archive members

SHA-256: 4e43cb7fd14afe5a812a1b185948c081a9f1a28afbf7a0a60a99102a8f89d780

### Engineering evidence used for this edition

The RA release is supported by its final package and closeout receipts, revision-2 Doctor verification, all-role archive checks, phase records, implementation report, and original-source comparison. The selective-context result retains its fixture output, source hashes, and reconstruction checks. The operational case uses the prior edition's dated evidence, completed Hub and Library activation records, and the October 23 selective-port installation and post-install verification receipts.

The public [RA verification summary](https://emp1241.github.io/assets/documents/ra-2.3-preview-verification.html) distinguishes fresh checks from reused results. A [standalone synthetic file-verification example](https://github.com/EMP1241/EMP1241.github.io/tree/main/assets/examples/handoff-integrity) makes the fingerprint-checking method inspectable without publishing private application source or team records.

Detailed private locators, hashes, and editorial decisions are retained separately. They include participant and operational records that are not part of this public paper. Public references provide design context; they are not independent validation of the RA deployment. Earlier references were reviewed for edition 3; the four added research sources were checked for this edition on October 23, 2026.

Prepared with AI-assisted source review and drafting under the author's direction. Creator reports, operational execution records, software tests, and independent human evaluation retain their stated evidence classes.
