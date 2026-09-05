# Animation Reference

Rich animation patterns for standalone HTML visualizations. Three tiers: CSS-only scroll reveals (zero dependencies), WAAPI utilities (zero dependencies), and Motion One (optional CDN for spring physics).

---

## Animation Presets

Choose an energy level that matches your content's tone. Use the easing and duration as defaults for all animations on the page.

| Preset | Duration | Easing | When to use |
|--------|----------|--------|-------------|
| **Subtle** | 0.5s | `cubic-bezier(0.25, 0.1, 0.25, 1)` | Data dashboards, professional reports — content speaks for itself |
| **Energetic** | 0.4s | `cubic-bezier(0.22, 1, 0.36, 1)` | Product launches, creative showcases — inject momentum |
| **Cinematic** | 0.8s | `cubic-bezier(0.16, 1, 0.3, 1)` | Presentations, hero sections — dramatic reveals |
| **Data-driven** | 0.6s | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Counters, charts, progress bars — slight overshoot draws attention to numbers |

---

## Scroll-Triggered Reveals

Infrastructure in `assets/infra.html` handles observation automatically. Add `data-animate` attributes to any element below the fold.

### Available Animations

```html
<div data-animate="fade-up">Slides up 20px while fading in</div>
<div data-animate="fade-down">Slides down 20px while fading in</div>
<div data-animate="fade-left">Slides right 20px while fading in</div>
<div data-animate="fade-right">Slides left 20px while fading in</div>
<div data-animate="scale-up">Scales from 0.95 while fading in</div>
<div data-animate="blur-in">Blurs from 8px while fading in</div>
```

### Customizing Timing

```html
<!-- Delay reveal by 200ms -->
<div data-animate="fade-up" data-delay="200">...</div>

<!-- Slow reveal (800ms instead of default 600ms) -->
<div data-animate="scale-up" data-duration="800">...</div>
```

### Stagger Patterns

**List reveal** — increment `data-delay` on each item:

```html
<div data-animate="fade-up">Item 1</div>
<div data-animate="fade-up" data-delay="100">Item 2</div>
<div data-animate="fade-up" data-delay="200">Item 3</div>
<div data-animate="fade-up" data-delay="300">Item 4</div>
```

**Grid cascade** — combine row and column delay:

```html
<div class="grid">
    <div data-animate="scale-up">Row 0, Col 0</div>
    <div data-animate="scale-up" data-delay="80">Row 0, Col 1</div>
    <div data-animate="scale-up" data-delay="160">Row 0, Col 2</div>
    <div data-animate="scale-up" data-delay="120">Row 1, Col 0</div>
    <div data-animate="scale-up" data-delay="200">Row 1, Col 1</div>
    <div data-animate="scale-up" data-delay="280">Row 1, Col 2</div>
</div>
```

---

## CSS Keyframes Library

Copy-paste keyframes for page-load entrance animations (complement scroll reveals with above-the-fold content):

```css
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInScale {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}

@keyframes blurIn {
    from { opacity: 0; filter: blur(8px); }
    to { opacity: 1; filter: blur(0); }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(30px); }
    to { opacity: 1; transform: translateX(0); }
}
```

---

## Spring-Like CSS Easings

Cubic-bezier curves that approximate spring physics without a library:

```css
/* Gentle spring — subtle overshoot, professional feel */
--ease-spring-gentle: cubic-bezier(0.34, 1.56, 0.64, 1);

/* Bouncy spring — noticeable overshoot, playful energy */
--ease-spring-bouncy: cubic-bezier(0.175, 0.885, 0.32, 1.275);

/* Snappy spring — fast attack, smooth settle */
--ease-spring-snappy: cubic-bezier(0.22, 1, 0.36, 1);
```

Use these for hover lifts, button presses, and card entrances where a spring feel adds personality.

---

## Number Counter (WAAPI)

Animated number that counts up when scrolled into view. Zero dependencies — uses Web Animations API.

