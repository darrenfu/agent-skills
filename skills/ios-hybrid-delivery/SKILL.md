---
name: ios-hybrid-delivery
description: Configure and operate a hybrid iOS delivery workflow that combines a no-timeout local macOS login keychain for direct Xcode device signing with Xcode Cloud and TestFlight for remote, phone-controlled builds and installs. Use when the user wants to stop repeated signing-key prompts, deliver iPhone or iPad builds without being at the Mac, configure Xcode Cloud or TestFlight, diagnose local-vs-cloud signing, or verify an exact iOS release candidate across local and cloud lanes.
---

# iOS Hybrid Delivery

Use two complementary lanes. Keep local Xcode signing for fast hardware debugging and exact-device acceptance. Use Xcode Cloud plus TestFlight for routine remote delivery that does not depend on the Mac login keychain.

## Start safely

1. Inspect the repository instructions, clean/dirty worktree state, bundle IDs, entitlements, team, schemes, and current commit.
2. Inspect live Apple Developer and App Store Connect state before claiming configuration or release success.
3. Never read, store, paste, or pass a Mac login password on a command line. Let the user type it into a local secure prompt when an unlock is unavoidable.
4. Never uninstall the app, reset privacy permissions, or replace persistent app data unless the user explicitly authorizes data loss.
5. Treat source tests, simulator tests, signed-device installation, physical-device acceptance, cloud build, and TestFlight distribution as separate evidence.

## Use a risk-tiered PR-to-RC pipeline

Worktree isolation is not writer isolation. One iOS PR/branch has one writer
session and one writer lease. Two independent Issues may be developed in
parallel, but one Mac has only one heavy Xcode/UI lane and every physical device,
signing/archive lane, and TestFlight upload lane is exclusive.

Declare the highest applicable tier:

| Tier | Scope | Default device rule |
|---|---|---|
| R0 | docs/internal automation with no app-package effect | no simulator or device |
| R1 | pure domain logic/state machine | focused/unit tests; no physical device |
| R2 | ordinary SwiftUI/layout/motion/audio presentation | relevant iPhone/iPad simulator coverage; at most one representative experience device after scope freeze |
| R3 | Camera, Speech, Photos, Pencil, permissions, signing-adjacent behavior, persistence | only affected physical device classes; two only for cross-device behavior |
| R4 | immutable RC, Family Sync, TestFlight/App Store release | full applicable suite plus one approved iPhone and one approved iPad |

Run focused tests while behavior is changing. Freeze scope before PR-wide,
simulator, signed-artifact, or physical-device validation. A new commit
invalidates evidence for the prior HEAD; rerun only gates required by the
current tier. Full archive and two-device evidence belong to a frozen R4 HEAD.

Ordinary R0-R3 PRs do not increment marketing/build versions solely because a
PR exists. Reserve version/build and create one archive/export when promoting
R4. When signing identity and provisioning cover the approved devices, install
that same artifact sequentially; otherwise distribute the same Internal
TestFlight build.

If HEAD and environment are unchanged, read the evidence manifest instead of
rerunning tests, builds, signing, installs, or audits. At the first context
compaction, write a <=2 KB checkpoint and continue in a fresh root session.
Routine work uses no subagents; complex review may use at most two direct,
non-nested, read-only subagents.

## Lane 1: local direct-device signing

Run `scripts/configure_no_timeout_keychain.sh` to inspect or configure the login keychain. The script must never accept a password argument.

- If the keychain is already unlocked, configure no timeout immediately.
- If locked, pause at the secure `security unlock-keychain` prompt for the user to enter the Mac password once, then configure no timeout.
- Verify with `security show-keychain-info`. Accept only explicit `no-timeout` output.
- Verify usable signing identities with `security find-identity -v -p codesigning`.
- Explain that no-timeout reduces local security: the keychain remains unlocked until logout, reboot, or manual lock. Do not represent it as permanent across reboots.
- For exact-HEAD acceptance, record the commit before build and re-check it after tests. Any commit change invalidates prior evidence.

Use local signing for camera, microphone, speech recognition, CloudKit behavior,
push notifications, and other hardware/account-specific checks. Use only the
affected device class for R3. Use the approved iPhone and iPad together only
when cross-device behavior or R4 acceptance is in scope.

## Lane 2: Xcode Cloud and TestFlight

Verify these prerequisites before onboarding:

- Active Apple Developer Program membership and the intended App Store Connect team.
- Explicit App ID, matching app record, bundle identifier, capabilities, and entitlements.
- Cloud-managed signing is available for the workflow.
- A shared scheme builds and tests non-interactively.
- Unique monotonically increasing build numbers.

Create a conservative workflow:

1. Trigger fast checks for PRs, broader integration on schedule/merge, and the
   release workflow only for a frozen R4 candidate; avoid full matrices on every
   commit.
2. Build, run the release test suite once, archive one artifact, and distribute
   that candidate to an internal TestFlight group.
3. Prefer cloud-managed certificates and provisioning profiles.
4. Cancel superseded builds and track monthly compute usage.
5. Confirm the build appears in App Store Connect and becomes installable in TestFlight. Do not call upload success a TestFlight release.

Use the remote path:

`phone-controlled GitHub/Codex work -> reviewed PR -> guarded merge -> Xcode Cloud -> App Store Connect -> TestFlight -> iPhone/iPad install`

TestFlight removes the daily dependency on the Mac keychain, but builds expire after 90 days and do not provide an attached debugger. Retain the local lane for diagnosis and physical-device evidence.

## Handle blockers

- If signing reports `errSecInternalComponent`, re-check keychain unlocked state, key partition access, signing identities, team, and provisioning before changing code.
- If Xcode Cloud cannot see a repository or team, inspect App Store Connect role, source-control authorization, agreements, and app-record ownership.
- If the bundle ID belongs to another team, do not silently change it. Report ownership evidence and propose a nearby explicit ID.
- If CloudKit or push capabilities differ between local and production, treat production configuration as a release blocker.
- If user interaction is required for Apple authentication, agreements, or a secure password prompt, prepare everything else first and request only that narrow action.

## Verify and report

Report each lane independently:

- Local: keychain policy, signing identity, exact commit, build result, installed device, and physical acceptance.
- Cloud: workflow name, trigger, commit/build number, test result, archive/distribution state, and TestFlight availability.
- Remaining blocker: exact UI/action the user must complete, if any.

For TadaWords, read `references/tadawords.md` before changing signing, CloudKit, device-test scope, or GitHub merge behavior.
