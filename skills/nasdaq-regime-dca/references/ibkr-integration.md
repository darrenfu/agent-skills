# IBKR Integration

Use this reference when an IBKR connector, Client Portal export, browser portal, or user-provided IBKR screenshot is part of the task.

## Connector Contract

Default to read-only first:

1. Fetch account summary, net liquidation value, base currency, cash balances, margin status, and available funds.
2. Fetch positions for QQQ, TQQQ, and cash-like instruments.
3. Fetch open orders for QQQ/TQQQ to avoid duplicate orders.
4. Run the strategy memo from `strategy.md`.
5. Produce an order draft only after the memo passes the risk gate.
6. Stop before final submission unless the user explicitly asks to proceed and confirms the exact order details.

If no exact IBKR connector is available, use exported statements, CSVs, or browser-visible data as the input source. State that portfolio data were not connector-verified.

## Order Drafting Rules

- Prefer limit orders for QQQ and TQQQ.
- Use share estimates from current bid/ask or last price, then round down to whole shares unless fractional shares are confirmed available.
- Include a cash buffer for commissions, SEC/TAF fees on sales, and price movement.
- Avoid market orders for TQQQ because volatility and spread can widen during the exact regimes where the strategy trades.
- Never enable margin, options permissions, or futures permissions as part of this strategy.

## Required Memo Fields Before Drafting Orders

- Account identifier or nickname, masked if needed.
- Net liquidation value.
- Cash available for trading.
- Existing QQQ/TQQQ quantity and market value.
- Proposed post-trade QQQ/TQQQ/cash weights.
- Estimated realized gain/loss if selling TQQQ.
- Limit price basis and expiry.
- "Do not submit" notice.

## Browser Portal Safety

If using the IBKR website instead of a connector:

- Stop on 2FA, email-token, CAPTCHA, account restriction, or any final submit button.
- Do not inspect or reveal passwords, tokens, recovery codes, or full account numbers.
- Treat a visible preview/order ticket as the handoff point unless the user confirms final submission in the current turn.
