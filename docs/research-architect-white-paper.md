# Research Architect for Coordinated AI Research

Technical white paper with an operational case study from the NWSW project

Brandon Santor
Creator and Principal Designer of Research Architect
October 23 2026
Revised public edition 4   Historical RA 2.1.0 case   Onboarding limitation added October 23 2026

## Executive summary

Research Architect provides an operating framework for human research teams working with AI. It converts a reviewed project design into individual role kits, preserves project state across sessions, records evidence and decisions, and supports versioned handoffs and recovery. The New World Screwworm (NWSW) deployment supplied an active setting in which these mechanisms were used and refined.

The documented results include creator-reported onboarding of eight people, verified remote exchanges, preservation of accumulated files during a live Hub upgrade, and an isolated whole-project restore. RA 2.1.0 distribution revision 2 carries reusable operational improvements into a separate development-preview package. Its October 16 release verification passed 171 offline regression tests.

Selected operational and release results

| Capability | Documented result and scope |
| --- | --- |
| Onboarding | Eight people reported onboarded by the creator on October 16; one framework configurator. |
| Exchange records | 262 unique transfer IDs in the October 16 inventory; individual receipts establish delivery. |
| Live upgrade continuity | 701 exchange files preserved and rehashed during the October 13 Hub upgrade. |
| Project recovery | 123,098 files verified in the original October 11 isolated restore exercise. |
| Release verification | 171 offline tests passed on Windows; no model calls or remote transfers in that run. |

This edition retains the deployment case and updates the distinction among generic software, project-specific operation, recipient reports and tested behavior. The evidence supports practical continuity and recovery mechanisms. Broader adoption, comparative efficiency and research-quality effects require their own evaluation. RA configures instructions and workflow around existing AI hosts; it does not train model weights.

## 1 Introduction

AI-assisted research often spans several people, model sessions and collections of files. A useful answer becomes difficult to carry forward when the next session lacks its scope, supporting evidence, decisions or unresolved work. Teams also need to identify the current artifact, distinguish review from delivery and recover work after a session or machine changes.

Existing agent literature supplies useful design context. OpenAI describes models, tools and instructions as foundational components and discusses orchestration and guardrails. AutoGen demonstrates configurable conversations combining agents, tools and human input. Anthropic describes the coordination, evaluation and reliability work behind a deployed multi-agent research system. These sources inform the architectural context; their performance results are not evidence of RA performance. [1-3]

RA addresses the operating structure surrounding a research task. The Architect helps establish questions, assignments, methods, dependencies and review requirements. A compiler produces individual role kits and coordinated folders. Local helpers preserve state and verify artifacts, while the selected AI host supplies model inference, file access and any available connectors. Human operators retain responsibility for scientific judgments and consequential decisions.

## 2 System architecture

RA combines a reviewed project design, human-operated roles and persistent records. Figure 1 shows the logical arrangement. The same framework can support different host applications, but each installation still needs its own tested startup, storage and transfer configuration.

### Project design and role kits

The Hub coordinates shared work, dispositions and authorized releases. Spokes conduct assigned workstreams with their human operators. The Ingestor organizes incoming material and technical checks. Generated kits carry the relevant identity, role, starting assignment, selected methods and continuity records. Generation does not establish that research is ready, that an operator has reviewed evidence or that a remote account has access.

### Persistent context and source retrieval

Supported startup resolves the designated current checkpoint rather than choosing a directory by timestamp. A successor snapshot preserves its base and records changed state. A routed dictionary can direct a Hub to exact original evidence and prior decisions. The generic multipart reader preserves source text and hashes, repeats governing controls and exposes missing or altered parts. Its character limits are distinct from a model provider's token window; reading parts sequentially does not guarantee cumulative model retention.

Figure 1  Research Architect components and operating flow. A reviewed human project design enters the Architect and compiler, producing Hub, Spoke and Ingestor role workspaces with checkpoints, evidence references and exchange records. Configured host connectors support authorized transfers; recovery tools support backup and restore.

### Versioned handoffs and recovery

Local helpers stage payloads, validate configured routes and retain receipts. Authorized host connectors perform remote transfer during active sessions. Preparation, delivery, reading, adoption, research acceptance and permitted downstream use remain distinct. Backup helpers verify selected project contents and captured external files, retain explicit recovery metadata and exercise restoration. Storage and transport configuration remain responsibilities of the deployment.

## 3 NWSW deployment

The NWSW project provided an operational case for RA-generated kits and a coordinating Hub. The creator reported onboarding eight people by October 16, 2026, while remaining the only person who had run or configured the Architect itself. This is evidence of participant onboarding in a creator-supported deployment, rather than eight independent framework configurations.

