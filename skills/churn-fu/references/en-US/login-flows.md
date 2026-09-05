# Login Flows

Use this shared reference before any browser login or portal handoff in Churn Fu workflows. It covers the repo web surfaces that may require Chrome state or visible user login help: American Express, Hilton, Southwest, Staples, Costco, Gmail, Doctor of Credit, Visa VGC access pages, and an issuer travel portal.

## Universal Chrome Autofill Method

1. Open a fresh normal Chrome window unless the user explicitly asks to reuse an existing authenticated session.
2. If the site is already signed in, verify the visible account context before doing any portal work.
3. If a login form is visible, distinguish a username/form-history suggestion from a Chrome password-manager credential. A username-only or form-history row can fill a login ID without selecting the saved password.
4. Select the visible Chrome password-manager credential row approved by the user. It is often exposed from the password field, a key icon, or the password-manager suggestion UI.
5. Verify only non-secret signals: the expected runtime login label is visible and the password field is non-empty or browser-autofilled. Do not inspect password values, reveal passwords, read cookies, export tokens, or query password-manager secret fields.
6. Do not press Enter while the username field is focused just to select a suggestion; some sites submit the form and create an empty-password error.
7. If the username changes but the password field remains empty, the password-manager credential was not selected. Ask the user to choose the credential from the password field or sign in manually.
8. If multiple visible saved credentials could match, ask the user for manual selection. Do not infer from username text alone.
9. Stop on MFA, OTP, CAPTCHA, passkey, CVV, identity verification, payment verification, wrong account, or any login mismatch.
10. After login, verify the account context by visible account label, expected card/reservation/order state, or user confirmation before continuing.

## Site Flows

### American Express

- Open the Amex login or portal page only after the workflow allows portal handoff.
- Amex remembered User ID or browser form history is not enough. Use the Chrome password-manager credential path and verify that the password field is non-empty before submitting.
- If several Amex credentials are visible for the same origin, ask the user to pick the intended credential from Chrome UI.
- After login, use the selected login only as a runtime label unless the user provides a separate non-sensitive PointClaw owner alias.
- Stop on wrong account, MFA, CAPTCHA, passkey, CVV, identity verification, or a password field that stays empty after username selection.

### Hilton

- Start every Hilton booking order by checking whether Hilton is already signed in.
- If not signed in, use the visible Chrome password-manager credential path, then return to the hotel search or reservation page after login.
- For semi-flex credit workflows, verify the account context before selecting dates, rooms, or payment cards.
- If a booking page is stuck for more than 60 seconds, close the current booking-flow tab and restart from Hilton search.
- Stop on MFA, CAPTCHA, wrong account, payment verification, page error, or ambiguous reservation state.

### Southwest

- Open Southwest or the configured airline site in Chrome and verify the saved airline account context before booking, changing, or cancelling.
- Use the shared Chrome password-manager credential method; do not treat a username/form-history suggestion as a completed login.
- Stop on MFA, CAPTCHA, payment verification, wrong account, or any refundability ambiguity.
- Do not proceed to purchase, change, or cancellation final submit unless a workflow-specific site-level batch authorization is active.

### Staples

- Open Staples with the configured account and verify the signed-in account before cart or checkout work.
- Use visible Chrome autofill only through the shared password-manager method.
- Stop on CAPTCHA, OTP, wrong account, login mismatch, unexpected product, fee, quantity, payment method, or ambiguous order state.
- Let the user handle CVV and final purchase authorization. A site-level batch authorization can cover multiple Staples submits in the same live run.

### Costco

- Open Costco with the configured account and verify the account before Digital Shop Card checkout or Wallet actions.
- Use visible Chrome autofill only through the shared password-manager method.
- Stop on CAPTCHA, OTP, wrong account, access-denied checkout loops, wallet login blockers, or ambiguous order/wallet state.
- Never save a Visa VGC as a default payment method.

### Gmail

- Prefer an existing authorized Chrome/Gmail session. Verify the mailbox/account label before reading or searching.
- If Google reauth is required, stop for the user to complete it; do not inspect passwords, cookies, tokens, or recovery data.
- Do not switch mailboxes unless the user explicitly asks or the workflow's configured routing says the target email may be elsewhere.
- Keep searches scoped to the workflow evidence needed.

### Doctor of Credit

- Doctor of Credit is treated as a public feed/search source, not a credentialed login surface.
- If the feed or post is unavailable, use the workflow's feed retry policy and record the blocker. Do not invent a login workaround.

### Visa VGC Access Pages

- Visa VGC access pages are usually reached through authorized email links or gift-card access URLs, not Chrome password-manager login.
- Do not store, print, or expose full card numbers, PINs, CVVs, or gift-card URLs in committed files or final reports.
- If an access page, challenge, image, or OCR result is unclear after the allowed retry, stop with the workflow blocker.

### Issuer Travel Portal

- Follow the issuer-specific login section first. For Amex Travel, use the American Express flow above.
- Verify the visible issuer account and eligible card context before booking, changing, or cancelling.
- Stop on MFA, CAPTCHA, wrong account, CVV, identity verification, or final booking/payment/cancellation submit not covered by an active site-level batch authorization.

## Recording Rules

- Store only non-sensitive aliases, visible last four digits, expiry when needed for saved-card disambiguation, reservation/order aliases, and blocker codes.
- Do not store passwords, OTPs, cookies, tokens, full card numbers, CVVs, PINs, full reservation confirmations, or private gift-card URLs.