```html
<span class="count-up" data-target="1234" data-duration="2000">0</span>

<script>
function countUp(el) {
    var target = parseInt(el.getAttribute('data-target'), 10);
    var prefix = el.getAttribute('data-prefix') || '';
    var suffix = el.getAttribute('data-suffix') || '';

    // Respect reduced-motion preference
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        el.textContent = prefix + target.toLocaleString() + suffix;
        return;
    }

    var duration = parseInt(el.getAttribute('data-duration') || '2000', 10);
    var start = performance.now();

    function update(now) {
        var progress = Math.min((now - start) / duration, 1);
        // easeOutExpo — fast burst then elegant deceleration into final number
        var eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
        var current = Math.round(eased * target);
        el.textContent = prefix + current.toLocaleString() + suffix;
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}

// Trigger on scroll into view
var counterObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
        if (entry.isIntersecting) {
            countUp(entry.target);
            counterObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.3 });

document.querySelectorAll('.count-up').forEach(function(el) {
    counterObserver.observe(el);
});
</script>
```

**Options**: Use `data-prefix="$"` or `data-suffix="%"` for formatted output.

---

## Progress Bar Fill

CSS transition triggered when scrolled into view. Uses the scroll-reveal observer from infra.html, but applies `data-animate` to the **parent container** — not the fill element. Putting `data-animate` on `.progress-fill` would conflict with infra.html's `transition-property: opacity, transform, filter`, which does not include `width`.

```html
<div class="progress-bar" data-animate="fade-up">
    <div class="progress-label">
        <span>Completion</span>
        <span>78%</span>
    </div>
    <div class="progress-track">
        <div class="progress-fill" style="--fill: 78%"></div>
    </div>
</div>

<style>
.progress-track {
    height: 8px;
    border-radius: 4px;
    background: var(--surface-hover, #e2e8f0);
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 4px;
    background: var(--primary, #3b82f6);
    width: 0;
    transition: width 1s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.progress-bar.is-visible .progress-fill {
    width: var(--fill);
}
</style>
```

The `.is-visible` class is added to the `.progress-bar` container by the scroll-reveal observer in infra.html. The descendant selector triggers the fill's `width` transition without conflicting with `data-animate`'s own transition properties.

---

## Motion One (Optional CDN)

For real spring physics, complex timelines, and gesture-driven animations. ~3.8KB gzipped. Created by the author of Framer Motion.

**Only load when the visualization genuinely needs spring physics or timeline orchestration.** CSS-only solutions cover 90% of cases.

### CDN Tag

```html
<script src="https://cdn.jsdelivr.net/npm/motion@11.18.2/dist/motion.js" integrity="sha384-lFfU+kVPBF9H3h8c1O+KQNuTRX7dilL8RZiy/kxQiYulHvYCHv4z+eba37GD2qTC" crossorigin="anonymous" defer></script>
```

### Spring Animation

```js
var { animate, spring } = Motion;

animate(
    document.querySelector('.hero-card'),
    { scale: [0.9, 1], opacity: [0, 1] },
    { easing: spring({ stiffness: 200, damping: 20 }) }
);
```

### Timeline

```js
var { timeline } = Motion;

timeline([
    ['.hero-title', { y: [20, 0], opacity: [0, 1] }, { duration: 0.5 }],
    ['.hero-subtitle', { y: [15, 0], opacity: [0, 1] }, { duration: 0.4, at: '-0.2' }],
    ['.hero-cta', { scale: [0.9, 1], opacity: [0, 1] }, { duration: 0.3, at: '-0.1' }],
]);
```

### When to Use Motion One

| Use Case | Use Motion One? |
|----------|-----------------|
| Fade-in on scroll | No — use `data-animate` |
| Number counter | No — use WAAPI `countUp()` |
| Card entrance stagger | No — use `animation-delay` |
| Spring hover effect | Maybe — CSS `cubic-bezier` is often enough |
| Complex orchestrated timeline | Yes |
| Gesture-driven interaction | Yes |
| Physics-based spring with precise control | Yes |

---

## Anti-Patterns

| Rule | Why |
|------|-----|
| **Max 3 animation types per page** | More creates visual noise — pick entrance, scroll, and one accent |
| **No delay > 1s** | Users lose patience; 0.8s is the upper comfort limit |
| **Prefer transform and opacity** | Other properties (width, height, margin) trigger layout reflow. Exception: progress bar fills use `width` transitions since they're simple one-shot animations on small elements where reflow cost is negligible |
| **Don't animate above-the-fold AND on scroll** for the same element | Pick one trigger per element — doubling up looks glitchy |
| **Respect `prefers-reduced-motion`** | infra.html handles this automatically for `data-animate`; for custom WAAPI animations, check `window.matchMedia('(prefers-reduced-motion: reduce)').matches` before animating |
