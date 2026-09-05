# First-Run Config Defaults

Do not ask a long setup questionnaire. Use defaults first, then ask only when the workflow is blocked or ambiguous.

## Default Setup Values

Use these defaults without asking:

- `local_sqlite_db_path`: `<PLUGIN_ROOT>/../pointclaw-data/pointclaw.sqlite`
- `legacy_churnfu_sqlite_db_path`: `<PLUGIN_ROOT>/skills/churn-fu/local/churn-fu.sqlite`
- `local_config_path`: `<PLUGIN_ROOT>/skills/churn-fu/local/config.yaml`
- `timezone`: system timezone from the machine
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
- `amex.account_alias_strategy`: `use_selected_login_username` for legacy BC and runtime login labels only

## Owner Label Rule

Do not ask for a household alias during first setup. Users may have multiple issuer logins. Treat issuer usernames selected by the user or visible after Chrome autofill as runtime login labels only.

Default config starts with `amex.accounts: []`. If the user does not provide an Amex owner label, use the Amex login username selected through Chrome autofill as a runtime label only. Persist canonical card and benefit state in PointClaw, mapped through `account_owner.display_label`, `account_owner.owner_id`, and `card_instance.card_id`.

## Ask Only When Needed

Ask only these runtime questions:

- If multiple Amex saved logins are visible: which username should be used?
- If no Amex saved login is visible: ask the user to select Chrome autofill, sign in manually, or provide a non-sensitive username alias.
- If the workflow requires purchase, booking, change, cancellation, enrollment, redemption, or payment: ask action-time confirmation.
- If the user requests execution beyond preparation: ask whether to switch from `prepare-only` to `user-confirmed-execution`.

## Credential Policy

Default to Chrome saved-password autofill:

1. Open the issuer portal in Chrome.
2. Use the visible Chrome autofill suggestion selected by the user or matching the intended username.
3. Do not inspect passwords, cookies, tokens, local storage, or password database secret fields.
4. Stop for MFA, OTP, CAPTCHA, passkey, CVV, or identity verification.
5. After login, use the selected issuer username only as a runtime label unless the user provides a different non-sensitive PointClaw owner label.
