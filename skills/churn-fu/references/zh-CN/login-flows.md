# 登录流程

任何 browser login 或 portal handoff 前，先读取这个共享 reference。它覆盖 repo 里可能需要 Chrome state 或用户可见登录选择的网站面：American Express、Hilton、Southwest、Staples、Costco、Gmail、Doctor of Credit、Visa VGC access pages，以及 issuer travel portal。

## 通用 Chrome Autofill 方法

1. 默认打开 fresh normal Chrome window，除非用户明确要求复用已有 authenticated session。
2. 如果网站已经登录，先验证可见 account context，再做 portal 操作。
3. 登录表单出现时，先区分 username/form-history suggestion 和 Chrome password-manager credential。username-only 或 form-history row 可能只填 login ID，不会选择 saved password。
4. 选择用户批准的可见 Chrome password-manager credential 行。它通常从 password field、key icon 或 password-manager suggestion UI 触发。
5. 只验证非敏感信号：目标 runtime login label 可见，且 password field is non-empty 或 browser-autofilled。do not inspect password，不展示 password，不读 cookies，不导出 tokens，不查询 password-manager secret fields。
6. Do not press Enter while username field is focused 来选择建议；有些网站会直接 submit，造成空 password error。
7. 如果 username 变了但 password field 仍为空，说明没有选中 password-manager credential。让用户从 password field 选择 credential，或手动 sign in。
8. 如果多条可见 saved credentials 都可能匹配，ask for manual selection。不要只凭 username text 推断。
9. 遇到 MFA、OTP、CAPTCHA、passkey、CVV、identity verification、payment verification、wrong account 或 login mismatch，停止。
10. 登录后用可见 account label、预期 card/reservation/order state 或用户确认来验证 account context，再继续。

## 站点流程

### American Express

- 只有 workflow 允许 portal handoff 后才打开 Amex login 或 portal。
- Amex remembered User ID 或 browser form history 不够。必须走 Chrome password-manager credential 路径，并在 submit 前确认 password field is non-empty。
- 如果同一 origin 下有多条 Amex credential 可见，让用户从 Chrome UI 选择目标 credential。
- 登录后，只把选中的 login 当作 runtime label，除非用户提供独立的非敏感 PointClaw owner alias。
- 遇到 wrong account、MFA、CAPTCHA、passkey、CVV、identity verification，或 username 选择后 password field 仍为空，停止。

### Hilton

- 每个 Hilton booking order 第一步都是检查是否已经 signed in。
- 未登录时，使用可见 Chrome password-manager credential 路径；登录后回到 hotel search 或 reservation 页面。
- semi-flex credit workflow 中，必须先验证 account context，再选日期、房型或 payment card。
- booking 页面卡住超过 60 seconds 时，关闭当前 booking-flow tab，从 Hilton search 重新开始。
- 遇到 MFA、CAPTCHA、wrong account、payment verification、page error 或 reservation state 不明确，停止。

### Southwest

- 在 Chrome 打开 Southwest 或配置的 airline site，booking、change、cancel 前先验证 saved airline account context。
- 使用共享 Chrome password-manager credential 方法；不要把 username/form-history suggestion 当作已完成登录。
- 遇到 MFA、CAPTCHA、payment verification、wrong account 或 refundability 不明确，停止。
- 没有 workflow-specific site-level batch authorization，不进入 purchase、change 或 cancellation final submit。

### Staples

- 用配置的 account 打开 Staples，并在 cart 或 checkout 前验证 signed-in account。
- 只通过共享 password-manager 方法使用 visible Chrome autofill。
- 遇到 CAPTCHA、OTP、wrong account、login mismatch、非预期 product、fee、quantity、payment method 或 order state 不明确，停止。
- CVV 和最终 purchase authorization 由用户处理。同一 live run 中，site-level batch authorization 可以覆盖多笔 Staples submit。

### Costco

- 用配置的 account 打开 Costco，并在 Digital Shop Card checkout 或 Wallet 操作前验证账号。
- 只通过共享 password-manager 方法使用 visible Chrome autofill。
- 遇到 CAPTCHA、OTP、wrong account、access-denied checkout loop、wallet login blocker 或 order/wallet state 不明确，停止。
- 不要把 Visa VGC 保存成 default payment method。

### Gmail

- 优先使用已有 authorized Chrome/Gmail session。读取或搜索前验证 mailbox/account label。
- 如果 Google 要求 reauth，停止让用户完成；不要读取 passwords、cookies、tokens 或 recovery data。
- 除非用户明确要求，或 workflow routing 指出目标邮件可能在其他 inbox，不要切换 mailbox。
- 搜索范围只限 workflow 所需 evidence。

### Doctor of Credit

- Doctor of Credit 作为 public feed/search source，不作为需要 credential 的 login surface。
- 如果 feed 或 post 不可用，走 workflow 的 feed retry policy 并记录 blocker。不要编造 login workaround。

### Visa VGC Access Pages

- Visa VGC access pages 通常通过授权 email link 或 gift-card access URL 进入，不是 Chrome password-manager login。
- 不要在 commit 文件或最终报告里存储、打印或暴露 full card numbers、PINs、CVVs 或 gift-card URLs。
- access page、challenge、image 或 OCR 结果在允许 retry 后仍不清楚时，按 workflow blocker 停止。

### Issuer Travel Portal

- 先遵循 issuer-specific login section。Amex Travel 使用上面的 American Express 流程。
- booking、change 或 cancellation 前，验证可见 issuer account 和 eligible card context。
- 遇到 MFA、CAPTCHA、wrong account、CVV、identity verification，或未被 active site-level batch authorization 覆盖的最终 booking/payment/cancellation submit，停止。

## 记录规则

- 只记录非敏感 aliases、visible last four、用于 saved-card 消歧的 expiry、reservation/order aliases 和 blocker codes。
- 不记录 passwords、OTPs、cookies、tokens、full card numbers、CVVs、PINs、full reservation confirmations 或 private gift-card URLs。
