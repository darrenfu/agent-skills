---
name: visualize
description: Visualize anything as a beautiful, distinctive HTML page. Use for session summaries, code explainers, data reports, onboarding guides, work summaries, meeting prep, presentations, experiment reports, and more. Produces production-grade interfaces with exceptional design quality.
argument-hint: <what to visualize>
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, AskUserQuestion, ToolSearch
---

# Visualize Skill

**Tagline**: "Visualize anything. HTML is your canvas."

Transform content into a beautiful, distinctive, interactive HTML page. Every visualization is unique — no generic "AI output" aesthetics.

## Invocation

```
/visualize <natural language instruction>
```

## Examples

```bash
/visualize summarize our conversation
/visualize explain how the auth system works
/visualize the query results as a dashboard
/visualize a quick-start guide for new devs
/visualize my work this week
/visualize a presentation on our Q4 results
/visualize an experiment report for the A/B test
/visualize compare Redis vs Memcached for our use case

# Custom output path
/visualize --output ~/projects/myapp/ explain the auth module
/visualize summarize this file, save it next to the source
```

---

## Output Rules (Non-Negotiable)

This skill produces **exactly one type of output**: a self-contained HTML file.

**DO:**
- Write HTML to `$WORKSPACE/index.html` using the `Write` tool
- Read files with `Read`, `Glob`, `Grep` to gather content

**DO NOT:**
- **No Google Slides** — even for "presentation" requests, create an HTML slide deck with keyboard navigation
- **No Google Docs** — do not create documents, only read from them if gathering content
- **No notebooks** — do not create Jupyter/Bento notebooks

If the user asks for a "presentation", "slides", or "deck" — create an **HTML presentation** with fullscreen slides and keyboard navigation, NOT a Google Slides document. HTML is always the output format.

---

## Workflow

### Step 1: Parse Intent

Analyze the user's instruction from `$1`:

1. **Identify content source**:
   - Current conversation context
   - Files/code in the workspace
   - Data/query results mentioned
   - External resources to gather

2. **Detect output path preference** (set `$OUTPUT_DIR`):
   - **Explicit flag**: If instruction contains `--output <path>`, extract the path and strip the flag from the instruction. Resolve `~` to `$HOME`.
   - **Natural language**: If instruction says "save next to the source", "output in the same folder", "put it in my project directory", etc., resolve the primary source file/directory path and use its parent directory.
   - **Default**: Leave `$OUTPUT_DIR` empty (Step 7 will use `$HOME/visualize/$DATE/$SLUG`).

3. **Detect custom template** (set `$CUSTOM_TEMPLATE`):
   - **Explicit flag**: If instruction contains `--template <path>`, extract the absolute file path and strip the flag from the instruction. This allows callers (e.g., plugins) to provide their own archetype reference file instead of using the built-in ones. The file should follow the same format as files in `references/` (communication goal, layout DNA, interaction DNA, flavor seeds, anti-patterns).
   - **Default**: Leave `$CUSTOM_TEMPLATE` empty (Step 4 will use built-in archetype references).

4. **Determine if clarification needed**:
   - If intent is crystal clear → proceed to archetype detection
   - If ambiguous → ask clarifying questions (Step 2)

### Step 2: Clarify (If Needed)

When the instruction is ambiguous, use AskUserQuestion to clarify:

**Content scope:**
- What content to include?
- Full conversation or specific parts?

**Format:**
- Presentation slides? Data report? Infographic? Or let me pick the best format?

**Audience:**
- Technical team? Executives? Broad org?

Offer recommendations based on the content type.

### Step 3: Detect Archetype

**If `$CUSTOM_TEMPLATE` is set, skip this step entirely.** The custom template IS the archetype — go directly to Step 4.

Match the content to the most appropriate visualization archetype. Use these signals:

