# TadaWords delivery constraints

Read this file only for `darrenfu/tadawords` delivery work.

## Identity and capabilities

The identifiers below are public-export placeholders. Resolve the approved values from private project configuration before signing or provisioning.

- Use the APP_ORGANIZATION Apple Developer team for production.
- Use the currently approved production App ID `PRODUCTION_BUNDLE_ID` on APP_ORGANIZATION team `APPLE_TEAM_ID`; do not switch back to the separately owned `LEGACY_BUNDLE_ID` identity.
- Preserve the iCloud container `ICLOUD_CONTAINER_ID`.
- Keep CloudKit and Push Notifications enabled for production entitlements.

## Device and data policy

- R0/R1 require no physical device. R2 may use at most one representative
  experience device after scope freeze. R3 uses only affected device classes.
- Use one approved iPhone and one approved iPad together only for cross-device
  scope or an immutable R4 release candidate.
- Never uninstall, privacy-reset, or overwrite learning records to make a test pass.
- Cross-device sync requires one iPhone plus one iPad and must cover launch-triggered sync plus profile/progress/settings/reward critical events; devices must not need to remain on the Family Sync screen.

## GitHub and release evidence

- Resolve repository instructions before editing.
- Keep issue and PR scope narrow. One PR/branch has one writer lease. Use guarded
  merge automation; do not push directly to `main`.
- Freeze scope before expensive verification. A new commit invalidates evidence
  for the prior HEAD; rerun only gates required by the declared R0-R4 tier.
- HEAD-unchanged status work reads existing evidence and never reruns gates.
- Keep these gates distinct: source tests, simulator tests, signed LocalQA build, physical-device smoke test, human acceptance, Xcode Cloud build, TestFlight availability, App Store submission.
- Preserve user work in dirty trees and never resolve unrelated conflicts destructively.

## Cloud workflow default

- Trigger fast PR checks separately from scheduled integration. Trigger the
  release workflow only for an explicitly promoted R4 candidate and allow
  manual runs.
- Run the release test pack once per frozen candidate, not a broad full matrix
  on every commit.
- Distribute successful candidates to the internal TadaWords TestFlight group.
- Reserve unique build numbers and record the exact Git commit in the handoff.
