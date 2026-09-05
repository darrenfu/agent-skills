---
name: design-audit
description: Audit or refine an existing UI when the user requests a design review, visual polish, hierarchy, spacing, color, typography, consistency, or accessibility improvements. Scope inspection and implementation to the requested component, flow, or product.
---

# Design Audit

Review and refine an existing interface within the user's requested scope. Improve readability, hierarchy, consistency, accessibility, and usability while preserving the intended product behavior.

## Scope and authorization

- A review request produces findings; an explicit request to fix or polish the interface authorizes the corresponding reversible implementation. Use approval already established in the conversation. Do not add a separate plan or phase approval for work already requested.
- Scope the work to a component, flow, page, or whole product. A spacing fix does not trigger a whole-app audit.
- Ask only for a missing decision that would materially change the result and cannot be inferred from the app or existing requirements. Continue independent work while that decision is pending.
- Functional changes beyond the requested design task need separate scoping. Preserve existing data flows, navigation, and accessibility behavior.

## Inspect

Read the relevant components, existing tokens, and any applicable product or design guidance. Inspect the affected live UI or a rendered artifact when available. Missing conventional files such as PRD.md or DESIGN_SYSTEM.md do not by themselves block the task.

For a full audit, sample representative screens, states, and supported viewport sizes. For a local fix, inspect the affected layout and its likely responsive impact. State coverage limits when runtime access is unavailable.

Use [design-principles.md](design-principles.md) as design heuristics, evaluated against the product's users and requirements. Simplification must preserve discoverability, meaning, and necessary controls; visual minimalism is not an independent acceptance criterion.

## Review dimensions

Select relevant checks: hierarchy; spacing and alignment; typography; color and contrast; component consistency; keyboard/focus behavior; loading, empty, error, and disabled states; responsiveness; motion and reduced-motion behavior; dark mode if supported.

Attach each actionable finding to an observed element or file, explain its user impact, and propose a concrete change. Distinguish measurement from subjective judgment. Do not invent contrast ratios or claim accessibility conformance without the applicable evidence.

## Implement and verify

Use existing design tokens and conventions. Add a token when reuse warrants it; avoid building a new token system for a one-off correction. If implementation is requested, make the scoped changes and inspect their effect before reporting completion.

Verification follows the project's risk tier. Check the affected component, relevant states, and representative widths. Broaden only when a shared token or layout change can affect other surfaces. Reuse evidence while the code and environment remain unchanged.

For a full review, adapt [audit-template.md](audit-template.md). For a small fix, a concise result and verification note are enough. Update existing project documentation only where the change warrants it; do not create progress or lessons files by default.