The Hub maintained exchanges, source routes, instructions and checkpoints while the team continued assigned work. The original case examined selected operational records from October 8 through October 16. This revision also considers later technical returns and Hub maintenance through October 22. Historical quantities below retain their observation dates; they are not estimates of the current complete project.

Generic RA, the deployed NWSW coordination system and the independent NWSW Spatial Evidence Workbench are separate systems. The Workbench's web interface, database, spatial features and application tests are not capabilities or validation results of the RA distribution. This paper reports coordination and software-engineering observations without publishing the project's research findings or contributor records.

## 4 Operational results

### File exchange and instruction continuity

The October 16 inventory recorded 98 incoming and 164 outgoing tickets with 262 unique transfer IDs. Tickets identify prepared exchanges; separate readback records support actual delivery. The October 8 repair distribution comprised 15 logical transfers and 30 remote objects. The October 13 distribution comprised 10 transfers and 20 remote files. The retained checks bound delivered objects to their intended destinations and bytes.

A complete versioned instruction was delivered through seven participant routes in October. Its register retained identity, version, supersession and observed delivery, with a subsequent report of retention and application. That report does not establish seven persistent installations. Later diagnostic returns and exported execution records strengthened evidence for participant-side setup and multipart restoration, while remaining distinct from independent observation of every device.

### Continuity during engineering changes

The authorized October 13 Hub upgrade preserved and rehashed 701 exchange files, totaling approximately 1.66 GB. Its preceding exchange store and pointer remained unchanged. The post-activation exercise combined file-hash comparison with inventory checks and verified restoration records. This is a demonstrated preservation result for that upgrade, rather than a guarantee that arbitrary concurrent writers can be merged safely.

An October 15 native Windows context-repair fixture reconstructed a 466,824-character startup section through five resume parts and eight full-context parts. The largest part contained 189,188 characters under the unchanged 200,000-character ceiling. Checks included Unicode and CRLF reconstruction, repeated controls, missing or altered parts and later checkpoint restoration. These are synthetic engineering checks, separate from participant adoption.

### Whole project backup and restoration

The October 11 capture covered 48 included Drive folders, 744 source files and 748 downloaded or exported artifacts, together with local project contents and dependencies. The original isolated restore verified 123,098 files totaling approximately 20.88 GB without using live sources. It materialized recorded dependencies and completed restored integrity and context checks.

A later authorized content amendment produced a separately documented backup inventory. It does not replace the historical restore result or authorize resurrection of excluded bytes. The deployment's two-copy rolling policy is project-specific; the reusable tools accept explicit retention configuration. Local backup and restore were evidenced, while actual offsite delivery was not established by the inspected capture records.

## 5 Engineering improvements and release verification

Field operation exposed requirements for stable state selection, reliable Windows publication, growing context and recoverable exchanges. RA 2.1.0 distribution revision 2 ports reusable mechanisms into a separate package while preserving earlier source and deployed project history.

Capabilities in the inspected RA 2.1 distribution

| Capability | Implemented mechanism |
| --- | --- |
| Current state selection | Verified designation, identity and manifest checks; invalid selectors stop affected work. |
| State publication | Separate successor snapshots, destination-local staging and expected-base checks. |
| Context continuity | Bounded retrieval and exact multipart restoration with repeated controls. |
| Exchange records | Configured local staging, version-bound receipts, idempotent repeats and guarded lock recovery. |
| Project recovery | Resumable capture, explicit retention, dependency materialization and standalone restore tools. |

The October 16 release receipt records 171 passing offline regression tests in eleven groups on Windows and Python 3.12.10, with zero failures, errors or skips. Coverage included kit generation, checkpoints, context reconstruction, local exchange, affected evidence services, extracted-package generation and rebuilding, and backup recovery. The run made no model calls or remote transfers. A read-only comparison for this edition found all 278 recorded source hashes unchanged. That integrity comparison is not a new regression run.

Instruction maintenance has a separate boundary. RA records stable IDs, complete versioned text, authority, applicability and explicit supersession. Routine Hub saves may append evidenced observations about an existing instruction, but cannot define or rewrite a rule. A new startup instruction requires reviewed reconfiguration and verification that the selected installation actually loads it. Delivered packages and acknowledgments alone do not establish fresh-session behavior.

The deployed Hub continued to evolve after the package freeze. An October 21 local update changed context rendering while retaining original source bytes, hashes and controls; its contributor rollout remained held. Later lightweight message-handling rules were also local operational changes. Neither change is included here as a shipped generic RA 2.1 feature or a team-wide upgrade.

## 6 Discussion and next phase

RA has supported continuing work across people, sessions and files. Role kits supplied assignments and governing context, checkpoints retained decisions and unresolved work, and verified exchanges made distribution traceable. The isolated restore established a recovery path. Operational defects supplied reproducible cases for the reusable package.

### Scope and assurance

