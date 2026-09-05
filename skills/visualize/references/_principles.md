# Creative Principles

Read this file on every invocation. These are the guardrails that ensure quality without constraining creativity.

---

## The Prime Directive

Every visualization must feel **intentionally designed for its specific content**. If you swapped the content out, the design choices should feel wrong. The typography, color, layout, and interactions should all be in service of THIS content, THIS audience, THIS moment.

---

## Anti-Slop Rules

These are non-negotiable. Every visualization must satisfy ALL of these:

| Rule | Why |
|------|-----|
| **Never use default fonts.** No Inter, Roboto, Arial, system-ui, or system fonts. Choose a distinctive Google Fonts pairing matched to the content's tone. Never use the same pairing twice in a row. | Default fonts are the #1 signal of generic AI output. |
| **Commit to a dominant color.** Not a balanced 5-color palette — one dominant hue with supporting accents. Use CSS custom properties for consistency. | Even distribution of colors creates visual noise. Dominance creates identity. |
| **`:root` is light mode. `.dark-mode` is dark mode. No exceptions.** `:root` CSS variables must define light backgrounds (white, off-white, light pastels) and dark text. `body.dark-mode` overrides must define dark backgrounds and light text. The page loads without the `dark-mode` class (light by default). If your creative vision is "dark aesthetic," make `.dark-mode` stunning — but `:root` must still be genuinely LIGHT. The hamburger menu toggle adds/removes `body.dark-mode`; violating this polarity breaks the toggle. | The infrastructure assumes `:root` = light, `.dark-mode` = dark. When both are dark, the toggle does nothing and users are stuck in a dark page with no escape. |
| **Dark mode is a redesign, not an inversion.** Adjust primary colors, reduce saturation, change surface colors. Don't just flip black and white. | Inverted designs look broken. Redesigned dark modes look intentional. |
| **Backgrounds have character.** Gradient meshes, subtle noise, geometric patterns, layered transparencies, textured surfaces. Never flat white or flat gray with no atmosphere. | Flat backgrounds make everything look like a wireframe. |
| **One orchestrated entrance animation.** Stagger content reveals on page load via `animation-delay`. Skip scattered micro-animations. CSS-only where possible. | A choreographed entrance feels designed. Random animations feel noisy. |
| **Every visualization looks different.** Vary fonts, colors, layout approaches, and interaction patterns across generations. If it looks like the last one you made, start over. | Repetition is the enemy of the skill's value proposition. |

---

## The Creative Brief

Before writing any HTML, you MUST complete this creative brief internally. Do not skip any question. Your design choices should flow from these answers.

### 1. PURPOSE
What is this visualization communicating? Who is the audience? What should they feel or understand after viewing it?

### 2. METAPHOR
What visual world does this content belong to? Don't name the archetype — name a PLACE or OBJECT.

Not "this is a dashboard" but "this is a mission control room." Not "this is a presentation" but "this is a museum exhibit." Not "this is a report" but "this is a field journal from an expedition."

The metaphor guides every downstream decision: colors, typography, spacing, interactions.

### 3. TYPOGRAPHY
Name two specific Google Fonts. Articulate WHY they fit:

- **Display font** (headings, hero elements): What's the emotional register? Authoritative → serif. Modern → geometric sans. Technical → monospace. Warm → rounded humanist. Elegant → high-contrast serif. Playful → variable weight or rounded.
- **Body font** (paragraphs, labels): Must be readable at 16px. Should contrast with the display font in personality while harmonizing in proportion.

Browse https://fonts.google.com mentally. Consider fonts you haven't used recently.

### 4. PALETTE
Name ONE dominant hue and articulate why it matches the content's mood:
- Urgent/critical → warm reds, deep oranges
- Calm/analytical → cool blues, muted teals
- Growth/success → greens, emeralds
- Creative/experimental → purples, magentas
- Warm/approachable → ambers, terracottas
- Technical/precise → cool grays + one vivid accent

Then pick an accent that creates tension or complement with the dominant.

**Define colors for BOTH modes:**
- **Light mode** (`:root`): Your dominant hue at normal-to-high lightness. Backgrounds must be light (white, off-white, tinted pastels). Text must be dark. Cards/surfaces should be white or near-white.
- **Dark mode** (`body.dark-mode`): Reduce saturation, darken backgrounds to near-black, lighten text. Redesign — don't invert.

### 5. SIGNATURE
What ONE thing will make someone remember this visualization? Describe it in one sentence.

This could be: a striking background treatment, an unexpected layout decision, a clever hover interaction, an unusual typography choice, a distinctive color pairing, a memorable visual metaphor rendered in CSS.

### 6. COMPOSITION
- Dense or spacious? (Information-rich like a cockpit, or editorial like a magazine?)
- Scrolling or fixed? (Long-form narrative, or single-screen diagram?)
- Centered column or full-bleed? (Focused reading, or immersive experience?)
- Grid or organic? (Structured cards, or flowing asymmetric layout?)

