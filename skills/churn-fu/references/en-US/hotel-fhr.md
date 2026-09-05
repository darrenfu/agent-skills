# Hotel FHR Placeholder

This file is a placeholder for future hotel portal or Fine Hotels + Resorts workflow design.

Do not use for live execution.

## Current Status

- No FHR execution workflow is implemented yet.
- Do not open a live issuer travel portal for FHR.
- Do not search, rank, book, change, cancel, or submit payment for FHR.
- Do not request site authorization for FHR transactions.
- Do not infer FHR policy or booking rules from the Hilton semi-flex workflow.

## Allowed Work

- Capture user requirements, constraints, and open questions.
- Record public official-source research notes when explicitly requested.
- Draft a future workflow proposal for user review.
- Keep any notes non-sensitive and out of committed runtime state unless the user asks for a repo update.

## Future Implementation Checklist

Before this file becomes executable, add:

- Official booking-channel eligibility rules.
- Login and portal handoff rules.
- Search, ranking, and cancellation-policy rules.
- Payment mapping and confirmation scope.
- SQLite state model and dry-run evals.
- Contract tests that fail before the implementation and pass after it.
