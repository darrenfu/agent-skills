# 安全确认

所有外部副作用前都使用本文件。

## Blocker types

统一使用这些 blocker types：

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

涉及 make transaction 的 workflow，在同一个 live run 里，每个网站第一次 final submit 前只要求 one confirmation per site per live run。这次确认形成 site-level batch authorization。

site-level batch authorization 生效后，只要下一笔 transaction 仍在确认范围内，Do not require per-card or per-reservation confirmation。

Reconfirm if the site, account, amount ceiling, payment mapping, or material transaction terms change。Material transaction terms 包括 merchant/site、owner/account、eligible cards、payment aliases、action type、product/hotel/route、date window、refundability、quantity、per-transaction cap、total batch cap、expected result 或 risk。

## 没有授权时必须停止在最终按钮前

- purchase
- booking
- reservation change
- cancellation
- refund request
- enrollment
- unenrollment
- redemption
- payment submission

## 确认内容

要求用户确认 site-level batch authorization：

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

只有用户明确给出 site-level confirmation 后才能继续。当 amount、account、card、payment method、reservation details 或其他 material transaction terms 发生变化时，不接受模糊确认。

## Blocker report

| Field | Value |
|---|---|
| Area | `<AREA>` |
| Alias | `<ALIAS>` |
| Blocker | `<BLOCKER>` |
| Required user action | `<ACTION>` |
| Severity | `<SEVERITY>` |
