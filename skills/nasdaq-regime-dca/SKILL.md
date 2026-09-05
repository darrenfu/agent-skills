---
name: nasdaq-regime-dca
description: Monthly Nasdaq DCA regime strategy workflow using CAPE percentile, Nasdaq drawdown, crash speed, VIX, QQQ/TQQQ holdings, cash reserve, and IBKR portfolio/order-review context. Use when the user asks about CAPE DD VIX Nasdaq DCA, QQQ/TQQQ dynamic allocation, Apodex Nasdaq backtest strategy, monthly rebalancing, ammunition cash bucket, or wants IBKR-connector-ready investment review output for this strategy.
---

# Nasdaq Regime DCA

Use this skill to turn a high-risk Nasdaq DCA idea into a monthly, reviewable decision memo. The skill is for research and order-ticket preparation, not autonomous trading.

## Required Inputs

Ask for or fetch these before producing an action:

- Account scope and base currency.
- Portfolio value, available cash, QQQ shares/value, TQQQ shares/value, and any money-market/cash-equivalent position.
- Monthly contribution amount and whether the user allows leveraged ETF exposure.
- Current Nasdaq-100 price level and drawdown from its prior high.
- 25-trading-day Nasdaq-100 return.
- VIX level.
- CAPE value and percentile or enough historical CAPE data to compute the percentile.
- Tax account type, margin status, and whether realized gains are acceptable this month.

If any live market value, price, VIX, CAPE, portfolio holding, or tax-sensitive fact matters, verify current data from a reliable source or the available connector before analysis.

## Workflow

1. Load `references/strategy.md` for the signal rules and output schema.
2. Load `references/ibkr-integration.md` when using an IBKR connector, browser portal, exported account statement, or order-ticket workflow.
3. Load `references/risk-notes.md` whenever TQQQ, leverage, high drawdown, taxes, or "should I follow this" is part of the request.
4. Produce a memo with:
   - Data freshness and sources.
   - Signal table: CAPE, drawdown, crash speed, VIX, heat/calm streak.
   - Regime classification: high valuation, normal, small bottom, major bottom, crash-risk reduction.
   - Target action: buy QQQ, buy TQQQ, skip contribution, trim TQQQ, drip cash to QQQ, or deploy ammunition cash.
   - Dollar sizing, share estimate, and cash left.
   - Risk gate, tax gate, and connector gate.
   - IBKR-ready order draft only when requested.

## Hard Rules

- Do not treat the source backtest as verified fact unless the backtest code/data have been independently rerun.
- Do not submit orders, transfer money, enable margin, or change account settings without explicit user confirmation at the final broker screen.
- Do not use market orders for TQQQ by default; prefer a reviewable limit-order draft.
- Do not recommend full-account TQQQ exposure. Keep TQQQ as a controlled accelerator with a stated max-loss path.
- If data are stale, missing, or contradictory, output `research further` rather than an action.

## Decision Labels

Use one of:

- `no-action`
- `normal-qqq-dca`
- `hold-cash-high-valuation`
- `trim-tqqq-to-ammunition`
- `small-bottom-qqq-boost`
- `major-bottom-tqqq-deploy`
- `risk-blocked`
- `needs-live-data`