Evidence includes creator statements, execution receipts, synthetic software checks and recipient reports. Later diagnostics and inspected exports strengthen specific execution histories, while participant adoption remains unevenly evidenced. Reports of successful save, reload or refresh support their observed scope; they do not establish that stale state or lost context has been eliminated.

File consistency does not authenticate authors or certify scientific validity. Human decisions remain distinct from technical checks, and local accounts and host configuration remain trust boundaries. Folder visibility alone does not establish research-use permission. Locks and selection checks do not form one transaction across uploads, designation and unrelated writers; cutover needs an idle window and reconciliation.

### Late-stage onboarding of participants and agents

Late-stage onboarding places separate demands on a new participant and their newly generated agent. The person must learn the project, while the agent must reconstruct the relevant decisions, terminology, evidence, dependencies and unresolved work. An experienced participant introducing a fresh agent still faces the agent's context gap. A role kit can contain supplied project context, but generating it does not automatically transfer the established team's accumulated working understanding.

This is a limitation of context transfer and assimilation in the AI technology on which RA depends. Shared Library access makes retained information available; it does not by itself establish that a new agent has selected, read, reconciled and understood the material needed for its assignment. While onboarding proceeds, the project continues producing and revising context. If relevant changes accumulate faster than the person and agent can assimilate them, a persistent catch-up backlog can develop. Loading more records is not equivalent to establishing current, usable understanding.

The lead and existing team must then supply explanations, identify authoritative records, resolve misunderstandings and verify the new pair's work. Existing agents may also spend context and inference resources assisting the newcomer. This diverts attention from established workstreams, can slow the team and can make late expansion impractical within the available time and cost budget. Adding a kit should therefore not be assumed to increase useful capacity. The severity depends on the role, project pace and completeness of retained reasoning; this is a technology and workflow limitation, not a measured claim that every late entrant can never become ready. Checkpoint restoration of an established workstream remains distinct from onboarding a new participant and agent.

### Context and performance evaluation

Bounded retrieval and durable checkpoints provide mechanisms for limiting working context. Their net benefit must be measured over complete tasks, including initialization, tool results, checkpoint creation, restoration, retries and failures. Exploratory runtime diagnostics showed reducible prompt overhead, but an incomplete lean-context recovery pilot did not establish completed-task savings. This paper makes no comparative productivity, token-cost or research-quality claim.

### Broader adoption

The next milestone is another project lead configuring a new team with documented support requirements. Existing-project adoption needs preserved state, a separate candidate, compatibility checks and deliberate cutover. Recipient tests must identify loaded startup guidance, selected checkpoint, complete restoration and behavior in fresh and resumed sessions. General automatic upgrades have not been established.

RA 2.1 remains a development preview. Broader platform validation, coordinated cutover, history management and held-out adoption and review evaluation remain planned. Proposed library extensions must preserve exact source versions, audiences and approved uses; design alone does not establish deployment.

## 7 Conclusion

Research Architect has supported a creator-configured team with verified exchanges, preserved history and whole-project recovery. Field experience informed tested improvements in RA 2.1. Later returns strengthened selected continuity evidence while adoption remained unevenly evidenced. The framework provides a reusable, human-supervised operating structure with traceable engineering results. Its next phase is repeatable deployment by additional project leads.

## References

[1] OpenAI. [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf). Technical guide. Accessed October 22 2026.

[2] Qingyun Wu and colleagues. [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversations](https://www.microsoft.com/en-us/research/wp-content/uploads/2023/08/LLM_agent.pdf). COLM 2024 research paper. Accessed October 22 2026.

[3] Anthropic. [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system). Engineering report June 13 2025. Accessed October 22 2026.

### Evidence availability

The operational case draws on retained private deployment records and dated software-validation receipts. This public edition reports aggregate engineering observations and does not include participant records or research findings. Detailed source locators, hashes, evidence classifications and revision decisions are retained separately for editorial review. The published references above provide scholarly and engineering context; they do not independently validate the RA case.

### Reading the engineering evidence

The numerical results belong to their stated dates and work units. Transfer identities count recorded exchanges rather than completed research tasks. The isolated restore is one recovery exercise, and the large context fixture is one synthetic engineering case. The release regression covers the named software scope. These observations should not be pooled into an adoption rate or treated as independent demonstrations of research quality.

Further evaluation should freeze the task, authorized evidence, runtime configuration, stopping rules and grading criteria before execution. Full-context, bounded-retrieval and checkpoint strategies should face the same task and evidence. Accounting should include failed attempts and restoration work, preserve missing counters as unknown, and assess citations, uncertainty and unauthorized actions alongside completion. This is an evaluation plan; it is not an additional result of this paper.

Prepared with AI-assisted source review and drafting. The author configured the deployment and supplied the dated onboarding report. File verification, AI review, recipient reporting and independent human evaluation are distinguished throughout.