| Archetype | Detection Signals |
|-----------|------------------|
| **Presentation Deck** | "slides", "presentation", "deck", "pitch", "talk"; content is sequential/narrative for an audience |
| **Experiment Report** | "experiment", "A/B test", "results", "analysis"; data with hypothesis/methodology |
| **Technical Proposal** | "proposal", "RFC", "design doc", "architecture"; problem + proposed solutions |
| **Visual** | "infographic", "diagram", "visual", "chart", "one-pager", "architecture diagram"; embeddable graphics, system diagrams, visual explainers |
| **Session Summary** | "summary", "recap", "worklog", "meeting notes"; timeline of events/decisions |
| **Dashboard** | "dashboard", "status", "metrics", "KPIs"; numeric health/monitoring data |
| **Comparison Matrix** | "compare", "comparison", "evaluation", "vs"; evaluating options against criteria |
| **FAQ / Reference** | "FAQ", "reference", "guide", "runbook", "how-to"; Q&A or step-by-step instructions |
| **Diff Review** | "diff", "PR", "review", "my changes", "what changed"; code review or local uncommitted changes |
| **Project Roadmap** | "roadmap", "project plan", "milestones", "phases", "where are we"; project progress with timeline strip and phase cards |
| **Graph** | "knowledge graph", "graph", "network", "connections", "map", "relationships"; entities with relationships, skill ecosystems, interconnected systems |
| **Freestyle** | None of the above match well; content is unique or mixed |

**If unsure between archetypes:** Pick the closest match and adapt. The archetype is an inspiration, not a constraint.

**If no archetype fits:** Skip to Step 5 and generate freely using only the shared design system principles.

### Step 4: Load Design References

Read the design reference files from the `references/` directory adjacent to this SKILL.md.

1. **Always read `references/_principles.md`** — Creative guardrails: anti-slop rules, the creative brief template, typography/color/motion/composition guidance. This is loaded every time.
2. **If `$CUSTOM_TEMPLATE` is set** — Read the custom template file at `$CUSTOM_TEMPLATE` instead of a built-in archetype. Skip Step 3's archetype detection — the custom template IS the archetype. This allows plugins to provide their own design references without modifying the visualize skill.
3. **Otherwise, read the matched archetype brief** (from Step 3) — Each archetype file is a ~70-line design brief describing communication goal, layout DNA, interaction DNA, flavor seeds, and anti-patterns. NO HTML templates — these are conceptual guidance that inspires unique output:
   - `references/presentation-deck.md`
   - `references/experiment-report.md`
   - `references/technical-proposal.md`
   - `references/visual.md`
   - `references/session-summary.md`
   - `references/dashboard.md`
   - `references/comparison-matrix.md`
   - `references/faq-reference.md`
   - `references/diff-review.md`
   - `references/project-roadmap.md`
   - `references/graph.md`
4. **Optionally read `references/components.md`** — Opt-in building blocks (metric cards, callouts, tables, timelines, etc.) when your design needs them. Don't force-include all components.
5. **Freestyle (no archetype matched and no custom template)**: Read only `_principles.md` and design freely.

**These are design briefs, not templates.** Each archetype provides flavor seeds — evocative visual metaphors that spark wildly different designs. Pick one that excites you, or invent your own.

### Step 5: Complete the Creative Brief

Before writing any HTML, you MUST complete the creative brief from `_principles.md`. Do not skip any question. Your design should flow from these answers:

1. **PURPOSE** — What is this communicating? Who is the audience?
2. **METAPHOR** — What visual world does this content belong to? Not "dashboard" but "mission control room." Not "report" but "field journal." The metaphor guides every downstream decision.
3. **TYPOGRAPHY** — Name two specific Google Fonts. Articulate WHY they fit this content's emotional register. Never reuse the same pairing twice.
4. **PALETTE** — Name ONE dominant hue and explain why it matches the content's mood. Then pick an accent.
5. **SIGNATURE** — What ONE thing will make someone remember this visualization? Describe it in one sentence.
6. **COMPOSITION** — Dense or spacious? Scrolling or fixed? Centered or full-bleed? Grid or organic? Why?

Then proceed to generate.

### Step 6: Gather Content

Based on the instruction, gather the content:

- **For session summaries**: Review conversation history, extract key points, decisions, action items
- **For code explainers**: Read relevant files, understand architecture, create diagrams
- **For data reports**: Collect metrics, analyze trends, prepare visualizations
- **For documentation**: Organize information, create clear sections
- **For presentations**: Distill into one-idea-per-slide structure
- **For experiment reports**: Structure as hypothesis → method → results → interpretation

### Step 7: Generate HTML

Create the HTML file from your creative brief and the archetype inspiration.

1. **Create workspace**:
   ```bash
   SLUG=$(echo "$INSTRUCTION" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | cut -c1-50)
   DATE=$(date +%Y-%m-%d)
   if [ -n "$OUTPUT_DIR" ]; then
       WORKSPACE="$OUTPUT_DIR"
   else
       WORKSPACE="$HOME/visualize/$DATE/$SLUG"
   fi
   mkdir -p "$WORKSPACE"
   ```

