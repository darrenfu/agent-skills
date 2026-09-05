# Visa VGC to PSE

Activate one authorized Visa Virtual Account, apply its full available balance as a one-time payment to an already authenticated Puget Sound Energy account, and remove the temporary card from the PSE wallet.

## Required inputs

- Authorized ActivationSpot or equivalent VGC access URL.
- Target PSE account context, preferably already signed in.
- User-authorized registration profile available at runtime: first and last name, email, U.S. address, ZIP code, and phone.
- Scope covering activation, full-balance payment now, and removal of the saved payment method after a successful receipt.

Never store or report the full card number, CVV, PIN, private access URL, or full confirmation number. Follow `SECURITY.md`: the user handles CAPTCHA, CVV prompts, and any final action-time confirmation required by repository or runtime policy.

## Authorization scope

Treat the complete workflow request as one Churn Fu site-level batch authorization covering VGC registration, runtime-only reading of balance and card identity, transmission to PSE/Paymentus, temporary wallet creation, exact-balance payment, and wallet removal.

Do not add Churn Fu-specific confirmations for expected account-credit, duplicate-payment, AutoPay, wallet-add, or wallet-removal transitions. If repository policy, the host browser, or the Codex runtime requires a confirmation or user handoff, request only the minimum required step and do not duplicate it.

Reconfirm when the PSE account changes, the amount differs from the VGC balance, a fee appears, the payment date is not today, the selected payment method is not the intended VGC, or a warning identifies a materially different consequence.

## Procedure

1. Read `login-flows.md` and `safety-confirmations.md`; use Chrome for the authenticated PSE session.
2. Open the authorized VGC URL and fill the approved registration profile without printing sensitive values.
3. Stop for user handling of CAPTCHA, MFA, identity verification, CVV entry, or any challenge required by policy.
4. After activation, keep any card data needed for the live handoff ephemeral. Never emit a DOM snapshot, screenshot, log, file, or report containing unmasked card data.
5. Retain only balance, expiry, and last four for workflow decisions and reporting.
6. Open PSE One-time payment and verify the visible target account. When explicitly authorized, ignore the existing PSE balance and pay the exact VGC balance.
7. Set Warm Home Fund to zero and payment date to now. Add the VGC as a temporary Credit payment method, with user handling CVV entry when prompted.
8. Select the new card by last four and continue. Expected warnings about account credit, similar payment, or AutoPay remain inside the workflow authorization unless they expose a fee, changed amount/date/account, or different material effect.
9. On Review and Confirm, verify account, last four, date, and exact amount. Submit only under the applicable action-time authorization and wait for Payment Receipt.
10. Treat a visible receipt with the expected amount and last four as authoritative success; do not report the full confirmation number.
11. Open My wallet, locate the card by last four and expiry, then remove it under the applicable action-time authorization.
12. Expected generic warnings that associated AutoPay schedules may be removed or future scheduled payments may still process remain inside scope. Stop if the page identifies an actual unexpected schedule or another card/account.
13. Verify the card last four no longer appears before reporting completion.

## Blockers

Stop for CAPTCHA/MFA, wrong PSE account, unclear balance, card decline, fee, changed amount/date, ambiguous wallet card, missing receipt, unknown submit outcome, or failed removal. Never retry a financial submit when its outcome is unknown.

## Completion report

Report only VGC last four, amount paid, target PSE account alias or last four, receipt observed, and wallet removal verified.
