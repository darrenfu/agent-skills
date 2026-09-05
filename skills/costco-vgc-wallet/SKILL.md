---
name: costco-vgc-wallet
description: Run user-authorized gift-card churn workflows that start with Staples Visa Virtual Gift Card purchases, fetch Visa VGC details from Gmail, use those VGCs to buy Costco eGift Cards, and add received Costco Digital Shop Cards to Costco Wallet. Use when the user mentions Staples VGC, Visa virtual gift card, Costco eGift card, Costco Shop Card, Costco Wallet, gift-card email monitoring, or tracking VGC balance usage across multiple orders.
---

# Costco VGC Wallet

## Scope

Use this skill for the end-to-end Staples Visa VGC -> Costco eGift Card -> Costco Wallet flow. Treat it as a live financial workflow: maintain a private per-session ledger, verify every amount before submit, and stop on ambiguous, changed, or blocked states.

Never expose full card numbers, CVVs, PINs, gift-card URLs, password values, or payment secrets in user-facing messages. Use tails, order numbers, amounts, and balances instead.

## Confirmation Rules

- Stop for explicit user confirmation before any irreversible final purchase submit unless the current conversation unambiguously pre-authorizes the exact merchant, item, quantity, recipient, payment method, and maximum total.
- Stop for clarification when a site changes the product, amount, fee, quantity limit, payment card, recipient, or delivery email from the expected values.
- Use saved browser autofill and visible logged-in sessions only. Do not inspect password stores or reveal secrets.
- For CVV lookup, use the user's local Notes app path below only as an authorized manual source. Do not store or print the CVV.

## Default Accounts And Anchors

This public export uses configuration placeholders. Resolve them from the user's private local configuration before starting; placeholder text is never a real account or payment destination.

- Staples login: `PRIMARY_EMAIL`; use Chrome autofill for password.
- Staples product URL: `https://www.staples.com/visa-virtual-200-00-gift-card-email-delivery/product_24596403`
- Staples payment method: card ending `PAYMENT_CARD_LAST4`, nickname `PAYMENT_CARD_NICKNAME`.
- PAYMENT_CARD_NICKNAME CVV lookup: open Notes.app, search note named `AUTHORIZED_NOTES_TITLE`, find the `PAYMENT_CARD_NICKNAME PAYMENT_CARD_LAST4` row, and read the three-digit CVV from that row.
- VGC delivery inbox: `PRIMARY_EMAIL`.
- Costco login: `COSTCO_EMAIL`, using saved login where available.
- Costco eGift recipient: `PRIMARY_EMAIL` unless the user overrides it.
- Costco billing cardholder name for VGC payments: `CARDHOLDER_NAME`.

## Session Ledger

Keep a masked operational ledger in the thread or automation state. Record card tails, amounts, order references, and statuses only; do not persist full card numbers, CVVs, PINs, or redeemable links:

```text
purchase_time:
staples_order:
  expected_item:
  quantity:
  total:
  order_number:
vgcs:
  - id: vgc-1
    tail:
    original_amount:
    remaining_amount:
    exp_known: true/false
    cvv_known: true/false
    source_email_time:
    status: unused/partially-used/used
costco_orders:
  - order_number:
    amount:
    vgc_id:
    recipient:
    status: placed/email-received/wallet-added
wallet_adds:
  - costco_card_tail:
    amount_added:
    balance_after:
    source_order:
```

User-facing reports may include counts, order numbers, card tails, amounts used, and wallet balances. Do not include full VGC card data, Costco card numbers, PINs, CVVs, or gift links.

## Workflow

### 1. Buy Staples Visa VGCs

1. Open Staples in Chrome and sign in as `PRIMARY_EMAIL` using Chrome autofill.
2. Go directly to the Staples product URL above.
3. Verify the listing is eligible:
   - The listing is a Visa virtual/eGift card with email delivery.
   - The per-card denomination is exactly `$200.00`.
   - The checkout line items still represent exactly the expected `$200.00` Visa VGC product.
4. If any eligibility check fails, do nothing else. Report `current visa vgc listing ineligible` with the observed reason and exit with error.
5. Buy quantity `4` of the exact `$200.00` card if Staples supports quantity four in one cart. If the site requires separate orders or changes limits/fees, stop and ask the user before changing the purchase structure.
6. Checkout using payment method ending `PAYMENT_CARD_LAST4` / nickname `PAYMENT_CARD_NICKNAME`.
7. Retrieve the CVV from Notes.app:
   - Open Notes.app.
   - Search `AUTHORIZED_NOTES_TITLE`.
   - Find the `PAYMENT_CARD_NICKNAME PAYMENT_CARD_LAST4` row.
   - Read the three-digit CVV visually and enter it into Staples.
