# Hilton Semi-Flex Credit Workflow

Use this for Amex Hilton Aspire, Surpass, and Business Platinum Hilton statement credit booking/refund workflows. Use it only when the user asks for execution. Before the first Hilton submit in a live run, obtain a site-level batch authorization that covers the eligible booking/refund/cancellation scope.

## Triggers

- SQLite or the Amex tracker shows current half or quarter Hilton-related credit remains unused.
- The user accepts forum-DP risk: the Hilton credit may be delayed, fail, or reverse after refund.
- The goal is to create a cancellable Hilton direct charge and mark the benefit `pending_credit`, not completed.

## Flow

1. Audit unused Amex Hilton-family benefits.
2. Route by product:
   - Aspire: Hilton Resort Credit, half-year cadence.
   - Surpass: Hilton Credit, quarter cadence.
   - Business Platinum: Hilton Statement Credit, quarter cadence.
3. Open Hilton and verify signed-in state; if not signed in, stop for the user to complete saved login.
4. Book `Hilton Grand Vacations Club Flamingo Las Vegas`.
5. Pick a 1-night stay 8 months out, outside peak and holiday-weekend windows.
6. Select the cheapest `Honors Discount Semi-Flex`; nightly room price must be below $300.
7. If the target date fails price or availability, roll one month later and try up to 5 dates; if no valid availability is found, exit with an error.
8. On Payment, choose Edit card and match the saved card by target card alias, visible last four, and expiry.
9. If saved card last four values are duplicated, require expiry to disambiguate; if still ambiguous, stop for manual selection.
10. Before the first final booking submit, verify or request a site-level batch authorization covering Hilton, eligible cards, card last four/expiry scope, benefits, room price ceiling, taxes/fees ceiling, stay date window, and cancellation rule.
11. Submit each covered booking while the active site-level batch authorization remains valid; do not require per-card or per-reservation confirmation.
12. After successful booking, record reservation alias, visible confirmation, hotel, date, rate, total, card last four, expiry, benefit period, and `pending_credit`.
13. Do not schedule cancellation until all target bookings are complete.
14. After all bookings finish, do not refund on a fixed day count. First sign in to Amex and verify that the Amex statement credit has posted, then start the refund flow. Refund/cancellation submits require an active Hilton site-level batch authorization for that live run.

## Date And Price Rules

- Default to the first Wednesday in the month 8 months after the current month; each retry uses the first Wednesday of the following month.
- Try at most 5 dates.
- Avoid holidays, long weekends, and major event peaks; roll again if pricing looks inflated.
- Select the lowest semi-flex rate, preferring `Honors Discount Semi-Flex`.
- The nightly room price must be under $300 before taxes/fees.

## Browser And Login Rules

- Read `login-flows.md` first and follow its Hilton section for booking login and its American Express section for credit-posting checks.
- First step for every new order: verify Hilton signed-in state.
- Use only visible saved login/autofill; never inspect secrets.
- If the page is stuck for more than 60 seconds, close the current booking flow page and restart from Hilton search.
- Stop for extra identity checks, payment checks, page errors, or ambiguous reservation state.

## Confirmation Scope

Use `safety-confirmations.md` for site-level batch authorization. One Hilton confirmation can cover all eligible bookings in the same live run when site, account, hotel, date-window strategy, room-rate ceiling, card/payment mapping, cancellation rule, and risk envelope are unchanged.

Reconfirm if the site, account, hotel, amount ceiling, payment mapping, date-window strategy, cancellation/refund terms, or material risk changes.

## Payment Method

- Use saved cards only, matching the PointClaw card alias to visible last four.
- When multiple saved cards share the same last four, use expiry to choose the intended card.
- If last four + expiry is still not unique, ask for manual selection.
- Store only last four, expiry, card alias, benefit alias, and reservation alias.

## DB State

After each successful booking:

- Insert a current-period PointClaw snapshot:
  - Aspire: `semiannual`, for example `2026-H2`, limit $200.
  - Surpass / Business Platinum Hilton: `quarterly`, for example `2026-Q3`, limit $50.
  - `status_code`: `pending_credit`.
  - `used_amount_cents`: benefit cap.
  - `remaining_amount_cents`: 0.
- Insert a redemption attempt with `action_state` set to `submitted`.
- Insert a manual note with reservation alias, hotel, rate, date, total, last four, expiry, and Amex statement credit check cadence.
- Do not treat a successful charge as posted issuer credit; wait for Amex tracker or statement-credit evidence.

## Refund After Amex Statement Credit Posts

After all bookings are complete, monitor them before refund.

1. Every 7 days, sign in and check all booked-but-not-refunded Amex cards.
2. Check whether the Amex statement credit has posted. Acceptable evidence includes a statement credit transaction, benefit tracker deduction, or equivalent Amex portal evidence.
3. Once a card's Amex statement credit posts, start the refund flow for that reservation.
4. If more than 21 days have passed since booking and the Amex credit has not posted, report error to the user; do not refund automatically.
5. For cards without posted credit and still within 21 days, keep `pending_credit` and wait for the next 7 days check.

After refund is allowed:

1. Open the Hilton reservation.
2. Verify hotel, date, rate, refund/cancellation policy, refund destination, and refund amount.
3. Stop if the page shows non-refundable, partial refund, or unclear refund method.
4. Before final cancellation/refund, verify that an active site-level batch authorization covers reservation alias scope, refund amount, refund method, and credit-reversal risk.
5. Continue only when the active site-level batch authorization covers the final refund/cancellation details.
6. Record the cancellation attempt and keep monitoring whether the Amex credit reverses.

## Dry Run / Eval

Use:

```bash
python3 <PLUGIN_ROOT>/scripts/churnfu.py hilton-semiflex-dry-run --as-of YYYY-MM-DD
```

Dry run must use mock state only and must not open live Hilton, Amex, Chrome, or network pages. It validates eligible benefit count, date rolling, last four + expiry disambiguation, the 60 seconds stuck-page recovery rule, 7 days Amex check cadence, 21 days report error threshold, and `pending_credit` status.