---

## Typography Exploration

Font selection is the single highest-leverage creative decision. Here are starting points — explore beyond these:

| Mood | Display Options | Body Options |
|------|----------------|-------------|
| Editorial/Magazine | Playfair Display, Lora, Merriweather | Source Sans 3, Libre Franklin |
| Technical/Precise | JetBrains Mono, Space Mono, Fira Code | IBM Plex Sans, DM Sans |
| Bold/Modern | Sora, Outfit, Plus Jakarta Sans | Work Sans, Nunito Sans |
| Warm/Humanist | Fraunces, Vollkorn, Bitter | Nunito, Open Sans |
| Geometric/Clean | Space Grotesk, Manrope, Urbanist | DM Sans, Karla |
| Elegant/Refined | Cormorant Garamond, Libre Baskerville | Lato, Raleway |
| Playful/Creative | Bricolage Grotesque, Rubik, Quicksand | Outfit, Red Hat Display |
| Data/Scientific | Fira Code, Source Code Pro | Fira Sans, Inter |

These are suggestions to spark exploration. The best choice is one that perfectly matches your metaphor.

---

## Color Exploration

Do NOT reuse the same palette. Explore these territories:

- **Warm earth**: Terracotta, sand, olive, warm brown, burnt sienna
- **Cool ocean**: Navy, teal, seafoam, pearl gray, deep blue
- **Monochromatic + pop**: All shades of one hue with a single contrasting accent
- **High contrast**: Near-black backgrounds with vivid accent (electric blue, hot pink, lime)
- **Muted/desaturated**: Soft pastels, dusty rose, sage, lavender
- **Bold/saturated**: Primary colors at full intensity, playful energy
- **Jewel tones**: Deep emerald, sapphire, amethyst, ruby
- **Industrial**: Concrete gray, steel blue, caution yellow, rust orange
- **Nordic**: Ice white, pale blue, soft gray, silver, pine green

---

## Motion Philosophy

### Page-Load Entrance
Stagger above-the-fold content blocks with `animation-delay` (0.1s increments). Use `fadeInUp` (opacity + translateY) as the baseline, but consider alternatives: scale reveals, slide-ins from sides, blur-to-focus.

### Scroll-Triggered Reveals
For content below the fold, use `data-animate` attributes instead of page-load animations. The infrastructure in `assets/infra.html` handles IntersectionObserver setup automatically. Available: `fade-up`, `fade-down`, `fade-left`, `fade-right`, `scale-up`, `blur-in`. Stagger with `data-delay`.

### Data Animations
- **Number counters**: Use the `countUp()` WAAPI pattern for KPIs and stats — counts from 0 to target when scrolled into view.
- **Progress bars**: Use CSS transitions triggered by `.is-visible` (from scroll observer) — fills to target width on reveal.

### Spring Physics
For orchestrated timelines or real spring behavior, Motion One (~3.8KB) can be loaded from CDN. See `references/animations.md` for CDN tag and spring presets. Use sparingly — CSS-only covers 90% of cases.

### Animation Presets
Choose one energy level per visualization and use it consistently:

| Preset | Duration | Feel |
|--------|----------|------|
| Subtle | 0.5s | Professional, restrained |
| Energetic | 0.4s | Momentum, crisp |
| Cinematic | 0.8s | Dramatic, deliberate |
| Data-driven | 0.6s | Slight overshoot, draws eye to numbers |

### Hover & Transitions
One meaningful hover state per interactive element. Subtle lift (translateY + shadow) for cards. Color shifts for links. Scale for buttons. 200-300ms for UI state changes.

### Restraint
- Max 3 animation types per page. More creates visual noise.
- No delay > 1s. 0.8s is the upper comfort limit.
- `transform` and `opacity` only for animations. Other properties trigger layout recalculation and jank.

---

## Composition Principles

- **Generous negative space OR controlled density** — never mushy middle ground. Decide which serves the content and commit.
- **Asymmetry creates energy.** Centered layouts are safe. Off-center hero text, overlapping elements, or breaking the grid creates visual interest.
- **Hierarchy through scale.** The most important element should be dramatically larger than everything else. If everything is the same size, nothing is important.
- **Maximum width matters.** Full-bleed for immersive (dashboards, graphs). 900-1100px max-width for reading (articles, proposals). 600-800px for diagrams.

---

## Footer

Every visualization ends with a two-line footer:

```
{owner name} · {date}
Generated by /visualize claude skill
```

- **Line 1**: The owner's name (from context — the user who invoked the skill, or the subject of the content) and today's date.
- **Line 2**: Attribution to `/visualize` skill.
- Keep it small (0.7rem), centered, muted color, with a `border-top` separator.
- This is the ONLY templated element.
