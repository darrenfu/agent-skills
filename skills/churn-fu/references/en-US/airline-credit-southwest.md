# Airline Credit Southwest Reference

Use this only after SQLite shows a ready action candidate for an airline credit benefit.

## Preconditions

- Benefit usage has current-period remaining value or user accepted uncertainty.
- Payment method alias is mapped to card alias.
- Travel workflows are enabled.
- Execution mode is `user-confirmed-execution`.
- Chrome access is available for the airline site, or the user is ready to complete login manually.
- The user understands issuer credits may post late or reverse after refunds.

## Credential Default

Read `login-flows.md` first and follow the Southwest section for Chrome autofill and login handoff.

1. Open the airline site in Chrome.
2. Use only the visible user-approved Chrome password-manager path described in `login-flows.md`.
3. Do not inspect password values, cookies, tokens, local storage, or password database secret fields.
4. Stop for MFA, CAPTCHA, passkey, identity verification, or payment verification.
5. If autofill is unavailable, ask the user to sign in manually and say when ready.

## Default Route And Date Strategy

Default search route:

- `HNL -> OGG`
- Treat this as an anonymized operational default: a short Honolulu-origin Southwest route that often exposes low-cost, changeable options.

If that route is unavailable or pricing is unsuitable, use another low-cost Southwest route only after recording why the default failed.

Default date rule:

- Choose a date about five months after the current date.
- Avoid Thanksgiving week.
- Avoid Christmas through New Year.
- Avoid major holiday weekends.
- Avoid dates adjacent to major holidays.
- Avoid dates too close to the current date.

## Amount Tracking Model

Before booking, compute:

- `target_remaining_credit`: current-period remaining benefit amount from SQLite.
- `target_card_id`: PointClaw `card_instance.card_id` tied to the benefit.
- `target_card_benefit_id`: PointClaw `card_benefit.card_benefit_id`.
- `payment_method_alias`: airline saved payment alias mapped to the PointClaw card id or visible last four.
- `cumulative_candidate_charges`: sum of purchase and change charges made during this workflow for the candidate.
- `remaining_gap`: `target_remaining_credit - cumulative_candidate_charges`.

After every confirmed purchase or change:

1. Record the action in session output; persist only if PointClaw has a workflow table for this action type.
2. Recompute `cumulative_candidate_charges`.
3. If `cumulative_candidate_charges >= target_remaining_credit`, exit the purchase/change loop.
4. If still below target, continue to the change flow and look for a reasonable additional amount, with an operational preference for each change charge to be close to `$70`.

Do not mark the benefit as used merely because the charge was made. Mark it as `pending_credit` until issuer evidence verifies the credit or usage tracker update.

## Fare Refundability Rules

The Southwest workflow default is to create a cash-refundable ticket, not future flight credit.

- Only select Southwest fares officially marked refundable: `Choice Preferred` or `Choice Extra`.
- Do not select `Basic` or `Choice`, even when they are cheaper, cancellable, changeable, or eligible for flight credit.
- Do not treat `cancellable`, `changeable`, `transferable flight credit`, or `no cancel fees` as equivalent to `refund to original form of payment`.
- If any funds in an existing reservation came from `Basic`, `Choice`, flight credit, voucher, gift card, or another non-cash-refundable source, do not assume upgrading to a refundable fare makes those funds refundable to the original card.
- Before booking, changing, or canceling, verify the refund destination for every part of the amount. If any part will become flight credit, travel credit, voucher, or is unclear, stop and ask the user.

## Flow

## Confirmation Scope

Before the first Southwest transaction submit in a live run, obtain a site-level batch authorization using `safety-confirmations.md`. The authorization must cover the airline site, account, eligible reservation/card/payment scope, per-transaction cap, total batch cap, route/date/fare constraints, refundability requirement, and issuer-credit reversal risk.

After that, do not ask per-card or per-reservation confirmation for purchase, change, or cancellation actions that stay inside the confirmed Southwest envelope. Reconfirm if the site, account, amount ceiling, payment mapping, route/date/fare rules, refundability, or risk envelope changes.

### 1. Candidate Load

1. Query SQLite for the open airline credit candidate.
2. Verify benefit type is airline credit or equivalent.
3. Verify usage status and remaining amount.
4. Verify payment method alias maps to the candidate PointClaw `card_instance.card_id` or visible last four.
5. If mapping is missing or ambiguous, stop and ask the user to map the saved airline payment method to the card.

### 2. Airline Login

1. Open Southwest or the configured airline site in Chrome.
2. Attempt Chrome autofill for the saved airline login.
3. If the login form requires user action, hand off for login/MFA and wait.
4. Verify account context after login through visible account identity or user confirmation.

