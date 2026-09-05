# Safety Confirmations Reference

Use before all external side effects.

## Blocker Types

Use these blocker types consistently:

- `login_required`
- `otp_required`
- `captcha_required`
- `wrong_account`
- `portal_unavailable`
- `terms_unclear`
- `usage_unknown`
- `payment_mapping_unclear`
- `final_confirmation_required`
- `credit_not_posted`
- `credit_reversed`
- `user_decision_required`

## Site-Level Batch Authorization

For transaction-making workflows, ask one confirmation per site per live run before the first final submit on that site. This creates a site-level batch authorization.

Do not require per-card or per-reservation confirmation once a site-level batch authorization is active and the next transaction stays inside the confirmed envelope.

Reconfirm if the site, account, amount ceiling, payment mapping, or material transaction terms change. Material transaction terms include merchant/site, owner/account, eligible cards, payment aliases, action type, product/hotel/route, date window, refundability, quantity, per-transaction cap, total batch cap, expected result, or risk.

## Stop Before Authorization Exists

- purchase
- booking
- reservation change
- cancellation
- refund request
- enrollment
- unenrollment
- redemption
- payment submission

## Confirmation Payload

Ask the user to confirm the site-level batch authorization:

| Field | Value |
|---|---|
| Site | `<SITE_ALIAS>` |
| Owner | `<POINTCLAW_OWNER_LABEL_OR_ID>` |
| Cards | `<POINTCLAW_CARD_IDS_OR_CARD_SCOPE>` |
| Payments | `<PAYMENT_METHOD_ALIASES>` |
| Benefits | `<POINTCLAW_CARD_BENEFIT_IDS_OR_SCOPE>` |
| Actions | `<AUTHORIZED_ACTIONS>` |
| Amount ceiling | `<PER_TRANSACTION_AND_BATCH_LIMITS>` |
| Material terms | `<PRODUCT_HOTEL_ROUTE_DATE_REFUNDABILITY_QUANTITY_SCOPE>` |
| Expected result | `<EXPECTED_RESULT>` |
| Risk | `<RISK_SUMMARY>` |

Proceed only after explicit site-level confirmation. Do not accept ambiguous confirmation when amount, account, card, payment method, reservation details, or other material transaction terms changed.

## Blocker Report

| Field | Value |
|---|---|
| Area | `<AREA>` |
| Alias | `<ALIAS>` |
| Blocker | `<BLOCKER>` |
| Required user action | `<ACTION>` |
| Severity | `<SEVERITY>` |
