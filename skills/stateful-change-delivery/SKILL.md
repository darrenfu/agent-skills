---
name: stateful-change-delivery
description: Safely deliver software changes that span code, persistent data, runtime configuration, external policy, and a target environment. Use for stateful migrations, authorization changes, account or identity repairs, schema and data fixes, provider or infrastructure transitions, or any change where updating code alone would leave the running system inconsistent. Platform-neutral and applicable to web, mobile, backend, desktop, CLI, embedded, and infrastructure projects.
---

# Stateful Change Delivery

## Purpose

Use this skill when a software change crosses more than one state boundary. The goal is not merely to edit or merge code; it is to leave code, stored data, runtime configuration, external control planes, and behavior in the target environment in one verified state with a usable rollback path.

Do not assume a particular language, framework, operating system, database, cloud, CI system, or release platform.

## Trigger Boundary

Use this workflow when at least two of these are involved:

- application or infrastructure code;
- persistent data or schema;
- runtime secrets or configuration;
- an external policy or provider console;
- an auditable change record and rollout or deployment;
- a user-visible state transition that cannot be completed by code alone.

Ordinary stateless refactors and documentation-only edits do not need this workflow.

## Safety Contract

- Inspect before mutating. Derive the root cause from live state plus source code.
- Separate facts, inference, and intended mutations.
- Back up the smallest sufficient recovery unit before destructive work. Prefer a full snapshot when it is cheap and safe.
- Record a checksum, snapshot identifier, or point-in-time recovery marker without exposing secrets.
- Preserve canonical records and history unless deletion is explicitly required.
- Mutate exact identifiers, never broad display fields or partial matches.
- Revoke or invalidate dependent sessions, caches, leases, or credentials when their parent binding changes.
- Never weaken a global security invariant to repair one account or one record.
- Keep code compatibility during rollout when old and new components may coexist.
- Do not claim completion until behavior in the target environment has been checked from the user-facing entry point.
- Stop before an irreversible or ambiguous mutation if the target cannot be uniquely identified.

## Agentic execution contract

Apply proportionate delivery discipline before the state-specific workflow:

- One Issue/PR has one root session, one branch/worktree, and one writer lease.
  Worktree isolation alone does not authorize multiple writers.
- Routine work uses no subagents. A bounded complex investigation may use at
  most two direct, non-nested, read-only subagents; concurrent writers are
  forbidden.
- At the first context compaction, write a checkpoint of at most 2 KB containing
  target outcome, Issue/PR, worktree, branch, HEAD, state owners, changed files,
  recovery evidence, completed checks, leases, blockers, and next action. End
  the old session and resume fresh.
- If HEAD and target environment are unchanged, status work reads recorded
  evidence; it does not rerun tests, deployments, migrations, or audits.
- Default routine implementation to the cost-efficient model with medium
  reasoning. Escalate only for a bounded architecture, consistency, security,
  signing, irreversible mutation, or release decision.

Classify the highest applicable delivery tier:

| Tier | Scope | Default verification |
|---|---|---|
| R0 | docs/internal tooling without runtime effect | relevant lint and changed-path tests |
| R1 | pure logic/deterministic state | focused and affected unit/integration tests |
| R2 | presentation/ordinary integration | focused tests and representative environments |
| R3 | persistent state, permissions, security, hardware, external policy | affected environment, rollback, migration, and end-to-end checks |
| R4 | immutable rollout/release candidate | complete release suite, artifact identity, rollout, and human acceptance |

Run focused tests during implementation, the normal PR gate after scope freeze,
and the complete release suite only for R4, scheduled validation, or an explicit
final audit. A new commit invalidates evidence for its prior HEAD, but only the
gates required by the current tier are regenerated.

Serialize scarce shared resources with leases: the PR writer, heavy build/test
runner, migration executor, mutable test environment, deployment target, and
release publisher. One coordinator owns any multi-environment acceptance
sequence.

## Workflow

### 1. Define the target outcome

State the desired externally observable result in one sentence. List the acceptance checks that distinguish a fully migrated target environment from a code-only change.

### 2. Map every state owner

Trace the request across:

```text
user entry point
  -> application logic
  -> persistent records
  -> runtime configuration or secrets
  -> external policy or provider
  -> built, installed, or deployed artifact
```

Mark which layer owns each decision. Do not conflate membership, identity binding, authorization role, and external access policy merely because they use the same email, username, or subject.

### 3. Run read-only preflight

