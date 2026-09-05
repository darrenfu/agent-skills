# Component Library

Opt-in building blocks for visualizations. Use these when your design needs them — don't force-include them all. Style each component to match your creative direction (fonts, colors, spacing). These are starting points, not finished designs.

---

## Metrics Card

A prominent number with label and optional trend indicator. Use for KPIs, stats, or any numeric highlight.

**Structure**: Value (large, colored), label (small, muted), optional trend arrow with percentage.
**Layout**: Typically in a grid (`repeat(auto-fit, minmax(200px, 1fr))`).
**Styling**: Surface background, border, rounded corners (12px), center-aligned.

---

## Callout / Alert

A highlighted message box with icon, title, and body text. Use for warnings, key decisions, important notes, or tips.

**Structure**: Icon (left), title (bold) + body text (right). Left border accent (4px solid).
**Variants**: Info (blue), success (green), warning (amber), error (red). Use `color-mix()` for tinted backgrounds.
**Icons**: Info → ℹ, Success → ✓, Warning → ⚠, Error → ✕

---

## Collapsible Section

Progressive disclosure via `<details>/<summary>`. Use for secondary content, deep dives, or optional detail.

**Structure**: `<details>` with styled `<summary>`. Arrow indicator rotates on open.
**Styling**: Border, rounded corners, background change on hover. Content area has top border separator.

---

## Code Block with Copy

Syntax-highlighted code with a copy button. Use when showing code examples, configurations, or CLI commands.

**Structure**: Header bar (language label + copy button) over dark pre/code block.
**Styling**: Dark background (#0f172a), monospace font, 0.85rem size. Copy button in header.
**Script**: `navigator.clipboard.writeText()` with "Copied!" feedback.

---

## Sortable Data Table

A table with clickable column headers for sorting. Use for structured comparisons or tabular data.

**Structure**: `<table>` with `data-sortable` attribute. `<th>` elements have `data-sort="string|number"`.
**Styling**: Uppercase headers (0.8rem), alternating row hover, border-bottom separators.
**Script**: Sort rows on header click, toggle ascending/descending, show ↕ indicator.

---

## Tabs

Switch between content panels without page reload. Use for comparing approaches, showing different views of the same data, or organizing related sections.

**Structure**: Tab buttons in a row (`.tab-list`) + content panels (`.tab-panel`). Active state via class toggle.
**Styling**: Bottom border on active tab (primary color), transparent background, smooth transitions.
**Script**: Click handler toggles active class on buttons and panels.

---

## Timeline

Vertical sequence of events with date markers. Use for session summaries, project history, incident timelines, or chronological narratives.

**Structure**: Vertical line (left), circular markers, date/title/body stacked right of the line.
**Styling**: Line uses gradient (primary → border color). Markers are circles with border ring. Stagger animate-in.

---

## Progress Bar

A horizontal fill bar showing completion or proportion. Use for project status, loading states, or comparative metrics.

**Structure**: Label row (name + percentage, `justify-content: space-between`) over track with fill.
**Styling**: Track is 8px tall, rounded, muted background. Fill is primary color with width transition.

---

## Tag / Badge

Small inline labels for categorization or status. Use for status indicators, category labels, or metadata.

**Structure**: Inline-block `<span>` with padding and border-radius (20px pill shape).
**Variants**: Primary, success, warning, error, neutral. Use `color-mix()` for tinted backgrounds.
**Sizing**: 0.75rem, 500 weight, tight letter-spacing.

---

## Chart (Chart.js)

Data visualization via Chart.js. Use for bar charts, line charts, pie charts, or any quantitative visualization.

**CDN**: `<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4" integrity="sha384-NrKB+u6Ts6AtkIhwPixiKTzgSKNblyhlk0Sohlgar9UHUBzai/sgnNNWWd291xqt" crossorigin="anonymous" defer></script>`
**Container**: Relative-positioned div with fixed height (300px), canvas element inside.
**Config**: `responsive: true`, `maintainAspectRatio: false`, legend at bottom.
**Types**: bar, line, pie, doughnut, radar, polarArea.

---

## Mermaid Diagram

Flowcharts, sequence diagrams, and other structured diagrams via Mermaid. Use for system architecture, workflows, state machines, or any process visualization.

**CDN**: `<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.5/dist/mermaid.min.js" integrity="sha384-enVdc7lTHDGtpROV85t9+VqPC2EyyB0hsRD0MrvQnHUsHmTHIz2D8SPP4EnBkstH" crossorigin="anonymous" defer></script>`
**Container**: `<pre class="mermaid">` inside a styled container div.
**Init**: `mermaid.initialize({ startOnLoad: true, theme: 'default' })` — adjust theme for dark mode.
**Types**: graph TD/LR, sequenceDiagram, stateDiagram, classDiagram, gantt, pie.

---

## CountUp (Animated Number)

An animated number that counts up from zero when scrolled into view. Use for KPIs, stats, or any numeric highlight that benefits from a reveal moment.

**Structure**: `<span>` with `data-target` (final value), optional `data-duration` (ms, default 2000), `data-prefix` (e.g. "$"), `data-suffix` (e.g. "%").
**Script**: Uses `requestAnimationFrame` with easeOutExpo (fast burst, elegant deceleration). IntersectionObserver triggers the count once when element enters viewport.
**Accessibility**: Final value is set immediately if `prefers-reduced-motion: reduce` is active.

See `references/animations.md` → "Number Counter (WAAPI)" for the complete implementation.

---

## ProgressFill (Animated Progress Bar)

A progress bar that fills to its target width when scrolled into view. Uses the scroll-reveal observer from `assets/infra.html`.

**Structure**: Label row (name + percentage) over a track div containing a fill div. Fill width is set via `--fill` CSS custom property.
**Styling**: Track is 8px tall, rounded, muted background. Fill uses primary color with spring-like transition (`cubic-bezier(0.34, 1.56, 0.64, 1)`, 1s).
**Trigger**: Add `data-animate="fade-up"` to the **parent container** (e.g. `.progress-bar`), not the fill element. Use `.progress-bar.is-visible .progress-fill { width: var(--fill); }` to trigger the fill. Do NOT put `data-animate` on `.progress-fill` — it conflicts with infra.html's `transition-property`.

See `references/animations.md` → "Progress Bar Fill" for the complete implementation.

---

## ScrollReveal (Declarative Wrapper)

A declarative pattern for revealing any content on scroll using `data-animate` attributes. Infrastructure is handled automatically by `assets/infra.html`.

**Available animations**: `fade-up`, `fade-down`, `fade-left`, `fade-right`, `scale-up`, `blur-in`.
**Timing attributes**: `data-delay="200"` (ms), `data-duration="800"` (ms).
**Stagger**: Increment `data-delay` on each sibling (e.g. 0, 100, 200, 300) for a list reveal.
**Print/capture safe**: Elements forced visible in print styles and screenshot capture.

See `references/animations.md` → "Scroll-Triggered Reveals" for all patterns and examples.

---

## Auto-Generated Table of Contents

Sticky sidebar navigation generated from page headings. Use for long-form content with multiple sections.

**Structure**: Fixed `<nav>` (left side), auto-populated `<ul>` from `<h2>` and `<h3>` elements.
**Behavior**: IntersectionObserver highlights the active section. Indent h3 items.
**Responsive**: Hide on screens narrower than 1400px.
**Print**: Hidden via `@media print`.
