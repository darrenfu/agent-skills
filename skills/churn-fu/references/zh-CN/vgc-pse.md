# Visa VGC 到 PSE

激活一张已授权的 Visa Virtual Account，把全部可用余额作为 one-time payment 付入已登录的 Puget Sound Energy 账户，然后从 PSE wallet 删除临时保存的卡。

## 必要输入

- 已授权的 ActivationSpot 或同类 VGC access URL。
- 目标 PSE account context，最好已经登录。
- runtime 可用且经用户授权的注册资料：first name、last name、email、美国地址、ZIP 和 phone。
- 覆盖 activation、立即支付全部余额、成功取得 receipt 后删除 saved payment method 的 scope。

不得存储或报告 full card number、CVV、PIN、private access URL 或 full confirmation number。遵守 `SECURITY.md`：CAPTCHA、CVV prompt，以及 repository/runtime policy 强制要求的 final action-time confirmation 由用户处理。

## Authorization scope

把完整 workflow 请求视为一次 Churn Fu site-level batch authorization，覆盖 VGC registration、仅在 runtime 读取 balance/card identity、传给 PSE/Paymentus、临时创建 wallet card、按精确余额付款和删除 wallet card。

不要为预期的 account credit、duplicate payment、AutoPay、wallet add 或 wallet removal 增加 Churn Fu 自己的确认。如果 repository policy、host browser 或 Codex runtime 强制要求 confirmation 或 user handoff，只执行最低限度的必要步骤，不重复询问。

只有 PSE account 变化、amount 不等于 VGC balance、出现 fee、payment date 不是今天、selected payment method 不是目标 VGC，或 warning 显示实质不同后果时才重新确认。

## 操作步骤

1. 读取 `login-flows.md` 和 `safety-confirmations.md`；使用 Chrome 复用已登录 PSE session。
2. 打开已授权 VGC URL，填写获准的注册资料，不输出敏感值。
3. CAPTCHA、MFA、identity verification、CVV entry 或 policy 要求的 challenge 交给用户处理。
4. 激活后，live handoff 所需卡片资料只保留在临时 runtime。不得输出包含未遮盖卡资料的 DOM snapshot、screenshot、log、file 或 report。
5. workflow 决策和报告只保留 balance、expiry 和 last four。
6. 打开 PSE One-time payment，验证可见 target account。用户明确授权时，忽略 PSE 现有 balance，按 VGC 精确余额付款。
7. Warm Home Fund 设为零，payment date 设为 now。把 VGC 添加为临时 Credit payment method；CVV prompt 出现时由用户输入。
8. 按 last four 选择新卡并继续。关于 account credit、similar payment 或 AutoPay 的预期 warning 保持在 workflow authorization 内；出现 fee、amount/date/account 变化或其他实质影响时停止。
9. 在 Review and Confirm 核对 account、last four、date 和 exact amount。只有适用的 action-time authorization 生效时才提交，并等待 Payment Receipt。
10. 金额和 last four 符合预期的可见 receipt 是权威成功信号；不得报告 full confirmation number。
11. 打开 My wallet，按 last four 和 expiry 定位该卡，在适用的 action-time authorization 下删除。
12. 删除时关于 associated AutoPay schedule 可能被删除，或 future scheduled payment 仍可能处理的通用 warning 保持在 scope 内。页面明确指出意外 schedule 或其他 card/account 时停止。
13. 报告完成前，验证 wallet 中已不再出现该 last four。

## Blockers

遇到 CAPTCHA/MFA、wrong PSE account、balance 不清楚、card decline、fee、amount/date 变化、wallet card 有歧义、缺少 receipt、submit 结果不明或删除失败时停止。financial submit 结果不明时不得重试。

## 完成报告

只报告 VGC last four、支付金额、target PSE account alias 或 last four、已看到 receipt、已验证 wallet card 被删除。
