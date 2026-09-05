# Setup Reference

Use this for first-time setup.

## Flow

1. Identify `<PLUGIN_ROOT>`.
2. Run doctor:

```bash
python3 <PLUGIN_ROOT>/scripts/churnfu.py doctor
```

3. If `sqlite3` is missing, use `mcp-installer-policy.md`.
4. Read `first-run-config.md`.
5. Generate default config without asking setup questions:

```bash
python3 <PLUGIN_ROOT>/scripts/churnfu.py config-wizard
```

6. Initialize database:

```bash
python3 <PLUGIN_ROOT>/scripts/churnfu.py init-db
```

7. Validate:

```bash
python3 <PLUGIN_ROOT>/scripts/churnfu.py validate
```

8. Show status:

```bash
python3 <PLUGIN_ROOT>/scripts/churnfu.py status
```

The default config lives under `<PLUGIN_ROOT>/skills/churn-fu/local/`. The default database is PointClaw at `<PLUGIN_ROOT>/../pointclaw-data/pointclaw.sqlite`; the historical Churn Fu local database remains legacy/BC-only.

## First-Version Scope

- Supported issuer: Amex only.
- CardPointers enrichment: disabled.
- State: PointClaw SQLite.
- Default database: `../pointclaw-data/pointclaw.sqlite`.
- Legacy database: skill-local SQLite under `skills/churn-fu/local/`, read only for BC or legacy benefit sync.
- Credential policy: Chrome autofill first, user handles MFA and sensitive prompts.
- Execution: user-confirmed only.
