# Astra 6 skill maintenance

Date: 2026-09-05. Scope: R0 instruction, metadata, and local discovery maintenance. All 50 custom skill names remain available on disk across 44 complete packages. This pass changes 22 definitions and their relevant resources, rather than deleting useful capabilities.

## Basis and limits

OpenAI's current Astra guidance describes stronger sensitivity to skill and AGENTS instructions, more clarification or stopping, detailed output, and occasionally disproportionate verification. That supports auditing conflicting instructions and stating when existing authorization is enough. The changes below are our application of that guidance, not a model-wide performance result. [Official model guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra)

Codex skills use progressive disclosure: metadata affects selection before the full instructions are loaded. Clear scope and one canonical definition reduce routing ambiguity; same-name definitions are not automatically combined. [Official skill documentation](https://learn.chatgpt.com/docs/build-skills)

The evaluation used seven read-only scenarios with a separate agent, plus structural and filesystem checks. It did not run an A/B benchmark, quantify speed or quality gains, or exercise live financial, publishing, login, deployment, or device workflows. Existing host and user instructions still govern tool use and authorization.

## Changes

| Skills | Adjustment |
|---|---|
| `paper-distiller` | Match requested depth, language, and format; make a full HTML teaching package optional. Update the UI invocation prompt and rendering contract accordingly. |
| `visualize` | Route native-format requests appropriately; make menu infrastructure, fonts, animation, creative briefs, and gallery metadata conditional. Preserve the bundled menu's actual integration contract when used. |
| `video-use` | Provide a direct simple-edit path without compulsory ASR, Scribe credentials, strategy approval, or animation subagents. Keep helper schema and media-correctness checks; move optional craft examples to a reference. |
| `design-audit` | Distinguish review from authorized fixes; scope inspection and validation to the affected UI. Remove mandatory whole-app discovery and per-phase approvals; repair resource links. |
| `design-system` | Keep reusable token guidance; limit HTML slide conventions to that pipeline and make narrative, chart tooling, and alignment task-dependent. |
| `ui-typography` | Scope typography edits to relevant UI work; preserve language, exact code/data, and existing design conventions. Repair resource links. |
| `stop-slop` | Preserve meaningful qualifiers, passive voice, and the author's intent. Remove absolute grammar bans and arbitrary self-scores from the entrypoint and linked examples. |
| `negentropy-lens` | Narrow routing to the requested entropy/tacit-knowledge lens; allow stable, mixed, or unknown outcomes instead of a forced decay/growth binary. |
| `renaissance-architecture` | Narrow routing to first-principles exploration; compare established and novel solutions without fixed database, writer-count, or line-count thresholds. |
| `vanity-engineering-review` | Evaluate costs and benefits without attributing motives; recognize reliability and future options as value. Replace automatic shutdown rules with optional review criteria and explicit execution boundaries. |
| `xiaohongshu-skills`, `xhs-auth`, `xhs-explore`, `xhs-interact`, `xhs-publish`, `xhs-content-ops` | Permit available documented transports with account and state checks. Continue authorized workflows without stepwise approval. Preserve final-content authorization, verify uncertain submissions, and distinguish cancellation, draft disposal, and post deletion. |
| `cua-driver` | Allow supported CLI or MCP transport without an artificial permission gate; retain UI grounding and the no-foreground contract. Replace references to a missing screenshot document with available guidance. |
| `notebooklm-studio` | Treat required scoped setup as part of authorized initialization where host policy allows; preserve account choice, MFA, and access-grant boundaries. |
| `paze-restaurant-availability` | Remove the dependency on an unavailable named browser skill while retaining live checkout evidence and the no-order boundary. |
| `costco-vgc-wallet` | Recognize exact authorization from the current conversation and keep payment secrets out of persistent ledgers; preserve private local defaults. |
| `vercel-react-view-transitions` | Apply patterns to the requested interaction rather than requiring an app-wide animation rollout; normalize description metadata. |
| `manim-video` | Move version into supported metadata; animation implementation remains unchanged. |

Automatic-selection policy was not disabled globally. Descriptions were narrowed where they previously selected a general-purpose opinion framework for nearly every task. Scripts, templates, assets, package licenses, project AGENTS rules, and system skills were retained. Runtime implementation files were not modified.

## Local installation handling

- Prepared a private backup before any local change and verified source hashes immediately before applying updates.
- Preserved private account, address, and other local substitutions while applying public instruction changes. The public repository continues to contain configuration placeholders.
- Moved 12 duplicate `~/.agents/skills` directories into private quarantine outside skill discovery. Complete canonical packages remain under `~/.codex/skills`; the older Xiaohongshu entrypoint remains in the public legacy archive for provenance.
- Replaced only the `~/.agents/skills/cua-driver` symlink with a managed copy. The application-bundled resource files were verified unchanged. Future CuaDriver updates need a deliberate comparison because this copy no longer follows app updates automatically.
- Observed 50 installed definitions with 50 unique names after maintenance, down from 62 definitions. The original session's 47 advertised names are historical; a fresh runtime reload was not verified in this task.

## Verification

- Strict definition validation: 50/50 repository definitions and 50/50 installed definitions pass.
- All current manifest file hashes and executable flags match the tree.
- Changed-document local links resolve; `git diff --check` passes.
- Local changes match the public instruction deltas while preserving private surrounding content.
- Quarantine targets and unchanged signed-app resources match recorded hashes.
- Rollback preflight passes against the installed state; rollback was not executed because the requested result is the tuned installation.

The independent scenario pass produced the requested two-sentence abstract explanation, chose editable PPTX for a native deck request, selected direct media trimming without ASR, reused unchanged publishing authorization while verifying a timeout, avoided saving a discarded draft, retained disaster-recovery value despite low usage, and preserved uncertainty in already-clear prose. It found residual contradictions in linked resources and title rewriting; those were corrected, with targeted rereads for the original contradictions. A final local review clarified draft-disposal evidence and the remaining title-shortening shorthand. These are bounded instruction-following observations, not end-to-end service tests.

## Rollback

The private backup contains an inventory, the exact applied-file plan, duplicate directories, the original CuaDriver symlink, and `rollback.py`. Running that script without arguments performs a read-only preflight; `--apply` restores this maintenance run. It refuses to overwrite targets changed since maintenance. The private backup path is provided in the task handoff and is intentionally absent from the public repository.

For the public repository, revert the maintenance commit or install the preceding revision. Do not copy public placeholders over private local configuration. Restoring a prior public revision alone does not recreate the user's private defaults or the quarantined local discovery layout.