2. **Compose HTML** following these rules:
   - Start with a clean `<!DOCTYPE html>` — design from scratch guided by your creative brief
   - **Add `<base target="_blank">` in the `<head>`** (after `<meta name="viewport">`). This forces all links to open in a new tab, which is important when the page is embedded in an iframe.
   - **Copy ALL THREE named blocks from `assets/infra.html`** (read the file first). This is the hamburger menu infrastructure. You MUST include all three — missing any one breaks the menu:
     1. **INFRA-MENU-CSS** — the `<style>` block starting with `.viz-menu {`. Paste into `<head>`. **This is the most commonly forgotten block — it looks like "more CSS" but it's critical infrastructure. Without it, menu items render as raw unstyled buttons at the top of the page.**
     2. **INFRA-MENU-HTML** — the `<nav class="viz-menu">` block with toggle button and menu panel. Paste at the start of `<body>`.
     3. **INFRA-MENU-JS** — the `<script>` block with `toggleMenu`, `toggleTheme`, `toggleFullscreen`, `loadHtml2Canvas`, `saveAsImage`, `doCapture`, and `initSlideHash`. Paste before `</body>`.
     Do NOT rewrite, abbreviate, or cherry-pick. Copy verbatim. **Every visualization MUST include all three blocks.**
   - **Slide deck hash navigation** is handled automatically by `initSlideHash()` in the infra JS. For presentation decks with `.slide` elements and a `goSlide()` function, the infra automatically: (a) updates the URL hash as the user navigates (e.g., `#5`), (b) jumps to the hash slide on page load, (c) responds to `hashchange` events. You do NOT need to add hash navigation code yourself — the infra handles it.
   - Load **Google Fonts** matching your chosen typography (never system fonts)
   - Define **CSS custom properties** for your color palette with this strict contract:
     - `:root` = **light mode** (light backgrounds like `#f8f7ff`, `#fafafa`, `#fff`; dark text like `#1a1a2e`, `#0f172a`)
     - `body.dark-mode` = **dark mode** (dark backgrounds like `#0c0e1a`, `#111`; light text like `#e8eaf6`, `#f1f5f9`)
     - The page loads WITHOUT `dark-mode` class — light by default
     - Even if your creative vision is "dark aesthetic," `:root` must still use genuinely light backgrounds — make `.dark-mode` stunning instead
   - Include **animations** — page-load entrance reveals and scroll-triggered animations using patterns from `references/animations.md`. Use `data-animate` attributes for below-the-fold content (infrastructure handles observation via `assets/infra.html`).
   - Only load CDN dependencies (D3, Chart.js, Mermaid) when actually used. Always copy the full `<script>` tag including `crossorigin` attributes from the reference files — never strip them.
   - **SRI hashes**: All CDN `<script>` tags in the reference files already include hardcoded `integrity` attributes — copy them verbatim. If you add a new CDN dependency not listed in `scripts/sri_hashes.json`, compute its hash by running `scripts/compute_sri.sh <url>`.
   - Pick building blocks from `references/components.md` as needed — don't include all of them
   - Respect the archetype's **anti-patterns** — these are the guardrails
   - Draw from the archetype's **flavor seeds** for visual inspiration, or invent your own
   - Make it **distinctive** — if it looks like the last visualization you generated, start over
   - **Spatial consistency**: When comparing two items (A vs B), keep them on the same side (left/right) throughout the entire page — hero, scorecard, table columns, teaser, etc. If A is on the left in the hero banner, A must stay on the left in every subsequent section. Inconsistent positioning breaks visual scanning and confuses the reader.

3. **Infra integrity check** — before saving, verify ALL THREE infra blocks are present by confirming these strings exist in your HTML:
   - `.viz-menu {` — the infra CSS (most commonly forgotten!)
   - `<nav class="viz-menu"` — the infra HTML
   - `function toggleMenu()` — the infra JS

   **If any is missing, STOP.** Re-read `assets/infra.html` and inject the missing block. Do not proceed to save.

4. **Theme polarity check** — verify the `:root` vs `.dark-mode` color contract before saving:
   - Find `--bg` in your `:root` block. It MUST be a light color (hex value starting with `#f`, `#e`, `#d`, or similar high-lightness values like `#fafafa`, `#f8f7ff`).
   - Find `--bg` in your `.dark-mode` block. It MUST be a dark color (hex value starting with `#0`, `#1`, `#2`).
   - Find `--text-primary` in `:root`. It MUST be a dark color (readable against light backgrounds).
   - **If `:root` has dark backgrounds, STOP.** You have inverted polarity. Swap the color blocks: move the dark colors to `.dark-mode` and create genuinely light colors for `:root`. Do not proceed to save until fixed.

