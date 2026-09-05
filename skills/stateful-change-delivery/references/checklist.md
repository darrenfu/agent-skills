# Stateful Change Delivery Checklist

## Preflight

- [ ] Desired production outcome is one sentence and externally testable.
- [ ] Code, data, config, external policy, rollout, and human steps are mapped.
- [ ] Live records and dependencies were queried read-only.
- [ ] Stable exact identifiers were selected.
- [ ] Unrelated worktree changes are identified and preserved.

## Recovery

- [ ] Backup, snapshot, export, or restore marker exists.
- [ ] Sensitive backup permissions are restricted.
- [ ] Backup is non-empty and has a checksum or snapshot ID.
- [ ] Rollback or inverse mutation is written down.
- [ ] Recovery-artifact access, retention, and eventual cleanup are defined.
- [ ] No secret or signed recovery URL will appear in the final report.

## Implementation

- [ ] Code changes the authoritative decision point.
- [ ] Compatibility during mixed-version rollout is explicit.
- [ ] New allowed, old allowed, and denied paths have tests.
- [ ] Original failure path remains protected where appropriate.
- [ ] Mutations are idempotent or safely retryable, with dry-run and concurrency protection when supported.
- [ ] Focused and proportionate regression tests pass.
- [ ] The project's auditable change record documents code, state, config, policy, order, and rollback.

## Execution

- [ ] Dependency order is explicit and uses expand-migrate-contract when coexistence is required.
- [ ] Rollout order avoids accidental over-permission and lockout.
- [ ] External policies are synchronized with application authorization.
- [ ] Persistent mutation targets exact stable IDs.
- [ ] Canonical records and history are preserved unless deletion is required.
- [ ] Dependent sessions, caches, leases, or credentials are invalidated.
- [ ] Mutation row counts match the preflight expectation.

## Target-environment verification

- [ ] Intended artifact or commit is live.
- [ ] Every intended principal or state succeeds.
- [ ] A normal unauthorized principal still fails.
- [ ] User-facing entry point reaches the final state.
- [ ] Provider-owned or human-completed step is marked pending until performed.
- [ ] Audit/log evidence shows no new errors.
- [ ] Rollback remains possible after verification.

## Final handoff

- [ ] Relevant change-record, release, artifact, rollout, and environment identifiers are recorded.
- [ ] Changed resources are summarized without sensitive values.
- [ ] Backup readiness and retention are stated.
- [ ] Remaining user action is explicit.
- [ ] Unrelated files and state preserved are noted.