### 3. Initial Booking

1. Search `HNL -> OGG` by default.
2. Use a date about five months out and outside holiday windows.
3. Select only `Choice Preferred` or `Choice Extra`; if only `Basic` or `Choice` has suitable pricing, stop and report that no compliant refundable option is available.
4. Verify on the page or in official fare text that the fare supports refund to the original form of payment.
5. Avoid optional paid add-ons.
6. Decline optional credit-card ads, promotional financing offers, or upsells. Do not accept paid add-ons without user confirmation.
7. Select the saved payment method alias mapped to the target card alias.
8. Before final purchase/review, verify that an active site-level batch authorization covers this purchase. If not, stop and request it.
9. The site-level batch authorization must include:
   - card alias
   - payment method alias
   - per-transaction amount and total batch ceiling
   - route
   - date window
   - flight time
   - fare type
   - refundability: must clearly be refund to original form of payment
   - target remaining credit
   - expected cumulative charges after purchase
10. Purchase only when the active site-level batch authorization covers the final review details.
11. Record reservation alias, charge amount, route, date, fare type, refundability, payment method alias, and status `submitted`.

### 4. Check Target Coverage

1. Recompute `cumulative_candidate_charges`.
2. If cumulative charges meet or exceed `target_remaining_credit`, stop making new charges.
3. If cumulative charges are below target, calculate `remaining_gap`.
4. Continue to the change flow only if the user still wants to pursue the remaining gap.

### 5. Change / Fare Difference Loop

Repeat until cumulative charges meet target or the user stops:

1. Open the reservation change flow.
2. Search the same route/date or a nearby eligible itinerary if needed.
3. Select only `Choice Preferred` or `Choice Extra`; do not change into `Basic` or `Choice`.
4. Prefer an additional fare difference close to `$70` for each change when feasible, but refundability has higher priority than the price target.
5. If multiple refundable options are near `$70`, choose the one that best covers the `remaining_gap` with the least overage.
6. Avoid large overage unless the user explicitly accepts it.
7. Before final change confirmation, verify that the active site-level batch authorization covers this change. If not, stop and request a new authorization.
8. The site-level batch authorization must cover:
   - reservation alias
   - additional amount due
   - distance from the `$70` per-change target
   - new cumulative candidate charges
   - remaining gap after change
   - route/date/flight/fare type
   - refundability: must clearly be refund to original form of payment; if the reservation contains historical non-refundable funds, list that risk separately
   - payment method alias
   - risk that issuer credit may not post or may reverse
9. Confirm change only when the active site-level batch authorization covers the final change details.
10. Record the change in session output; persist only if PointClaw has a workflow table for this action type.
11. Recompute `cumulative_candidate_charges`.
12. Exit the loop if target is satisfied.

### 6. Exit Criteria

Exit the booking/change loop when any of these is true:

- `cumulative_candidate_charges >= target_remaining_credit`
- no reasonable low-overage change exists
- payment method mapping becomes ambiguous
- the user declines further charges
- the airline site blocks progress
- the session reaches a final side-effect step without active site-level batch authorization

### 7. Cancellation Scheduling

If a cancellable reservation was created:

1. Schedule a follow-up for the next day at 11:00 in the configured/system timezone, unless the user gives another time.
2. Store:
   - reservation alias
   - route
   - date
   - fare type
   - total candidate charges
   - refund method expectation: full refund to original form of payment
   - non-refundable funds check: none expected
   - instruction to stop before final cancellation
3. Verify timezone handling before claiming the follow-up is scheduled.

### 8. Cancellation / Refund

At cancellation time:

1. Open the airline cancellation flow.
2. Locate the reservation by alias or user-provided confirmation.
3. Verify passenger alias, route, date, fare type, refund method, and refund amount.
4. Require the full refund method to be refund to original form of payment.
5. If the site only offers travel credit, flight credit, voucher, points redeposit, or only a partial refund to the original form of payment, stop and ask the user. Do not cancel.
6. Before final cancellation, verify that the active site-level batch authorization covers this cancellation. If not, stop and request a new authorization.
7. The site-level batch authorization must cover:
   - reservation alias
   - route/date
   - refund amount
   - refund method: full original form of payment
   - flight credit amount: must be `$0` or none
   - risk of issuer credit reversal
8. Cancel only when the active site-level batch authorization covers the final cancellation details.
9. Record cancellation and refund request in session output; persist only if PointClaw has a workflow table for this action type.
10. Keep monitoring issuer credit posting and reversal status.

## Risk

Issuer credits may post late or reverse after refunds. Never mark pending credit as completed usage.