5. **Save HTML to workspace**:
   - `$WORKSPACE/index.html` - Main visualization

6. **Set `$TITLE`** — a short, human-readable title for the visualization (e.g. "Q4 Experiment Results", "Auth System Architecture"). Derive it from the creative brief's PURPOSE, not the slug.

7. **Write classification metadata** — Write `$WORKSPACE/metadata.json` with structured fields that classify this visualization across three dimensions.

   **Label format rules** (apply to ALL classification fields):
   - All lowercase
   - Words joined by `-` (dash)
   - Max 3 words (max 2 dashes)
   - No articles, prepositions, or filler ("the", "of", "for", "a")

   Write this JSON to `$WORKSPACE/metadata.json`:

   ```json
   {
     "title": "$TITLE",
     "instruction": "$INSTRUCTION",
     "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
     "intent": "<broad purpose category>",
     "intent_detail": "<specific intent, max 3 words>",
     "output_type": "<format of generated artifact>",
     "output_subtype": "<specific variant, max 3 words>",
     "source_type": "<primary content source>",
     "source_count": <number of distinct sources consumed>,
     "num_sections": <count of major sections in the HTML>,
     "cdn_libs": "<comma-separated library names in alphabetical order, or 'none'>",
     "has_interactivity": <1 if tabs/filters/toggles/accordions, 0 otherwise>
   }
   ```

   **Intent** — WHY the user invoked /visualize:
   | `intent` | When to use |
   |----------|-------------|
   | `summary` | Summarize, recap, digest, debrief |
   | `comparison` | Compare, vs, evaluate, contrast |
   | `diagram` | Architecture, flow, system map, graph |
   | `analysis` | Analyze, investigate, metrics, trends |
   | `report` | Report, findings, results, experiment |
   | `explanation` | Explain, teach, guide, onboard, how-to |
   | `presentation` | Present, pitch, deck, slides |
   | `mockup` | Mockup, wireframe, prototype, design |
   | `status` | Status, dashboard, health, KPIs |
   | `review` | Review diff, PR, code changes |
   | Other | Use your best judgment, follow the label format rules |

   **`intent_detail`** — Specific intent within the category (e.g., `work-recap`, `architecture-options`, `debug-funnel`, `topline-metrics`, `onboarding-guide`, `experiment-results`). Apply the same format rules.

   **Output** — WHAT was actually generated:
   | `output_type` | When to use |
   |---------------|-------------|
   | `slide-deck` | Multi-slide presentation with navigation |
   | `single-page` | Long-form scrollable page |
   | `dashboard` | Metrics/charts layout |
   | `interactive-graph` | D3/force-directed/network visualization |
   | `diagram` | Static or animated system diagram |
   | `report` | Structured document with sections |
   | Other | Use your best judgment, follow the label format rules |

   **`output_subtype`** — Specific variant (e.g., `topline-metrics`, `force-directed`, `comparison-table`, `timeline-view`, `code-walkthrough`).

   **Source** — WHERE the content came from:
   | `source_type` | When to use |
   |---------------|-------------|
   | `local-file` | Files from disk |
   | `conversation` | Current chat context only |
   | `url` | External URL or web content |
   | `mixed` | Multiple source types combined |

### Step 8: Open / Share

After generating the HTML, help the user access it:

1. **Open locally** — suggest opening the file in a browser:
   ```bash
   open "$WORKSPACE/index.html"   # macOS
   xdg-open "$WORKSPACE/index.html"  # Linux
   ```

2. **Optional: serve locally** for live-reload workflows:
   ```bash
   npx serve "$WORKSPACE"
   # or
   python3 -m http.server 8080 -d "$WORKSPACE"
   ```

3. **Optional: deploy** — if the user wants to share publicly, suggest:
   - GitHub Pages
   - Netlify (`npx netlify deploy --dir=$WORKSPACE`)
   - Vercel (`npx vercel $WORKSPACE`)
   - Any static file host

### Step 9: Report Success

**Output template:**

```
Visualization ready!

Local: {workspace}/index.html

{Brief 1-2 sentence summary of what was visualized}
Format: {output_type} ({output_subtype})
```
