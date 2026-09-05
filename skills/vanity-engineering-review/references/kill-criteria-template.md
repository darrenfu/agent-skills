# Optional lifecycle review criteria

Use when the user asks for a lifecycle plan, an experiment needs a stopping rule, or ongoing investment has a material unresolved hypothesis. An ordinary code review does not need this artifact.

Record:

- Component or experiment, owner, intended value, and dependencies.
- Success measure and baseline, with a source and sampling window.
- Review trigger and rationale, using stakeholder-approved thresholds where available; mark proposed thresholds as proposals.
- Options at review: retain, repair, simplify, replace, or retire.
- Costs of stopping, data retention needs, rollback, recovery time, and affected users.
- Who can decide and what existing authorization or runbook permits execution.

A threshold schedules or motivates a review only if that follow-up is requested. It does not authorize an agent to shut down a service, delete data, send notifications, or create an automation. A low-usage recovery component may still be essential. A security incident calls for the applicable incident-response process, not an automatic deletion rule invented by this skill.

Only use automatic containment already defined by an authorized operational runbook, within its exact target and conditions. Where an outcome is ambiguous, verify state before retrying a mutation.
