---
name: renaissance-architecture
description: Explore first-principles product ideas, new interaction models, or a substantial architecture rethink when the user requests those forms of design exploration. Compare novel and established approaches against user outcomes and constraints.
---

# Renaissance Architecture

Use first-principles thinking to explore what a product or architecture should achieve. Novelty is an option, not an acceptance criterion. Reuse, incremental improvements, and established patterns may best serve the user.

## Scope

Use for first-principles product ideation, exploration of new workflows, or an explicitly requested architecture rethink. A routine feature, bug fix, or code review should follow the existing architecture unless the task provides a reason to revisit it.

## Design from the problem

- Identify the user's job, unmet need, constraints, and desired outcome from available context. Challenge an inherited assumption only when it limits that outcome.
- Compare a simple extension of the current system, a conventional alternative, and a novel approach when each is plausible. Consider delivery cost, adoption, ownership, accessibility, and migration risk.
- Use the least complexity that can meet the requirements, including reliability, security, and credible growth needs. Measure bottlenecks before introducing a distributed boundary solely for scale.
- Choose a framework according to current capabilities, team expertise, ecosystem support, and deployment constraints. Verify version-sensitive claims from primary documentation when making a technical recommendation.

## Architecture choices

| Decision | Evidence to examine |
|---|---|
| Embedded database or server database | Write contention, transaction and availability requirements, operational model, required extensions, and measured workload |
| One module or several | Cohesion, independent responsibilities, ownership, testability, and navigation cost |
| Monolith or services | Deployment isolation, failure boundaries, team ownership, scaling needs, and distributed coordination cost |
| Static or server-rendered application | Authentication, computation, data freshness, caching, and hosting constraints |
| Local-first or cloud-dependent | Offline user needs, privacy, collaboration, synchronization correctness, device loss, and maintenance cost |

Do not use a fixed writer count, database size, or line count as a universal migration threshold. Evaluate the actual workload and product requirements.

## Useful design properties

- Make state, ownership, configuration, errors, and recovery understandable to maintainers and users.
- Compose stable interfaces and reuse existing components where they fit. Avoid unnecessary abstraction, but preserve boundaries that protect invariants.
- Offer immediate feedback, clear progress, and cancellation or undo where practical. Do not imply that an operation succeeded before verifying its outcome.
- Preserve spatial consistency, keyboard access, legible typography, and attention. Motion should help comprehension and respect reduced-motion preferences.
- Support export or an exit path when lock-in is a material concern. Do not require every product to work fully offline when its core function depends on shared services.

## Deliver

Match the request: an exploration presents options and a recommendation; an authorized implementation carries the selected scope through to verification. Ask only about missing choices with a material effect. Scale the written design and checks to the problem and project rules rather than requiring a full framework exercise for every change.
