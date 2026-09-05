---
name: stock-risk-first-trading
description: Risk-first stock and options analysis workflow for evaluating trade ideas, viral trading stories, high-risk stock speculation, 0DTE/options leverage, value-investing claims, margin-of-safety checks, and post-trade reviews. Use when the user asks about 炒股, 美股, 个股, 期权, 短线交易, 暴富故事拆解, 投资避坑, or wants a disciplined checklist before considering a stock or options trade.
---

# Stock Risk First Trading

## Overview

Use this skill to turn stock or options ideas into a risk-first decision memo. The goal is survival, error avoidance, and falsifiable reasoning before upside discussion.

This is not a recommendation engine. For real tickers, current prices, fundamentals, laws, taxes, and news are unstable: verify live data from primary or reputable sources before analysis.

## Core Workflow

1. **Define the setup**
   - Identify instrument, ticker, market, trade type, time horizon, intended capital, maximum acceptable loss, and whether leverage/options/borrowed money are involved.
   - If any symbol, price, news, valuation multiple, earnings, or option chain matters, fetch current data first.

2. **Extract the thesis**
   - State the reason the trade should work in one sentence.
   - Separate catalyst, business quality, valuation, sentiment, and technical timing.
   - Name the invalidation condition before discussing target return.

3. **Run the blow-up filter**
   - Flag as `reject` or `speculative only` if the idea depends on borrowed money, 0DTE or very short-dated options, undefined max loss, position size that impairs sleep, averaging down without a new thesis, or copying a viral success story.
   - Treat "ordinary person made millions" stories as survivor-bias evidence unless the base rate, losses, and position sizing are documented.

4. **Check business and valuation**
   - Ask whether the business is durable or cyclical.
   - For cyclical sectors such as memory, commodities, shipping, and energy, do not mistake a temporary contract, shortage, or price spike for durable demand.
   - Require a margin of safety: compare valuation with cycle-normalized earnings or cash flow, not only recent growth or popular narratives.

5. **Size for survival**
   - Compute max loss in dollars and as a percentage of portfolio.
   - Limit single-idea loss before entry; options premium should be fully loss-assumed.
   - Prefer a smaller research position or watchlist when the thesis is interesting but valuation, timing, or risk is unclear.

6. **Produce a decision**
   - Use one of: `reject`, `watchlist`, `research further`, `small-risk experiment`, or `acceptable risk`.
   - Include thesis, evidence, key risks, invalidation, max loss, position sizing logic, and what new evidence would change the view.

## Viral Trading Story Protocol

When analyzing a viral trading story, do not extract a "strategy" until the following are answered:

- What was the full path, including losses and near-ruin points?
- Was leverage, 0DTE, margin, borrowed money, or concentrated betting involved?
- What was the base rate: how many comparable traders failed?
- Which part was skill, which part was one-time luck, and which part was market regime?
- Is the final lesson "copy this" or "avoid this failure mode"?

Default conclusion for stories built on extreme short-dated options or leverage: useful as a warning, not as an operating model.

## Output Template

```markdown
## Risk-First Trade Memo

Instrument:
Time horizon:
Setup:

### Current Data Checked
- Price/news/fundamentals/options chain:
- Sources:

### Thesis
-

### Blow-Up Filter
- Borrowed money:
- Leverage/options:
- Max loss:
- Survivor-bias risk:
- Verdict:

### Business And Valuation
- Business durability:
- Cycle risk:
- Margin of safety:
- What must be true:

### Position And Exit
- Portfolio risk:
- Entry condition:
- Invalidation:
- Stop or exit rule:

### Decision
Verdict: reject / watchlist / research further / small-risk experiment / acceptable risk
Reason:
What would change the decision:
```

## Reference

For the source video that motivated this skill, read `references/source_distillation.md` when the user asks about the ByteDance employee trading story, 0DTE/末日期权, viral stock-success lessons, or the origin of this framework.