8. Before clicking the final `Place order`, verify item, quantity, total, delivery method, account, and payment method. Then follow the Confirmation Rules.
9. If Staples asks for a security code, enter the authorized CVV from the `PAYMENT_CARD_NICKNAME PAYMENT_CARD_LAST4` Notes row and submit only that confirmation.
10. If Staples returns a payment, credit-card-information, security-code, or billing-address verification error, stop the workflow immediately. Do not retry, edit billing details, switch cards, continue to Gmail monitoring, or proceed to Costco. Report the exact page error and the last verified order state.
11. Record the purchase time, order number, quantity, expected card count, and expected total in the private ledger only after a confirmed successful order page or order number appears.

### 2. Fetch Visa VGC Details From Gmail

1. Two hours after the Staples purchase time, open Gmail for `PRIMARY_EMAIL`.
2. Search unread emails after the purchase time with subject containing `You have received a Visa® Virtual Gift Card`.
3. For each matching email:
   - Open the email.
   - Click `View Gift`.
   - Extract the Visa VGC details needed for later checkout: cardholder/name as shown, full card number, expiration date, CVV, and dollar amount.
   - Use payment secrets only within the authorized checkout flow. Keep only masked references and balances in the ledger; do not persist full card numbers, CVVs, or redeemable links.
   - Mark the email/card processed using a non-sensitive identifier such as card tail and amount.
4. If fewer VGC emails arrive than expected, report how many are missing and, if the user requested monitoring, create or continue a timed monitor.

### 3. Buy Costco eGift Cards With VGCs

1. Open Costco in Chrome and sign in as `COSTCO_EMAIL` using saved login where available.
2. Search for and select the `$100` Costco eGift Card / Digital Shop Card.
3. Send each Costco eGift Card to `PRIMARY_EMAIL` unless the user overrides the recipient.
4. Use the ledger to identify the current VGC, then obtain its payment details from the authorized source for this checkout:
   - A `$200` VGC normally funds two `$100` Costco eGift orders.
   - Ignore stale saved card digits left in fields; enter the current VGC details directly.
   - Set cardholder name to `CARDHOLDER_NAME` when required.
   - Do not save the card as a default payment method.
5. Follow the Confirmation Rules before each final Costco order submit unless the user explicitly pre-authorized the batch.
6. After each successful order, record the order number, VGC id, amount used, and remaining VGC balance.
7. Stop on payment decline, OTP, CAPTCHA, persistent `Access Denied`, account mismatch, cart amount mismatch, or any site state that makes the order uncertain.

### 4. Add Costco Digital Shop Cards To Wallet

1. Monitor Gmail for Costco Digital Shop Card emails. Check `PRIMARY_EMAIL` first. Only check other logged-in Gmail accounts, such as `COSTCO_EMAIL` or `ALTERNATE_EMAIL`, if the user has authorized that routing or prior context shows the card emails went there.
2. Search for Costco Digital Shop Card emails or `Access Card Now` links after the Costco order times.
3. For each new card email:
   - Open the card access page.
   - Use `Add to Costco Wallet` when available.
   - Fill card number and PIN into Costco Wallet if the link does not transfer them automatically.
   - Click `Add`.
   - Verify the success message.
   - Immediately read the Costco Wallet Shop Card Balance Total.
   - Report the new balance to the user before processing the next card.
4. Record card tail, amount added, Costco order, and balance after each add.
5. Stop and report the exact blocker after a retry if login, OTP, CAPTCHA, backend errors, or wallet-add failures occur.

## Monitoring

For delayed VGC or Costco card emails, create a recurring automation only when the user asks for monitoring or a delay. Include the current ledger state, purchase/order times, expected remaining email count, and the instruction not to expose secrets. Close extra Chrome/Gmail tabs before handoff when practical.

## Troubleshooting

- If Costco cart or checkout repeatedly shows `Access Denied`, try a normal Chrome window refresh, a fresh tab, and a clean navigation path. If it persists, stop and report likely bot mitigation/session block.
- If Staples reports `Please verify the Credit Card information and Billing Address is correct` or an equivalent payment verification error after CVV entry, treat it as a hard stop. Report the error and leave the checkout page for handoff; do not continue the e2e flow.
- If Gmail search misses expected emails, search by sender, subject fragments, order time window, all mail, promotions, spam, and the other authorized Gmail accounts.
- If autofill selects the wrong card or leaves old digits, clear/re-enter the visible payment fields rather than trusting residual values.
- If a card balance appears inconsistent, stop using that card and report the ledger discrepancy.
