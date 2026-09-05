# MCP Installer Policy

Use this when a required local dependency, such as `sqlite3`, is missing.

## Policy

1. Do not silently install system software.
2. Prefer a trusted third-party installer or package-manager MCP when available.
3. Search available tools for installer/package-manager capability.
4. If a suitable MCP exists, explain the exact dependency and ask the user for approval before invoking it.
5. If no suitable MCP exists, ask the user whether they want manual install instructions.
6. Record the blocker in SQLite after the database exists, or in the session blocker list before that.

## SQLite Missing Message

Use this wording:

```text
sqlite3 is required to initialize Churn Fu local state. I found no working sqlite3 command. I will use an available installer/package-manager MCP if one is configured; otherwise I need your approval to provide or run a manual install path for this machine.
```

## Do Not

- Do not run package manager commands without user approval.
- Do not choose a package manager based on guesswork.
- Do not install unrelated dependencies.
- Do not bypass the dependency by creating a hidden database with a different engine.
