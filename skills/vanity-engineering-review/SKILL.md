---
name: vanity-engineering-review
description: Assess suspected overengineering, unnecessary abstractions, or maintenance complexity when the user requests a complexity audit, vanity check, simplification review, or a requirements-versus-cost evaluation. Ground findings in evidence and tradeoffs.
---

# Complexity and Value Review

Evaluate suspected overengineering through evidence about requirements, maintenance cost, operational risk, and user or business value. Do not infer an engineer's motives from a technology choice.

## Scope

Use for an explicit complexity audit, overengineering question, or simplification assessment. An ordinary bug review does not require this framework. A review produces recommendations; it does not authorize deleting systems, disabling services, or scheduling shutdowns.

## Method

1. Establish the relevant users, required behavior, constraints, current workload, credible planned changes, and ownership from available context. Ask only about gaps that could change the recommendation. Missing information is uncertainty, not evidence of vanity.
2. Inspect the affected code or design. Use [detection-patterns.md](references/detection-patterns.md) for questions to investigate, not automatic diagnoses.
3. For each finding, identify concrete complexity, its benefit, its ongoing cost, and a feasible alternative. Include migration effort, reversibility, dependencies, failure modes, and capabilities lost by removal.
4. Consider reliability, security, compliance, platform reuse, testability, and future options as legitimate value. Low daily usage does not make disaster recovery or a safety control unnecessary.
5. Recommend retaining, simplifying, replacing, or retiring the component according to evidence. Keep a system when its benefits justify its cost. Do not force a deletion recommendation or invent precise maintenance-hour estimates.
6. For a requested lifecycle plan or an uncertain investment, adapt [kill-criteria-template.md](references/kill-criteria-template.md) into review criteria. These are optional and do not become execution authorization.

## Output

Lead with the recommendation and strongest evidence. For each significant finding, give its location, practical impact, simpler alternative if one exists, and tradeoffs. Use project severity conventions; avoid arbitrary ratios or mandatory scores. Mark estimates and confidence. A small review may need only a few paragraphs.

Use direct, respectful language about the system and its constraints. Apply the negentropy framework only when the task calls for that lens, not as an automatic second review.
