# 首次配置默认值

不要给用户展示冗长问卷。先用默认值；只有遇到阻塞或歧义时才提问。

## 默认值

无需询问，直接使用：

- `local_sqlite_db_path`: `<PLUGIN_ROOT>/../pointclaw-data/pointclaw.sqlite`
- `legacy_churnfu_sqlite_db_path`: `<PLUGIN_ROOT>/skills/churn-fu/local/churn-fu.sqlite`
- `local_config_path`: `<PLUGIN_ROOT>/skills/churn-fu/local/config.yaml`
- `timezone`: 系统时区
- `language`: `auto`
- `execution_mode`: `prepare-only`
- `supported_issuers`: `amex`
- `cardpointers_enabled`: `false`
- `credential_policy`: `chrome_autofill_then_user_mfa`
- `portal_handoff_allowed`: `true`
- `followups_enabled`: `true`
- `travel_workflows_enabled`: `true`
- `sensitive_storage`: `aliases_and_card_last_four`
- `amex.pointclaw_owner_label_strategy`: `use_account_owner_display_label`
- `amex.account_alias_strategy`: `use_selected_login_username`，仅用于 legacy BC 和 runtime login labels

## Owner Label 规则

首次设置时不要询问 household alias。用户可能有多个 issuer login。用户选择的 issuer 登录用户名，或者 Chrome autofill 后页面中可见/用户确认的用户名，只作为 runtime login label。

默认配置从 `amex.accounts: []` 开始。如果用户没有提供 Amex owner label，就只在 runtime 使用 Chrome autofill 选中的 Amex 登录用户名作为 label。canonical card 和 benefit state 持久化在 PointClaw 中，通过 `account_owner.display_label`、`account_owner.owner_id` 和 `card_instance.card_id` 映射。

## 只在需要时提问

只问这些运行时问题：

- 如果可见多个 Amex saved login：要使用哪个 username？
- 如果没有可见 Amex saved login：请用户选择 Chrome autofill、手动登录，或提供非敏感 username alias。
- 如果 workflow 涉及 purchase、booking、change、cancel、enroll、redeem、payment：必须 action-time confirmation。
- 如果用户要求从准备阶段进入实际执行：询问是否从 `prepare-only` 切换到 `user-confirmed-execution`。

## 凭证策略

默认使用 Chrome saved-password autofill：

1. 在 Chrome 打开 issuer portal。
2. 使用用户选中的，或与目标 username 匹配的可见 Chrome autofill 建议。
3. 不读取 password、cookie、token、local storage 或 password database secret fields。
4. 遇到 MFA、OTP、CAPTCHA、passkey、CVV 或身份验证，停止并交给用户。
5. 登录后，只把选中的 issuer username 当作 runtime label，除非用户提供其他非敏感 PointClaw owner label。
