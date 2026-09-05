# Design audit reporting template

Use this structure for a substantial audit; omit empty sections and shorten it for a component review. For an authorized implementation, report the result rather than presenting another approval gate.

- **Scope and evidence:** inspected surfaces, states, viewports, and access limitations.
- **Findings:** observed problem → concrete proposed change → user impact. Group by severity only when useful.
- **Implementation:** relevant component/file, existing token or proposed value, and behavior to preserve. Distinguish inspected values from illustrative examples.
- **Verification:** checks appropriate to the affected UI and project risk tier; list what was actually observed.
- **Open decisions:** only missing product choices or newly expanded scope that need user input.

Use critical/refinement/polish phases if they help sequence a large body of work. Do not require all three or approval after every phase. Existing authorization covers unchanged scope. Reuse the design system; a new token does not create a separate approval requirement unless project rules or the user require one.

Measure contrast or layout values before reporting them as facts. Prefer an exact selector and reproducible observation over adjectives such as “premium.”