- Inspect repository status, change history, rollout conventions, migrations, and tests when those mechanisms exist.
- Query the exact live records involved, including dependent rows and active sessions.
- Inspect external policy and deployment state.
- Confirm that the selected identifiers are unique and stable.
- Check for mixed worktrees and preserve unrelated user files.

If live state contradicts the proposed diagnosis, revise the plan before editing.

### 4. Design the smallest safe transition

Prefer a narrow repair over a global behavior change. Classify each planned action as:

- reversible code or configuration change;
- state mutation with explicit rollback;
- user-completed transition, such as reauthentication;
- irreversible action requiring confirmation.

Maintain compatibility fields or adapters while clients or deployments may still expect the previous contract.

Prefer mutations that are idempotent or safely retryable. When supported, provide a dry-run, use transactions or locking for coupled writes, and record enough progress to resume after interruption without repeating completed destructive work.

### 5. Create recovery evidence

Before any destructive mutation:

- create a snapshot, export, backup, or point-in-time restore marker;
- restrict local backup permissions when it contains sensitive data;
- record its location, time, and checksum privately;
- verify the backup is non-empty and structurally usable;
- write the inverse operation or restore procedure;
- define who may access the recovery artifact, how long it is retained, and how it will be safely removed after verification.

Do not print tokens, signed backup URLs, session hashes, private keys, or provider secrets in the final report.

### 6. Implement and test the code path

Change the source of authorization or state transition, not only the UI. Add tests for:

- every newly allowed principal or state;
- previously allowed behavior;
- ordinary denied behavior;
- normalization and exact matching;
- compatibility response fields;
- prevention of self-removal or unsafe mutation;
- the original conflict or failure path;
- invalid, duplicated, partial, and stale identifiers.

Keep the patch narrowly scoped. Run focused tests first, then the repository's
proportionate regression suite. Freeze scope before expensive end-to-end or
release verification. When the commit and environment are unchanged, reuse the
recorded evidence instead of rerunning it.

### 7. Publish an auditable change record

Use the project's normal review mechanism: a PR, commit, release ticket, change request, runbook entry, or equivalent. When applicable, it must explain:

- the observed symptom and verified root cause;
- which state owners are involved;
- code, data, configuration, and external-policy changes;
- compatibility behavior;
- backup and rollback plan;
- automated checks;
- manual production checks still required.

Record only intended files and resources. Use the project's existing versioning and release conventions when they exist.

### 8. Execute in dependency order

Draw the dependency order first. Prefer an `expand -> migrate -> contract` transition when old and new states must coexist. Choose an order that never leaves the target environment more permissive or permanently locked out. One common sequence is:

1. deploy backward-compatible code;
2. update external policy or runtime configuration;
3. mutate exact persistent records;
4. invalidate dependent state;
5. let the user complete any provider-owned transition;
6. remove temporary compatibility only in a later release.

If the order differs, state why it is safer for this system.

### 9. Verify the target environment end to end

Check both allowed and denied paths:

- deployment points at the intended commit or artifact;
- expected principals reach the protected function;
- an ordinary principal remains denied;
- data mutation affected the expected row counts only;
- dependent sessions or caches were invalidated;
- the public entry point reaches the intended final state;
- logs and audit records show no unexpected errors.

Provider-owned callbacks or human authentication cannot be declared verified until the user actually completes them.

### 10. Hand off the state, not just the code

Report:

- relevant change-record, version, artifact, rollout, and environment identifiers;
- exact target-environment checks and results;
- rows or resources changed, without sensitive values;
- backup or rollback readiness;
- any remaining user action;
- intentionally preserved unrelated files or state.

## Identity And Access Repair Pattern

When the change involves login or admin access, keep these concepts separate:

- account record: canonical user and membership state;
- provider identity: provider plus immutable subject binding;
- application session: revocable access derived from the account;
- application authorization: role or exact principal allowlist;
- external access gate: independently enforced policy before the application.

For a deliberate provider switch, normally preserve the account record, remove only the confirmed old provider binding, revoke that account's sessions, and require fresh provider authentication. Do not enable email-only automatic linking globally to fix one conflict.

For multiple administrators, use a normalized exact allowlist or a durable role model appropriate to the project. Synchronize every independent access gate, protect all administrators from self-removal, and retain compatibility fields if existing clients expect one primary administrator.

## Stop Conditions

Stop and request direction when:

- more than one record could be the mutation target;
- the backup or restore path cannot be verified;
- the external gate cannot be inspected or updated;
- the requested change would broaden authorization beyond named principals;
- schema constraints make the intended transition lossy;
- a provider callback requires user interaction;
- the target environment differs materially from the tested artifact.

Use [the detailed checklist](references/checklist.md) before final handoff.
