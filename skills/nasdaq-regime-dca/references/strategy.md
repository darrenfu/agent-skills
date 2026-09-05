# Strategy Reference

This reference distills the public article "Is Nasdaq DCA really optimal? I used AI to backtest 26 years and found a 34% annualized strategy" by @app_sail, mirrored by YouMind from an X Article dated 2026-06-25.

Source links:

- X Article: https://x.com/app_sail/status/2070037504674173060
- Public mirror used for extraction: https://youmind.com/zh-CN/landing/x-viral-articles/nasdaq-ai-backtest-investment-strategy

Treat the article as a strategy hypothesis, not as independently verified research. It reports a 2000-2026 monthly backtest with QQQ, TQQQ, and a three-signal dynamic framework. It also says pre-2010 TQQQ was synthetically modeled as 3x Nasdaq exposure.

## Core Thesis

Plain QQQ DCA is a robust baseline but may leave return on the table. Plain TQQQ DCA has much higher return potential but path risk is psychologically and financially severe. The strategy tries to keep QQQ as the default core, use TQQQ only when valuation, drawdown, and fear line up, and build an ammunition cash bucket during overheated markets.

The edge is not "always use leverage." The edge is:

- Avoid adding leverage when valuation is high and price is near highs.
- Preserve cash during overvaluation or excessive calm.
- Deploy cash and TQQQ exposure during deep, fearful selloffs.
- Keep a floor allocation so the strategy does not fully exit the market.

## Signals

Use five-day smoothed values when available. Evaluate monthly, preferably on the first trading day.

Valuation signal: CAPE percentile

- Below 20%: extremely cheap.
- Above 70%: expensive.
- Above 85%: bubble-warning zone.

Trend/drawdown signal: Nasdaq-100 drawdown and crash speed

- Drawdown from prior high greater than 20%: deep drawdown.
- 25-trading-day decline greater than 12%: fast-crash warning, used to reduce leverage.

Fear/calm signal: VIX

- Above 40: extreme fear.
- Below 12: excessive calm, especially dangerous when valuation is high.

## Monthly Decision Tree

First count low-zone signals:

- CAPE percentile below 20%.
- Nasdaq-100 drawdown greater than 20%.
- VIX above 40.

Then decide:

- If 2-3 low-zone signals are active: classify as `major-bottom-tqqq-deploy`. Deploy all ammunition cash plus up to 3x the monthly contribution into TQQQ, subject to risk gates. Scale into the target leverage over roughly six months instead of jumping all exposure in one day.
- If exactly 1 low-zone signal is active: classify as `small-bottom-qqq-boost`. Invest up to 2x the monthly contribution into QQQ, subject to cash and risk gates.
- Else if 25-trading-day Nasdaq decline is worse than -12%: classify as `trim-tqqq-to-ammunition`. Sell or draft a sale for half of TQQQ exposure into the ammunition bucket.
- Else if CAPE percentile is above 70% and Nasdaq is close to its historical high: classify as `hold-cash-high-valuation`. Skip the monthly buy and add contribution to the ammunition bucket.
- Else if excessive heat/calm persists for six or more months, defined as VIX below 12 or CAPE percentile above 85%: classify as `trim-tqqq-to-ammunition`. Sell roughly one-twelfth of TQQQ exposure per month while retaining the strategy's minimum TQQQ floor.
- Else: classify as `normal-qqq-dca`. Invest the standard monthly contribution into QQQ.

## Ammunition Bucket

Use the ammunition bucket for money moved out of TQQQ or skipped during high-valuation months.

- Park it in cash or a money-market-like instrument, depending on the account.
- If no low-zone signal is active, drip one-sixth of the bucket into QQQ each month, unless the user chooses a slower drip.
- If any low-zone signal activates, deploy the full bucket according to the small-bottom or major-bottom rule.

The source article claims slower drip schedules tested better in its backtest. Do not treat that as universal; it may be sample-specific and tax/friction-sensitive.

## Output Schema

```markdown
## Nasdaq Regime DCA Memo

Date:
Account:
Mode: research / IBKR draft / live review

### Data Freshness
- CAPE:
- CAPE percentile:
- Nasdaq-100 level:
- Nasdaq-100 drawdown from high:
- 25-trading-day return:
- VIX:
- Portfolio holdings:
- Cash / ammunition bucket:

### Signal Table
| Signal | Current | Threshold | State |
| --- | ---: | ---: | --- |
| CAPE percentile | | <20 / >70 / >85 | |
| Nasdaq drawdown | | >20% | |
| 25-day crash speed | | <-12% | |
| VIX | | >40 / <12 | |
| Heat/calm streak | | >=6 months | |

### Decision
Label:
Action:
Sizing:
Cash left:

### Risk Gate
- Max projected drawdown:
- TQQQ exposure after action:
- Tax/friction concern:
- Margin concern:
- Data concern:

### IBKR Draft
- Orders to prepare:
- Order type:
- Limit-price logic:
- Do not submit without explicit confirmation:
```
