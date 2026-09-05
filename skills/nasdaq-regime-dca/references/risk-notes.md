# Risk Notes

Use this strategy as a disciplined hypothesis, not a promise of future returns.

## Main Failure Modes

- Backtest overfit: thresholds such as CAPE 20/70/85, VIX 12/40, and drawdown 20% may fit the 2000-2026 sample but fail in a different regime.
- Synthetic TQQQ: the article uses synthetic 3x Nasdaq exposure before TQQQ existed in 2010, so the early-period results are model-dependent.
- Leveraged ETF path dependency: TQQQ targets daily 3x returns. Over multi-day holding periods, compounding and volatility can cause returns to deviate materially from 3x the index.
- Behavioral risk: a strategy with a -50% drawdown path can still be abandoned at the worst time.
- Tax drag: monthly trimming and redeployment can realize gains in taxable accounts.
- Execution drag: spreads, limit misses, slippage, borrow/funding costs embedded in swaps, and cash yield assumptions can change results.
- Regime mismatch: CAPE is usually based on S&P 500 earnings, while the traded exposure is Nasdaq-100. It is a market valuation proxy, not a Nasdaq-specific earnings model.
- Signal lag: CAPE changes slowly, VIX spikes quickly, and drawdown reacts after price damage. They measure different clocks.

## Concept Map

CAPE measures long-cycle valuation pressure. High CAPE usually means investors are paying a high price for normalized earnings, so future long-term returns may be lower and the market is more vulnerable to disappointment. It is poor for day-to-day timing but useful for deciding whether to add leverage.

Drawdown measures trend damage. It shows whether the market has already repriced meaningfully from its high. Deep drawdown plus cheap valuation suggests better forward expected returns, but drawdown alone can keep worsening.

VIX measures near-term implied volatility and fear from S&P 500 options. High VIX often appears near forced-selling periods. Low VIX can signal complacency, especially when valuation is already stretched.

The three-signal logic is a regime classifier:

- CAPE answers: "Is the market expensive or cheap relative to normalized earnings?"
- Drawdown answers: "Has price already reset?"
- VIX answers: "Is there forced fear or complacency?"

The strategy wants leverage only when expected return has improved and the market is emotionally stressed, not when the index is expensive, calm, and near highs.

## Risk Gate

Before any order draft, check:

- Would a 70-90% TQQQ decline be tolerable in dollars?
- Would total portfolio drawdown exceed the user's stated limit?
- Is this a taxable account where trimming creates a large tax bill?
- Is the data current as of the intended trading day?
- Is the user trying to chase an article without accepting the path risk?

If any answer blocks execution, return `risk-blocked`.
