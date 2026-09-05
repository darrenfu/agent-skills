# Complexity investigation prompts

A pattern is a reason to inspect its costs and benefits, not evidence of an author's motives. Establish the actual requirements before recommending a change.

| Pattern | Investigate | Reasons it may be justified |
|---|---|---|
| Single-implementation interface | Does it simplify testing, ownership, or substitution enough to justify indirection? | Dependency inversion, external contract, security boundary |
| Plugin mechanism | What extensions exist or are committed, and how costly is the protocol? | Customer extensibility, isolation, independent ownership |
| Generic abstraction | Which variations does it represent and who understands it? | Repeated domain behavior, reliable type constraints |
| Services or orchestration | Compare deployment and operational cost with a simpler topology | Isolation, team ownership, existing platform, regulatory boundaries |
| Event-driven flow | Is asynchronous decoupling needed, and how are ordering/retries observed? | Buffering, durable integration, independent consumers |
| Custom implementation | Compare supported alternatives including migration and dependency risks | Missing capability, license, security, performance, offline requirements |
| Large configuration surface | Which options are used and how are invalid states prevented? | Multi-tenant needs, safe operational control |
| Defensive error handling | Can the condition occur across dependency or trust boundaries? | Untrusted inputs, partial failures, changing external services |
| Extensive tests or CI | Are checks tied to failure cost and changed paths? | Safety, persistence, compatibility, immutable release acceptance |
| Performance optimization | What profiling or credible workload evidence supports it? | Latency budget, capacity limit, cost at scale |
| Many small modules | Does navigation and ownership improve or worsen? | Stable boundaries, independent reuse, understandable responsibilities |
| Elaborate types | Do they catch meaningful invalid states at a reasonable comprehension cost? | Protocol correctness, domain invariants, maintainable API guarantees |

Do not use a fixed line count, interface count, team size, bundle size, or hypothetical user threshold as a universal cutoff. Look for measured cost, repeated failure, or unnecessary coupling and describe a proportionate alternative. Retain useful complexity when replacement risk exceeds its benefit.
